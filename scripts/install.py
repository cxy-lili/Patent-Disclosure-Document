#!/usr/bin/env python3
"""Install the shared skill into a client's native directory; standard library only."""

import argparse
import json
from pathlib import Path
import shutil
import tempfile
import uuid


SKILL_NAME = "patent-disclosure"
SOURCE = Path(__file__).resolve().parents[1] / "skills" / SKILL_NAME
CLIENTS = {
    "codex": {"user": ".agents/skills", "project": ".agents/skills"},
    "claude": {"user": ".claude/skills", "project": ".claude/skills"},
    "cursor": {"user": ".cursor/skills", "project": ".cursor/skills"},
    "copilot": {"user": ".copilot/skills", "project": ".github/skills"},
}


def destination_for(client, scope, project=None, home=None):
    base = (Path(home) if home is not None else Path.home()) if scope == "user" else Path(project or Path.cwd())
    return base / CLIENTS[client][scope] / SKILL_NAME


def install_skill(destination, source=SOURCE, replace=False, dry_run=False):
    source = Path(source).resolve()
    target = Path(destination).expanduser()
    if target.is_symlink():
        raise ValueError("Refusing to replace a symbolic-link destination; choose its intended location explicitly.")
    target = target.resolve()
    if source == target or target.is_relative_to(source) or source.is_relative_to(target):
        raise ValueError("Source and destination must not contain one another.")
    if not (source / "SKILL.md").is_file():
        raise ValueError("Source is missing SKILL.md.")
    if any(p.is_symlink() for p in source.rglob("*")):
        raise ValueError("Source contains symbolic links; inspect the package before installing.")
    if target.exists():
        if not replace:
            raise FileExistsError("Destination exists. Use --replace to retain a backup and install the new version.")
        marker = target / "SKILL.md"
        if not target.is_dir() or not marker.is_file() or "name: patent-disclosure" not in marker.read_text(encoding="utf-8-sig"):
            raise ValueError("Existing destination is not a patent-disclosure skill; choose another location.")
    result = {"status": "dry-run" if dry_run else "installed", "source": str(source), "destination": str(target), "backup": None}
    if dry_run:
        return result
    target.parent.mkdir(parents=True, exist_ok=True)
    # The temporary directory is created under the verified destination parent.
    # Its context manager removes only that generated staging directory.
    with tempfile.TemporaryDirectory(prefix=".patent-disclosure-install-", dir=target.parent) as temporary:
        staged = Path(temporary) / SKILL_NAME
        shutil.copytree(source, staged, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        backup = None
        if target.exists():
            if not replace:
                raise FileExistsError("Destination appeared during installation; no files were replaced.")
            # Keep backups outside the conventional skills discovery root so a
            # client cannot accidentally discover a second copy of the skill.
            backup = target.parent.parent / ".patent-disclosure-backups" / uuid.uuid4().hex / SKILL_NAME
            backup.parent.mkdir(parents=True)
            target.rename(backup)
        try:
            staged.rename(target)
        except OSError:
            if backup is not None and not target.exists():
                backup.rename(target)
            raise
        result["backup"] = str(backup) if backup is not None else None
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client", required=True, choices=CLIENTS)
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument("--project", type=Path, help="Project root when --scope project is selected.")
    parser.add_argument("--destination", type=Path, help="Explicit final skill directory; overrides the conventional location.")
    parser.add_argument("--replace", action="store_true", help="Back up an existing skill before replacing it.")
    parser.add_argument("--dry-run", action="store_true", help="Show the destination without changing any files.")
    args = parser.parse_args(argv)
    if args.project is not None and args.scope != "project":
        parser.error("--project requires --scope project")
    if args.project is not None and args.destination is not None:
        parser.error("Use either --project or --destination, not both.")
    target = args.destination if args.destination is not None else destination_for(args.client, args.scope, args.project)
    try:
        result = install_skill(target, replace=args.replace, dry_run=args.dry_run)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Installation failed: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
