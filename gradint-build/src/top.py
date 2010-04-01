#!/usr/bin/env python
# -*- coding: utf-8 -*-

program_name = "gradint v0.9955 (c) 2002-2010 Silas S. Brown. GPL v3+."

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

if not sys.version_info[0]==2: # oh panic, someone's probably trying to run us on Py3k
    sys.stderr.write("Sorry, Gradint cannot run on Python "+repr(sys.version_info[0])+"\nPlease install a 2.x version of Python (must be 2.2+).\n")
    sys.exit(1)

# --------------------------------------------------------
