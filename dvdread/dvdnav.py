# Copyright © 2025 Borden Rhodes
#
# dvdnav.py is free software: you can redistribute it and/or modify it under
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
ctypes wrapper to VideoLAN's libdvdnav library header files.

These are low-level wrappers. For most purposes, you want to use the module's
DVD class instead. Refer to the C header documentation, such as it is, for
usage information.

The wrappers try to appear in the same order as the original header file. This
module wraps definitions from outside the libdvdnav API where those definitions
are necessary to complete a function prototype. Further, wrappers will appear
out of order from the header file when this module needs to define something
before defining something else. Python doesn't have forward declarations to
allow the original ordering.
"""

import ctypes
import os

from dvdread import (
    _AudioAttrT, _DVDFileT, _DVDReaderStreamCB, _DVDReaderT, _DSIT,
    _IFOHandleT, _PCIT, _PGCT, _SubPAttrT, _UserOpsT, _VMCmdT
)

_POSIX_DVDNAV_LIB = "libdvdnav.so.4"
"""
Name of the libdvdnav shared object library on POSIX systems to be loaded.
"""

_WIN_DVDNAV_LIB = os.path.expandvars(
    "%PROGRAMFILES%/VideoLAN/VLC/plugins/access/libdvdnav_plugin.dll"
)
"""
Path to the libdvdnav DLL on Windows systems.
"""

if os.name == 'posix':
    _libdvdnav = ctypes.CDLL(_POSIX_DVDNAV_LIB)
elif os.name == 'nt':
    _libdvdnav = ctypes.CDLL(_WIN_DVDNAV_LIB)
else:
    raise RuntimeError(f"Unsupported operating system {os.name}. "
                       + "This is almost certainly a bug.")

_PThreadMutexT = ctypes.c_void_p
"""
Representation of the pthread_mutex_t union type.

TODO: Not sure that this will work, as it's supposed to be opaque and system
dependent.
"""

# <editor-fold desc="Grouping for libdvdnav/src/read_cache.c source file.">
_READ_CACHE_CHUNKS = 10
"""
Preprocessor alias for READ_CACHE_CHUNKS system value.

Source: libdvdnav/src/read_cache.c:44 
"""


class _ReadCacheChunkS(ctypes.Structure):
    """
    Struct for the libdvdnav read_cache_chunk_s type.

    Source: libdvdnav/src/read_cache.c:52
    """
    _fields_ = [
        ("cache_buffer", ctypes.POINTER(ctypes.c_uint8)),
        ("cache_buffer_base", ctypes.POINTER(ctypes.c_uint8)),
        ("cache_start_sector", ctypes.c_int32),
        ("cache_read_count", ctypes.c_int32),
        ("cache_block_count", ctypes.c_size_t),
        ("cache_malloc_size", ctypes.c_size_t),
        ("cache_valid", ctypes.c_int),
        ("usage_count", ctypes.c_int)
    ]


_ReadCacheChunkT = _ReadCacheChunkS
"""
Representation of the read_cache_chunk_t typedef.

Source: libdvdnav/src/read_cache.c:61
"""


class _ReadCacheS(ctypes.Structure):
    """
    Struct for the libdvdnav read_cache_s type.

    Source: libdvdnav/src/read_cache.c:63
    """


_ReadCacheS._fields_ = [
    ("chunk", _ReadCacheChunkT * _READ_CACHE_CHUNKS),
    ("current", ctypes.c_int),
    ("freeing", ctypes.c_int),
    ("read_ahead_size", ctypes.c_uint32),
    ("read_ahead_incr", ctypes.c_int),
    ("last_sector", ctypes.c_int),
    ("lock", _PThreadMutexT)
]


# </editor-fold>

# <editor-fold desc="Grouping for libdvdnav/src/vm/decoder.h header file.">
class _RegistersT(ctypes.Structure):
    """
    Struct for the libdvdnav registers_t type.

    TODO: used c_time_t for timeval. Not sure if this is correct.
    Source: libdvdnav/src/vm/decoder.h:80
    """
    _fields_ = [
        ("SPRM", ctypes.c_uint16 * 24),
        ("GPRM", ctypes.c_uint16 * 16),
        ("GPRM_mode", ctypes.c_uint8 * 16),
        ("GPRM_time", ctypes.c_time_t * 16)
    ]


# </editor-fold>

# <editor-fold desc="Grouping for dvdnav/dvd_types.h header file.">

# For the purposes of function prototypes, enums are just int wrappers in
# C. Omitting an enum type ought not to break anything. Happy to stand
# corrected.
_DVDMenuIDT = ctypes.c_int
"""
Representation of the DVDMenuID_t enum.

Source: libdvdnav/src/dvdnav/dvd_types.h:35
"""

_DVDNavStreamTypeT = ctypes.c_int
"""
Representation of the dvdnav_stream_type_t enum.

Source: libdvdnav/src/dvdnav/dvd_types.h:51
"""

_DVDDomainT = ctypes.c_int
"""
Representation of the DVDDomain_t enum.

Source: libdvdnav/src/dvdnav/dvd_types.h:57
"""


class _DVDNavHighlightAreaT(ctypes.Structure):
    """
    Struct for the libdvdnav dvdnav_highlight_area_t type.

    Source: libdvdnav/src/dvdnav/dvd_types.h:68
    """
    _fields_ = [
        ("palette", ctypes.c_uint32),
        ("sx", ctypes.c_uint16),
        ("sy", ctypes.c_uint16),
        ("ex", ctypes.c_uint16),
        ("ey", ctypes.c_uint16),
        ("pts", ctypes.c_uint32),
        ("buttonN", ctypes.c_uint32)
    ]


_DVDAudioFormatT = ctypes.c_int
"""
Representation of the DVDAudioFormat_t enum.

Source: libdvdnav/src/dvdnav/dvd_types.h:79
"""

# <editor-fold desc="Per libdvdnav/src/dvdnav/dvd_types.h, the following are unused. Including because they may be used in future.">
_DVDUOPT = ctypes.c_int
"""
Representation of the DVDUOP_t enum.

Source: libdvdnav/src/dvdnav/dvd_types.h:95
"""

_DVDParentalLevelT = ctypes.c_int
"""
Representation of the DVDParentalLevel_t enum.

Source: libdvdnav/src/dvdnav/dvd_types.h:124
"""

_DVDLangIDT = ctypes.c_uint16
"""
Representation of the DVDLangID_t typedef.

Source: libdvdnav/src/dvdnav/dvd_types.h:137
"""

_DVDCountryIDT = ctypes.c_uint16
"""
Representation of the DVDCountryID_t typedef.

Source: libdvdnav/src/dvdnav/dvd_types.h:139
"""

_DVDRegisterT = ctypes.c_uint16
"""
Representation of the DVDRegister_t typedef.

Source: libdvdnav/src/dvdnav/dvd_types.h:143
"""

_DVDBoolT = ctypes.c_int
"""
Representation of the DVDBool_t enum.

Source: libdvdnav/src/dvdnav/dvd_types.h:144
"""

_DVDGPRMArrayT = _DVDRegisterT * 16
"""
Representation of the DVDGPRMArray_t typedef.

Source: libdvdnav/src/dvdnav/dvd_types.h:148
"""

_DVDSPRMArrayT = _DVDRegisterT * 24
"""
Representation of the DVDSPRMArray_t typedef.

