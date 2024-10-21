# pyOCD debugger
# Copyright (c) 2024 Huada Semiconductor Corporation
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ...coresight.coresight_target import CoreSightTarget
from ...core.memory_map import (FlashRegion, RamRegion, MemoryMap)
from ...debug.svd.loader import SVDFile


class DBGMCU:
    MCUSTPCTL = 0x40015004
    MCUSTPCTL_VALUE = 0x09


FLASH_ALGO = {
    'load_address' : 0x20000000,

    # Flash algorithm as a hex string
    'instructions': [
    0xE00ABE00,
    0x4770ba40, 0x4770ba40, 0x4770ba40, 0x4770bac0, 0x4770bac0, 0x4770bac0, 0x49022001, 0x49026088,
    0x47707088, 0x40000800, 0x40000a80, 0xf000b510, 0xbd10f819, 0x4604b510, 0xf0004620, 0xbd10f847,
    0x49062000, 0x200260c8, 0x20076088, 0x70884904, 0x43c02000, 0x60084901, 0x00004770, 0x40000800,
    0x40000a80, 0x2400b510, 0x49162001, 0x460860c8, 0x21ff68c0, 0x43083151, 0x60c84912, 0x60002000,
    0x1c64e007, 0x42844810, 0xf000d303, 0x2001f945, 0x480cbd10, 0x21ff6900, 0x40083101, 0xd1f04288,
    0x4808e005, 0x21106940, 0x49064308, 0x48056148, 0x21106900, 0x28004008, 0x4902d1f3, 0xbf0060c8,
    0x0000e7e6, 0x40000800, 0x00061a80, 0x4604b570, 0xf0002500, 0x2001f921, 0x60c84915, 0x68c04608,
    0x314121ff, 0x49124308, 0x200060c8, 0xe0076020, 0x48101c6d, 0xd3034285, 0xf90ef000, 0xbd702001,
    0x6900480b, 0x310121ff, 0x42884008, 0xe005d1f0, 0x69404807, 0x43082110, 0x61484905, 0x69004804,
    0x40082110, 0xd1f32800, 0x60c84901, 0xe7e6bf00, 0x40000800, 0x00061a80, 0x20ffb510, 0x49033024,
    0x48036008, 0xf7ff6008, 0xbd10ff67, 0x40000800, 0x00003210, 0xb082b5f7, 0x2000460c, 0x9f049001,
    0xf8daf000, 0x49432001, 0x460860c8, 0x21ff68c0, 0x43083131, 0x60c8493f, 0x26009d02, 0x6838e026,
    0x20006028, 0xe00b9001, 0x1c409801, 0x493a9001, 0x42889801, 0xf000d304, 0x2001f8bf, 0xbdf0b005,
    0x69004834, 0x40082110, 0xd1ed2810, 0x4831e005, 0x21106940, 0x492f4308, 0x482e6148, 0x21106900,
    0x28104008, 0x1d3fd0f3, 0x1c761d2d, 0x42b008a0, 0x07a0d8d5, 0x28000f80, 0x9700d030, 0xe0282600,
    0x78009800, 0x20007028, 0xe00a9001, 0x1c409801, 0x49219001, 0x42889801, 0xf000d303, 0x2001f88d,
    0x481ce7cc, 0x21106900, 0x28104008, 0xe005d1ee, 0x69404818, 0x43082110, 0x61484916, 0x69004815,
    0x40082110, 0xd0f32810, 0x1c409800, 0x1c6d9000, 0x07a01c76, 0x42b00f80, 0xbf00d8d2, 0x490d2000,
    0x900160c8, 0x9801e00a, 0x90011c40, 0x9801490a, 0xd3034288, 0xf860f000, 0xe79f2001, 0x69004805,
    0x310121ff, 0x42884008, 0xf000d1ed, 0x2000f855, 0x0000e794, 0x40000800, 0x00009c40, 0x4604b570,
    0x4616460d, 0xff58f7ff, 0xbd702000, 0x4604b570, 0x4616460d, 0x46294632, 0xf7ff4620, 0xbd70ff5b,
    0x49034802, 0x48036088, 0x47706088, 0xffff0123, 0x4000cc00, 0xffff3210, 0x4604b510, 0xfec0f7ff,
    0xbd102000, 0x4603b5f8, 0x2100460c, 0x20002600, 0x461e9000, 0xe0062500, 0x6817ce01, 0xd00042b8,
    0x1d12e004, 0x08a01c6d, 0xd8f542a8, 0x9600bf00, 0xe0082100, 0x78079800, 0x90001c40, 0x42875c50,
    0xe004d000, 0x07a01c49, 0x42880f80, 0xbf00d8f2, 0x18c000a8, 0xbdf81840, 0x4804b510, 0x07c06800,
    0x28000fc0, 0xf000d101, 0xbd10f803, 0x40010680, 0x4823b570, 0xb2846840, 0x68004822, 0x4008210c,
    0x48200886, 0x210f6800, 0x40080209, 0x2e000a05, 0x11a4d101, 0x2e01e008, 0x12a4d101, 0x2e02e004,
    0x1324d101, 0x13a4e000, 0xd0012d00, 0xd1022d0f, 0xff96f7ff, 0x07e8e022, 0x28000fc0, 0x2c00d004,
    0xf7ffd11c, 0xe019ff8d, 0x40282002, 0xd1042802, 0xd1132c01, 0xff84f7ff, 0x2004e010, 0x28044028,
    0x2c02d104, 0xf7ffd10a, 0xe007ff7b, 0x40282008, 0xd1032808, 0xd1012c03, 0xff72f7ff, 0x0000bd70,
    0x4000cc00, 0x40010680, 0x00000000
    ],

    # Relative function addresses
    'pc_init': 0x20000281,
    'pc_unInit': 0x200002bd,
    'pc_program_page': 0x20000291,
    'pc_erase_sector': 0x20000039,
    'pc_eraseAll': 0x20000031,

    'static_base' : 0x20000000 + 0x00000004 + 0x000003c8,
    'begin_stack' : 0x20000600,
    'begin_data' : 0x20000000 + 0x1000,
    'page_size' : 0x200,
    'analyzer_supported' : False,
    'analyzer_address' : 0x00000000,
    'page_buffers' : [0x20001000, 0x20001200],   # Enable double buffering
    'min_program_length' : 0x200,

    # Flash information
    'flash_start': 0x0,
    'flash_size': 0x40000,
    'sector_sizes': (
        (0x0, 0x200),
    )
}


