#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# string functions Split
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
'''
in general, splitting is fast
this module has some split utilities that can be useful
getIterPartsAndBothStarts is a true iterator but takes a RE find object
'''

from six            import print_ as print3

from String.Find import getFinder

class Success( Exception ): pass


def _getTextStartsAndSplitStarts( lSplit, sSplitOn ):
    #
    from Iter.AllVers import iRange
    #
    iSplitOnLen = len( sSplitOn )
    #
    iSplitLen   = len( lSplit )
    #
    lSplitBegs  = [ None ] * iSplitLen
    lTextBegs   = [ None ] * iSplitLen
    #
    iHere = 0
    #
    for i in iRange( iSplitLen ):
        #
        lTextBegs[ i ] = iHere
        #
        iHere += len( lSplit[ i ] ) 
        #
        lSplitBegs[ i ] = iHere
        #
        iHere += iSplitOnLen
        #
    #
    return lTextBegs, lSplitBegs




def getPartsIterAndBothStarts(
        s, sSplitOn, sLower = '',
        bNeedStarts = True, iMaxSplits = -1, bSplitLeft = True ):
    #
    # checked and pronounced OK 2012-04-18
    """
    may return an iterator instead of the fragments list
    say sOrig = 'abcdefg<table>hijklm<table>nopqrs<table>tuvwxyz'
    getPartsIterAndBothStarts( sOrig, '<table>' )
    returns
    ['abcdefg', 'hijklm', 'nopqrs', 'tuvwxyz'],
        [0, 14, 27, 40], [7, 20, 33, 47]
    WARNINGS!:
    1) list of string fragments will be a iterator, not the actual list
    2) last number in 2nd list is length of whole string!
    getPartsListAndBothStarts( sOrig, '<table>' )
    returns same except list for iterator
    """
    #
    # from copy       import copy
    #
    from Iter.AllVers   import iMap, iZip
    #
    lStartText  = []
    lStartSplit = []
    #
    sSplitOnLower   = sSplitOn.lower()
    #
    iStringLen      = len( s )
    #
    bPartsOK        = False
    #
    try:
        # split if possible
        #
        if sSplitOnLower == sSplitOn.upper():
            #
            if bSplitLeft:
                lParts  = s.split(  sSplitOn, iMaxSplits )
            else:
                lParts  = s.rsplit( sSplitOn, iMaxSplits )
            #
            raise Success # no alpha in sSplitOn
        #
        if len( sLower ) != iStringLen: # make sLower
            #
            sLower = s.lower()
            #
        #
        if bSplitLeft:
            lParts  = sLower.split(  sSplitOnLower, iMaxSplits )
        else:
            lParts  = sLower.rsplit( sSplitOnLower, iMaxSplits )
        #
        if len( lParts ) == 1:
            #
            lParts = [ s ]
            #
            raise Success # no sSplitOn in s
        #
    except Success:
        #
        bPartsOK = True # if Success was raised, lParts is right
        #
    #
    #
    #print 'bPartsOK:', bPartsOK
    if bNeedStarts or not bPartsOK:
        #
        lStartText, lStartSplit = _getTextStartsAndSplitStarts(
                                                    lParts, sSplitOn )
        #
    #
    if bPartsOK:
        #
        iterParts   = lParts
        #
    else:
        #
        def getFrag( t ): return s[ t[0] : t[1] ]
        #
        iterParts   = iMap( getFrag, iZip( lStartText, lStartSplit ) )
        #
    #
    # WARNING! last number in lStartSplit is length of whole string!
    #
    return iterParts, lStartText, lStartSplit


_oFindVariableLenPattern = getFinder( '\*|\+|\||\?|\{\d+,\d*\}' )




def __getListsPartsAndBothStarts( s, uSplitOn ):
    #
    """
    say sOrig = 'abcdefg<table>hijklm<table>nopqrs<table>tuvwxyz'
    getListsPartsAndBothStarts( sOrig, getFinder( '<table>' ) )
    returns
    ['abcdefg', 'hijklm', 'nopqrs', 'tuvwxyz'],
        [0, 14, 27, 40],
        [7, 20, 33, 47]
    WARNING:
    last number in 2nd list is length of whole string!
    """
    #
    from six            import next as getNext
    #
    from Iter.AllVers   import iRange
   #from Utils.Both2n3  import getNext
    #
    if isinstance( uSplitOn, str ):
        #
        bSplitOnStr = True
        #
        bVariableSplitOn = False
        #
        sSplitOn = uSplitOn
        #
        lParts = s.split( sSplitOn )
        #
    else:
        #
        bSplitOnStr = False
        #
        oFinder = uSplitOn
        #
        sPattern = oFinder.pattern
        #
        bVariableSplitOn = _oFindVariableLenPattern.findall( sPattern )
        #
        lParts = oFinder.split( s )
        #
    #
    iPartsLen = len( lParts )
    #
    lStartText  = [ 0 ] * iPartsLen
    lStartSplit = [ 0 ] * iPartsLen
    #
    if iPartsLen  > 1:
        #
        if bSplitOnStr:
            #
            iSplitOnLen = len( sSplitOn )
            #
            def getLen( u ): return iSplitOnLen
            #
            arg = None
            #
        else:
            #
            iterSplitOn = oFinder.finditer( s )
            #
            arg = iterSplitOn
            #
            if bVariableSplitOn:
                #
                def getLen( iterSplitOn ):
                    return len( getNext( iterSplitOn ).group(0) )
                #
            else:
                #
                iSplitOnLen = len( getNext( iterSplitOn ).group(0) )
                #
                def getLen( u ): return iSplitOnLen
                #
        #
        for i in iRange( iPartsLen - 1 ):
            #
            lStartText[  i+1 ] = (
                lStartText[ i ] + len( lParts[ i ] ) + getLen( arg ) )
            lStartSplit[ i   ] = (
                lStartText[ i ] + len( lParts[ i ] ) )
            #
            #
        #
        lStartSplit[ -1 ] = len( s )
        #
    #
    #if lStartText and not lParts[  0 ]: del lStartText[  0 ]
    #if lStartText and not lParts[ -1 ]: del lStartText[ -1 ]
    #
    return lParts, lStartText, lStartSplit




def _getListsPartsAndBothStarts( s, oFinder ):
    #
    """
    say sOrig = 'abcdefg<table>hijklm<table>nopqrs<table>tuvwxyz'
    getListsPartsAndBothStarts( sOrig, getFinder( '<table>' ) )
    returns
    ['abcdefg', 'hijklm', 'nopqrs', 'tuvwxyz'],
        [0, 14, 27, 40],
        [7, 20, 33, 47]
    WARNING:
    last number in 2nd list is length of whole string!
    """
    #
    from six            import next as getNext
    #
    from Iter.AllVers   import iRange
   #from Utils.Both2n3  import getNext
    #
    sPattern = oFinder.pattern
    #
    bVariableSplitOn = _oFindVariableLenPattern.findall( sPattern )
    #
    lParts = oFinder.split( s )
    #
    iPartsLen = len( lParts )
    #
    lStartText  = [ 0 ] * iPartsLen
    lStartSplit = [ 0 ] * iPartsLen
    #
    if iPartsLen  > 1:
        #
        iterSplitOn = oFinder.finditer( s )
        #
        arg = iterSplitOn
        #
        if bVariableSplitOn:
            #
            def getLen( iterSplitOn ):
                return len( getNext( iterSplitOn ).group(0) )
            #
        else:
            #
            iSplitOnLen = len( getNext( iterSplitOn ).group(0) )
            #
            def getLen( u ): return iSplitOnLen
            #
        #
        for i in iRange( iPartsLen - 1 ):
            #
            lStartText[  i+1 ] = (
                lStartText[ i ] + len( lParts[ i ] ) + getLen( arg ) )
            lStartSplit[ i   ] = (
                lStartText[ i ] + len( lParts[ i ] ) )
            #
            #
        #
        lStartSplit[ -1 ] = len( s )
        #
    #
    #if lStartText and not lParts[  0 ]: del lStartText[  0 ]
    #if lStartText and not lParts[ -1 ]: del lStartText[ -1 ]
    #
    return lParts, lStartText, lStartSplit



