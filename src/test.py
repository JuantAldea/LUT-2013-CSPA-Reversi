#!/usr/bin/python2.7

# Reversi is a multiplayer reversi game with dedicated server
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

import select
import sys
from socket import *

from GameServerPDUCodec import *
from GameInstancePDUCodec import *
from GameClientPDUCodec import *
from socket import *
from struct import *

s = socket(AF_INET, SOCK_STREAM)
s.connect(('127.0.0.1', 27015))
clients = [s, sys.stdin]
while True:
    input_ready, output_ready, except_ready = select.select(clients, [], [], 5)
    for fd in input_ready:
        if fd == s:
            data = s.recv(4096, MSG_PEEK)
            if len(data) == 0:
                exit(0)
            else:
                decoded = GameClientPDUCodec.decode(data)
                if decoded[0] != -1:
                    s.recv(decoded[1])
                    print decoded
                else:
                    print data
        else:
            line = sys.stdin.readline()
            if line[0] == 'c':
                s.send(GameServerPDUCodec.connect_pdu())
            if line[0] == 'p':
                place_pdu = GameInstancePDUCodec.place_pdu(3, 1)
                s.send(place_pdu)
                print GameInstancePDUCodec.decode(place_pdu)
            elif line[0] == 'o':
                place_pdu = GameInstancePDUCodec.place_pdu(6, 1)
                s.send(place_pdu)
                print GameInstancePDUCodec.decode(place_pdu)
            elif line[0] == 'i':
                place_pdu = GameInstancePDUCodec.place_pdu(3, 2)
                s.send(place_pdu)
                print GameInstancePDUCodec.decode(place_pdu)
            elif line[0] == 'u':
                place_pdu = GameInstancePDUCodec.place_pdu(4, 2)
                s.send(place_pdu)
                print GameInstancePDUCodec.decode(place_pdu)
