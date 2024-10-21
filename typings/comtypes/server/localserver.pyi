from ctypes import *

import comtypes
from _typeshed import Incomplete
from comtypes.hresult import *
from comtypes.server import IClassFactory as IClassFactory

logger: Incomplete
REGCLS_SINGLEUSE: int
REGCLS_MULTIPLEUSE: int
REGCLS_MULTI_SEPARATE: int
REGCLS_SUSPENDED: int
REGCLS_SURROGATE: int

def run(classes) -> None: ...

class ClassFactory(comtypes.COMObject):
    regcls = REGCLS_MULTIPLEUSE
    def __init__(self, cls, *args, **kw) -> None: ...
    def IUnknown_AddRef(self, this): ...
    def IUnknown_Release(self, this): ...
    def CreateInstance(self, this, punkOuter, riid, ppv): ...
    def LockServer(self, this, fLock): ...
