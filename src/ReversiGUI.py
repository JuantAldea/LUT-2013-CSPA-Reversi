# -*- coding: utf8 -*-

#################################
# Juan Antonio Aldea Armenteros #
# CSPA - LUT - 2013             #
#################################

import gobject
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

from player import Player
from gamelogic import GameLogic
from GameClient import GameClient
from IGameClientInd import IGameClientInd


class ReversiGUI(IGameClientInd):

    def __init__(self):
        self.yourturn = False
        self.player = Player.WHITE
        self.pending_drawings = None

        self.widgets = None
        self.window = None
        self.drawingarea = None
        self.toolbuttonShowHint = None

        self.background = None
        self.white = None
        self.black = None
        self.hint = None
        self.scaledbackground = None
        self.scaledwhite = None
        self.scaledblack = None
        self.scaledhint = None

        self.width = None
        self.height = None
        self.size = None
        self.ratio = None
        self.cellsize = None
        self.shift_x = None
        self.shift_y = None
        self.shift_border = None

        self.selection_row = None
        self.selection_column = None
        self.selection_valid = False

        self.request = GameClient()
        self.request.indication = self
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
        self.pending_drawings = list()
        self.drawingarea.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 0, 0))
        self.load_resources()
        self.resize_drawing_area(None, None)
        self.update_status_bar()
        self.connected = False
        # Connect signals to slots
        dic = {
            "on_imagemenuitemConnect_activate": self.show_dialog_connect,
            "on_imagemenuitemDisconnect_activate": self.disconnect,
            "on_imagemenuitemAbout_activate": self.show_dialog_about,
            "on_toolbuttonConnect_clicked": self.show_dialog_connect,
            "on_toolbuttonDisconnect_clicked": self.disconnect,
            "on_windowMain_destroy": self.quit,
            "on_imagemenuitemQuit_activate": self.quit,
            "on_buttonAboutClose_clicked": self.hide_dialog_about,
            "on_buttonConnectCancel_clicked": self.hide_dialog_connect,
            "on_buttonConnectOk_clicked": self.connect,
            "on_drawingarea_expose_event": self.draw,
            "on_drawingarea_size_allocate": self.resize_drawing_area,
            "on_drawingarea_button_press_event": self.clicked,
            "on_drawingarea_motion_notify_event": self.moved,
            "on_toolbuttonShowHint_toggled": self.draw,
        }

        self.widgets.signal_autoconnect(dic)
        self.widgets.get_widget("dialogAbout").connect('delete-event', lambda w, e: w.hide() or True)
        self.widgets.get_widget("dialogConnect").connect('delete-event', lambda w, e: w.hide() or True)
        self.widgets.get_widget("dialogConnecting").connect('delete-event', lambda w, e: w.hide() or True)
        self.widgets.get_widget("dialogDisconnection").connect('delete-event', lambda w, e: w.hide() or True)
        self.set_ui_disconnected_state()

    def set_request(self, request):
        self.request = request

    def run(self):
        gtk.threads_enter()
        gtk.main()
        gtk.threads_leave()

    def quit(self, widget):
        self.request.shutdown_req()
        gtk.main_quit()

    def show_dialog_connect(self, widget):
        self.widgets.get_widget("dialogConnect").show()

    def hide_dialog_connect(self, widget):
        self.widgets.get_widget("dialogConnect").hide()

    def show_dialog_about(self, widget):
        self.widgets.get_widget("dialogAbout").show()

    def hide_dialog_about(self, widget):
        self.widgets.get_widget("dialogAbout").hide()

    def connect(self, widget):
        ip = self.widgets.get_widget("entryIp").get_text()
        port = self.widgets.get_widget("spinbuttonPort").get_value_as_int()
        if self.request.connect_req(ip, port):
            self.widgets.get_widget("dialogConnect").hide()
            response = self.widgets.get_widget("dialogConnecting").run()
            if response == gtk.RESPONSE_CANCEL:
                response = self.widgets.get_widget("dialogConnecting").hide()
                self.request.disconnect_req()
                self.request.shutdown_req()
                self.set_ui_disconnected_state()
        self.draw()

    def disconnect(self, widget):
        self.set_ui_disconnected_state()
        self.request.disconnect_req()
        self.request.shutdown_req()

    def load_resources(self):
        self.background = gtk.gdk.pixbuf_new_from_file("res/background.png")
        self.white = gtk.gdk.pixbuf_new_from_file("res/white.png")
        self.black = gtk.gdk.pixbuf_new_from_file("res/black.png")
        self.hint = gtk.gdk.pixbuf_new_from_file("res/hint.png")

    # Scales images every time the area is resized and stores some variables to be used in draw method
    def resize_drawing_area(self, widgets, events):
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
        for i in range(self.request.board_model.get_size()):
            for j in range(self.request.board_model.get_size()):
                player = self.request.board_model.get(i, j)
                if player == Player.WHITE:
                    self.draw_cell(i, j, self.scaledwhite)
                elif player == Player.BLACK:
                    self.draw_cell(i, j, self.scaledblack)
                elif self.yourturn and self.toolbuttonShowHint.get_active() and GameLogic.is_valid_position(self.request.board_model, i, j, self.player):
                    self.draw_cell(i, j, self.scaledhint)

        if self.yourturn and self.selection_row is not None and self.selection_column is not None and self.selection_valid:
            self.drawingarea.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
            self.draw_cell(self.selection_row, self.selection_column,
                           self.scaledwhite if self.player == Player.WHITE else self.scaledblack)
        else:
            self.drawingarea.window.set_cursor(None)

    def draw_cell(self, row, column, image):
        self.drawingarea.window.draw_pixbuf(None, image, 0, 0, int(
            round(self.shift_x + self.shift_border + column * self.cellsize)), int(round(self.shift_y + self.shift_border + row * self.cellsize)))

    def moved(self, widget, event):
        if self.connected is False:
            return

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
            self.selection_valid = self.request.board_model.get(self.selection_row, self.selection_column) == Player.EMPTY
            # GameLogic.is_valid_position(self.request.board_model, self.selection_row, self.selection_column, self.player)
        else:
            self.selection_column = None
            self.selection_row = None
            self.selection_valid = False
        if previous_valid != self.selection_valid or ((previous_row != self.selection_row or previous_column != self.selection_column) and self.selection_valid):
            if self.selection_valid and previous_valid is False:
                self.drawingarea.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
                self.draw_cell(self.selection_row, self.selection_column,
                               self.scaledwhite if self.player == Player.WHITE else self.scaledblack)
            else:
                self.draw()

    def clicked(self, widget, event):
        if self.selection_row is not None and self.selection_column is not None:
            self.request.place_req(self.selection_row, self.selection_column)
            self.yourturn = False
            self.update_status_bar()

    def draw_affected_positions(self):
        if len(self.pending_drawings) == 0:
            self.update_status_bar()
            if self.toolbuttonShowHint.get_active():
                self.draw()
            return False
        else:
            player, [row, column] = self.pending_drawings.pop(0)
            print "pending", row, column
            self.draw_cell(row, column, self.scaledwhite if player == Player.WHITE else self.scaledblack)
            return True

    def update_status_bar(self):
        white_count, black_count = self.request.board_model.count_disks()
        if self.player == Player.WHITE:
            self.widgets.get_widget("labelWhiteCount").set_text("You (" + str(white_count) + " disks)")
            self.widgets.get_widget("labelBlackCount").set_text("Opponent (" + str(black_count) + " disks)")
        else:
            self.widgets.get_widget("labelWhiteCount").set_text("Opponent (" + str(white_count) + " disks)")
            self.widgets.get_widget("labelBlackCount").set_text("You (" + str(black_count) + " disks)")
        self.widgets.get_widget("labelTurn").set_text("Your turn" if self.yourturn else "Opponent's turn")

    def update_board(self, player, changed_positions):
        # self.pending_drawings += changed_positions
        self.pending_drawings += [[player, position] for position in changed_positions]
        print self.pending_drawings
        gobject.timeout_add(100, self.draw_affected_positions)
        self.drawingarea.window.set_cursor(None)
        self.selection_row = None
        self.selection_column = None
        self.selection_valid = False

    def set_ui_disconnected_state(self):
        self.connected = False
        self.widgets.get_widget("toolbuttonConnect").set_sensitive(True)
        self.widgets.get_widget("toolbuttonDisconnect").set_sensitive(False)
        self.widgets.get_widget("imagemenuitemConnect").set_sensitive(True)
        self.widgets.get_widget("imagemenuitemDisconnect").set_sensitive(False)
        self.widgets.get_widget("imagemenuitemDisconnect").set_sensitive(False)
        self.widgets.get_widget("toolbuttonShowHint").set_sensitive(False)
        self.widgets.get_widget("toolbuttonShowHint").set_active(False)

    def connection_ok(self, player):
        self.player = player
        self.connected = True
        self.widgets.get_widget("dialogConnecting").hide()
        self.widgets.get_widget("toolbuttonConnect").set_sensitive(False)
        self.widgets.get_widget("toolbuttonDisconnect").set_sensitive(True)
        self.widgets.get_widget("imagemenuitemConnect").set_sensitive(False)
        self.widgets.get_widget("imagemenuitemDisconnect").set_sensitive(True)
        self.widgets.get_widget("toolbuttonShowHint").set_sensitive(True)
        self.update_status_bar()

    def updated_board(self, player, changed_positions):
        self.update_board(player, changed_positions)

    def winner(self, winner):
        self.set_ui_disconnected_state()
        self.request.disconnect_req()
        self.request.shutdown_req()
        winner_dialog = None
        if winner == Player.EMPTY:
            winner_dialog = gtk.MessageDialog(
                parent=None, flags=gtk.DIALOG_MODAL, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK, message_format="Draw")
        else:
            if self.player == winner:
                winner_dialog = gtk.MessageDialog(parent=None, flags=gtk.DIALOG_MODAL,
                                                  type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK, message_format="You won!")
            else:
                winner_dialog = gtk.MessageDialog(parent=None, flags=gtk.DIALOG_MODAL,
                                                  type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK, message_format="You lost")

        winner_dialog.connect("response", lambda widget, response_id: winner_dialog.hide())
        winner_dialog.show()

    def turn(self):
        self.yourturn = True
        self.update_status_bar()

    def place_error(self):
        self.drawingarea.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.X_CURSOR))
        gobject.timeout_add(500, lambda: self.drawingarea.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.X_CURSOR)))

    def disconnection(self):
        self.widgets.get_widget("dialogConnecting").hide()
        if self.connected:
            self.connected = False
            self.set_ui_disconnected_state()
            dialog = gtk.MessageDialog(parent=None, flags=gtk.DIALOG_MODAL,
                                       type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK, message_format="Disconnected from server")
            dialog.connect("response", lambda widget, response_id: dialog.destroy() or True)
            dialog.show()

    # IGameClientInd implementation
    def connection_ok_ind(self, player):
        gobject.idle_add(self.connection_ok, player)

    def updated_board_ind(self, player, changed_positions):
        print "updated_board_ind", player, changed_positions
        gobject.idle_add(self.updated_board, player, changed_positions)

    def winner_ind(self, winner):
        gobject.idle_add(self.winner, winner)

    def turn_ind(self):
        gobject.idle_add(self.turn)

    def place_error_ind(self):
        gobject.idle_add(self.place_error)

    def disconnection_ind(self):
        gobject.idle_add(self.disconnection)