Source: libdvdnav/src/dvdnav/dvd_types.h:149
"""

_DVDStreamT = ctypes.c_int
"""
Representation of the DVDStream_t typedef.

Source: libdvdnav/src/dvdnav/dvd_types.h:152
"""

_DVDPTTT = ctypes.c_int
"""
Representation of the DVDPTT_t typedef.

Source: libdvdnav/src/dvdnav/dvd_types.h:153
"""

_DVDTitleT = ctypes.c_int
"""
Representation of the DVDTitle_t typedef.

Source: libdvdnav/src/dvdnav/dvd_types.h:154
"""

_DVDAngleT = ctypes.c_int
"""
Representation of the DVDAngle_t typedef.

Source: libdvdnav/src/dvdnav/dvd_types.h:157
"""


class _DVDTimecodeT(ctypes.Structure):
    """
    Struct for the libdvdnav DVDTimecode_t type.

    Source: libdvdnav/src/dvdnav/dvd_types.h:160
    """
    _fields_ = [
        ("Hours", ctypes.c_uint8),
        ("Minutes", ctypes.c_uint8),
        ("Seconds", ctypes.c_uint8),
        ("Frames", ctypes.c_uint8)
    ]


_DVDSubpictureStreamT = ctypes.c_int
"""
Representation of the DVDSubpictureStream_t typedef.

Source: libdvdnav/src/dvdnav/dvd_types.h:168
"""

_DVDAudioStreamT = ctypes.c_int
"""
Representation of the DVDAudioStream_t typedef.

Source: libdvdnav/src/dvdnav/dvd_types.h:171
"""

_DVDAudioAppModeT = ctypes.c_int
"""
Representation of the DVDAudioAppMode_t enum.

Source: libdvdnav/src/dvdnav/dvd_types.h:174
"""

_DVDAudioLangExtT = ctypes.c_int
"""
Representation of the DVDAudioLangExt_t enum.

Source: libdvdnav/src/dvdnav/dvd_types.h:182
"""

_DVDSubpictureLangExtT = ctypes.c_int
"""
Representation of the DVDSubpictureLangExt_t enum.

Source: libdvdnav/src/dvdnav/dvd_types.h:191
"""

_DVDKaraokeDownmixT = ctypes.c_int
"""
Representation of the DVDKaraokeDownmix_t enum.

Source: libdvdnav/src/dvdnav/dvd_types.h:206
"""

_DVDKaraokeDownmixMaskT = ctypes.c_int
"""
Representation of the DVDKaraokeDownmixMask_t enum.

Source: libdvdnav/src/dvdnav/dvd_types.h:222
"""

_DVDDisplayModeT = ctypes.c_int
"""
Representation of the DVDDisplayMode_t enum.

Source: libdvdnav/src/dvdnav/dvd_types.h:225
"""


class _DVDAudioAttributesT(ctypes.Structure):
    """
    Struct for the libdvdnav DVDAudioAttributes_t type.

    Source: libdvdnav/src/dvdnav/dvd_types.h:233
    """


_DVDAudioSampleFreqT = ctypes.c_int
"""
Representation of the DVDAudioSampleFreq_t typedef.

Source: libdvdnav/src/dvdnav/dvd_types.h:243
"""

_DVDAudioSampleQuantT = ctypes.c_int
"""
Representation of the DVDAudioSampleQuant_t typedef.

Source: libdvdnav/src/dvdnav/dvd_types.h:244
"""

_DVDChannelNumberT = ctypes.c_int
"""
Representation of the DVDChannelNumber_t typedef.

Source: libdvdnav/src/dvdnav/dvd_types.h:245
"""

_DVDAudioAttributesT._fields_ = [
    ("AppMode", _DVDAudioAppModeT),
    ("AudioFormat", _DVDAudioFormatT),
    ("Language", _DVDLangIDT),
    ("LanguageExtension", _DVDAudioLangExtT),
    ("HasMultichannelInfo", _DVDBoolT),
    ("SampleFrequency", _DVDAudioSampleFreqT),
    ("SampleQuantization", _DVDAudioSampleQuantT),
    ("NumberOfChannels", _DVDChannelNumberT)
]

_DVDSubpictureTypeT = ctypes.c_int
"""
Representation of the DVDSubpictureType_t enum.

Source: libdvdnav/src/dvdnav/dvd_types.h:248
"""

_DVDSubpictureCodingT = ctypes.c_int
"""
Representation of the DVDSubpictureCoding_t enum.

Source: libdvdnav/src/dvdnav/dvd_types.h:253
"""

_DVDSubpictureAttributesT = ctypes.c_int
"""
Representation of the DVDSubpictureAttributes_t enum.

Source: libdvdnav/src/dvdnav/dvd_types.h:258
"""


class _DVDVideoAttributesT(ctypes.Structure):
    """
    Struct for the libdvdnav DVDVideoAttributes_t type.

    Source: libdvdnav/src/dvdnav/dvd_types.h:233
    """


_DVDVideoCompressionT = ctypes.c_int
"""
Representation of the DVDVideoCompression_t typedef.

Source: libdvdnav/src/dvdnav/dvd_types.h:278
"""

_DVDVideoAttributesT._fields_ = [
    ("PanscanPermitted", _DVDBoolT),
    ("LetterboxPermitted", _DVDBoolT),
    ("AspectX", ctypes.c_int),
    ("AspectY", ctypes.c_int),
    ("FrameRate", ctypes.c_int),
    ("FrameHeight", ctypes.c_int),
    ("Compression", _DVDVideoCompressionT),
    ("Line21Field1InGop", _DVDBoolT),
    ("Line21Field2InGop", _DVDBoolT),
    ("more_to_come", ctypes.c_int)
]


# </editor-fold>
# </editor-fold>

# <editor-fold desc="Grouping for libdvdnav/src/vm/vm.h header file.">
class _DVDStateT(ctypes.Structure):
    """
    Struct for the libdvdnav dvd_state_t type.

    Source: libdvdnav/src/vm/vm.h:29
    """
    _fields_ = [
        ("registers", _RegistersT),
        ("domain", _DVDDomainT),
        ("vtsN", ctypes.c_int),
        ("pgc", ctypes.POINTER(_PGCT)),
        ("pgcN", ctypes.c_int),
        ("pgN", ctypes.c_int),
        ("cellN", ctypes.c_int),
        ("cell_restart", ctypes.c_int32),
        ("blockN", ctypes.c_int),
        ("rsm_vtsN", ctypes.c_int),
        ("rsm_blockN", ctypes.c_int),
        ("rsm_regs", ctypes.c_uint16 * 5),
        ("rsm_pgcN", ctypes.c_int),
        ("rsm_cellN", ctypes.c_int)
    ]


class _VMPositionS(ctypes.Structure):
    """
    Struct for the libdvdnav vm_position_s type.

    Source: libdvdnav/src/vm/vm.h:49
    """
    _fields_ = [
        ("button", ctypes.c_int16),
        ("vts", ctypes.c_int32),
        ("domain", _DVDDomainT),
        ("spu_channel", ctypes.c_int32),
        ("angle_channel", ctypes.c_int32),
        ("audio_channel", ctypes.c_int32),
        ("hop_channel", ctypes.c_int32),
        ("title", ctypes.c_int32),
        ("chapter", ctypes.c_int32),
        ("cell", ctypes.c_int32),
        ("cell_restart", ctypes.c_int32),
        ("cell_start", ctypes.c_int32),
        ("still", ctypes.c_int32),
        ("block", ctypes.c_int32)
    ]


_VMPositionT = _VMPositionS
"""
Representation of the vm_position_t typedef.

