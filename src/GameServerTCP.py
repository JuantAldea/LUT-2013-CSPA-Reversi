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

#################################
# Juan Antonio Aldea Armenteros #
# CSPA - LUT - 2013             #
#################################

import signal
import select
import socket
from ITCPReq import ITCPReq


class GameServerTCP(ITCPReq):
    def __init__(self, port):
        self.game_server = None
        self.port = port
        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listening_socket.bind(('', self.port))
        self.listening_socket.listen(10)
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)
        self.running = True
        self.waitting_players = 0
        self.connected_clients = []

    def set_indication(self, game_server):
        self.game_server = game_server

    def run(self):
        try:
            while self.running:
                input_ready, output_ready, except_ready = select.select([self.listening_socket] + self.connected_clients, [], [])
                print "[TCPServer] Activity"
                for client in input_ready:
                    if client == self.listening_socket:
                        print "[TCPServer] New connection"
                        client, (ip, address) = self.listening_socket.accept()
                        client.setblocking(0)
                        print client, ip, address
                        self.connected_clients += [client]
                    elif client in self.connected_clients:
                        peek = client.recv(1, socket.MSG_PEEK)
                        if len(peek) == 0:
                            # disconnection
                            print "[TCPServer] Client disconnected"
                            self.game_server.disconnection_ind(client)
                            client.close()
                            self.connected_clients.remove(client)
                        else:
                            print "[TCPServer] Data received"
                            raw_data = client.recv(4096)
                            self.game_server.recv_ind(client, raw_data)
                            try:
                                while len(client.recv(4096)) > 0:
                                    pass
                            except:
                                pass
        except KeyboardInterrupt:
            print "Shutting down..."
            self.shutdown()
            return

    def shutdown(self):
        print "[TCPServer] Closing listening socket"
        if self.listening_socket > 0:
            self.listening_socket.close()
            self.listening_socket = -1

    # ITCPReq implementation
    def shutdown_req(self):
        self.shutdown()

    def send_req(self, client, data):
        # server doesn't send anything to clients
        return

    def disconnect_req(self, client):
        print "[TCPServer] CloseReq, removing client from list"
        client.close()
        try:
            self.connected_clients.remove(client)
        except ValueError:
            print "Remove called but client is unknown"
