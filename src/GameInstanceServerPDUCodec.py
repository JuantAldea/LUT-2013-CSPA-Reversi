# -*- coding: utf-8 -*-

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
