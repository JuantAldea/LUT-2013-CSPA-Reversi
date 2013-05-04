# -*- coding: utf-8 -*-

#################################
# Juan Antonio Aldea Armenteros #
# CSPA - LUT - 2013             #
#################################

import struct
from PDUCodes import PDUCodes
from IGameClientPDU import IGameClientPDU


class GameClientPDUCodec(IGameClientPDU):

    @staticmethod
    def connect_ok_pdu(player_color):
        msg_type = struct.pack("<h", PDUCodes.CLIENT_CONNECT_OK)
        msg_payload = struct.pack("<h", player_color)
        msg_size = struct.pack("<h", 2 + len(msg_type) + len(msg_payload))
        return msg_size + msg_type + msg_payload

    @staticmethod
    def turn_pdu():
        msg_type = struct.pack("<h", PDUCodes.TURN)
        msg_size = struct.pack("<h", 2 + len(msg_type))
        return msg_size + msg_type

    @staticmethod
    def update_board_pdu(player, changed_positions):
        msg_type = struct.pack("<h", PDUCodes.UPDATE_BOARD)
        msg_player = struct.pack("<h", player)
        changed_positions_flatten = [coordinate for coordinates in changed_positions for coordinate in coordinates]
        msg_payload = struct.pack("<" + "h" * len(changed_positions_flatten), *changed_positions_flatten)
        msg_size = struct.pack("<h", 2 + len(msg_type) + len(msg_player) + len(msg_payload))
        return msg_size + msg_type + msg_player + msg_payload

    @staticmethod
    def place_error_pdu():
        msg_type = struct.pack("<h", PDUCodes.PLACE_ERROR)
        msg_size = struct.pack("<h", 2 + len(msg_type))
        return msg_size + msg_type

    @staticmethod
    def winner_pdu(winner):
        msg_type = struct.pack("<h", PDUCodes.WINNER)
        msg_payload = struct.pack("<h", winner)
        msg_size = struct.pack("<h", 2 + len(msg_type) + len(msg_payload))
        return msg_size + msg_type + msg_payload

    @staticmethod
    def error_pdu():
        msg_type = struct.pack("<h", PDUCodes.ERROR)
        msg_size = struct.pack("<h", 2 + len(msg_type))
        return msg_size + msg_type

    @staticmethod
    def decode(data):
        print "DECODING"
        offset = 0
        msg_size, = struct.unpack("<h", data[offset:offset + 2])
        print "offset, msg_size", offset, msg_size
        offset += 2
        if len(data) >= msg_size:
            msg_type, = struct.unpack("<h", data[offset:offset + 2])
            print "offset, msg_type", offset, msg_type
            offset += 2
            if msg_type == PDUCodes.CLIENT_CONNECT_OK:
                msg_payload, = struct.unpack("<h", data[offset:offset + 2])
                return (msg_type, msg_size, [msg_payload])
            elif msg_type == PDUCodes.TURN:
                return (msg_type, msg_size, [])
            elif msg_type == PDUCodes.UPDATE_BOARD:
                msg_player, = struct.unpack("<h", data[offset:offset + 2])
                offset += 2
                msg_board = struct.unpack("<" + "h" * ((msg_size - offset) / 2), data[offset:msg_size])
                msg_board = list(msg_board)
                number_of_coordinate_pairs = len(msg_board) / 2
                msg_board = [msg_board[2 * i: 2 * i + 2] for i in range(number_of_coordinate_pairs)]
                return (msg_type, msg_size, [msg_player, msg_board])
            elif msg_type == PDUCodes.PLACE_ERROR:
                return (msg_type, msg_size, [])
            elif msg_type == PDUCodes.WINNER:
                msg_payload, = struct.unpack("<h", data[offset:offset + 2])
                return (msg_type, msg_size, [msg_payload])

        return (PDUCodes.ERROR, -1, [])
