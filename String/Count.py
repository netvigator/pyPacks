#!/home/rick/.local/bin/pythonTest
# -*- coding: utf-8 -*-
#
# string functions Count
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


try:
    from ..String.Dumpster  import getDigitsOnly, getAlphaNumCleanNoSpaces
    from ..String.Split     import SplitRegular, SplitC
except ( ValueError, ImportError ):
    from String.Dumpster    import getDigitsOnly, getAlphaNumCleanNoSpaces
    from String.Split       import SplitRegular, SplitC


def CountRegular( s, sCountThese ): return s.count( sCountThese )

def CountSplit(   s, sCountThese ):
    #
    #
    return len( SplitRegular( s, sCountThese ) ) - 1

def CountSplitC(  s, sCountThese ):
    #
    #
    return len( SplitC(       s, sCountThese ) ) - 1


def OccursIn( sSearchIn, sSearchFor ):
    #
    """
    Returns how many times sSearchFor can be found in sSearchIn.
    Performs a case-sensitive search.
    """
    #
    return CountSplit( sSearchIn, sSearchFor )


def OccursInC( sSearchIn, sSearchFor ):
    #
    """
    Returns how many times sSearchFor can be found in sSearchIn.
    Performs a search that is not case-sensitive.
    """
    #
    return CountSplitC( sSearchIn, sSearchFor )


def getDigitCount( s ):
    #
    #
    return len( getDigitsOnly( s ) )


def getAlphaNumCount( s ):
    #
    #
    return len( getAlphaNumCleanNoSpaces( s ) )



if __name__ == "__main__":
    #
    from Utils.Both2n3  import print3
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    sTest       = 'aABabcABCDabcdeABCDEF'
    #
    if CountRegular( sTest, 'A' ) != 3:
        #
        lProblems.append( 'CountRegular()' )
        #
    if CountSplit( sTest, 'AB' ) != 3:
        #
        lProblems.append( 'CountSplit()' )
        #
    if CountSplitC( sTest, 'AB' ) != 5:
        #
        lProblems.append( 'CountSplitC()' )
        #
    if OccursIn( sTest, 'AB' ) != 3:
        #
        lProblems.append( 'OccursIn()' )
        #
    if OccursInC( sTest, 'AB' ) != 5:
        #
        lProblems.append( 'OccursInC()' )
        #
    #
    if getDigitCount( '1 (800) 555-1212' ) != 11:
        #
        lProblems.append( 'getDigitCount()' )
        #
    #
    if getAlphaNumCount( 'Melrose 2 1212' ) != 12:
        #
        lProblems.append( 'getAlphaNumCount()' )
        #
    #
    sayTestResult( lProblems )
