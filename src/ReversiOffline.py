#!/usr/bin/python
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

import gobject
import sys
try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

from Player import *
from BoardModel import *
from GameLogic import *


class ReversiOffline(object):

    yourturn = True
    player = Player.WHITE
    boardmodel = None
    pending_drawings = None

    widgets = None
    window = None
    drawingarea = None
    toolbuttonShowHint = None

    background = None
    white = None
    black = None
    hint = None
    scaledbackground = None
    scaledwhite = None
    scaledblack = None
    scaledhint = None

    width = None
    height = None
    size = None
    ratio = None
    cellsize = None
    shift_x = None
    shift_y = None
    shift_border = None

    selection_row = None
    selection_column = None
    selection_valid = False

    def __init__(self):
    # Load widgets from Glade file
        self.widgets = gtk.glade.XML("interface.glade")

        # Shorcuts for exhaustive use of widgets
        self.window = self.widgets.get_widget("windowMain")
        self.drawingarea = self.widgets.get_widget("drawingarea")
        self.toolbuttonShowHint = self.widgets.get_widget("toolbuttonShowHint")

        # Show main window
        # self.window.maximize()
        self.window.show()

        # Initialize
        self.boardmodel = BoardModel(8)
        self.pending_drawings = list()
        self.drawingarea.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 0, 0))
        self.loadResources()
        self.resizeDrawingArea(None, None)
        self.updateStatusBar()

        # Connect signals to slots
        dic = {
            "on_imagemenuitemConnect_activate": self.showDialogConnect,
            "on_imagemenuitemDisconnect_activate": self.disconnect,
            "on_imagemenuitemAbout_activate": self.showDialogAbout,
            "on_toolbuttonConnect_clicked": self.showDialogConnect,
            "on_toolbuttonDisconnect_clicked": self.disconnect,
            "on_windowMain_destroy": self.quit,
            "on_imagemenuitemQuit_activate": self.quit,
            "on_buttonAboutClose_clicked": self.hideDialogAbout,
            "on_buttonConnectCancel_clicked": self.hideDialogConnect,
            "on_buttonConnectOk_clicked": self.connect,
            "on_drawingarea_expose_event": self.draw,
            "on_drawingarea_size_allocate": self.resizeDrawingArea,
            "on_drawingarea_button_press_event": self.clicked,
            "on_drawingarea_motion_notify_event": self.moved,
            "on_toolbuttonShowHint_toggled": self.draw,
        }
        self.widgets.signal_autoconnect(dic)

    def start(self):
        gtk.main()

    def quit(self, widget):
        gtk.main_quit()

    def showDialogConnect(self, widget):
        self.widgets.get_widget("dialogConnect").show()

    def hideDialogConnect(self, widget):
        self.widgets.get_widget("dialogConnect").hide()

    def showDialogAbout(self, widget):
        self.widgets.get_widget("dialogAbout").show()

    def hideDialogAbout(self, widget):
        self.widgets.get_widget("dialogAbout").hide()

    def connect(self, widget):
        ip = self.widgets.get_widget("entryIp").get_text()
        port = self.widgets.get_widget("spinbuttonPort").get_value_as_int()

        connected = True
        print "TODO connect to server " + ip + ":" + str(port)

        if connected:
            self.widgets.get_widget("dialogConnect").hide()
            self.widgets.get_widget("toolbuttonConnect").set_sensitive(False)
            self.widgets.get_widget("toolbuttonDisconnect").set_sensitive(True)
            self.widgets.get_widget("imagemenuitemConnect").set_sensitive(False)
            self.widgets.get_widget("imagemenuitemDisconnect").set_sensitive(True)

    def disconnect(self, widget):
        print "TODO disconnect from server"

        self.widgets.get_widget("toolbuttonConnect").set_sensitive(True)
        self.widgets.get_widget("toolbuttonDisconnect").set_sensitive(False)
        self.widgets.get_widget("imagemenuitemConnect").set_sensitive(True)
        self.widgets.get_widget("imagemenuitemDisconnect").set_sensitive(False)

    def loadResources(self):
        self.background = gtk.gdk.pixbuf_new_from_file("res/background.png")
        self.white = gtk.gdk.pixbuf_new_from_file("res/white.png")
        self.black = gtk.gdk.pixbuf_new_from_file("res/black.png")
        self.hint = gtk.gdk.pixbuf_new_from_file("res/hint.png")

    # Scales images every time the area is resized and stores some variables to be used in draw method
    def resizeDrawingArea(self, widgets, events):
        self.width, self.height = self.drawingarea.window.get_size()
        self.size = max(1, min(self.width, self.height))
        self.ratio = self.size / float(self.background.get_width())
        self.cellsize = self.white.get_width() * self.ratio

        self.scaledbackground = self.background.scale_simple(
            int(round(self.size)), int(round(self.size)), gtk.gdk.INTERP_BILINEAR)
        self.scaledwhite = self.white.scale_simple(
            int(round(self.cellsize)), int(round(self.cellsize)), gtk.gdk.INTERP_BILINEAR)
        self.scaledblack = self.black.scale_simple(
            int(round(self.cellsize)), int(round(self.cellsize)), gtk.gdk.INTERP_BILINEAR)
        self.scaledhint = self.hint.scale_simple(int(round(self.cellsize)), int(round(self.cellsize)), gtk.gdk.INTERP_BILINEAR)

        self.shift_x = abs(self.width - self.scaledbackground.get_width()) / 2.0
        self.shift_y = abs(self.height - self.scaledbackground.get_height()) / 2.0
        self.shift_border = 96 * self.ratio  # 96px is the width of the border built-in the image

    def draw(self, widget=None, events=None):
        self.drawingarea.window.draw_pixbuf(
            None, self.scaledbackground, 0, 0, int(round(self.shift_x)), int(round(self.shift_y)))

        for i in range(self.boardmodel.get_size()):
            for j in range(self.boardmodel.get_size()):
                player = self.boardmodel.get(i, j)
                if player == Player.WHITE:
                    self.drawCell(i, j, self.scaledwhite)
                elif player == Player.BLACK:
                    self.drawCell(i, j, self.scaledblack)
                elif self.yourturn and self.toolbuttonShowHint.get_active() and GameLogic.is_valid_position(self.boardmodel, i, j, self.player):
                    self.drawCell(i, j, self.scaledhint)

        if self.yourturn and self.selection_row is not None and self.selection_column is not None and self.selection_valid:
            self.drawingarea.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
            self.drawCell(self.selection_row, self.selection_column,
                          self.scaledwhite if self.player == Player.WHITE else self.scaledblack)
        else:
            self.drawingarea.window.set_cursor(None)

    def drawCell(self, row, column, image):
        self.drawingarea.window.draw_pixbuf(None, image, 0, 0, int(
            round(self.shift_x + self.shift_border + column * self.cellsize)), int(round(self.shift_y + self.shift_border + row * self.cellsize)))

    def moved(self, widget, event):
        if len(self.pending_drawings) > 0:
            return

        previous_row = self.selection_row
        previous_column = self.selection_column
        previous_valid = self.selection_valid
        noshift_x = event.x - self.shift_x - self.shift_border
        noshift_y = event.y - self.shift_y - self.shift_border
        if 0 <= noshift_x and noshift_x < self.size - 2 * self.shift_border and 0 <= noshift_y and noshift_y < self.size - 2 * self.shift_border:
            self.selection_column = int((noshift_x / self.cellsize) % 8.0)
            self.selection_row = int((noshift_y / self.cellsize) % 8.0)
            self.selection_valid = GameLogic.is_valid_position(
                self.boardmodel, self.selection_row, self.selection_column, self.player)
        else:
            self.selection_column = None
            self.selection_row = None
            self.selection_valid = False
        if previous_valid != self.selection_valid or ((previous_row != self.selection_row or previous_column != self.selection_column) and self.selection_valid):
            if self.selection_valid and previous_valid is False:
                self.drawingarea.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
                self.drawCell(self.selection_row, self.selection_column,
                              self.scaledwhite if self.player == Player.WHITE else self.scaledblack)
            else:
                self.draw()

    def clicked(self, widget, event):
        if self.selection_row is not None and self.selection_column is not None:
            print "[" + str(self.selection_row) + ", " + str(self.selection_column) + "]"
            positions = GameLogic.get_affected_positions(
                self.boardmodel, self.selection_row, self.selection_column, self.player)
            if len(positions) > 0:
                self.boardmodel.set(self.selection_row, self.selection_column, self.player)
                for i, j in positions:
                    self.boardmodel.set(i, j, self.player)

                self.pending_drawings.append([self.selection_row, self.selection_column])
                self.pending_drawings.extend(positions)

                gobject.timeout_add(100, self.drawAffectedPositions)

                self.drawingarea.window.set_cursor(None)
                self.selection_row = None
                self.selection_column = None
                self.selection_valid = False

    def drawAffectedPositions(self):
        if len(self.pending_drawings) == 0:
            self.player = Player.WHITE if self.player == Player.BLACK else Player.BLACK
            self.updateStatusBar()
            if self.toolbuttonShowHint.get_active():
                self.draw()
            return False

        row, column = self.pending_drawings.pop(0)
        self.drawCell(row, column, self.scaledwhite if self.player == Player.WHITE else self.scaledblack)
        return True

    def updateStatusBar(self):
        white_count, black_count = self.boardmodel.count_disks()
        if self.player == Player.WHITE:
            self.widgets.get_widget("labelWhiteCount").set_text("You (" + str(white_count) + " disks)")
            self.widgets.get_widget("labelBlackCount").set_text("Opponent (" + str(black_count) + " disks)")
        else:
            self.widgets.get_widget("labelWhiteCount").set_text("Opponent (" + str(white_count) + " disks)")
            self.widgets.get_widget("labelBlackCount").set_text("You (" + str(black_count) + " disks)")
        self.widgets.get_widget("labelTurn").set_text("Your turn" if self.yourturn else "Opponent's turn")


if __name__ == "__main__":
    ReversiOffline().start()
