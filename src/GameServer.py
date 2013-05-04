# -*- coding: utf8 -*-

#################################
# Juan Antonio Aldea Armenteros #
# CSPA - LUT - 2013             #
#################################

import os
from ITCPInd import ITCPInd
from GameInstanceServer import GameInstanceServer
from GameServerPDUCodec import GameServerPDUCodec
from PDUCodes import PDUCodes


class GameServerState:

    def connect_pdu(self, game_server_context, client):
        return

    def disconnect_ind(self, game_server_context, client):
        if client == game_server_context.player_one:
            print "[GameServerState] Disconnected WP1: WP2 -> WP1"
            game_server_context.player_one = None
            game_server_context.state = game_server_context.WAITING_PLAYER_1
        elif client == game_server_context.player_two:
            print "[GameServerState] Disconnected WP2: WP1 -> WP2"
            game_server_context.player_two = None
            game_server_context.state = game_server_context.WAITING_PLAYER_2


class WAITING_PLAYER_1(GameServerState):

    def connect_pdu(self, game_server_context, client):
        if client != game_server_context.player_two:
            game_server_context.player_one = client
            if game_server_context.player_two is None:
                print "[GameServerState] Connected WP1, WP2 aboutsent: WP1 -> WP2"
                game_server_context.state = game_server_context.WAITING_PLAYER_2
            else:
                game_server_context.state = game_server_context.WAITING_PLAYER_1
                print "[GameServerState] Connected WP1: WP2 present => launch game"
                game_server_context.start_game()


class WAITING_PLAYER_2(GameServerState):

    def connect_pdu(self, game_server_context, client):
        if client != game_server_context.player_one:
            game_server_context.player_two = client
            if game_server_context.player_one is None:
                print "[GameServerState] Connected WP2, WPI absent: WP2 -> WP1"
                game_server_context.state = game_server_context.WAITING_PLAYER_1
            else:
                game_server_context.state = game_server_context.WAITING_PLAYER_1
                print "[GameServerState] Connected WP2: WP1 present => launch game and WP2 -> WP1"
                game_server_context.start_game()


class GameServer(ITCPInd):

    def __init__(self, tcp_server):
        self.player_one = None
        self.player_two = None
        self.tcp_server = tcp_server
        self.WAITING_PLAYER_1 = WAITING_PLAYER_1()
        self.WAITING_PLAYER_2 = WAITING_PLAYER_2()
        self.state = self.WAITING_PLAYER_1

    def start_game(self):
        print "[GAMESERVER] Starting game"
        childPid = os.fork()
        if childPid == 0:
            # child process
            # close listening socket
            self.tcp_server.shutdown_req()
            GameInstanceServer([self.player_one, self.player_two]).start()
            os._exit(0)
        else:
            # father forgets about emancipated childs
            self.tcp_server.disconnect_req(self.player_one)
            self.player_one = None
            self.tcp_server.disconnect_req(self.player_two)
            self.player_two = None

    def run(self):
        self.tcp_server.run()

    def shutdown(self):
        if self.player_one is not None and self.player_one.fileno() > 0:
            self.tcp_server.disconnect_req(self.player_one)
        if self.player_two is not None and self.player_two.fileno() > 0:
            self.tcp_server.disconnect_req(self.player_two)

    # ITCPInd implementation
    def recv_ind(self, client, data):
        (pdu_id, len_pdu, _) = GameServerPDUCodec.decode(data)
        if pdu_id == PDUCodes.CLIENT_CONNECT:
            self.state.connect_pdu(self, client)
        return len_pdu

    def disconnection_ind(self, client):
        self.state.disconnect_ind(self, client)
