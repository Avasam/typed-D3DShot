## Unreleased

* Changed build backend to `setuptools >= 69.0.0`
* Renamed project to `typed-D3DShot`
* Bumped the minimum Python version to 3.8
* Removed upper bound from all dependency pins
* Remove `pillow` from required dependencies
* Added extras: `[PIL]`, `[numpy]` and `[torch]` as per the 3 supported outputs
* Bumped `pillow >= 9.1.0`
  * Root-level enum members (like `Image.Transpose.ROTATE_90`) are deprecated not exposed in the current `py.typed` version of Pillow. To avoid `types-pillow` as a type dependency, we bumped to the first version that included said enums
* Bumped `numpy >= 1.21.0` (the first `py.typed` NumPy version with `numpy.typing.NDArray`)
* Bumped `"torch >= 2.0.0` (the first `py.typed` PyTorch version)
* Trying to create a second instance of a Singleton now "raises" a `Warning` instead of printing
* Errors whilst trying to capture a Display will now "raise" Warnings or type `DisplayCaptureWarning` (subtype of `DisplayCaptureError`) instead of silencing all Exceptions. This is to help catch potential errors in code. These may actually raise an Exception once we know which ones were meant to be silenced
* Parameter `process_func` of `d3dshot.dll.dxgi.get_dxgi_output_duplication_frame` is no longer optional
* Passing `region=None` to `d3dshot.dll.dxgi.get_dxgi_output_duplication_frame` now defaults to `(0, 0, width, height)` instead of raising an error
* Support `pathlib.Path` when specifying directory to save to
* Allowed region to be any iterable
* Made region validation a bit more efficient
* Avoid validating region every loop iteration
* Avoid double region validation (yes twice per loop iteration) in `screenshot_to_disk_every`, `screenshot_every`
* Various automated performance improvements thanks to [Ruff](https://github.com/astral-sh/ruff)
* Passing an invalid Capture Output name will now raise a `ValueError` instead of an `AttributeError`

## 0.1.5

* FIX: Made the D3DShot class a singleton to avoid crashes when subsequent calls are made to `create()`
* FIX: Actually honor `DXGI_MAPPED_RECT.Pitch` when building the capture output. This resolves issues with garbled output at some resolutions.

## 0.1.4

* FIX: If no display is identified as the primary display, default to the first one (@Ricky54326)
* FIX: When stopping a capture, give the capture thread a budget of up to 1 second to join. Should provide a better guarantee the frame buffer won't be written to after stop() returns
* FIX: When saving the frame buffer to disk, iterate over a tuple-cast frame buffer copy. Prevents iteration errors if the frame buffer gets written to during iteration
* INTERNAL: Manage dependencies + builds with Poetry
* INTERNAL: Code auto-formatting with Black
