=======================
syshwinfo release 2.1.1
=======================

This package contains a tool to find out information about a Linux system (OS
version, CPU, HD, etc.). The tool can be used directly or as a library. Also
supplied are a server and associated client agent that can be used to centrally
gather information about a number of clients.

Files included are:

``syshwinfo.py`` 
    The command-line tool and library to gather information about the system.
    Optionally can be run in agent mode where it sends the system information
    to a server rather than printing it to the screen.  Run it with the --help
    option to see usage instructions.

``hwinfoserver.py``
    XML-RPC server that listens for connections from agents and stores system
    information in a database.

``hwinforpc.cgi``
    CGI script for running hwinfoserver.py under a webserver.

``hwinfo.cgi``
    CGI script that queries the database and returns it in CSV format.


Installation
============

Run ``python setup.py install``, or just copy the files wherever
necessary. In order to use the server+agent system you can edit
hwinfoserver.py to set the DBFILE variable to point to where you want
to store the database (a single file in sqlite 3.x format). The
default is in the current directory where the server is run. Then run
the syshwinfo.py script in agent mode, optionally giving it the URL of
the server, e.g. ``syshwinfo.py -a -s
http://192.168.0.1/path/to/hwinforpc.cgi``. The default URL is
``http://localhost:8000``, which is also the URL when hwinfoserver.py
is started directly from the command line without a web server.