Source: libdvdnav/src/vm/vm.h:67
"""


class _VMT(ctypes.Structure):
    """
    Struct for the libdvdnav vm_t type.

    Source: libdvdnav/src/vm/vm.h:69
    """
    # _fields_ assignment is before the _DVDEventsHeader class declaration.


# </editor-fold>

# <editor-fold desc="Grouping class for libdvdnav/src/dvdnav_internal.h header file.">
_MAX_ERR_LEN = 255
"""
Preprocessor alias for MAX_ERR_LEN system value.

Source: libdvdnav/src/dvdnav_internal.h:73 
"""

_ReadCacheT = _ReadCacheS
"""
Representation of the read_cache_t typedef.

Source: libdvdnav/src/dvdnav_internal.h:87
"""


class _DVDNavVOBUS(ctypes.Structure):
    """
    Struct for the libdvdnav dvdnav_vobu_s type.

    Source: libdvdnav/src/dvdnav_internal.h:175
    """
    _fields_ = [
        ("vobu_start", ctypes.c_int32),
        ("vobu_length", ctypes.c_int32),
        ("blockN", ctypes.c_int32),
        ("vobu_next", ctypes.c_int32)
    ]


class _DVDNavS(ctypes.Structure):
    """
    Struct for the libdvdnav dvdnav_s type.

    Source: libdvdnav/src/dvdnav_internal.h:184
    """
    # _fields_ assignment is before the _DVDEventsHeader class declaration.


_DVDNavT = _DVDNavS
"""
Representation of the dvdnav_t typedef.

Source: libdvdnav/src/dvdnav/dvdnav.h:51
"""
# </editor-fold>

# <editor-fold desc="Grouping for dvdnav/dvdnav.h header file.">

_DVDNavStatusT = ctypes.c_int32
"""
Representation of the dvdnav_status_t typedef.

Source: libdvdnav/src/dvdnav/dvdnav.h:54
"""

_DVDNavStreamCB = _DVDReaderStreamCB
"""
Representation of the dvdnav_stream_cb typedef.

Source: libdvdnav/src/dvdnav/dvdnav.h:56
"""

_DVDNavLoggerLevelT = ctypes.c_int
"""
Representation of the dvdnav_logger_level_t enum.

Source: libdvdnav/src/dvdnav/dvdnav.h:73
"""


class _DVDNavLoggerCB(ctypes.Structure):
    """
    Struct for the libdvdnav dvdnav_logger_cb type.

    TODO: Takes variadic va_list. Figure out how to resolve
    Source: libdvdnav/src/dvdnav/dvdnav.h:81
    """


_DVDNavLoggerCB._fields_ = [
    ("pf_log", ctypes.CFUNCTYPE(
        ctypes.c_void_p,
        ctypes.c_void_p,
        _DVDNavLoggerLevelT,
        ctypes.POINTER(ctypes.c_char)
    ))
]

dvdnav_open = _libdvdnav.dvdnav_open
"""
Function wrapper for libdvdnav dvdnav_open.

Source: libdvdnav/src/dvdnav/dvdnav.h:102
"""
dvdnav_open.restype = _DVDNavStatusT
dvdnav_open.argtypes = (
    ctypes.POINTER(ctypes.POINTER(_DVDNavT)),
    ctypes.POINTER(ctypes.c_char)
)

dvdnav_open_stream = _libdvdnav.dvdnav_open_stream
"""
Function wrapper for libdvdnav dvdnav_open_stream.

Source: libdvdnav/src/dvdnav/dvdnav.h:103
"""
dvdnav_open_stream.restype = _DVDNavStatusT
dvdnav_open_stream.argtypes = (
    ctypes.POINTER(ctypes.POINTER(_DVDNavT)),
    ctypes.c_void_p,
    ctypes.POINTER(_DVDNavStreamCB)
)

dvdnav_open2 = _libdvdnav.dvdnav_open2
"""
Function wrapper for libdvdnav dvdnav_open2.

Source: libdvdnav/src/dvdnav/dvdnav.h:106
"""
dvdnav_open2.restype = _DVDNavStatusT
dvdnav_open2.argtypes = (
    ctypes.POINTER(ctypes.POINTER(_DVDNavT)),
    ctypes.c_void_p,
    ctypes.POINTER(_DVDNavLoggerCB),
    ctypes.POINTER(ctypes.c_char)
)

dvdnav_open_stream2 = _libdvdnav.dvdnav_open_stream2
"""
Function wrapper for libdvdnav dvdnav_open_stream2.

Source: libdvdnav/src/dvdnav/dvdnav.h:109
"""
dvdnav_open_stream2.restype = _DVDNavStatusT
dvdnav_open_stream2.argtypes = (
    ctypes.POINTER(ctypes.POINTER(_DVDNavT)),
    ctypes.c_void_p,
    ctypes.POINTER(_DVDNavLoggerCB),
    ctypes.POINTER(_DVDNavStreamCB)
)

dvdnav_dup = _libdvdnav.dvdnav_dup
"""
Function wrapper for libdvdnav dvdnav_dup.

Source: libdvdnav/src/dvdnav/dvdnav.h:113
"""
dvdnav_dup.restype = _DVDNavStatusT
dvdnav_dup.argtypes = (
    ctypes.POINTER(ctypes.POINTER(_DVDNavT)),
    ctypes.POINTER(_DVDNavT)
)

dvdnav_free_dup = _libdvdnav.dvdnav_free_dup
"""
Function wrapper for libdvdnav dvdnav_free_dup.

Source: libdvdnav/src/dvdnav/dvdnav.h:114
"""
dvdnav_free_dup.restype = _DVDNavStatusT
dvdnav_free_dup.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

dvdnav_close = _libdvdnav.dvdnav_close
"""
Function wrapper for libdvdnav dvdnav_close.

Source: libdvdnav/src/dvdnav/dvdnav.h:120
"""
dvdnav_close.restype = _DVDNavStatusT
dvdnav_close.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

dvdnav_reset = _libdvdnav.dvdnav_reset
"""
Function wrapper for libdvdnav dvdnav_reset.

Source: libdvdnav/src/dvdnav/dvdnav.h:125
"""
dvdnav_reset.restype = _DVDNavStatusT
dvdnav_reset.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

dvdnav_path = _libdvdnav.dvdnav_path
"""
Function wrapper for libdvdnav dvdnav_path.

Source: libdvdnav/src/dvdnav/dvdnav.h:132
"""
dvdnav_path.restype = _DVDNavStatusT
dvdnav_path.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(ctypes.POINTER(ctypes.c_char))
)

dvdnav_err_to_string = _libdvdnav.dvdnav_err_to_string
"""
Function wrapper for libdvdnav dvdnav_err_to_string.

Source: libdvdnav/src/dvdnav/dvdnav.h:137
"""
dvdnav_err_to_string.restype = ctypes.POINTER(ctypes.c_char)
dvdnav_err_to_string.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

dvdnav_version = _libdvdnav.dvdnav_version
"""
Function wrapper for libdvdnav dvdnav_version.

Source: libdvdnav/src/dvdnav/dvdnav.h:139
"""
dvdnav_version.restype = ctypes.POINTER(ctypes.c_char)

dvdnav_set_region_mask = _libdvdnav.dvdnav_set_region_mask
"""
Function wrapper for libdvdnav dvdnav_set_region_mask.

