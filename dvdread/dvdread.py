# Copyright © 2025 Borden Rhodes
#
# dvdread.py is free software: you can redistribute it and/or modify it under
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
ctypes wrapper to VideoLAN's libdvdread library header files.

These are low-level wrappers. For most purposes, you want to use the module's
DVD class instead. Refer to the C header documentation, such as it is, for
usage information.

The wrappers try to appear in the same order as the original header file. This
module wraps definitions from outside the libdvdread API where those
definitions are necessary to complete a function prototype. Further, wrappers
will appear out of order from the header file when this module needs to define
something before defining something else. Python doesn't have forward
declarations to allow the original ordering.
"""

import ctypes
import os

from dvdcss import _DVDCSST

_POSIX_DVDREAD_LIB = "libdvdread.so.8"
"""
Name of the libdvdread shared object library on POSIX systems to be loaded.
"""

_WIN_VLCCORE_LIB = os.path.expandvars(
    "%PROGRAMFILES%/VideoLAN/VLC/libvlccore.dll"
)
"""
Path to the libvlccore DLL on Windows systems.

This is a prerequisite to load the other libdvd DLLs.
"""

_WIN_DVDREAD_LIB = os.path.expandvars(
    "%PROGRAMFILES%/VideoLAN/VLC/plugins/access/libdvdread_plugin.dll"
)
"""
Path to the libdvdread DLL on Windows systems.
"""

if os.name == 'posix':
    _libdvdread = ctypes.CDLL(_POSIX_DVDREAD_LIB)
elif os.name == 'nt':
    _libvlccore = ctypes.CDLL(_WIN_VLCCORE_LIB)
    _libdvdread = ctypes.CDLL(_WIN_DVDREAD_LIB)
else:
    raise RuntimeError(f"Unsupported operating system {os.name}. "
                       + "This is almost certainly a bug.")

_OffT = ctypes.c_long
"""
Representation of the off_t typedef.

TODO: Not sure that this will work, as it's supposed to be opaque and system
dependent.
"""


# <editor-fold desc="Grouping for libdvdread/src/dvd_input.c header file.">
class _DVDInputS(ctypes.Structure):
    """
    Struct for the libdvdread dvd_input_s type.

    Source: libdvdread/src/dvd_input.c:99
    """
    # _fields_ assignment is after the nav_read_dsi function declaration.


# </editor-fold>

# <editor-fold desc="Grouping for libdvdread/src/dvd_input.h header file.">
_DVDInputT = ctypes.POINTER(_DVDInputS)
"""
Struct for the libdvdread dvd_input_t type.

Source: libdvdread/src/dvd_input.h:32
"""


# </editor-fold>

# <editor-fold desc="Grouping for libdvdread/src/dvd_reader.c header file.">
class _DVDReaderDeviceS(ctypes.Structure):
    """
    Struct for the libdvdread dvd_reader_device_s type.

    Source: libdvdread/src/dvd_reader.c:187
    """
    _fields_ = [
        ("isImageFile", ctypes.c_int),
        ("css_state", ctypes.c_int),
        ("css_title", ctypes.c_int),
        ("dev", _DVDInputT),
        ("path_root", ctypes.POINTER(ctypes.c_char)),
        ("udfcache_level", ctypes.c_int),
        ("udfcache", ctypes.c_void_p)
    ]


_TITLES_MAX = 9
"""
Preprocessor alias for TITLES_MAX system value.

Source: libdvdread/src/dvd_reader.c:207
"""


class _DVDFileS(ctypes.Structure):
    """
    Struct for the libdvdread dvd_file_s type.

    Source: libdvdread/src/dvd_reader.c:209
    """
    # _fields_ assignment is after the nav_read_dsi function declaration.


# </editor-fold>


# <editor-fold desc="Grouping for libdvdread/src/dvdread_internal.h header file.">
class _DVDReaderS(ctypes.Structure):
    """
    Struct for the libdvdread dvd_reader_s type.

    Source: libdvdread/src/dvdread_internal.h:37
    """
    # _fields_ assignment is after the nav_read_dsi function declaration.


# </editor-fold>

# <editor-fold desc="Grouping for libdvdread/src/dvdread/bitreader.h header file.">
class _GetBitsStateT(ctypes.Structure):
    """
    Struct for the libdvdread getbits_state_t type.

    Source: libdvdread/src/dvdread/bitreader.h:30
    """
    _fields_ = [
        ("start", ctypes.POINTER(ctypes.c_uint8)),
        ("byte_position", ctypes.c_uint32),
        ("bit_position", ctypes.c_uint32)
    ]


dvdread_getbits_init = _libdvdread.dvdread_getbits_init
"""
Function wrapper for libdvdread dvdread_getbits_init.

Source: libdvdread/src/dvdread/bitreader.h:36
"""
dvdread_getbits_init.restype = ctypes.c_int
dvdread_getbits_init.argtypes = (
    ctypes.POINTER(_GetBitsStateT),
    ctypes.POINTER(ctypes.c_uint8)
)

dvdread_getbits = _libdvdread.dvdread_getbits
"""
Function wrapper for libdvdread dvdread_getbits.

Source: libdvdread/src/dvdread/bitreader.h:37
"""
dvdread_getbits.restype = ctypes.c_uint32
dvdread_getbits.argtypes = (
    ctypes.POINTER(_GetBitsStateT),
    ctypes.c_uint32
)
# </editor-fold>

# <editor-fold desc="Grouping for libdvdread/src/dvdread/dvd_reader.h header file.">

_DVD_VIDEO_LB_LEN = 2048
"""
Preprocessor alias for DVD_VIDEO_LB_LEN system value.

Source: libdvdread/src/dvdread/dvd_reader.h:54
"""

_MAX_UDF_FILE_NAME_LEN = 2048
"""
Preprocessor alias for MAX_UDF_FILE_NAME_LEN system value.

Source: libdvdread/src/dvdread/dvd_reader.h:59
"""

_DVDReaderT = _DVDReaderS
"""
Representation of the dvd_reader_t typedef.

Source: libdvdread/src/dvdread/dvd_reader.h:68
"""

_DVDReaderDeviceT = _DVDReaderDeviceS
"""
Representation of the dvd_reader_device_t typedef.

Source: libdvdread/src/dvdread/dvd_reader.h:69
"""

_DVDFileT = _DVDFileS
"""
Representation of the dvd_file_t typedef.

Source: libdvdread/src/dvdread/dvd_reader.h:74
"""


class _DVDReaderStreamCB(ctypes.Structure):
    """
    Struct for the libdvdread dvd_reader_stream_cb type.

    Source: libdvdread/src/dvdread/dvd_reader.h:76
    """
    _fields_ = [
        ("pf_seek", ctypes.CFUNCTYPE(
            ctypes.POINTER(ctypes.c_int),
            ctypes.c_void_p,
            ctypes.c_int64
        )),
        ("pf_read", ctypes.CFUNCTYPE(
            ctypes.POINTER(ctypes.c_int),
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_int
        )),
        ("pf_readv", ctypes.CFUNCTYPE(
            ctypes.POINTER(ctypes.c_int),
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_int
        ))
    ]


_DVDLoggerLevelT = ctypes.c_int
"""
Representation of the dvd_logger_level_t enum.

Source: libdvdread/src/dvdread/dvd_reader.h:92
"""


class _DVDLoggerCB(ctypes.Structure):
    """
    Struct for the libdvdread dvd_logger_cb type.

    TODO: Takes variadic va_list. Figure out how to resolve
    Source: libdvdread/src/dvdread/dvd_reader.h:100
    """
    _fields_ = [
        ("pf_log", ctypes.CFUNCTYPE(
            ctypes.c_void_p,
            ctypes.c_void_p,
            _DVDLoggerLevelT,
            ctypes.POINTER(ctypes.c_char)
        ))
    ]


class _DVDStatT(ctypes.Structure):
    """
    Struct for the libdvdread dvd_stat_t type.

    Source: libdvdread/src/dvdread/dvd_reader.h:108
    """
    _fields_ = [
        ("size", _OffT),
        ("nr_parts", ctypes.c_int),
        ("parts_size", _OffT * 9)
    ]


dvd_open = _libdvdread.DVDOpen
"""
Function wrapper for libdvdread DVDOpen.

Source: libdvdread/src/dvdread/dvd_reader.h:141
"""
dvd_open.restype = ctypes.POINTER(_DVDReaderT)
dvd_open.argtypes = (
    ctypes.POINTER(ctypes.c_char),
)

dvd_open_stream = _libdvdread.DVDOpenStream
"""
Function wrapper for libdvdread DVDOpenStream.

Source: libdvdread/src/dvdread/dvd_reader.h:142
"""
dvd_open_stream.restype = ctypes.POINTER(_DVDReaderT)
dvd_open_stream.argtypes = (
    ctypes.POINTER(ctypes.c_char),
    ctypes.POINTER(_DVDReaderStreamCB)
)

dvd_open2 = _libdvdread.DVDOpen2
"""
Function wrapper for libdvdread DVDOpen2.

Source: libdvdread/src/dvdread/dvd_reader.h:156
"""
dvd_open2.restype = ctypes.POINTER(_DVDReaderT)
dvd_open2.argtypes = (
    ctypes.c_void_p,
    ctypes.POINTER(_DVDLoggerCB),
    ctypes.POINTER(ctypes.c_char)
)

dvd_open_stream2 = _libdvdread.DVDOpenStream2
"""
Function wrapper for libdvdread DVDOpenStream2.

