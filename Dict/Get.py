#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# dict functions get
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

from Utils.Version  import PYTHON3

from Iter.Get import getIterSwapValueKey as _getIterSwapValueKey

if PYTHON3:
    #
    def getKeyIter( d ):
        #
        return d.keys()
    #
    def getValueIter( d ):
        #
        return d.values()
    #
    def getItemIter( d ):
        #
        return d.items()
    #
    def getKeyList( d ):
        #
        return list( d.keys() )
    #
    def getValueList( d ):
        #
        return list( d.values() )
    #
    def getItemList( d ):
        #
        return list( d.items() )
    #
    def getKeyTuple( d ):
        #
        return tuple( d.keys() )
    #
    def getValueTuple( d ):
        #
        return tuple( d.values() )
    #
    def getItemTuple( d ):
        #
        return tuple( d.items() )
    #
else:
    #
    def getKeyIter( d ):
        #
        return d.iterkeys()
    #
    def getValueIter( d ):
        #
        return d.itervalues()
    #
    def getItemIter( d ):
        #
        return d.iteritems()
    #
    def getKeyList( d ):
        #
        return d.keys()
    #
    def getValueList( d ):
        #
        return d.values()
    #
    def getItemList( d ):
        #
        return d.items()
    #
    def getKeyTuple( d ):
        #
        return tuple( d.iterkeys() )
    #
    def getValueTuple( d ):
        #
        return tuple( d.itervalues() )
    #
    def getItemTuple( d ):
        #
        return tuple( d.iteritems() )
    #
    


def getDictOffPairOfLists( lKeys, lValues ): # getDictOffTwoLists, getDictOff2Lists
    #
    from Iter.AllVers import iZip
    #
    return dict( iZip( lKeys, lValues ) ) # dict() new in 2.2



def _getTypicalValueIter( uTypicalValue = None ):
    #
    from copy import deepcopy
    #
    while True:
        #
        yield deepcopy( uTypicalValue )



def _getDictManuallyGotKeys( keys, uTypicalValue = None ):
    #
    """
    Return a dictionary with keys from keys and copies of uTypicalValue for values.
    dict.fromkeys doe not give you a copy, but the same value for each item.
    From this function, every item can have its own, separate list or other mutable.
    if the typical value is None or an immutable, use dict.fromkeys.
    """
    #
    dReturnDict                     = {}
    #
    if keys:
        #
        dReturnDict = getDictOffPairOfLists(
                        keys,
                        _getTypicalValueIter( uTypicalValue ) )
        #
    #
    return dReturnDict


def getDictGotKeys( keys, uTypicalValue = None ):
    #
    """
    Return a dictionary with keys from keys and copies of uTypicalValue for values.
    dict.fromkeys doe not give you a copy, but the same value for each item.
    From this function, every item can have its own, separate list or other mutable.
    if the typical value is None or an immutable, use dict.fromkeys.
    """
    #
    from Object.Test import isMutable
    #
    if isMutable( uTypicalValue ):
        #
        return _getDictManuallyGotKeys( keys, uTypicalValue )
        #
    else:
        #
        return dict.fromkeys( keys, uTypicalValue ) # new in python 2.3


def getDictOfListsOffItems( items ):
    #
    """
    Pass one list,
    each item is a list containing at least two items,
    the first goes in as the key.
    The value of the returned dict is a list,
    so the second goes in as an item in the list.
    First items do not need to be unique,
    as values get appended and are not overwritten."""
    #
    dReturn     = {}
    #
    for k, v in items:
        #
        dReturn.setdefault( k, [] ).append( v )
        #
    #
    return dReturn



def _getDictOffKwargs(**kwargs):
    """
    Python Cookbook example
    "Contructing a Dictionary without Excessive Quoting"!
    but 2.3 made this obsolete
    a = dict(one=1, two=2, three=3)
    """
    return kwargs




def getReverseDictGotUniqueItems( dOrig ):
    #
    """Return a dictionary with the values as keys and the keys as values.
    Since you claim the values are unique, in the returned reverse dictionary,
    the original keys are the new values."""
    #
    return dict( _getIterSwapValueKey( getItemIter( dOrig ) ) )



def getReverseDict( dOrig ):
    #
    """Return a dictionary with the values as keys and the keys as values.
    Since the values may not be unique, in the returned reverse dictionary,
    the original keys are in a list for each unique original value."""
    #
    return getDictOfListsOffItems( _getIterSwapValueKey( getItemIter( dOrig ) ) )



