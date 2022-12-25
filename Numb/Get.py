#!/home/rick/.local/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Number functions get
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
#
from itertools              import islice
from math                   import ceil
from pprint                 import pprint
from random                 import random, shuffle
from string                 import digits

from six                    import print_ as print3
from six.moves              import reduce as Reduce

try:
    from .Test              import isFloat, hasIntegersOnly
    from ..Collect.Test     import isListOrTuple, AnyMeet
    from ..Iter.AllVers     import iMap, iRange, iZipLongest
    from ..Utils.TimeTrial  import TimeTrial
except ( ValueError, ImportError ):
    from Numb.Test          import isFloat, hasIntegersOnly
    from Collect.Test       import isListOrTuple, AnyMeet
    from Iter.AllVers       import iMap, iRange, iZipLongest
    from Utils.TimeTrial    import TimeTrial


def getAdder( iAddTo ):
    #
    def Adder( i ): return i + iAddTo
    #
    return Adder



def getMultiplier( iTimes ):
    #
    def Multiplier( i ): return i * iTimes
    #
    return Multiplier



def _gotRepeats( s, chars = digits, troubleshoot = False ):
    #
    '''
    goal (not super strict): minimal repeating characters in s
    if chars = digits, iCharsLen = 10
    if length of s is 10, this is OK: 0012345678
    if length of s is 20, this is OK: 00112345678901234567
    if length of s is 30, this is OK: 001122345678901234567890123456    
    '''
    #
    inputLen    = len( s )
    iCharsLen   = len( chars )
    #
    fMultiple   = float( inputLen ) / iCharsLen
    #
    iMax        = ceil( fMultiple )
    #
    dChars      = dict.fromkeys( tuple( chars ), 0 )
    #
    iDictLen    = len( dChars )
    #
    bTooManyRepeats = False
    #
    for c in s:
        #
        dChars[ c ] += 1
        #
        if dChars[ c ] > iMax:
            #
            bTooManyRepeats = True
            #
            break
            #
        #
    #
    iGotCharsLen = len( tuple( [ c for c in dChars if dChars[ c ] > 0 ] ) )
    #
    if iGotCharsLen < inputLen / 2:
        #
        bTooManyRepeats = True
        #
    #
    if bTooManyRepeats and troubleshoot:
        #
        print( 'inputLen    : %s' % inputLen     )
        print( 'iCharsLen   : %s' % iCharsLen    )
        print( 'fMultiple   : %s' % fMultiple    )
        print( 'iMax        : %s' % iMax         )
        print( 'iDictLen    : %s' % iDictLen     )
        print( 'iGotCharsLen: %s' % iGotCharsLen )
        pprint( dChars )                
        #
    #
    return bTooManyRepeats


def getRandomDigits( iHowMany = 10 ):
    #
    sRandom = ''
    #
    while len( sRandom  ) < iHowMany + 3:
        #
        iRandom = int( random() * float( pow( 10, iHowMany + 3 ) ) )
        #
        sRandom = str( iRandom )
        #
    return  '%s' % sRandom[ 1 : -2 ]


def getRandomDigitsMinRepeats( iHowMany = 10 ):
    #
    sRandomDigits = ''
    #
    while True:
        #
        sRandomDigits = getRandomDigits( iHowMany )
        #
        if not _gotRepeats( sRandomDigits ):
            #
            break
            #
        #
    #
    return sRandomDigits





def _RandomDigitFeederFactory():
    #
    #
    lDigits = []
    #
    while True:
        #
        if not lDigits:
            #
            lRandom = list( str( random() ) )
            #
            del lRandom[ : 2 ]
            #
            shuffle( lRandom )
            #
            lDigits.extend( lRandom )
            #
        #
        yield lDigits.pop()







def getBooleanIntSlower( u ):
    #
    return int( not not u )



def getBooleanInt( u ):
    #
    if u: return 1
    else: return 0


def getBooleanIntOther( u ):
    #
    if u: return 1
    #
    return 0




def _getBooleanIntTimeTrial():
    #
    #
    tTestVals = ( 'a', '', 10, 0, 0.1, 0.0, [''], [],  getAdder, None )
    #
    print3( iMap( getBooleanInt, tTestVals ) )
    #
    print3( '\nusing getBooleanIntOther ...' )
    #
    TimeTrial( getBooleanIntOther, tTestVals )
    #
    print3( '\nusing getBooleanInt ...' )
    #
    TimeTrial( getBooleanInt, tTestVals )



def getFloatHalfRound( f ):
    #
    i = int( f )
    #
    if int( round( f ) ) == i:
        #
        f = float( i )
        #
    else:
        #
        f = float( i ) + 0.5
        #
    return f


def pairSum(      x, y ): return x + y

def pairSubtract( x, y ): return x - y

def pairMultiply( x, y ): return x * y

def pairDivide(   x, y ): return x / y


def getSumOnlyIntegers( *Numbers, **kwargs ):
    #
    '''
    sum() was new in python 2.3
    if you have a sequence of integers, sum() is much faster!
    this function is obsolete!!!
    '''
    #
    #
    nEmptyListValue = kwargs.get( 'nEmptyListValue', 0 )
    #
    if Numbers:
        tNumbs  = tuple( Numbers )
    else:
        tNumbs  = [ nEmptyListValue ]
    #
    return Reduce( pairSum, tNumbs )


