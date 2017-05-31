#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Collection functions Query
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


def get1stThatMeets( iterable, fCondition = bool ):
    #
    """
    this stops testing after finding one list member that meets the condition.
    """
    #
    from six            import next as getNext
    #
    from Iter.AllVers   import iFilter
   #from Utils.Both2n3  import getNext
    #
    uReturn = None
    #
    try:
        #
        uReturn = getNext( iFilter( fCondition, iterable ) )
        #
    except ( TypeError, StopIteration ):
        #
        pass
        #
    #
    return uReturn


# def get1stTrue( iterable ): return get1stThatMeets( iterable )

get1stTrue = get1stThatMeets


def get1stThatFails( iterable, fCondition = bool ):
    #
    """
    this stops testing after finding one list member that fails the condition.
    """
    #
    def failure( u ): return not fCondition( u )
    #
    return get1stThatMeets( iterable, failure )


# def get1stFalse( iterable ): return get1stThatFails( iterable )

get1stFalse = get1stThatFails



def getBegAndEndIfInOrder( seq1, seq2 ):
    #
    '''
    getBegAndEndIfInOrder( 'Kimberley', 'Kimberly' ) returns 'Kimberly'
    getBegAndEndIfInOrder( 'anna',      'deanna'   ) returns 'anna'
    getBegAndEndIfInOrder( 'Kimberley', 'Joe'      ) returns empty string
    '''
    #
    from Iter.AllVers import iRange
    #
    iLen1, iLen2 = len( seq1 ), len( seq2 )
    #
    iBegMatch = None
    iEndMatch = None
    #
    for i in iRange( min( iLen1, iLen2 ) ):
        #
        if seq1[ i ] != seq2[ i ]:
            #
            break
            #
        iBegMatch = i + 1
        #
    #
    iLast = min( iLen1, iLen2 )
    #
    if max( iLen1, iLen2 ) > iLast: iLast += 1
    #
    for i in iRange( -1, - iLast, -1 ):
        #
        if seq1[ i ] != seq2[ i ]:
            #
            break
        #
        iEndMatch = i
    #
    returnSeq = seq1[ 0 : 0 ]
    #
    if iBegMatch is not None: returnSeq  = seq1[ : iBegMatch   ]
    if iEndMatch is not None: returnSeq += seq1[   iEndMatch : ]
    #
    return returnSeq



if __name__ == "__main__":
    #
    from string import digits
    from string import ascii_letters as letters
    #
    from Iter.AllVers   import iRange, tRange
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    #
    def GotA( c ): return c == 'A'
    #
    if get1stThatMeets( letters, GotA ) != 'A':
        #
        lProblems.append( 'get1stThatMeets()' )
        #
    #
    tMostlyZeros = ( 0, 0, 0, 8, 0 )
    #
    if get1stTrue( tMostlyZeros ) != 8:
        #
        lProblems.append( 'get1stTrue()' )
        #
    #
    if get1stThatFails( letters, GotA ) != 'a':
        #
        lProblems.append( 'get1stThatFails() a aint A' )
        #
    #
    if get1stThatFails( digits, GotA ) != '0':
        #
        lProblems.append( 'get1stThatFails() zero aint A' )
        #
    #
    if get1stThatFails( letters ):
        #
        # nothing should fail
        #
        lProblems.append( 'get1stThatFails() letters' )
        #
    #
    tSomeDigits = ( 8, 7, 6, 5, 4, 0, 2, 1 )
    #
    if get1stFalse( tSomeDigits ) != 0:
        #
        lProblems.append( 'get1stFalse() got 0' )
        #
    #    
    tSomeDigits = tRange( 8 )[ 1 : ]
    #
    if get1stFalse( tSomeDigits ) is not None:
        #
        lProblems.append( 'get1stFalse() no False among non-zero digits' )
        #
    #    
    if      getBegAndEndIfInOrder( 'Kimberley', 'Kimberly' ) != 'Kimberly' or \
            getBegAndEndIfInOrder( 'Kimberley', 'Joe' ) or \
            getBegAndEndIfInOrder( 'anna', 'deanna' ) != 'anna':
        #
        lProblems.append( 'getBegAndEndIfInOrder()' )
        #
    #
    sayTestResult( lProblems )