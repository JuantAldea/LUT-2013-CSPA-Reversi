# pyReversi is a multiplayer reversi game with dedicated server
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
