#!/usr/bin/pythonTest
#
# Number functions Accumulate
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
# Copyright 2004-2011 Rick Graves
#


class AccumulatorClass( object ):
    #
    def __init__( self, iStart = 0 ):
        #
        self.iValue = iStart
        #
    def getCumulative( self, iMore ):
        #
        self.iValue += iMore
        #
        return self.iValue



def _ReturnParam( u ): return u



def getCumulativeTotals( lThisList, iAddTo = 0, iStart = 0, f = _ReturnParam ):
    #
    oAccumlator     = AccumulatorClass( iStart )
    #
    return [ oAccumlator.getCumulative( f( uMember ) + iAddTo )
             for uMember in lThisList ]



def getCumulativeIntegerTotals( lThisList, iAddTo = 0, iStart = 0 ):
    #
    return getCumulativeTotals( lThisList, iAddTo, iStart, int )



def getCumulativeFloatTotals( lThisList, iAddTo = 0, iStart = 0 ):
    #
    return getCumulativeTotals( lThisList, iAddTo, iStart, float )



if __name__ == "__main__":
    #
    from Iter.AllVers   import iRange
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if getCumulativeIntegerTotals( iRange(9) ) != [0,1,3,6,10,15,21,28,36]:
        #
        lProblems.append( 'getCumulativeIntegerTotals()' )
        #
    if getCumulativeFloatTotals( iRange(9) ) != \
            [0.0,1.0,3.0,6.0,10.0,15.0,21.0,28.0,36.0]:
        #
        lProblems.append( 'getCumulativeFloatTotals()' )
        #

    #
    sayTestResult( lProblems )