Source: libdvdread/src/dvdread/dvd_reader.h:157
"""
dvd_open_stream2.restype = ctypes.POINTER(_DVDReaderT)
dvd_open_stream2.argtypes = (
    ctypes.c_void_p,
    ctypes.POINTER(_DVDLoggerCB),
    ctypes.POINTER(_DVDReaderStreamCB)
)

dvd_close = _libdvdread.DVDClose
"""
Function wrapper for libdvdread DVDClose.

Source: libdvdread/src/dvdread/dvd_reader.h:168
"""
dvd_close.restype = None
dvd_close.argtypes = (
    ctypes.POINTER(_DVDReaderT),
)

_DVDReadDomainT = ctypes.c_int
"""
Representation of the dvd_read_domain_t enum.

Source: libdvdread/src/dvdread/dvd_reader.h:173
"""

dvd_file_stat = _libdvdread.DVDFileStat
"""
Function wrapper for libdvdread DVDFileStat.

Source: libdvdread/src/dvdread/dvd_reader.h:207
"""
dvd_file_stat.restype = ctypes.c_int
dvd_file_stat.argtypes = (
    ctypes.POINTER(_DVDReaderT),
    ctypes.c_int,
    _DVDReadDomainT,
    ctypes.POINTER(_DVDStatT)
)

dvd_open_file = _libdvdread.DVDOpenFile
"""
Function wrapper for libdvdread DVDOpenFile.

Source: libdvdread/src/dvdread/dvd_reader.h:222
"""
dvd_open_file.restype = ctypes.POINTER(_DVDFileT)
dvd_open_file.argtypes = (
    ctypes.POINTER(_DVDReaderT),
    ctypes.c_int,
    _DVDReadDomainT
)

dvd_close_file = _libdvdread.DVDCloseFile
"""
Function wrapper for libdvdread DVDCloseFile.

Source: libdvdread/src/dvdread/dvd_reader.h:231
"""
dvd_close_file.restype = None
dvd_close_file.argtypes = (
    ctypes.POINTER(_DVDFileT),
)

dvd_read_blocks = _libdvdread.DVDReadBlocks
"""
Function wrapper for libdvdread DVDReadBlocks.

Source: libdvdread/src/dvdread/dvd_reader.h:248
"""
dvd_read_blocks.restype = ctypes.c_ssize_t
dvd_read_blocks.argtypes = (
    ctypes.POINTER(_DVDFileT),
    ctypes.c_int,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_char)
)

dvd_file_seek = _libdvdread.DVDFileSeek
"""
Function wrapper for libdvdread DVDFileSeek.

Source: libdvdread/src/dvdread/dvd_reader.h:262
"""
dvd_file_seek.restype = ctypes.c_int32
dvd_file_seek.argtypes = (
    ctypes.POINTER(_DVDFileT),
    ctypes.c_int32
)

dvd_read_bytes = _libdvdread.DVDReadBytes
"""
Function wrapper for libdvdread DVDReadBytes.

Source: libdvdread/src/dvdread/dvd_reader.h:276
"""
dvd_read_bytes.restype = ctypes.c_ssize_t
dvd_read_bytes.argtypes = (
    ctypes.POINTER(_DVDFileT),
    ctypes.c_void_p,
    ctypes.c_size_t
)

dvd_file_size = _libdvdread.DVDFileSize
"""
Function wrapper for libdvdread DVDFileSize.

Source: libdvdread/src/dvdread/dvd_reader.h:286
"""
dvd_file_size.restype = ctypes.c_ssize_t
dvd_file_size.argtypes = (
    ctypes.POINTER(_DVDFileT),
)

dvd_disc_id = _libdvdread.DVDDiscID
"""
Function wrapper for libdvdread DVDDiscID.

Source: libdvdread/src/dvdread/dvd_reader.h:301
"""
dvd_disc_id.restype = ctypes.c_int
dvd_disc_id.argtypes = (
    ctypes.POINTER(_DVDReaderT),
    ctypes.POINTER(ctypes.c_ubyte)
)

dvd_volume_info = _libdvdread.DVDUDFVolumeInfo
"""
Function wrapper for libdvdread DVDUDFVolumeInfo.

Source: libdvdread/src/dvdread/dvd_reader.h:321
"""
dvd_volume_info.restype = ctypes.c_int
dvd_volume_info.argtypes = (
    ctypes.POINTER(_DVDReaderT),
    ctypes.POINTER(ctypes.c_char),
    ctypes.c_uint,
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.c_uint
)

dvd_file_seek_force = _libdvdread.DVDFileSeekForce
"""
Function wrapper for libdvdread DVDFileSeekForce.

Source: libdvdread/src/dvdread/dvd_reader.h:324
"""
dvd_file_seek_force.restype = ctypes.c_int
dvd_file_seek_force.argtypes = (
    ctypes.POINTER(_DVDFileT),
    ctypes.c_int,
    ctypes.c_int
)

dvd_iso_volume_info = _libdvdread.DVDISOVolumeInfo
"""
Function wrapper for libdvdread DVDISOVolumeInfo.

Source: libdvdread/src/dvdread/dvd_reader.h:347
"""
dvd_iso_volume_info.restype = ctypes.c_int
dvd_iso_volume_info.argtypes = (
    ctypes.POINTER(_DVDReaderT),
    ctypes.POINTER(ctypes.c_char),
    ctypes.c_uint,
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.c_uint
)

dvd_udf_cache_level = _libdvdread.DVDUDFCacheLevel
"""
Function wrapper for libdvdread DVDUDFCacheLevel.

Source: libdvdread/src/dvdread/dvd_reader.h:362
"""
dvd_udf_cache_level.restype = ctypes.c_int
dvd_udf_cache_level.argtypes = (
    ctypes.POINTER(_DVDReaderT),
    ctypes.c_int
)
# </editor-fold>

# <editor-fold desc="Grouping for libdvdread/src/dvdread/dvd_udf.h header file.">
udf_find_file = _libdvdread.UDFFindFile
"""
Function wrapper for libdvdread UDFFindFile.

Source: libdvdread/src/dvdread/dvd_udf.h:50
"""
udf_find_file.restype = ctypes.c_uint32
udf_find_file.argtypes = (
    ctypes.POINTER(_DVDReaderT),
    ctypes.POINTER(ctypes.c_char),
    ctypes.POINTER(ctypes.c_uint32)
)

udf_get_volume_identifier = _libdvdread.UDFGetVolumeIdentifier
"""
Function wrapper for libdvdread UDFGetVolumeIdentifier.

Source: libdvdread/src/dvdread/dvd_udf.h:52
"""
udf_get_volume_identifier.restype = ctypes.c_int
udf_get_volume_identifier.argtypes = (
    ctypes.POINTER(_DVDReaderT),
    ctypes.POINTER(ctypes.c_char),
    ctypes.c_uint
)

udf_get_volume_set_identifier = _libdvdread.UDFGetVolumeSetIdentifier
"""
Function wrapper for libdvdread UDFGetVolumeSetIdentifier.

Source: libdvdread/src/dvdread/dvd_udf.h:54
"""
udf_get_volume_set_identifier.restype = ctypes.c_int
udf_get_volume_set_identifier.argtypes = (
    ctypes.POINTER(_DVDReaderT),
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint
)


# </editor-fold>

# <editor-fold desc="Grouping for libdvdread/src/dvdread/ifo_types.h header file.">
class _DVDTimeT(ctypes.Structure):
    """
    Struct for the libdvdread dvd_time_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:63
    """
    _fields_ = [
        ("hour", ctypes.c_uint8),
        ("minute", ctypes.c_uint8),
        ("second", ctypes.c_uint8),
        ("frame_u", ctypes.c_uint8)
    ]


class _VMCmdT(ctypes.Structure):
    """
    Struct for the libdvdread vm_cmd_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:73
    """
    _fields_ = [
        ("bytes", ctypes.c_uint8 * 8)
    ]


_COMMAND_DATA_SIZE = 8
"""
Preprocessor alias for COMMAND_DATA_SIZE system value.