def _getSumNoneOK( x, y = None ):
    #
    if y is None:
        #
        return x
        #
    else:
        #
        return x + y


def getSumLeft2Right( *args ):
    #
    #
    if args and len( args ) == 1 and isListOrTuple( args[0] ):
        #
        args = args[0]
    #
    nResult = 0
    #
    for n in args:
        #
        nResult += n
    #
    return nResult





def getSumOffList( *Numbers ):
    #
    '''
    sum() was new in python 2.3 but sums from left to right,
    which can result in catastrophic cumulative rounding errors
    if there are floats.  this avoids rounding errors.
    '''
    #
    #
    if len( Numbers ) == 1 and isListOrTuple( Numbers[0] ):
        #
        Numbers = Numbers[0]
    #
    if Numbers:
        lNumbs  = list( Numbers )
    else:
        lNumbs  = [ 0 ]
    #
    nSum = None
    #
    if AnyMeet( lNumbs, isFloat ): # doing this to minimize cumulative error
        #
        iListLen        = len( lNumbs )
        #
        lNumbs.sort()
        #
        #print3( lNumbs )
        while len( lNumbs ) > 1:
            #
            iterEvens = islice( lNumbs, 0, iListLen, 2 )
            #
            iterOdds  = islice( lNumbs, 1, iListLen, 2 )
            #
            lNumbs    = [ sum( tPair )
                          for tPair
                          in iZipLongest( iterEvens, iterOdds, fillvalue=0 ) ]
            #
            # print3( lNumbs )
        #

        #
        if lNumbs: nSum = lNumbs[0]
        #
    else:
        #
        nSum = Reduce( pairSum, lNumbs )
        #
    #
    return nSum


def getSum( *args ):
    #
    '''
    sum() was new in python 2.3 but sums from left to right,
    which can result in catastrophic cumulative rounding errors
    if there are floats.  this avoids rounding errors.
    '''
    #
    #
    if args and len( args ) == 1 and isListOrTuple( args[0] ):
        #
        args = args[0]
    #
    if hasIntegersOnly( *args ):
        #
        uSum = sum( args )
        #
    else:
        #
        uSum = getSumOffList( *args )
        #
    #
    return uSum



def iRanger( iStart, iStop, iStep = 1 ):
    #
    '''
    range(   6, 10 ) returns 6, 7, 8, 9
    iRanger( 6, 10 ) returns 6, 7, 8, 9, 10
    '''
    #
    #
    return iRange( iStart, iStop + iStep, iStep ) 


def lRanger( iStart, iStop, iStep = 1 ):
    #
    return list( iRanger( iStart, iStop, iStep ) )


def tRanger( iStart, iStop, iStep = 1 ):
    #
    return tuple( iRanger( iStart, iStop, iStep ) )




def getOneDigitOffLong( iNumb, iStart = 1, iLimit = 5 ):
    #
    '''
    gets a digit off a longer number
    same digit is returned from same longer number every time
    
    pass
    iNumb  the required longer number
    iStart defaults to 1
    iLimit defaults to 5 never returns this number, will return this minus 1
    
    getOneDigitOffLong( 1, 0, 4 ) returns 1
    getOneDigitOffLong( 2, 0, 4 ) returns 2
    getOneDigitOffLong( 3, 0, 4 ) returns 3
    getOneDigitOffLong( 4, 0, 4 ) returns 0

    getOneDigitOffLong( 102, 1, 4 ) returns 1
    getOneDigitOffLong( 103, 1, 4 ) returns 2
    getOneDigitOffLong( 104, 1, 4 ) returns 3
    getOneDigitOffLong( 105, 1, 4 ) returns 1
    '''
    #
    iRemain = int( iNumb ) % ( iLimit - iStart ) # remainder
    #
    return iStart + iRemain


def getHowManyDigitsNeeded( iNumb ):
    #
    '''
    if you pass an integer under     10, returns 1
    if you pass an integer under    100, returns 2
    if you pass an integer under   1000, returns 3
    if you pass an integer under 10,000, returns 4
    '''
    #
    for i in iRange( 1, 20 ):
        #
        if iNumb < 10**i:
            #
            return i






