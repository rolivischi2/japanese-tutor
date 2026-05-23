#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "markdown>=3.6",
#     "pyyaml>=6.0",
# ]
# ///
"""Build the deployed site under public/ from the curriculum sources.

Reads INDEX.md for module status, walks modules/, renders each .md file to
HTML using tools/templates/page.html, and writes the home page using
tools/templates/landing.html.

Run with --self-test to exercise the pure helper functions.
"""

from __future__ import annotations

import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml
import markdown as md_lib

ROOT = Path(__file__).resolve().parent.parent
MODULES_DIR = ROOT / "modules"
TEMPLATES_DIR = ROOT / "tools" / "templates"
OUT_DIR = ROOT / "public"
GITHUB_BLOB = "https://github.com/rolivischi2/japanese-tutor/blob/main"


@dataclass
class ModuleMeta:
    slug: str           # e.g. "01-copula-basics"
    number: str         # e.g. "01"
    title: str          # e.g. "Copula Basics"
    status: str         # "done" | "active" | "locked"
    key_grammar: str    # e.g. "です、じゃない、は、か、の"


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return run_self_tests()
    # Full build implemented in later tasks.
    print("build_site.py: skeleton only — full build not yet implemented")
    return 0


def run_self_tests() -> int:
    print("build_site.py self-tests: 0 cases (skeleton)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
