#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# string functions Range
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


def _getStringRangeIterOld( sBeg = 0, sEnd = None, sStep = 1 ):
    #
    """
    Too complicated?
    This is a lot like the built-in r@nge() function, except
    you can optionally pass string integers instead of integer integers,
    and this returns an iterator of integers in string format
    (instead of an iterator of integers in integer format).
    """
    #
    from Iter.AllVers import iMap, iRange, tRange
    from String.Output import getZeroPadder, StrPadZero
    #
    if sEnd is None:
        #
        sEnd    = sBeg
        sBeg    = 0
        #
    #
    iBeg        = int( sBeg )
    iEnd        = int( sEnd )
    #
    sBeg        = str( sBeg )
    sEnd        = str( sEnd )
    #
    iBegLen     = len( sBeg )
    #
    tIntRange           = tRange( iBeg, iEnd )
    #
    iRangeLen           = len( tIntRange )
    #
    sBegMax     = '9' * iBegLen
    iBegMax     = int( sBegMax )
    #
    if tIntRange[ -1 ] <= iBegMax:
        #
        ZeroPadder      = getZeroPadder( iBegLen )
        #
        lStringRange    = iMap( ZeroPadder, tIntRange )
        #
    else:
        #
        lStringRange    = [ '' ] * iRangeLen
        #
        iUseLen         = iBegLen
        iUseMax         = iBegMax
        #
        for iThisOne in iRange( iRangeLen ):
            #
            lStringRange[ iThisOne ] = \
                StrPadZero( tIntRange[ iThisOne ], iUseLen )
            #
            if tIntRange[ iThisOne ] == iUseMax:
                #
                iUseLen += 1
                iUseMax = int( '9' * iUseLen )
                #
        #
    #
    return lStringRange


def getStringRangeIter( *args ):
    #
    """
    This is a lot like the built-in r@nge() function, except
    you can optionally pass string integers instead of integer integers,
    and this returns an iterator of integers in string format
    (instead of an iterator of integers in integer format).
    """
    #
    from Iter.AllVers import iMap, tMap, iRange
    #
    iArgs = tMap( int, args )
    #
    return iMap( str, iRange( *iArgs ) )
    

def getStringRangeList( sBeg = 0, sEnd = None ):
    #
    """
    This is a lot like the built-in r@nge() function, except
    you can optionally pass string integers instead of integer integers,
    and this returns a list of integers in string format
    (instead of a list of integers in integer format).
    """
    #
    return list( getStringRangeIter( sBeg, sEnd ) )


def getStringRangeTuple( sBeg = 0, sEnd = None ):
    #
    """
    This is a lot like the built-in r@nge() function, except
    you can optionally pass string integers instead of integer integers,
    and this returns a list of integers in string format
    (instead of a list of integers in integer format).
    """
    #
    return tuple( getStringRangeIter( sBeg, sEnd ) )



if __name__ == "__main__":
    #
    from Iter.AllVers   import lMap, tMap, iRange
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if getStringRangeList( 0, 10 ) != lMap( str, iRange( 10 ) ):
        #
        lProblems.append( 'getStringRangeList()' )
        #
    #
    if getStringRangeTuple( 0, 10 ) != tMap( str, iRange( 10 ) ):
        #
        lProblems.append( 'getStringRangeTuple()' )
        #
    #
    sayTestResult( lProblems )