# Copyright © 2025 Borden Rhodes
#
# dvdcss.py is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.


"""
ctypes wrapper to VideoLAN's libdvdcss API header files.

These are low-level wrappers. For most purposes, you want to use the module's
DVD class instead. Refer to the C header documentation, such as it is, for
usage information.

The wrappers try to appear in the same order as the original header file. This
module wraps definitions from outside the libdvdcss API where those definitions
are necessary to complete a function prototype. Further, wrappers will appear
out of order from the header file when this module needs to define something
before defining something else. Python doesn't have forward declarations to
allow the original ordering.

libdvdread handles CSS scrambling, which may be illegal in your jurisdiction.
This is offered for completeness. It does not yet control for the library not
being installed.
"""

import ctypes
import os

_POSIX_DVDCSS_LIB = "libdvdcss.so.2"
"""
Name of the libdvdcss shared object library on POSIX systems to be loaded.
"""

if os.name == 'posix':
    _libdvdcss = ctypes.CDLL(_POSIX_DVDCSS_LIB)
elif os.name == 'nt':
    raise RuntimeError("Windows support not yet implemented. Sorry!")
else:
    raise RuntimeError(f"Unsupported operating system {os.name}. "
                       + "This is almost certainly a bug.")

# <editor-fold desc="Grouping for linux/limits.h header file.">
_PATH_MAX = 4096
"""
PATH_MAX preprocessor definition.

Source: linux/limits.h:13
"""


# </editor-fold>

# <editor-fold desc="Grouping for x86_64-linux-gnu/bits/types/struct_iovec.h header file.">
class _IOVec(ctypes.Structure):
    """
    Struct for the struct_iovec iovec type.

    TODO: This appears platform-dependent. Not sure if this is correct
    Source: x86_64-linux-gnu/bits/types/struct_iovec.h:26
    """
    _fields_ = [
        ("iov_base", ctypes.c_void_p),
        ("iov_len", ctypes.c_size_t)
    ]


# </editor-fold>

# <editor-fold desc="Grouping for libdvdcss/src/css.h header file.">
_DVD_KEY_SIZE = 5
"""
DVD_KEY_SIZE preprocessor definition.

Source: libdvdcss/src/css.h:38
"""

_DVD_KEY = ctypes.c_uint8 * _DVD_KEY_SIZE
"""
uint8 array of length _DVD_KEY_SIZE

Source: libdvdcss/src/css.h:40
"""


class _DVDTitle(ctypes.Structure):
    """
    Struct for the libdvdcss dvd_title type.

    Source: libdvdcss/src/css.h:42
    """


_DVDTitle._fields_ = [
    ("i_startlb", ctypes.c_int),
    ("p_key", _DVD_KEY),
    ("p_next", ctypes.POINTER(_DVDTitle))
]


class _CSS(ctypes.Structure):
    """
    Struct for the libdvdcss css type.

    Source: libdvdcss/src/css.h:49
    """
    _fields_ = [
        ("i_agid", ctypes.c_int),
        ("p_bus_key", _DVD_KEY),
        ("p_disc_key", _DVD_KEY),
        ("p_title_key", _DVD_KEY)
    ]


# </editor-fold>

# <editor-fold desc="Grouping for libdvdcss/src/libdvdcss.h header file.">

# For the purposes of function prototypes enums are just int wrappers in C.
# Omitting an enum type ought not to break anything. Happy to stand corrected.
_DVDCSSMethod = ctypes.c_int
"""
Representation of the dvdcss_method enum.

Source: libdvdcss/src/libdvdcss.h:36
"""


class _DVDCSSS(ctypes.Structure):
    """
    Struct for the libdvdcss dvdcss_s type.

    Source: libdvdcss/src/libdvdcss.h:44
    """


_DVDCSST = ctypes.POINTER(_DVDCSSS)
"""
Struct for the libdvdcss dvdcss_t type.

Source: libdvdcss/src/dvdcss/dvdcss.h:43
"""


# </editor-fold>

# <editor-fold desc="Grouping for libdvdcss/src/dvdcss/dvdcss.h header file.">
class _DVDCSSStreamCB(ctypes.Structure):
    """
    Struct for the libdvdcss dvdcss_stream_cb type.

    Source: libdvdcss/src/dvdcss/dvdcss.h:46
    """
    _fields_ = [
        ("pf_seek", ctypes.CFUNCTYPE(
            ctypes.POINTER(ctypes.c_int),
            ctypes.c_void_p,
            ctypes.c_uint64)),
        ("pf_read", ctypes.CFUNCTYPE(
            ctypes.POINTER(ctypes.c_int),
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_int)),
        ("pf_readv", ctypes.CFUNCTYPE(
            ctypes.POINTER(ctypes.c_int),
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_int))
    ]


dvdcss_open = _libdvdcss.dvdcss_open
"""
Function wrapper for libdvdcss dvdcss_open.

Source: libdvdcss/src/dvdcss/dvdcss.h:90
"""
dvdcss_open.restype = _DVDCSST
dvdcss_open.argtypes = (
    ctypes.POINTER(ctypes.c_char),
)