Source: libdvdnav/src/dvdnav/dvdnav.h:158
"""
dvdnav_set_region_mask.restype = _DVDNavStatusT
dvdnav_set_region_mask.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_int32
)

dvdnav_get_region_mask = _libdvdnav.dvdnav_get_region_mask
"""
Function wrapper for libdvdnav dvdnav_get_region_mask.

Source: libdvdnav/src/dvdnav/dvdnav.h:166
"""
dvdnav_get_region_mask.restype = _DVDNavStatusT
dvdnav_get_region_mask.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(ctypes.c_int32)
)

DVDNavVOBUT = _DVDNavVOBUS
"""
Representation of the dvdnav_vobu_t typedef.

Source: libdvdnav/src/dvdnav/dvdnav.h:180
"""

dvdnav_set_readahead_flag = _libdvdnav.dvdnav_set_readahead_flag
"""
Function wrapper for libdvdnav dvdnav_set_readahead_flag.

Source: libdvdnav/src/dvdnav/dvdnav.h:181
"""
dvdnav_set_readahead_flag.restype = _DVDNavStatusT
dvdnav_set_readahead_flag.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_int32
)

dvdnav_get_readahead_flag = _libdvdnav.dvdnav_get_readahead_flag
"""
Function wrapper for libdvdnav dvdnav_get_readahead_flag.

Source: libdvdnav/src/dvdnav/dvdnav.h:186
"""
dvdnav_get_readahead_flag.restype = _DVDNavStatusT
dvdnav_get_readahead_flag.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(ctypes.c_int32)
)

dvdnav_set_pgc_positioning_flag = _libdvdnav.dvdnav_set_PGC_positioning_flag
"""
Function wrapper for libdvdnav dvdnav_set_PGC_positioning_flag.

Source: libdvdnav/src/dvdnav/dvdnav.h:195
"""
dvdnav_set_pgc_positioning_flag.restype = _DVDNavStatusT
dvdnav_set_pgc_positioning_flag.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_int32
)

dvdnav_get_pgc_positioning_flag = _libdvdnav.dvdnav_get_PGC_positioning_flag
"""
Function wrapper for libdvdnav dvdnav_get_PGC_positioning_flag.

Source: libdvdnav/src/dvdnav/dvdnav.h:200
"""
dvdnav_get_pgc_positioning_flag.restype = _DVDNavStatusT
dvdnav_get_pgc_positioning_flag.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(ctypes.c_int32)
)

dvdnav_get_next_block = _libdvdnav.dvdnav_get_next_block
"""
Function wrapper for libdvdnav dvdnav_get_next_block.

Source: libdvdnav/src/dvdnav/dvdnav.h:226
"""
dvdnav_get_next_block.restype = _DVDNavStatusT
dvdnav_get_next_block.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_int32),
    ctypes.POINTER(ctypes.c_int32)
)

dvdnav_get_next_cache_block = _libdvdnav.dvdnav_get_next_cache_block
"""
Function wrapper for libdvdnav dvdnav_get_next_cache_block.

Source: libdvdnav/src/dvdnav/dvdnav.h:237
"""
dvdnav_get_next_cache_block.restype = _DVDNavStatusT
dvdnav_get_next_cache_block.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(ctypes.POINTER(ctypes.c_uint8)),
    ctypes.POINTER(ctypes.c_int32),
    ctypes.POINTER(ctypes.c_int32)
)

dvdnav_free_cache_block = _libdvdnav.dvdnav_free_cache_block
"""
Function wrapper for libdvdnav dvdnav_free_cache_block.

Source: libdvdnav/src/dvdnav/dvdnav.h:245
"""
dvdnav_free_cache_block.restype = _DVDNavStatusT
dvdnav_free_cache_block.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(ctypes.c_ubyte)
)

dvdnav_still_skip = _libdvdnav.dvdnav_still_skip
"""
Function wrapper for libdvdnav dvdnav_still_skip.

Source: libdvdnav/src/dvdnav/dvdnav.h:252
"""
dvdnav_still_skip.restype = _DVDNavStatusT
dvdnav_still_skip.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

dvdnav_wait_skip = _libdvdnav.dvdnav_wait_skip
"""
Function wrapper for libdvdnav dvdnav_wait_skip.

Source: libdvdnav/src/dvdnav/dvdnav.h:261
"""
dvdnav_wait_skip.restype = _DVDNavStatusT
dvdnav_wait_skip.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

dvdnav_get_next_still_flag = _libdvdnav.dvdnav_get_next_still_flag
"""
Function wrapper for libdvdnav dvdnav_get_next_still_flag.

Source: libdvdnav/src/dvdnav/dvdnav.h:271
"""
dvdnav_get_next_still_flag.restype = ctypes.c_uint32
dvdnav_get_next_still_flag.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

dvdnav_stop = _libdvdnav.dvdnav_stop
"""
Function wrapper for libdvdnav dvdnav_stop.

Source: libdvdnav/src/dvdnav/dvdnav.h:279
"""
dvdnav_stop.restype = _DVDNavStatusT
dvdnav_stop.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

# TODO: Not defined in Debian. Temporarily removing.
# dvdnav_get_disk_region_mask = _libdvdnav.dvdnav_get_disk_region_mask
# """
# Function wrapper for libdvdnav dvdnav_get_disk_region_mask.
#
# Source: libdvdnav/src/dvdnav/dvdnav.h:293
# """
# dvdnav_get_disk_region_mask.restype = _DVDNavStatusT
# dvdnav_get_disk_region_mask.argtypes = (
#     ctypes.POINTER(_DVDNavT),
#     ctypes.POINTER(ctypes.c_int32)
# )

dvdnav_get_number_of_titles = _libdvdnav.dvdnav_get_number_of_titles
"""
Function wrapper for libdvdnav dvdnav_get_number_of_titles.

Source: libdvdnav/src/dvdnav/dvdnav.h:302
"""
dvdnav_get_number_of_titles.restype = _DVDNavStatusT
dvdnav_get_number_of_titles.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(ctypes.c_int32)
)

dvdnav_get_number_of_parts = _libdvdnav.dvdnav_get_number_of_parts
"""
Function wrapper for libdvdnav dvdnav_get_number_of_parts.

Source: libdvdnav/src/dvdnav/dvdnav.h:307
"""
dvdnav_get_number_of_parts.restype = _DVDNavStatusT
dvdnav_get_number_of_parts.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_int32,
    ctypes.POINTER(ctypes.c_int32)
)

dvdnav_get_number_of_angles = _libdvdnav.dvdnav_get_number_of_angles
"""
Function wrapper for libdvdnav dvdnav_get_number_of_angles.

Source: libdvdnav/src/dvdnav/dvdnav.h:312
"""
dvdnav_get_number_of_angles.restype = _DVDNavStatusT
dvdnav_get_number_of_angles.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_int32,
    ctypes.POINTER(ctypes.c_int32)
)

dvdnav_title_play = _libdvdnav.dvdnav_title_play
"""
Function wrapper for libdvdnav dvdnav_title_play.

Source: libdvdnav/src/dvdnav/dvdnav.h:317
"""
dvdnav_title_play.restype = _DVDNavStatusT
dvdnav_title_play.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_int32
)