FLASH_ALGO_NVR = {
    'load_address' : 0x20000000,

    # Flash algorithm as a hex string
    'instructions': [
    0xE00ABE00,
    0x4770ba40, 0x4770ba40, 0x4770ba40, 0x4770bac0, 0x4770bac0, 0x4770bac0, 0x49022001, 0x49026088,
    0x47707088, 0x40000800, 0x40000a80, 0xf000b510, 0xbd10f819, 0x4604b510, 0xf0004620, 0xbd10f86b,
    0x49062000, 0x200260c8, 0x20076088, 0x70884904, 0x43c02000, 0x60084901, 0x00004770, 0x40000800,
    0x40000a80, 0x2400b510, 0x49262001, 0x460860c8, 0x21ff68c0, 0x43083141, 0x60c84922, 0x49222000,
    0xe0076008, 0x48211c64, 0xd3034284, 0xf968f000, 0xbd102001, 0x6900481b, 0x310121ff, 0x42884008,
    0xe005d1f0, 0x69404817, 0x43082110, 0x61484915, 0x69004814, 0x40082110, 0xd1f32800, 0x60084914,
    0x1c64e007, 0x42844811, 0xf000d303, 0x2001f949, 0x480ce7df, 0x21ff6900, 0x40083101, 0xd1f04288,
    0x4808e005, 0x21106940, 0x49064308, 0x48056148, 0x21106900, 0x28004008, 0x4902d1f3, 0xbf0060c8,
    0x0000e7c7, 0x40000800, 0x01000800, 0x00061a80, 0x01000a00, 0x4604b570, 0xf0002500, 0x2001f921,
    0x60c84915, 0x68c04608, 0x314121ff, 0x49124308, 0x200060c8, 0xe0076020, 0x48101c6d, 0xd3034285,
    0xf90ef000, 0xbd702001, 0x6900480b, 0x310121ff, 0x42884008, 0xe005d1f0, 0x69404807, 0x43082110,
    0x61484905, 0x69004804, 0x40082110, 0xd1f32800, 0x60c84901, 0xe7e6bf00, 0x40000800, 0x00061a80,
    0x20ffb510, 0x49033024, 0x48036008, 0xf7ff6008, 0xbd10ff43, 0x40000800, 0x00003210, 0xb082b5f7,
    0x2000460c, 0x9f049001, 0xf8daf000, 0x49432001, 0x460860c8, 0x21ff68c0, 0x43083131, 0x60c8493f,
    0x26009d02, 0x6838e026, 0x20006028, 0xe00b9001, 0x1c409801, 0x493a9001, 0x42889801, 0xf000d304,
    0x2001f8bf, 0xbdf0b005, 0x69004834, 0x40082110, 0xd1ed2810, 0x4831e005, 0x21106940, 0x492f4308,
    0x482e6148, 0x21106900, 0x28104008, 0x1d3fd0f3, 0x1c761d2d, 0x42b008a0, 0x07a0d8d5, 0x28000f80,
    0x9700d030, 0xe0282600, 0x78009800, 0x20007028, 0xe00a9001, 0x1c409801, 0x49219001, 0x42889801,
    0xf000d303, 0x2001f88d, 0x481ce7cc, 0x21106900, 0x28104008, 0xe005d1ee, 0x69404818, 0x43082110,
    0x61484916, 0x69004815, 0x40082110, 0xd0f32810, 0x1c409800, 0x1c6d9000, 0x07a01c76, 0x42b00f80,
    0xbf00d8d2, 0x490d2000, 0x900160c8, 0x9801e00a, 0x90011c40, 0x9801490a, 0xd3034288, 0xf860f000,
    0xe79f2001, 0x69004805, 0x310121ff, 0x42884008, 0xf000d1ed, 0x2000f855, 0x0000e794, 0x40000800,
    0x00009c40, 0x4604b570, 0x4616460d, 0xff58f7ff, 0xbd702000, 0x4604b570, 0x4616460d, 0x46294632,
    0xf7ff4620, 0xbd70ff5b, 0x49034802, 0x48036088, 0x47706088, 0xffff0123, 0x4000cc00, 0xffff3210,
    0x4604b510, 0xfe9cf7ff, 0xbd102000, 0x4603b5f8, 0x2100460c, 0x20002600, 0x461e9000, 0xe0062500,
    0x6817ce01, 0xd00042b8, 0x1d12e004, 0x08a01c6d, 0xd8f542a8, 0x9600bf00, 0xe0082100, 0x78079800,
    0x90001c40, 0x42875c50, 0xe004d000, 0x07a01c49, 0x42880f80, 0xbf00d8f2, 0x18c000a8, 0xbdf81840,
    0x4804b510, 0x07c06800, 0x28000fc0, 0xf000d101, 0xbd10f803, 0x40010680, 0x4823b570, 0xb2846840,
    0x68004822, 0x4008210c, 0x48200886, 0x210f6800, 0x40080209, 0x2e000a05, 0x11a4d101, 0x2e01e008,
    0x12a4d101, 0x2e02e004, 0x1324d101, 0x13a4e000, 0xd0012d00, 0xd1022d0f, 0xff96f7ff, 0x07e8e022,
    0x28000fc0, 0x2c00d004, 0xf7ffd11c, 0xe019ff8d, 0x40282002, 0xd1042802, 0xd1132c01, 0xff84f7ff,
    0x2004e010, 0x28044028, 0x2c02d104, 0xf7ffd10a, 0xe007ff7b, 0x40282008, 0xd1032808, 0xd1012c03,
    0xff72f7ff, 0x0000bd70, 0x4000cc00, 0x40010680, 0x00000000
    ],

    # Relative function addresses
    'pc_init': 0x200002c9,
    'pc_unInit': 0x20000305,
    'pc_program_page': 0x200002d9,
    'pc_erase_sector': 0x20000039,
    'pc_eraseAll': 0x20000031,

    'static_base' : 0x20000000 + 0x00000004 + 0x00000410,
    'begin_stack' : 0x20000700,
    'begin_data' : 0x20000000 + 0x1000,
    'page_size' : 0x200,
    'analyzer_supported' : False,
    'analyzer_address' : 0x00000000,
    'page_buffers' : [0x20001000, 0x20001200],   # Enable double buffering
    'min_program_length' : 0x200,

    # Flash information
    'flash_start': 0x1000800,
    'flash_size': 0x400,
    'sector_sizes': (
        (0x0, 0x200),
    )
}


