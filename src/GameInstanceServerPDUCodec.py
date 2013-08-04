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
from IGameInstanceServerPDU import IGameInstanceServerPDU
from PDUCodes import PDUCodes


class GameInstanceServerPDUCodec(IGameInstanceServerPDU):

    @staticmethod
    def disconnect_pdu():
        msg_type = struct.pack("<h", PDUCodes.CLIENT_QUIT)
        msg_size = struct.pack("<h", len(msg_type) + 2)
        return msg_size + msg_type

    @staticmethod
    def place_pdu(x, y):
        msg_type = struct.pack("<h", PDUCodes.PLACE)
        msg_x = struct.pack("<h", x)
        msg_y = struct.pack("<h", y)
        msg_size = struct.pack("<h", len(msg_type) + len(msg_x) + len(msg_y) + 2)
        return msg_size + msg_type + msg_x + msg_y

    @staticmethod
    def decode(data):
        offset = 0
        msg_size, = struct.unpack("<h", data[offset:offset + 2])
        if len(data) >= msg_size:
            offset += 2
            msg_type, = struct.unpack("<h", data[offset:offset + 2])
            offset += 2
            if msg_type == PDUCodes.CLIENT_QUIT:
                return (PDUCodes.CLIENT_QUIT, msg_size, [])
            elif msg_type == PDUCodes.PLACE:
                x, = struct.unpack("<h", data[offset:offset + 2])
                offset += 2
                y, = struct.unpack("<h", data[offset:offset + 2])
                return (PDUCodes.PLACE, msg_size, [x, y])

        return (PDUCodes.ERROR, -1, [])
