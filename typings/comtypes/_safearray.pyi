from ctypes import *
from ctypes.wintypes import *

from _typeshed import Incomplete
from comtypes import GUID as GUID, HRESULT as HRESULT

VARTYPE = c_ushort
PVOID = c_void_p
USHORT = c_ushort

class tagSAFEARRAYBOUND(Structure): ...

SAFEARRAYBOUND = tagSAFEARRAYBOUND

class tagSAFEARRAY(Structure): ...

SAFEARRAY = tagSAFEARRAY
SafeArrayAccessData: Incomplete
SafeArrayCreateVectorEx: Incomplete
SafeArrayCreateEx: Incomplete
SafeArrayCreate: Incomplete
SafeArrayUnaccessData: Incomplete

def SafeArrayGetVartype(pa): ...

SafeArrayGetElement: Incomplete
SafeArrayDestroy: Incomplete
SafeArrayCreateVector: Incomplete
SafeArrayDestroyData: Incomplete
SafeArrayGetDim: Incomplete

def SafeArrayGetLBound(pa, dim): ...
def SafeArrayGetUBound(pa, dim): ...

SafeArrayLock: Incomplete
SafeArrayPtrOfIndex: Incomplete
SafeArrayUnlock: Incomplete

def SafeArrayGetIID(pa): ...

SafeArrayDestroyDescriptor: Incomplete
