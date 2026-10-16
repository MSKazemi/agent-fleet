# Copyright 2026 Mohsen Seyedkazemi Ardebili
# SPDX-License-Identifier: Apache-2.0
"""`fleet` entry point for pip/pipx installs.

The tool itself is bash (bin/fleet) plus a stdlib-only python queue engine (libexec/fleet-queue).
The wheel ships both unchanged under this package, so bin/fleet finds its engine by the same
relative path it uses in a git clone. This wrapper only locates bash, restores the executable
bits a wheel may lose, and adds the one command that has no meaning in a clone: install-skill.
"""
import os
import shutil
import sys

from . import PACKAGE_DIR

BIN = PACKAGE_DIR / "bin" / "fleet"
ENGINE = PACKAGE_DIR / "libexec" / "fleet-queue"
SKILL = PACKAGE_DIR / "skills" / "agent-fleet"


def _install_skill() -> int:
    """Link the packaged skill into ~/.claude/skills so Claude Code can load it."""
    dest_dir = os.path.join(os.path.expanduser("~"), ".claude", "skills")
    dest = os.path.join(dest_dir, "agent-fleet")
    os.makedirs(dest_dir, exist_ok=True)
    if os.path.islink(dest):
        if os.path.realpath(dest) == str(SKILL.resolve()):
            print(f"ok       {dest}")
            return 0
        os.remove(dest)
    elif os.path.exists(dest):
        print(f"SKIPPED  {dest} exists and is not a symlink - move it aside first", file=sys.stderr)
        return 1
    os.symlink(SKILL, dest)
    print(f"linked   {dest} -> {SKILL}")
    return 0


def main() -> None:
    argv = sys.argv[1:]
    if argv[:1] == ["install-skill"]:
        raise SystemExit(_install_skill())
    bash = shutil.which("bash")
    if bash is None:
        raise SystemExit("fleet: bash is required but was not found on PATH")
    for exe in (BIN, ENGINE):
        if not os.access(exe, os.X_OK):
            try:
                os.chmod(exe, 0o755)
            except OSError as err:
                raise SystemExit(f"fleet: {exe} is not executable and cannot be fixed: {err}")
    os.execv(bash, [bash, str(BIN), *argv])