dvdnav_part_play = _libdvdnav.dvdnav_part_play
"""
Function wrapper for libdvdnav dvdnav_part_play.

Source: libdvdnav/src/dvdnav/dvdnav.h:322
"""
dvdnav_part_play.restype = _DVDNavStatusT
dvdnav_part_play.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_int32,
    ctypes.c_int32
)

dvdnav_program_play = _libdvdnav.dvdnav_program_play
"""
Function wrapper for libdvdnav dvdnav_program_play.

Source: libdvdnav/src/dvdnav/dvdnav.h:327
"""
dvdnav_program_play.restype = _DVDNavStatusT
dvdnav_program_play.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_int32,
    ctypes.c_int32,
    ctypes.c_int32
)

dvdnav_describe_title_chapters = _libdvdnav.dvdnav_describe_title_chapters
"""
Function wrapper for libdvdnav dvdnav_program_play.

Source: libdvdnav/src/dvdnav/dvdnav.h:336
"""
dvdnav_describe_title_chapters.restype = ctypes.c_uint32
dvdnav_describe_title_chapters.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_int32,
    ctypes.POINTER(ctypes.POINTER(ctypes.c_uint64)),
    ctypes.POINTER(ctypes.c_uint64)
)

dvdnav_part_play_auto_stop = _libdvdnav.dvdnav_part_play_auto_stop
"""
Function wrapper for libdvdnav dvdnav_part_play_auto_stop.

Source: libdvdnav/src/dvdnav/dvdnav.h:344
"""
dvdnav_part_play_auto_stop.restype = _DVDNavStatusT
dvdnav_part_play_auto_stop.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_int32,
    ctypes.c_int32,
    ctypes.c_int32
)

dvdnav_time_play = _libdvdnav.dvdnav_time_play
"""
Function wrapper for libdvdnav dvdnav_time_play.

Source: libdvdnav/src/dvdnav/dvdnav.h:352
"""
dvdnav_time_play.restype = _DVDNavStatusT
dvdnav_time_play.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_int32,
    ctypes.c_int64
)

dvdnav_menu_call = _libdvdnav.dvdnav_menu_call
"""
Function wrapper for libdvdnav dvdnav_menu_call.

Source: libdvdnav/src/dvdnav/dvdnav.h:360
"""
dvdnav_menu_call.restype = _DVDNavStatusT
dvdnav_menu_call.argtypes = (
    ctypes.POINTER(_DVDNavT),
    _DVDMenuIDT
)

dvdnav_current_title_info = _libdvdnav.dvdnav_current_title_info
"""
Function wrapper for libdvdnav dvdnav_current_title_info.

Source: libdvdnav/src/dvdnav/dvdnav.h:367
"""
dvdnav_current_title_info.restype = _DVDNavStatusT
dvdnav_current_title_info.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(ctypes.c_int32),
    ctypes.POINTER(ctypes.c_int32)
)

dvdnav_current_title_program = _libdvdnav.dvdnav_current_title_program
"""
Function wrapper for libdvdnav dvdnav_current_title_program.

Source: libdvdnav/src/dvdnav/dvdnav.h:374
"""
dvdnav_current_title_program.restype = _DVDNavStatusT
dvdnav_current_title_program.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(ctypes.c_int32),
    ctypes.POINTER(ctypes.c_int32),
    ctypes.POINTER(ctypes.c_int32)
)

dvdnav_get_position_in_title = _libdvdnav.dvdnav_get_position_in_title
"""
Function wrapper for libdvdnav get_position_in_title.

Source: libdvdnav/src/dvdnav/dvdnav.h:384
"""
dvdnav_get_position_in_title.restype = _DVDNavStatusT
dvdnav_get_position_in_title.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.POINTER(ctypes.c_uint32)
)

dvdnav_part_search = _libdvdnav.dvdnav_part_search
"""
Function wrapper for libdvdnav dvdnav_part_search.

Source: libdvdnav/src/dvdnav/dvdnav.h:394
"""
dvdnav_part_search.restype = _DVDNavStatusT
dvdnav_part_search.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_int32
)

dvdnav_sector_search = _libdvdnav.dvdnav_sector_search
"""
Function wrapper for libdvdnav dvdnav_sector_search.

Source: libdvdnav/src/dvdnav/dvdnav.h:415
"""
dvdnav_sector_search.restype = _DVDNavStatusT
dvdnav_sector_search.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_int64,
    ctypes.c_int32
)

dvdnav_get_current_time = _libdvdnav.dvdnav_get_current_time
"""
Function wrapper for libdvdnav dvdnav_get_current_time.

Source: libdvdnav/src/dvdnav/dvdnav.h:422
"""
dvdnav_get_current_time.restype = ctypes.c_int64
dvdnav_get_current_time.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

dvdnav_time_search = _libdvdnav.dvdnav_time_search
"""
Function wrapper for libdvdnav dvdnav_time_search.

Source: libdvdnav/src/dvdnav/dvdnav.h:431
"""
dvdnav_time_search.restype = _DVDNavStatusT
dvdnav_time_search.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_uint64
)

dvdnav_jump_to_sector_by_time = _libdvdnav.dvdnav_jump_to_sector_by_time
"""
Function wrapper for libdvdnav dvdnav_jump_to_sector_by_time.

Source: libdvdnav/src/dvdnav/dvdnav.h:444
"""
dvdnav_jump_to_sector_by_time.restype = _DVDNavStatusT
dvdnav_jump_to_sector_by_time.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_uint64,
    ctypes.c_int32
)

dvdnav_go_up = _libdvdnav.dvdnav_go_up
"""
Function wrapper for libdvdnav dvdnav_go_up.

Source: libdvdnav/src/dvdnav/dvdnav.h:451
"""
dvdnav_go_up.restype = _DVDNavStatusT
dvdnav_go_up.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

dvdnav_prev_pg_search = _libdvdnav.dvdnav_prev_pg_search
"""
Function wrapper for libdvdnav dvdnav_prev_pg_search.

Source: libdvdnav/src/dvdnav/dvdnav.h:457
"""
dvdnav_prev_pg_search.restype = _DVDNavStatusT
dvdnav_prev_pg_search.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

dvdnav_top_pg_search = _libdvdnav.dvdnav_top_pg_search
"""
Function wrapper for libdvdnav dvdnav_top_pg_search.

Source: libdvdnav/src/dvdnav/dvdnav.h:463
"""
dvdnav_top_pg_search.restype = _DVDNavStatusT
dvdnav_top_pg_search.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

dvdnav_next_pg_search = _libdvdnav.dvdnav_next_pg_search
"""
Function wrapper for libdvdnav dvdnav_next_pg_search.

Source: libdvdnav/src/dvdnav/dvdnav.h:469
"""
dvdnav_next_pg_search.restype = _DVDNavStatusT
dvdnav_next_pg_search.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

dvdnav_get_position = _libdvdnav.dvdnav_get_position
"""
Function wrapper for libdvdnav dvdnav_get_position.

Source: libdvdnav/src/dvdnav/dvdnav.h:479
"""
dvdnav_get_position.restype = _DVDNavStatusT
dvdnav_get_position.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.POINTER(ctypes.c_uint32)
)

dvdnav_get_current_highlight = _libdvdnav.dvdnav_get_current_highlight
"""
Function wrapper for libdvdnav dvdnav_get_current_highlight.

Source: libdvdnav/src/dvdnav/dvdnav.h:501
"""
dvdnav_get_current_highlight.restype = _DVDNavStatusT
dvdnav_get_current_highlight.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(ctypes.c_int32)
)

