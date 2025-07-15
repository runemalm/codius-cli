import re
import subprocess
import sys
from pathlib import Path

VERSION_FILE = Path("src/codius/version.py")

def read_version():
    content = VERSION_FILE.read_text()
    match = re.search(r'__version__ = "(\d+)\.(\d+)\.(\d+)"', content)
    if not match:
        sys.exit("Could not find version string.")
    return tuple(map(int, match.groups()))

def write_version(version):
    major, minor, patch = version
    new_content = re.sub(
        r'__version__ = "(\d+)\.(\d+)\.(\d+)"',
        f'__version__ = "{major}.{minor}.{patch}"',
        VERSION_FILE.read_text(),
    )
    VERSION_FILE.write_text(new_content)
    print(f"Bumped to {major}.{minor}.{patch}")

def detect_bump_type():
    result = subprocess.run(
        ["git", "log", "$(git describe --tags --abbrev=0)..HEAD", "--pretty=format:%s"],
        stdout=subprocess.PIPE,
        text=True,
        shell=True,
    )

    commits = result.stdout.splitlines()

    if any("BREAKING CHANGE" in c or "!" in c.split(":")[0] for c in commits):
        return "major"
    if any(c.startswith("feat:") for c in commits):
        return "minor"
    if any(c.startswith("fix:") for c in commits):
        return "patch"
    return "patch"

def bump_version(bump_type):
    major, minor, patch = read_version()

    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        sys.exit(f"Unknown bump type: {bump_type}")

    write_version((major, minor, patch))

if __name__ == "__main__":
    bump_type = detect_bump_type()
    print(f"Detected bump type: {bump_type}")
    bump_version(bump_type)
