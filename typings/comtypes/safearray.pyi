import types

from _typeshed import Incomplete
from comtypes import IUnknown as IUnknown, com_interface_registry as com_interface_registry
from comtypes.patcher import Patch as Patch

class _SafeArrayAsNdArrayContextManager:
    thread_local: Incomplete
    def __enter__(self) -> None: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None: ...
    def __bool__(self) -> bool: ...
    __nonzero__ = __bool__

safearray_as_ndarray: Incomplete
