from ctypes import *

from _typeshed import Incomplete
from comtypes import COMMETHOD as COMMETHOD, GUID as GUID, IUnknown as IUnknown

class tagPALETTEENTRY(Structure): ...
class tagLOGPALETTE(Structure): ...
class tagDVTARGETDEVICE(Structure): ...

class tagExtentInfo(Structure):
    cb: Incomplete
    def __init__(self, *args, **kw) -> None: ...

DVEXTENTINFO = tagExtentInfo
IAdviseSink = IUnknown

class IViewObject(IUnknown): ...
class IViewObject2(IViewObject): ...
class IViewObjectEx(IViewObject2): ...

DVASPECT = c_int
DVASPECT_CONTENT: int
DVASPECT_THUMBNAIL: int
DVASPECT_ICON: int
DVASPECT_DOCPRINT: int
DVASPECT2 = c_int
DVASPECT_OPAQUE: int
DVASPECT_TRANSPARENT: int
DVEXTENTMODE = c_int
DVEXTENT_CONTENT: int
DVEXTENT_INTEGRAL: int
