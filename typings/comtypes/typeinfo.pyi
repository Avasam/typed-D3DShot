import ctypes
from ctypes import _Pointer, c_int, c_void_p
from ctypes.wintypes import DWORD, WCHAR
from typing import Any, Sequence, TypeVar, overload

from _typeshed import Incomplete
from comtypes import (
    BSTR as BSTR,
    COMMETHOD as COMMETHOD,
    GUID as GUID,
    IID as IID,
    STDMETHOD as STDMETHOD,
    TYPE_CHECKING as TYPE_CHECKING,
    IUnknown as IUnknown,
)
from comtypes.automation import (
    DISPID as DISPID,
    DISPPARAMS as DISPPARAMS,
    EXCEPINFO as EXCEPINFO,
    LCID as LCID,
    SCODE as SCODE,
    VARIANT as VARIANT,
    VARIANTARG as VARIANTARG,
    VARTYPE as VARTYPE,
    tagVARIANT as tagVARIANT,
)

_T_IUnknown = TypeVar("_T_IUnknown", bound=IUnknown)

is_64_bit: Incomplete
BOOL = c_int
HREFTYPE = DWORD
INT = c_int
MEMBERID = DISPID
OLECHAR = WCHAR
PVOID = c_void_p
SHORT = ctypes.c_short
ULONG_PTR: Incomplete
USHORT = ctypes.c_ushort
LPOLESTR: Incomplete
tagSYSKIND = c_int
SYS_WIN16: int
SYS_WIN32: int
SYS_MAC: int
SYS_WIN64: int
SYSKIND = tagSYSKIND
tagREGKIND = c_int
REGKIND_DEFAULT: int
REGKIND_REGISTER: int
REGKIND_NONE: int
REGKIND = tagREGKIND
tagTYPEKIND = c_int
TKIND_ENUM: int
TKIND_RECORD: int
TKIND_MODULE: int
TKIND_INTERFACE: int
TKIND_DISPATCH: int
TKIND_COCLASS: int
TKIND_ALIAS: int
TKIND_UNION: int
TKIND_MAX: int
TYPEKIND = tagTYPEKIND
tagINVOKEKIND = c_int
INVOKE_FUNC: int
INVOKE_PROPERTYGET: int
INVOKE_PROPERTYPUT: int
INVOKE_PROPERTYPUTREF: int
INVOKEKIND = tagINVOKEKIND
tagDESCKIND = c_int
DESCKIND_NONE: int
DESCKIND_FUNCDESC: int
DESCKIND_VARDESC: int
DESCKIND_TYPECOMP: int
DESCKIND_IMPLICITAPPOBJ: int
DESCKIND_MAX: int
DESCKIND = tagDESCKIND
tagVARKIND = c_int
VAR_PERINSTANCE: int
VAR_STATIC: int
VAR_CONST: int
VAR_DISPATCH: int
VARKIND = tagVARKIND
tagFUNCKIND = c_int
FUNC_VIRTUAL: int
FUNC_PUREVIRTUAL: int
FUNC_NONVIRTUAL: int
FUNC_STATIC: int
FUNC_DISPATCH: int
FUNCKIND = tagFUNCKIND
tagCALLCONV = c_int
CC_FASTCALL: int
CC_CDECL: int
CC_MSCPASCAL: int
CC_PASCAL: int
CC_MACPASCAL: int
CC_STDCALL: int
CC_FPFASTCALL: int
CC_SYSCALL: int
CC_MPWCDECL: int
CC_MPWPASCAL: int
CC_MAX: int
CALLCONV = tagCALLCONV
IMPLTYPEFLAG_FDEFAULT: int
IMPLTYPEFLAG_FSOURCE: int
IMPLTYPEFLAG_FRESTRICTED: int
IMPLTYPEFLAG_FDEFAULTVTABLE: int
tagTYPEFLAGS = c_int
TYPEFLAG_FAPPOBJECT: int
TYPEFLAG_FCANCREATE: int
TYPEFLAG_FLICENSED: int
TYPEFLAG_FPREDECLID: int
TYPEFLAG_FHIDDEN: int
TYPEFLAG_FCONTROL: int
TYPEFLAG_FDUAL: int
TYPEFLAG_FNONEXTENSIBLE: int
TYPEFLAG_FOLEAUTOMATION: int
TYPEFLAG_FRESTRICTED: int
TYPEFLAG_FAGGREGATABLE: int
TYPEFLAG_FREPLACEABLE: int
TYPEFLAG_FDISPATCHABLE: int
TYPEFLAG_FREVERSEBIND: int
TYPEFLAG_FPROXY: int
TYPEFLAGS = tagTYPEFLAGS
tagFUNCFLAGS = c_int
FUNCFLAG_FRESTRICTED: int
FUNCFLAG_FSOURCE: int
FUNCFLAG_FBINDABLE: int
FUNCFLAG_FREQUESTEDIT: int
FUNCFLAG_FDISPLAYBIND: int
FUNCFLAG_FDEFAULTBIND: int
FUNCFLAG_FHIDDEN: int
FUNCFLAG_FUSESGETLASTERROR: int
FUNCFLAG_FDEFAULTCOLLELEM: int
FUNCFLAG_FUIDEFAULT: int
FUNCFLAG_FNONBROWSABLE: int
FUNCFLAG_FREPLACEABLE: int
FUNCFLAG_FIMMEDIATEBIND: int
FUNCFLAGS = tagFUNCFLAGS
tagVARFLAGS = c_int
VARFLAG_FREADONLY: int
VARFLAG_FSOURCE: int
VARFLAG_FBINDABLE: int
VARFLAG_FREQUESTEDIT: int
VARFLAG_FDISPLAYBIND: int
VARFLAG_FDEFAULTBIND: int
VARFLAG_FHIDDEN: int
VARFLAG_FRESTRICTED: int
VARFLAG_FDEFAULTCOLLELEM: int
VARFLAG_FUIDEFAULT: int
VARFLAG_FNONBROWSABLE: int
VARFLAG_FREPLACEABLE: int
VARFLAG_FIMMEDIATEBIND: int
VARFLAGS = tagVARFLAGS
PARAMFLAG_NONE: int
PARAMFLAG_FIN: int
PARAMFLAG_FOUT: int
PARAMFLAG_FLCID: int
PARAMFLAG_FRETVAL: int
PARAMFLAG_FOPT: int
PARAMFLAG_FHASDEFAULT: int
PARAMFLAG_FHASCUSTDATA: int

