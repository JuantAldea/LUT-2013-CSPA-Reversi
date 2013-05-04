# -*- coding: utf-8 -*-

#################################
# Juan Antonio Aldea Armenteros #
# CSPA - LUT - 2013             #
#################################


class PDUCodes(object):
    # -1          0               1                2        3      4        5              6        7
    ERROR, CLIENT_CONNECT, CLIENT_CONNECT_OK, CLIENT_QUIT, TURN, PLACE, PLACE_ERROR, UPDATE_BOARD, WINNER = range(-1, 8)
