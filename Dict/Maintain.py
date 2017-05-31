#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# dict functions Maintain
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
# Copyright 2004-2012 Rick Graves
#


def removeBlankValues( d ):
    #
    lKeysBlankValues = [ k for k in d if not d[ k ] ]
    #
    for k in lKeysBlankValues:
        #
        del d[ k ]
        #

def purgeNegativeValueMembers( d ):
    #
    '''
    getItemList & getKeyTuple versions were slower than removeBlankValues
    per TimeTrial with 256 length dictionary
    '''
    #
    from Dict.Get import getKeyTuple
    #
    for k in getKeyTuple( d ):
        #
        if not d[k]: del d[ k ]
        #
    #

purgeNegativeValueMembers = removeBlankValues


def _doTimeTrial():
    #
    from Numb.Test       import isOdd
    from Utils.TimeTrial import TimeTrial
    #
    dTest = {}
    #
    for i in range( 256 ):
        #
        if isOdd( i ):
            dTest[i] = chr(i)
        else:
            dTest[i] = ''
        #
        #
    #
    TimeTrial( removeBlankValues, dTest )
    #
    TimeTrial( purgeNegativeValueMembers, dTest )


if __name__ == "__main__":
    #
    lProblems = []
    #
    from copy           import copy
    from Utils.Result   import sayTestResult
    #
    dTest0 = dict( a=10, b=11, c=12, d=13, e=14, f=15, g=16, h=17, i=18, j=19 )
    dTestA = dict( a=10, b=11, c=12, d=13, e=14, f=15, g=16, h=17, i=18, j=19 )
    #
    dTestA[ 'k' ] = None
    dTestA[ 'm' ] = []
    dTestA[ 'n' ] = {}
    dTestA[ 'o' ] = ''
    #
    dTest1 = copy( dTestA )
    dTest2 = copy( dTestA )
    #
    removeBlankValues( dTest1 )
    #
    if dTest1 != dTest0 or dTest2 == dTest0:
        #
        lProblems.append( 'removeBlankValues()' )
        #
    #
    dTest1 = copy( dTestA )
    dTest2 = copy( dTestA )
    #
    purgeNegativeValueMembers( dTest1 )
    #
    if dTest1 != dTest0 or dTest2 == dTest0:
        #
        lProblems.append( 'purgeNegativeValueMembers()' )
        #
    #
    sayTestResult( lProblems )