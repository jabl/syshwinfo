#!/usr/bin/python

"""
Copyright (C) 2006, 2007, 2008 Janne Blomqvist

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


Print out some data about hardware.

"""

version = 2008.3

import os, platform, socket, sys, csv, datetime

def meminfo():
    """Get the amount of memory and swap, Mebibytes"""
    f = open("/proc/meminfo")
    hwinfo = {}
    for line in f.readlines():
        meml = line.split()
        if (meml[0] == "MemTotal:"):
            mem = int(meml[1])
            hwinfo["Mem (MiB)"] = mem/1024
        elif (meml[0] == "SwapTotal:"):
            swap = int(meml[1])
            hwinfo["Swap (MiB)"] = swap/1024
    f.close()
    return hwinfo

def cpuinfo():
    """Get the cpu info"""
    f = open("/proc/cpuinfo")
    hwinfo = {}
    for line in f.readlines():
        cpul = line.split(":")
        name = cpul[0].strip()
        if (len(cpul) > 1):
            val = cpul[1].strip()
        if (name == "model name"):
            hwinfo["CPU"] = val
        elif (name == "cpu MHz"):
            hwinfo["MHz"] = int(round(float(val)))
    f.close()
    return hwinfo

def uname():
    """Get the architecture"""
    uname = os.uname()
    return {"Arch":uname[4], "Kernel":uname[2]}

def pcidata():
    """Get some pci data."""
    f = os.popen ("/sbin/lspci -m")
    pdata = {}
    for line in f.readlines():
        p = line.split("\"")
        name = p[1].strip()
        if (name == "Host bridge"):
            pdata["Chipset"] = p[3] + " " + p[5]
            pdata["Motherboard"] = p[7] + " " + p[9]
        elif (name == "VGA compatible controller"):
            pdata["Graphics"] = p[3] + " " + p[5]
    f.close()
    return pdata

def diskdata():
    """Get total disk size in GB."""
    p = os.popen("/bin/df -l -P")
    ddata = {}
    tsize = 0
    for line in p.readlines():
        d = line.split()
        if ("/dev/sd" in d[0] or "/dev/hd" in d[0] or "/dev/mapper" in d[0]):
            tsize = tsize + int(d[1])
    ddata["Disk (GB)"] = int(tsize)/1000000
    p.close()
    return ddata

def distro():
    """Get the distro and version."""
    d = platform.dist()
    dv = d[0] + " " + d[1]
    return {"Distro":d[0], "DistroVersion":d[1]}

def hostname():
    """Get hostname."""
    return {"Hostname":socket.gethostname()}

def getallhwinfo():
    """Get all the hw info."""
    hwinfo = meminfo()
    hwinfo.update(cpuinfo())
    hwinfo.update(uname())
    hwinfo.update(pcidata())
    hwinfo.update(distro())
    hwinfo.update(diskdata())
    hwinfo.update(hostname())    
    return hwinfo

def header_fields(h=None):
    """The order of the fields in the header."""
    hfields = ['Hostname', 'Distro', 'DistroVersion', 'Kernel', 'CPU', 'MHz', 'Arch', 'Mem (MiB)', 'Swap (MiB)', 'Disk (GB)', 'Motherboard', 'Chipset', 'Graphics']
    if h != None:
	if h.has_key('Date'):
	    hfields.append('Date')
    return hfields

def printheader(h=None):
    """Print the header for the CSV table."""
    writer = csv.writer(sys.stdout)
    writer.writerow(header_fields(h))

def printtable(h, header):
    """Print as a table."""
    hk = header_fields(h)
    if (header):
        printheader()
    #else:
    #    hk.remove('Hostname')
    writer = csv.DictWriter(sys.stdout, hk, extrasaction='ignore')
    if h.has_key('Date'):
        d = datetime.datetime.fromtimestamp(h['Date'])
        h['Date'] = d.isoformat()
    writer.writerow(h)

def agent(server="http://localhost:8000"):
    """Run in agent mode.

    This gathers data, and sends it to a server given by the server argument.

    """
    import xmlrpclib
    sp = xmlrpclib.ServerProxy(server)
    try:
        sp.puthwinfo(xmlrpclib.dumps((getallhwinfo(),)))
    except xmlrpclib.Error, v:
        print "ERROR occured: ", v

if __name__=="__main__":
    import pprint
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-t", "--table", dest="table",
                      action="store_true",
                      help="Write output as a CSV table")
    parser.add_option("-v", "--verbose", dest="verbose",
                      action="store_true",
                      help="Write output header and hostname for table")
    parser.add_option("-o", "--header", dest="header",
                      action="store_true",
                      help="Write only the table header.")
    parser.add_option("-V", "--version", dest="version",
                      action="store_true",
                      help="Print program version.")
    parser.add_option("-a", "--agent", dest="agent", action="store_true",
            help="Run in agent mode, send data to server.")
    parser.add_option("-s", "--server", dest="server", 
            help="Server to send results to when running in agent mode.")
    (options, args) = parser.parse_args()
    if (options.header):
        printheader()
    elif (options.table):
        printtable(getallhwinfo(), options.verbose)
    elif (options.version):
        print version
    elif (options.agent):
        if (options.server):
            agent(options.server)
        else:
            agent()
    else:
        pp = pprint.PrettyPrinter()
        pp.pprint(getallhwinfo())
