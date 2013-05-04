# -*- coding: utf-8 -*-

#################################
# Juan Antonio Aldea Armenteros #
# CSPA - LUT - 2013             #
#################################

from abc import ABCMeta, abstractmethod


class IGameClientPDU:
    __metaclass__ = ABCMeta

    @abstractmethod
    def connect_ok_pdu():
        return

    @abstractmethod
    def turn_pdu():
        return

    @abstractmethod
    def update_board_pdu(player, changed_positions):
        return

    @abstractmethod
    def place_error_pdu():
        return

    @abstractmethod
    def winner_pdu(color):
        return

    @abstractmethod
    def error_pdu():
        return
