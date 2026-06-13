"""
Smoke test: import every one of our own modules, including submodules.

Catches import-time errors early: syntax errors, missing dependencies
and broken platform guards in module-level code.
"""

from __future__ import annotations

import importlib
import operator
import pkgutil
import sys
import unittest
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

SRC_DIR = Path(__file__).parent.parent / "d3dshot"
sys.path.insert(0, str(SRC_DIR))


def iter_all_modules() -> Generator[str]:
    """Yields every modules, followed by its direct submodules."""
    for top_level in sorted(pkgutil.iter_modules([SRC_DIR]), key=operator.attrgetter("name")):
        yield top_level.name
        if top_level.ispkg:
            for submodule in pkgutil.iter_modules([SRC_DIR / top_level.name]):
                yield f"{top_level.name}.{submodule.name}"


class TestImportAllModules(unittest.TestCase):
    def test_import_all_modules(self) -> None:
        for module_name in iter_all_modules():
            with self.subTest(module=module_name):
                importlib.import_module(module_name)


if __name__ == "__main__":
    unittest.main()
