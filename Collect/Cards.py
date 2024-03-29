#!/home/rick/.local/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Collection functions Cards
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
'''
simulates suffling a deck of cards
you supply the sequence (the deck)
'''

from copy               import copy
from random             import random, randrange, shuffle

try:
    from ..Iter.AllVers import iRange, tRange, iMap
    from ..Numb.Crunch  import getIntegerDivisionRoundUp
    from ..Numb.Get     import getSumOnlyIntegers
    from ..Numb.Test    import isOdd
except ( ValueError, ImportError ):
    from Iter.AllVers   import iRange, tRange, iMap
    from Numb.Crunch    import getIntegerDivisionRoundUp
    from Numb.Get       import getSumOnlyIntegers
    from Numb.Test      import isOdd


_dMaxShuffles = {
    3 : 1,
    4 : 3,
    5 : 3,
    6 : 2,
    7 : 2 }



def getCutPosition( uSeq, bPutBack = False, iOffset = 0 ):
    #
    '''
    returns iCutAt, the regular index position of the place to cut,
    with the first character having a regular index position of zero
    string will be cut as follows:
    return uSeq[ : iCutAt ], uSeq[ iCutAt : ]

    getCutPosition( 26, iOffset = -13 ) returns  0
    getCutPosition( 26, iOffset =   0 ) returns 13
    getCutPosition( 26, iOffset =  13 ) returns 26
    getCutPosition( 25, iOffset = -12 ) returns  0
    getCutPosition( 25, iOffset =   0 ) returns 12
    getCutPosition( 25, iOffset =  13 ) returns 25
    '''
    #
    if isinstance( uSeq, int ):
        #
        iLen    = uSeq
        #
    else:
        #
        iLen    = len( uSeq )
        #
    #
    if bPutBack:
        #
        iCutAt  = getIntegerDivisionRoundUp( iLen, 2 ) - iOffset
        #
    else:
        #
        iCutAt  = iLen // 2 + iOffset
        #
    #
    return iCutAt



def CutTheCards( uSeq, bPutBack = False, bSloppy = False, iOffset = 0 ):
    #
    iCutAt = getCutPosition( uSeq, bPutBack = bPutBack, iOffset = iOffset )
    #
    if bSloppy:
        #
        iLenTenth   = iCutAt // 5 or 1
        #
        iCutAt      = iCutAt + \
                      ( 1 if random() > 0.5 else -1 *
                        randrange( iLenTenth ) )
        #
    #
    return uSeq[ : iCutAt ], uSeq[ iCutAt : ]




def ShuffleTheCards( uSeq, bPutBack = False, iShuffles = 1 ):
    #
    bGotString              = isinstance( uSeq, str )
    #
    iLen                    = len( uSeq )
    #
    lSeq                    = list( uSeq )
    #
    iHalfLen                = getIntegerDivisionRoundUp( iLen, 2 )
    #
    tCardIndexes            = tRange( iHalfLen )
    #
    lSeq                    = list( uSeq )
    #
    for iShuffle in iRange( iShuffles ):
        #
        if bPutBack:
            #
            lBeg, lEnd      = [], []
            #
            for iThisCard in tCardIndexes:
                #
                lBeg.append( lSeq[ ( 2 * iThisCard ) + 0 ] )
                #
                if ( 2 * iThisCard ) + 1 < iLen:
                    #
                    lEnd.append( lSeq[ ( 2 * iThisCard ) + 1 ] )
                    #
                #
            #
            lShuffled       = lBeg + lEnd
            #
        else:
            #
            lShuffled       = []
            #
            for iThisCard in tCardIndexes:
                #
                lShuffled.append( lSeq[ iThisCard ] )
                #
                if iThisCard + iHalfLen < iLen:
                    #
                    lShuffled.append( lSeq[ iThisCard + iHalfLen ] )
                    #
                #
            #
        #
        lSeq = lShuffled
        #
    #
    if bGotString:
        #
        return ''.join( lSeq )
    #
    return lSeq




def _getOffBottom( lSeq, iMax = 3 ):
    #
    iEat            = randrange( 1, iMax + 1 )
    #
    lEatThis        = list( lSeq[ - iEat : ] )
    lLeftOver       = list( lSeq[ : - iEat ] )
    #
    return lEatThis, lLeftOver



