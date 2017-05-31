#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Collection functions get
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
from Collect.Test   import isScaler
from Iter.AllVers   import iMap, iFilter, iRange, iZip
from Utils.Get      import getTrue as _getTrue



def getListFromNestedLists( lList, gotScaler = isScaler ): # flatten nested list
    #
    """This returns a single, flat list.
    """
    lFlat = []
    #
    for uMember in lList:
        #
        if gotScaler( uMember ):   # list or tuple
            #
            lFlat.append( uMember )
            #
        else:
            #
            # recursive call coming up!
            #
            lAddTo = getListFromNestedLists( uMember, gotScaler = gotScaler )
            #
            lFlat += lAddTo
            #
        #
    #
    return lFlat



def getListOfListsFromNestedLists( lNestedLists ):
    #
    """This returns a list of lists.
    Each sublist in the list of lists is flat.
    """
    lFlatter    = [ ( uKey, uItem ) for uKey, lList in lNestedLists for uItem in lList ]
    #
    lFlat       = [ [ uKey ] + list( uItem ) for uKey, uItem in lFlatter ]
    #
    return lFlat



def getSequencePairsThisWithNext( lSeq ):
    #
    """
    Say you got a sequence, ('a', 'b', 'c', 'd', 'e' ).
    This returns an tuple
    ('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e').
    If you want an iterator instead of a tuple, import from Iter.Get.
    """
    #
    from Iter.Get import getSequencePairsThisWithNext as getWithNext
    #
    return tuple( getWithNext( lSeq ) )





def getDecoratedIter( seq, getDecoration, fCondition = None ):
    #
    """
    To sort a list fast on some component,
    the fasted approach (according to the cookbook) is typically
    "Decorate, Sort, Undecorate".
    see also getDictValuesSortedKeyOrder & getDictKeysValuesSortedKeyOrder
    """
    #
    def getTuple( u ): return getDecoration( u ), u
    #
    if fCondition is None:
        #
        return iMap( getTuple, seq )
        #
    else:
        #
        return iMap( getTuple, iFilter( fCondition, seq ) )



def getDecoratedList( seq, getDecoration, fCondition = None ):
    #
    """
    To sort a list fast on some component,
    the fasted approach (according to the cookbook) is typically
    "Decorate, Sort, Undecorate".
    see also getDictValuesSortedKeyOrder & getDictKeysValuesSortedKeyOrder
    """
    #
    return list( getDecoratedIter( seq, getDecoration, fCondition = fCondition ) )


def _hasElement( seq, iIndex = 1 ):
    #
    '''does the list or tuple have an element of a certain index?
    '''
    #
    from Collect.Test   import isListOrTuple
    #
    return isListOrTuple( seq ) and len( seq ) > iIndex


def _hasLast( u ):
    #
    '''does the list or tuple have an element of index one or higher?
    '''
    #
    return _hasElement( u )


def _getZero( t ): return t[0]

def getLast( t ): return t[-1]

def getElement( t, i ):
    #
    uElement = None
    #
    if _hasElement( t, i ):
        #
        uElement = t[ i ]
        #
    #
    return uElement



def getKeyIterOffItems( items, fCondition = None ):
    #
    # formerly getDecorListOffDecoratedList
    #
    '''
    returns a generator y!elding the keys off an item list or sequence
    '''
    #
    if fCondition is None:
        #
        return iMap( _getZero, iFilter( _hasElement, items ) )
        #
    else:
        #
        return iMap( _getZero, iFilter( _hasElement, iFilter( fCondition, items ) ) )


def getKeyListOffItems( items, fCondition = None ):
    #
    '''
    returns a list of keys off an item list or sequence
    '''
    #
    return list( getKeyIterOffItems( items, fCondition = fCondition ) )


def getKeyTupleOffItems( items, fCondition = None ):
    #
    '''
    returns a list of keys off an item list or sequence
    '''
    #
    return tuple( getKeyIterOffItems( items, fCondition = fCondition ) )


