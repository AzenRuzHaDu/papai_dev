#!/usr/bin/env python3
"""
Bidirectional sync between Claude Code (.claude/) and Gemini CLI (.gemini/) configurations.

Converts:
- Commands:  .md (Claude) <-> .toml (Gemini)
- Root doc:  CLAUDE.md <-> GEMINI.md
- Docs:      .claude/docs/ <-> .gemini/docs/
- Project:   .claude/project/ <-> .gemini/project/

Usage:
    bin/sync-agents.py                # Claude -> Gemini (default)
    bin/sync-agents.py --to-claude    # Gemini -> Claude
    bin/sync-agents.py --dry-run      # Preview without writing
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CLAUDE_DIR = ".claude"
GEMINI_DIR = ".gemini"
CLAUDE_MD = "CLAUDE.md"
GEMINI_MD = "GEMINI.md"

SUBDIRS = ["commands", "docs", "project"]

# Ordered replacements — applied in sequence, so more specific patterns first.
PATH_REPLACEMENTS_C2G = [
    (".claude/docs/", ".gemini/docs/"),
    (".claude/project/", ".gemini/project/"),
]

ARG_REPLACEMENTS_C2G = [
    ("$ARGUMENTS", "{{args}}"),
]

TAG_REPLACEMENTS_C2G = [
    ("[claude/dev]", "[gemini/dev]"),
    ("[claude/architect]", "[gemini/architect]"),
    ("[claude/tester]", "[gemini/tester]"),
    ("[claude/planner]", "[gemini/planner]"),
    ("[claude/agent]", "[gemini/agent]"),
    ("[claude/prd]", "[gemini/prd]"),
    ("[claude/review]", "[gemini/review]"),
    ("[claude/stack]", "[gemini/stack]"),
    ("[claude/doc-feed]", "[gemini/doc-feed]"),
]


def _reverse(pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    return [(b, a) for a, b in pairs]


PATH_REPLACEMENTS_G2C = _reverse(PATH_REPLACEMENTS_C2G)
ARG_REPLACEMENTS_G2C = _reverse(ARG_REPLACEMENTS_C2G)
TAG_REPLACEMENTS_G2C = _reverse(TAG_REPLACEMENTS_C2G)

# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------


def apply_replacements(text: str, *replacement_lists: list[tuple[str, str]]) -> str:
    for rlist in replacement_lists:
        for old, new in rlist:
            text = text.replace(old, new)
    return text


def extract_yaml_frontmatter(md: str) -> tuple[dict[str, str], str]:
    """Return (frontmatter_dict, body) from a markdown file.

    Only extracts simple key: value pairs (no nesting).
    """
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", md, re.DOTALL)
    if not m:
        return {}, md
    raw = m.group(1)
    body = md[m.end() :]
    meta: dict[str, str] = {}
    for line in raw.splitlines():
        kv = re.match(r"^(\w[\w-]*):\s*(.+)$", line)
        if kv:
            val = kv.group(2).strip().strip("\"'")
            meta[kv.group(1)] = val
    return meta, body


# ---------------------------------------------------------------------------
# Command conversion
# ---------------------------------------------------------------------------


def md_to_toml(md_content: str) -> str:
    """Convert a Claude .md command to Gemini .toml format."""
    content = apply_replacements(
        md_content,
        PATH_REPLACEMENTS_C2G,
        ARG_REPLACEMENTS_C2G,
        TAG_REPLACEMENTS_C2G,
    )

    meta, body = extract_yaml_frontmatter(content)
    description = meta.get("description", "")

    # Fallback: derive description from first heading
    if not description:
        heading = re.match(r"^\s*#\s+(.+)", body)
        if heading:
            description = heading.group(1).strip()

    # TOML triple-quoted strings: escape sequences of 3+ consecutive "
    body_escaped = re.sub(r'"{3,}', lambda m: '""' + '\\"' * (len(m.group()) - 2), body.strip())

    lines: list[str] = []
    if description:
        safe_desc = description.replace("\\", "\\\\").replace('"', '\\"')
        lines.append(f'description = "{safe_desc}"')
    lines.append(f'prompt = """\n{body_escaped}\n"""')
    return "\n".join(lines) + "\n"


def toml_to_md(toml_content: str) -> str:
    """Convert a Gemini .toml command to Claude .md format."""
    # Extract prompt — multiline first, then single-line fallback
    prompt = ""
    m = re.search(r'prompt\s*=\s*"""(.*?)"""', toml_content, re.DOTALL)
    if m:
        prompt = m.group(1)
        # Strip exactly one leading newline (TOML convention for multiline)
        if prompt.startswith("\n"):
            prompt = prompt[1:]
    else:
        m = re.search(r'prompt\s*=\s*"((?:[^"\\]|\\.)*)"', toml_content)
        if m:
            prompt = m.group(1).replace('\\"', '"').replace("\\\\", "\\")

    # Unescape TOML triple-quote escaping
    prompt = prompt.replace('\\"', '"')

    # Convert @{path} injections to plain path references
    prompt = re.sub(r"@\{([^}]+)\}", r"`\1`", prompt)

    prompt = apply_replacements(
        prompt,
        PATH_REPLACEMENTS_G2C,
        ARG_REPLACEMENTS_G2C,
        TAG_REPLACEMENTS_G2C,
    )

    return prompt.rstrip() + "\n"


# ---------------------------------------------------------------------------
# File operations
# ---------------------------------------------------------------------------


def convert_doc_file(src: Path, dst: Path, *replacement_lists: list[tuple[str, str]]) -> None:
    """Copy a documentation .md file with text replacements."""
    content = src.read_text(encoding="utf-8")
    content = apply_replacements(content, *replacement_lists)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(content, encoding="utf-8")


def sync_directory(
    src_root: Path,
    dst_root: Path,
    subdir: str,
    *,
    convert_commands: bool,
    direction: str,  # "c2g" or "g2c"
    dry_run: bool,
) -> list[str]:
    """Sync a subdirectory. Returns list of actions taken."""
    actions: list[str] = []
    src_dir = src_root / subdir
    dst_dir = dst_root / subdir

    if not src_dir.exists():
        return actions

    if direction == "c2g":
        path_repls = PATH_REPLACEMENTS_C2G
        tag_repls = TAG_REPLACEMENTS_C2G
    else:
        path_repls = PATH_REPLACEMENTS_G2C
        tag_repls = TAG_REPLACEMENTS_G2C

    for src_file in sorted(src_dir.rglob("*")):
        if src_file.is_dir():
            continue

        rel = src_file.relative_to(src_dir)

        if subdir == "commands" and convert_commands:
            if direction == "c2g" and src_file.suffix == ".md":
                dst_file = dst_dir / rel.with_suffix(".toml")
                action = f"  {src_file} -> {dst_file}  [md->toml]"
                actions.append(action)
                if not dry_run:
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    md_content = src_file.read_text(encoding="utf-8")
                    dst_file.write_text(md_to_toml(md_content), encoding="utf-8")

            elif direction == "g2c" and src_file.suffix == ".toml":
                dst_file = dst_dir / rel.with_suffix(".md")
                action = f"  {src_file} -> {dst_file}  [toml->md]"
                actions.append(action)
                if not dry_run:
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    toml_content = src_file.read_text(encoding="utf-8")
                    dst_file.write_text(toml_to_md(toml_content), encoding="utf-8")
            else:
                # Copy as-is (non-matching extension)
                dst_file = dst_dir / rel
                action = f"  {src_file} -> {dst_file}  [copy]"
                actions.append(action)
                if not dry_run:
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_file, dst_file)

        elif src_file.suffix == ".md":
            dst_file = dst_dir / rel
            action = f"  {src_file} -> {dst_file}  [convert]"
            actions.append(action)
            if not dry_run:
                convert_doc_file(src_file, dst_file, path_repls, tag_repls)

        else:
            # Non-markdown files: copy as-is (e.g. .gitkeep)
            dst_file = dst_dir / rel
            action = f"  {src_file} -> {dst_file}  [copy]"
            actions.append(action)
            if not dry_run:
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dst_file)

    return actions


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync agent configurations between Claude Code and Gemini CLI."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--to-gemini",
        action="store_true",
        default=True,
        help="Convert Claude -> Gemini (default)",
    )
    group.add_argument(
        "--to-claude",
        action="store_true",
        help="Convert Gemini -> Claude",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing files",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Don't remove the destination directory before syncing",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path("."),
        help="Project root directory (default: current directory)",
    )
    args = parser.parse_args()

    root = args.project_root.resolve()

    if args.to_claude:
        direction = "g2c"
        src_dir_name = GEMINI_DIR
        dst_dir_name = CLAUDE_DIR
        src_md = GEMINI_MD
        dst_md = CLAUDE_MD
        path_repls = PATH_REPLACEMENTS_G2C
        tag_repls = TAG_REPLACEMENTS_G2C
        label = "Gemini -> Claude"
    else:
        direction = "c2g"
        src_dir_name = CLAUDE_DIR
        dst_dir_name = GEMINI_DIR
        src_md = CLAUDE_MD
        dst_md = GEMINI_MD
        path_repls = PATH_REPLACEMENTS_C2G
        tag_repls = TAG_REPLACEMENTS_C2G
        label = "Claude -> Gemini"

    src_root = root / src_dir_name
    dst_root = root / dst_dir_name
    src_md_path = root / src_md
    dst_md_path = root / dst_md

    if not src_root.exists():
        print(f"Error: source directory {src_root} does not exist.", file=sys.stderr)
        sys.exit(1)

    prefix = "[dry-run] " if args.dry_run else ""
    print(f"{prefix}Syncing: {label}")
    print(f"{prefix}Source:  {src_root}")
    print(f"{prefix}Target:  {dst_root}")
    print()

    all_actions: list[str] = []

    # --- Clean destination ---
    if not args.no_clean and dst_root.exists():
        action = f"  rm -rf {dst_root}"
        all_actions.append(action)
        if not args.dry_run:
            shutil.rmtree(dst_root)

    # --- Root markdown file ---
    if src_md_path.exists():
        action = f"  {src_md_path} -> {dst_md_path}  [convert]"
        all_actions.append(action)
        if not args.dry_run:
            convert_doc_file(src_md_path, dst_md_path, path_repls, tag_repls)

    # --- Subdirectories ---
    for subdir in SUBDIRS:
        actions = sync_directory(
            src_root,
            dst_root,
            subdir,
            convert_commands=(subdir == "commands"),
            direction=direction,
            dry_run=args.dry_run,
        )
        all_actions.extend(actions)

    # --- Ensure project/.gitkeep exists ---
    gitkeep = dst_root / "project" / ".gitkeep"
    if not gitkeep.exists() or args.dry_run:
        action = f"  touch {gitkeep}"
        all_actions.append(action)
        if not args.dry_run:
            gitkeep.parent.mkdir(parents=True, exist_ok=True)
            gitkeep.touch()

    # --- Report ---
    if all_actions:
        print("Actions:")
        for a in all_actions:
            print(a)
        print(f"\n{prefix}Done. {len(all_actions)} file(s) processed.")
    else:
        print("Nothing to do.")

    # --- Warn about settings ---
    if direction == "c2g":
        settings_local = src_root / "settings.local.json"
        if settings_local.exists():
            print(
                f"\nNote: {settings_local} has no Gemini equivalent.\n"
                "Gemini CLI uses ~/.gemini/settings.json for local overrides."
            )
    elif direction == "g2c":
        settings = src_root / "settings.json"
        if settings.exists():
            print(
                f"\nNote: {settings} format differs from Claude's.\n"
                "Claude uses .claude/settings.local.json for local settings."
            )


if __name__ == "__main__":
    main()