Source: libdvdread/src/dvdread/ifo_types.h:76
"""


class _VideoAttrT(ctypes.Structure):
    """
    Struct for the libdvdread video_attr_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:82
    """
    _fields_ = [
        ("mpeg_version", ctypes.c_ubyte, 2),
        ("video_format", ctypes.c_ubyte, 2),
        ("display_aspect_ratio", ctypes.c_ubyte, 2),
        ("permitted_df", ctypes.c_ubyte, 2),
        ("line21_cc_1", ctypes.c_ubyte, 1),
        ("line21_cc_2", ctypes.c_ubyte, 1),
        ("unknown1", ctypes.c_ubyte, 1),
        ("bit_rate", ctypes.c_ubyte, 1),
        ("picture_size", ctypes.c_ubyte, 2),
        ("letterboxed", ctypes.c_ubyte, 1),
        ("film_mode", ctypes.c_ubyte, 1)
    ]


class _AudioAttrT(ctypes.Structure):
    """
    Struct for the libdvdread audio_attr_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:101
    """

    class _AppInfo(ctypes.Union):
        """
        Struct for the libdvdread app_info sub-type.

        TODO: header file sets packing. Seems Python does this automatically.
        Source: libdvdread/src/dvdread/ifo_types.h:115
        """

        class _Karaoke(ctypes.Structure):
            """
            Struct for the libdvdread karaoke sub-sub-type.

            TODO: header file sets packing. Seems Python does this automatically.
            Source: libdvdread/src/dvdread/ifo_types.h:116
            """
            _fields_ = [
                ("unknown4", ctypes.c_ubyte, 1),
                ("channel_assignment", ctypes.c_ubyte, 3),
                ("version", ctypes.c_ubyte, 2),
                ("mc_intro", ctypes.c_ubyte, 1),
                ("mode", ctypes.c_ubyte, 1)
            ]

        class _Surround(ctypes.Structure):
            """
            Struct for the libdvdread surround sub-sub-type.

            TODO: header file sets packing. Seems Python does this automatically.
            Source: libdvdread/src/dvdread/ifo_types.h:123
            """
            _fields_ = [
                ("unknown5", ctypes.c_ubyte, 4),
                ("dolby_encoded", ctypes.c_ubyte, 1),
                ("unknown6", ctypes.c_ubyte, 3)
            ]

        _fields_ = [
            ("karaoke", _Karaoke),
            ("surround", _Surround)
        ]

    _fields_ = [
        ("audio_format", ctypes.c_ubyte, 3),
        ("multichannel_extension", ctypes.c_ubyte, 1),
        ("lang_type", ctypes.c_ubyte, 2),
        ("application_mode", ctypes.c_ubyte, 2),
        ("quantization", ctypes.c_ubyte, 2),
        ("sample_frequency", ctypes.c_ubyte, 2),
        ("unknown1", ctypes.c_ubyte, 1),
        ("channels", ctypes.c_ubyte, 3),
        ("lang_code", ctypes.c_uint16),
        ("lang_extension", ctypes.c_uint8),
        ("code_extension", ctypes.c_uint8),
        ("unknown3", ctypes.c_uint8),
        ("app_info", _AppInfo)
    ]


class _MultichannelExtT(ctypes.Structure):
    """
    Struct for the libdvdread multichannel_ext_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:135
    """
    _fields_ = [
        ("zero1", ctypes.c_ubyte, 7),
        ("ach0_gme", ctypes.c_ubyte, 1),
        ("zero2", ctypes.c_ubyte, 7),
        ("ach1_gme", ctypes.c_ubyte, 1),
        ("zero3", ctypes.c_ubyte, 4),
        ("ach2_gv1e", ctypes.c_ubyte, 1),
        ("ach2_gv2e", ctypes.c_ubyte, 1),
        ("ach2_gm1e", ctypes.c_ubyte, 1),
        ("ach2_gm2e", ctypes.c_ubyte, 1),
        ("zero4", ctypes.c_ubyte, 4),
        ("ach3_gv1e", ctypes.c_ubyte, 1),
        ("ach3_gv2e", ctypes.c_ubyte, 1),
        ("ach3_gmAe", ctypes.c_ubyte, 1),
        ("ach3_se2e", ctypes.c_ubyte, 1),
        ("zero5", ctypes.c_ubyte, 4),
        ("ach4_gv1e", ctypes.c_ubyte, 1),
        ("ach4_gv2e", ctypes.c_ubyte, 1),
        ("ach4_gmBe", ctypes.c_ubyte, 1),
        ("ach4_seBe", ctypes.c_ubyte, 1),
        ("zero6", ctypes.c_uint8 * 19)
    ]


class _SubPAttrT(ctypes.Structure):
    """
    Struct for the libdvdread subp_attr_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:166
    """
    _fields_ = [
        ("code_mode", ctypes.c_ubyte, 3),
        ("zero1", ctypes.c_ubyte, 3),
        ("type", ctypes.c_ubyte, 2),
        ("zero2", ctypes.c_uint8),
        ("lang_code", ctypes.c_uint16),
        ("lang_extension", ctypes.c_uint8),
        ("code_extension", ctypes.c_uint8)
    ]


class _PGCCommandTblT(ctypes.Structure):
    """
    Struct for the libdvdread pgc_command_tbl_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:191
    """
    _fields_ = [
        ("nr_of_pre", ctypes.c_uint16),
        ("nr_of_post", ctypes.c_uint16),
        ("nr_of_cell", ctypes.c_uint16),
        ("last_byte", ctypes.c_uint16),
        ("pre_cmds", ctypes.POINTER(_VMCmdT)),
        ("post_cmds", ctypes.POINTER(_VMCmdT)),
        ("cell_cmds", ctypes.POINTER(_VMCmdT))
    ]


_PGC_COMMAND_TBL_SIZE = 8
"""
Preprocessor alias for PGC_COMMAND_TBL_SIZE system value.

Source: libdvdread/src/dvdread/ifo_types.h:200
"""

_PGCProgramMapT = ctypes.c_uint8
"""
Representation of the pgc_program_map_t typedef.

Source: libdvdread/src/dvdread/ifo_types.h:205
"""


class _CellPlaybackT(ctypes.Structure):
    """
    Struct for the libdvdread cell_playback_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:210
    """
    _fields_ = [
        ("block_mode", ctypes.c_ubyte, 2),
        ("block_type", ctypes.c_ubyte, 2),
        ("seamless_play", ctypes.c_ubyte, 1),
        ("interleaved", ctypes.c_ubyte, 1),
        ("stc_discontinuity", ctypes.c_ubyte, 1),
        ("seamless_angle", ctypes.c_ubyte, 1),
        ("zero_1", ctypes.c_ubyte, 1),
        ("playback_mode", ctypes.c_ubyte, 1),
        ("restricted", ctypes.c_ubyte, 1),
        ("cell_type", ctypes.c_ubyte, 5),
        ("still_time", ctypes.c_uint8),
        ("cell_cmd_nr", ctypes.c_uint8),
        ("playback_time", _DVDTimeT),
        ("first_sector", ctypes.c_uint32),
        ("first_ilvu_end_sector", ctypes.c_uint32),
        ("last_vobu_start_sector", ctypes.c_uint32),
        ("last_sector", ctypes.c_uint32)
    ]


_BLOCK_TYPE_NONE = 0
"""
Preprocessor alias for BLOCK_TYPE_NONE system value.

TODO: Header defines this in hexadecimal. Not sure it makes any difference
Source: libdvdread/src/dvdread/ifo_types.h:230
"""

_BLOCK_TYPE_ANGLE_BLOCK = 1
"""
Preprocessor alias for BLOCK_TYPE_ANGLE_BLOCK system value.

TODO: Header defines this in hexadecimal. Not sure it makes any difference
Source: libdvdread/src/dvdread/ifo_types.h:231
"""

_BLOCK_MODE_NOT_IN_BLOCK = 0
"""
Preprocessor alias for BLOCK_MODE_NOT_IN_BLOCK system value.

TODO: Header defines this in hexadecimal. Not sure it makes any difference
Source: libdvdread/src/dvdread/ifo_types.h:233
"""

_BLOCK_MODE_FIRST_CELL = 1
"""
Preprocessor alias for BLOCK_MODE_FIRST_CELL system value.

TODO: Header defines this in hexadecimal. Not sure it makes any difference
Source: libdvdread/src/dvdread/ifo_types.h:234
"""

_BLOCK_MODE_IN_BLOCK = 2
"""
Preprocessor alias for BLOCK_MODE_IN_BLOCK system value.

TODO: Header defines this in hexadecimal. Not sure it makes any difference
Source: libdvdread/src/dvdread/ifo_types.h:235
"""

_BLOCK_MODE_LAST_CELL = 3
"""
Preprocessor alias for BLOCK_MODE_LAST_CELL system value.

