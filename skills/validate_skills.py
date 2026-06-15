#!/usr/bin/env python3
"""Validate agentskills.io SKILL.md bundles under skills/."""
import sys, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME, MAX_DESC, MAX_BODY = 64, 1024, 8000

def parse_frontmatter(text):
    if not text.startswith("---"):
        return None, text, "missing YAML frontmatter (must start with '---')"
    end = text.find("\n---", 3)
    if end == -1:
        return None, text, "unterminated YAML frontmatter"
    fm_raw, body = text[3:end].strip(), text[end+4:].lstrip("\n")
    fm = {}
    for line in fm_raw.splitlines():
        if ":" in line and not line.startswith((" ", "\t", "#")):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, body, None

def validate(skill_dir):
    errs = []
    md = skill_dir / "SKILL.md"
    if not md.exists():
        return [f"{skill_dir.name}: no SKILL.md"]
    fm, body, ferr = parse_frontmatter(md.read_text(encoding="utf-8"))
    if ferr:
        return [f"{skill_dir.name}: {ferr}"]
    name = fm.get("name", "")
    desc = fm.get("description", "")
    if not name: errs.append(f"{skill_dir.name}: missing 'name'")
    if name and not NAME_RE.match(name):
        errs.append(f"{skill_dir.name}: name '{name}' not lowercase-hyphen")
    if len(name) > MAX_NAME: errs.append(f"{skill_dir.name}: name >{MAX_NAME} chars")
    if name and name != skill_dir.name:
        errs.append(f"{skill_dir.name}: name '{name}' != folder '{skill_dir.name}'")
    if not desc: errs.append(f"{skill_dir.name}: missing 'description'")
    if len(desc) > MAX_DESC:
        errs.append(f"{skill_dir.name}: description {len(desc)}>{MAX_DESC} chars")
    if len(body) > MAX_BODY:
        errs.append(f"{skill_dir.name}: body {len(body)}>{MAX_BODY} chars")
    return errs

def main():
    targets = sys.argv[1:] or [str(p) for p in sorted(ROOT.iterdir())
                               if p.is_dir() and (p / "SKILL.md").exists()]
    all_errs = []
    for t in targets:
        d = Path(t) if Path(t).is_absolute() else ROOT / t
        all_errs += validate(d)
    if all_errs:
        print("FAIL:"); [print("  -", e) for e in all_errs]; sys.exit(1)
    print(f"PASS: {len(targets)} skill(s) valid"); sys.exit(0)

if __name__ == "__main__":
    main()
