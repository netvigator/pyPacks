#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# string functions Test
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
# Copyright 2004-2016 Rick Graves
#

from Utils.Both2n3      import setNumberTypes


def isEven( iNumb2Test ):
    #
    return iNumb2Test % 2 == 0

def isOdd( iNumb2Test ):
    #
    return iNumb2Test % 2 == 1

def isFloat( u ):   return type( u ) == float

def isInteger( u ): return type( u ) == int

def isLong( u ):    return type( u ) == type( 88**88 )


def isNumber( u ):  return type( u ) in setNumberTypes

def isWhole( n ):   return int( n ) == n


def hasIntegersOnly( *args ):
    #
    from Collect.Test   import isListOrTuple
    #
    if args and len( args ) == 1 and isListOrTuple( args[0] ):
        #
        args = args[0]
    #
    from Collect.Test import AllMeet
    #
    bIntegerOnly = AllMeet( args, isInteger )
    #
    return bIntegerOnly


def areClose( nOrig, nTest, iPerCent = 1 ):
    #
    '''
    both 9 and 11 are within 10% of 10
    pass nOrig, nTest, iPerCent (integer)
    returns whether nTest is within iPerCent of nOrig
    formerly named isClose( 10,  9, 10 )
    '''
    #
    fSmaller = ( 1.0 - ( iPerCent / 100.0 ) ) * nOrig
    fBigger  = ( 1.0 + ( iPerCent / 100.0 ) ) * nOrig
    #
    return fSmaller <= nTest <= fBigger


def areEquals( nOrig, nTest, iPerCent = 0 ):
    #
    '''
    tester is plug compatible with areClose()
    '''
    #
    return nOrig == nTest

    

def getHowClose( nOrig, nTest ):
    #
    from Iter.AllVers import iRange
    #
    if nOrig == nTest:
        #
        sHowClose = 'identical'
        #
    else:
        #
        sHowClose = 'not even within 10%'
        #
        for i in iRange( 20 ):
            #
            iPerCent = 10.0 / 10 ** i
            #
            if areClose( nOrig, nTest, iPerCent ):
                #
                if iPerCent > 0.5: iPerCent = int( iPerCent )
                #
                sSayPercent = str( iPerCent )
                #
                if i > 2: sSayPercent = '0.%s1' % ( '0' * ( i - 2 ) )
                #
                sHowClose = 'within %s%%' % sSayPercent
                #
            else:
                #
                break
                #
            #
        #
    #
    return sHowClose


def getCloseEnoughTester( iOrder ):
    #
    def closeEnough( *t ):
        #
        if len( t ) == 1: t = t[0]
        #
        nOrig, nTest = t
        #
        return areClose( nOrig, nTest, 1.0 / 10 ** iOrder )
    #
    return closeEnough
    


if __name__ == "__main__":
    #
    from six            import print_ as print3
    #
    from Iter.AllVers   import lRange, tRange
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #

    if isEven( 11 ) or not isEven( 88 ):
        #
        lProblems.append( 'isEven()' )
        #
    if isOdd( 88 ) or not isOdd( 99 ):
        #
        lProblems.append( 'isOdd()' )
        #
    if isFloat( 2 ) or not isFloat( 8.8 ):
        #
        lProblems.append( 'isFloat()' )
        #
    if isInteger( 8.8 ) or not isInteger( 2 ):
        #
        lProblems.append( 'isInteger()' )
        #
    if isLong( 8.8 ) or not isLong( 88888888888888888888 ):
        #
        lProblems.append( 'isLong()' )
        #
    if          isNumber(      'abc' ) or \
            not isNumber(          2 ) or \
            not isNumber(        8.8 ) or \
            not isNumber( 8888888888 ):
        #
        lProblems.append( 'isNumber()' )
        #
    if          isWhole( 5.5 ) or \
            not isWhole( 5.0 ) or \
            not isWhole( 5   ):
        #
        lProblems.append( 'isWhole()' )
        #
    #
    if not hasIntegersOnly( tRange(9) ):
        #
        lProblems.append( 'hasIntegersOnly() integers only' )
        #
    #
    l = lRange(9)
    #
    l[5] = float( l[5] )
    #
    if hasIntegersOnly( l ):
        #
        lProblems.append( 'hasIntegersOnly() one float' )
        #
    #
    # both 9 and 11 are within 10% of 10
    #
    if (    not areClose( 10,  9, 10 ) or
            not areClose( 10, 11, 10 ) or
            not areClose( 10, 10, 10 ) or
                areClose( 10, 12, 10 ) or    
                areClose( 10,  8, 10 ) ):
        #
        print3( 'areClose( 10,  9, 10 ):', areClose( 10,  9, 10 ) )
        print3( 'areClose( 10, 11, 10 ):', areClose( 10, 11, 10 ) )
        print3( 'areClose( 10, 12, 10 ):', areClose( 10, 12, 10 ) )
        print3( 'areClose( 10,  8, 10 ):', areClose( 10,  8, 10 ) )
        lProblems.append( 'areClose()' )
        #
    #
    if getHowClose( 1, 1.05 ) != 'within 10%':
        #
        lProblems.append( 'getHowClose() within 10%' )
        #
    #
    if getHowClose( 1, 1.5 ) != 'not even within 10%':
        #
        lProblems.append( 'getHowClose() not even within 10%' )
        #
    #
    if getHowClose( 1, 1.000005 ) != 'within 0.001%':
        #
        print3( getHowClose( 1, 1.000005 ) )
        lProblems.append( 'getHowClose() within 0.001%' )
        #
    #
    if getHowClose( 1.000005, 1.000005 ) != 'identical':
        #
        lProblems.append( 'getHowClose() identical' )
        #
    #
    closeEnoughDot0 = getCloseEnoughTester( 0 )
    closeEnoughDot6 = getCloseEnoughTester( 6 )
    #
    if closeEnoughDot0( 1.0, 1.02 ):
        #
        lProblems.append( 'getCloseEnoughTester() not within 1%' )
        #
    #
    if not closeEnoughDot0( 1.0, 1.005 ):
        #
        lProblems.append( 'getCloseEnoughTester() within 1%' )
        #
    #
    if closeEnoughDot0( 1.0, 1.02 ):
        #
        lProblems.append( 'getCloseEnoughTester() not within 1%' )
        #
    #
    if not closeEnoughDot0( 1.0, 1.005 ):
        #
        lProblems.append( 'getCloseEnoughTester() within 1%' )
        #
    #
    if closeEnoughDot6( 1.0, 1.00000002 ):
        #
        lProblems.append( 'getCloseEnoughTester() not within 1%' )
        #
    #
    if not closeEnoughDot6( 1.0, 1.000000005 ):
        #
        lProblems.append( 'getCloseEnoughTester() within 1%' )
        #
    #
    #
    sayTestResult( lProblems )