TODO: Header defines this in hexadecimal. Not sure it makes any difference
Source: libdvdread/src/dvdread/ifo_types.h:236
"""


class _CellPositionT(ctypes.Structure):
    """
    Struct for the libdvdread cell_position_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:241
    """
    _fields_ = [
        ("vob_id_nr", ctypes.c_uint16),
        ("zero_1", ctypes.c_uint8),
        ("cell_nr", ctypes.c_uint8)
    ]


class _UserOpsT(ctypes.Structure):
    """
    Struct for the libdvdread user_ops_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:250
    """
    _fields_ = [
        ("zero", ctypes.c_ubyte, 7),
        ("video_pres_mode_change", ctypes.c_ubyte, 1),
        ("karaoke_audio_pres_mode_change", ctypes.c_ubyte, 1),
        ("angle_change", ctypes.c_ubyte, 1),
        ("subpic_stream_change", ctypes.c_ubyte, 1),
        ("audio_stream_change", ctypes.c_ubyte, 1),
        ("pause_on", ctypes.c_ubyte, 1),
        ("still_off", ctypes.c_ubyte, 1),
        ("button_select_or_activate", ctypes.c_ubyte, 1),
        ("resume", ctypes.c_ubyte, 1),
        ("chapter_menu_call", ctypes.c_ubyte, 1),
        ("angle_menu_call", ctypes.c_ubyte, 1),
        ("audio_menu_call", ctypes.c_ubyte, 1),
        ("subpic_menu_call", ctypes.c_ubyte, 1),
        ("root_menu_call", ctypes.c_ubyte, 1),
        ("title_menu_call", ctypes.c_ubyte, 1),
        ("backward_scan", ctypes.c_ubyte, 1),
        ("forward_scan", ctypes.c_ubyte, 1),
        ("next_pg_search", ctypes.c_ubyte, 1),
        ("prev_or_top_pg_search", ctypes.c_ubyte, 1),
        ("time_or_chapter_search", ctypes.c_ubyte, 1),
        ("go_up", ctypes.c_ubyte, 1),
        ("stop", ctypes.c_ubyte, 1),
        ("title_play", ctypes.c_ubyte, 1),
        ("chapter_search_or_play", ctypes.c_ubyte, 1),
        ("title_or_time_play", ctypes.c_ubyte, 1)
    ]


class _PGCT(ctypes.Structure):
    """
    Struct for the libdvdread pgc_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:285
    """
    _fields_ = [
        ("zero_1", ctypes.c_uint16),
        ("nr_of_programs", ctypes.c_uint8),
        ("nr_of_cells", ctypes.c_uint8),
        ("playback_time", _DVDTimeT),
        ("prohibited_ops", _UserOpsT),
        ("audio_control", ctypes.c_uint16 * 8),
        ("subp_control", ctypes.c_uint32 * 32),
        ("next_pgc_nr", ctypes.c_uint16),
        ("prev_pgc_nr", ctypes.c_uint16),
        ("goup_pgc_nr", ctypes.c_uint16),
        ("pg_playback_mode", ctypes.c_uint8),
        ("still_time", ctypes.c_uint8),
        ("palette", ctypes.c_uint32 * 16),
        ("command_tbl_offset", ctypes.c_uint16),
        ("program_map_offset", ctypes.c_uint16),
        ("cell_playback_offset", ctypes.c_uint16),
        ("cell_position_offset", ctypes.c_uint16),
        ("command_tbl", ctypes.POINTER(_PGCCommandTblT)),
        ("program_map", ctypes.POINTER(_PGCProgramMapT)),
        ("cell_playback", ctypes.POINTER(_CellPlaybackT)),
        ("cell_position", ctypes.POINTER(_CellPositionT)),
        ("ref_count", ctypes.c_int)
    ]


_PGC_SIZE = 236
"""
Preprocessor alias for PGC_SIZE system value.

Source: libdvdread/src/dvdread/ifo_types.h:309
"""


class _PGCISrPT(ctypes.Structure):
    """
    Struct for the libdvdread pgci_srp_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:314
    """
    _fields_ = [
        ("entry_id", ctypes.c_uint8),
        ("block_mode", ctypes.c_ubyte, 2),
        ("block_type", ctypes.c_ubyte, 2),
        ("zero_1", ctypes.c_ubyte, 4),
        ("ptl_id_mask", ctypes.c_uint16),
        ("pgc_start_byte", ctypes.c_uint32),
        ("pgc", ctypes.POINTER(_PGCT))
    ]


_PGCI_SRP_SIZE = 8
"""
Preprocessor alias for PGCI_SRP_SIZE system value.

Source: libdvdread/src/dvdread/ifo_types.h:323
"""


class _PGCITT(ctypes.Structure):
    """
    Struct for the libdvdread pgcit_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:328
    """
    _fields_ = [
        ("nr_of_pgci_srp", ctypes.c_uint16),
        ("zero_1", ctypes.c_uint16),
        ("last_byte", ctypes.c_uint32),
        ("pgci_srp", ctypes.POINTER(_PGCISrPT)),
        ("ref_count", ctypes.c_int)
    ]


_PGCIT_SIZE = 8
"""
Preprocessor alias for PGCIT_SIZE system value.

Source: libdvdread/src/dvdread/ifo_types.h:335
"""


class _PGCILUT(ctypes.Structure):
    """
    Struct for the libdvdread pgci_lu_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:340
    """
    _fields_ = [
        ("lang_code", ctypes.c_uint16),
        ("lang_extension", ctypes.c_uint8),
        ("exists", ctypes.c_uint8),
        ("lang_start_byte", ctypes.c_uint32),
        ("pgcit", ctypes.POINTER(_PGCITT))
    ]


_PGCI_LU_SIZE = 8
"""
Preprocessor alias for PGCI_LU_SIZE system value.

Source: libdvdread/src/dvdread/ifo_types.h:347
"""


class _PGCIUTT(ctypes.Structure):
    """
    Struct for the libdvdread pgci_ut_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:352
    """
    _fields_ = [
        ("nr_of_lus", ctypes.c_uint16),
        ("zero_1", ctypes.c_uint16),
        ("last_byte", ctypes.c_uint32),
        ("lu", ctypes.POINTER(_PGCILUT))
    ]


_PGCI_UT_SIZE = 8
"""
Preprocessor alias for PGCI_UT_SIZE system value.

Source: libdvdread/src/dvdread/ifo_types.h:358
"""


class _CellAdrT(ctypes.Structure):
    """
    Struct for the libdvdread cell_adr_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:363
    """
    _fields_ = [
        ("vob_id", ctypes.c_uint16),
        ("cell_id", ctypes.c_uint8),
        ("zero_1", ctypes.c_uint8),
        ("start_sector", ctypes.c_uint32),
        ("last_sector", ctypes.c_uint32)
    ]


class _CAdTT(ctypes.Structure):
    """
    Struct for the libdvdread c_adt_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:374
    """
    _fields_ = [
        ("nr_of_vobs", ctypes.c_uint16),
        ("zero_1", ctypes.c_uint16),
        ("last_byte", ctypes.c_uint32),
        ("cell_adr_table", ctypes.POINTER(_CellAdrT))
    ]


_C_ADT_SIZE = 8
"""
Preprocessor alias for C_ADT_SIZE system value.

Source: libdvdread/src/dvdread/ifo_types.h:380
"""


class _VOBUAdMapT(ctypes.Structure):
    """
    Struct for the libdvdread vobu_admap_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:385
    """
    _fields_ = [
        ("last_byte", ctypes.c_uint32),
        ("vobu_start_sectors", ctypes.POINTER(ctypes.c_uint32))
    ]


_VOBU_ADMAP_SIZE = 4
"""
Preprocessor alias for VOBU_ADMAP_SIZE system value.

Source: libdvdread/src/dvdread/ifo_types.h:389
"""


class _VMGIMatT(ctypes.Structure):
    """
    Struct for the libdvdread vmgi_mat_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:403
    """
    _fields_ = [
        ("vmg_identifier", ctypes.c_char * 12),
        ("vmg_last_sector", ctypes.c_uint32),
        ("zero_1", ctypes.c_uint8 * 12),
        ("vmgi_last_sector", ctypes.c_uint32),
        ("zero_2", ctypes.c_uint8),
        ("specification_version", ctypes.c_uint8),
        ("vmg_category", ctypes.c_uint32),
        ("vmg_nr_of_volumes", ctypes.c_uint16),
        ("vmg_this_volume_nr", ctypes.c_uint16),
        ("disc_side", ctypes.c_uint8),
        ("zero_3", ctypes.c_uint8 * 19),
        ("vmg_nr_of_title_sets", ctypes.c_uint16),
        ("provider_identifier", ctypes.c_char * 32),
        ("vmg_pos_code", ctypes.c_uint64),
        ("zero_4", ctypes.c_uint8 * 24),
        ("vmgi_last_byte", ctypes.c_uint32),
        ("first_play_pgc", ctypes.c_uint32),
        ("zero_5", ctypes.c_uint8 * 56),
        ("vmgm_vobs", ctypes.c_uint32),
        ("tt_srpt", ctypes.c_uint32),
        ("vmgm_pgci_ut", ctypes.c_uint32),
        ("ptl_mait", ctypes.c_uint32),
        ("vts_atrt", ctypes.c_uint32),
        ("txtdt_mgi", ctypes.c_uint32),
        ("vmgm_c_adt", ctypes.c_uint32),
        ("vmgm_vobu_admap", ctypes.c_uint32),
        ("zero_6", ctypes.c_uint8 * 32),
        ("vmgm_video_attr", _VideoAttrT),
        ("zero_7", ctypes.c_uint8),
        ("nr_of_vmgm_audio_streams", ctypes.c_uint8),
        ("vmgm_audio_attr", _AudioAttrT),
        ("zero_8", _AudioAttrT * 7),
        ("zero_9", ctypes.c_uint8 * 17),
        ("nr_of_vmgm_subp_streams", ctypes.c_uint8),
        ("vmgm_subp_attr", _SubPAttrT),
        ("zero_10", _SubPAttrT * 27)
    ]


class _PlaybackTypeT(ctypes.Structure):
    """
    Struct for the libdvdread playback_type_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:443
    """
    _fields_ = [
        ("zero_1", ctypes.c_ubyte, 1),
        ("multi_or_random_pgc_title", ctypes.c_ubyte, 1),
        ("jlc_exists_in_cell_cmd", ctypes.c_ubyte, 1),
        ("jlc_exists_in_prepost_cmd", ctypes.c_ubyte, 1),
        ("jlc_exists_in_button_cmd", ctypes.c_ubyte, 1),
        ("jlc_exists_in_tt_dom", ctypes.c_ubyte, 1),
        ("chapter_search_or_play", ctypes.c_ubyte, 1),
        ("title_or_time_play", ctypes.c_ubyte, 1)
    ]


class _TitleInfoT(ctypes.Structure):
    """
    Struct for the libdvdread title_info_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:457
    """
    _fields_ = [
        ("pb_ty", _PlaybackTypeT),
        ("nr_of_angles", ctypes.c_uint8),
        ("nr_of_ptts", ctypes.c_uint16),
        ("parental_id", ctypes.c_uint16),
        ("title_set_nr", ctypes.c_uint8),
        ("vts_ttn", ctypes.c_uint8),
        ("title_set_sector", ctypes.c_uint32)
    ]


class _TtSrPTT(ctypes.Structure):
    """
    Struct for the libdvdread tt_srpt_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:470
    """
    _fields_ = [
        ("nr_of_srpts", ctypes.c_uint16),
        ("zero_1", ctypes.c_uint16),
        ("last_byte", ctypes.c_uint32),
        ("title", ctypes.POINTER(_TitleInfoT))
    ]


_TT_SRPT_SIZE = 8
"""
Preprocessor alias for TT_SRPT_SIZE system value.

