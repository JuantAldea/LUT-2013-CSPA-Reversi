# -*- coding: utf-8 -*-

#################################
# Juan Antonio Aldea Armenteros #
# CSPA - LUT - 2013             #
#################################

from abc import ABCMeta, abstractmethod


class IGameClientInd:
    __metaclass__ = ABCMeta

    @abstractmethod
    def connection_ok_ind(self):
        return

    @abstractmethod
    def updated_board_ind(self, board):
        return

    @abstractmethod
    def winner_ind(self, winner):
        return

    @abstractmethod
    def turn_ind(self):
        return

    @abstractmethod
    def place_error_ind(self):
        return

    @abstractmethod
    def disconnection_ind(self):
        return