dvdnav_get_current_nav_pci = _libdvdnav.dvdnav_get_current_nav_pci
"""
Function wrapper for libdvdnav dvdnav_get_current_nav_pci.

Source: libdvdnav/src/dvdnav/dvdnav.h:510
"""
dvdnav_get_current_nav_pci.restype = ctypes.POINTER(_PCIT)
dvdnav_get_current_nav_pci.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

dvdnav_get_current_nav_dsi = _libdvdnav.dvdnav_get_current_nav_dsi
"""
Function wrapper for libdvdnav dvdnav_get_current_nav_dsi.

Source: libdvdnav/src/dvdnav/dvdnav.h:519
"""
dvdnav_get_current_nav_dsi.restype = ctypes.POINTER(_DSIT)
dvdnav_get_current_nav_dsi.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

dvdnav_get_highlight_area = _libdvdnav.dvdnav_get_highlight_area
"""
Function wrapper for libdvdnav dvdnav_get_highlight_area.

Source: libdvdnav/src/dvdnav/dvdnav.h:524
"""
dvdnav_get_highlight_area.restype = _DVDNavStatusT
dvdnav_get_highlight_area.argtypes = (
    ctypes.POINTER(_PCIT),
    ctypes.c_int32,
    ctypes.c_int32,
    ctypes.POINTER(_DVDNavHighlightAreaT)
)

dvdnav_upper_button_select = _libdvdnav.dvdnav_upper_button_select
"""
Function wrapper for libdvdnav dvdnav_upper_button_select.

Source: libdvdnav/src/dvdnav/dvdnav.h:530
"""
dvdnav_upper_button_select.restype = _DVDNavStatusT
dvdnav_upper_button_select.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(_PCIT)
)

dvdnav_lower_button_select = _libdvdnav.dvdnav_lower_button_select
"""
Function wrapper for libdvdnav dvdnav_lower_button_select.

Source: libdvdnav/src/dvdnav/dvdnav.h:531
"""
dvdnav_lower_button_select.restype = _DVDNavStatusT
dvdnav_lower_button_select.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(_PCIT)
)

dvdnav_right_button_select = _libdvdnav.dvdnav_right_button_select
"""
Function wrapper for libdvdnav dvdnav_right_button_select.

Source: libdvdnav/src/dvdnav/dvdnav.h:532
"""
dvdnav_right_button_select.restype = _DVDNavStatusT
dvdnav_right_button_select.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(_PCIT)
)

dvdnav_left_button_select = _libdvdnav.dvdnav_left_button_select
"""
Function wrapper for libdvdnav dvdnav_left_button_select.

Source: libdvdnav/src/dvdnav/dvdnav.h:533
"""
dvdnav_left_button_select.restype = _DVDNavStatusT
dvdnav_left_button_select.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(_PCIT)
)

dvdnav_button_activate = _libdvdnav.dvdnav_button_activate
"""
Function wrapper for libdvdnav dvdnav_button_activate.

Source: libdvdnav/src/dvdnav/dvdnav.h:538
"""
dvdnav_button_activate.restype = _DVDNavStatusT
dvdnav_button_activate.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(_PCIT)
)

dvdnav_button_select = _libdvdnav.dvdnav_button_select
"""
Function wrapper for libdvdnav dvdnav_button_select.

Source: libdvdnav/src/dvdnav/dvdnav.h:543
"""
dvdnav_button_select.restype = _DVDNavStatusT
dvdnav_button_select.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(_PCIT),
    ctypes.c_int32
)

dvdnav_button_select_and_activate = _libdvdnav.dvdnav_button_select_and_activate
"""
Function wrapper for libdvdnav dvdnav_button_select_and_activate.

Source: libdvdnav/src/dvdnav/dvdnav.h:548
"""
dvdnav_button_select_and_activate.restype = _DVDNavStatusT
dvdnav_button_select_and_activate.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(_PCIT),
    ctypes.c_int32
)

dvdnav_button_activate_cmd = _libdvdnav.dvdnav_button_activate_cmd
"""
Function wrapper for libdvdnav dvdnav_button_activate_cmd.

Source: libdvdnav/src/dvdnav/dvdnav.h:553
"""
dvdnav_button_activate_cmd.restype = _DVDNavStatusT
dvdnav_button_activate_cmd.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_int32,
    ctypes.POINTER(_VMCmdT)
)

dvdnav_mouse_select = _libdvdnav.dvdnav_mouse_select
"""
Function wrapper for libdvdnav dvdnav_mouse_select.

Source: libdvdnav/src/dvdnav/dvdnav.h:559
"""
dvdnav_mouse_select.restype = _DVDNavStatusT
dvdnav_mouse_select.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(_PCIT),
    ctypes.c_int32,
    ctypes.c_int32
)

dvdnav_mouse_activate = _libdvdnav.dvdnav_mouse_activate
"""
Function wrapper for libdvdnav dvdnav_mouse_activate.

Source: libdvdnav/src/dvdnav/dvdnav.h:564
"""
dvdnav_mouse_activate.restype = _DVDNavStatusT
dvdnav_mouse_activate.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(_PCIT),
    ctypes.c_int32,
    ctypes.c_int32
)

dvdnav_menu_language_select = _libdvdnav.dvdnav_menu_language_select
"""
Function wrapper for libdvdnav dvdnav_menu_language_select.

Source: libdvdnav/src/dvdnav/dvdnav.h:579
"""
dvdnav_menu_language_select.restype = _DVDNavStatusT
dvdnav_menu_language_select.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(ctypes.c_char)
)

dvdnav_audio_language_select = _libdvdnav.dvdnav_audio_language_select
"""
Function wrapper for libdvdnav dvdnav_audio_language_select.

Source: libdvdnav/src/dvdnav/dvdnav.h:585
"""
dvdnav_audio_language_select.restype = _DVDNavStatusT
dvdnav_audio_language_select.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(ctypes.c_char)
)

dvdnav_spu_language_select = _libdvdnav.dvdnav_spu_language_select
"""
Function wrapper for libdvdnav dvdnav_spu_language_select.

Source: libdvdnav/src/dvdnav/dvdnav.h:591
"""
dvdnav_spu_language_select.restype = _DVDNavStatusT
dvdnav_spu_language_select.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(ctypes.c_char)
)

dvdnav_get_title_string = _libdvdnav.dvdnav_get_title_string
"""
Function wrapper for libdvdnav dvdnav_get_title_string.

Source: libdvdnav/src/dvdnav/dvdnav.h:607
"""
dvdnav_get_title_string.restype = _DVDNavStatusT
dvdnav_get_title_string.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(ctypes.POINTER(ctypes.c_char))
)

dvdnav_get_serial_string = _libdvdnav.dvdnav_get_serial_string
"""
Function wrapper for libdvdnav dvdnav_get_serial_string.

Source: libdvdnav/src/dvdnav/dvdnav.h:614
"""
dvdnav_get_serial_string.restype = _DVDNavStatusT
dvdnav_get_serial_string.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(ctypes.POINTER(ctypes.c_char))
)

# TODO: Not defined in Debian. Temporarily removing.
# dvdnav_get_volid_string = _libdvdnav.dvdnav_get_volid_string
# """
# Function wrapper for libdvdnav dvdnav_get_volid_string.
#
# Source: libdvdnav/src/dvdnav/dvdnav.h:627
# """
# dvdnav_get_volid_string.restype = ctypes.POINTER(ctypes.c_char)
# dvdnav_get_volid_string.argtypes = (
#     ctypes.POINTER(_DVDNavT),
# )

