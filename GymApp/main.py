#! /usr/bin/python3
# -*- coding: utf-8 -*-
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from model import Model
from controller import Controller
from view import View

BASEDEDATOS = 'database.db'

if __name__ == "__main__":
    
    model = Model(BASEDEDATOS)
    Controller(View(), model)

    Gtk.main()