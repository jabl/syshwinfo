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
    along with syshwinfo.  If not, see <http://www.gnu.org/licenses/>.

This file is the CGI version of the RPC server
"""

import DocXMLRPCServer
import hwinfoserver
import os.path

if not os.path.isfile(hwinfoserver.DBFILE):
    hwinfoserver.createdb(hwinfoserver.DBFILE)

handler = DocXMLRPCServer.DocCGIXMLRPCRequestHandler()
handler.register_introspection_functions()
handler.register_instance(hwinfoserver.HwInfoServer())

handler.handle_request()