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

from skytemple_files.common.ppmdu_config.xml_reader import Pmd2XmlReader
from skytemple_files.common.util import get_ppmdu_config_for_rom
from skytemple_files.container.sir0.handler import Sir0Handler
from skytemple_files.list.actor.model import ActorListBin

if __name__ == '__main__':
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

    rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_eu_patched.nds'))

    bin_before = rom.getFileByName('BALANCE/actor_list.bin')
    # noinspection PyTypeChecker
    # - Bug in PyCharm with bound TypeVars
    actor_list_before: ActorListBin = Sir0Handler.unwrap_obj(
        Sir0Handler.deserialize(bin_before), ActorListBin
    )
    # This only works with unmodified ROMs!
    assert actor_list_before.list == Pmd2XmlReader.load_default('EoS_EU').script_data.level_entities

    bin_after = Sir0Handler.serialize(Sir0Handler.wrap_obj(actor_list_before))
    # noinspection PyTypeChecker
    actor_list_after: ActorListBin = Sir0Handler.unwrap_obj(
        Sir0Handler.deserialize(bin_after), ActorListBin
    )

    with open('/tmp/before.bin', 'wb') as f:
        f.write(bin_before)

    with open('/tmp/after.bin', 'wb') as f:
        f.write(bin_after)

    assert actor_list_before.list == actor_list_after.list

    for entry in actor_list_after.list:
        print(entry)
        entry.entid = 328

    bin_after = Sir0Handler.serialize(Sir0Handler.wrap_obj(actor_list_after))
    rom.setFileByName('BALANCE/actor_list.bin', bin_after)

    rom.saveToFile(os.path.join(base_dir, 'skyworkcopy_eu_patched_edit.nds'))

    # Test config patching
    config = get_ppmdu_config_for_rom(rom)
    for entry in config.script_data.level_entities:
        assert entry.entid == 328
