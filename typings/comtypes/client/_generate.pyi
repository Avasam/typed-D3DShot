import types
from typing import Any

from _typeshed import Incomplete
from comtypes import GUID as GUID, typeinfo as typeinfo
from comtypes.tools import codegenerator as codegenerator, tlbparser as tlbparser

logger: Incomplete
PATH: Incomplete

def GetModule(tlib: Any | typeinfo.ITypeLib) -> types.ModuleType: ...

class ModuleGenerator:
    wrapper_name: Incomplete
    friendly_name: Incomplete
    pathname: Incomplete
    tlib: Incomplete
    def __init__(self, tlib: typeinfo.ITypeLib, pathname: str | None) -> None: ...
    def generate(self) -> types.ModuleType: ...
