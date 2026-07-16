from time import time
from typing import Final, TypeAlias, final

from _libspacetime_cffi import ffi, lib

_MarsTimeTuple: TypeAlias = tuple[int, int, int, int, int, int, int, int]

# TODO: Match constructor of struct_time
# TODO: How to make it match from when we get the ctype?
# TODO: Make it print like this:
# Mars time called from FFI: (191, 1, 4, 0, 0, 0, 0, 0)
# strptime called from python: time.struct_time(tm_year=2000, tm_mon=10, tm_mday=10, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=1, tm_yday=284, tm_isdst=-1)
@final
class struct_marstime(_MarsTimeTuple):
    # this is cool
    # no isdst var
    __match_args__: Final = ("mars_tm_year", "mars_tm_mon", "mars_tm_msol", "mars_tm_hour", "mars_tm_min", "mars_tm_sec", "mars_tm_wsol", "mars_tm_ysol")

    @property
    def mars_tm_year(self) -> int:
        ...

    @property
    def mars_tm_mon(self) -> int:
        ...

    @property
    def mars_tm_msol(self) -> int:
        ...

    @property
    def mars_tm_hour(self) -> int:
        ...

    @property
    def mars_tm_min(self) -> int:
        ...

    @property
    def mars_tm_sec(self) -> int:
        ...

    @property
    def mars_tm_wsol(self) -> int:
        ...



def mars_time() -> float:
    return lib.earth_time_to_msd(int(time())) * 86400.0

def strfmarstime(format: str, time_tuple: _MarsTimeTuple | struct_marstime = ..., /) -> str:
    _format = ffi.new("char[]", format.encode("utf-8"))
    tm = ffi.new("struct mars_tm*", time_tuple)
    _buf = ffi.new("char[]", 256)

    # 256 is arbitrary
    lib.strfmarstime(_buf, 256, _format, tm)
    return ffi.string(_buf).decode()

def strpmarstime(data_string: str, format: str = "%a %b %d %H:%M:%S %Y", /) -> struct_marstime:
    # There may be a better way to do this..
    _data_string = ffi.new("char[]", data_string.encode("utf-8"))
    _format = ffi.new("char[]", format.encode("utf-8"))
    _out = ffi.new("struct mars_tm*")
    lib.strpmarstime(_data_string, _format, _out)
    return struct_marstime((_out.mars_tm_year, _out.mars_tm_mon, _out.mars_tm_msol, _out.mars_tm_hour, _out.mars_tm_min, _out.mars_tm_sec, _out.mars_tm_wsol, _out.mars_tm_ysol))
