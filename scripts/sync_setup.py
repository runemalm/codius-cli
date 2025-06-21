#!/usr/bin/env python3

import sys
import toml
import re
from pathlib import Path

def parse_pipfile(pipfile_path):
    data = toml.load(pipfile_path)
    packages = data.get("packages", {})
    return [f"{name}{version if version != '*' else ''}" for name, version in packages.items()]

def format_install_requires(requirements, indent='    '):
    return ',\n'.join(f"{indent*2}'{req}'" for req in requirements)

def update_setup_py(requirements, setup_path):
    indent = '    '
    formatted = format_install_requires(requirements, indent)
    new_block = f"{indent}install_requires=[\n{formatted},\n{indent}],"

    text = setup_path.read_text()
    updated = re.sub(
        r"^\s*install_requires=\[[^\]]*\],?",
        new_block,
        text,
        flags=re.DOTALL | re.MULTILINE
    )
    setup_path.write_text(updated)
    print("✅ install_requires block in setup.py updated.")

def dry_run(requirements):
    print("🔍 install_requires (dry run):\n")
    print("install_requires = [")
    for r in requirements:
        print(f"    '{r}',")
    print("]")

def main():
    if len(sys.argv) < 4 or sys.argv[1] not in ("--dry-run", "--sync"):
        print("Usage:")
        print("  --dry-run <Pipfile> <setup.py>   Preview install_requires")
        print("  --sync <Pipfile> <setup.py>      Update setup.py")
        sys.exit(1)

    mode = sys.argv[1]
    pipfile_path = Path(sys.argv[2])
    setup_path = Path(sys.argv[3])

    requirements = parse_pipfile(pipfile_path)

    if mode == "--dry-run":
        dry_run(requirements)
    elif mode == "--sync":
        update_setup_py(requirements, setup_path)

if __name__ == "__main__":
    main()