def getIterPartsAndBothStarts( s, oFinder ):
    #
    """
    pass a string and a RE finder object
    returns iterator
    say sOrig = 'abcdefg<table>hijklm<table>nopqrs<table>tuvwxyz'
    list( getIterPartsAndBothStarts( sOrig, getFinder( '<table>' ) ) )
    returns
    [ ('abcdefg',  0,  7),
      ('hijklm',  14, 20),
      ('nopqrs',  27, 33),
      ('tuvwxyz', 40, 47) ]
    WARNING:
    last number in last tuple is length of whole string!
    """
    #
    from six            import next as getNext
    #
   #from Utils.Both2n3  import getNext
    #
    iterSplitOn = oFinder.finditer( s )
    #
    iPartStart  = 0
    #
    for oMatch in iterSplitOn:
        #
        # iSplitOnLen = len( oMatch.group(0) )
        #
        iBeg = oMatch.start()
        iEnd = oMatch.end()
        #
        yield s[ iPartStart : iBeg ], iPartStart, iBeg
        #
        iPartStart = iEnd
        #
    #
    yield s[ iEnd : ], iEnd, len( s )



def getListsPartsAndBothStarts( s, oFinder ):
    #
    from Collect.Get import unZip
    #
    return unZip( getIterPartsAndBothStarts( s, oFinder ) )


def getListsSplitsAndSplitEnds( s, uSplitOn ):
    #
    lParts, lStartText, lStartSplit = getListsPartsAndBothStarts( s, uSplitOn )
    #
    return lParts, lStartSplit



def getIterSplitsAndSplitEnds( s, oFinder ):
    #
    iterPartsAndBothStarts = getIterPartsAndBothStarts( s, oFinder )
    #
    for sPart, iStart, iSplit in iterPartsAndBothStarts:
        #
        yield sPart, iSplit



def getListsSplitsAndStarts( s, uSplitOn ):
    #
    lParts, lStartText, lStartSplit = getListsPartsAndBothStarts( s, uSplitOn )
    #
    return lParts, lStartText



def getIterSplitsAndStarts( s, oFinder ):
    #
    iterPartsAndBothStarts = getIterPartsAndBothStarts( s, oFinder )
    #
    for sPart, iStart, iSplit in iterPartsAndBothStarts:
        #
        yield sPart, iStart



def getPartsListAndBothStarts( s, sSplitOn, sLower = '', iMaxSplits = -1 ):
    #
    """
    say sOrig = 'abcdefg<table>hijklm<table>nopqrs<table>tuvwxyz'
    getPartsListAndBothStarts( sOrig, '<table>' )
    returns
    ['abcdefg', 'hijklm', 'nopqrs', 'tuvwxyz'],
        [0, 14, 27, 40], [7, 20, 33, 47]
    compare getPartsIterAndStarts( sOrig, '<table>' )
    """
    #
    oParts, lStartText, lStartSplit = getPartsIterAndBothStarts(
                                            s, sSplitOn, sLower, iMaxSplits )
    #
    return list( oParts ), lStartText, lStartSplit



def getPartsIterAndStarts( s, sSplitOn, sLower = '', iMaxSplits = -1 ):
    #
    """
    may return an iterator instead of the fragments list
    say sOrig = 'abcdefg<table>hijklm<table>nopqrs<table>tuvwxyz'
    getPartsIterAndStarts( sOrig, '<table>' )
    returns
    ['abcdefg', 'hijklm', 'nopqrs', 'tuvwxyz'], [0, 14, 27, 40]
    WARNING!:
    list of string fragments will be a iterator, not the actual list
    compare:
    getPartsListAndStarts( sOrig, '<table>' )
    returns
    ['abcdefg', 'hijklm', 'nopqrs', 'tuvwxyz'], [7, 20, 33, 47]
    """
    #
    oParts, lStartText, lStartSplit = getPartsIterAndBothStarts(
                                            s, sSplitOn, sLower, iMaxSplits )
    #
    return oParts, lStartText



def getPartsListAndStarts( s, sSplitOn, sLower = '' ):
    #
    """
    say sOrig = 'abcdefg<table>hijklm<table>nopqrs<table>tuvwxyz'
    getPartsListAndStarts( sOrig, '<table>' )
    returns
    ['abcdefg', 'hijklm', 'nopqrs', 'tuvwxyz'], [0, 14, 27, 40]
    """
    #
    oParts, lStartText, lStartSplit = getPartsIterAndBothStarts(
                                            s, sSplitOn, sLower )
    #
    return list( oParts ), lStartText



def getSplitsIterAndSplitEnds( s, sSplitOn, sLower = '', iMaxSplits = -1 ):
    #
    """
    returns a iterator instead of the fragments list
    say sOrig = 'abcdefg<table>hijklm<table>nopqrs<table>tuvwxyz'
    map( list, getSplitsIterAndSplitEnds( sOrig, '<table>' ) )
    returns
    ['abcdefg', 'hijklm', 'nopqrs', 'tuvwxyz'], [7, 20, 33, 47]
    WARNING!:
    list of string fragments will be a iterator, not the actual list
    """
    #
    oParts, lStartText, lStartSplit = getPartsIterAndBothStarts(
                                            s, sSplitOn, sLower, iMaxSplits )
    #
    return oParts, lStartSplit




def getSplitsListAndSplitEnds( s, sSplitOn, sLower = '' ):
    #
    oParts, lEnds = getSplitsIterAndSplitEnds( s, sSplitOn, sLower )
    #
    return list( oParts ), lEnds


def getSplitEnds( s, sSplitOn, sLower = '' ):
    #
    """
    may return an iterator instead of the fragments list
    say sOrig = 'abcdefg<table>hijklm<table>nopqrs<table>tuvwxyz'
    getSplitsIterAndSplitEnds( sOrig, '<table>' )
    returns
    ['abcdefg', 'hijklm', 'nopqrs', 'tuvwxyz'], [7, 20, 33, 47]
    note last member of lEnds is length of string
    """
    #
    oParts, lEnds = getSplitsIterAndSplitEnds( s, sSplitOn, sLower )
    #
    return lEnds



def getListSplitEnds( s, uSplitOn ):
    #
    """
    may return an iterator instead of the fragments list
    say sOrig = 'abcdefg<table>hijklm<table>nopqrs<table>tuvwxyz'
    getSplitsIterAndSplitEnds( sOrig, '<table>' )
    returns
    ['abcdefg', 'hijklm', 'nopqrs', 'tuvwxyz'], [7, 20, 33, 47]
    """
    #
    lParts, lStartText, lStartSplit = getListsPartsAndBothStarts( s, uSplitOn )
    #
    return lStartSplit


