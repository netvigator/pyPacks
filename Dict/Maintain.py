#!/home/rick/bin/pythonTest
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
#   http://www.gnu.org/licenses/
#
# Copyright 2004-2020 Rick Graves
#
try:
    from .Get               import getKeyTuple
    from ..Numb.Test        import isOdd
    from ..Utils.TimeTrial  import TimeTrial
except ( ValueError, ImportError ):
    from Dict.Get           import getKeyTuple
    from Numb.Test          import isOdd
    from Utils.TimeTrial    import TimeTrial


def _isFalse( u ): return not u


def purgeFalseValueItems( d, fTest = _isFalse ):
    #
    lKeysPurgeValues = [ k for k in d if fTest( d[ k ] ) ]
    #
    for k in lKeysPurgeValues:
        #
        del d[ k ]
        #


def _isNone( u ): return u is None


def purgeNoneValueItems( d ):
    #
    purgeFalseValueItems( d, fTest = _isNone )



def _isNegative( n ): return n < 0


def purgeNegativeValueItems( d ):
    #
    purgeFalseValueItems( d, fTest = _isNegative )




def getDictValuesFromSingleElementLists( d ):
    #
    '''some dicts come to you with single element lists for every value
    this gets the values out of the lists'''
    #
    for k in d:
        #
        if isinstance( d[k], list ) and len( d[k] ) == 1:
            #
            d[k] = d[k][0]
            #
        if isinstance( d[k], dict ):
            #
            # recursive call coming up!
            #
            getDictValuesFromSingleElementLists( d[k] )
    #


def _doTimeTrial():
    #
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
    TimeTrial( purgeFalseValueItems, dTest )
    #
    TimeTrial( purgeNegativeValueItems, dTest )


if __name__ == "__main__":
    #
    lProblems = []
    #
    from copy           import copy, deepcopy
    from pprint         import pprint
    #
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
    purgeFalseValueItems( dTest1 )
    #
    if dTest1 != dTest0 or dTest2 == dTest0:
        #
        lProblems.append( 'purgeFalseValueItems()' )
        #
    #
    dTest1 = copy( dTestA )
    #
    dTest2 = {}
    #
    for k, v in dTestA.items():
        if v is not None:
            dTest2[k] = v
    #
    purgeNoneValueItems( dTest1 )
    #
    if dTest1 != dTest2 or dTest2 == dTest0:
        #
        lProblems.append( 'purgeNoneValueItems()' )
        #
    #
    dTestA[ 'k' ] = -1
    dTestA[ 'm' ] = -2
    dTestA[ 'n' ] = -3
    dTestA[ 'o' ] = -4
    #
    dTest1 = copy( dTestA )
    dTest2 = copy( dTestA )
    #
    purgeNegativeValueItems( dTest1 )
    #
    if dTest1 != dTest0 or dTest2 == dTest0:
        #
        lProblems.append( 'purgeNegativeValueItems()' )
        #
    #
    dLevel3 = dict( aaa=[110], bbb=[111], ccc=[112], ddd=[113], eee=[114] )
    dLevel2 = dict( aa =[ 10], bb =[ 11], cc =[ 12], dd =[ 13], ee = [dLevel3])
    dLevel1 = dict( a  =[  0], b  =[  1], c  =[  2], d  =[  3], e  =  dLevel2 )
    #
    dNestedWithSingleElementListValues = deepcopy( dLevel1 )
    #
    dLevel3 = dict( aaa= 110,  bbb= 111,  ccc= 112,  ddd= 113,  eee= 114  )
    dLevel2 = dict( aa =  10,  bb =  11,  cc =  12,  dd =  13,  ee = dLevel3 )
    dLevel1 = dict( a  =   0,  b  =   1,  c  =   2,  d  =   3,  e  = dLevel2 )
    #
    getDictValuesFromSingleElementLists( dNestedWithSingleElementListValues )
    #
    if dNestedWithSingleElementListValues != dLevel1:
        #
        lProblems.append( 'getDictValuesFromSingleElementLists()' )
        #
    #
    
    sayTestResult( lProblems )