def getValueIterOffItems( items, fCondition = None ):
    #
    '''
    returns a generator y!elding the values off an item list
    '''
    #
    if fCondition is None:
        #
        return iMap( getLast, iFilter( _hasLast, items ) )
        #
    else:
        #
        return iMap( getLast,
                     iFilter( _hasLast,
                     iFilter( fCondition, items ) ) )


def getValueListOffItems( items, fCondition = None ):
    #
    '''
    returns a list of the values off an item list
    '''
    #
    return list( getValueIterOffItems( items, fCondition = fCondition ) )


def getValueTupleOffItems( items, fCondition = None ):
    #
    '''
    returns a tuple of the values off an item list
    '''
    #
    return tuple( getValueIterOffItems( items, fCondition = fCondition ) )


def _cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    # http://code.activestate.com/recipes/576653/
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0  
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K


def getRevSorted( iterable, cmp = None, key = None ):
    #
    if cmp is not None and key is None:
        #
        key = _cmp_to_key( cmp )
        #
    #
    return sorted( iterable, key = key, reverse = True )



def getRevOrder( iterable ):
    #
    l = list( iterable )
    #
    l.reverse()
    #
    return l


def getSeparateKeysValues( items, fCondition = _getTrue ):
    #
    """getSeparateKeysValues( [(97,'a'),(98,'b'),(99,'c'),(100,'d'),(101,'e')] )
    returns
    ( [97, 98, 99, 100, 101], ['a', 'b', 'c', 'd', 'e'] )

    """
    #
    from Collect.Test import isListOrTuple
    #
    iThis = 0
    #
    if isListOrTuple( items ):
        #
        tItems  = items
        #
    else:
        #
        tItems  = tuple( items )
        #
    #
    lKeys   = [ None ] * len( tItems )
    lValues = [ None ] * len( tItems )
    #
    if fCondition is _getTrue:
        #
        for t in tItems:
            #
            lKeys[ iThis ], lValues[ iThis ] = t[0], t[-1]
            #
            iThis += 1
            #
    else:
        #
        for t in tItems:
            #
            if fCondition( t ):
                #
                lKeys[ iThis ], lValues[ iThis ] = t[0], t[-1]
                #
                iThis += 1
                #
        #
        lKeys   = lKeys[   : iThis ]
        lValues = lValues[ : iThis ]
        #
    #
    return lKeys, lValues



# unZip = getSeparateKeysValues

def unZip( items ):
    #
    from Collect.Test import isListOrTuple
    from Iter.AllVers import iRange, tRange
    #
    if isListOrTuple( items ):
        #
        tItems  = items
        #
    else:
        #
        tItems  = tuple( items )
        #
    #
    iOutsideLen = len( tItems )
    iInsideLen  = len( tItems[0] )
    #
    lReturn = [None] * iInsideLen
    #
    tOutside = tRange( iOutsideLen )
    #
    for i in iRange( iInsideLen ):
        #
        lReturn[i] = [ tItems[j][i] for j in tOutside ]
        #
    #
    return lReturn


def getNewValuesIter4Items( items, fValue, fCondition = _getTrue ):
    #
    if fCondition is _getTrue:
        #
        for k, v in items:
            #
            yield k, fValue( v )
        #
    else:
        #
        for k, v in items:
            #
            if not fCondition( k ): continue
            #
            yield k, fValue( v )
    

def getNewValuesList4Items( items, fValue, fCondition = _getTrue ):
    #
    return list( getNewValuesIter4Items( items, fValue, fCondition = fCondition ) )


def getNewValuesTuple4Items( items, fValue, fCondition = _getTrue ):
    #
    return tuple( getNewValuesIter4Items( items, fValue, fCondition = fCondition ) )


def getNewKeysIter4Items( items, fKey, fCondition = _getTrue ):
    #
    if fCondition is _getTrue:
        #
        for k, v in items:
            #
            yield fKey( k ), v
        #
    else:
        #
        for k, v in items:
            #
            if not fCondition( k ): continue
            #
            yield fKey( k ), v