def getPartsIterAndPositions( s, sSplitOn, sLower = '', iMaxSplits = -1 ):
    #
    """
    returns a iterator instead of the fragments list
    say sOrig = 'abcdefg<table>hijklm<table>nopqrs<table>tuvwxyz'
    map( list, getPartsIterAndPositions( sOrig, '<table>' ) )
    returns
    ['abcdefg', 'hijklm', 'nopqrs', 'tuvwxyz'], [7, 20, 33, 47]
    WARNING!:
    list of string fragments will be a iterator, not the actual list
    compare:
    getPartsListAndPositions( sOrig, '<table>' )
    returns
    ['abcdefg', 'hijklm', 'nopqrs', 'tuvwxyz'], [7, 20, 33, 47]
    """
    #
    oParts, lStartText, lStartSplit = getPartsIterAndBothStarts(
                                            s, sSplitOn, sLower, iMaxSplits )
    #
    return oParts, lStartSplit


def getPartsListAndPositions( s, sSplitOn, sLower = '' ):
    #
    '''
    say sOrig = 'abcdefg<table>hijklm<table>nopqrs<table>tuvwxyz'
    getPartsListAndPositions( sOrig, '<table>' )
    returns
    ['abcdefg', 'hijklm', 'nopqrs', 'tuvwxyz'], [7, 20, 33, 47]
    '''
    oParts, lStartSplit = getPartsIterAndPositions( s, sSplitOn, sLower )
    #
    return list( oParts ), lStartSplit





def getSplitWithSplitOns( s, oFinder ):
    #
    '''
    for this to work,
    oFinder must contain one and only one single group for the whole match
    make sure your finder is working as intended!
    '''
    #
    return oFinder.split( s )



def getPartsAndPositionsUseFinder( s, uSplitOn ):
    #
    '''
    say sOrig = 'abcdefg<table>hijklm<table>nopqrs<table>tuvwxyz'
    getPartsAndPositionsUseFinder( sOrig, oFinder )
    returns
    ['abcdefg', 'hijklm', 'nopqrs', 'tuvwxyz'], [7, 20, 33, 47]
    '''
    #
    lParts, lStartText, lStartSplit = getListsPartsAndBothStarts( s, uSplitOn )
    #
    return lParts, lStartSplit



def getCharPositions( s, sSplitOn, sLower = '' ):
    #
    """
    returns a list of the positions sSplitOn in s
    l = getCharPositions( s, sSplitOn )
    
    say sOrig = 'abcdefg<table>hijklm<table>nopqrs<table>tuvwxyz'
    getCharPositions( sOrig, '<table>' )
    returns [7, 20, 33]
    getPartsIterAndPositions( sOrig, '<table>' )
    ['abcdefg', 'hijklm', 'nopqrs', 'tuvwxyz'], [7, 20, 33, 47]
    compare:
    getPartsIterAndStarts( sOrig, '<table>' )
    returns
    ['abcdefg', 'hijklm', 'nopqrs', 'tuvwxyz'], [0, 14, 27, 40]
    compare:
    getSplitEnds( sOrig, '<table>' )
    returns
    [7, 20, 33, 47]
    """
    #
    oParts, lStartText, lStartSplit = getPartsIterAndBothStarts(
                                            s, sSplitOn, sLower )
    #
    if lStartSplit: del lStartSplit[ -1 ]
    #
    return lStartSplit






def getCharPositionsUseFinder( s, uSplitOn ):
    #
    """
    say sOrig = 'abcdefg<table>hijklm<table>nopqrs<table>tuvwxyz'
    getCharPositionsUseFinder( sOrig, oFinder )
    returns
    ['abcdefg', 'hijklm', 'nopqrs', 'tuvwxyz'], [7, 20, 33, 47]
    compare:
    getPartsIterAndStarts( sOrig, '<table>' )
    returns
    ['abcdefg', 'hijklm', 'nopqrs', 'tuvwxyz'], [0, 14, 27, 40]
    compare:
    getSplitEnds ( sOrig, '<table>' )
    returns
    [7, 20, 33, 47]
    """
    #
    lParts, lStartText, lStartSplit = getListsPartsAndBothStarts( s, uSplitOn )
    #
    return lStartSplit



def iterSplitC(
        s,
        sSplitOn    = '',
        sLower      = '',
        iMaxSplits  = -1,
        bSplitLeft  = True ):
    #
    """
    may return an iterator for the fragment list, or just the list
    Like split, except not case sensitive.
    """
    #
    oParts, l1, l2 = getPartsIterAndBothStarts(
                        s, sSplitOn,
                        sLower      = sLower,
                        bNeedStarts = False,
                        iMaxSplits  = iMaxSplits,
                        bSplitLeft  = bSplitLeft )
    #
    return oParts




def SplitC( s, sSplitOn = '', sLower = '', iMaxSplits = -1, bSplitLeft = True ):
    #
    """
    Like split, except not case sensitive.
    """
    #
    return list( iterSplitC(
                    s, sSplitOn,
                    sLower      = sLower,
                    iMaxSplits  = iMaxSplits,
                    bSplitLeft  = bSplitLeft ) )


def SplitRightC( s, sSplitOn = '', sLower = '', iMaxSplits = -1 ):
    #
    return SplitC( s, sSplitOn, sLower, iMaxSplits, bSplitLeft = False )




def SplitRegular( s, sSplitOn = None, sLower = '', iMaxSplits = -1 ):
    #
    """
    Exactly like split, except wrapped to be plug-compatible with SplitC.
    """
    #
    return s.split( sSplitOn, iMaxSplits )



def SplitRight( s, sSplitOn = None, sLower = '', iMaxSplits = -1 ):
    #
    """
    Exactly like rsplit, except wrapped to be plug-compatible with SplitC.
    """
    #
    return s.rsplit( sSplitOn, iMaxSplits )



def iterSplit( s, oFinder ):
    #
    iterSplitOn = oFinder.finditer( s )
    #
    iPartStart  = 0
    iEnd        = len( s )
    #
    for oMatch in iterSplitOn:
        #
        # iSplitOnLen = len( oMatch.group(0) )
        #
        iBeg = oMatch.start()
        iEnd = oMatch.end()
        #
        yield s[ iPartStart : iBeg ]
        #
        iPartStart = iEnd
        #
    #
    yield s[ iEnd : ]
    



def _origGetTextSplitHere( sText, lSplits, iDrop = 0 ):
    #
    # Here comes in as lSplits, a list of split positions
    #
    lParts      = [''] * ( len( lSplits ) + 1 )
    #
    iLastSplit  = - iDrop
    #
    iIndex      = -1
    #
    for iIndex, iSplit in enumerate( lSplits ):
        #
        lParts[ iIndex ] = sText[ iLastSplit + iDrop : iSplit ]
        #
        iLastSplit  = iSplit
        #
    #
    if iIndex >= 0:
        #
        lParts[ iIndex + 1 ] = sText[ iLastSplit + iDrop : ]
    #
    return lParts



def getTextSplitHere( sText, lSplits, iDrop = 0 ):
    #
    from Iter.Get   import getSequencePairsThisWithNext as getThisWithNext
    #
    lSplitParts     = list( lSplits )
    #
    lSplitParts[ 0 : 0 ] = [ -iDrop ]
    #
    if lSplits and lSplits[ -1 ] < len( sText ):
        #
        lSplitParts.append( len( sText ) )
        #
    #
    for ( iBeg, iEnd ) in getThisWithNext( lSplitParts ):
        #
        yield sText[ iBeg + iDrop : iEnd ]