Source: libdvdread/src/dvdread/ifo_types.h:476
"""

_PTL_MAIT_NUM_LEVEL = 8
"""
Preprocessor alias for TT_SRPT_SIZE system value.

Source: libdvdread/src/dvdread/ifo_types.h:483
"""

_PFLevelT = ctypes.c_uint16 * _PTL_MAIT_NUM_LEVEL
"""
Representation of the pf_level_t typedef.

Source: libdvdread/src/dvdread/ifo_types.h:484
"""


class _PtlMaITCountryT(ctypes.Structure):
    """
    Struct for the libdvdread ptl_mait_country_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:489
    """
    _fields_ = [
        ("country_code", ctypes.c_uint16),
        ("zero_1", ctypes.c_uint16),
        ("pf_ptl_mai_start_byte", ctypes.c_uint16),
        ("zero_2", ctypes.c_uint16),
        ("pf_ptl_mai", ctypes.POINTER(_PFLevelT))
    ]


_PTL_MAIT_COUNTRY_SIZE = 8
"""
Preprocessor alias for PTL_MAIT_COUNTRY_SIZE system value.

Source: libdvdread/src/dvdread/ifo_types.h:496
"""


class _PtlMaITT(ctypes.Structure):
    """
    Struct for the libdvdread ptl_mait_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:501
    """
    _fields_ = [
        ("nr_of_countries", ctypes.c_uint16),
        ("nr_of_vtss", ctypes.c_uint16),
        ("last_byte", ctypes.c_uint32),
        ("countries", ctypes.POINTER(_PtlMaITCountryT))
    ]


_PTL_MAIT_SIZE = 8
"""
Preprocessor alias for PTL_MAIT_SIZE system value.

Source: libdvdread/src/dvdread/ifo_types.h:507
"""


class _VTSAttributesT(ctypes.Structure):
    """
    Struct for the libdvdread vts_attributes_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:512
    """
    _fields_ = [
        ("last_byte", ctypes.c_uint32),
        ("vts_cat", ctypes.c_uint32),
        ("vtsm_vobs_attr", _VideoAttrT),
        ("zero_1", ctypes.c_uint8),
        ("nr_of_vtsm_audio_streams", ctypes.c_uint8),
        ("vtsm_audio_attr", _AudioAttrT),
        ("zero_2", _AudioAttrT * 7),
        ("zero_3", ctypes.c_uint8 * 16),
        ("zero_4", ctypes.c_uint8),
        ("nr_of_vtsm_subp_streams", ctypes.c_uint8),
        ("vtsm_subp_attr", _SubPAttrT),
        ("zero_5", _SubPAttrT * 27),
        ("zero_6", ctypes.c_uint8 * 2),
        ("vtstt_vobs_video_attr", _VideoAttrT),
        ("zero_7", ctypes.c_uint8),
        ("nr_of_vtstt_audio_streams", ctypes.c_uint8),
        ("vtstt_audio_attr", _AudioAttrT * 8),
        ("zero_8", ctypes.c_uint8 * 16),
        ("zero_9", ctypes.c_uint8),
        ("nr_of_vtstt_subp_streams", ctypes.c_uint8),
        ("vtstt_subp_attr", _SubPAttrT * 32)
    ]


_VTS_ATTRIBUTES_SIZE = 542
"""
Preprocessor alias for VTS_ATTRIBUTES_SIZE system value.

Source: libdvdread/src/dvdread/ifo_types.h:538
"""

_VTS_ATTRIBUTES_MIN_SIZE = 356
"""
Preprocessor alias for VTS_ATTRIBUTES_MIN_SIZE system value.

Source: libdvdread/src/dvdread/ifo_types.h:539
"""


class _VTSAtrTT(ctypes.Structure):
    """
    Struct for the libdvdread vts_atrt_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:544
    """
    _fields_ = [
        ("nr_of_vtss", ctypes.c_uint16),
        ("zero_1", ctypes.c_uint16),
        ("last_byte", ctypes.c_uint32),
        ("vts", ctypes.POINTER(_VTSAttributesT)),
        ("vts_atrt_offsets", ctypes.POINTER(ctypes.c_uint32))
    ]


_VTS_ATRT_SIZE = 8
"""
Preprocessor alias for VTS_ATRT_SIZE system value.

Source: libdvdread/src/dvdread/ifo_types.h:551
"""


class _TxtDtT(ctypes.Structure):
    """
    Struct for the libdvdread txtdt_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:556
    """
    _fields_ = [
        ("last_byte", ctypes.c_uint32),
        ("offsets", ctypes.c_uint16 * 100),
        # Commented out in header file. May need to be commented out here, too.
        ("unknown", ctypes.c_uint16),
        ("zero_1", ctypes.c_uint16),
        ("type_of_info", ctypes.c_uint8),
        ("unknown1", ctypes.c_uint8),
        ("unknown2", ctypes.c_uint8),
        ("unknown3", ctypes.c_uint8),
        ("unknown4", ctypes.c_uint8),
        ("unknown5", ctypes.c_uint8),
        ("offset", ctypes.c_uint16),
        ("text", ctypes.c_char * 12)
    ]


class _TxtDtLUT(ctypes.Structure):
    """
    Struct for the libdvdread txtdt_lu_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:578
    """
    _fields_ = [
        ("lang_code", ctypes.c_uint16),
        ("zero_1", ctypes.c_uint8),
        ("char_set", ctypes.c_uint8),
        ("txtdt_start_byte", ctypes.c_uint32),
        ("txtdt", ctypes.POINTER(_TxtDtT))
    ]


_TXTDT_LU_SIZE = 8
"""
Preprocessor alias for TXTDT_LU_SIZE system value.

Source: libdvdread/src/dvdread/ifo_types.h:585
"""


class _TxtDtMgIT(ctypes.Structure):
    """
    Struct for the libdvdread txtdt_mgi_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:596
    """
    _fields_ = [
        ("disc_name", ctypes.c_char * 12),
        ("unknown1", ctypes.c_uint16),
        ("nr_of_language_units", ctypes.c_uint16),
        ("last_byte", ctypes.c_uint32),
        ("lu", ctypes.POINTER(_TxtDtLUT))
    ]


_TXTDT_MGI_SIZE = 20
"""
Preprocessor alias for TXTDT_MGI_SIZE system value.

