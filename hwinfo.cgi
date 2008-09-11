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


CGI script to return the DB in CSV format
"""

import hwinfoserver
import syshwinfo

db = hwinfoserver.getdb()

print "Content-Type: text/csv"
print ""

if len(db) > 0:
    syshwinfo.printheader(db[0])

for ent in db:
    syshwinfo.printtable(ent, False)
