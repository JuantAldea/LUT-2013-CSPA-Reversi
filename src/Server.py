#!/usr/bin/python2.7
# -*- coding: utf8 -*-

#################################
# Juan Antonio Aldea Armenteros #
# CSPA - LUT - 2013             #
#################################

from GameServer import GameServer
from GameServerTCP import GameServerTCP

if __name__ == '__main__':
    tcp_server = GameServerTCP(27015)
    game_server = GameServer(tcp_server)
    tcp_server.set_indication(game_server)
    game_server.run()