Source: libdvdread/src/dvdread/ifo_types.h:597
"""


class _VTSIMaTT(ctypes.Structure):
    """
    Struct for the libdvdread vtsi_mat_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:609
    """
    _fields_ = [
        ("vts_identifier", ctypes.c_char * 12),
        ("vts_last_sector", ctypes.c_uint32),
        ("zero_1", ctypes.c_uint8 * 12),
        ("vtsi_last_sector", ctypes.c_uint32),
        ("zero_2", ctypes.c_uint8),
        ("specification_version", ctypes.c_uint8),
        ("vts_category", ctypes.c_uint32),
        ("zero_3", ctypes.c_uint16),
        ("zero_4", ctypes.c_uint16),
        ("zero_5", ctypes.c_uint8),
        ("zero_6", ctypes.c_uint8 * 19),
        ("zero_7", ctypes.c_uint16),
        ("zero_8", ctypes.c_uint8 * 32),
        ("zero_9", ctypes.c_uint64),
        ("zero_10", ctypes.c_uint8 * 24),
        ("vtsi_last_byte", ctypes.c_uint32),
        ("zero_11", ctypes.c_uint32),
        ("zero_12", ctypes.c_uint8 * 56),
        ("vtsm_vobs", ctypes.c_uint32),
        ("vtstt_vobs", ctypes.c_uint32),
        ("vts_ptt_srpt", ctypes.c_uint32),
        ("vts_pgcit", ctypes.c_uint32),
        ("vtsm_pgci_ut", ctypes.c_uint32),
        ("vts_tmapt", ctypes.c_uint32),
        ("vtsm_c_adt", ctypes.c_uint32),
        ("vtsm_vobu_admap", ctypes.c_uint32),
        ("vts_c_adt", ctypes.c_uint32),
        ("vts_vobu_admap", ctypes.c_uint32),
        ("zero_13", ctypes.c_uint8 * 24),
        ("vtsm_video_attr", _VideoAttrT),
        ("zero_14", ctypes.c_uint8),
        ("nr_of_vtsm_audio_streams", ctypes.c_uint8),
        ("vtsm_audio_attr", _AudioAttrT),
        ("zero_15", _AudioAttrT * 7),
        ("zero_16", ctypes.c_uint8 * 17),
        ("nr_of_vtsm_subp_streams", ctypes.c_uint8),
        ("vtsm_subp_attr", _SubPAttrT),
        ("zero_17", _SubPAttrT * 27),
        ("zero_18", ctypes.c_uint8 * 2),
        ("vts_video_attr", _VideoAttrT),
        ("zero_19", ctypes.c_uint8),
        ("nr_of_vts_audio_streams", ctypes.c_uint8),
        ("vts_audio_attr", _AudioAttrT * 8),
        ("zero_20", ctypes.c_uint8 * 17),
        ("nr_of_vts_subp_streams", ctypes.c_uint8),
        ("vts_subp_attr", _SubPAttrT * 32),
        ("zero_21", ctypes.c_uint16),
        ("vts_mu_audio_attr", _MultichannelExtT * 8)
    ]


class _PtTInfoT(ctypes.Structure):
    """
    Struct for the libdvdread ptt_info_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:666
    """
    _fields_ = [
        ("pgcn", ctypes.c_uint16),
        ("pgn", ctypes.c_uint16)
    ]


class _TTUT(ctypes.Structure):
    """
    Struct for the libdvdread ttu_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:674
    """
    _fields_ = [
        ("nr_of_ptts", ctypes.c_uint16),
        ("ptt", ctypes.POINTER(_PtTInfoT))
    ]


class _VTSPtTSrPTT(ctypes.Structure):
    """
    Struct for the libdvdread vts_ptt_srpt_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:682
    """
    _fields_ = [
        ("nr_of_srpts", ctypes.c_uint16),
        ("zero_1", ctypes.c_uint16),
        ("last_byte", ctypes.c_uint32),
        ("title", ctypes.POINTER(_TTUT)),
        ("ttu_offset", ctypes.POINTER(ctypes.c_uint32))
    ]


_VTS_PTT_SRPT_SIZE = 8
"""
Preprocessor alias for VTS_PTT_SRPT_SIZE system value.

Source: libdvdread/src/dvdread/ifo_types.h:689
"""

_MapEntT = ctypes.c_uint32
"""
Representation of the map_ent_t typedef.

Source: libdvdread/src/dvdread/ifo_types.h:696
"""


class _VTSTMapT(ctypes.Structure):
    """
    Struct for the libdvdread vts_tmap_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:701
    """
    _fields_ = [
        ("tmu", ctypes.c_uint8),
        ("zero_1", ctypes.c_uint8),
        ("nr_of_entries", ctypes.c_uint16),
        ("map_ent", ctypes.POINTER(_MapEntT))
    ]


_VTS_TMAP_SIZE = 4
"""
Preprocessor alias for VTS_TMAP_SIZE system value.

Source: libdvdread/src/dvdread/ifo_types.h:707
"""


class _VTSTMapTT(ctypes.Structure):
    """
    Struct for the libdvdread vts_tmapt_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:712
    """
    _fields_ = [
        ("nr_of_tmaps", ctypes.c_uint16),
        ("zero_1", ctypes.c_uint16),
        ("last_byte", ctypes.c_uint32),
        ("tmap", ctypes.POINTER(_VTSTMapT)),
        ("tmap_offset", ctypes.POINTER(ctypes.c_uint32))
    ]


_VTS_TMAPT_SIZE = 8
"""
Preprocessor alias for VTS_TMAPT_SIZE system value.

Source: libdvdread/src/dvdread/ifo_types.h:719
"""


class _IFOHandleT(ctypes.Structure):
    """
    Struct for the libdvdread ifo_handle_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/ifo_types.h:733
    """
    _fields_ = [
        ("vmgi_mat", ctypes.POINTER(_VMGIMatT)),
        ("tt_srpt", ctypes.POINTER(_TtSrPTT)),
        ("first_play_pgc", ctypes.POINTER(_PGCT)),
        ("ptl_mait", ctypes.POINTER(_PtlMaITT)),
        ("vts_atrt", ctypes.POINTER(_VTSAtrTT)),
        ("txtdt_mgi", ctypes.POINTER(_TxtDtMgIT)),
        ("pgci_ut", ctypes.POINTER(_PGCIUTT)),
        ("menu_c_adt", ctypes.POINTER(_CAdTT)),
        ("menu_vobu_admap", ctypes.POINTER(_VOBUAdMapT)),
        ("vtsi_mat", ctypes.POINTER(_VTSIMaTT)),
        ("vts_ptt_srpt", ctypes.POINTER(_VTSPtTSrPTT)),
        ("vts_pgcit", ctypes.POINTER(_PGCITT)),
        ("vts_tmapt", ctypes.POINTER(_VTSTMapTT)),
        ("vts_c_adt", ctypes.POINTER(_CAdTT)),
        ("vts_vobu_admap", ctypes.POINTER(_VOBUAdMapT))
    ]


# </editor-fold>

# <editor-fold desc="Grouping for libdvdread/src/dvdread/ifo_print.h header file.">
ifo_print = _libdvdread.ifo_print
"""
Function wrapper for libdvdread ifo_print.

Source: libdvdread/src/dvdread/ifo_print.h:27
"""
ifo_print.restype = None
ifo_print.argtypes = (
    ctypes.POINTER(_DVDReaderT),
    ctypes.c_int
)

dvdread_print_time = _libdvdread.dvdread_print_time
"""
Function wrapper for libdvdread dvdread_print_time.

Source: libdvdread/src/dvdread/ifo_print.h:28
"""
dvdread_print_time.restype = None
dvdread_print_time.argtypes = (
    ctypes.POINTER(_DVDTimeT),
)
# </editor-fold>

# <editor-fold desc="Grouping for libdvdread/src/dvdread/ifo_read.h header file.">
ifo_open = _libdvdread.ifoOpen
"""
Function wrapper for libdvdread ifoOpen.

Source: libdvdread/src/dvdread/ifo_read.h:40
"""
ifo_open.restype = ctypes.POINTER(_IFOHandleT)
ifo_open.argtypes = (
    ctypes.POINTER(_DVDReaderT),
    ctypes.c_int
)

ifo_open_vmgi = _libdvdread.ifoOpenVMGI
"""
Function wrapper for libdvdread ifoOpenVMGI.

Source: libdvdread/src/dvdread/ifo_read.h:49
"""
ifo_open_vmgi.restype = ctypes.POINTER(_IFOHandleT)
ifo_open_vmgi.argtypes = (
    ctypes.POINTER(_DVDReaderT),
)

ifo_open_vtsi = _libdvdread.ifoOpenVTSI
"""
Function wrapper for libdvdread ifoOpenVTSI.

Source: libdvdread/src/dvdread/ifo_read.h:58
"""
ifo_open_vtsi.restype = ctypes.POINTER(_IFOHandleT)
ifo_open_vtsi.argtypes = (
    ctypes.POINTER(_DVDReaderT),
    ctypes.c_int
)

ifo_close = _libdvdread.ifoClose
"""
Function wrapper for libdvdread ifoClose.

Source: libdvdread/src/dvdread/ifo_read.h:65
"""
ifo_close.restype = None
ifo_close.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_read_ptl_mait = _libdvdread.ifoRead_PTL_MAIT
"""
Function wrapper for libdvdread ifoRead_PTL_MAIT.

Source: libdvdread/src/dvdread/ifo_read.h:80
"""
ifo_read_ptl_mait.restype = ctypes.c_int
ifo_read_ptl_mait.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_read_vts_atrt = _libdvdread.ifoRead_VTS_ATRT
"""
Function wrapper for libdvdread ifoRead_VTS_ATRT.

Source: libdvdread/src/dvdread/ifo_read.h:90
"""
ifo_read_vts_atrt.restype = ctypes.c_int
ifo_read_vts_atrt.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_read_tt_srpt = _libdvdread.ifoRead_TT_SRPT
"""
Function wrapper for libdvdread ifoRead_TT_SRPT.

Source: libdvdread/src/dvdread/ifo_read.h:99
"""
ifo_read_tt_srpt.restype = ctypes.c_int
ifo_read_tt_srpt.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_read_vts_ptt_srpt = _libdvdread.ifoRead_VTS_PTT_SRPT
"""
Function wrapper for libdvdread ifoRead_VTS_PTT_SRPT.

Source: libdvdread/src/dvdread/ifo_read.h:109
"""
ifo_read_vts_ptt_srpt.restype = ctypes.c_int
ifo_read_vts_ptt_srpt.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_read_fp_pgc = _libdvdread.ifoRead_FP_PGC
"""
Function wrapper for libdvdread ifoRead_FP_PGC.

Source: libdvdread/src/dvdread/ifo_read.h:118
"""
ifo_read_fp_pgc.restype = ctypes.c_int
ifo_read_fp_pgc.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_read_pgcit = _libdvdread.ifoRead_PGCIT
"""
Function wrapper for libdvdread ifoRead_PGCIT.