def getReverseDictCarefully( dOrig ):
    #
    """Return a dictionary with the values as keys and the keys as values.
    Since the values may not be unique, in the returned reverse dictionary,
    the original keys are in a list for each unique original value.
    This is done CAREFULLY where the original values may be tuples or strings."""
    #
    lValueuKeys = []
    #
    for uKey, uValue in getItemIter( dOrig ):
        #
        if type( uValue ) == tuple:
            #
            for sValue in uValue:
                #
                lValueuKeys.append( ( sValue, uKey ) )
                #
            #
        else:
            #
            lValueuKeys.append( ( uValue, uKey ) )
    #
    dValueKeys = {}
    #
    for sValue, uKey in lValueuKeys:
        #
        if not sValue in dValueKeys: dValueKeys[ sValue ] = []
        #
        dValueKeys[ sValue ].append( uKey )
    #
    return dValueKeys




def getIndexLookupDict( seq ):
    #
    '''
    this could speed things up if you must look up lots of indexes in a long list
    pass the list to this function
    this function returns a dictionary
    the items are the keys and the list indicies are the values
    so the index look ups go much faster
    '''
    #
    lItemIndex      = _getIterSwapValueKey( enumerate( seq ) )
    #
    return dict( lItemIndex )


def getIntersectingKeys( d1, d2 ):
    #
    # fasest solution from "Finding the Intersection of Two Dictionaries", 1st Python Cookbook
    #
    # not used anywhere yet
    #
    return  [ k for k in d1 if k in d2 ]


def getDictSubset( dOrig, *args ):
    #
    '''
    get a new dictionary that has subset of the keys in the original
    say you have dOrig as {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}
    getDictSubset( d, 'a', 'b', 'c' ) returns
    nNew as {'a': 1, 'b': 2, 'c': 3}
    '''
    #
    dNew = {}
    #
    for k in args:
        #
        dNew[ k ] = dOrig.get( k )
        #
    #
    return dNew




