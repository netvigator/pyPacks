#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# object functions Output
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
# Copyright 2020 Rick Graves
#
from io                     import StringIO

from pyPacks.Utils.Both2n3  import print3_n_2



def _getLinesForPrinting( uPrintThis, iLeft = 0, sBegEnd = '', lLines = [] ):
    #
    if isinstance( uPrintThis, dict ):
        #
        for k, v in uPrintThis.items():
            #
            oString = StringIO()
            #
            print3_n_2( '%s: %s' % ( k, v ),
                        beg = iLeft + 2,
                        file = oString )
            #
        #
        sLines = str( oString )
        #
        lLines = sLines.split( '\n' )
        #
        lLines[  0 ] = '{ ' + lLines[  0 ][  2 : ]
        lLines[ -1 ] =        lLines[ -1 ][ : -1 ] + ' }'
        #
        return lLines




def ObjectPrint( uPrintThis ):
    #
    lLines = _getLinesForPrinting(
                    uPrintThis, iLeft = 0, sBegEnd = '', lLines = [] )
    #
    #
    print( '\n'.join( lLines )


if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    dTest = dict( a = 1, b = 2, c = 3 )
    #
    sayTestResult( lProblems )
