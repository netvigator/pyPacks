#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# dict functions Lists
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
from Dict.Get import getItemIter


def getListOfListsOffDictOfLists( dLists ):
    #
    # this flattens a *DICTIONARY* -- see also getListFromNestedLists
    #
    lCombos = [ ( uKey, uItem ) for uKey, lList in getItemIter( dLists ) for uItem in lList ]
    #
    return lCombos



def getListOfListsOffDictOfDicts( dDicts ):
    #
    from Collect.Get    import getListOfListsFromNestedLists
    from Dict.Get       import getItemTuple
    #
    lListOfLists = [ ( uKey, getItemTuple( d ) )
                     for uKey, d
                     in getItemTuple( dDicts ) ]
    #
    lFlat        = getListOfListsFromNestedLists( lListOfLists )
    #
    return lFlat



def getDictKeysValuesSortedKeyOrder( d ):
    #
    from Iter.AllVers   import lMap
    from Dict.Get       import getKeyList
    #
    lKeys   = getKeyList( d )
    #
    lKeys.sort()
    #
    return lKeys, lMap( d.__getitem__, lKeys )



def getDictValuesSortedKeyOrder( d ):
    #
    lKeys, lValues = getDictKeysValuesSortedKeyOrder( d )
    #
    return lValues






if __name__ == "__main__":
    #
    from six            import print_ as print3
    #
    from Iter.AllVers   import tMap, iRange, tRange, lZip
    from Dict.Get       import getDictOfListsOffItems, getDictOffPairOfLists
    from Utils.Result   import sayTestResult
    #
    tTest0 = tRange( 10 )
    tTestA = tMap( chr, iRange( 97, 108 ) )
    #
    dTest0 = getDictOffPairOfLists(  tTestA, tTest0 )
    dTest1 = dict( a=10, b=11, c=12, d=13, e=14, f=15, g=16, h=17, i=18, j=19 )
    #
    lTest01= lZip( tTestA, tTest0 )
    #
    lTest01.extend( getItemIter( dTest1 ) )
    #
    lProblems = []
    #
    lRef  = [('a', 0), ('a', 10), ('b', 1), ('b', 11), ('c', 2), ('c', 12),
             ('d', 3), ('d', 13), ('e', 4), ('e', 14), ('f', 5), ('f', 15),
             ('g', 6), ('g', 16), ('h', 7), ('h', 17), ('i', 8), ('i', 18),
             ('j', 9), ('j', 19)]
    #
    lLofL = getListOfListsOffDictOfLists( getDictOfListsOffItems( lTest01 ) )
    #
    lLofL.sort()
    #
    if lLofL != lRef:
        #
        lProblems.append( 'getListOfListsOffDictOfLists()' )
        #
    #
    #
    dDicts = dict( A = dTest1, B = dTest0 )
    #
    lExpecting = [
            ['A', 'a', 10], ['A', 'c', 12], ['A', 'b', 11], ['A', 'e', 14],
            ['A', 'd', 13], ['A', 'g', 16], ['A', 'f', 15], ['A', 'i', 18],
            ['A', 'h', 17], ['A', 'j', 19],
            ['B', 'a',  0], ['B', 'c',  2], ['B', 'b',  1], ['B', 'e',  4],
            ['B', 'd',  3], ['B', 'g',  6], ['B', 'f',  5], ['B', 'i',  8],
            ['B', 'h',  7], ['B', 'j',  9]]
    #
    lResult = getListOfListsOffDictOfDicts( dDicts )
    #
    lExpecting.sort()
    lResult.sort()
    #
    if lResult  != lExpecting:
        #
        print3( lResult )
        lProblems.append( 'getListOfListsOffDictOfDicts()' )
        #
    #
    if getDictKeysValuesSortedKeyOrder( dTest1 ) != \
            (['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'],
             [10,  11,  12,  13,  14,  15,  16,  17,  18,  19]):
        #
        lProblems.append( 'getDictKeysValuesSortedKeyOrder()' )
        #
    if getDictValuesSortedKeyOrder( dTest1 ) != \
            [10,  11,  12,  13,  14,  15,  16,  17,  18,  19]:
        #
        lProblems.append( 'getDictValuesSortedKeyOrder()' )
        #

    #
    sayTestResult( lProblems )