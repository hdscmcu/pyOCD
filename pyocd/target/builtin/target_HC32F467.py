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
    STCTL = 0xE0042020
    STCTL_VALUE = 0x7FFFFF

    STCTL1 = 0xE0042028
    STCTL1_VALUE = 0xFFF

    TRACECTL = 0xE0042024
    TRACECTL_VALUE = 0x0

FLASH_ALGO = {
    'load_address' : 0x20000000,

    # Flash algorithm as a hex string. HDSC.HC32F467.1.0.1.pack 10515
    'instructions': [
    0xE00ABE00,
    0x4770ba40, 0x4770ba40, 0x4770ba40, 0x4770bac0, 0x4770bac0, 0x4770bac0, 0x0030ea4f, 0x00004770,
    0x0030ea4f, 0x00004770, 0x0030ea4f, 0x00004770, 0x49062000, 0x49057008, 0xf8813936, 0x49040026,
    0x20016008, 0x390c4901, 0x47707008, 0x40054036, 0x40010418, 0x49102000, 0x48107008, 0xf0006800,
    0xb1200001, 0x490c480e, 0x600831ca, 0x480de003, 0x31ca4909, 0x20056008, 0x6008490b, 0x4906480b,
    0x62083936, 0x49042000, 0x7008390c, 0x49022005, 0xf8813936, 0x47700026, 0x40054036, 0x40010684,
    0x22205981, 0x22204781, 0x40010418, 0x00116310, 0xf000b510, 0xbd10f84d, 0x4604b510, 0xf0004620,
    0xbd10f8bb, 0x491b2000, 0x1d096008, 0x1d096008, 0x1d096008, 0x1d096008, 0x1d096008, 0x1d096008,
    0x1d096008, 0xf44f6008, 0x49133040, 0x20006008, 0x60081f09, 0x391c4910, 0x20016008, 0x7008490f,
    0x490e480f, 0xf8c13926, 0x20000100, 0x20016208, 0x1d09490a, 0x480b7008, 0x6008490b, 0x604812c0,
    0x6108480a, 0x4025f44f, 0x39264904, 0x03fef8a1, 0x00004770, 0x40010590, 0x4001041c, 0x40054026,
    0x11101300, 0xfffffa0e, 0x40048000, 0xa5a50000, 0xf000b570, 0xf44ff9ed, 0x49337083, 0x25006008,
    0x4410f44f, 0x60202000, 0x1c6de007, 0x4285482f, 0xf000d303, 0x2001f9dd, 0x482bbd70, 0x68001d00,
    0x7080f400, 0x7f80f5b0, 0x4827d007, 0x68001d00, 0x7080f000, 0x7f80f1b0, 0xe007d1e7, 0x30084822,
    0xf0406800, 0x49201010, 0x60083108, 0x1d00481e, 0xf0006800, 0x28001010, 0x2004d1f0, 0x6008491a,
    0x20004c1b, 0xf0006020, 0xe007f9b3, 0x30084816, 0xf0406800, 0x49141010, 0x60083108, 0x1d004812,
    0xf0006800, 0x28001010, 0x2004d1f0, 0x6008490e, 0x20004c10, 0xf0006020, 0xe007f99b, 0x3008480a,
    0xf0406800, 0x49081010, 0x60083108, 0x1d004806, 0xf0006800, 0x28001010, 0x4903d1f0, 0xf0006008,
    0x2000f987, 0x0000e7a8, 0x4001041c, 0x00061a80, 0x03002000, 0x03004000, 0x4604b570, 0xf978f000,
    0x20042500, 0x6008491a, 0x60202000, 0x1c6de009, 0x42854818, 0xf000d305, 0xf7fff96b, 0x2001ff33,
    0x4813bd70, 0x68001d00, 0x7080f400, 0x7f80f5b0, 0x480fd007, 0x68001d00, 0x7080f000, 0x7f80f1b0,
    0xe007d1e5, 0x3008480a, 0xf0406800, 0x49081010, 0x60083108, 0x1d004806, 0xf0006800, 0x28001010,
    0x4903d1f0, 0xf0006008, 0x2000f943, 0x0000e7d8, 0x4001041c, 0x00061a80, 0xf000b510, 0xf240f939,
    0x49161023, 0xf2436008, 0x60082010, 0x30fff04f, 0x60084913, 0x60081d09, 0x60081d09, 0x60081d09,
    0x60081d09, 0x60081d09, 0x60081d09, 0x60081d09, 0x490a480c, 0x60081d09, 0x600843c0, 0x4907480a,
    0x60083118, 0x1d0912c0, 0xf24a6008, 0x49075001, 0xf7ff8008, 0xf000fe9f, 0xbd10f90b, 0x40010400,
    0x40010590, 0x01234567, 0x00080005, 0x400543fe, 0x43f8e92d, 0x460c4606, 0xf0004617, 0xf649f8f9,
    0x90004040, 0xf24046b8, 0x494a1003, 0x46356008, 0x4040f649, 0xbf009000, 0xf8eaf000, 0x0000f8d8,
    0xf5b56028, 0xd22e1f80, 0x68004843, 0x42884943, 0x2000d029, 0xe00e9000, 0x1c409800, 0xf6499000,
    0x98004140, 0xd3064288, 0xf8d2f000, 0xfe9af7ff, 0xe8bd2001, 0x483783f8, 0x68001d00, 0x0010f000,
    0xd1e92810, 0x4833e007, 0x68003008, 0x0010f040, 0x31084930, 0x482f6008, 0x68001d00, 0x0010f000,
    0xd0f02810, 0x2000e029, 0xe00d9000, 0x1c409800, 0xf6499000, 0x98004140, 0xd3054288, 0xf8a8f000,
    0xfe70f7ff, 0xe7d42001, 0x1d004822, 0xf4006800, 0xf5b01080, 0xd1e91f80, 0x481ee007, 0x68003008,
    0x1080f440, 0x3108491b, 0x481a6008, 0x68001d00, 0x1080f400, 0x1f80f5b0, 0xf108d0ef, 0x1d2d0804,
    0x2c041f24, 0x2000d298, 0x60084912, 0xe00d9000, 0x1c409800, 0xf6499000, 0x98004140, 0xd3054288,
    0xf876f000, 0xfe3ef7ff, 0xe7a22001, 0x1d004809, 0xf4006800, 0xf5b07080, 0xd0077f80, 0x1d004805,
    0xf0006800, 0xf1b07080, 0xd1e17f80, 0xf860f000, 0xe78e2000, 0x4001041c, 0x03002000, 0x005a5a5a,
    0x4604b570, 0x4616460d, 0xff16f7ff, 0xbd702000, 0x4604b570, 0x4616460d, 0x46294632, 0xf7ff4620,
    0xbd70ff47, 0x49034802, 0x48036008, 0x47706008, 0xffff0123, 0x40049408, 0xffff3210, 0x4604b510,
    0xfe00f7ff, 0xbd102000, 0x4604b5f0, 0x2300460d, 0x27002600, 0x21004626, 0xf856e007, 0x6810cb04,
    0xd0004584, 0x1d12e004, 0xebb11c49, 0xd3f40f95, 0x4637bf00, 0xe0062300, 0xcb01f817, 0x45845cd0,
    0xe004d000, 0xf0051c5b, 0x42980003, 0xbf00d8f4, 0x0081eb04, 0xbdf04418, 0x49034802, 0x48036088,
    0x47706088, 0xffff0123, 0x40049000, 0xffff3210, 0x4807b510, 0xf4006800, 0xb9083080, 0xf854f000,
    0x68004803, 0x0001f000, 0xf000b908, 0xbd10f809, 0x40010680, 0x1e01bf00, 0x0001f1a0, 0x4770d1fb,
    0x481fb570, 0xb2846800, 0x6800481e, 0x0681f3c0, 0x6800481c, 0x2503f3c0, 0x11a4b90e, 0x2e01e008,
    0x12a4d101, 0x2e02e004, 0x1324d101, 0x13a4e000, 0x2d0fb10d, 0xf7ffd102, 0xe020ff85, 0x0001f005,
    0xb9e4b118, 0xff7ef7ff, 0xf005e019, 0x28020002, 0x2c01d104, 0xf7ffd113, 0xe010ff75, 0x0004f005,
    0xd1042804, 0xd10a2c02, 0xff6cf7ff, 0xf005e007, 0x28080008, 0x2c03d103, 0xf7ffd101, 0xbd70ff63,
    0x40049404, 0x40010680, 0x4823b570, 0xb2846840, 0x68004822, 0x4681f3c0, 0x68004820, 0x6503f3c0,
    0x11a4b90e, 0x2e01e008, 0x12a4d101, 0x2e02e004, 0x1324d101, 0x13a4e000, 0x2001b90d, 0x2000e000,
    0xd1012d0f, 0xe0002101, 0x43082100, 0xf7ffb110, 0xe020ff73, 0x0001f005, 0xb9e4b118, 0xff6cf7ff,
    0xf005e019, 0x28020002, 0x2c01d104, 0xf7ffd113, 0xe010ff63, 0x0004f005, 0xd1042804, 0xd10a2c02,
    0xff5af7ff, 0xf005e007, 0x28080008, 0x2c03d103, 0xf7ffd101, 0xbd70ff51, 0x40049000, 0x40010680,
    0x00000000
    ],

    # Relative function addresses
    'pc_init': 0x20000485,
    'pc_unInit': 0x200004c1,
    'pc_program_page': 0x20000495,
    'pc_erase_sector': 0x200000bd,
    'pc_eraseAll': 0x200000b5,

    'static_base' : 0x20000000 + 0x00000004 + 0x00000680,
    'begin_stack' : 0x20000900,
    'begin_data' : 0x20000000 + 0x1000,
    'page_size' : 0x400,
    'analyzer_supported' : False,
    'analyzer_address' : 0x00000000,
    'page_buffers' : [0x20001000, 0x20001400],   # Enable double buffering
    'min_program_length' : 0x400,

    # Flash information
    'flash_start': 0x0,
    'flash_size': 0x100000,
    'sector_sizes': (
        (0x0, 0x2000),
    )
}