dvdnav_get_video_aspect = _libdvdnav.dvdnav_get_video_aspect
"""
Function wrapper for libdvdnav dvdnav_get_video_aspect.

Source: libdvdnav/src/dvdnav/dvdnav.h:636
"""
dvdnav_get_video_aspect.restype = ctypes.c_uint8
dvdnav_get_video_aspect.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

dvdnav_get_video_resolution = _libdvdnav.dvdnav_get_video_resolution
"""
Function wrapper for libdvdnav dvdnav_get_video_resolution.

Source: libdvdnav/src/dvdnav/dvdnav.h:641
"""
dvdnav_get_video_resolution.restype = _DVDNavStatusT
dvdnav_get_video_resolution.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.POINTER(ctypes.c_uint32)
)

dvdnav_get_video_scale_permission = _libdvdnav.dvdnav_get_video_scale_permission
"""
Function wrapper for libdvdnav dvdnav_get_video_scale_permission.

Source: libdvdnav/src/dvdnav/dvdnav.h:650
"""
dvdnav_get_video_scale_permission.restype = ctypes.c_uint8
dvdnav_get_video_scale_permission.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

dvdnav_audio_stream_to_lang = _libdvdnav.dvdnav_audio_stream_to_lang
"""
Function wrapper for libdvdnav dvdnav_audio_stream_to_lang.

Source: libdvdnav/src/dvdnav/dvdnav.h:656
"""
dvdnav_audio_stream_to_lang.restype = ctypes.c_uint16
dvdnav_audio_stream_to_lang.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_uint8
)

dvdnav_audio_stream_format = _libdvdnav.dvdnav_audio_stream_format
"""
Function wrapper for libdvdnav dvdnav_audio_stream_format.

Source: libdvdnav/src/dvdnav/dvdnav.h:662
"""
dvdnav_audio_stream_format.restype = ctypes.c_uint16
dvdnav_audio_stream_format.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_uint8
)

dvdnav_audio_stream_channels = _libdvdnav.dvdnav_audio_stream_channels
"""
Function wrapper for libdvdnav dvdnav_audio_stream_channels.

Source: libdvdnav/src/dvdnav/dvdnav.h:668
"""
dvdnav_audio_stream_channels.restype = ctypes.c_uint16
dvdnav_audio_stream_channels.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_uint8
)

dvdnav_spu_stream_to_lang = _libdvdnav.dvdnav_spu_stream_to_lang
"""
Function wrapper for libdvdnav dvdnav_spu_stream_to_lang.

Source: libdvdnav/src/dvdnav/dvdnav.h:674
"""
dvdnav_spu_stream_to_lang.restype = ctypes.c_uint16
dvdnav_spu_stream_to_lang.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_uint8
)

dvdnav_get_audio_logical_stream = _libdvdnav.dvdnav_get_audio_logical_stream
"""
Function wrapper for libdvdnav dvdnav_get_audio_logical_stream.

Source: libdvdnav/src/dvdnav/dvdnav.h:679
"""
dvdnav_get_audio_logical_stream.restype = ctypes.c_int8
dvdnav_get_audio_logical_stream.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_uint8
)

dvdnav_get_audio_attr = _libdvdnav.dvdnav_get_audio_attr
"""
Function wrapper for libdvdnav dvdnav_get_audio_attr.

Source: libdvdnav/src/dvdnav/dvdnav.h:685
"""
dvdnav_get_audio_attr.restype = _DVDNavStatusT
dvdnav_get_audio_attr.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_uint8,
    ctypes.POINTER(_AudioAttrT)
)

dvdnav_get_spu_logical_stream = _libdvdnav.dvdnav_get_spu_logical_stream
"""
Function wrapper for libdvdnav dvdnav_get_spu_logical_stream.

Source: libdvdnav/src/dvdnav/dvdnav.h:690
"""
dvdnav_get_spu_logical_stream.restype = ctypes.c_int8
dvdnav_get_spu_logical_stream.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_uint8
)

dvdnav_get_spu_attr = _libdvdnav.dvdnav_get_spu_attr
"""
Function wrapper for libdvdnav dvdnav_get_spu_attr.

Source: libdvdnav/src/dvdnav/dvdnav.h:696
"""
dvdnav_get_spu_attr.restype = _DVDNavStatusT
dvdnav_get_spu_attr.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_uint8,
    ctypes.POINTER(_SubPAttrT)
)

dvdnav_get_active_audio_stream = _libdvdnav.dvdnav_get_active_audio_stream
"""
Function wrapper for libdvdnav dvdnav_get_active_audio_stream.

Source: libdvdnav/src/dvdnav/dvdnav.h:701
"""
dvdnav_get_active_audio_stream.restype = ctypes.c_int8
dvdnav_get_active_audio_stream.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

dvdnav_get_active_spu_stream = _libdvdnav.dvdnav_get_active_spu_stream
"""
Function wrapper for libdvdnav dvdnav_get_active_spu_stream.

Source: libdvdnav/src/dvdnav/dvdnav.h:706
"""
dvdnav_get_active_spu_stream.restype = ctypes.c_int8
dvdnav_get_active_spu_stream.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

dvdnav_get_restrictions = _libdvdnav.dvdnav_get_restrictions
"""
Function wrapper for libdvdnav dvdnav_get_audio_logical_stream.

Source: libdvdnav/src/dvdnav/dvdnav.h:713
"""
dvdnav_get_restrictions.restype = _UserOpsT
dvdnav_get_restrictions.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

# TODO: Not defined in Debian. Temporarily removing.
# dvdnav_get_number_of_streams = _libdvdnav.dvdnav_get_number_of_streams
# """
# Function wrapper for libdvdnav dvdnav_get_number_of_streams.
#
# Source: libdvdnav/src/dvdnav/dvdnav.h:718
# """
# dvdnav_get_number_of_streams.restype = ctypes.c_int8
# dvdnav_get_number_of_streams.argtypes = (
#     ctypes.POINTER(_DVDNavT),
#     _DVDNavStreamTypeT
# )

# TODO: Not defined in Debian. Temporarily removing.
# dvdnav_toggle_spu_stream = _libdvdnav.dvdnav_toggle_spu_stream
# """
# Function wrapper for libdvdnav dvdnav_toggle_spu_stream.
#
# Source: libdvdnav/src/dvdnav/dvdnav.h:730
# """
# dvdnav_toggle_spu_stream.restype = _DVDNavStatusT
# dvdnav_toggle_spu_stream.argtypes = (
#     ctypes.POINTER(_DVDNavT),
#     ctypes.c_uint8
# )

# TODO: Not defined in Debian. Temporarily removing.
# dvdnav_set_active_stream = _libdvdnav.dvdnav_set_active_stream
# """
# Function wrapper for libdvdnav dvdnav_set_active_stream.
#
# Source: libdvdnav/src/dvdnav/dvdnav.h:737
# """
# dvdnav_set_active_stream.restype = _DVDNavStatusT
# dvdnav_set_active_stream.argtypes = (
#     ctypes.POINTER(_DVDNavT),
#     ctypes.c_uint8,
#     _DVDNavStreamTypeT
# )

