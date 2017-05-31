#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Collection functions Filter
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
# Copyright 2004-2017 Rick Graves
#

from Collect.Test   import isEmpty
from Iter.AllVers   import iFilter, lFilter


def RemoveDupes( seq ):
    #
    """
    this tries three approaches, fastest (might not work) to slowest (always works).
    """
    #
    try:
        #
        return list( frozenset( seq ) )
        #
    except TypeError:
        #
        pass # not hashable
        #
    #
    lList = list( seq )
    #
    try:
        #
        lList.sort()
        #
    except TypeError:
        #
        pass
        #
    else:
        #
        return [ u for i, u in enumerate( lList )
                 if not i or u != lList[ i - 1 ] ]
        #
    #
    lOut = []
    #
    for u in seq:
        #
        if u not in lOut: lOut.append( u )
        #
    #
    return lOut



def RemoveDupesKeepOrder( lList ):
    #
    setThroAway = set( [] )
    #
    lOut    = []
    #
    for uThisItem in lList:
        #
        if not uThisItem in setThroAway:
            #
            lOut.append( uThisItem )
            #
            setThroAway.add( uThisItem )
            #
        #
    #
    return lOut



def DumpDupesAndEmpties( lLines ):
    #
    from String.Test   import isStringNotEmpty
    #
    return lFilter( isStringNotEmpty, RemoveDupes( lLines ) )




def DumpDupesAndEmptiesKeepOrder( lLines ):
    #
    from String.Test  import isStringNotEmpty
    #
    return lFilter( isStringNotEmpty, RemoveDupesKeepOrder( lLines ) )



def _cut2ndThenFilter1st( lFilterThese, lCutThese, iWantOutput ):
    #
    """
    lFilterThese & lCutThese should have the same items
    but in different order, such as best and fastest
    this is a methodology to select the best, fastest
    by eliminating the slowest and worst.
    First, some get cut off the end of lCutThese.
    If lCutThese is in speed order, the slowest would be cut.
    Then items from lFilterThese are returned,
    but only those remaining in lCutThese.
    So you run through lBest, lFastest once,
    then run through lFastest, lBest (reverse order)
    """
    #
    iKeepKeys           = ( len( lCutThese ) + iWantOutput ) // 2
    #
    lMadeTheCut         = lCutThese[ : iKeepKeys ]
    #
    setKeysCutEnd       = frozenset( lMadeTheCut )
    #
    def hasCutEndKey( uKey ): return uKey in setKeysCutEnd
    #
    lFiltered           = lFilter( hasCutEndKey, lFilterThese )
    #
    return lFiltered, lMadeTheCut




def getBestFastest( lBestOrder, lFastOrder, iWantOutput, iVerbose = 0 ):
    #
    """
    Say you have two lists of the same items,
    one in order of best to worst, the other in order of fastest to slowest.
    This returns the subset of iWantOutput items
    that results from eliminating items on the end of each list.
    """
    #
    global iVerbosity
    #
    iVerbosity = iVerbose
    #
    iTarget     = iWantOutput  + ( 0.05 * ( len( lBestOrder ) - iWantOutput ) )
    #
    while  len( lBestOrder ) > int( iTarget ):
        #
        lFastOrder, lBestOrder \
                = _cut2ndThenFilter1st( lFastOrder, lBestOrder, iWantOutput )
        #
        lBestOrder, lFastOrder \
                = _cut2ndThenFilter1st( lBestOrder, lFastOrder, iWantOutput )
        #
        #
    #
    lBestOrder          = lBestOrder[ : iWantOutput ]
    #
    return lBestOrder



def getOneItemListIfStr( lExpectList ):
    #
    if type( lExpectList ) == str:
        #
        sKeepItem = lExpectList
        #
        lExpectList  = []
        #
        lExpectList.append( sKeepItem )
        #
    #
    return list( lExpectList )


def getStringsWithSubstringInThisList( l, lSubs, bCaseSensitive = False ):
    #
    from String.Test import getHasSubstringTester
    #
    lLinkRel = []
    #
    for sLinkLinkText in lSubs:
        #
        isThisTextInThere   = getHasSubstringTester( sLinkLinkText, bCaseSensitive )
        #
        lLinkRel += iFilter( isThisTextInThere, l )
        #
    #
    return lLinkRel



