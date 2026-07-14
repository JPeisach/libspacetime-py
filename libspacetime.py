from time import time
from datetime import datetime

from _libspacetime_cffi import ffi, lib

def mars_time() -> float:
    return lib.earth_time_to_msd(int(time())) * 86400.0
