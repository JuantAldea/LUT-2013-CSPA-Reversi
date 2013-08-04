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

import threading
import pygtk
import gtk
pygtk.require("2.0")

from ReversiGUI import ReversiGUI

# gobject.threads_init()
gtk.gdk.threads_init()

if __name__ == "__main__":
    ui = ReversiGUI()
    ui.run()

    for thread in threading.enumerate():
        if thread is not threading.currentThread():
            thread.join()