def getNewKeysList4Items( items, fKey, fCondition = _getTrue ):
    #
    return list( getNewKeysIter4Items( items, fKey, fCondition = fCondition ) )


def getNewKeysTuple4Items( items, fKey, fCondition = _getTrue ):
    #
    return tuple( getNewKeysIter4Items( items, fKey, fCondition = fCondition ) )


def getDecoratedKeysFromObject( lKeys, uObject, getDecoration, fCondition = None ):
    #
    # it can be faster to sort just the decoration + key than decoration + object
    #
    from Iter.AllVers import lZip
    #
    if fCondition is None:
        #
        lDecorations    = iMap( getDecoration, lKeys )
        #
        lDecorsKeys     = lZip( lDecorations, lKeys )
        #
    else:
        #
        lDecorsKeys     = [ ( getDecoration( uKey ), uKey ) for uKey in lKeys
                            if   fCondition( uKey ) ]
        #
    #
    return lDecorsKeys



def getSwapSortKeys( lKeysValues, sOrder = 'ascending' ):
    #
    from Iter.Get import getListSwapValueKey
    #
    lValuesKeys     = getListSwapValueKey( lKeysValues )
    #
    lValuesKeys.sort()      # lesser values on top
    #
    if sOrder != 'ascending':
        #
        lValuesKeys.reverse() # greater values on top
        #
    #
    lValues, lKeys  = unZip( lValuesKeys )
    #
    return lKeys, lValues




def getCombinedNoDupes( *lListOfLists ):
    #
    """
    Combine two or more lists into a single list.
    No duplicates allowed, final list is sorted if possible.
    This makes the list of lists automatically,
    when calling this function,
    just send each list as a separate parameter.
    """
    #
    setTemp     = set( [] )
    #
    for lList in lListOfLists:
        #
        setTemp.update( lList )
        #
    #
    lCombined   = list( setTemp )
    #
    try:
        lCombined.sort()
    except TypeError:
        #
        lCombined = sorted( lCombined, key = str )
        #
    #
    return lCombined


def _getStripped( s ): return str( s ).strip()


def getStrStripIter( l ):
    #
    return iMap( _getStripped, l )


def getStringsStripped( l ):
    #
    return list( getStrStripIter( l ) )



def getLongest( iterable ):
    #
    l = [( len( u ), u ) for u in iterable ]
    #
    sLongest = ''
    #
    if l:
        #
        l.sort()
        #
        sLongest = l[-1][1]
        #
    #
    return sLongest