class HC32F155xA(CoreSightTarget):

    VENDOR = "HDSC"

    MEMORY_MAP = MemoryMap(
        FlashRegion( start=0x00000000, length=0x20000, page_size=0x200, sector_size=0x200,
                        is_boot_memory=True,
                        algo=FLASH_ALGO),
        FlashRegion( start=0x01000800, length=0x400, page_size=0x200, sector_size=0x200,
                        is_boot_memory=False,
                        is_default=False,
                        algo=FLASH_ALGO_NVR),
        RamRegion(   start=0x20000000, length=0x8000)
        )

    def __init__(self, session):
        super(HC32F155xA, self).__init__(session, self.MEMORY_MAP)
        self._svd_location = SVDFile.from_builtin("HC32F155.svd")

    def post_connect_hook(self):
        self.write32(DBGMCU.MCUSTPCTL, DBGMCU.MCUSTPCTL_VALUE)

class HC32F155xC(CoreSightTarget):

    VENDOR = "HDSC"

    MEMORY_MAP = MemoryMap(
        FlashRegion( start=0x00000000, length=0x40000, page_size=0x200, sector_size=0x200,
                        is_boot_memory=True,
                        algo=FLASH_ALGO),
        FlashRegion( start=0x01000800, length=0x400, page_size=0x200, sector_size=0x200,
                        is_boot_memory=False,
                        is_default=False,
                        algo=FLASH_ALGO_NVR),
        RamRegion(   start=0x20000000, length=0x8000)
        )

    def __init__(self, session):
        super(HC32F155xC, self).__init__(session, self.MEMORY_MAP)
        self._svd_location = SVDFile.from_builtin("HC32F155.svd")

    def post_connect_hook(self):
        self.write32(DBGMCU.MCUSTPCTL, DBGMCU.MCUSTPCTL_VALUE)
