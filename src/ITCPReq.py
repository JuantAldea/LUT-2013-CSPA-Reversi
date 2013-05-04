# -*- coding: utf-8 -*-

#################################
# Juan Antonio Aldea Armenteros #
# CSPA - LUT - 2013             #
#################################

from abc import ABCMeta, abstractmethod


class ITCPReq:
    __metaclass__ = ABCMeta

    @abstractmethod
    def send_req(self, client, data):
        return

    @abstractmethod
    def disconnect_req(self, client):
        return

    @abstractmethod
    def shutdown_req(self):
        return
