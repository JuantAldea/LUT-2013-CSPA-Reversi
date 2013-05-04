# -*- coding: utf-8 -*-

#################################
# Juan Antonio Aldea Armenteros #
# CSPA - LUT - 2013             #
#################################

from abc import ABCMeta, abstractmethod


class ITCPInd:
    __metaclass__ = ABCMeta

    @abstractmethod
    def recv_ind(self, client, data):
        return

    @abstractmethod
    def disconnection_ind(self, client):
        return
