#  Copyright 2020 Parakoopa
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.

import os

from ndspy.rom import NintendoDSRom

from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import get_files_from_rom_with_extension, get_ppmdu_config_for_rom
from skytemple_files.graphics.fonts.graphic_font.handler import GraphicFontHandler
from skytemple_files.graphics.pal.handler import PalHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
out_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
os.makedirs(out_dir, exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us.nds'))
config = get_ppmdu_config_for_rom(rom)

for fn in ["FONT/staffont", "FONT/markfont"]:
    font = GraphicFontHandler.deserialize(rom.getFileByName(fn+".dat"))
    pal = PalHandler.deserialize(rom.getFileByName(fn+".pal"))
    font.set_palette(pal)
    for i in range(font.get_nb_entries()):
        e = font.get_entry(i)
        if e:
            e.save(os.path.join(out_dir, fn.replace('/', '_') + f'_{i:0>4}.png'))
    assert rom.getFileByName(fn+".dat") == GraphicFontHandler.serialize(font)