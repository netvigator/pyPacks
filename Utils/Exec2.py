#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# exec for python 3, solve incompatibility with version 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# The GNU General Public License is available from:
#   The Free Software Foundation, Inc.
#   51 Franklin Street, Fifth Floor
#   Boston MA 02110-1301 USA
#
#   http://www.gnu.org/licenses/gpl.html
#
# Copyright 2014 Rick Graves
#



def doExec2( object, globals = None, locals = None ):
    #
    if globals is None and locals is None:
        #
        exec object
        #
    elif locals is None:
        #
        exec  object in globals
        #
    else:
        #
        exec object in globals, locals
        #



if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #


    #
    sayTestResult( lProblems )