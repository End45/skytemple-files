import os

from bitstring import BitStream
from ndspy.rom import NintendoDSRom

from skytemple_files.unique.bg_list_dat.handler import BgListDatHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

bin = BitStream(rom.getFileByName('MAP_BG/bg_list.dat'))
bg_list = BgListDatHandler.deserialize(bin)

for i, l in enumerate(bg_list.level):
    print(f"{i}: {l}")
