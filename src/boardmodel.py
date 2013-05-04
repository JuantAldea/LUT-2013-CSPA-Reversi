# -*- coding: utf8 -*-

#################################
# Juan Antonio Aldea Armenteros #
# CSPA - LUT - 2013             #
#################################

from player import Player


class BoardModel(object):
    def __init__(self, size, initial_positions=False):
        self.size = size
        self.board_status = [[Player.EMPTY for i in xrange(size)] for i in xrange(size)]
        if initial_positions:
            self.board_status[size / 2 - 1][size / 2 - 1] = Player.WHITE
            self.board_status[size / 2][size / 2] = Player.WHITE
            self.board_status[size / 2 - 1][size / 2] = Player.BLACK
            self.board_status[size / 2][size / 2 - 1] = Player.BLACK

    def printt(self):
        for row in self.board_status:
            print row

    def get_size(self):
        return self.size

    def get(self, row, column):
        return self.board_status[row][column]

    def set(self, row, column, value):
        self.board_status[row][column] = value

    def count_disks(self):
        black_count = 0
        white_count = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board_status[i][j] == Player.WHITE:
                    white_count += 1
                elif self.board_status[i][j] == Player.BLACK:
                    black_count += 1
        return white_count, black_count
