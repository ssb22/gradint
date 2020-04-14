#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   (Python 2 or Python 3, but more fully tested on 2)

program_name = "gradint v3.03 (c) 2002-20 Silas S. Brown. GPL v3+."

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

# Note: To make Gradint easier to package on all the platforms, all the main parts are in a single Python file.  In development however several different python files are used, which are then concatenated together to make the one file.  Comments indicate the start of the various component files in the main file.

progressFileHeader = "# -*- mode: python -*-\n# Do not add more comments - this file will be overwritten\n"

appTitle = "Language lesson"

import sys,os

if sys.version_info[0]>2:
    _map,_filter = map,filter
    def map(*args): return list(_map(*args))
    def filter(*args): return list(_filter(*args))
    from functools import cmp_to_key
    def sort(l,c): l.sort(key=cmp_to_key(c))
    raw_input,unichr,xrange = input,chr,range
    def chr(x): return unichr(x).encode('latin1')
    from subprocess import getoutput
    popenRB,popenWB = "r","w"
    def unicode(b,enc): return b.decode(enc)
else: # Python 2
    def sort(l,c): l.sort(c)
    popenRB,popenWB = "rb","wb"
    bytes = str
    try: from commands import getoutput
    except ImportError: pass
def readB(f,m=None):
    if hasattr(f,"buffer"): f=f.buffer # Python 3 non-"b" file
    if m: return f.read(m)
    else: return f.read() # no "None" in Python 2
def writeB(f,b):
    if hasattr(f,"buffer"): f=f.buffer # Python 3 non-"b" file
    f.write(b)
def B(x):
    if type(x)==bytes: return x
    try: return x.encode('utf-8')
    except: return x # maybe not a string
def LB(x):
    if type(x)==bytes: return x
    try: return x.encode('latin1')
    except: return x
def S(x):
    if type(x)==bytes and not bytes==str: return x.decode('utf-8')
    return x
def S2(s):
    try: return S(s)
    except: return s # coding errors OK in unavail, leave as byte-string

# --------------------------------------------------------
