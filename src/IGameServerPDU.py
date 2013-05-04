# -*- coding: utf-8 -*-

#################################
# Juan Antonio Aldea Armenteros #
# CSPA - LUT - 2013             #
#################################

from abc import ABCMeta, abstractmethod


class IGameServerPDU():
    __metaclass__ = ABCMeta

    @abstractmethod
    def connect_pdu():
        return

    @abstractmethod
    def decode(data):
        return
