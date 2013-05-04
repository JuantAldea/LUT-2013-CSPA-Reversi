# -*- coding: utf8 -*-

#################################
# Juan Antonio Aldea Armenteros #
# CSPA - LUT - 2013             #
#################################

import select
import socket
from ITCPReq import ITCPReq


class GameInstanceServerTCP(ITCPReq):
    def __init__(self, socket_player_white, socket_player_black, indication):
        self.socket_player_white = socket_player_white
        self.socket_player_black = socket_player_black
        self.indication = indication
        self.running = True
        self.socket_player_white.setblocking(0)
        self.socket_player_black.setblocking(0)

    def run(self):
        clients = [self.socket_player_white, self.socket_player_black]
        while self.running:
            input_ready, output_ready, except_ready = select.select(clients, [], [], 5)
            for client in input_ready:
                try:
                    # got a disconnection
                    if len(client.recv(1, socket.MSG_PEEK)) == 0:
                        self.indication.disconnection_ind(client)
                        clients.remove(client)
                        client.close()
                        break
                    else:
                        # got data
                        print "[TCPGameInstanceTCPServer] GOT DATA"
                        msg_size = self.indication.recv_ind(client, client.recv(4096, socket.MSG_PEEK))
                        if msg_size != -1:
                            print "[TCPGameInstanceTCPServer] Removing PDU from buffer"
                            # remove from buffer
                            client.recv(msg_size)
                        else:
                            # error, just empty socket's buffer
                            print "[TCPGameInstanceTCPServer] Empty buffer"
                            while len(client.recv(4096)) > 0:
                                pass
                except socket.error:
                    pass
        self.socket_player_white.close()
        self.socket_player_black.close()

    # ITCPReq implementation
    def shutdown_req(self):
        self.running = False

    def send_req(self, client, data):
        try:
            if client == self.socket_player_white:
                self.socket_player_white.sendall(data)
            elif client == self.socket_player_black:
                self.socket_player_black.sendall(data)
        except socket.error:
            pass

    def disconnect_req(self, client):
        return
