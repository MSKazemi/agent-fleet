# Copyright 2026 Mohsen Seyedkazemi Ardebili
# SPDX-License-Identifier: Apache-2.0
"""agent-fleet — parallel Claude Code sessions against one shared task queue."""
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
__version__ = (PACKAGE_DIR / "VERSION").read_text().strip() \
    if (PACKAGE_DIR / "VERSION").exists() else (PACKAGE_DIR.parents[2] / "VERSION").read_text().strip()