dvdnav_angle_change = _libdvdnav.dvdnav_angle_change
"""
Function wrapper for libdvdnav dvdnav_angle_change.

Source: libdvdnav/src/dvdnav/dvdnav.h:761
"""
dvdnav_angle_change.restype = _DVDNavStatusT
dvdnav_angle_change.argtypes = (
    ctypes.POINTER(_DVDNavT),
    ctypes.c_uint32
)

dvdnav_get_angle_info = _libdvdnav.dvdnav_get_angle_info
"""
Function wrapper for libdvdnav dvdnav_get_angle_info.

Source: libdvdnav/src/dvdnav/dvdnav.h:766
"""
dvdnav_get_angle_info.restype = _DVDNavStatusT
dvdnav_get_angle_info.argstype = (
    ctypes.POINTER(_DVDNavT),
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.POINTER(ctypes.c_uint32)
)

dvdnav_is_domain_fp = _libdvdnav.dvdnav_is_domain_fp
"""
Function wrapper for libdvdnav dvdnav_is_domain_fp.

Source: libdvdnav/src/dvdnav/dvdnav.h:776
"""
dvdnav_is_domain_fp.restype = ctypes.c_int8
dvdnav_is_domain_fp.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

dvdnav_is_domain_vmgm = _libdvdnav.dvdnav_is_domain_vmgm
"""
Function wrapper for libdvdnav dvdnav_is_domain_vmgm.

Source: libdvdnav/src/dvdnav/dvdnav.h:781
"""
dvdnav_is_domain_vmgm.restype = ctypes.c_int8
dvdnav_is_domain_vmgm.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

dvdnav_is_domain_vtsm = _libdvdnav.dvdnav_is_domain_vtsm
"""
Function wrapper for libdvdnav dvdnav_is_domain_vtsm.

Source: libdvdnav/src/dvdnav/dvdnav.h:786
"""
dvdnav_is_domain_vtsm.restype = ctypes.c_int8
dvdnav_is_domain_vtsm.argtypes = (
    ctypes.POINTER(_DVDNavT),
)

dvdnav_is_domain_vts = _libdvdnav.dvdnav_is_domain_vts
"""
Function wrapper for libdvdnav dvdnav_is_domain_vts.

Source: libdvdnav/src/dvdnav/dvdnav.h:791
"""
dvdnav_is_domain_vts.restype = ctypes.c_int8
dvdnav_is_domain_vts.argtypes = (
    ctypes.POINTER(_DVDNavT),
)
# </editor-fold>

# Sadly, this has to be declared all the way down here because of the circular
# references in the original header files.
_VMT._fields_ = [
    ("priv", ctypes.c_void_p),
    ("logcb", _DVDNavLoggerCB),
    ("streamcb", _DVDNavStreamCB),
    ("videolanlibdvd", ctypes.POINTER(_DVDReaderT)),
    ("dvdstreamcb", _DVDReaderStreamCB),
    ("vmgi", ctypes.POINTER(_IFOHandleT)),
    ("vtsi", ctypes.POINTER(_IFOHandleT)),
    ("state", _DVDStateT),
    ("hop_channel", ctypes.c_int32),
    ("dvd_name", ctypes.c_char * 50),
    ("dvd_serial", ctypes.c_char * 15),
    ("stopped", ctypes.c_int)
]

# Sadly, this has to be declared all the way down here because of the circular
# references in the original header files.
_DVDNavS._fields_ = [
    ("path", ctypes.POINTER(ctypes.c_char)),
    ("file", ctypes.POINTER(_DVDFileT)),
    ("position_next", _VMPositionT),
    ("position_current", _VMPositionT),
    ("vobu", DVDNavVOBUT),
    ("pci", _PCIT),
    ("dsi", _DSIT),
    ("last_cmd_nav_lbn", ctypes.c_uint32),
    ("skip_still", ctypes.c_int),
    ("sync_wait", ctypes.c_int),
    ("sync_wait_skip", ctypes.c_int),
    ("spu_clut_changed", ctypes.c_int),
    ("spu_clut_changed", ctypes.c_int),
    ("started", ctypes.c_int),
    ("use_read_ahead", ctypes.c_int),
    ("pgc_based", ctypes.c_int),
    ("cur_cell_time", ctypes.c_int),
    ("vm", ctypes.POINTER(_VMT)),
    ("vm_lock", _PThreadMutexT),
    ("priv", ctypes.c_void_p),
    ("logcb", _DVDNavLoggerCB),
    ("cache", ctypes.POINTER(_ReadCacheT)),
    ("err_str", ctypes.c_char * _MAX_ERR_LEN)
]


# <editor-fold desc="Grouping for dvdnav/dvdnav_events.h header file.">

class _DVDNavStillEventT(ctypes.Structure):
    """
    Struct for the libdvdnav dvdnav_still_event_t type.

    Source: libdvdnav/src/dvdnav/dvdnav_events.h:58
    """
    _fields_ = [
        ("length", ctypes.c_int)
    ]


class _DVDNavSPUStreamChangeEventT(ctypes.Structure):
    """
    Struct for the libdvdnav dvdnav_spu_stream_change_event_t type.

    Source: libdvdnav/src/dvdnav/dvdnav_events.h:72
    """
    _fields_ = [
        ("physical_wide", ctypes.c_int),
        ("physical_letterbox", ctypes.c_int),
        ("physical_pan_scan", ctypes.c_int),
        ("logical", ctypes.c_int)
    ]


class _DVDNavAudioStreamChangeEventT(ctypes.Structure):
    """
    Struct for the libdvdnav dvdnav_audio_stream_change_event_t type.

    Source: libdvdnav/src/dvdnav/dvdnav_events.h:100
    """
    _fields_ = [
        ("physical", ctypes.c_int),
        ("logical", ctypes.c_int)
    ]


class _DVDNavVTSChangeEventT(ctypes.Structure):
    """
    Struct for the libdvdnav dvdnav_vts_change_event_t type.

    Source: libdvdnav/src/dvdnav/dvdnav_events.h:119
    """
    _fields_ = [
        ("old_vtsN", ctypes.c_int),
        ("old_domain", _DVDDomainT),
        ("new_vtsN", ctypes.c_int),
        ("new_domain", _DVDDomainT)
    ]


class _DVDNavCellChangeEventT(ctypes.Structure):
    """
    Struct for the libdvdnav cell_change_event_t type.

    Source: libdvdnav/src/dvdnav/dvdnav_events.h:139
    """
    _fields_ = [
        ("cellN", ctypes.c_int),
        ("pgN", ctypes.c_int),
        ("cell_length", ctypes.c_int64),
        ("pg_length", ctypes.c_int64),
        ("pgc_length", ctypes.c_int64),
        ("cell_start", ctypes.c_int64),
        ("pg_start", ctypes.c_int64)
    ]


class _DVDNavHighlightEventT(ctypes.Structure):
    """
    Struct for the libdvdnav dvdnav_highlight_event_t type.

    Source: libdvdnav/src/dvdnav/dvdnav_events.h:189
    """
    _fields_ = [
        ("display", ctypes.c_int),
        ("palette", ctypes.c_uint32),
        ("sx", ctypes.c_uint16),
        ("sy", ctypes.c_uint16),
        ("ex", ctypes.c_uint16),
        ("ey", ctypes.c_uint16),
        ("pts", ctypes.c_uint32),
        ("buttonN", ctypes.c_uint32)
    ]
# </editor-fold>
