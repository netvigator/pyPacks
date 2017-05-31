#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# dict functions DictList
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

"""
DictList = list of dictionaries
like what you get from some database queries
each row is a dictionary, column names are the keys,
column contents are the values
"""

from Iter.AllVers import iZip
from Utils.Get    import getTrue


def _WipeNull( s ):
    #
    if s == 'NULL': s = ''
    #
    return s


def getDictListFields( d, oFields, bWipeNulls = False ):
    #
    """
    To sort a list fast on some component,
    the fasted approach (according to the cookbook) is typically
    "Decorate, Sort, Undecorate".
    """
    #
    from Iter.AllVers import iMap
    #
    # need single quotes inside CSV out looks OK in spreadsheets
    # 2012-08-15
    #
    l = [ d.get( sFieldName, "'%s' not found!" % sFieldName )
          for sFieldName in oFields ]
    #
    if bWipeNulls:
        #
        l = iMap( _WipeNull, l )
        #
    #
    return tuple( l )


def getListOfDictListFields( lDictList, oFields, fCondition = getTrue ):
    #
    """To sort a list fast on some component,
    the fasted approach (according to the cookbook) is typically
    "Decorate, Sort, Undecorate".
    """
    #
    if type( oFields ) == type( '' ):
        #
        def getFields( d, tDump ): return d[ oFields ]
        #
    elif len( oFields ) == 1:
        #
        def getFields( d, tDump ): return d[ oFields[0] ]
        #
    elif len( oFields ) == 2:
        #
        def getFields( d, tDump ): return d[ oFields[0] ], d[ oFields[1] ]
        #
    elif len( oFields ) == 3:
        #
        def getFields( d, tDump ): return d[ oFields[0] ], d[ oFields[1] ], d[ oFields[2] ]
        #
    else:
        #
        getFields = getDictListFields
    #
    #
    if fCondition is getTrue or fCondition is None:
        #
        return [ getFields( d, oFields ) for d in lDictList ]
        #
    else:
        #
        return [ getFields( d, oFields ) for d in lDictList if fCondition( d ) ]



def getDecoratedDictIter(
        lDictList, oFields,
        fCondition  = None,
        bOneColOnly = False ):
    #
    """
    this decorates each dict with a tuple of certain values
    returns an iterator of all the dicts in the list
    
    To sort a list fast on some component,
    the fasted approach (according to the cookbook) is typically
    "Decorate, Sort, Undecorate".
    but you cannot sort an iterator like this function returns
    """
    #
    # not self tested but getDecoratedDictList is
    #
    if fCondition is None: fCondition = getTrue
    #
    if bOneColOnly and not isinstance( oFields, str ):
        #
        bIsFirst = True
        #
        for d in lDictList:
            #
            if not fCondition( d ): continue
            #
            if bIsFirst:
                #
                for s in oFields:
                    if s in d: break
                #
                bIsFirst = False
                #
            #
            yield ( d.get( s ), d )
            #
        #
    elif isinstance( oFields, str ):
        #
        for d in lDictList:
            #
            if not fCondition( d ): continue
            #
            yield ( d.get( oFields ), d )
            #
        #
    else:
        #
        for d in lDictList:
            #
            if not fCondition( d ): continue
            #
            yield ( tuple( [ d.get( s ) for s in oFields ] ), d )



def getDecoratedDictList(
        lDictList, oFields,
        fCondition  = getTrue,
        bOneColOnly = False ):
    #
    """
    this decorates each dict with a tuple of certain values
    returns an list of all the dicts in the list
    
    To sort a list fast on some component,
    the fasted approach (according to the cookbook) is typically
    "Decorate, Sort, Undecorate".
    """
    #
    return list( getDecoratedDictIter(
                    lDictList, oFields, fCondition, bOneColOnly ) )




def _getTupleOfDictListFieldTuples(
            lDictList, oFieldsL, oFieldsR,
            fConditionL = getTrue, fConditionR = getTrue ):
    #
    from Iter.AllVers import tZip
    #
    lFieldsL    = getListOfDictListFields( lDictList, oFieldsL, fConditionL )
    #
    lFieldsR    = getListOfDictListFields( lDictList, oFieldsR, fConditionR )
    #
    return tZip( lFieldsL, lFieldsR )



