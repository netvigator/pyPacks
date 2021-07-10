#!/home/rick/bin/pythonTest
# -*- coding: utf-8 -*-
#
# myCrypto functions Math
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
# Copyright 2021 Rick Graves
#


def getGCD( bigger, smaller ):
    #
    '''get the Greatest Common Denominator of 2 integers
    using the Extended Euclidean Algorithm
    GCD( r0, r1 ) = s*r0 + t*r1
    want to find GCD also s & t'''
    #
    if smaller > bigger:
        #
        bigger, smaller = smaller, bigger
        #
    #
    iList = [ bigger, smaller ] # integers list, starting with these two
    #
    sList  = [ 1, 0 ] # initial values are given
    tList  = [ 0, 1 ] # proof is available
    #
    r = smaller # initialize to start while loop, throw away value
    #
    while r > 0:
        #
        q = iList[-2] // iList[-1]
        #
        s = sList[-2] - q * sList[-1]
        #
        t = tList[-2] - q * tList[-1]
        #
        r = ( s * iList[0] ) + ( t * iList[1] ) # remainder
        #
        iList.append( r )
        sList.append( s )
        tList.append( t )
        #
    #
    # last one is a zero remainder, prior values are the ones we need
    #
    gcd, s, t = iList[-2], sList[-2], tList[-2]
    #
    return gcd, s, t


if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if getGCD( 973, 301 ) != (7, 13, -42):
        #
        # 13 * 973 - 42 * 301 = 7
        #
        lProblems.append( 'getGCD( 973, 301 )' )
        #
    #
    # wikipedia example
    if getGCD( 46, 240 )!= (2, -9, 47):
        #
        # -9 * 240 + 47 * 46 = 2
        #
        lProblems.append( 'getGCD( 46, 240 )' )
        #
    #
    #
    sayTestResult( lProblems )

