# pyReversi is a multiplayer reversi game with dedicated server
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

from random import shuffle

from PDUCodes import PDUCodes
from BoardModel import BoardModel
from GameLogic import GameLogic
from GameInstanceServerPDUCodec import GameInstanceServerPDUCodec
from GameInstanceServerTCP import GameInstanceServerTCP
from GameClientPDUCodec import GameClientPDUCodec
from ITCPInd import ITCPInd
from Player import Player


class GameInstanceState:
    def disconnection_ind(self, context, client):
        print "[Game Instance] Got a disconnection"
        winner = None
        if client == context.socket_player_white:
            other_player = context.socket_player_black
            winner = Player.BLACK
        else:
            other_player = context.socket_player_white
            winner = Player.WHITE
        context.request.send_req(other_player, GameClientPDUCodec.winner_pdu(winner))
        context.request.shutdown_req()

    def place_pdu(self, context, socket, x, y):
        return

    def turn_req(self, context):
        context.request.send_req(context.turn, GameClientPDUCodec.turn_pdu())

    def end_game(self, context):
        white_count, black_count = context.boardmodel.count_disks()

        winner_pdu = GameClientPDUCodec.winner_pdu(Player.EMPTY)

        if white_count > black_count:
            winner_pdu = GameClientPDUCodec.winner_pdu(Player.WHITE)
        elif black_count > white_count:
            winner_pdu = GameClientPDUCodec.winner_pdu(Player.BLACK)

        context.request.send_req(context.socket_player_white, winner_pdu)
        context.request.send_req(context.socket_player_black, winner_pdu)
        context.request.shutdown_req()


class WHITE_TURN(GameInstanceState):

    def place_pdu(self, context, client, x, y):
        if client == context.socket_player_white:
            if GameLogic.is_valid_position(context.boardmodel, x, y, Player.WHITE):
                affected_positions = GameLogic.get_affected_positions(context.boardmodel, x, y, Player.WHITE)
                GameLogic.apply_move(context.boardmodel, x, y, Player.WHITE)
                board_pdu = GameClientPDUCodec.update_board_pdu(Player.WHITE, affected_positions)
                context.request.send_req(context.socket_player_white, board_pdu)
                context.request.send_req(context.socket_player_black, board_pdu)
                next_turn_player = GameLogic.next_turn_player(context.boardmodel, Player.WHITE)

                white_count, black_count = context.boardmodel.count_disks()
                # if white_count > 4:
                #    context.end_game()

                if next_turn_player == Player.WHITE:
                    context.turn = context.socket_player_white
                    context.state = context.WHITE_TURN
                    context.state.turn_req(context)
                elif next_turn_player == Player.BLACK:
                    context.turn = context.socket_player_black
                    context.state = context.BLACK_TURN
                    context.state.turn_req(context)
                else:
                    # no valid movements->board full or no valid placements for any player
                    context.end_game()
            else:
                context.request.send_req(client, GameClientPDUCodec.place_error_pdu())
                context.request.send_req(client, GameClientPDUCodec.turn_pdu())
        else:
            # not your turn
            # read protocol, I don't remember if it's specified to report the error or not
            context.request.send_req(client, GameClientPDUCodec.place_error_pdu())


class BLACK_TURN(GameInstanceState):

    def place_pdu(self, context, client, x, y):
        if client == context.socket_player_black:
            if GameLogic.is_valid_position(context.boardmodel, x, y, Player.BLACK):
                affected_positions = GameLogic.get_affected_positions(context.boardmodel, x, y, Player.BLACK)
                GameLogic.apply_move(context.boardmodel, x, y, Player.BLACK)
                board_pdu = GameClientPDUCodec.update_board_pdu(Player.BLACK, affected_positions)
                # update boards
                context.request.send_req(context.socket_player_white, board_pdu)
                context.request.send_req(context.socket_player_black, board_pdu)

                white_count, black_count = context.boardmodel.count_disks()
                # if black_count > 4:
                 #   context.end_game()

                next_turn_player = GameLogic.next_turn_player(context.boardmodel, Player.BLACK)
                if next_turn_player == Player.WHITE:
                    context.turn = context.socket_player_white
                    context.state = context.WHITE_TURN
                    context.state.turn_req(context)
                elif next_turn_player == Player.BLACK:
                    context.turn = context.socket_player_black
                    context.state = context.BLACK_TURN
                    context.state.turn_req(context)
                else:
                    # no valid movements->board full or no valid placements for any player
                    context.end_game()
            else:
                context.request.send_req(client, GameClientPDUCodec.place_error_pdu())
                context.request.send_req(client, GameClientPDUCodec.turn_pdu())
        else:
            # not your turn
            # read protocol, I don't remember if it's specified to report or not the error
            context.request.send_req(client, GameClientPDUCodec.place_error_pdu())


class GameInstanceServer(GameInstanceServerPDUCodec, ITCPInd):

    def __init__(self, clients):
        shuffle(clients)
        self.socket_player_white = clients[0]
        self.socket_player_black = clients[1]
        self.request = GameInstanceServerTCP(self.socket_player_white, self.socket_player_black, self)
        self.WHITE_TURN = WHITE_TURN()
        self.BLACK_TURN = BLACK_TURN()
        self.boardmodel = BoardModel(8, True)
        # black player starts according to reversi rules
        self.state = self.BLACK_TURN
        self.turn = self.socket_player_black

    def game_init(self):
        self.request.send_req(self.socket_player_white, GameClientPDUCodec.connect_ok_pdu(Player.WHITE))
        self.request.send_req(self.socket_player_black, GameClientPDUCodec.connect_ok_pdu(Player.BLACK))

        initial_board = GameLogic.initial_board_as_affected_positions(8)
        self.request.send_req(self.socket_player_white, GameClientPDUCodec.update_board_pdu(Player.WHITE, initial_board[0]))
        self.request.send_req(self.socket_player_white, GameClientPDUCodec.update_board_pdu(Player.BLACK, initial_board[1]))
        self.request.send_req(self.socket_player_black, GameClientPDUCodec.update_board_pdu(Player.WHITE, initial_board[0]))
        self.request.send_req(self.socket_player_black, GameClientPDUCodec.update_board_pdu(Player.BLACK, initial_board[1]))

        self.request.send_req(self.socket_player_black, GameClientPDUCodec.turn_pdu())

    def start(self):
        self.game_init()
        self.request.run()

    # input delegated to states
    def turn_req(self):
        self.state.turn_req(self)

    def place_pdu(self, socket, x, y):
        self.state.place_pdu(self, socket, x, y)

    def end_game(self):
        self.state.end_game(self)

    def error_req(self, socket):
        self.state.error_req(self, socket)

    # ITCPInd implementation
    def recv_ind(self, client, data):
        print "[GAME INSTANCE] Data indication"
        (pdu_id, pdu_size, pdu_data) = self.decode(data)
        print (pdu_id, pdu_size, pdu_data)
        if pdu_id == PDUCodes.PLACE:
            self.place_pdu(client, pdu_data[0], pdu_data[1])
        elif pdu_id == PDUCodes.CLIENT_QUIT:
            self.state.disconnection_ind(self, client)
        else:
            print "ALGO RARO", data
        return pdu_size

    def disconnection_ind(self, client):
        self.state.disconnection_ind(self, client)
