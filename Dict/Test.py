#!/usr/bin/pythonTest
#
# dict functions Test
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
# Copyright 2004-2012 Rick Graves
#


def isDict( u ): return isinstance( u, dict )


def getHasKeyTester( d ):
    #
    """
    tester may be used by m@p or f!lter
    """
    #
    def isKeyInDict( k ): return k in d
    #
    return isKeyInDict


if __name__ == "__main__":
    #
    from Iter.AllVers   import iZip, iRange
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if isDict( lProblems ) or not isDict( {} ):
        #
        lProblems.append( 'isDict()' )
        #
    #
    dTest1      = dict( iZip( list( 'abcde' ), iRange(5) ) )
    dTest2      = dict( iZip( list( 'fghij' ), iRange(5) ) )
    #
    isKeyInD1 = getHasKeyTester( dTest1 )
    isKeyInD2 = getHasKeyTester( dTest2 )
    #
    if      not isKeyInD1( 'a' ) or \
            not isKeyInD2( 'j' ) or \
                isKeyInD1( 'j' ) or \
                isKeyInD2( 'a' ):
        #
        lProblems.append( 'getHasKeyTester()' )
        #

    #
    sayTestResult( lProblems )