import importlib.util
from typing import TYPE_CHECKING, Any, Callable, Final

if TYPE_CHECKING:
    from typing_extensions import override as override  # noqa: PLC0414
else:

    def override(arg: Callable[..., Any], /) -> Callable[..., Any]:
        """
        Indicate that a method is intended to override a method in a base class.

        Usage:

            class Base:
                def method(self) -> None:
                    pass

            class Child(Base):
                @override
                def method(self) -> None:
                    super().method()

        When this decorator is applied to a method, the type checker will
        validate that it overrides a method with the same name on a base class.
        This helps prevent bugs that may occur when a base class is changed
        without an equivalent change to a child class.

        There is no runtime checking of these properties. The decorator
        sets the ``__override__`` attribute to ``True`` on the decorated object
        to allow runtime introspection.

        See PEP 698 for details.

        """
        try:
            arg.__override__ = True  # type: ignore[attr-defined]
        except (AttributeError, TypeError):
            # Skip the attribute silently if it is not writable.
            # AttributeError happens if the object has __slots__ or a
            # read-only property, TypeError if it's a builtin class.
            pass
        return arg


pil_is_available: Final = importlib.util.find_spec("PIL") is not None
numpy_is_available: Final = importlib.util.find_spec("numpy") is not None
pytorch_is_available: Final = numpy_is_available and importlib.util.find_spec("torch") is not None
if pytorch_is_available:
    import torch

    pytorch_gpu_is_available: Final = torch.cuda.is_available()
else:
    # We only assign once: https://github.com/python/mypy/issues/10736#issuecomment-2374797327
    pytorch_gpu_is_available: Final = False  # type: ignore[misc]