def SloppyShuffle( uSeq, iShuffles = 1 ):
    #
    uEmpty              = uSeq[ len( uSeq ) : ]
    #
    #
    for iShuffle in iRange( iShuffles ):
        #
        lTop, lBot          = CutTheCards( uSeq, bSloppy = True )
        #
        #
        def getMax( lToEat, lOther ):
            #
            iMax            = min( len( lToEat ) - len( lOther ), 3 )
            #
            iMax            = max( iMax, 2 )
            #
            return iMax
        #
        lShuffled           = []
        #
        if random() > 0.5:  # start with the bottom
            #
            iMax            = getMax( lBot, lTop )
            #
            lEatThis, lBot  = _getOffBottom( lBot, iMax )
            #
            lShuffled       = lEatThis
        #
        while len( lTop ) + len( lBot ) > 0:
            #
            iMax            = getMax( lTop, lBot )
            #
            lEatThis, lTop  = _getOffBottom( lTop, iMax )
            #
            lShuffled       = lEatThis + lShuffled
            #
            iMax            = getMax( lBot, lTop )
            #
            lEatThis, lBot  = _getOffBottom( lBot, iMax )
            #
            lShuffled       = lEatThis + lShuffled
            #
        #
        if type( uEmpty ) == str:
            #
            sShuffled = ''.join( lShuffled )
            #
        else:
            #
            sShuffled = lShuffled
            #
        #
        uSeq            = sShuffled
        #
    #
    return sShuffled



def ShuffleAndCut(
            uSeq,
            bPutBack    = False,
            iShuffles   = None,
            bSloppy     = False,
            iCutOffset  = 0 ):
    #
    iLen            = len( uSeq )
    #
    bGotString = isinstance( uSeq, str )
    #
    lSeq            = list( uSeq )
    #
    if iShuffles is None:
        #
        iStartAt    = 1 if iLen % 7 == 0 else 2
        #
        iDivisor    = 2 if isOdd( iLen ) else 3
        #
        iShuffles   = iStartAt + ( iLen % iDivisor )
        #
    #
    if bPutBack:
        #
        for iThisShuffle in iRange( iShuffles ):
            #
            lTop, lBot  = CutTheCards(
                            lSeq, bPutBack = True, iOffset = iCutOffset )
            #
            lSeq        = lBot + lTop   # put bottom on top
            #
            lSeq        = ShuffleTheCards( lSeq, bPutBack = True )
            #
            #
        #
    else:
        #
        for iThisShuffle in iRange( iShuffles ):
            #
            if bSloppy:
                #
                lSeq    = SloppyShuffle(   lSeq )
                #
            else:
                #
                lSeq    = ShuffleTheCards( lSeq )
                #
            #
            lTop, lBot  = CutTheCards(
                            lSeq, bSloppy = bSloppy, iOffset = iCutOffset )
            #
            lSeq        = lBot + lTop   # put bottom on top
            #
        #
    #
    if bGotString:
        #
        return ''.join( lSeq )
        #
    return lSeq



def ShuffleDigits( sDigits, bPutBack = False ):
    #
    '''
    digits  iShuffleMax
    3       1
    4       3
    5       3
    6       2
    7       2
    8       5
    9       5
    '''
    #
    iSum        = getSumOnlyIntegers( *iMap( int, sDigits ) )
    #
    iLen        = len( sDigits )
    #
    iBase       = _dMaxShuffles.get( iLen, 5 )
    #
    iShuffles   = 1 + iSum % iBase
    #
    iOffset     = ( iSum % iLen ) - iLen // 2
    #
    return ShuffleAndCut( sDigits,
            bPutBack    = bPutBack,
            iShuffles   = iShuffles,
            iCutOffset  = iOffset )



    


def getRandoms( lSeq, iWant = -1, bSloppyShuffle = False ):
    #
    if len( lSeq ) == 0: return lSeq
    #
    bGotTuple = bGotString = False
    #
    if   type( lSeq ) == tuple:
        bGotTuple   = True
        lSeq = list( lSeq )
    elif type( lSeq ) == str:
        bGotString  = True
        lSeq = list( lSeq )
    #
    shuffle( lSeq )
    #
    # from Python docs on shuffle
    # Note that for even rather small len(x),
    # the total number of permutations of x
    # is larger than the period of most random number generators;
    # this implies that most permutations
    # of a long sequence can never be generated.
    #
    if bSloppyShuffle:
        #
        lTop, lBot  = CutTheCards(
                SloppyShuffle( ShuffleAndCut( lSeq ) ), bSloppy = True )
        #
    else:
        #
        lTop, lBot  = CutTheCards( lSeq, bSloppy = True )
        #
    #
    # lSeq        = lBot + lTop
    #
    if iWant < 0: iWant = len( lSeq )
    #
    lSeq    = lBot[ : iWant ]
    #
    iSeqLen = len( lSeq )
    #
    if iSeqLen < iWant:
        #
        lSeq += lTop[ : iWant - iSeqLen ]
        #
    #
    if bGotTuple:
        #
        lSeq    = tuple( lSeq )
        #
    elif bGotString:
        #
        lSeq    = ''.join( lSeq )
        #
    #
    return lSeq



