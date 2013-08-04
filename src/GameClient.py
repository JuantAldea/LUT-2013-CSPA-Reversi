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

from ITCPInd import ITCPInd
from IGameClientReq import IGameClientReq
from GameServerPDUCodec import GameServerPDUCodec
from GameInstanceServerPDUCodec import GameInstanceServerPDUCodec
from GameClientPDUCodec import GameClientPDUCodec
from PDUCodes import PDUCodes
from GameClientTCP import GameClientTCP
from BoardModel import BoardModel
from GameLogic import GameLogic


class GameClientState:

    def connect_req(self, context, ip, port):
        return

    def disconnection_ind(self, context):
        return

    def place_req(self, context, x, y):
        return

    def place_error_ind(self, context):
        return

    def disconnect_req(self, context):
        return

    def connection_ok_ind(self, context, player):
        return

    def turn_ind(self, context):
        return

    def winner_ind(self, context, winner):
        return

    def updated_board_ind(self, context, player, affected_positions):
        return

    def shutdown_req(self, context):
        return


class DISCONNECTED(GameClientState):

    def connect_req(self, context, ip, port):
        context.request = GameClientTCP()
        context.request.set_indication(context)
        connected = context.request.connect_req(ip, port)
        if connected:
            context.request.send_req(None, GameServerPDUCodec.connect_pdu())
            context.state = context.WAITING_FOR_ANOTHER_PLAYER
            print "Thread starts"
            context.request.start()
        else:
            context.request = None
        return connected


class WAITING_FOR_ANOTHER_PLAYER(GameClientState):

    def disconnect_req(self, context):
        context.request.disconnect_req(None)
        context.state = context.DISCONNECTED

    def disconnection_ind(self, context):
        context.state = context.DISCONNECTED
        context.indication.disconnection_ind()

    def connection_ok_ind(self, context, player):
        context.indication.connection_ok_ind(player)
        context.state = context.CONNECTED

    def shutdown_req(self, context):
        context.request.send_req(None, GameInstanceServerPDUCodec.disconnect_pdu())
        context.request.shutdown_req()


class CONNECTED(GameClientState):

    def disconnect_req(self, context):
        context.request.send_req(None, GameInstanceServerPDUCodec.disconnect_pdu())
        context.request.disconnect_req(None)
        context.state = context.DISCONNECTED

    def disconnection_ind(self, context):
        context.state = context.DISCONNECTED
        context.indication.disconnection_ind()

    def place_req(self, context, x, y):
        context.request.send_req(None, GameInstanceServerPDUCodec.place_pdu(x, y))

    def place_error_ind(self, context):
        context.indication.place_error_ind()

    def turn_ind(self, context):
        context.indication.turn_ind()

    # TODO: Disconnect on winner ind?
    def winner_ind(self, context, winner):
        context.indication.winner_ind(winner)

    def updated_board_ind(self, context, player, affected_positions):
        GameLogic.apply_updated_positions(context.board_model, player, affected_positions)
        context.indication.updated_board_ind(player, affected_positions)

    def shutdown_req(self, context):
        context.request.send_req(None, GameInstanceServerPDUCodec.disconnect_pdu())
        context.request.shutdown_req()


class GameClient(IGameClientReq, ITCPInd):

    def __init__(self):
        self.board_model = BoardModel(8)
        self.indication = None
        self.request = None
        self.DISCONNECTED = DISCONNECTED()
        self.WAITING_FOR_ANOTHER_PLAYER = WAITING_FOR_ANOTHER_PLAYER()
        self.CONNECTED = CONNECTED()
        self.state = self.DISCONNECTED

    def set_indication(self, indication):
        self.indication = indication

    def set_request(self, request):
        self.request = request

    # IGameClientReq implementation
    def shutdown_req(self):
        self.state.shutdown_req(self)
        self.board_model = BoardModel(8)

    def connect_req(self, ip, port):
        return self.state.connect_req(self, ip, port)

    def place_req(self, x, y):
        self.state.place_req(self, x, y)

    def disconnect_req(self):
        self.state.disconnect_req(self)
        self.board_model = BoardModel(8)

    # ITCPInd implementation

    def recv_ind(self, client, data):
        (pdu_id, pdu_size, pdu_data) = GameClientPDUCodec.decode(data)
        print (pdu_id, pdu_size, pdu_data)
        if pdu_id == PDUCodes.CLIENT_CONNECT_OK:
            self.state.connection_ok_ind(self, pdu_data[0])
        elif pdu_id == PDUCodes.PLACE_ERROR:
            self.state.place_error_ind(self)
        elif pdu_id == PDUCodes.TURN:
            self.state.turn_ind(self)
        elif pdu_id == PDUCodes.WINNER:
            self.state.winner_ind(self, pdu_data[0])
        elif pdu_id == PDUCodes.UPDATE_BOARD:
            self.state.updated_board_ind(self, pdu_data[0], pdu_data[1])
        return pdu_size

    def disconnection_ind(self, client):
        self.board_model = BoardModel(8)
        self.state.disconnection_ind(self)
