# -*- coding: utf8 -*-

#################################
# Juan Antonio Aldea Armenteros #
# CSPA - LUT - 2013             #
#################################

from Player import Player


class GameLogic(object):
    @staticmethod
    def initial_board_as_affected_positions(size):
        player_white = [[size / 2 - 1, size / 2 - 1], [size / 2, size / 2]]
        player_black = [[size / 2 - 1, size / 2], [size / 2, size / 2 - 1]]
        return [player_white, player_black]

    @staticmethod
    def next_turn_player(boardmodel, current_player):
        other_player = Player.WHITE if current_player == Player.BLACK else Player.BLACK
        if GameLogic.is_there_any_valid_position(boardmodel, other_player):
            return other_player
        elif GameLogic.is_there_any_valid_position(boardmodel, current_player):
            return current_player
        else:
            return Player.EMPTY

    @staticmethod
    def is_there_any_valid_position(boardmodel, player):
        for i in xrange(boardmodel.get_size()):
            for j in xrange(boardmodel.get_size()):
                if (GameLogic.is_valid_position(boardmodel, i, j, player)):
                    return True
        return False

    @staticmethod
    def is_valid_position(boardmodel, row, column, player):
        return len(GameLogic.get_affected_positions(boardmodel, row, column, player)) > 0

    @staticmethod
    def apply_move(boardmodel, row, column, player):
        affected_positions = GameLogic.get_affected_positions(boardmodel, row, column, player)
        if len(affected_positions) > 0:
            boardmodel.set(row, column, player)
            GameLogic.apply_updated_positions(boardmodel, player, affected_positions)

    @staticmethod
    def apply_updated_positions(boardmodel, player, updated_positions):
        for i, j in updated_positions:
            boardmodel.set(i, j, player)

    @staticmethod
    def get_affected_positions(boardmodel, row, column, player):
        positions = list()

        # Check whether position is empty
        if boardmodel.get(row, column) != Player.EMPTY:
            return positions

        opponent = Player.WHITE if player == Player.BLACK else Player.BLACK

        # Check vertical up
        if row > 0 and boardmodel.get(row - 1, column) == opponent:
            candidates = list()
            candidates.append([row - 1, column])
            for i in reversed(range(row - 2 + 1)):
                if boardmodel.get(i, column) == player:
                    positions.extend(candidates)
                    break
                elif boardmodel.get(i, column) == Player.EMPTY:
                    break
                else:
                    candidates.append([i, column])

        # Check vertical down
        if (row + 1) < boardmodel.get_size() and boardmodel.get(row + 1, column) == opponent:
            candidates = list()
            candidates.append([row + 1, column])
            for i in range(row + 2, boardmodel.get_size()):
                if boardmodel.get(i, column) == player:
                    positions.extend(candidates)
                    break
                elif boardmodel.get(i, column) == Player.EMPTY:
                    break
                else:
                    candidates.append([i, column])

        # Check horizontal left
        if column > 0 and boardmodel.get(row, column - 1) == opponent:
            candidates = list()
            candidates.append([row, column - 1])
            for j in reversed(range(column - 2 + 1)):
                if boardmodel.get(row, j) == player:
                    positions.extend(candidates)
                    break
                elif boardmodel.get(row, j) == Player.EMPTY:
                    break
                else:
                    candidates.append([row, j])

        # Check horizontal right
        if (column + 1) < boardmodel.get_size() and boardmodel.get(row, column + 1) == opponent:
            candidates = list()
            candidates.append([row, column + 1])
            for j in range(column + 2, boardmodel.get_size()):
                if boardmodel.get(row, j) == player:
                    positions.extend(candidates)
                    break
                elif boardmodel.get(row, j) == Player.EMPTY:
                    break
                else:
                    candidates.append([row, j])

        # Check diagonal left, up
        if row > 0 and column > 0 and boardmodel.get(row - 1, column - 1) == opponent:
            candidates = list()
            candidates.append([row - 1, column - 1])
            i = row - 2
            j = column - 2
            while i >= 0 and j >= 0:
                if boardmodel.get(i, j) == player:
                    positions.extend(candidates)
                    break
                elif boardmodel.get(i, j) == Player.EMPTY:
                    break
                else:
                    candidates.append([i, j])
                i -= 1
                j -= 1

        # Check diagonal left, down
        if row + 1 < boardmodel.get_size() and column > 0 and boardmodel.get(row + 1, column - 1) == opponent:
            candidates = list()
            candidates.append([row + 1, column - 1])
            i = row + 2
            j = column - 2
            while i < boardmodel.get_size() and j >= 0:
                if boardmodel.get(i, j) == player:
                    positions.extend(candidates)
                    break
                elif boardmodel.get(i, j) == Player.EMPTY:
                    break
                else:
                    candidates.append([i, j])
                i += 1
                j -= 1

        # Check diagonal right, down
        if row + 1 < boardmodel.get_size() and column + 1 < boardmodel.get_size() and boardmodel.get(row + 1, column + 1) == opponent:
            candidates = list()
            candidates.append([row + 1, column + 1])
            i = row + 2
            j = column + 2
            while i < boardmodel.get_size() and j < boardmodel.get_size():
                if boardmodel.get(i, j) == player:
                    positions.extend(candidates)
                    break
                elif boardmodel.get(i, j) == Player.EMPTY:
                    break
                else:
                    candidates.append([i, j])
                i += 1
                j += 1

        # Check diagonal right, up
        if row > 0 and column + 1 < boardmodel.get_size() and boardmodel.get(row - 1, column + 1) == opponent:
            candidates = list()
            candidates.append([row - 1, column + 1])
            i = row - 2
            j = column + 2
            while i >= 0 and j < boardmodel.get_size():
                if boardmodel.get(i, j) == player:
                    positions.extend(candidates)
                    break
                elif boardmodel.get(i, j) == Player.EMPTY:
                    break
                else:
                    candidates.append([i, j])
                i -= 1
                j += 1

        if len(positions) > 0:
            positions.insert(0, [row, column])

        return positions
