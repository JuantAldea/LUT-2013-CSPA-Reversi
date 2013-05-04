#!/usr/bin/python
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
