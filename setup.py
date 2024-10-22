from pathlib import Path

from mypyc.build import mypycify  # type: ignore[import-untyped]
from setuptools import setup

setup(
    # False-positive in typeshed's setuptools-stubs
    ext_modules=mypycify([  # pyright: ignore[reportArgumentType]
        path
        for path in Path("d3dshot").rglob("*.py")
        # https://github.com/mypyc/mypyc/issues/1072
        if path.name != "d3dshot.py"
    ]),
)
