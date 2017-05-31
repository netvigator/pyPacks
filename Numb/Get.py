#!/usr/bin/pythonTest
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
#   http://www.gnu.org/licenses/gpl.html
#
# Copyright 2004-2017 Rick Graves
#

from six import print_ as print3


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





def getRandomDigits( iHowMany = 10 ):
    #
    from random import random
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


def _RandomDigitFeederFactory():
    #
    from random import random, shuffle
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
    from Iter.AllVers       import iMap
    from Utils.TimeTrial  import TimeTrial
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
    from six.moves      import reduce as Reduce
    #
    #from Utils.Both2n3 import Reduce
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
    from Collect.Test import isListOrTuple
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
    '''sum() was new in python 2.3 but sums from left to right,
    which can result in catastrophic cumulative rounding errors
    if there are floats.  this avoids rounding errors.'''
    #
    from itertools      import islice
    #
    from six.moves      import reduce as Reduce
    #
    from Collect.Test   import isListOrTuple
    from Iter.AllVers   import iMap, iZipLongest
    from Numb.Test      import isFloat
   #from Utils.Both2n3  import Reduce
    from Collect.Test   import AnyMeet
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
    from Numb.Test      import hasIntegersOnly
    from Collect.Test   import isListOrTuple
    #
    if args and len( args ) == 1 and isListOrTuple( args[0] ):
        #
        args = args[0]
    #
    if hasIntegersOnly( *args ):
        #
        uSum = getSumOnlyIntegers( *args )
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
    from Iter.AllVers   import iRange
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



if __name__ == "__main__":
    #
    from six            import next as getNext
    #
    from Iter.AllVers   import iRange, tMap
   #from Utils.Both2n3  import getNext
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
    #
    sayTestResult( lProblems )