def getSplitButNotIfQuoted( s, sSplitOn ):
    #
    '''
    split this on commas:
    '"Mattia Melocchi, Macom srl" <mattia@macomsrl.it>, "Yipin Appliances Ltd" <zhyipin@163.com>'
    should be split in two on right comma only;
    i.e., ignore the first comma, the one within "Mattia Melocchi, Macom srl"
    '''
    #
    from Collect.Query  import get1stThatMeets
    from Iter.AllVers   import lMap
    from Iter.Get       import iRevRange
    from Iter.Get       import getSequencePairsThisWithNext as getThisWithNext
    from Numb.Test      import isOdd
    #
    Finished = Success
    #
    lParts = s.split( sSplitOn )
    #
    try:
        #
        if len( lParts ) == 1:              raise Finished
        #
        if not ( '"' in s or "'" in s ):    raise Finished
        #
        lCountSingle = [ s.count( "'" ) for s in lParts ]
        lCountDouble = [ s.count( '"' ) for s in lParts ]
        #
        bGotOddSingle = get1stThatMeets( lCountSingle, isOdd )
        bGotOddDouble = get1stThatMeets( lCountDouble, isOdd )
        #
        if not ( bGotOddSingle or
                 bGotOddDouble ):           raise Finished
        #
        iterPairs = getThisWithNext( iRevRange( len( lParts ) ) )
        #
        tDidBackTo = len( lParts )
        #
        for iRight, iLeft in iterPairs:
            #
            if iRight >= tDidBackTo: continue
            #
            bMergeSingle = (
                    bGotOddSingle and
                    isOdd( lCountSingle[ iRight ] ) and
                    get1stThatMeets( lCountSingle[ : iRight ], isOdd ) )
            #
            bMergeDouble = (
                    bGotOddDouble and
                    isOdd( lCountDouble[ iRight ] ) and
                    get1stThatMeets( lCountDouble[ : iRight ], isOdd ) )
            #
            if bMergeSingle or bMergeDouble:
                #
                if bMergeDouble:
                    #
                    lCount = lCountDouble
                    #
                else:
                    #
                    lCount = lCountSingle
                    #
                #
                lGotQuote = lMap( isOdd, lCount[ : iRight ] )
                lGotQuote.reverse()
                iJoinBackTo = len( lGotQuote ) - lGotQuote.index( 1 ) - 1
                #
                lParts[ iJoinBackTo ] = sSplitOn.join( lParts[ iJoinBackTo : iRight + 1 ] )
                #
                del lParts[ iJoinBackTo + 1 : iRight + 1 ]
                #
                tDidBackTo = iJoinBackTo
            #
        #
    except Finished:
        #
        pass
        #
    #
    return lParts



def _getPartitioned( sHaystack, sNeedle, bRFind = False ):
    #
    '''
    string method str.partition() was new in 2.5

    Split the string at the first occurrence of sep, 
    and return a 3-tuple containing the part before the separator, 
    the separator itself, and the part after the separator. 
    If the separator is not found, 
    return a 3-tuple containing the string itself, 
    followed by two empty strings.
    '''
    #
    if bRFind:
        #
        iIndex = sHaystack.rfind( sNeedle )
        #
    else:
        #
        iIndex = sHaystack.find( sNeedle )
        #
    #
    if iIndex == -1:
        #
        t = ( sHaystack, '', '' )
        #
    else:
        #
        iNeedleEnd = iIndex + len( sNeedle )
        #
        t = ( sHaystack[            : iIndex     ],
              sHaystack[ iIndex     : iNeedleEnd ],
              sHaystack[ iNeedleEnd :            ] )
        #
    #
    return t


def _getRPartitioned( sHaystack, sNeedle ):
    #
    '''
    string method str.rpartition() was new in 2.5

    Split the string at the last occurrence of sep, 
    and return a 3-tuple containing the part before the separator, 
    the separator itself, and the part after the separator. 
    If the separator is not found, 
    return a 3-tuple containing two empty strings, 
    followed by the string itself.
    '''
    #
    return _getPartitioned( sHaystack, sNeedle, bRFind = True )


try:
    #
    'abc'.partition( 'b' )
    #
    def getPartitioned( sHaystack, sNeedle ):
        return sHaystack.partition( sNeedle )
    #
    def getRPartitioned( sHaystack, sNeedle ):
        return sHaystack.rpartition( sNeedle )
    #
except AttributeError:
    #
    getPartitioned  = _getPartitioned
    getRPartitioned = _getRPartitioned
    #



def getSplitAndStrip( s, uSplitOn = ',' ):
    #
    from Iter.AllVers   import tMap
    from String.Get     import getStripped
    #
    if isinstance( uSplitOn, str ):
        if uSplitOn.upper() == uSplitOn.lower():
            lParts = s.split( uSplitOn )
        else:
            lParts = iterSplitC( s, uSplitOn )
    else:
        lParts = uSplitOn .split( s )
    #
    return tMap( getStripped, lParts )



def getRemoved( s, sRemove ):
    #
    tParts = getSplitAndStrip( s, sRemove )
    #
    sRemoved = ' '.join( tParts )
    #
    return sRemoved.strip()



def getWhiteCleaned( s ):
    #
    from Iter.AllVers import iFilter
    #
    iParts = iFilter( bool, s.split() )
    #
    return ' '.join( iParts )




def _chopViaSplit( sHaystack, sNeedle ):
    #
    lParts = sHaystack.split( sNeedle, 1 )
    #
    return lParts[ -1 ]


def _chopViaRfind( sHaystack, sNeedle ):
    #
    iLoc = sHaystack.rfind( sNeedle )
    #
    if iLoc > -1:
        #
        sHaystack = sHaystack[ : iLoc ]
        #
    #
    return sHaystack


def _chopTimeTrial():
    #
    from String.Text4Tests import sGoogleQuerResult_Chrome as sHTML
    from Utils.TimeTrial   import TimeTrial
    #
    TimeTrial( _chopViaSplit, sHTML, '<' )
    TimeTrial( _chopViaRfind, sHTML, '<' )

# _chopViaRfind is somewhat faster,
# implemented by getChoppedOff in String.Dumpster



def _PartsAndStartsTimeTrial():
    #
    from Collect.Get        import unZip
    from String.Text4Tests  import sGoogleQuerResult_Chrome as sHTML
    from Utils.TimeTrial    import TimeTrial
    #
    def getListLists( s, sSplitOn, sLower = '' ):
        #
        iterParts, lStartText, lStartSplit = getPartsIterAndBothStarts(
                                                        s, sSplitOn, sLower )
        #
        return list( iterParts ), lStartText, lStartSplit
    #
    oFinder = getFinder( '<script.' )
    #
    def getIterLists( s, oFinder ):
        #
        return tuple( getIterPartsAndBothStarts( s, oFinder ) )
    #
    def getReLists( s, oFinder ):
        #
        return tuple( _getListsPartsAndBothStarts( s, oFinder ) )
    #
    sHtmlLower = sHTML.lower()
    #
    print3( '\ngetPartsIterAndBothStarts (the easier way) ...' )
    #
    TimeTrial( getListLists, sHTML, '<script', sHtmlLower )
    #
    #print3( '\ngetIterLists(the iter way) ...' )
    ##
    #TimeTrial( getIterLists, sHTML, oFinder )
    ##
    #print3( '\n_getListsPartsAndBothStarts (the re way) ...' )
    ##
    #TimeTrial( getReLists, sHTML, oFinder )


