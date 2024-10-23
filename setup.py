from pathlib import Path

from setuptools import setup

# mypyc $(git ls-files 'd3dshot/**.py' ':!:d3dshot/d3dshot.py' ':!:d3dshot/dll/*')

try:
    from mypyc.build import mypycify  # type: ignore[import-untyped]

    ext_modules = mypycify(
        # Build isolation causes this file to be moved to and run from
        # a temp directory where mypy.ini doesn't exists.
        ["--disable-error-code=attr-defined", "--disable-error-code=no-any-return"]
        + [
            str_path
            for str_path in (  # fmt: skip # noqa: RUF028
                str(path) for path in Path("d3dshot").rglob("*.py")
            )
            if not (
                str_path
                in {
                    # https://github.com/mypyc/mypyc/issues/1072
                    "d3dshot\\d3dshot.py",
                    # idk, but at this point I just want a POC
                    # https://github.com/mypyc/mypyc/issues/961
                    "d3dshot\\display.py",
                }
                # https://github.com/mypyc/mypyc/issues/1033
                # https://github.com/mypyc/mypyc/issues/1073
                or "dll" in str_path
            )
        ]
    )

except ModuleNotFoundError:
    # Hackily depend on build isolation to not run mypyc during self-install
    print(
        "mypyc not available, assuming this is an install, not a build",
        "Remember to add mypy to [build-system].requires in your pyproject.toml.",
    )
    ext_modules = []

setup(
    # False-positive in typeshed's setuptools-stubs
    ext_modules=ext_modules  # pyright: ignore[reportArgumentType]
)