class ITypeLib(IUnknown):
    def GetTypeInfoCount(self) -> int: ...
    def GetTypeInfo(self, index: int) -> ITypeInfo: ...
    def GetTypeInfoType(self, index: int) -> int: ...
    def GetTypeInfoOfGuid(self, guid: GUID) -> ITypeInfo: ...
    def GetTypeComp(self) -> ITypeComp: ...
    def GetDocumentation(self, index: int) -> tuple[str, str, int, str | None]: ...
    def ReleaseTLibAttr(self, ptla: _Pointer[TLIBATTR]) -> int: ...
    def GetLibAttr(self) -> TLIBATTR: ...
    def IsName(self, name: str, lHashVal: int = 0) -> str | None: ...
    def FindName(self, name: str, lHashVal: int = 0) -> tuple[int, ITypeInfo] | None: ...

@overload
def fix_name(name: None) -> None: ...
@overload
def fix_name(name: str) -> str: ...

class ITypeInfo(IUnknown):
    def GetTypeComp(self) -> ITypeComp: ...
    def GetRefTypeOfImplType(self, index: int) -> int: ...
    def GetImplTypeFlags(self, index: int) -> int: ...
    def GetDllEntry(self, memid: int, invkind: int) -> tuple[str | None, str | None, int]: ...
    def GetRefTypeInfo(self, href: int) -> ITypeInfo: ...
    def GetMops(self, index: int) -> str | None: ...
    def GetContainingTypeLib(self) -> tuple[ITypeLib, int]: ...
    def ReleaseTypeAttr(self, pTypeAttr: _Pointer[TYPEATTR]) -> int: ...
    def ReleaseFuncDesc(self, pFuncDesc: _Pointer[FUNCDESC]) -> int: ...
    def ReleaseVarDesc(self, pVarDesc: _Pointer[VARDESC]) -> int: ...
    def GetTypeAttr(self): ...
    def GetDocumentation(self, memid): ...
    def GetFuncDesc(self, index): ...
    def GetVarDesc(self, index): ...
    def GetNames(self, memid: int, count: int = 1) -> list[str]: ...
    def GetIDsOfNames(self, *names: str) -> list[int]: ...
    def AddressOfMember(self, memid, invkind): ...
    def CreateInstance(
        self,
        punkouter: type[_Pointer[IUnknown]] | None = None,
        interface: type[_T_IUnknown] = ...,  # pyright: ignore[reportInvalidTypeVarUse]
        iid: GUID | None = None,
    ) -> _T_IUnknown: ...

class ITypeComp(IUnknown):
    def Bind(
        self, name: str, flags: int = 0, lHashVal: int = 0
    ) -> tuple[str, FUNCDESC | VARDESC | ITypeComp] | None: ...
    def BindType(self, name: str, lHashVal: int = 0) -> tuple[ITypeInfo, ITypeComp]: ...

class ICreateTypeLib(IUnknown): ...
class ICreateTypeLib2(ICreateTypeLib): ...

class ICreateTypeInfo(IUnknown):
    def SetFuncAndParamNames(self, index: int, *names: str) -> int: ...

class IRecordInfo(IUnknown):
    def GetFieldNames(self, *args: Any) -> list[str | None]: ...

