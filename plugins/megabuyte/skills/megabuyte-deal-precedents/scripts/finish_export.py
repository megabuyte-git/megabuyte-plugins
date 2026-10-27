"""Final step for every Word, PowerPoint and Excel export: fonts, fallback hints and bullets.

Usage: python <skill_dir>/scripts/finish_export.py <file.docx|file.pptx> [more files...]
.docx: Lato is embedded, with Arial named as the fallback (verified in Word without Lato installed).
.pptx: fonts are NOT embedded (PowerPoint rejects them). Every Lato reference, including the theme,
       gets the same sans-serif hint (panose, pitchFamily 34) so Office substitutes an Arial-class
       font consistently; character bullets are set to the brand pink in Arial.
.xlsx: Excel cannot embed fonts. Every font, including the base Normal style, is set to Lato with the
       sans-serif family hint (2), and theme-font links are removed, so substitution is consistent. Run it last, after the file is written (and, for .pptx,
after any theme step). Excel (.xlsx) cannot embed fonts, so this script skips it.

Lato is licensed under the SIL Open Font License (assets/fonts/OFL.txt), which permits
embedding; its OS/2 fsType is 0 (installable)."""
import os, re, sys, uuid, zipfile, shutil, tempfile

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(SKILL, "assets", "fonts")
# family -> {style: file}
FAMILIES = {
    "Lato": {"Regular": "Lato-Regular.ttf", "Bold": "Lato-Bold.ttf", "Italic": "Lato-Italic.ttf"},
    "Lato Black": {"Regular": "Lato-Black.ttf"},
}
PANOSE = {"Lato": "020F0502020204030203", "Lato Black": "020F0A02020204030203"}
R_FONT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/font"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def _read(z, name):
    return z.read(name).decode("utf-8")


def _rewrite(path, changes, additions):
    """Copy the zip, replacing members in `changes` and adding members in `additions`."""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(path)[1]).name
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = changes.get(item.filename)
            zout.writestr(item, data if data is not None else zin.read(item.filename))
        for name, data in additions.items():
            zout.writestr(name, data)
    shutil.move(tmp, path)


def _add_default(ct, ext, ctype):
    if f'Extension="{ext}"' in ct:
        return ct
    return ct.replace("<Default ", f'<Default Extension="{ext}" ContentType="{ctype}"/><Default ', 1)


def _open_root(xml, tag):
    """Turn a self-closing root element (<x .../>) into <x ...></x> so children can be appended."""
    m = re.search(rf"<{re.escape(tag)}(\s[^>]*)?/>", xml)
    if m:
        attrs = m.group(1) or ""
        xml = xml[:m.start()] + f"<{tag}{attrs}></{tag}>" + xml[m.end():]
    return xml


def _next_rid(rels):
    ids = [int(x) for x in re.findall(r'Id="rId(\d+)"', rels)] or [0]
    return max(ids) + 1


# ---------------------------------------------------------------- Word
def _obfuscate(data, key_guid):
    key = bytes.fromhex(key_guid.strip("{}").replace("-", ""))[::-1]
    head = bytes(b ^ key[i % 16] for i, b in enumerate(data[:32]))
    return head + data[32:]


