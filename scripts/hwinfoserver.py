#!/usr/bin/python

"""
Copyright (C) 2008, 2011 Janne Blomqvist

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


XML-RPC server writing HW info to a DB and returns the DB.
 
"""

DBFILE="syshw.sq3"

import datetime
import xmlrpclib

try:
    import sqlite3 # Python 2.5+
except ImportError:
    import pysqlite2 as sqlite3 # Python < 2.5 with python-sqlite2 package


def opendb(filename=DBFILE):
    """Open sqlite3 db"""
    return sqlite3.connect(
        filename, 
        detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def getdb():
    """Return the DB as a list of dicts"""
    try:
	conn = opendb()
    except:
        pass
    else:
        conn.row_factory = dict_factory
	c = conn.cursor()
        c.execute('''select * from syshw order by Hostname''')
        res = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        return res
    return []

def createdb(filename):
    """Create the sqlite DB"""
    conn = opendb(filename)
    c = conn.cursor()
    c.execute('''create table syshw (
Hostname text primary key,
Distro text,
DistroVersion text,
Kernel text,
Arch text,
CPU text,
MHz integer,
Mem_MiB integer,
Swap_MiB integer,
Disk_GB integer,
Graphics text,
MAC text,
Serial text,
System_manufacturer,
System_product_name,
Date timestamp
)''')
    conn.commit()
    c.close()
    conn.close()

def add_record(conn, hwrec):
    """insert or update record"""
    c = conn.cursor()
    rc = c.execute('''insert or replace into syshw (
hostname, arch, cpu, disk_GB, distro, distroversion,
graphics, kernel, mac, mhz, mem_MiB, swap_MiB, date, serial,
System_manufacturer, System_product_name)
values (:Hostname, :Arch, :CPU, :Disk_GB, :Distro,
:DistroVersion, :Graphics, :Kernel, :MAC, :MHz, :Mem_MiB,
:Swap_MiB, :Date, :Serial, :System_manufacturer, 
:System_product_name)''', hwrec)
    conn.commit()
    c.close()

class HwInfoServer:
    def puthwinfo(self, hwinfostr):
	"""Insert hw info into DB"""
	(hwinfot,meth) = xmlrpclib.loads(hwinfostr)
	hwinfo = hwinfot[0]
	# Append date before inserting
	hwinfo.update({'Date': datetime.datetime.now()})
	try:
	    conn = opendb()
        except:
            return False
        else:
	    add_record(conn, hwinfo)
            conn.close()
	return True

    def gethwinfo(self):
	"""Return the entire HW database"""
	return xmlrpclib.dumps((getdb(),))
 
if __name__ == '__main__':
    import os.path
    import time
    if not os.path.isfile(DBFILE):
        createdb(DBFILE)
    from DocXMLRPCServer import DocXMLRPCServer
    server = DocXMLRPCServer(("", 8000), logRequests=0)
    server.register_introspection_functions()
    server.register_instance(HwInfoServer())

    print time.asctime(), 'Application Starting.'
    server.serve_forever()
    print time.asctime(), 'Application Finishing.'
