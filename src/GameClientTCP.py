# -*- coding: utf8 -*-

#################################
# Juan Antonio Aldea Armenteros #
# CSPA - LUT - 2013             #
#################################

import select
import socket
import threading
import struct
from ITCPReq import ITCPReq


class GameClientTCP(ITCPReq, threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.indication = None
        self.running = True

    def set_indication(self, indication):
        self.indication = indication

    def run(self):
        while self.running:
            if True:
            # try:
                rlist, wlist, xlist = select.select([self.socket], [], [], 1.0)
                if self.socket in rlist:
                    if len(self.socket.recv(1, socket.MSG_PEEK)) == 0:
                        # disconnection
                        self.indication.disconnection_ind(None)
                        self.disconnect_req(None)
                    else:
                        data = self.socket.recv(4096, socket.MSG_PEEK)
                        msg_size, = struct.unpack("<h", data[:2])
                        print msg_size, len(data)
                        if msg_size <= len(data):
                            pdu_len = self.indication.recv_ind(None, data)
                            if pdu_len > 0:
                                self.socket.recv(pdu_len)
                                print "RESTAN", len(data) - pdu_len
                            else:
                                # error, just empty socket's buffer
                                print "[TCPGameInstanceTCPServer] Empty buffer"
                                while len(self.socket.recv(4096)) > 0:
                                    pass
            # except:
                # print "EXCEPTION"
                # pass
        self.socket.close()
        print "Thread death"

    def connect_req(self, address, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.socket.connect_ex((address, port)) == 0:
            self.socket.setblocking(0)
            self.running = True
            return True
        return False

    # ITCPReq Implementation
    def shutdown_req(self):
        self.running = False

    def send_req(self, client, data):
        self.socket.sendall(data)

    def disconnect_req(self, client):
        self.running = False
