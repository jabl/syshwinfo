#!/usr/bin/python

"""
Copyright (C) 2008 Janne Blomqvist

This file is part of syshwinfo.

    Syshwinfo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Syshwinfo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

Agent that uploads HW info to the server.
"""

SERVER = "http://diileri.hut.fi/~syshwdb/hwinforpc.cgi"

import xmlrpclib, syshwinfo

server = xmlrpclib.ServerProxy(SERVER)

try:
    server.puthwinfo(xmlrpclib.dumps((syshwinfo.getallhwinfo(),)))
except xmlrpclib.Error, v:
    print "ERROR", v