if __name__ == "__main__":
    #
    from six            import print_ as print3
    from six            import next   as getNext
    #
    from Collect.Test   import hasAny
    from Iter.AllVers   import iMap, tMap, iRange, tRange, iZip, lZip
   #from Utils.Both2n3  import getNext
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    tTest0 = tRange( 10 )
    tTestA = tMap( chr, iRange( 97, 107 ) )
    #
    dTest0 = dict( iZip( tTestA, tTest0 ) )
    dTest1 = _getDictOffKwargs( a=10, b=11, c=12, d=13, e=14, f=15, g=16, h=17, i=18, j=19 )
    #
    lTest01= lZip( tTestA, tTest0 )
    #
    lTest01.extend( getItemIter( dTest1 ) )
    #
    lOrigKeys  = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j' ]
    lOrigVals  = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
    lOrigItems = lZip( lOrigKeys, lOrigVals )
    #
    lTestKeys  = list( getKeyIter( dTest0 ) )
    lTestKeys.sort()
    #
    if lTestKeys != lOrigKeys:
        #
        lProblems.append( 'getKeyIter()' )
        #
    #
    lTestVals  = list( getValueIter( dTest0 ) )
    lTestVals.sort()
    #
    if lTestVals != lOrigVals:
        #
        lProblems.append( 'getKeyIter()' )
        #
    #
    lTestItems = list( getItemIter( dTest0 ) )
    lTestItems.sort()
    #
    if lTestItems != lOrigItems:
        #
        lProblems.append( 'getKeyIter()' )
        #
    #
    lTestKeys  = getKeyList( dTest0 )
    lTestKeys.sort()
    #
    if lTestKeys != lOrigKeys:
        #
        lProblems.append( 'getKeyIter()' )
        #
    #
    lTestVals  = getValueList( dTest0 )
    lTestVals.sort()
    #
    if lTestVals != lOrigVals:
        #
        lProblems.append( 'getKeyIter()' )
        #
    #
    lTestItems = getItemList( dTest0 )
    lTestItems.sort()
    #
    if lTestItems != lOrigItems:
        #
        lProblems.append( 'getKeyIter()' )
        #
    #
    lTestKeys  = list( getKeyTuple( dTest0 ) )
    lTestKeys.sort()
    #
    if lTestKeys != lOrigKeys:
        #
        lProblems.append( 'getKeyIter()' )
        #
    #
    lTestVals  = list( getValueTuple( dTest0 ) )
    lTestVals.sort()
    #
    if lTestVals != lOrigVals:
        #
        lProblems.append( 'getKeyIter()' )
        #
    #
    lTestItems = list( getItemTuple( dTest0 ) )
    lTestItems.sort()
    #
    if lTestItems != lOrigItems:
        #
        lProblems.append( 'getKeyIter()' )
        #
    #
    #
    dOfLists = getDictOfListsOffItems( lTest01 )
    #
    if dOfLists != \
            {'a': [0, 10], 'b': [1, 11], 'c': [2, 12], 'd': [3, 13], 'e': [4, 14],
             'f': [5, 15], 'g': [6, 16], 'h': [7, 17], 'i': [8, 18], 'j': [9, 19]}:
        #
        print3( dOfLists )
        lProblems.append( 'getDictOfListsOffItems()' )
        #
    #
    if getDictOffPairOfLists( tTest0, tTestA ) != \
            {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j'}:
        #
        lProblems.append( 'getDictOffPairOfLists()' )
        #
    #
    tTypicals = ( [], {}, set([]) )
    #
    lIters = iMap( _getTypicalValueIter, tTypicals )
    #
    tVals = tMap( getNext, lIters )
    #
    if tTypicals != tVals:
        #
        lProblems.append( '_getTypicalValueIter() d/n get typical values' )
        #
    #
    def isIs( t ): return t[0] is t[1]
    #
    if False in tMap( isIs, iZip( range(5), range(5) ) ):
        #
        lProblems.append( 'isIs() not working' )
        #
    #        
    if hasAny( iMap( isIs, iZip( tTypicals, tVals ) ) ):
        #
        lProblems.append( '_getTypicalValueIter() got same objects' )
        #
    #
    if _getDictManuallyGotKeys( tTestA ) != getDictOffPairOfLists( tTestA, [ None ] * 10 ):
        #
        lProblems.append( '_getDictManuallyGotKeys()' )
        #
    if getDictGotKeys( tTestA ) != getDictOffPairOfLists( tTestA, [ None ] * 10 ):
        #
        lProblems.append( 'GetDictGotKeys()' )
        #
    if _getDictOffKwargs( a=0, b=1, c=2, d=3, e=4, f=5, g=6, h=7, i=8, j=9 ) != \
            dTest0:
        #
        lProblems.append( '_getDictOffKwargs()' )
        #
    if getReverseDict( dTest0 ) != \
            {0:['a'],1:['b'],2:['c'],3:['d'],4:['e'],5:['f'],6:['g'],7:['h'],8:['i'],9:['j']}:
        #
        lProblems.append( 'getReverseDict()' )
        #
    #
    if getReverseDictGotUniqueItems( dTest0 ) != \
            {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h',8:'i',9:'j'}:
        #
        lProblems.append( 'getReverseDictGotUniqueItems()' )
        #
    #    
    dTestT = {'a': 0, 'c': (2,10), 'b': 1, 'e': 4, 'd': 3, 'g': 6, 'f': 5, 'i': 8, 'h': 7, 'j': 9}
    #
    if getReverseDictCarefully( dTestT ) != \
            {   0: ['a'], 1: ['b'], 2: ['c'], 3: ['d'], 4: ['e'],
                5: ['f'], 6: ['g'], 7: ['h'], 8: ['i'], 9: ['j'], 10: ['c']}:
        #
        lProblems.append( 'getReverseDictCarefully()' )
        #
    if getIndexLookupDict( tTestA  ) != getDictOffPairOfLists( tTestA, tTest0 ):
        #
        lProblems.append( 'getIndexLookupDict()' )
        #
    #
    dTest1 = dict( a = 1, b = 2, c = 3, d = 4, e = 5, f = 6 )
    dTest2 = dict( e = 1, f = 2, g = 3, h = 4, i = 5, j = 6 )
    #
    lKeys = getIntersectingKeys( dTest1, dTest2 )
    lKeys.sort()
    #
    if lKeys != ['e', 'f']:
        #
        lProblems.append( 'getIntersectingKeys()' )
        #
    #
    dOrig = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}
    dWant = {'a': 1, 'b': 2, 'c': 3}
    #
    if getDictSubset( dOrig, 'a', 'b', 'c' ) != dWant:
        #
        lProblems.append( 'getDictSubset()' )
        #
    #
    #
    sayTestResult( lProblems )