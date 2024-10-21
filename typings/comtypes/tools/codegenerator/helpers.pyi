from typing import Any

from _typeshed import Incomplete
from comtypes.tools import typedesc as typedesc
from comtypes.tools.codegenerator.modulenamer import name_wrapper_module as name_wrapper_module

class lcid: ...

class dispid:
    memid: Incomplete
    def __init__(self, memid) -> None: ...

class helpstring:
    text: Incomplete
    def __init__(self, text) -> None: ...

ctypes_names: Incomplete

def get_real_type(tp): ...

ASSUME_STRINGS: bool

class ComMethodGenerator:
    data: Incomplete
    def __init__(self, m: typedesc.ComMethod, isdual: bool) -> None: ...
    def generate(self) -> str: ...

class DispMethodGenerator:
    data: Incomplete
    def __init__(self, m: typedesc.DispMethod) -> None: ...
    def generate(self) -> str: ...

class DispPropertyGenerator:
    def __init__(self, m: typedesc.DispProperty) -> None: ...
    def generate(self) -> str: ...

class TypeNamer:
    def __call__(self, t: Any) -> str: ...
