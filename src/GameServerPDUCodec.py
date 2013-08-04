# Reversi is a multiplayer reversi game with dedicated server
# Copyright (C) 2012-2013, Juan Antonio Aldea Armenteros
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf8 -*-

#################################
# Juan Antonio Aldea Armenteros #
# CSPA - LUT - 2013             #
#################################

import struct
from IGameServerPDU import IGameServerPDU
from PDUCodes import PDUCodes


class GameServerPDUCodec(IGameServerPDU):

    @staticmethod
    def connect_pdu():
        msg_type = struct.pack("<h", PDUCodes.CLIENT_CONNECT)
        msg_magic_number = struct.pack("<h", 1234)
        msg_size = struct.pack("<h", len(msg_type) + len(msg_magic_number) + 2)
        return msg_size + msg_type + msg_magic_number

    @staticmethod
    def decode(data):
        offset = 0
        msg_size, = struct.unpack("<h", data[offset:offset + 2])
        if len(data) >= msg_size:
            offset += 2
            msg_type, = struct.unpack("<h", data[offset:offset + 2])
            if msg_type == PDUCodes.CLIENT_CONNECT:
                offset += 2
                msg_magic_number, = struct.unpack("<h", data[offset:offset + 2])
                if msg_magic_number == 1234:
                    return (PDUCodes.CLIENT_CONNECT, msg_size, [])

        return (PDUCodes.ERROR, -1, [])
