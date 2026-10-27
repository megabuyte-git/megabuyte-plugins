"""Install Lato and stage the Megabuyte logos for this session.
Usage: python <skill_dir>/scripts/brand_setup.py
Prints the staged paths. Safe to run more than once."""
import os, shutil, subprocess, sys
skill = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assets = os.path.join(skill, "assets")
fonts_dst = os.path.expanduser("~/.fonts"); os.makedirs(fonts_dst, exist_ok=True)
for f in os.listdir(os.path.join(assets, "fonts")):
    if f.endswith(".ttf"):
        shutil.copy(os.path.join(assets, "fonts", f), fonts_dst)
subprocess.run(["fc-cache", "-f"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
out = "/tmp/mb_brand"; os.makedirs(out, exist_ok=True)
for f in ("logo_white.png", "logo_pink.png"):
    shutil.copy(os.path.join(assets, f), os.path.join(out, f))
ok = subprocess.run(["fc-list"], capture_output=True, text=True).stdout.count("Lato") > 0
print(f"fonts: {'Lato installed' if ok else 'Lato NOT installed - use Arial'}")
print(f"logo_white: {out}/logo_white.png\nlogo_pink: {out}/logo_pink.png")
