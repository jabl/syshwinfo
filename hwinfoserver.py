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


XML-RPC server writing HW info to a DB and returns the DB.
 
"""

DBFILE="/home/job/src/syshwrpc/syshw.db"

import time
import gdbm
import syshwinfo
import xmlrpclib
import cPickle as pickle

def getdb():
    """Return the DB as a list of dicts"""
    res = []
    try:
	db = gdbm.open(DBFILE, "r")
	k = db.firstkey()
	while k != None:
	    res.append(pickle.loads(db[k]))
	    k = db.nextkey(k)
    finally:
	db.close()
    return res

class HwInfoServer:
    def puthwinfo(self, hwinfostr):
	"""Insert hw info into DB"""
	(hwinfot,meth) = xmlrpclib.loads(hwinfostr)
	hwinfo = hwinfot[0]
	# Append date before inserting
	hwinfo.update({'Date': time.asctime()})
	hwinfos = pickle.dumps(hwinfo)
	res = False
	try:
	    db = gdbm.open(DBFILE, "c", 0600)
	    db[hwinfo["Hostname"]] = hwinfos
	    res = True
	finally:
	    db.close()
	return res

    def gethwinfo(self):
	"""Return the entire HW database"""
	return xmlrpclib.dumps((getdb(),))
 
if __name__ == '__main__':
    from DocXMLRPCServer import DocXMLRPCServer
    server = DocXMLRPCServer(("", 8000), logRequests=0)
    server.register_introspection_functions()
    server.register_instance(HwInfoServer())

    print time.asctime(), 'Application Starting.'
    server.serve_forever()
    print time.asctime(), 'Application Finishing.'
