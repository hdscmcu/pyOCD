# pyOCD debugger
# Copyright (c) 2022 Huada Semiconductor Corporation
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
    STPCTL = 0xE0042020
    STPCTL_VALUE = 0x03


FLASH_ALGO = { 'load_address' : 0x20000000,
               'instructions' : [
    0xE00ABE00, 
    0x4770ba40, 0x4770ba40, 0x4770bac0, 0x4770bac0, 0x0030ea4f, 0x00004770, 0x0030ea4f, 0xb5704770,
    0x460d4604, 0xf0004616, 0x2000f845, 0xb510bd70, 0xf0004604, 0x2000f847, 0xb510bd10, 0xf89ff000,
    0xb510bd10, 0x46204604, 0xf8c9f000, 0xb570bd10, 0x460d4604, 0x46324616, 0x46204629, 0xf83af000,
    0xb5f0bd70, 0x460d4604, 0x26002300, 0x46262700, 0xe0072100, 0xcb04f856, 0x45846810, 0xe004d000,
    0x1c491d12, 0x0f95ebb1, 0xbf00d3f4, 0x23004637, 0xf817e006, 0x5cd0cb01, 0xd0004584, 0x1c5be004,
    0x0003f005, 0xd8f44298, 0xeb04bf00, 0x44180081, 0x0000bdf0, 0x1023f240, 0x60084961, 0x2010f243,
    0x47706008, 0x495e2000, 0x6008310c, 0x495c1e40, 0x47706008, 0x4603b578, 0x90002000, 0x20014615,
    0x360c4e57, 0x46306030, 0xf4406800, 0x60307098, 0xbf00461c, 0x60206828, 0x90002000, 0x9800e009,
    0x90001c40, 0x4640f649, 0x42b09800, 0x2001d301, 0x484bbd78, 0x68003010, 0x0010f000, 0xd1ee2810,
    0x4847e007, 0x68003014, 0x0010f040, 0x36144e44, 0x48436030, 0x68003010, 0x0010f000, 0xd0f02810,
    0x1d241d2d, 0x29041f09, 0x2000d2d4, 0x360c4e3c, 0x90006030, 0x9800e009, 0x90001c40, 0x4640f649,
    0x42b09800, 0x2001d301, 0x4835e7d2, 0x68003010, 0x7080f400, 0x7f80f5b0, 0x2000d1ed, 0x2100e7c8,
    0x4a2f2001, 0x6010320c, 0x68004610, 0x70a8f440, 0x20006010, 0xe0056000, 0x482a1c49, 0xd3014281,
    0x47702001, 0x30104826, 0xf4006800, 0xf5b07080, 0xd1f17f80, 0x4822e007, 0x68003014, 0x0010f040,
    0x32144a1f, 0x481e6010, 0x68003010, 0x0010f000, 0xd1f02800, 0x320c4a1a, 0xbf006010, 0x4601e7e1,
    0x20012200, 0x330c4b16, 0x46186018, 0xf4406800, 0x601870a0, 0x60082000, 0x1c52e005, 0x42824811,
    0x2001d301, 0x480e4770, 0x68003010, 0x7080f400, 0x7f80f5b0, 0xe007d1f1, 0x30144809, 0xf0406800,
    0x4b070010, 0x60183314, 0x30104805, 0xf0006800, 0x28000010, 0x4b02d1f0, 0x6018330c, 0xe7e1bf00,
    0x40010400, 0x00061a80, 0x00000000
    ],

    # Relative function addresses
    'pc_init': 0x20000023,
    'pc_unInit': 0x20000033,
    'pc_program_page': 0x20000053,
    'pc_erase_sector': 0x20000047,
    'pc_eraseAll': 0x2000003f,

    'static_base' : 0x20000000 + 0x00000004 + 0x00000248,
    'begin_stack' : 0x20000500,
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


class HC32M424xC(CoreSightTarget):

    VENDOR = "HDSC"

    MEMORY_MAP = MemoryMap(
        FlashRegion( start=0x00000000, length=0x40000, page_size=0x200, sector_size=0x200,
                        is_boot_memory=True,
                        algo=FLASH_ALGO),
        RamRegion(   start=0x1FFFC000, length=0x8000)
        )

    def __init__(self, session):
        super(HC32M424xC, self).__init__(session, self.MEMORY_MAP)
        self._svd_location = SVDFile.from_builtin("HC32M424.svd")

    def post_connect_hook(self):
        self.write32(DBGMCU.STPCTL, DBGMCU.STPCTL_VALUE)

