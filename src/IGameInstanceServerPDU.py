# -*- coding: utf-8 -*-

#################################
# Juan Antonio Aldea Armenteros #
# CSPA - LUT - 2013             #
#################################

from abc import ABCMeta, abstractmethod


class IGameInstanceServerPDU:
    __metaclass__ = ABCMeta

    @abstractmethod
    def disconnect_pdu(self):
        return

    @abstractmethod
    def place_pdu(self, x, y):
        return