def embed_docx(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        ft = _read(z, "word/fontTable.xml")
        settings = _read(z, "word/settings.xml")
        ct = _read(z, "[Content_Types].xml")
        rels_name = "word/_rels/fontTable.xml.rels"
        rels = _read(z, rels_name) if rels_name in names else (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>')
    if "w:embedRegular" in ft:
        return "already embedded"
    rels = _open_root(rels, "Relationships")
    ft = _open_root(ft, "w:fonts")
    if 'xmlns:r=' not in ft[:600]:
        ft = ft.replace("<w:fonts ", f'<w:fonts xmlns:r="{NS_R}" ', 1)
    additions, n = {}, _next_rid(rels)
    for fam, styles in FAMILIES.items():
        embeds = []
        for style, fname in styles.items():
            key = "{" + str(uuid.uuid4()).upper() + "}"
            part = f"fonts/font{n}.odttf"
            with open(os.path.join(FONTS, fname), "rb") as fh:
                additions["word/" + part] = _obfuscate(fh.read(), key)
            rels = rels.replace("</Relationships>",
                                f'<Relationship Id="rId{n}" Type="{R_FONT}" Target="{part}"/></Relationships>')
            embeds.append(f'<w:embed{style} r:id="rId{n}" w:fontKey="{key}"/>')
            n += 1
        entry = (f'<w:font w:name="{fam}"><w:altName w:val="Arial"/><w:panose1 w:val="{PANOSE[fam]}"/>'
                 '<w:charset w:val="00"/><w:family w:val="swiss"/><w:pitch w:val="variable"/>'
                 + "".join(embeds) + "</w:font>")
        # replace an existing entry for this family, else append
        pat = re.compile(rf'<w:font w:name="{re.escape(fam)}"(?:/>|>.*?</w:font>)', re.S)
        ft = pat.sub(entry, ft, count=1) if pat.search(ft) else ft.replace("</w:fonts>", entry + "</w:fonts>")
    if "w:embedTrueTypeFonts" not in settings:
        # CT_Settings order: ... printFormsData, embedTrueTypeFonts, embedSystemFonts, saveSubsetFonts, ...
        before = ["writeProtection", "view", "zoom", "removePersonalInformation", "removeDateAndTime",
                  "doNotDisplayPageBoundaries", "displayBackgroundShape", "printPostScriptOverText",
                  "printFractionalCharacterWidth", "printFormsData"]
        pos = re.search(r"<w:settings[^>]*>", settings).end()
        for tag in before:
            for m in re.finditer(rf"<w:{tag}\b[^>]*?(?:/>|>.*?</w:{tag}>)", settings, re.S):
                pos = max(pos, m.end())
        settings = settings[:pos] + "<w:embedTrueTypeFonts/>" + settings[pos:]
    ct = _add_default(ct, "odttf", "application/vnd.openxmlformats-officedocument.obfuscatedFont")
    changes = {"word/fontTable.xml": ft, "word/settings.xml": settings, "[Content_Types].xml": ct}
    if rels_name in names:
        changes[rels_name] = rels
    else:
        additions[rels_name] = rels
    _rewrite(path, changes, additions)
    return "embedded"


# ---------------------------------------------------------------- PowerPoint
def _pink_bullets(xml):
    """pptxgenjs can't colour bullets: give every character bullet the brand pink, in Arial (Lato has no square).
    CT_TextParagraphProperties order matters to PowerPoint (LibreOffice and the validator are lenient):
    lnSpc, spcBef, spcAft, buClr, buSz*, buFont, buChar. buClr after buSzPct is silently ignored."""
    def fix(m):
        ppr = m.group(0)
        if "<a:buChar " not in ppr:
            return ppr
        ppr = re.sub(r"<a:buClr>.*?</a:buClr>|<a:buClrTx/>|<a:buFont [^>]*/>|<a:buFontTx/>", "", ppr)
        clr = '<a:buClr><a:srgbClr val="FF004D"/></a:buClr>'
        first = re.search(r"<a:buSz(?:Tx|Pct|Pts)\b|<a:buChar ", ppr)
        ppr = ppr[:first.start()] + clr + ppr[first.start():]
        ppr = ppr.replace("<a:buChar ", '<a:buFont typeface="Arial"/><a:buChar ', 1)
        return ppr
    return re.sub(r"<a:pPr\b[^>]*>.*?</a:pPr>", fix, xml, flags=re.S)


def _lato_hints(xml):
    """Give every Lato / Lato Black <a:latin> the same substitution hint."""
    def fix(m):
        face = m.group(1)
        return f'<a:latin typeface="{face}" panose="{PANOSE[face]}" pitchFamily="34" charset="0"/>'
    return re.sub(r'<a:latin typeface="(Lato|Lato Black)"[^>]*/>', fix, xml)


def style_pptx(path):
    """PowerPoint rejects plain TrueType embedded fonts ("General Failure" on open, tested 2026-10-21),
    so .pptx files get NO font embedding. Fallback hints are normalised and bullets styled instead."""
    changes = {}
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if not re.match(r"ppt/(slides/slide|slideLayouts/slideLayout|slideMasters/slideMaster|theme/theme|charts/chart)\d*\.xml$", n):
                continue
            x = _read(z, n)
            y = _lato_hints(x)
            if n.startswith("ppt/slides/") and "<a:buChar " in y:
                y = _pink_bullets(y)
            if y != x:
                changes[n] = y
    if changes:
        _rewrite(path, changes, {})
    return "fallback hints set, bullets styled (fonts not embedded: PowerPoint substitutes an Arial-class font)"


def style_xlsx(path):
    """Excel can't embed fonts or name a fallback: make every font Lato with the swiss family hint."""
    with zipfile.ZipFile(path) as z:
        st = _read(z, "xl/styles.xml")
    def fix(m):
        f = m.group(0)
        f = re.sub(r"<scheme [^>]*/>", "", f)          # a theme-font link would override the name
        f = re.sub(r"<family [^>]*/>", "", f)
        f = re.sub(r'<name val="[^"]*"/>', '<name val="Lato"/><family val="2"/>', f)
        if "<name " not in f:
            f = f.replace("</font>", '<name val="Lato"/><family val="2"/></font>')
        return f
    new = re.sub(r"<font>.*?</font>|<font/>", lambda m: fix(m) if m.group(0) != "<font/>" else
                 '<font><name val="Lato"/><family val="2"/></font>', st, flags=re.S)
    if new != st:
        _rewrite(path, {"xl/styles.xml": new}, {})
    return "fonts set to Lato with Arial-class fallback hint (Excel can't embed fonts)"


def embed_pptx(path):
    """NOT USED: kept for reference only. PowerPoint expects Embedded OpenType (.fntdata) and shows an
    'Install Embedded Fonts - General Failure' dialog for the plain TrueType this writes."""
    with zipfile.ZipFile(path) as z:
        slide_changes = {n: _pink_bullets(_read(z, n)) for n in z.namelist()
                         if re.match(r"ppt/slides/slide\d+\.xml$", n) and "<a:buChar " in _read(z, n)
                         and "<a:buClr>" not in _read(z, n)}
        pres = _read(z, "ppt/presentation.xml")
        rels = _read(z, "ppt/_rels/presentation.xml.rels")
        ct = _read(z, "[Content_Types].xml")
    if "<p:embeddedFontLst" in pres:
        return "already embedded"
    rels = _open_root(rels, "Relationships")
    additions, n, fonts_xml = {}, _next_rid(rels), []
    style_tag = {"Regular": "regular", "Bold": "bold", "Italic": "italic"}
    for fam, styles in FAMILIES.items():
        parts = []
        for style, fname in styles.items():
            part = f"fonts/font{n}.fntdata"
            with open(os.path.join(FONTS, fname), "rb") as fh:
                additions["ppt/" + part] = fh.read()
            rels = rels.replace("</Relationships>",
                                f'<Relationship Id="rId{n}" Type="{R_FONT}" Target="{part}"/></Relationships>')
            parts.append(f'<p:{style_tag[style]} r:id="rId{n}"/>')
            n += 1
        fonts_xml.append(f'<p:embeddedFont><p:font typeface="{fam}" panose="{PANOSE[fam]}" '
                         f'pitchFamily="34" charset="0"/>{"".join(parts)}</p:embeddedFont>')
    lst = "<p:embeddedFontLst>" + "".join(fonts_xml) + "</p:embeddedFontLst>"
    # schema order: ... sldSz, notesSz, smartTags?, embeddedFontLst, custShowLst, ...
    m = re.search(r"<p:notesSz[^>]*/>", pres)
    if not m:
        raise SystemExit("presentation.xml has no <p:notesSz/>; cannot place embeddedFontLst")
    end = m.end()
    sm = re.match(r"\s*<p:smartTags[^>]*/>", pres[end:])
    if sm:
        end += sm.end()
    pres = pres[:end] + lst + pres[end:]
    if "embedTrueTypeFonts" not in pres:
        pres = re.sub(r"(<p:presentation\b)", r'\1 embedTrueTypeFonts="1"', pres, count=1)
    ct = _add_default(ct, "fntdata", "application/x-fontdata")
    _rewrite(path, {"ppt/presentation.xml": pres, "ppt/_rels/presentation.xml.rels": rels,
                    "[Content_Types].xml": ct, **slide_changes}, additions)
    return "embedded"


if __name__ == "__main__":
    for p in sys.argv[1:]:
        ext = os.path.splitext(p)[1].lower()
        if ext == ".docx":
            print(p, embed_docx(p))
        elif ext == ".pptx":
            print(p, style_pptx(p))
        elif ext == ".xlsx":
            print(p, style_xlsx(p))
        else:
            print(p, "skipped (not a Word, PowerPoint or Excel file)")
