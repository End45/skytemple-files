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
from skytemple_files.script.ssa_sse_sss.position import SsaPosition


class SsaObject:
    def __init__(self, object_id, unk4, unk6, pos: SsaPosition, script_id, unk12):
        self.object_id = object_id
        self.unk4 = unk4
        self.unk6 = unk6
        self.pos = pos
        self.script_id = script_id
        self.unk12 = unk12

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return f"SsaObject<{str({k: v for k, v in self.__dict__.items() if v is not None})}>"