if __name__ == "__main__":
    #
    lProblems = []
    #
    from string             import digits
    from string             import ascii_letters as letters
    #
    from Iter.AllVers       import lRange
    from Iter.AllVers       import iMap
    from Utils.Result       import sayTestResult
    from Utils.Both2n3      import print3
    #
    #
    lSeq = letters
    #
    if not getRandoms( lSeq, iWant = -1, bSloppyShuffle = False ):
        #
        lProblems.append( 'getRandoms()' )
        #

    # tests to make sure ShuffleAndCut( sChars ) != sChars
    #
    sChars      = letters + digits
    #
    iCharsLen   = len( sChars )
    #
    lChars      = list( sChars )
    #
    lCardsRange = lRange( iCharsLen )[ 3 : ]
    #
    lProblems += [ i for i in lCardsRange
                   if lChars[ : i ] == ShuffleAndCut( lChars[ : i ] ) ]
    #
    del lCardsRange[ : 3 ]
    #
    if [ i for i in lCardsRange
         if ShuffleAndCut( lChars[ : i ] ) ==
            ShuffleAndCut( lChars[ : i ], bSloppy = True ) ]:
        #
        lProblems.append( 'ShuffleAndCut( lChars, bSloppy = True )' )
        #
    #
    for i in iRange(5):
        #
        sDigits = getRandoms(
                ''.join( iMap( str, iRange(10) ) ), iWant = i + 4 )
        #
        sShuffled = ShuffleDigits( sDigits )
        sPutBack  = ShuffleDigits( sShuffled, bPutBack = True )
        #
        if sPutBack != sDigits:
            #
            lProblems.append( 'ShuffleDigits() "%s"' % sDigits )
            #
        #
    #
    lCut = CutTheCards( letters, bPutBack = False, iOffset = 10 )
    #
    sNew = lCut[1] + lCut[0]
    #
    lCut = CutTheCards( sNew, bPutBack = True, iOffset = 10 )
    #
    sNewer = lCut[1] + lCut[0]
    #
    if sNewer != letters:
        #
        lProblems.append( 'CutTheCards() put back' )
        #
    #
    sNew = ShuffleAndCut( letters, bPutBack = False, iCutOffset = 10 )
    #
    if ShuffleAndCut( sNew, bPutBack = True, iCutOffset = 10 ) != letters:
        #
        lProblems.append( 'ShuffleAndCut() put back' )
        #
    #
    if (    getCutPosition( 26, iOffset =  -13 ) !=  0 or
            getCutPosition( 26, iOffset =    0 ) != 13 or
            getCutPosition( 26, iOffset =   13 ) != 26 or
            getCutPosition( 25, iOffset =  -12 ) !=  0 or
            getCutPosition( 25, iOffset =    0 ) != 12 or
            getCutPosition( 25, iOffset =   13 ) != 25 ):
        #
        lProblems.append( 'getCutPosition() various' )
        #
    #
    #
    sCards = '0123456789ABCDEF'
    #
    lCards = [ ShuffleAndCut( sCards, iCutOffset = i )
               for i in range( -7, 8 ) ]
    #
    setCards = frozenset( lCards )
    #
    if len( lCards ) != len( setCards ):
        #
        lProblems.append( 'ShuffleAndCut() over a range' )
        #
    #
    if ShuffleTheCards( letters, iShuffles = 8 ) != letters:
        #
        lProblems.append( 'ShuffleTheCards() '
                          'deck of letters back to the original' )
        #
    #
    for t in ( ( letters, 'letters' ), ( digits, 'digits' ) ):
        #
        for i in iRange(8):
            #
            sShuffled = ShuffleTheCards(
                            t[0],   iShuffles = i )
            sPutBack  = ShuffleTheCards(
                            sShuffled, iShuffles = i, bPutBack = True )
            #
            if sPutBack != t[0]:
                #
                lProblems.append(
                        'ShuffleTheCards( %s, iShuffles = %s ) put back' %
                        ( t[1], i ) )
                #
    #
    sayTestResult( lProblems )