def getListOfStrings( uInput ):
    #
    from Iter.Test      import isIterable
    from String.Test    import isStringAndNotEmpty
    #
    uReturn     = None
    #
    if type( uInput ) == str:
        #
        uReturn = [ uInput, ]
        #
    elif isIterable( uInput ):
        #
        uReturn = lFilter( isStringAndNotEmpty, uInput )
        #
    elif uInput is None:
        #
        uReturn = [ '' ]
        #
    #
    return uReturn





if __name__ == "__main__":
    #
    from string import digits
    from string import ascii_letters   as letters
    from string import ascii_uppercase as uppercase
    from string import ascii_lowercase as lowercase
    #
    from six            import print_ as print3
    #
    from Collect.Get    import getListFromNestedLists
    from Iter.AllVers   import iRange, lRange
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    def getSeq( i ): return lRange( i + 1 )
    #
    lTest   = getListFromNestedLists( [ getSeq( i ) for i in iRange( 10 ) ] )
    #
    lUniq   = RemoveDupes( lTest )
    #
    lUniq.sort()
    #
    if lUniq != [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
        #
        lProblems.append( 'RemoveDupes()' )
        #
    #
    lTest.reverse()
    #
    if RemoveDupesKeepOrder( lTest ) != [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]:
        #
        lProblems.append( 'RemoveDupesKeepOrder()' )
        #
    #
    lTest.append( None )
    #
    lNoDupes = DumpDupesAndEmpties( lTest )
    #
    lNoDupes.sort()
    #
    if lNoDupes != [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        #
        lProblems.append( 'DumpDupesAndEmpties()' )
        #
    if DumpDupesAndEmptiesKeepOrder( lTest ) != [9, 8, 7, 6, 5, 4, 3, 2, 1]:
        #
        lProblems.append( 'DumpDupesAndEmptiesKeepOrder()' )
        #
    #
    # letters + digits + random.shuffle()
    #
    sBest = 'FnZcjRIlOg6hKW7t9VNuBpJDYEvmk13Mdrb4zTSfo5XxALaHeUP0Gw2yQ8iqsC'
    #        ^ ^^^^^  ^^  ^^ ^^^    ^ ^^ ^^^^^^^^^
    #
    sFast = '9kb3Hj5Vf81PxcqoXiSyQDv2T7FgzZ6aLReIWUEGM4rdNtJwmChBlOuA0snpKY'
    #        ^^^^ ^ ^  ^  ^       ^^  ^^^^^^  ^ ^^ ^ ^^^^^
    #
    sBestFast = getBestFastest( sBest, sFast, 25 )
    #
    if list( sBestFast ) != list( 'FZcjRIg6W79VNDEvk13Mdrb4z' ):
        #
        print3( 'expected:', 'FZcjRIg6W79VNDEvk13Mdrb4z' )
        print3( 'actually:', sBestFast )
        lProblems.append( 'getBestFastest()' )
        #
    #
    #
    if      getOneItemListIfStr( iRange(10) ) != lRange(10) or \
            getOneItemListIfStr( digits     ) != [ digits ]:
        #
        print3( getOneItemListIfStr( iRange(10) ) )
        print3( getOneItemListIfStr( digits     ) )
        lProblems.append( 'getOneItemListIfStr()' )
        #
    #
    lLetters = [ letters[ i : i+4 ] for i in iRange( 0, 52, 4 ) ]
    #
    # ['abcd', 'efgh', 'ijkl', 'mnop', 'qrst', 'uvwx', 'yzAB',
    #  'CDEF', 'GHIJ', 'KLMN', 'OPQR', 'STUV', 'WXYZ']
    #
    lSubs0   = [ 'za', 'Bc', 'pQ' ]
    lSubs1   = [ 'zA', 'bc', 'PQ' ]
    #
    if      getStringsWithSubstringInThisList( lLetters, lSubs0 ) != \
                ['yzAB', 'abcd', 'OPQR'] or \
            getStringsWithSubstringInThisList( lLetters, lSubs0, 1 ) or \
            getStringsWithSubstringInThisList( lLetters, lSubs1 ) != \
                ['yzAB', 'abcd', 'OPQR']:
        #
        lProblems.append( 'getStringsWithSubstringInThisList()' )
        #
    if      getListOfStrings(       'abc'   ) != [ 'abc' ] or \
            getListOfStrings( list( 'abc' ) ) != [ 'a', 'b', 'c' ] or \
            getListOfStrings( None          ) != [ '' ]:
        #
        lProblems.append( 'getListOfStrings()' )
        #


    #
    sayTestResult( lProblems )