if __name__ == "__main__":
    #
    from six            import next as getNext
    #
    from Iter.AllVers   import tMap
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    oAdd2 = getAdder(  2 )
    oSub2 = getAdder( -2 )
    #
    if oAdd2( 2 ) != 4 or oSub2( 2 ):
        #
        lProblems.append( 'getAdder()' )
        #
    #
    oTimes2 = getMultiplier(   2 )
    oDivBy2 = getMultiplier( 0.5 )
    #
    if oTimes2( 2 ) != 4 or oDivBy2( 2 ) != 1:
        #
        lProblems.append( 'getMultiplier()' )
        #
    #
    sDigits = getRandomDigits( 5 )
    #
    if len( sDigits ) != 5 or not sDigits.isdigit():
        #
        lProblems.append( 'getRandomDigits()' )
        #
    #
    if getBooleanInt( 'a' ) != 1 or getBooleanInt( '' ) != 0:
        #
        lProblems.append( 'getBooleanIntSlower()' )
        #
    #
    l = [ 1.0 + float( i )/10 for i in iRange(10) ]
    #
    l.append( 2.0 )
    #
    tHalfRounds = tMap( getFloatHalfRound, l )
    #
    if tHalfRounds != ( 1.0, 1.0, 1.0, 1.0, 1.0, 1.5, 1.5, 1.5, 1.5, 1.5, 2.0 ):
        #
        lProblems.append( 'getFloatHalfRound()' )
        #
    #
    if pairSum( 2, 3 ) != 5:
        #
        lProblems.append( 'pairSum()' )
        #
    #
    if getSumOffList( 1. ) != 1:
        #
        lProblems.append( 'getSumOffList( 1. )' )
        #
    #
    fResult = getSumOffList( 1.8, 2.8, 3.8 )
    #
    if fResult > 8.41 or fResult < 8.39:
        #
        print3( fResult )
        lProblems.append( 'getSumOffList( 1.8, 2.8, 3.8 )' )
        #
    #
    fResult = getSumOffList( ( 1.8, 2.8, 3.8 ) )
    #
    if fResult > 8.41 or fResult < 8.39:
        #
        print3( fResult )
        lProblems.append( 'getSumOffList( 1.8, 2.8, 3.8 )' )
        #
    #
    fResult = getSumLeft2Right( 1.8, 2.8, 3.8 )
    #
    if fResult > 8.41 or fResult < 8.39:
        #
        print3( fResult )
        lProblems.append( 'getSumLeft2Right( 1.8, 2.8, 3.8 )' )
        #
    #
    if getSumOffList( 1,   2,   3   ) != 6:
        #
        lProblems.append( 'getSumOffList( 1,   2,   3   )' )
        #
    #
    if getSumOnlyIntegers( 1, 2, 3 ) != 6:
        #
        lProblems.append( 'getSumOnlyIntegers()' )
        #
    #
    if getSum( 1, 2, 3 ) != 6:
        #
        lProblems.append( 'getSum() integers' )
        #
    #
    if getSum( tHalfRounds ) != 14.5:
        #
        print3( getSum( tHalfRounds ) )
        lProblems.append( 'getSum() floats' )
        #
    #
    if tRanger( 6, 10 ) != ( 6, 7, 8, 9, 10 ):
        #
        lProblems.append( 'tRanger()' )
        #
    #
    getRandomDigitFeeder = _RandomDigitFeederFactory()
    #
    sTest = getNext( getRandomDigitFeeder )
    #
    if not sTest.isdigit(): 
        #
        lProblems.append( '_RandomDigitFeederFactory()' )
        #
    #
    if getOneDigitOffLong( 102, 1, 4 ) != 1:
        #
        lProblems.append(
            'getOneDigitOffLong( 102, 1, 4 ) returns %s'
             % getOneDigitOffLong( 102, 1, 4 ) )
        #
    #
    if getOneDigitOffLong( 103, 1, 4 ) != 2:
        #
        lProblems.append(
            'getOneDigitOffLong( 103, 1, 4 ) returns %s'
             % getOneDigitOffLong( 103, 1, 4 ) )
        #
    #
    if getOneDigitOffLong( 104, 1, 4 ) != 3:
        #
        lProblems.append(
            'getOneDigitOffLong( 104, 1, 4 ) returns %s'
             % getOneDigitOffLong( 104, 1, 4 ) )
        #
    #
    if getOneDigitOffLong( 105, 1, 4 ) != 1:
        #
        lProblems.append(
            'getOneDigitOffLong( 105, 1, 4 ) returns %s'
             % getOneDigitOffLong( 105, 1, 4 ) )
        #
    #
    for i in iRange( 1, 19 ):
        #
        if getHowManyDigitsNeeded( 10**i - 1 ) != i:
            #
            lProblems.append(
                    'getHowManyDigitsNeeded( %s ) returns %s not %s' %
                    ( (10**i - 1),
                      getHowManyDigitsNeeded( 10**i - 1 ),
                      i ) )
            #
    #
    s = digits
    #
    if _gotRepeats( s, troubleshoot = False ):
        #
        lProblems.append(
            '_gotRepeats( %s ) returns True' % s )
        #
    #
    s = digits + '0'
    #
    if _gotRepeats( s ):
        #
        _gotRepeats( s, troubleshoot = True )
        #
        lProblems.append(
            '_gotRepeats( %s ) returns True' % s )
        #
    #
    s = digits + '00'
    #
    if not _gotRepeats( s ):
        #
        _gotRepeats( s, troubleshoot = True )
        #
        lProblems.append(
            '_gotRepeats( %s ) returns False' % s )
        #
    #
    s = '0012'
    #
    if not _gotRepeats( s ):
        #
        _gotRepeats( s, troubleshoot = True )
        #
        lProblems.append(
            '_gotRepeats( %s ) returns False' % s )
        #
    #
    sayTestResult( lProblems )
