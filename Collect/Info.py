#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Collection functions Info
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

def getMaxLen( lList ):
    #
    from Iter.AllVers import iMap
    #
    def getLen( u ):
        #
        try:
            iLen = len( u )
        except:
            iLen = 0
        #
        return iLen
    #
    #
    return max( iMap( getLen, lList ) )




def getAllIndexes( lList, uValue ):
    #
    """
    Looks for uValue in lList, returns a list of indexes for each uValue found.
    """
    #
    lIndexes4Value  = []
    #
    if uValue in lList:
        #
        iIndex4ThisValue = lList.index( uValue )
        #
        lIndexes4Value.append( iIndex4ThisValue )
        #
        lGotMore    = []
        #
        if iIndex4ThisValue < len( lList ) - 1: # need to look in the rest of the list
            #
            # watch out! recursive call coming up!
            #
            lGotMore    = getAllIndexes( lList[ iIndex4ThisValue + 1 : ], uValue )
            #
        #
        if len( lGotMore ) > 0:
            #
            for iThisMore in iRange( len( lGotMore ) ):
                #
                lGotMore[ iThisMore ] += iIndex4ThisValue + 1
                #
            lIndexes4Value  += lGotMore
            #
        #
    #
    return lIndexes4Value


def getCumulativeLengths( lParts, iAddTo = 0, iStart = 0 ):
    #
    'pass lParts, iAddTo, iStart, returns Cumulative Lengths'
    #
    from Numb.Accumulate import getCumulativeTotals
    #
    return getCumulativeTotals( lParts, iAddTo, iStart, len )



def getCounts( l ):
    #
    '''pass a sequence
    returns a dictionary of counts

    do not use getDictOfCountsOffList in Dict.Numbs
    '''
    #
    dCounts = {}
    #
    for u in l:
        #
        dCounts[ u ] = 1 + dCounts.setdefault( u, 0 )
        #
    #
    return dCounts



if __name__ == "__main__":
    #
    lProblems = []
    #
    from string import digits
    from string import ascii_letters   as letters
    from string import ascii_lowercase as lowercase
    from random import shuffle, choice
    #
    from Iter.AllVers   import iRange
    from Utils.Result   import sayTestResult
    #
    sTest = digits + letters
    #
    lTest = list( sTest )
    #
    def getSome( i ):
        #
        lSome = []
        #
        while len( lSome ) < i:
            lSome.append( choice( lTest ) )
        #
        return lSome
    #
    lTest = [ getSome( i ) for i in iRange( 63 ) ]
    #
    [ shuffle( l ) for l in lTest ]
    #
    shuffle( lTest )
    #
    lTest = [ ''.join( l ) for l in lTest ]
    #
    if getMaxLen( lTest ) != 62:
        #
        lProblems.append( 'getMaxLen()' )
        #
    #
    lTest = [ digits[ : i ] for i in iRange( 11 ) ]
    #
    sLines = ''.join( lTest )
    #
    if getAllIndexes( sLines, '1' ) != [2, 4, 7, 11, 16, 22, 29, 37, 46]:
        #
        lProblems.append( 'getAllIndexes()' )
        #
    #
    t = ( 'a', 'ab', 'abc', 'abcd', 'abcde' )
    #
    if getCumulativeLengths( t ) != [ 1, 3, 6, 10, 15 ]:
        #
        lProblems.append( 'getCumulativeLengths()' )
        #
    #
    #
    lNumbs = []
    #
    for i in iRange(10):
        #
        lNumbs.extend( iRange(i) )
        #
    #
    if getCounts( lNumbs ) != \
            {   0: 9,
                1: 8,
                2: 7,
                3: 6,
                4: 5,
                5: 4,
                6: 3,
                7: 2,
                8: 1 }:
        #
        lProblems.append( 'getCounts()' )
        #
    #
    sayTestResult( lProblems )