FLASH_ALGO_OTP = {
    'load_address' : 0x20000000,

    # Flash algorithm as a hex string. HDSC.HC32F467.1.0.1.pack 10515
    'instructions': [
    0xE00ABE00,
    0x4770ba40, 0x4770ba40, 0x4770ba40, 0x4770bac0, 0x4770bac0, 0x4770bac0, 0x0030ea4f, 0x00004770,
    0x0030ea4f, 0x00004770, 0x0030ea4f, 0x00004770, 0x49062000, 0x49057008, 0xf8813936, 0x49040026,
    0x20016008, 0x390c4901, 0x47707008, 0x40054036, 0x40010418, 0x49102000, 0x48107008, 0xf0006800,
    0xb1200001, 0x490c480e, 0x600831ca, 0x480de003, 0x31ca4909, 0x20056008, 0x6008490b, 0x4906480b,
    0x62083936, 0x49042000, 0x7008390c, 0x49022005, 0xf8813936, 0x47700026, 0x40054036, 0x40010684,
    0x22205981, 0x22204781, 0x40010418, 0x00116310, 0xf000b510, 0xbd10f84d, 0x4604b510, 0xf0004620,
    0xbd10f84e, 0x491b2000, 0x1d096008, 0x1d096008, 0x1d096008, 0x1d096008, 0x1d096008, 0x1d096008,
    0x1d096008, 0xf44f6008, 0x49133040, 0x20006008, 0x60081f09, 0x391c4910, 0x20016008, 0x7008490f,
    0x490e480f, 0xf8c13926, 0x20000100, 0x20016208, 0x1d09490a, 0x480b7008, 0x6008490b, 0x604812c0,
    0x6108480a, 0x4025f44f, 0x39264904, 0x03fef8a1, 0x00004770, 0x40010590, 0x4001041c, 0x40054026,
    0x11101300, 0xfffffa0e, 0x40048000, 0xa5a50000, 0xf000b510, 0xf000f913, 0x2000f911, 0xb510bd10,
    0xf0004604, 0xf000f90b, 0x2000f909, 0x0000bd10, 0xf000b510, 0xf240f903, 0x49161023, 0xf2436008,
    0x60082010, 0x30fff04f, 0x60084913, 0x60081d09, 0x60081d09, 0x60081d09, 0x60081d09, 0x60081d09,
    0x60081d09, 0x60081d09, 0x490a480c, 0x60081d09, 0x600843c0, 0x4907480a, 0x60083118, 0x1d0912c0,
    0xf24a6008, 0x49075001, 0xf7ff8008, 0xf000ff43, 0xbd10f8d5, 0x40010400, 0x40010590, 0x01234567,
    0x00080005, 0x400543fe, 0x43f8e92d, 0x460c4605, 0xf0004616, 0xf649f8c3, 0x90004040, 0xf24046b0,
    0x49311003, 0x462f6008, 0x4040f649, 0xbf009000, 0xf8b4f000, 0x0000f8d8, 0x20006038, 0xe00e9000,
    0x1c409800, 0xf6499000, 0x98004140, 0xd3064288, 0xf8a4f000, 0xff46f7ff, 0xe8bd2001, 0x482283f8,
    0x68001d00, 0x0010f000, 0xd1e92810, 0x481ee007, 0x68003008, 0x0010f040, 0x3108491b, 0x481a6008,
    0x68001d00, 0x0010f000, 0xd0f02810, 0x0804f108, 0x1f241d3f, 0xd2cb2c04, 0x49132000, 0x90006008,
    0x9800e00d, 0x90001c40, 0x4140f649, 0x42889800, 0xf000d305, 0xf7fff873, 0x2001ff15, 0x480ae7cd,
    0x68001d00, 0x7080f400, 0x7f80f5b0, 0x4806d007, 0x68001d00, 0x7080f000, 0x7f80f1b0, 0xf000d1e1,
    0x2000f85d, 0x0000e7b9, 0x4001041c, 0x4604b570, 0x4616460d, 0xff4cf7ff, 0xbd702000, 0x4604b570,
    0x4616460d, 0x46294632, 0xf7ff4620, 0xbd70ff7d, 0x49034802, 0x48036008, 0x47706008, 0xffff0123,
    0x40049408, 0xffff3210, 0x4604b510, 0xfedaf7ff, 0xbd102000, 0x4604b5f0, 0x2300460d, 0x27002600,
    0x21004626, 0xf856e007, 0x6810cb04, 0xd0004584, 0x1d12e004, 0xebb11c49, 0xd3f40f95, 0x4637bf00,
    0xe0062300, 0xcb01f817, 0x45845cd0, 0xe004d000, 0xf0051c5b, 0x42980003, 0xbf00d8f4, 0x0081eb04,
    0xbdf04418, 0x49034802, 0x48036088, 0x47706088, 0xffff0123, 0x40049000, 0xffff3210, 0x4807b510,
    0xf4006800, 0xb9083080, 0xf854f000, 0x68004803, 0x0001f000, 0xf000b908, 0xbd10f809, 0x40010680,
    0x1e01bf00, 0x0001f1a0, 0x4770d1fb, 0x481fb570, 0xb2846800, 0x6800481e, 0x0681f3c0, 0x6800481c,
    0x2503f3c0, 0x11a4b90e, 0x2e01e008, 0x12a4d101, 0x2e02e004, 0x1324d101, 0x13a4e000, 0x2d0fb10d,
    0xf7ffd102, 0xe020ff85, 0x0001f005, 0xb9e4b118, 0xff7ef7ff, 0xf005e019, 0x28020002, 0x2c01d104,
    0xf7ffd113, 0xe010ff75, 0x0004f005, 0xd1042804, 0xd10a2c02, 0xff6cf7ff, 0xf005e007, 0x28080008,
    0x2c03d103, 0xf7ffd101, 0xbd70ff63, 0x40049404, 0x40010680, 0x4823b570, 0xb2846840, 0x68004822,
    0x4681f3c0, 0x68004820, 0x6503f3c0, 0x11a4b90e, 0x2e01e008, 0x12a4d101, 0x2e02e004, 0x1324d101,
    0x13a4e000, 0x2001b90d, 0x2000e000, 0xd1012d0f, 0xe0002101, 0x43082100, 0xf7ffb110, 0xe020ff73,
    0x0001f005, 0xb9e4b118, 0xff6cf7ff, 0xf005e019, 0x28020002, 0x2c01d104, 0xf7ffd113, 0xe010ff63,
    0x0004f005, 0xd1042804, 0xd10a2c02, 0xff5af7ff, 0xf005e007, 0x28080008, 0x2c03d103, 0xf7ffd101,
    0xbd70ff51, 0x40049000, 0x40010680, 0x00000000
    ],

    # Relative function addresses
    'pc_init': 0x200002d1,
    'pc_unInit': 0x2000030d,
    'pc_program_page': 0x200002e1,
    'pc_erase_sector': 0x200000bd,
    'pc_eraseAll': 0x200000b5,

    'static_base' : 0x20000000 + 0x00000004 + 0x000004cc,
    'begin_stack' : 0x20000700,
    'begin_data' : 0x20000000 + 0x1000,
    'page_size' : 0x1800,
    'analyzer_supported' : False,
    'analyzer_address' : 0x00000000,
    'page_buffers' : [0x20001000, 0x20002800],   # Enable double buffering
    'min_program_length' : 0x1800,

    # Flash information
    'flash_start': 0x3000000,
    'flash_size': 0x1800,
    'sector_sizes': (
        (0x0, 0x1800),
    )
}


class HC32F467xG(CoreSightTarget):

    VENDOR = "HDSC"

    MEMORY_MAP = MemoryMap(
        FlashRegion( start=0x00000000, length=0x100000, page_size=0x400, sector_size=0x2000,
                        is_boot_memory=True,
                        algo=FLASH_ALGO),
        FlashRegion( start=0x3000000, length=0x1800, page_size=0x1800, sector_size=0x1800,
                        is_boot_memory=False,
                        is_default=False,
                        algo=FLASH_ALGO_OTP),
        RamRegion(   start=0x1FFFE000, length=0x80000),
        RamRegion(   start=0x200F0000, length=0x1000)
        )

    def __init__(self, session):
        super(HC32F467xG, self).__init__(session, self.MEMORY_MAP)
        self._svd_location = SVDFile.from_builtin("HC32F467.svd")

    def post_connect_hook(self):
        self.write32(DBGMCU.STCTL, DBGMCU.STCTL_VALUE)
        self.write32(DBGMCU.STCTL1, DBGMCU.STCTL1_VALUE)
        self.write32(DBGMCU.TRACECTL, DBGMCU.TRACECTL_VALUE)