Source: libdvdread/src/dvdread/ifo_read.h:129
"""
ifo_read_pgcit.restype = ctypes.c_int
ifo_read_pgcit.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_read_pgci_ut = _libdvdread.ifoRead_PGCI_UT
"""
Function wrapper for libdvdread ifoRead_PGCI_UT.

Source: libdvdread/src/dvdread/ifo_read.h:141
"""
ifo_read_pgci_ut.restype = ctypes.c_int
ifo_read_pgci_ut.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_read_vts_tmapt = _libdvdread.ifoRead_VTS_TMAPT
"""
Function wrapper for libdvdread ifoRead_VTS_TMAPT.

Source: libdvdread/src/dvdread/ifo_read.h:151
"""
ifo_read_vts_tmapt.restype = ctypes.c_int
ifo_read_vts_tmapt.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_read_c_adt = _libdvdread.ifoRead_C_ADT
"""
Function wrapper for libdvdread ifoRead_C_ADT.

Source: libdvdread/src/dvdread/ifo_read.h:163
"""
ifo_read_c_adt.restype = ctypes.c_int
ifo_read_c_adt.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_read_title_c_adt = _libdvdread.ifoRead_TITLE_C_ADT
"""
Function wrapper for libdvdread ifoRead_TITLE_C_ADT.

Source: libdvdread/src/dvdread/ifo_read.h:173
"""
ifo_read_title_c_adt.restype = ctypes.c_int
ifo_read_title_c_adt.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_read_vobu_admap = _libdvdread.ifoRead_VOBU_ADMAP
"""
Function wrapper for libdvdread ifoRead_VOBU_ADMAP.

Source: libdvdread/src/dvdread/ifo_read.h:185
"""
ifo_read_vobu_admap.restype = ctypes.c_int
ifo_read_vobu_admap.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_read_title_vobu_admap = _libdvdread.ifoRead_TITLE_VOBU_ADMAP
"""
Function wrapper for libdvdread ifoRead_TITLE_VOBU_ADMAP.

Source: libdvdread/src/dvdread/ifo_read.h:195
"""
ifo_read_title_vobu_admap.restype = ctypes.c_int
ifo_read_title_vobu_admap.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_read_txtdt_mgi = _libdvdread.ifoRead_TXTDT_MGI
"""
Function wrapper for libdvdread ifoRead_TXTDT_MGI.

Source: libdvdread/src/dvdread/ifo_read.h:205
"""
ifo_read_txtdt_mgi.restype = ctypes.c_int
ifo_read_txtdt_mgi.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_free_ptl_mait = _libdvdread.ifoFree_PTL_MAIT
"""
Function wrapper for libdvdread ifoFree_PTL_MAIT.

Source: libdvdread/src/dvdread/ifo_read.h:213
"""
ifo_free_ptl_mait.restype = None
ifo_free_ptl_mait.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_free_vts_atrt = _libdvdread.ifoFree_VTS_ATRT
"""
Function wrapper for libdvdread ifoFree_VTS_ATRT.

Source: libdvdread/src/dvdread/ifo_read.h:214
"""
ifo_free_vts_atrt.restype = None
ifo_free_vts_atrt.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_free_tt_srpt = _libdvdread.ifoFree_TT_SRPT
"""
Function wrapper for libdvdread ifoFree_TT_SRPT.

Source: libdvdread/src/dvdread/ifo_read.h:215
"""
ifo_free_tt_srpt.restype = None
ifo_free_tt_srpt.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_free_vts_ptt_srpt = _libdvdread.ifoFree_VTS_PTT_SRPT
"""
Function wrapper for libdvdread ifoFree_VTS_PTT_SRPT.

Source: libdvdread/src/dvdread/ifo_read.h:216
"""
ifo_free_vts_ptt_srpt.restype = None
ifo_free_vts_ptt_srpt.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_free_fp_pgc = _libdvdread.ifoFree_FP_PGC
"""
Function wrapper for libdvdread ifoFree_FP_PGC.

Source: libdvdread/src/dvdread/ifo_read.h:217
"""
ifo_free_fp_pgc.restype = None
ifo_free_fp_pgc.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_free_pgcit = _libdvdread.ifoFree_PGCIT
"""
Function wrapper for libdvdread ifoFree_PGCIT.

Source: libdvdread/src/dvdread/ifo_read.h:218
"""
ifo_free_pgcit.restype = None
ifo_free_pgcit.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_free_pgci_ut = _libdvdread.ifoFree_PGCI_UT
"""
Function wrapper for libdvdread ifoFree_PGCI_UT.

Source: libdvdread/src/dvdread/ifo_read.h:219
"""
ifo_free_pgci_ut.restype = None
ifo_free_pgci_ut.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_free_vts_tmapt = _libdvdread.ifoFree_VTS_TMAPT
"""
Function wrapper for libdvdread ifoFree_VTS_TMAPT.

Source: libdvdread/src/dvdread/ifo_read.h:220
"""
ifo_free_vts_tmapt.restype = None
ifo_free_vts_tmapt.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_free_c_adt = _libdvdread.ifoFree_C_ADT
"""
Function wrapper for libdvdread ifoFree_C_ADT.

Source: libdvdread/src/dvdread/ifo_read.h:221
"""
ifo_free_c_adt.restype = None
ifo_free_c_adt.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_free_title_c_adt = _libdvdread.ifoFree_TITLE_C_ADT
"""
Function wrapper for libdvdread ifoFree_TITLE_C_ADT.

Source: libdvdread/src/dvdread/ifo_read.h:222
"""
ifo_free_title_c_adt.restype = None
ifo_free_title_c_adt.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_free_vobu_admap = _libdvdread.ifoFree_VOBU_ADMAP
"""
Function wrapper for libdvdread ifoFree_VOBU_ADMAP.

Source: libdvdread/src/dvdread/ifo_read.h:223
"""
ifo_free_vobu_admap.restype = None
ifo_free_vobu_admap.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_free_title_vobu_admap = _libdvdread.ifoFree_TITLE_VOBU_ADMAP
"""
Function wrapper for libdvdread ifoFree_TITLE_VOBU_ADMAP.

Source: libdvdread/src/dvdread/ifo_read.h:224
"""
ifo_free_title_vobu_admap.restype = None
ifo_free_title_vobu_admap.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)

ifo_free_txtdt_mgi = _libdvdread.ifoFree_TXTDT_MGI
"""
Function wrapper for libdvdread ifoFree_TXTDT_MGI.

Source: libdvdread/src/dvdread/ifo_read.h:225
"""
ifo_free_txtdt_mgi.restype = None
ifo_free_txtdt_mgi.argtypes = (
    ctypes.POINTER(_IFOHandleT),
)
# </editor-fold>

# <editor-fold desc="Grouping for libdvdread/src/dvdread/nav_types.h header file.">
_PCI_BYTES = int("3d4", 16)
"""
Preprocessor alias for PCI_BYTES system value.

Source: libdvdread/src/dvdread/nav_types.h:37
"""

_DSI_BYTES = int("3fa", 16)
"""
Preprocessor alias for DSI_BYTES system value.

Source: libdvdread/src/dvdread/nav_types.h:38
"""

_PS2_PCI_SUBSTREAM_ID = 0
"""
Preprocessor alias for PS2_PCI_SUBSTREAM_ID system value.

Source: libdvdread/src/dvdread/nav_types.h:40
"""

_PS2_DSI_SUBSTREAM_ID = 1
"""
Preprocessor alias for PS2_DSI_SUBSTREAM_ID system value.

Source: libdvdread/src/dvdread/nav_types.h:41
"""

_DSI_START_BYTE = 1031
"""
Preprocessor alias for DSI_START_BYTE system value.