def GetRecordInfoFromTypeInfo(tinfo: ITypeInfo) -> IRecordInfo: ...
def GetRecordInfoFromGuids(
    rGuidTypeLib: str, verMajor: int, verMinor: int, lcid: int, rGuidTypeInfo: str
) -> IRecordInfo: ...
def LoadRegTypeLib(
    guid: str | GUID, wMajorVerNum: int, wMinorVerNum: int, lcid: int = 0
) -> ITypeLib: ...
def LoadTypeLibEx(szFile: str, regkind: int = ...) -> ITypeLib: ...
def LoadTypeLib(szFile: str) -> ITypeLib: ...
def UnRegisterTypeLib(
    libID: str, wVerMajor: int, wVerMinor: int, lcid: int = 0, syskind: int = ...
) -> int: ...
def RegisterTypeLib(tlib: ITypeLib, fullpath: str, helpdir: str | None = None) -> int: ...
def CreateTypeLib(filename: str, syskind: int = ...) -> ICreateTypeLib2: ...
def QueryPathOfRegTypeLib(libid: str, wVerMajor: int, wVerMinor: int, lcid: int = 0) -> str: ...

class tagTLIBATTR(ctypes.Structure):
    guid: GUID
    lcid: int
    syskind: int
    wMajorVerNum: int
    wMinorVerNum: int
    wLibFlags: int

TLIBATTR = tagTLIBATTR

class tagTYPEATTR(ctypes.Structure):
    guid: GUID
    lcid: int
    dwReserved: int
    memidConstructor: int
    memidDestructor: int
    lpstrSchema: str
    cbSizeInstance: int
    typekind: int
    cFuncs: int
    cVars: int
    cImplTypes: int
    cbSizeVft: int
    cbAlignment: int
    wTypeFlags: int
    wMajorVerNum: int
    wMinorVerNum: int
    tdescAlias: TYPEDESC
    idldescType: IDLDESC

TYPEATTR = tagTYPEATTR

class tagFUNCDESC(ctypes.Structure):
    memid: int
    lprgscode: int
    lprgelemdescParam: Sequence[ELEMDESC]
    funckind: int
    invkind: int
    callconv: int
    cParams: int
    cParamsOpt: int
    oVft: int
    cScodes: int
    elemdescFunc: ELEMDESC
    wFuncFlags: int

FUNCDESC = tagFUNCDESC

class tagVARDESC(ctypes.Structure):
    memid: int
    lpstrSchema: str
    _: N10tagVARDESC5DOLLAR_205E
    elemdescVar: ELEMDESC
    wVarFlags: int
    varkind: int

VARDESC = tagVARDESC

class tagBINDPTR(ctypes.Union):
    lpfuncdesc: _Pointer[FUNCDESC]
    lpvardesc: _Pointer[VARDESC]
    lptcomp: ITypeComp

BINDPTR = tagBINDPTR

class tagTYPEDESC(ctypes.Structure):
    _: N11tagTYPEDESC5DOLLAR_203E
    vt: int

TYPEDESC = tagTYPEDESC

class tagIDLDESC(ctypes.Structure):
    dwReserved: int
    wIDLFlags: int

IDLDESC = tagIDLDESC

class tagARRAYDESC(ctypes.Structure):
    tdescElem: TYPEDESC
    cDims: int
    rgbounds: Sequence[SAFEARRAYBOUND]

class IProvideClassInfo(IUnknown):
    def GetClassInfo(self) -> ITypeInfo: ...

class IProvideClassInfo2(IProvideClassInfo):
    def GetGUID(self, dwGuidKind: int) -> GUID: ...

class N11tagTYPEDESC5DOLLAR_203E(ctypes.Union):
    lptdesc: TYPEDESC
    lpadesc: tagARRAYDESC
    hreftype: int

class N10tagVARDESC5DOLLAR_205E(ctypes.Union):
    oInst: int
    lpvarValue: VARIANT

class tagELEMDESC(ctypes.Structure):
    tdesc: TYPEDESC
    _: N11tagELEMDESC5DOLLAR_204E

class N11tagELEMDESC5DOLLAR_204E(ctypes.Union):
    idldesc: IDLDESC
    paramdesc: PARAMDESC

class tagPARAMDESC(ctypes.Structure):
    pparamdescex: tagPARAMDESCEX
    wParamFlags: int

class tagPARAMDESCEX(ctypes.Structure):
    cBytes: int
    varDefaultValue: VARIANTARG

LPPARAMDESCEX: Incomplete
PARAMDESC = tagPARAMDESC
ELEMDESC = tagELEMDESC

class tagSAFEARRAYBOUND(ctypes.Structure):
    cElements: int
    lLbound: int

SAFEARRAYBOUND = tagSAFEARRAYBOUND
__known_symbols__: Incomplete
