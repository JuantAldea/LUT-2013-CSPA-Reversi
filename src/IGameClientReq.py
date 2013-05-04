# -*- coding: utf-8 -*-

#################################
# Juan Antonio Aldea Armenteros #
# CSPA - LUT - 2013             #
#################################

from abc import ABCMeta, abstractmethod


class IGameClientReq:
    __metaclass__ = ABCMeta

    @abstractmethod
    def connect_req(self, ip, port):
        return

    @abstractmethod
    def place_req(self, x, y):
        return

    @abstractmethod
    def disconnect_req(self):
        return

    @abstractmethod
    def shutdown_req(self):
        return