Source: libdvdread/src/dvdread/nav_types.h:44
"""


class _PCIGIT(ctypes.Structure):
    """
    Struct for the libdvdread pci_gi_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/nav_types.h:49
    """
    _fields_ = [
        ("nv_pck_lbn", ctypes.c_uint32),
        ("vobu_cat", ctypes.c_uint16),
        ("zero1", ctypes.c_uint16),
        ("vobu_uop_ctl", _UserOpsT),
        ("vobu_s_ptm", ctypes.c_uint32),
        ("vobu_e_ptm", ctypes.c_uint32),
        ("vobu_se_e_ptm", ctypes.c_uint32),
        ("e_eltm", _DVDTimeT),
        ("vobu_isrc", ctypes.c_char * 32)
    ]


class _NSmlAglIT(ctypes.Structure):
    """
    Struct for the libdvdread nsml_agli_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/nav_types.h:64
    """
    _fields_ = [
        ("nsml_agl_dsta", ctypes.c_uint32 * 9)
    ]


class _HLGIT(ctypes.Structure):
    """
    Struct for the libdvdread hl_gi_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/nav_types.h:77
    """
    _fields_ = [
        ("hli_ss", ctypes.c_uint16),
        ("hli_s_ptm", ctypes.c_uint32),
        ("hli_e_ptm", ctypes.c_uint32),
        ("btn_se_e_ptm", ctypes.c_uint32),
        ("zero1", ctypes.c_ubyte, 2),
        ("btngr_ns", ctypes.c_ubyte, 2),
        ("zero2", ctypes.c_ubyte, 1),
        ("btngr1_dsp_ty", ctypes.c_ubyte, 3),
        ("zero3", ctypes.c_ubyte, 1),
        ("btngr2_dsp_ty", ctypes.c_ubyte, 3),
        ("zero4", ctypes.c_ubyte, 1),
        ("btngr3_dsp_ty", ctypes.c_ubyte, 3),
        ("btn_ofn", ctypes.c_uint8),
        ("btn_ns", ctypes.c_uint8),
        ("nsl_btn_ns", ctypes.c_uint8),
        ("zero5", ctypes.c_uint8),
        ("fosl_btnn", ctypes.c_uint8),
        ("foac_btnn", ctypes.c_uint8)
    ]


class _BtnColITT(ctypes.Structure):
    """
    Struct for the libdvdread btn_colit_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/nav_types.h:107
    """
    _fields_ = [
        ("btn_coli", ctypes.c_uint32 * 3 * 2)
    ]


class _BtnIT(ctypes.Structure):
    """
    Struct for the libdvdread btni_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/nav_types.h:118
    """
    _fields_ = [
        ("btn_coln", ctypes.c_uint, 2),
        ("x_start", ctypes.c_uint, 10),
        ("zero1", ctypes.c_uint, 2),
        ("x_end", ctypes.c_uint, 10),
        ("auto_action_mode", ctypes.c_uint, 2),
        ("y_start", ctypes.c_uint, 10),
        ("zero2", ctypes.c_uint, 2),
        ("y_end", ctypes.c_uint, 10),
        ("zero3", ctypes.c_uint, 2),
        ("up", ctypes.c_uint, 6),
        ("zero4", ctypes.c_uint, 2),
        ("down", ctypes.c_uint, 6),
        ("zero5", ctypes.c_uint, 2),
        ("left", ctypes.c_uint, 6),
        ("zero6", ctypes.c_uint, 2),
        ("right", ctypes.c_uint, 6),
        ("cmd", _VMCmdT)
    ]


class _HLIT(ctypes.Structure):
    """
    Struct for the libdvdread hli_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/nav_types.h:143
    """
    _fields_ = [
        ("hl_gi", _HLGIT),
        ("btn_colit", _BtnColITT),
        ("btnit", _BtnIT * 36)
    ]


class _PCIT(ctypes.Structure):
    """
    Struct for the libdvdread pci_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/nav_types.h:152
    """
    _fields_ = [
        ("pci_gi", _PCIGIT),
        ("nsml_agli", _NSmlAglIT),
        ("hli", _HLIT),
        ("zero1", ctypes.c_uint8 * 189)
    ]


class _DSIGIT(ctypes.Structure):
    """
    Struct for the libdvdread dsi_gi_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/nav_types.h:165
    """
    _fields_ = [
        ("nv_pck_scr", ctypes.c_uint32),
        ("nv_pck_lbn", ctypes.c_uint32),
        ("vobu_ea", ctypes.c_uint32),
        ("vobu_1stref_ea", ctypes.c_uint32),
        ("vobu_2ndref_ea", ctypes.c_uint32),
        ("vobu_3rdref_ea", ctypes.c_uint32),
        ("vobu_vob_idn", ctypes.c_uint16),
        ("zero1", ctypes.c_uint8),
        ("vobu_c_idn", ctypes.c_uint8),
        ("c_eltm", _DVDTimeT)
    ]


class _SmlPBIT(ctypes.Structure):
    """
    Struct for the libdvdread sml_pbi_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/nav_types.h:181
    """

    class _VOBA(ctypes.Structure):
        """
        Struct for the libdvdread vob_a type.

        TODO: header file sets packing. Seems Python does this automatically.
        Source: libdvdread/src/dvdread/nav_types.h:188
        """
        _fields_ = [
            ("stp_ptm1", ctypes.c_uint32),
            ("stp_ptm2", ctypes.c_uint32),
            ("gap_len1", ctypes.c_uint32),
            ("gap_len2", ctypes.c_uint32)
        ]

    _fields_ = [
        ("category", ctypes.c_uint16),
        ("ilvu_ea", ctypes.c_uint32),
        ("ilvu_sa", ctypes.c_uint32),
        ("size", ctypes.c_uint16),
        ("vob_v_s_s_ptm", ctypes.c_uint32),
        ("vob_v_e_e_ptm", ctypes.c_uint32),
        ("vob_a", _VOBA * 8)
    ]


class _SmlAglDataT(ctypes.Structure):
    """
    Struct for the libdvdread sml_agl_data_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/nav_types.h:199
    """
    _fields_ = [
        ("address", ctypes.c_uint32),
        ("size", ctypes.c_uint16)
    ]


class _SmlAglIT(ctypes.Structure):
    """
    Struct for the libdvdread sml_agli_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/nav_types.h:207
    """
    _fields_ = [
        ("data", _SmlAglDataT * 9)
    ]


class _VOBUSrIT(ctypes.Structure):
    """
    Struct for the libdvdread vobu_sri_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/nav_types.h:214
    """
    _fields_ = [
        ("next_video", ctypes.c_uint32),
        ("fwda", ctypes.c_uint32 * 19),
        ("next_vobu", ctypes.c_uint32),
        ("prev_vobu", ctypes.c_uint32),
        ("bwda", ctypes.c_uint32 * 19),
        ("prev_video", ctypes.c_uint32)
    ]


_SRI_END_OF_CELL = int("3fffffff", 16)
"""
Preprocessor alias for XXX system value.

Source: libdvdread/src/dvdread/nav_types.h:223
"""


class _SyncIT(ctypes.Structure):
    """
    Struct for the libdvdread synci_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/nav_types.h:228
    """
    _fields_ = [
        ("a_synca", ctypes.c_uint16 * 8),
        ("sp_synca", ctypes.c_uint32 * 32)
    ]


class _DSIT(ctypes.Structure):
    """
    Struct for the libdvdread dsi_t type.

    TODO: header file sets packing. Seems Python does this automatically.
    Source: libdvdread/src/dvdread/nav_types.h:236
    """
    _fields_ = [
        ("dsi_gi", _DSIGIT),
        ("sml_pbi", _SmlPBIT),
        ("sml_agli", _SmlAglIT),
        ("vobu_sri", _VOBUSrIT),
        ("synci", _SyncIT),
        ("zero1", ctypes.c_uint8 * 471)
    ]


# </editor-fold>

# <editor-fold desc="Grouping for libdvdread/src/dvdread/nav_print.h header file.">
nav_print_pci = _libdvdread.navPrint_PCI
"""
Function wrapper for libdvdread navPrint_PCI.

Source: libdvdread/src/dvdread/nav_print.h:42
"""
nav_print_pci.restype = None
nav_print_pci.argtypes = (
    ctypes.POINTER(_PCIT),
)

nav_print_dsi = _libdvdread.navPrint_DSI
"""
Function wrapper for libdvdread navPrint_DSI.

Source: libdvdread/src/dvdread/nav_print.h:49
"""
nav_print_dsi.restype = None
nav_print_dsi.argtypes = (
    ctypes.POINTER(_DSIT),
)
# </editor-fold>

# <editor-fold desc="Grouping for libdvdread/src/dvdread/nav_read.h header file.">
nav_read_pci = _libdvdread.navRead_PCI
"""
Function wrapper for libdvdread navRead_PCI.

Source: libdvdread/src/dvdread/nav_read.h:41
"""
nav_read_pci.restype = None
nav_read_pci.argtypes = (
    ctypes.POINTER(_PCIT),
    ctypes.POINTER(ctypes.c_ubyte)
)

nav_read_dsi = _libdvdread.navRead_DSI
"""
Function wrapper for libdvdread navRead_DSI.

Source: libdvdread/src/dvdread/nav_read.h:49
"""
nav_read_dsi.restype = None
nav_read_dsi.argtypes = (
    ctypes.POINTER(_DSIT),
    ctypes.POINTER(ctypes.c_ubyte)
)
# </editor-fold>


# Sadly, this has to be declared all the way down here because of the circular
# references in the original header files.
_DVDInputS._fields_ = [
    ("dvdcss", _DVDCSST),
    ("priv", ctypes.c_void_p),
    ("logcb", ctypes.POINTER(_DVDLoggerCB)),
    ("ipos", _OffT),
    ("fd", ctypes.c_int),
    ("stream_cb", ctypes.POINTER(_DVDReaderStreamCB))
]

# Sadly, this has to be declared all the way down here because of the circular
# references in the original header files.
_DVDFileS._fields_ = [
    ("ctx", ctypes.POINTER(_DVDReaderT)),
    ("css_title", ctypes.c_int),
    ("lb_start", ctypes.c_uint32),
    ("seek_pos", ctypes.c_uint32),
    ("title_sizes", ctypes.c_size_t * _TITLES_MAX),
    ("title_devs", _DVDInputT * _TITLES_MAX),
    ("filesize", ctypes.c_ssize_t),
    ("cache", ctypes.POINTER(ctypes.c_ubyte))
]

# Sadly, this has to be declared all the way down here because of the circular
# references in the original header files.
_DVDReaderS._fields_ = [
    ("rd", ctypes.POINTER(_DVDReaderDeviceT)),
    ("priv", ctypes.c_void_p),
    ("logcb", _DVDLoggerCB),
    ("ifoBUPflags", ctypes.c_uint64 * 2)
]
