#!/usr/bin/python

"""
Copyright (c) 2008, 2011, 2012 Janne Blomqvist

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


XML-RPC server writing HW info to a DB and returns the DB.
 
"""

DBFILE="syshw.sq3"

import datetime
import xmlrpclib

try:
    import sqlite3 # Python 2.5+
except ImportError:
    # Python < 2.5 with python-sqlite2 package
    from pysqlite2 import dbapi2 as sqlite3


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