def _gelDictListKeysValuesDictOfLists(
            lDictList, tKeyFields, tValueFields, fKeyCondition = None, fValueCondition = None ):
    #
    from Dict.Get  import getDictOfListsOffItems
    #
    lKeysValues    = _getTupleOfDictListFieldTuples(
                        lDictList, tKeyFields, tValueFields, fKeyCondition, fValueCondition )
    #
    dKeysValues    = getDictOfListsOffItems( lKeysValues )
    #
    return dKeysValues



def gelDictListKeysCounts(
            lDictList, tKeyFields, tValueFields, fKeyCondition = None, fValueCondition = None ):
    #
    '''
    pass a dict list & tuples of key & value fields
    returns counts -- for each unique key combo, how many rows are there
    Why pass values?
    '''
    #
    from Dict.Numbs     import getDictOfCountsOffDictOfLists
    from Dict.Get       import getItemList
    #
    dKeysValues     = _gelDictListKeysValuesDictOfLists(
                        lDictList, tKeyFields, tValueFields, fKeyCondition, fValueCondition )
    #
    dKeysCounts     = getDictOfCountsOffDictOfLists( dKeysValues )
    #
    return getItemList( dKeysCounts )



def gelDictListKeysAvgs(
            lDictList, tKeyFields, tValueFields, fKeyCondition = None, fValueCondition = None ):
    #
    '''
    pass a dict list & tuples of key & value fields
    returns avgs -- for each unique key combo, what is the avg value ?
    '''
    #
    from Dict.Numbs     import getDictOfAvgsOffDictOfLists
    from Dict.Get       import getItemList
    #
    dKeysValues     = _gelDictListKeysValuesDictOfLists(
                        lDictList, tKeyFields, tValueFields, fKeyCondition, fValueCondition )
    #
    dKeysAvgs       = getDictOfAvgsOffDictOfLists( dKeysValues )
    #
    return getItemList( dKeysAvgs )



def getDictValueDict( lDictList, sCol, fCondition = getTrue, bOneColOnly = False ):
    #
    '''
    you have a dict list, one column is a unique ID
    make a dict with the ID's as the keys and the dicts as the values
    '''
    return dict(
        getDecoratedDictIter( lDictList, sCol, fCondition, bOneColOnly ) )



def getValueKeyLookupDict( d, sValue, fCondition = getTrue ):
    #
    '''
    the dict list has already been converted to a dictionary
    each dict in the list has a key, so the value for each key is a dict
    you have specific values from the value dicts
    and you want to look up the key for each specific value
    this works best if the specific values are unique
    pass the dict and the value
    '''
    #
    from Dict.Get import getKeyIter
    #
    dLookUp = {}
    #
    if fCondition == getTrue:
        #
        for k in getKeyIter( d ):
            #
            dLookUp[ d[ k ][ sValue ] ] = k
            #
        #
    else:
        #
        for k in getKeyIter( d ):
            #
            newKey = d[ k ][ sValue ]
            #
            if fCondition( newKey ):
                #
                dLookUp[ newKey ] = k
            #
        #
    #
    return dLookUp



