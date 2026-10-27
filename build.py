
import sys
import shutil
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SHARED = ROOT / "src" / "shared"

SKILLS = ROOT / "src" / "skills"

PLUGIN = ROOT / "plugins" / "megabuyte"
OUT = PLUGIN / "skills"

MANIFESTS = [
    PLUGIN / ".claude-plugin" / "plugin.json",
    PLUGIN / ".codex-plugin" / "plugin.json"
]

ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}

EXCLUDE = {"__pycache__", ".DS_Store", "evals"}


def validate(skill_dir):
    errs = []

    skill_text = (skill_dir / "SKILL.md").read_text()

    frontmatter_match = re.match(r"^---\n(.*?)\n---\n", skill_text, re.S)
    if not frontmatter_match:
        return [str(ValueError("no YAML frontmatter"))]
    frontmatter = frontmatter_match.group(1)

    frontmatter_keys = {k for k in re.findall(r"^([A-Za-z][\w-]*):", frontmatter, re.M)}
    if frontmatter_keys - ALLOWED_KEYS:
        errs.append(f"unexpected frontmatter keys: {sorted(frontmatter_keys - ALLOWED_KEYS)}")

    skill_name = re.search(r"^name:\s*(\S+)", frontmatter, re.M)
    if not skill_name or skill_name.group(1) != skill_dir.name:
        errs.append("frontmatter name must equal the folder name")

    for shared_filename in set(re.findall(r"`((?:references|scripts|assets)/[\w./-]+)`", skill_text)):
        if not (skill_dir / shared_filename).exists():
            errs.append(f"SKILL.md refers to {shared_filename}, which is not in the built skill")

    return errs


def build():
    """Assemble every skill into their destinations. Returns {skill name: [errors]} for skills that fail validation."""

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    failures = {}
    for source_skill_directory in sorted(p for p in SKILLS.iterdir() if (p / "SKILL.md").exists()):
        destination_skill_directory = OUT / source_skill_directory.name
        shutil.copytree(
            src = source_skill_directory,
            dst = destination_skill_directory,
            ignore = shutil.ignore_patterns(*EXCLUDE)
        )
        shutil.copytree(
            src = SHARED,
            dst = destination_skill_directory,
            dirs_exist_ok = True,
            ignore = shutil.ignore_patterns(*EXCLUDE)
        )

        errs = validate(destination_skill_directory)
        if errs:
            failures[source_skill_directory.name] = errs

    return failures


def set_manifest_versions(version):
    for f in MANIFESTS:
        text = f.read_text()
        new = re.sub(r'("version"\s*:\s*")[^"]*(")', rf"\g<1>{version}\g<2>", text, count=1)
        if new != text:
            f.write_text(new)


def main():
    _ = argparse.ArgumentParser(
        description="Build Megabuyte MCP skills from src/skills into plugins/megabuyte/skills. "
        "This script is only for running before making a commit, though there's no harm in running "
        "it at any other point."
    ).parse_args()

    failed = False
    for name, errs in build().items():
        failed = True
        print(f"FAIL {name}:\n  - " + "\n  - ".join(errs))

    set_manifest_versions((ROOT / "VERSION").read_text().strip())

    print(f"\nMegabuyte MCP skills -> {OUT.relative_to(ROOT)}" + ("  FAILED" if failed else ""))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