dvdcss_open_stream = _libdvdcss.dvdcss_open_stream
"""
Function wrapper for libdvdcss dvdcss_open_stream.

Source: libdvdcss/src/dvdcss/dvdcss.h:91
"""
dvdcss_open_stream.restype = _DVDCSST
dvdcss_open_stream.argtypes = (
    ctypes.c_void_p,
    ctypes.POINTER(_DVDCSSStreamCB)
)

dvdcss_close = _libdvdcss.dvdcss_close
"""
Function wrapper for libdvdcss dvdcss_close.

Source: libdvdcss/src/dvdcss/dvdcss.h:93
"""
dvdcss_close.restype = ctypes.c_int
dvdcss_close.argtypes = (
    _DVDCSST,
)

dvdcss_seek = _libdvdcss.dvdcss_seek
"""
Function wrapper for libdvdcss dvdcss_seek.

Source: libdvdcss/src/dvdcss/dvdcss.h:94
"""
dvdcss_seek.restype = ctypes.c_int
dvdcss_seek.argtypes = (
    _DVDCSST,
    ctypes.c_int,
    ctypes.c_int
)

dvdcss_read = _libdvdcss.dvdcss_read
"""
Function wrapper for libdvdcss dvdcss_read.

Source: libdvdcss/src/dvdcss/dvdcss.h:97
"""
dvdcss_read.restype = ctypes.c_int
dvdcss_read.argtypes = (
    _DVDCSST,
    ctypes.c_void_p,
    ctypes.c_int,
    ctypes.c_int
)

dvdcss_readv = _libdvdcss.dvdcss_readv
"""
Function wrapper for libdvdcss dvdcss_readv.

Source: libdvdcss/src/dvdcss/dvdcss.h:101
"""
dvdcss_readv.restype = ctypes.c_int
dvdcss_readv.argtypes = (
    _DVDCSST,
    ctypes.c_void_p,
    ctypes.c_int,
    ctypes.c_int
)

dvdcss_error = _libdvdcss.dvdcss_error
"""
Function wrapper for libdvdcss dvdcss_error.

Source: libdvdcss/src/dvdcss/dvdcss.h:105
"""
dvdcss_error.restype = ctypes.POINTER(ctypes.c_char)
dvdcss_error.argtypes = (
    _DVDCSST,
)

dvdcss_is_scrambled = _libdvdcss.dvdcss_is_scrambled
"""
Function wrapper for libdvdcss dvdcss_is_scrambled.

Source: libdvdcss/src/dvdcss/dvdcss.h:107
"""
dvdcss_is_scrambled.restype = ctypes.c_int
dvdcss_is_scrambled.argtypes = (
    _DVDCSST,
)
# </editor-fold>


# <editor-fold desc="DVDCSSS/T._fields_ definition.">

# Sadly, this has to be done all the way down here because of forward
# declarations.
_DVDCSSS._fields_ = [
    ("psz_device", ctypes.POINTER(ctypes.c_char)),
    ("i_fd", ctypes.c_int),
    ("i_pos", ctypes.c_int),
    ("pf_seek", ctypes.CFUNCTYPE(
        ctypes.POINTER(ctypes.c_int),
        _DVDCSST,
        ctypes.c_int)),
    ("pf_read", ctypes.CFUNCTYPE(
        ctypes.POINTER(ctypes.c_int),
        _DVDCSST,
        ctypes.c_void_p,
        ctypes.c_int)),
    ("pf_readv", ctypes.CFUNCTYPE(
        ctypes.POINTER(ctypes.c_int),
        _DVDCSST,
        ctypes.POINTER(_IOVec),
        ctypes.c_int)),
    ("i_method", _DVDCSSMethod),
    ("css", _CSS),
    ("b_ioctls", ctypes.c_int),
    ("b_scrambled", ctypes.c_int),
    ("p_titles", ctypes.POINTER(_DVDTitle)),
    ("psz_cachefile", ctypes.c_char * _PATH_MAX),
    ("psz_block", ctypes.POINTER(ctypes.c_char)),
    ("psz_error", ctypes.POINTER(ctypes.c_char)),
    ("b_errors", ctypes.c_int),
    ("b_debug", ctypes.c_int)
]
# The interpreter is wrong. Sequence has an append() method.
if os.name == 'nt':
    _DVDCSSS._fields_.append(
        ("b_file", ctypes.c_int)
    )
    _DVDCSSS._fields_.append(
        ("p_readv_buffer", ctypes.POINTER(ctypes.c_char))
    )
    _DVDCSSS._fields_.append(
        ("i_readv_buf_size", ctypes.c_int)
    )
# NT section finished, continue adding struct elements
_DVDCSSS._fields_.append(
    ("p_stream", ctypes.c_void_p)
)
_DVDCSSS._fields_.append(
    ("p_stream_cb", ctypes.POINTER(_DVDCSSStreamCB))
)
# </editor-fold>