if __name__ == "__main__":
    #
    from string import ascii_lowercase as lowercase
    from string import ascii_uppercase as uppercase
    #
    from six            import print_ as print3
    #
    from Dict.Get       import getItemIter, getKeyList
    from Iter.AllVers   import lMap, lRange, tRange
    from String.Get     import getUpper
    from Utils.Version  import PYTHON3
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    def getExample( seq ): return [ seq[ i : i + 2 ] for i in iRange( 0, 26, 2 ) ]
    #
    lList   = [ getExample( uppercase ), getExample( lowercase ) ]
    #
    # [['AB','CD','EF','GH','IJ','KL','MN','OP','QR','ST','UV','WX','YZ'],
    #  ['ab','cd','ef','gh','ij','kl','mn','op','qr','st','uv','wx','yz']]
    #
    lFlat = getListFromNestedLists( lList )
    #
    if lFlat != \
            ['AB','CD','EF','GH','IJ','KL','MN','OP','QR','ST','UV','WX','YZ',
             'ab','cd','ef','gh','ij','kl','mn','op','qr','st','uv','wx','yz']:
        #
        lProblems.append( 'getListFromNestedLists()' )
        #
    #
    lIndexList = enumerate( lMap( list, getExample( lowercase ) ) )
    #
    # [( 0,['a','b']),( 1,['c','d']),( 2,['e','f']),( 3,['g','h']),
    #  ( 4,['i','j']),( 5,['k','l']),( 6,['m','n']),( 7,['o','p']),
    #  ( 8,['q','r']),( 9,['s','t']),(10,['u','v']),(11,['w','x']),
    #  (12,['y','z'])]
    #
    if getListOfListsFromNestedLists( lIndexList ) != \
            [[ 0,'a'],[ 0,'b'],[ 1,'c'],[ 1,'d'],[ 2,'e'],[ 2,'f'],
             [ 3,'g'],[ 3,'h'],[ 4,'i'],[ 4,'j'],[ 5,'k'],[ 5,'l'],
             [ 6,'m'],[ 6,'n'],[ 7,'o'],[ 7,'p'],[ 8,'q'],[ 8,'r'],
             [ 9,'s'],[ 9,'t'],[10,'u'],[10,'v'],[11,'w'],[11,'x'],
             [12,'y'],[12,'z']]:
        #
        lProblems.append( 'getListOfListsFromNestedLists()' )
        #
    if getSequencePairsThisWithNext( ('a', 'b', 'c', 'd', 'e' ) ) != \
            ( ('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e') ):
        #
        lProblems.append( 'getSequencePairsThisWithNext()' )
        #
    #
    lKeyValue = [(97,'a'),(98,'b'),(99,'c'),(100,'d'),(101,'e')]
    #
    if getDecoratedList( ('a','b','c','d','e' ), ord ) != lKeyValue:
        #
        lProblems.append( 'getDecoratedList()' )
        #
    #
    t = tuple( iRange(10) )
    #
    if not _hasElement( t, 9 ) or _hasElement( t, 10 ):
        #
        lProblems.append( '_hasElement()' )
        #
    #
    if      getElement( t, 1 ) != 1 or \
            getElement( t, 10 ) is not None:
        #
        lProblems.append( 'getElement()' )
        #
    #
    if getKeyListOffItems( lKeyValue ) != lRange( 97, 102 ):
        #
        print3( lKeyValue )
        print3( getKeyListOffItems( lKeyValue ) )
        lProblems.append( 'getKeyListOffItems()' )
        #
    #
    if getKeyTupleOffItems( lKeyValue ) != tRange( 97, 102 ):
        #
        print3( lKeyValue )
        print3( getKeyTupleOffItems( lKeyValue ) )
        lProblems.append( 'getKeyTupleOffItems()' )
        #
    #
    if getValueListOffItems( lKeyValue ) != ['a', 'b', 'c', 'd', 'e']:
        #
        lProblems.append( 'getValueListOffItems()' )
        #
    #
    if getValueTupleOffItems( lKeyValue ) != ('a', 'b', 'c', 'd', 'e'):
        #
        print3( lKeyValue )
        print3( tuple( getValueTupleOffItems( lKeyValue ) ) )
        lProblems.append( 'getValueTupleOffItems()' )
        #
    #
    if getSeparateKeysValues( lKeyValue ) != \
            ( lRange( 97, 102 ), ['a', 'b', 'c', 'd', 'e'] ):
        #
        lProblems.append( 'getSeparateKeysValues()' )
        #
    if unZip( lKeyValue ) != [[97,98,99,100,101],['a','b','c','d','e']]:
        #
        lProblems.append( 'unZip() dict type 2 element items' )
        #
    #
    l3Elements = [
            ('', 0, 0),
            ('abcdefghijklmnopqrstuvwxyz', 10, 36),
            ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 46, 72),
            ('', 82, 82) ]
    #
    if unZip( l3Elements ) != [
            [   '',
                'abcdefghijklmnopqrstuvwxyz',
                'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                ''],
            [0, 10, 46, 82],
            [0, 36, 72, 82] ]:
        #
        lProblems.append( 'unZip() oddball 3 element items' )
        #
    #
    #
    lKeyValueStrs = [('0','a'),('1','b'),('2','c'),('3','d'),('4','e')]
    #
    if getNewValuesList4Items( lKeyValue, getUpper ) != \
            [ (97,'A'),(98,'B'),(99,'C'),(100,'D'),(101,'E') ]:
        #
        lProblems.append( 'getNewValuesList4Items()' )
        #
    #
    if getNewValuesTuple4Items( lKeyValue, getUpper ) != \
            ( (97,'A'),(98,'B'),(99,'C'),(100,'D'),(101,'E') ):
        #
        lProblems.append( 'getNewValuesTuple4Items()' )
        #
    #
    #
    dTest = dict( a = 1, b = 2, c = 3, d = 4, e = 5 )
    #
    def getDecoPretend( k ): return dTest.get( k )
    #
    lKeys = getKeyList( dTest )
    #
    lKeys.sort()
    #
    if getDecoratedKeysFromObject( lKeys, dTest, getDecoPretend ) != \
            [(1,'a'),(2,'b'),(3,'c'),(4,'d'),(5,'e')]:
        #
        print3( getDecoratedKeysFromObject( lKeys,dTest,getDecoPretend ) )
        lProblems.append( 'GetDecoratedKeysFromObject()' )
        #
    #
    lKeys = ['a', 'b', 'c', 'd', 'e']
    #
    lWant = ['AB', 'ab', 'CD', 'cd', 'EF', 'ef', 'GH', 'gh', 'IJ', 'ij',
             'KL', 'kl', 'MN', 'mn', 'OP', 'op', 'QR', 'qr', 'ST', 'st',
             'UV', 'uv', 'WX', 'wx', 'YZ', 'yz']
    #
    if getRevOrder( iRange( 6 ) ) != [5, 4, 3, 2, 1, 0]:
        #
        print3( 'getRevOrder( iRange( 6 ) ):', getRevSorted( iRange( 6 ) ) )
        lProblems.append( 'getRevOrder()' )
        #
    #
    #
    if list( getRevSorted( iRange( 6 ) ) ) != [5, 4, 3, 2, 1, 0]:
        #
        print3( 'list( getRevSorted( iRange( 6 ) ) ):', list( getRevSorted( iRange( 6 ) ) ) )
        lProblems.append( 'getRevSorted()' )
        #
    #
    if      getSwapSortKeys( getItemIter( dTest ), sOrder = 'ascending' ) != \
                (['a','b','c','d','e'],[1,2,3,4,5]) or \
            getSwapSortKeys( getItemIter( dTest ), sOrder = 'other' ) != \
                (['e','d','c','b','a'],[5,4,3,2,1]):
        #
        lProblems.append( 'getSwapSortKeys()' )
        #
    #
    if PYTHON3:
        lWant = [
            ('0', 'a'), ('1', 'b'), ('2', 'c'), ('3', 'd'), ('4', 'e'),
            ('a',  1 ), ('b',  2 ), ('c',  3 ), ('d',  4 ), ('e',  5 ),
            (100, 'd'), (101, 'e'), (97,  'a'), (98,  'b'), (99,  'c')]
    else:
        lWant = [
            (97,  'a'), (98,  'b'), (99,  'c'), (100, 'd'), (101, 'e'),
            ('0', 'a'), ('1', 'b'), ('2', 'c'), ('3', 'd'), ('4', 'e'),
            ('a',  1 ), ('b',  2 ), ('c',  3 ), ('d',  4 ), ('e',  5 )]
    #
    if getCombinedNoDupes(
            lKeyValue, getItemIter(dTest), lKeyValueStrs, lKeyValue ) != lWant:
        #
        print3( getCombinedNoDupes(
                    lKeyValue,getItemIter(dTest),lKeyValueStrs,lKeyValue ) )
        lProblems.append( 'getCombinedNoDupes()' )
        #
    #
    def getPadded( s ): return '  %s  ' % s
    #
    lPaddedNos = lMap( getPadded, iRange(10) )
    #
    if getStringsStripped( lPaddedNos ) != lMap( str, iRange(10) ):
        #
        lProblems.append( 'getStringsStripped()' )
        #
    #
    t = ( 'abc', 'abcd', 'abcde', 'ab', 'a' )
    #
    if getLongest( t ) != 'abcde':
        #
        lProblems.append( 'getLongest()' )
        #
    #
    sayTestResult( lProblems )