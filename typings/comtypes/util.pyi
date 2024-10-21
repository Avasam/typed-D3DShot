from ctypes import *

__all__ = ["byref_at", "cast_field"]

def byref_at(obj, offset, _byref=..., _c_void_p_from_address=..., _byref_pointer_offset=...): ...
def cast_field(
    struct,
    fieldname,
    fieldtype,
    offset: int = 0,
    _POINTER=...,
    _byref_at=...,
    _byref=...,
    _divmod=...,
    _sizeof=...,
): ...
