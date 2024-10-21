from _typeshed import Incomplete

__all__ = ["interop"]

class Interop:
    enabled: bool
    VARIANT_dtype: Incomplete
    typecodes: Incomplete
    datetime64: Incomplete
    com_null_date64: Incomplete
    def __init__(self) -> None: ...
    def isndarray(self, value): ...
    def isdatetime64(self, value): ...
    @property
    def numpy(self): ...
    def enable(self) -> None: ...

interop: Incomplete
