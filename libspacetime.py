from time import time
from typing import Final, TypeAlias, final

from _libspacetime_cffi import ffi, lib

_MarsTimeTuple: TypeAlias = tuple[int, int, int, int, int, int, int, int]

# TODO: Match constructor of struct_time
# TODO: How to make it match from when we get the ctype?
@final
class struct_marstime(_MarsTimeTuple):
    # this is cool
    # no isdst var
    __match_args__: Final = ("mars_tm_year", "mars_tm_mon", "mars_tm_msol", "mars_tm_hour", "mars_tm_min", "mars_tm_sec", "mars_tm_wsol", "mars_tm_ysol")

    def __init__(self, mars_tm_year, mars_tm_mon, mars_tm_msol, mars_tm_hour, mars_tm_min, mars_tm_sec, mars_tm_wsol, mars_tm_ysol):
        self.mars_tm_year = mars_tm_year
        self.mars_tm_mon = mars_tm_mon
        self.mars_tm_msol = mars_tm_msol
        self.mars_tm_hour = mars_tm_hour
        self.mars_tm_min = mars_tm_min
        self.mars_tm_sec = mars_tm_sec
        self.mars_tm_wsol = mars_tm_wsol
        self.mars_tm_ysol = mars_tm_ysol

    # Python actually has a module (written in C), so that is why it prints out
    # like "time.struct_time(tm_year=foo, tm_mon=bar, ...)"
    # So we need to do this ourselves unless we use a module.
    # Month starts at 0, instead of 1, so add 1
    def __str__(self) -> str:
        return f"libspacetime.struct_marstime(tm_year={self.mars_tm_year}, tm_mon={self.mars_tm_mon + 1}, tm_msol={self.mars_tm_msol}, tm_hour={self.mars_tm_hour}, tm_min={self.mars_tm_min}, tm_sec={self.mars_tm_sec}, tm_wsol={self.mars_tm_wsol}, tm_ysol={self.mars_tm_ysol}"

    def __repr__(self) -> str:
        # see above
        return self.__str__()

def mars_time() -> float:
    return lib.earth_time_to_msd(int(time())) * 86400.0

def ammarstime(seconds: float | int | None = None, /) -> struct_marstime:
    # If secs is None, use current time.
    if seconds is None:
        seconds = int(mars_time())

    _out = lib.ammarstime(ffi.new("long*", seconds))
    return struct_marstime(mars_tm_year=_out.mars_tm_year, mars_tm_mon=_out.mars_tm_mon, mars_tm_msol=_out.mars_tm_msol, mars_tm_hour=_out.mars_tm_hour, mars_tm_min=_out.mars_tm_min, mars_tm_sec=_out.mars_tm_sec, mars_tm_wsol=_out.mars_tm_wsol, mars_tm_ysol=_out.mars_tm_ysol)

# TODO: Timezones.
def localmarstime(seconds: float | int | None = None, /) -> struct_marstime:
    # Until timezones exist, just call ammarstime.
    # Which is just what the library does.
    # When that changes this won't need an update (hopefully)..
    # validation checks may be needed
    # If secs is None, use current time.
    if seconds is None:
        seconds = int(mars_time())

    return ammarstime(seconds)

# TODO: I don't get the rationale for how a float could be returned for this.
# TODO: If time cannot be represented raise error
def mkmarstime(time_tuple: _MarsTimeTuple | struct_marstime, /) -> float:
    # As far as I know.. the best way to do this
    tm = ffi.new("struct mars_tm*")
    tm.mars_tm_year = time_tuple.mars_tm_year
    tm.mars_tm_mon = time_tuple.mars_tm_mon
    tm.mars_tm_msol = time_tuple.mars_tm_msol
    tm.mars_tm_hour = time_tuple.mars_tm_hour
    tm.mars_tm_min = time_tuple.mars_tm_min
    tm.mars_tm_sec = time_tuple.mars_tm_sec
    tm.mars_tm_wsol = time_tuple.mars_tm_wsol
    tm.mars_tm_ysol = time_tuple.mars_tm_ysol
    return lib.mkmarstime(tm)

# TODO: in strftime, python checks for legal formats
def strfmarstime(format: str, time_tuple: _MarsTimeTuple | struct_marstime = ..., /) -> str:
    _format = ffi.new("char[]", format.encode("utf-8"))
    tm = ffi.new("struct mars_tm*", time_tuple)
    _buf = ffi.new("char[]", 256)

    # 256 is arbitrary
    lib.strfmarstime(_buf, 256, _format, tm)
    return ffi.string(_buf).decode()

# TODO: in strptime, python checks for legal formats
def strpmarstime(data_string: str, format: str = "%a %b %d %H:%M:%S %Y", /) -> struct_marstime:
    # There may be a better way to do this..
    _data_string = ffi.new("char[]", data_string.encode("utf-8"))
    _format = ffi.new("char[]", format.encode("utf-8"))
    _out = ffi.new("struct mars_tm*")
    lib.strpmarstime(_data_string, _format, _out)

    return struct_marstime(mars_tm_year=_out.mars_tm_year, mars_tm_mon=_out.mars_tm_mon, mars_tm_msol=_out.mars_tm_msol, mars_tm_hour=_out.mars_tm_hour, mars_tm_min=_out.mars_tm_min, mars_tm_sec=_out.mars_tm_sec, mars_tm_wsol=_out.mars_tm_wsol, mars_tm_ysol=_out.mars_tm_ysol)
