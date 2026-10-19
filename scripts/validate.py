#!/usr/bin/env python3
"""Validate this skill package's metadata, UTF-8 files and local Markdown links."""

import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    root = Path(root).resolve()
    errors = []
    skill = root / "skills" / "patent-disclosure"
    entry = skill / "SKILL.md"
    if not entry.is_file():
        return ["Missing skills/patent-disclosure/SKILL.md"]
    # This repository deliberately uses only name and a JSON-compatible quoted
    # description in its YAML frontmatter; this is not a general YAML parser.
    try:
        text = entry.read_text(encoding="utf-8")
        header = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        if header is None:
            errors.append("SKILL.md: missing YAML frontmatter")
        else:
            fields = {}
            for line in header.group(1).splitlines():
                key, value = line.split(":", 1)
                if key in fields:
                    raise ValueError("Duplicate frontmatter key")
                fields[key] = value.strip()
            if set(fields) != {"name", "description"} or fields.get("name") != "patent-disclosure":
                errors.append("SKILL.md: invalid name or unsupported frontmatter keys")
            description = json.loads(fields.get("description", '""'))
            if not isinstance(description, str) or not description.strip():
                errors.append("SKILL.md: description must be a nonempty quoted string")
    except (OSError, UnicodeError, ValueError) as error:
        errors.append(f"SKILL.md: invalid metadata ({type(error).__name__})")
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in {".git", "__pycache__", ".venv"} for part in relative.parts):
            continue
        if path.is_symlink():
            errors.append(f"{relative}: symbolic links are not included in this package")
            continue
        if not path.is_file() or path.suffix not in {".md", ".py", ".yaml"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            errors.append(f"{relative}: not valid UTF-8")
            continue
        if "\ufffd" in text:
            errors.append(f"{relative}: contains a replacement character")
        if path.suffix != ".md":
            continue
        if text.count("```") % 2:
            errors.append(f"{relative}: unclosed code fence")
        for match in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", text):
            url = match.group(1).strip().strip("<>")
            parsed = urlsplit(url)
            if parsed.scheme or not parsed.path:
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            if not target.is_relative_to(root) or not target.is_file():
                errors.append(f"{relative}: missing or external local link {url}")
            elif path.is_relative_to(skill) and not target.is_relative_to(skill):
                errors.append(f"{relative}: installed skill links outside its own package")
    return errors


def main():
    errors = validate()
    if errors:
        print("Validation failed:")
        for error in errors:
            print("- " + error)
        return 1
    print("PASS: metadata, UTF-8, Markdown fences, local links and self-contained skill references")
    return 0


if __name__ == "__main__":
    sys.exit(main())