if __name__ == "__main__":
    #
    lProblems = []
    #
    from six            import print_ as print3
    #
    from Utils.Result   import sayTestResult
    #
    dTest0 = dict( a =  1, b =  2, c =  3, d =  4, e =  5, f =  6, g =  7, h =  8 )
    dTest1 = dict( a = 11, b = 12, c = 13, d = 14, e = 15, f = 16, g = 17, h = 18 )
    #
    lDictList = [ dTest0, dTest1 ]
    #
    if getDictListFields( dTest0, ( 'd', 'e' ) ) != (4, 5):
        #
        lProblems.append( 'getDictListFields()' )
        #
    #
    if  getListOfDictListFields( [ dTest0 ],   'a'                  ) != [ 1 ]       or \
        getListOfDictListFields( [ dTest0 ], ( 'a', 'b'           ) ) != [(1, 2)]    or \
        getListOfDictListFields( [ dTest0 ], ( 'a', 'b', 'c'      ) ) != [(1, 2, 3)] or \
        getListOfDictListFields( [ dTest0 ], ( 'a', 'b', 'c', 'd' ) ) != [(1, 2, 3, 4)]:
        #
        lProblems.append( 'getListOfDictListFields()' )
        #
    #
    # lDictList
    # [{'a':  1, 'c':  3, 'b':  2, 'e':  5, 'd':  4, 'g':  7, 'f':  6, 'h':  8},
    #  {'a': 11, 'c': 13, 'b': 12, 'e': 15, 'd': 14, 'g': 17, 'f': 16, 'h': 18}]
    #
    if getDecoratedDictList( lDictList, ( 'a', 'b' ) ) != \
            [(( 1,  2), {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}),
             ((11, 12), {'a':11, 'b':12, 'c':13, 'd':14, 'e':15, 'f':16, 'g':17, 'h':18})]:
        #
        lProblems.append( 'getDecoratedDictList()' )
        #
    #
    if _getTupleOfDictListFieldTuples( lDictList, ( 'a', 'b' ), ( 'g', 'h' ) ) != \
            ( (( 1,  2), ( 7,  8)),
              ((11, 12), (17, 18)) ):
        #
        lProblems.append( '_getTupleOfDictListFieldTuples()' )
        #
    #
    lKeysValues = _gelDictListKeysValuesDictOfLists( lDictList, ( 'a', 'b' ), ( 'g', 'h' ) )
    #
    if lKeysValues != \
            {( 1 , 2): [( 7,  8)],
             (11, 12): [(17, 18)]}:
        #
        print3( lKeysValues )
        lProblems.append( '_gelDictListKeysValuesDictOfLists()' )
        #
    #
    lKeysCounts = list( gelDictListKeysCounts( lDictList, ( 'a', 'b' ), ( 'g', 'h' ) ) )
    #
    if lKeysCounts != \
            [(( 1,  2), 1),
             ((11, 12), 1)]:
        #
        print3( lKeysCounts )
        lProblems.append( 'gelDictListKeysCounts()' )
        #
    #
    lKeysAvgs = list( gelDictListKeysAvgs( lDictList, ( 'a', 'b' ), ( 'h' ) ) )
    #
    if lKeysAvgs != \
            [(( 1,  2),  8.0),
             ((11, 12), 18.0)]:
        #
        lProblems.append( 'gelDictListKeysAvgs()' )
        #
    #
    # lDictList
    # [{'a':  1, 'c':  3, 'b':  2, 'e':  5, 'd':  4, 'g':  7, 'f':  6, 'h':  8},
    #  {'a': 11, 'c': 13, 'b': 12, 'e': 15, 'd': 14, 'g': 17, 'f': 16, 'h': 18}]
    #
    dDictListManual = dict( [ ( d['a'], d ) for d in lDictList ] )
    #
    dDictListFunct = getDictValueDict( lDictList, ( 'z', 'a' ), bOneColOnly = True )
    #
    if dDictListFunct != dDictListManual:
        #
        lProblems.append( 'getDictValueDict() col name last' )
        #
    #
    dDictListFunct = getDictValueDict( lDictList, ( 'a', 'x' ), bOneColOnly = True )
    #
    if dDictListFunct != dDictListManual:
        #
        lProblems.append( 'getDictValueDict() col name first' )
        #
    #
    dGotCgetKey = getValueKeyLookupDict( dDictListFunct, 'c' )
    #
    if dGotCgetKey[ 3 ] != 1:
        #
        lProblems.append( 'dGotCgetKey[ 3 ]' )
        #
    if dGotCgetKey[ 13 ] != 11:
        #
        lProblems.append( 'dGotCgetKey[ 13 ]' )
        #
    #
    #
    sayTestResult( lProblems )