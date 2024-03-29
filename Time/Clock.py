#!/home/rick/.local/bin/pythonTest
# -*- coding: utf-8 -*-
#
# time functions Clock
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
#   http://www.gnu.org/licenses/
#
# Copyright 2004-2023 Rick Graves
#

from time import gmtime, mktime

def getSecsSinceEpoch():
    #
    """This has a resolution of one second only!!!"""
    #
    #
    return int( mktime( gmtime() ) )


def getTupleGMT():
    #
    #
    return gmtime()






if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if getSecsSinceEpoch() < 1176815605:
        #
        lProblems.append( 'getSecsSinceEpoch()' )
        #
    if len( getTupleGMT() ) != 9:
        #
        lProblems.append( 'getTupleGMT()' )
        #
    #
    sayTestResult( lProblems )
