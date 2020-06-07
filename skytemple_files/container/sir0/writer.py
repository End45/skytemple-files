"""Converts Sir0 models back into the binary format used by the game"""
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

from skytemple_files.common.util import *
from skytemple_files.container.sir0 import HEADER_LEN
from skytemple_files.container.sir0.model import Sir0


class Sir0Writer:
    def __init__(self, model: Sir0):
        self.model = model
        self.data = None
        self.bytes_written = 0

    def write(self) -> bytes:
        # Correct all pointers in content by HEADER_LEN
        if not isinstance(self.model.content, bytearray):
            self.model.content = bytearray(self.model.content)
        for i, pnt_off in enumerate(self.model.content_pointer_offsets):
            self.model.content_pointer_offsets[i] = pnt_off + HEADER_LEN
            write_uintle(self.model.content, read_uintle(self.model.content, pnt_off, 4) + HEADER_LEN, pnt_off, 4)

        # Also add the two header pointers
        pointer_offsets = [4, 8] + self.model.content_pointer_offsets

        # Pointer offsets list
        pol = bytearray(4 * len(pointer_offsets))
        pol_cursor = self._encode_pointer_offsets(pol, pointer_offsets)
        pol = pol[:pol_cursor]

        len_content_padding = self._len_pad(len(self.model.content))
        len_eof_padding = self._len_pad(len(pol))

        pointer_pol = HEADER_LEN + len(self.model.content) + len_content_padding
        self.bytes_written = 0
        self.data = bytearray(pointer_pol + len(pol) + len_eof_padding)

        # Header
        self._append(b'SIR0')
        self._write_data(self.model.data_pointer + HEADER_LEN)
        self._write_data(pointer_pol)
        self._write_data(0)

        assert self.bytes_written == HEADER_LEN
        self._append(self.model.content)
        self._pad(len_content_padding)

        assert self.bytes_written == pointer_pol
        self._append(pol)
        self._pad(len_eof_padding)

        assert self.bytes_written == len(self.data)
        return self.data

    def _append(self, data: bytes):
        self.data[self.bytes_written:self.bytes_written+len(data)] = data
        self.bytes_written += len(data)

    def _pad(self, padding_length):
        self._append(bytes(0xAA for _ in range(0, padding_length)))

    def _len_pad(self, cur_len):
        if cur_len % 16 == 0:
            return 0
        return 16 - (cur_len % 16)

    def _write_data(self, val, length=4, signed=False):
        if signed:
            write_sintle(self.data, val, self.bytes_written, length)
        else:
            write_uintle(self.data, val, self.bytes_written, length)
        self.bytes_written += length

    # Based on C++ algorithm by psy_commando from
    # https://projectpokemon.org/docs/mystery-dungeon-nds/sir0siro-format-r46/
    def _encode_pointer_offsets(self, buffer: bytearray, pointer_offsets: List[int]):
        cursor = 0
        # used to add up the sum of all the offsets up to the current one
        offset_so_far = 0
        for offset in pointer_offsets:
            offset_to_encode = offset - offset_so_far
            # This tells the loop whether it needs to encode null bytes, if at least one higher byte was non-zero
            has_higher_non_zero = False
            # Set the value to the latest offset, so we can properly subtract it from the next offset.
            offset_so_far = offset

            # Encode every bytes of the 4 bytes integer we have to
            for i in range(4, 0, -1):
                currentbyte = (offset_to_encode >> (7 * (i - 1))) & 0x7F
                # the lowest byte to encode is special
                if i == 1:
                    # If its the last byte to append, leave the highest bit to 0 !
                    buffer[cursor] = currentbyte
                    cursor += 1
                elif currentbyte != 0 or has_higher_non_zero:
                    # if any bytes but the lowest one! If not null OR if we have encoded a higher non-null byte before!
                    buffer[cursor] = currentbyte | 0x80
                    cursor += 1
                    has_higher_non_zero = True

        return cursor + 1
