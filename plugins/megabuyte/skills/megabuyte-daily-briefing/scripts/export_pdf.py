"""Make a PDF copy of a finished .docx, .pptx or .xlsx export, with Lato embedded.

Usage: python <skill_dir>/scripts/export_pdf.py <file> [more files...]
Writes <name>.pdf beside each input and prints the fonts the PDF embeds.
Run brand_setup.py first: the PDF can only embed Lato if Lato is installed."""
import glob, os, shutil, subprocess, sys

def soffice_cmd():
    # Prefer the sandbox-safe wrapper shipped with the public docx/pptx skills; bare soffice can hang.
    for w in glob.glob("/mnt/skills/public/*/scripts/office/soffice.py"):
        return [sys.executable, w]
    exe = shutil.which("soffice") or shutil.which("libreoffice")
    if not exe:
        raise SystemExit("No LibreOffice found: offer the Word/PowerPoint file only.")
    return [exe]

for f in sys.argv[1:]:
    out = os.path.dirname(os.path.abspath(f))
    subprocess.run(soffice_cmd() + ["--headless", "--convert-to", "pdf", "--outdir", out, f],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
    pdf = os.path.splitext(os.path.abspath(f))[0] + ".pdf"
    if not os.path.exists(pdf):
        print(f, "-> PDF conversion failed"); continue
    fonts = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout
    names = sorted({l.split()[0].split("+")[-1] for l in fonts.splitlines()[2:] if l.strip()})
    flag = "OK" if any(n.startswith("Lato") for n in names) else "WARNING: Lato not embedded"
    print(f"{pdf}  [{flag}]  fonts: {', '.join(names)}")
