#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# dict functions Numbs#
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


def getDictOfCountsOffDictOfLists( dDictOfLists ):
    #
    """
    dict of lists dictionary: values are lists
    counts the number of items in the list
    returns dict, keys are same as original
    values are len( Value List ) for each key
    """
    #
    from copy import copy
    #
    dDictofCounts   = copy( dDictOfLists )
    #
    for uKey in dDictofCounts:
        #
        try:
            dDictofCounts[ uKey ] = len( dDictofCounts[ uKey ] )
        except TypeError:
            dDictofCounts[ uKey ] = 0
        #
    #
    #
    return dDictofCounts



def getDictOfSumsOffDictOfLists( dDictOfLists ):
    #
    from Collect.Get    import getNewValuesIter4Items
    from Numb.Get       import getSumOffList
    from Dict.Get       import getItemIter
    #
    iterTotals = getNewValuesIter4Items(
                getItemIter( dDictOfLists ), getSumOffList )
    #
    return dict( iterTotals )


def _isValNonZero( t ): return t[1]


def getDictOfAvgsOffDictOfLists( dDictOfLists ):
    #
    from Iter.AllVers   import iZip, iFilter
    from Collect.Get    import unZip
    from Dict.Get       import getItemIter
    #
    dDictOfSums     = getDictOfSumsOffDictOfLists( dDictOfLists )
    #
    dDictOfCounts   = getDictOfCountsOffDictOfLists( dDictOfLists )
    #
    #lKeysCounts     = [ t for t in getItemIter( dDictOfCounts ) if t[1] > 0 ]
    #
    #lKeys, lCounts  = unZip( lKeysCounts )
    #
    lKeys, lCounts  = unZip(
                        iFilter( _isValNonZero,
                                 getItemIter( dDictOfCounts ) ) )
    
    lSums           = [ dDictOfSums[ uKey ] for uKey in lKeys ]
    #
    lAvgs           = [ t[0] / float( t[1] ) for t in iZip( lSums, lCounts ) ]
    #
    lKeysAvgs       = iZip( lKeys, lAvgs )
    #
    return dict( lKeysAvgs )



def getDictOfCountsOffList( lList ):
    #
    '''pass a sequence
    returns a dictionary of counts

    '''
    dCounts = {}
    #
    for uItem in lList:
        #
        dCounts[ uItem ] = dCounts.setdefault( uItem, 0 ) + 1
        #
    #
    return dCounts


def getValuesAdded( dMain, dMore ):
    #
    '''pass two dictionaries, dMain and dMore
    function modifies dMain and returns None (dMore is unmodified)
    for each k, v in dMore, v is added to value for same k in dMain
    if k is not in dMain, k and v from dMore are added to dMain
    '''
    #
    from Dict.Get import getKeyIter
    #
    for k in getKeyIter( dMore ):
        #
        dMain[ k ] = dMain.setdefault( k, 0 ) + dMore[ k ]



if __name__ == "__main__":
    #
    lProblems = []
    #
    from six            import print_ as print3
    #
    from Collect.Get    import getListFromNestedLists
    from Iter.AllVers   import tMap, iRange
    from Utils.Result   import sayTestResult
    #
    def getChar( i ): return chr( 97 + i )
    #
    dTest   = dict(
                    a=[1,2,3,4,5,6,7,8,9,10],
                    b=  [2,3,4,5,6,7,8,9,10],
                    c=    [3,4,5,6,7,8,9,10],
                    d=      [4,5,6,7,8,9,10],
                    e=        [5,6,7,8,9,10],
                    f=          [6,7,8,9,10],
                    g=            [7,8,9,10],
                    h=              [8,9,10],
                    i=                [9,10],
                    j=                  [10] )
    #
    if getDictOfCountsOffDictOfLists( dTest ) != \
            {'a':10,'b':9,'c':8,'d':7,'e':6,'f':5,'g':4,'h':3,'i':2,'j':1}:
        #
        lProblems.append( 'getDictOfCountsOffDictOfLists()' )
        #
    if getDictOfSumsOffDictOfLists( dTest ) != \
            {'a':55,'b':54,'c':52,'d':49,'e':45,
             'f':40,'g':34,'h':27,'i':19,'j':10}:
        #
        lProblems.append( 'getDictOfSumsOffDictOfLists()' )
        #
    if getDictOfAvgsOffDictOfLists( dTest ) != \
            {'a':5.5,'b':6.0,'c':6.5,'d':7.0,'e': 7.5,
             'f':8.0,'g':8.5,'h':9.0,'i':9.5,'j':10.0}:
        #
        # print3( getDictOfAvgsOffDictOfLists( dTest ) )
        lProblems.append( 'getDictOfAvgsOffDictOfLists()' )
        #
    #
    lChars = getListFromNestedLists( [ tMap( getChar, iRange(i) ) for i in iRange(10) ] )
    #
    dChars = getDictOfCountsOffList( lChars )
    #
    if dChars != \
            {   'a': 9,
                'b': 8,
                'c': 7,
                'd': 6,
                'e': 5,
                'f': 4,
                'g': 3,
                'h': 2,
                'i': 1 }:
        #
        lProblems.append( 'getDictOfCountsOffList()' )
        #
    #
    dTotals = {}
    #
    getValuesAdded( dTotals, dChars )
    getValuesAdded( dTotals, dChars )
    #
    if dTotals != \
            {   'a': 2 * 9,
                'b': 2 * 8,
                'c': 2 * 7,
                'd': 2 * 6,
                'e': 2 * 5,
                'f': 2 * 4,
                'g': 2 * 3,
                'h': 2 * 2,
                'i': 2 * 1 }:
        #
        lProblems.append( 'getDictOfCountsOffList()' )
        #
    #
    sayTestResult( lProblems )