if __name__ == "__main__":
    #
    from string import digits
    from string import ascii_letters   as letters
    from string import ascii_lowercase as lowercase
    from string import ascii_uppercase as uppercase
    #
    from Collect.Get    import unZip
    from Dict.Get       import getItemList
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    sTest0  = digits + lowercase + digits + uppercase + digits
    sTest1  = digits + lowercase + digits + lowercase + digits
    #
    lDigitsTriple   = ['0123456789', '0123456789', '0123456789']
    lAlphaSandwich  = ['', 'abcdefghijklmnopqrstuvwxyz',
                           'ABCDEFGHIJKLMNOPQRSTUVWXYZ', '']
    #
    sOrig0  = 'abcdefg<table>hijklm<table>nopqrs<table>tuvwxyz'
    sOrig1  = 'abcdefg<TABLE>hijklm<TABLE>nopqrs<TABLE>tuvwxyz'
    sOrig2  = 'abcdefg<tAbLe>hijklm<TaBlE>nopqrs<tAbLe>tuvwxyz'
    #
    lTableFrags     = ['abcdefg', 'hijklm', 'nopqrs', 'tuvwxyz']
    lTextAt         = [0, 14, 27, 40]
    lSplitAt        = [7, 20, 33, 47]
    #
    oFinderLowerC   = getFinder( lowercase )
    oFinderDigits   = getFinder( digits    )
    oFinderTableTag = getFinder( '<table>' )
    #
    #
    oOut, lBegText0, lBegSplits0 = getPartsIterAndBothStarts( sTest0, lowercase )
    #
    if ( list( oOut ), lBegText0, lBegSplits0 ) != \
            ( lDigitsTriple,  [0, 36, 72], [10, 46, 82] ):
        #
        print3( list(oOut), lBegText0, lBegSplits0 )
        lProblems.append( 'getPartsIterAndBothStarts( sTest0, lowercase )' )
        #
    #
    lOut, lBegText1, lBegSplits1 = getListsPartsAndBothStarts(
                                    sTest0, oFinderLowerC )
    #
    if ( lOut, lBegText1, lBegSplits1 ) != \
            ( lDigitsTriple,  [0, 36, 72], [10, 46, 82] ):
        #
        #print getListsPartsAndBothStarts( sTest0, oFinderLowerC )
        lProblems.append( 'getListsPartsAndBothStarts() identical split ons' )
        #
    #
    oOut, lBegText0, lBegSplits0 = getPartsIterAndBothStarts( sTest0, lowercase )
    #
    if ( ( list( oOut ), lBegText0, lBegSplits0 ) !=
         ( lOut, lBegText1, lBegSplits1 ) ):
        #
        #print getListsPartsAndBothStarts( sTest0, oFinderLowerC )
        lProblems.append( 'getListsPartsAndBothStarts() != getPartsIterAndBothStarts()' )
        #
        oOut, lBegText0, lBegSplits0 = getPartsIterAndBothStarts( sTest0, lowercase )
        #
        if list( oOut ) != lOut:
            #
            print3( 'list( oOut ):', list( oOut ) )
            #
    #
    if _getTextStartsAndSplitStarts(
            lOut, lowercase ) != ( [0, 36, 72], [10, 46, 82] ):
        #
        lProblems.append( '_getTextStartsAndSplitStarts() split on lowercase' )
        #
    #
    lPartsStarts  = list( getIterPartsAndBothStarts( sTest0, oFinderLowerC ) )
    #
    if lPartsStarts != [
            ('0123456789',  0, 10),
            ('0123456789', 36, 46),
            ('0123456789', 72, 82) ]:
        #
        # #print unZip( lPartsStarts )
        lProblems.append( 'getIterPartsAndBothStarts() identical split ons' )
        #
    #
    oFinderLowerCorOther = getFinder( lowercase + '|8765' )
    #
    lOut, lBegText, lBegSplits = getListsPartsAndBothStarts(
                                    sTest0, oFinderLowerCorOther )
    #
    if ( lOut, lBegText, lBegSplits ) != \
            ( lDigitsTriple,  [0, 36, 72], [10, 46, 82] ):
        #
        lProblems.append( 'getListsPartsAndBothStarts() variable split ons' )
        #
    #
    lPartsStarts = list(
            getIterPartsAndBothStarts( sTest0, oFinderLowerCorOther ) )
    #
    if lPartsStarts != [
            ('0123456789',  0, 10),
            ('0123456789', 36, 46),
            ('0123456789', 72, 82) ]:
        #
        # #print unZip( lPartsStarts )
        lProblems.append( 'getIterPartsAndBothStarts() variable split ons' )
        #
    #
    oOut, lBegText, lBegSplits = getPartsIterAndBothStarts( sTest0, digits )
    #
    if ( list( oOut ), lBegText, lBegSplits ) != \
            (lAlphaSandwich, [0, 10, 46, 82], [0, 36, 72, 82]):
        #
        oOut, lBegText, lBegSplits = getPartsIterAndBothStarts( sTest0, digits )
        #print list( oOut ), lBegText, lBegSplits
        lProblems.append( 'getPartsIterAndBothStarts( sTest0, digits )' )
        #
    #
    lOut, lBegText, lBegSplits = getListsPartsAndBothStarts( sTest0, oFinderDigits )
    #
    if ( lOut, lBegText, lBegSplits ) != \
                             (lAlphaSandwich, [0, 10, 46, 82], [0, 36, 72, 82]):
        #
        lProblems.append( 'getListsPartsAndBothStarts() send finder, split on digits' )
        #
    #
    lOut, lBegText, lBegSplits = __getListsPartsAndBothStarts( sTest0, digits )
    #
    if ( lOut, lBegText, lBegSplits ) != \
            (lAlphaSandwich, [0, 10, 46, 82], [0, 36, 72, 82]):
        #
        lProblems.append( '__getListsPartsAndBothStarts() send string, split on digits' )
        #
    #
    if _getTextStartsAndSplitStarts(
            lOut, digits ) != ( [0, 10, 46, 82], [0, 36, 72, 82] ):
        #
        lProblems.append( '_getTextStartsAndSplitStarts() on digits' )
        #
    #
    #
    oOut, lBegText, lBegSplits = getPartsIterAndBothStarts( letters, 'a' )
    #
    lOut = list( oOut )
    if ( lOut, lBegText, lBegSplits ) != \
            (['', 'bcdefghijklmnopqrstuvwxyz', 'BCDEFGHIJKLMNOPQRSTUVWXYZ'],
             [0,  1, 27],
             [0, 26, 52]):
        #
        #print lOut
        lProblems.append( "getPartsIterAndBothStarts( letters, 'a' )" )
        #
    #
    oFinderA = getFinder( 'a' )
    #
    lOut, lBegText, lBegSplits = getListsPartsAndBothStarts( letters, oFinderA )
    #
    # ### ### orig version gets it wrong on this one ### ###
    #
    if ( lOut, lBegText, lBegSplits ) != \
            (['', 'bcdefghijklmnopqrstuvwxyz', 'BCDEFGHIJKLMNOPQRSTUVWXYZ'],
             [0,  1, 27],
             [0, 26, 52]):
        #
        lProblems.append( 'getListsPartsAndBothStarts() send finder, split on "a"' )
        #
    #
    oOut, lBegText, lBegSplits = getPartsIterAndBothStarts( sOrig0, '<table>' )
    #
    if ( list( oOut ), lBegText, lBegSplits ) != \
            (lTableFrags, lTextAt, lSplitAt):
        #
        lProblems.append( "getPartsIterAndBothStarts( sOrig0, '<table>' )" )
        #
    #
    lOut, lBegText, lBegSplits = getListsPartsAndBothStarts( sOrig0, oFinderTableTag )
    #
    if ( lOut, lBegText, lBegSplits ) != \
            (lTableFrags, lTextAt, lSplitAt):
        #
        #print lOut, lBegText, lBegSplits
        #print lTableFrags, lTextAt, lSplitAt
        lProblems.append( 'getListsPartsAndBothStarts() split sOrig0 w oFinderTableTag' )
        #
    #
    lOut, lBegText, lBegSplits = __getListsPartsAndBothStarts( sOrig0, '<table>' )
    #
    if ( lOut, lBegText, lBegSplits ) != \
            (lTableFrags, lTextAt, lSplitAt):
        lProblems.append( '__getListsPartsAndBothStarts() split sOrig0 w string' )
        #
    #
    oOut, lBegText, lBegSplits = getPartsIterAndBothStarts( sOrig1, '<table>'  )
    #
    if ( list( oOut ), lBegText, lBegSplits ) != \
            (lTableFrags, lTextAt, lSplitAt):
        #
        lProblems.append( "getPartsIterAndBothStarts( sOrig1, '<table>' )" )
        #
    #
    lOut, lBegText, lBegSplits = getListsPartsAndBothStarts( sOrig1, oFinderTableTag )
    #
    if ( lOut, lBegText, lBegSplits ) != \
            (lTableFrags, lTextAt, lSplitAt):
        lProblems.append( 'getListsPartsAndBothStarts() split sOrig1 w oFinderTableTag' )
        #
    #
    oOut, lBegText, lBegSplits = getPartsIterAndBothStarts( sOrig2, '<table>'  )
    #
    if ( list( oOut ), lBegText, lBegSplits ) != \
            (lTableFrags, lTextAt, lSplitAt):
        #
        lProblems.append( "getPartsIterAndBothStarts( sOrig2, '<table>' )" )
        #
    #
    lOut, lBegText, lBegSplits = getListsPartsAndBothStarts( sOrig2, oFinderTableTag )
    #
    if ( lOut, lBegText, lBegSplits ) != \
            (lTableFrags, lTextAt, lSplitAt):
        lProblems.append( 'getListsPartsAndBothStarts() split sOrig2 w oFinderTableTag' )
        #
    #
    #
    if SplitC( sTest0, lowercase ) != lDigitsTriple:
        #
        lProblems.append( 'SplitC( sTest0, lowercase )' )
        #
    #
    if SplitC( sTest1, lowercase ) != lDigitsTriple:
        #
        lProblems.append( 'SplitC( sTest1, lowercase )' )
        #
    #
    if SplitC( sTest0, digits    ) != lAlphaSandwich:
        #
        lProblems.append( 'SplitC( sTest0, digits )' )
        #
    #
    if SplitC( letters, 'a' ) != \
                ['',
                 'bcdefghijklmnopqrstuvwxyz',
                 'BCDEFGHIJKLMNOPQRSTUVWXYZ']:
        #
        #print SplitC( letters, 'a' )
        lProblems.append( "SplitC( letters, 'a' )" )
        #
    #
    if SplitC( letters, 'z'      ) != \
                ['abcdefghijklmnopqrstuvwxy',
                 'ABCDEFGHIJKLMNOPQRSTUVWXY',
                 '']:
        #
        lProblems.append( "SplitC( letters, 'z' )" )
        #
    #
    if list( iterSplit( sTest0, oFinderLowerC ) ) != lDigitsTriple:
        #
        lProblems.append( 'iterSplit( sTest0, oFinderLowerC )' )
        #
    #
    if list( iterSplit( sTest0, oFinderDigits ) ) != lAlphaSandwich:
        #
        lProblems.append( 'iterSplit( sTest0, oFinderDigits )' )
        #
    #
    if SplitRegular( sTest0, lowercase ) != [ digits, digits + uppercase + digits ]:
        #
        lProblems.append( 'SplitRegular()' )
        #
    #
    # sTest0  = digits + lowercase + digits + uppercase + digits
    #
    if SplitRight(
            sTest0, uppercase, 1 ) != [
                    digits + lowercase + digits, digits ]:
        #
        lProblems.append( 'SplitRight()' )
        #
    #
    if      getPartsListAndStarts( sTest0, lowercase ) != \
                (lDigitsTriple,  [0, 36, 72]):
        #
        #print getPartsListAndStarts( sTest0, lowercase )
        lProblems.append( 'getPartsIterAndStarts( sTest0, lowercase )' )
        #
    #
    if      getPartsListAndStarts( sTest0, digits    ) != \
                (lAlphaSandwich, [0, 10, 46, 82] ):
        #
        #print getPartsListAndStarts( sTest0, digits    )
        lProblems.append( 'getPartsIterAndStarts( sTest0, digits )' )
        #
    if      getPartsListAndStarts( sOrig0, '<table>'  ) != \
                (lTableFrags, lTextAt):
        #
        lProblems.append( "getPartsIterAndStarts( sOrig0, '<table>' )" )
        #
    if      getPartsListAndStarts( sOrig1, '<table>'  ) != \
                (lTableFrags, lTextAt):
        #
        lProblems.append( "getPartsIterAndStarts( sOrig1, '<table>' )" )
        #
    if      getPartsListAndStarts( sOrig2, '<table>'  ) != \
                (lTableFrags, lTextAt):
        #
        lProblems.append(  "getPartsIterAndStarts( sOrig2, '<table>' )" )
        #
    #
    if      getListsSplitsAndStarts( sTest0, oFinderLowerC ) != \
                (lDigitsTriple,  [0, 36, 72]):
        #
        #print getListsSplitsAndStarts( sTest0, oFinderLowerC )
        lProblems.append( 'getListsSplitsAndStarts( sTest0, oFinderLowerC )' )
        #
    #
    if list( getIterSplitsAndStarts( sTest0, oFinderLowerC ) ) != \
                [ ('0123456789',  0),
                  ('0123456789', 36),
                  ('0123456789', 72) ]:
        #
        #print list( getIterSplitsAndStarts( sTest0, oFinderLowerC ) )
        lProblems.append( 'getIterSplitsAndStarts() sTest0 lowercase' )
        #
    #
    if      getListsSplitsAndStarts( sTest0, oFinderDigits ) != \
                (lAlphaSandwich, [0, 10, 46, 82]):
        #
        #print getListsSplitsAndStarts( sTest0, oFinderDigits )
        lProblems.append( 'getListsSplitsAndStarts() sTest0 oFinderDigits' )
        #
    #
    if list( getIterSplitsAndStarts( sTest0, oFinderDigits ) ) != \
                [ ('', 0),
                  ('abcdefghijklmnopqrstuvwxyz', 10),
                  ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 46),
                  ('', 82) ]:
        #
        # #print list( getIterSplitsAndStarts( sTest0, oFinderDigits ) )
        lProblems.append( 'getIterSplitsAndStarts() sTest0 digits' )
        #
    #
    if      getListsSplitsAndStarts( sOrig0, oFinderTableTag ) != \
                (lTableFrags, lTextAt):
        #
        #print getListsSplitsAndStarts( sOrig0, oFinderTableTag )
        lProblems.append( 'getListsSplitsAndStarts() sOrig0 Table' )
        #
    #
    if list( getIterSplitsAndStarts( sOrig0, oFinderTableTag ) ) != \
                [ ('abcdefg',  0),
                  ('hijklm',  14),
                  ('nopqrs',  27),
                  ('tuvwxyz', 40) ]:
        #
        #print list( getIterSplitsAndStarts( sOrig0, oFinderTableTag ) )
        lProblems.append( 'getIterSplitsAndStarts() sOrig0 Table' )
        #
    #
    if      getListsSplitsAndStarts( sOrig1, oFinderTableTag ) != \
                (lTableFrags, lTextAt):
        #
        #print getListsSplitsAndStarts( sOrig1, oFinderTableTag )
        lProblems.append( 'getListsSplitsAndStarts() sOrig1 Table' )
        #
    #
    if list( getIterSplitsAndStarts( sOrig1, oFinderTableTag ) ) != \
                [ ('abcdefg',  0),
                  ('hijklm',  14),
                  ('nopqrs',  27),
                  ('tuvwxyz', 40) ]:
        #
        #print list( getIterSplitsAndStarts( sOrig1, oFinderTableTag ) )
        lProblems.append( 'getIterSplitsAndStarts() sOrig1 Table' )
        #
    #
    if      getListsSplitsAndStarts( sOrig2, oFinderTableTag ) != \
                (lTableFrags, lTextAt):
        #
        #print getListsSplitsAndStarts( sOrig2, oFinderTableTag )
        lProblems.append( 'getListsSplitsAndStarts() sOrig2 Table' )
        #
    #
    if list( getIterSplitsAndStarts( sOrig2, oFinderTableTag ) ) != \
                [ ('abcdefg',  0),
                  ('hijklm',  14),
                  ('nopqrs',  27),
                  ('tuvwxyz', 40) ]:
        #
        #print list( getIterSplitsAndStarts( sOrig2, oFinderTableTag ) )
        lProblems.append( 'getIterSplitsAndStarts() sOrig2 Table' )
        #
    #
    #
    #
    if getSplitsListAndSplitEnds( sTest0, lowercase ) != \
                (lDigitsTriple,  [10, 46, 82]):
        #0
        lProblems.append( 'getSplitsIterAndSplitEnds( sTest0, lowercase )' )
        #
    #
    if getListsSplitsAndSplitEnds( sTest0, oFinderLowerC ) != \
                (lDigitsTriple,  [10, 46, 82]):
        #
        #print getListsSplitsAndSplitEnds( sTest0, oFinderLowerC )
        lProblems.append( 'getListsSplitsAndSplitEnds( sTest0, oFinderLowerC )' )
        #
    #
    if list( getIterSplitsAndSplitEnds( sTest0, oFinderLowerC ) ) != \
                [('0123456789', 10),
                 ('0123456789', 46),
                 ('0123456789', 82)]:
        #
        # #print list( getIterSplitsAndSplitEnds( sTest0, oFinderLowerC ) )
        lProblems.append( 'getIterSplitsAndSplitEnds( sTest0, oFinderLowerC )' )
        #
    #
    if getSplitsListAndSplitEnds( sTest0, digits ) != \
                (lAlphaSandwich, [0, 36, 72, 82]):
        #
        lProblems.append( 'getSplitsIterAndSplitEnds(  sTest0, digits )' )
        #
    #
    if getListsSplitsAndSplitEnds( sTest0, oFinderDigits ) != \
                (lAlphaSandwich, [0, 36, 72, 82]):
        #
        #print getListsSplitsAndSplitEnds( sTest0, oFinderDigits )
        lProblems.append( 'getListsSplitsAndSplitEnds( sTest0, oFinderDigits )' )
        #
    #
    if list( getIterSplitsAndSplitEnds( sTest0, oFinderDigits ) ) != \
                [ ('', 0),
                  ('abcdefghijklmnopqrstuvwxyz', 36),
                  ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 72),
                  ('', 82)]:
        #
        #print list( getIterSplitsAndSplitEnds( sTest0, oFinderDigits ) )
        lProblems.append( 'getIterSplitsAndSplitEnds( sTest0, oFinderDigits )' )
        #
    #
    if getSplitsListAndSplitEnds( sOrig0, '<table>' ) != \
                (lTableFrags, [7, 20, 33, 47]):
        #
        lProblems.append( "getSplitsIterAndSplitEnds( sOrig0, '<table>' )" )
        #
    #
    if getListsSplitsAndSplitEnds( sOrig0, oFinderTableTag ) != \
                (lTableFrags, [7, 20, 33, 47]):
        #
        #print getListsSplitsAndSplitEnds( sOrig0, oFinderTableTag )
        lProblems.append( 'getListsSplitsAndSplitEnds( sOrig0, oFinderTableTag )' )
        #
    #
    if list( getIterSplitsAndSplitEnds( sOrig0, oFinderTableTag ) ) != \
                [ ('abcdefg',  7),
                  ('hijklm',  20),
                  ('nopqrs',  33),
                  ('tuvwxyz', 47) ]:
        #
        #print list( getIterSplitsAndSplitEnds( sOrig0, oFinderTableTag ) )
        lProblems.append( 'getIterSplitsAndSplitEnds( sOrig0, oFinderTableTag )' )
        #
    #
    if getSplitsListAndSplitEnds( sOrig1, '<table>' ) != \
                (lTableFrags, [7, 20, 33, 47]):
        #
        lProblems.append( "getSplitsIterAndSplitEnds( sOrig1, '<table>' )" )
        #
    #
    if getListsSplitsAndSplitEnds( sOrig1, oFinderTableTag ) != \
                (lTableFrags, [7, 20, 33, 47]):
        #
        lProblems.append( 'getListsSplitsAndSplitEnds( sOrig1, oFinderTableTag )' )
        #
    #
    if getSplitsListAndSplitEnds( sOrig2, '<table>' ) != \
                (lTableFrags, [7, 20, 33, 47]):
        #
        lProblems.append( "getSplitsIterAndSplitEnds( sOrig2, '<table>' )" )
        #
    #
    if getListsSplitsAndSplitEnds( sOrig2, oFinderTableTag ) != \
                (lTableFrags, [7, 20, 33, 47]):
        #
        lProblems.append( 'getListsSplitsAndSplitEnds( sOrig2, oFinderTableTag )' )
        #
    #
    if list( getIterSplitsAndSplitEnds( sOrig2, oFinderTableTag ) ) != \
                [ ('abcdefg',  7),
                  ('hijklm',  20),
                  ('nopqrs',  33),
                  ('tuvwxyz', 47) ]:
        #
        lProblems.append( "getIterSplitsAndSplitEnds( sOrig2, '<table>' )" )
        #
    #
    if      getSplitEnds( sTest0, lowercase ) != [10, 46, 82    ] or \
            getSplitEnds( sTest0, digits    ) != [ 0, 36, 72, 82] or \
            getSplitEnds( sOrig0, '<table>' ) != [ 7, 20, 33, 47] or \
            getSplitEnds( sOrig1, '<table>' ) != [ 7, 20, 33, 47] or \
            getSplitEnds( sOrig2, '<table>' ) != [ 7, 20, 33, 47]:
        #
        lProblems.append( 'getSplitEnds()' )
        #
    #
    if      getListSplitEnds( sTest0, oFinderLowerC   ) != [10, 46, 82]:
        #
        #print getListSplitEnds( sTest0, oFinderLowerC   )
        lProblems.append( 'getListSplitEnds( sTest0, oFinderLowerC )' )
        #
    if      getListSplitEnds( sTest0, oFinderDigits   ) != [ 0, 36, 72, 82]:
        #
        #print getListSplitEnds( sTest0, oFinderDigits   )
        lProblems.append( 'getListSplitEnds( sTest0, oFinderDigits )' )
        #
    if      getListSplitEnds( sOrig0, oFinderTableTag ) != [ 7, 20, 33, 47]:
        #
        #print getListSplitEnds( sOrig0, oFinderTableTag )
        lProblems.append( 'getListSplitEnds( sOrig0, oFinderTableTag )' )
        #
    if      getListSplitEnds( sOrig1, oFinderTableTag ) != [ 7, 20, 33, 47]:
        #
        #print getListSplitEnds( sOrig1, oFinderTableTag )
        lProblems.append( 'getListSplitEnds( sOrig1, oFinderTableTag )' )
        #
    if      getListSplitEnds( sOrig2, oFinderTableTag ) != [ 7, 20, 33, 47]:
        #
        #print getListSplitEnds( sOrig2, oFinderTableTag )
        lProblems.append( 'getListSplitEnds( sOrig2, oFinderTableTag )' )
        #
    #
    oFinderSpaces = getFinder( r'(\s+)' )
    #
    sWantSplit = 'The Cat in the  Hat'
    #
    lWantSplitOns = ['The', ' ', 'Cat', ' ', 'in', ' ', 'the', '  ', 'Hat']
    #
    if getSplitWithSplitOns( sWantSplit, oFinderSpaces ) != lWantSplitOns:
        #
        #print getListSplitEnds( sOrig2, oFinderTableTag )
        lProblems.append( 'getSplitWithSplitOns()' )
        #
    #
    #
    if      getPartsListAndPositions( sOrig0, '<table>' ) != \
                (lTableFrags, [7, 20, 33, 47]) or \
            getPartsListAndPositions( sOrig1, '<table>' ) != \
                (lTableFrags, [7, 20, 33, 47]) or \
            getPartsListAndPositions( sOrig2, '<table>' ) != \
                (lTableFrags, [7, 20, 33, 47]):
        #
        lProblems.append( 'getPartsIterAndPositions()' )
        #
    #
    if      getPartsAndPositionsUseFinder( sOrig0, oFinderTableTag ) != \
                (lTableFrags, [7, 20, 33, 47]) or \
            getPartsAndPositionsUseFinder( sOrig1, oFinderTableTag ) != \
                (lTableFrags, [7, 20, 33, 47]) or \
            getPartsAndPositionsUseFinder( sOrig2, oFinderTableTag ) != \
                (lTableFrags, [7, 20, 33, 47]):
        #
        lProblems.append( 'getPartsAndPositionsUseFinder()' )
        #
    #
    if      getCharPositions( sOrig0, '<table>' ) != [7, 20, 33] or \
            getCharPositions( sOrig1, '<table>' ) != [7, 20, 33] or \
            getCharPositions( sOrig2, '<table>' ) != [7, 20, 33]:
        #
        lProblems.append( 'getCharPositions()' )
        #   
    #
    if      getCharPositionsUseFinder( sOrig0, oFinderTableTag ) != [7, 20, 33, 47] or \
            getCharPositionsUseFinder( sOrig1, oFinderTableTag ) != [7, 20, 33, 47] or \
            getCharPositionsUseFinder( sOrig2, oFinderTableTag ) != [7, 20, 33, 47]:
        #
        lProblems.append( 'getCharPositionsUseFinder()' )
        #
    #
    if      list( getTextSplitHere( digits*3, [5,25]            ) ) != \
                ['01234', '56789012345678901234', '56789'] or \
            list( getTextSplitHere( digits*3, [5,25], iDrop = 2 ) ) != \
                ['01234',   '789012345678901234',   '789'] or \
            list( getTextSplitHere( digits*3, [0,5,25]          ) ) != \
            ['', '01234', '56789012345678901234', '56789']:
        #
        lProblems.append( 'getTextSplitHere()' )
        #
    #
    s = 'abc'
    #
    if getSplitButNotIfQuoted( s, ',' ) != [ s ]:
        #
        lProblems.append( 'getSplitButNotIfQuoted() no split on char in string' )
        #
    #
    s = 'abc, def'
    #
    if getSplitButNotIfQuoted( s, ',' ) != [ 'abc', ' def' ]:
        #
        lProblems.append( 'getSplitButNotIfQuoted() split on char in string but not quoted' )
        #
    #
    s =     (    '"Mattia Melocchi, Macom srl" <mattia@macomsrl.it>, '
                '"Yipin Appliances Ltd" <zhyipin@163.com>' )
    #
    lWant = [   '"Mattia Melocchi, Macom srl" <mattia@macomsrl.it>',
               ' "Yipin Appliances Ltd" <zhyipin@163.com>' ]
    #
    if getSplitButNotIfQuoted( s, ',' ) != lWant:
        #
        lProblems.append( 'getSplitButNotIfQuoted() quoted split char in string' )
        #
    #
    s =     (   '"Sharon Wang, Advanced Approach Ltd." <info@advanced-app.com.hk, '
                '"Mattia Melocchi, President, Macom srl" <mattia@macomsrl.it>, '
                '"Yipin Appliances Ltd" <zhyipin@163.com>' )
    #
    lWant = [   '"Sharon Wang, Advanced Approach Ltd." <info@advanced-app.com.hk',
               ' "Mattia Melocchi, President, Macom srl" <mattia@macomsrl.it>',
               ' "Yipin Appliances Ltd" <zhyipin@163.com>' ]
    #
    if getSplitButNotIfQuoted( s, ',' ) != lWant:
        #
        lProblems.append( 'getSplitButNotIfQuoted() complicated quoted split char in string' )
        #
    #
    if _getPartitioned( digits, '45' ) != ('0123', '45', '6789'):
        #
        lProblems.append( '_getPartitioned() separator in string' )
        #
    #
    if _getPartitioned( digits, 'ab' ) != ( digits, '', ''):
        #
        lProblems.append( '_getPartitioned() separator not in string' )
        #
    #
    if getPartitioned( digits, '45' ) != ('0123', '45', '6789'):
        #
        lProblems.append( 'getPartitioned() separator in string' )
        #
    #
    if getPartitioned( digits, 'ab' ) != ( digits, '', ''):
        #
        lProblems.append( 'getPartitioned() separator not in string' )
        #
    #
    sDoubleDigits = digits * 2
    #
    if _getRPartitioned(
            sDoubleDigits, '45' ) != ('01234567890123', '45', '6789'):
        #
        lProblems.append( '_getRPartitioned() separator in string' )
        #
    #
    if getSplitAndStrip( 'spam, eggs, toast ' ) != ( 'spam', 'eggs', 'toast' ):
        #
        lProblems.append( 'getSplitAndStrip() default split on' )
        #
    #
    oFinder = getFinder( ',' )
    #
    if getSplitAndStrip(
            'spam, eggs, toast ', oFinder ) != ( 'spam', 'eggs', 'toast' ):
        #
        lProblems.append( 'getSplitAndStrip() oFinder split on' )
        #
    #
    if getRemoved( lowercase, 'abc' ) != lowercase[ 3 : ]:
        #
        lProblems.append( 'getRemoved() take off front' )
        #
    #
    if getRemoved( lowercase, 'lmno' ) != '%s %s' % ( lowercase[ : 11 ], lowercase[ 15 : ] ):
        #
        lProblems.append( 'getRemoved() extract from middle' )
        #
    #
    if getRemoved( lowercase, 'xyz' ) != lowercase[ : -3 ]:
        #
        lProblems.append( 'getRemoved() take off end' )
        #
    #
    if getRemoved( lowercase, '0123' ) != lowercase:
        #
        lProblems.append( 'getRemoved() nothing to remove' )
        #
    #
    sCharPositions = '01234<6789>\rabcd\nfghijkl<*>ABCDE</*>'
    #
    dPositions = {}
    #
    for sChar in ( '<', '>', '\r', '\n', "<*", "</*>" ):
        #
        dPositions[ sChar ] = getCharPositions( sCharPositions, sChar )
    #
    lPositions = getItemList( dPositions )
    #
    lPositions.sort()
    #
    lExpect = [
        ('\n', [16]),
        ('\r', [11]),
        ('<', [5, 24, 32]),
        ('<*', [24]),
        ('</*>', [32]),
        ('>', [10, 26, 35]) ]
    #
    if lPositions != lExpect:
        #
        lProblems.append( 'getCharPositions() series of characters' )
        #
    #
    #
    sayTestResult( lProblems )