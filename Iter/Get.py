#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Iter functions get
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
# itertools: New in version 2.3.

from Utils.Get import getTrue as _getTrue


def getSequencePairsThisWithNext( something ):
    #
    """
    Say you got a sequence, ('a','b','c','d','e').
    This returns an iterator ('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e')
    """
    #
    from six            import next as getNext
    #
    #from Utils.Both2n3  import getNext
    #
    iterable = iter( something )
    #
    uPrior = getNext( iterable )
    #
    for uThis in iterable:
        #
        yield uPrior, uThis
        #
        uPrior = uThis




def getItemIterWithKeysConsistentCase( lItems, bUpper = True ):
    #
    from Collect.Get    import unZip
    from Dict.Get       import getItemIter
    #
    if isinstance( lItems, dict ):
        #
        lItems  = getItemIter( lItems )
        #
    #
    if bUpper:
        #
        def getFixCase( sKey ): return sKey.upper()
        #
    else:
        #
        def getFixCase( sKey ): return sKey.lower()
        #
    #
    for sKey, uValue in lItems:
        #
        yield getFixCase( sKey ), uValue



def getPairsOffIterable( iterable ):
    #
    """Say you got a sequence, ('a','b','c','d','e').
    This returns an iterator [('a', 'b'), ('c', 'd'), ('e', None)].
    """
    #
    from six            import next as getNext
    #
    from Iter.Test      import isIterator
   #from Utils.Both2n3  import getNext
    #
    bOddLen = False
    #
    if not isIterator( iterable ): iterable = iter( iterable )
    #
    for uThis in iterable:
        #
        try:
            uNext   = getNext( iterable )
        except StopIteration:
            uNext   = None
            bOddLen = True
        #
        yield uThis, uNext
        #
        if bOddLen: raise StopIteration



def getIterSwapValueKey( items, fCondition = _getTrue ):
    #
    if fCondition is _getTrue:
        #
        for t in items:
            #
            yield t[-1], t[0]
            #
    else:
        #
        for t in items:
            #
            if fCondition( t ):
                #
                yield t[-1], t[0]




def getListSwapValueKey( d, fCondition = _getTrue ):
    #
    return list( getIterSwapValueKey( d, fCondition ) )


def getTupleSwapValueKey( d, fCondition = _getTrue ):
    #
    return tuple( getIterSwapValueKey( d, fCondition ) )


def iRevRange( iLen ): # for stepping thru a list backwards
    #
    """For stepping thru a list backwards."""
    #
    from Iter.AllVers import iRange
    #
    return iRange( iLen - 1, -1, -1 )


def lRevRange( iLen ): # for stepping thru a list backwards
    #
    """For stepping thru a list backwards."""
    #
    from Iter.AllVers import iRange
    #
    return list( iRevRange( iLen ) )


def tRevRange( iLen ): # for stepping thru a list backwards
    #
    """For stepping thru a list backwards."""
    #
    from Iter.AllVers import iRange
    #
    return tuple( iRevRange( iLen ) )



def lZipLongest( *args, **kwargs ):
    #
    from Iter.AllVers import iZipLongest
    #
    return list( iZipLongest( *args, **kwargs ) )


def tZipLongest( *args, **kwargs ):
    #
    from Iter.AllVers import iZipLongest
    #
    return tuple( iZipLongest( *args, **kwargs ) )




if __name__ == "__main__":
    #
    from six            import print_ as print3
    #
    from Iter.AllVers   import lMap, iRange, tRange
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if tuple( getSequencePairsThisWithNext( ('a','b','c','d','e') ) ) != \
            ( ('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e') ):
        #
        lProblems.append( 'getSequencePairsThisWithNext()' )
        #
    if list( getItemIterWithKeysConsistentCase(
            [('A', 'a'), ('b', 'b'), ('C', 'c'), ('d', 'd'), ('E', 'e')] ) ) != \
            [('A', 'a'), ('B', 'b'), ('C', 'c'), ('D', 'd'), ('E', 'e')]:
        #
        lProblems.append( 'getItemIterWithKeysConsistentCase()' )
        #
    if list( getPairsOffIterable( ('a','b','c','d','e') ) ) != \
            [('a', 'b'), ('c', 'd'), ('e', None )]:
        #
        lProblems.append( 'getPairsOffIterable()' )
        #
    #
    if getListSwapValueKey(
            [('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5)] ) != \
            [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd'), (5, 'e')]:
        #
        lProblems.append( 'getListSwapValueKey()' )
        #
    #
    if tuple( iRevRange( 5 ) ) != ( 4, 3, 2, 1, 0 ):
        #
        lProblems.append( 'iRevRange()' )
        #
    #
    lWant = [ ('a', 0), ('b', 1), ('c', 2), ('d', 3), ('e', 4), (None, 5) ]
    #
    luGet = lZipLongest( ['a', 'b', 'c', 'd', 'e'], iRange(6) )
    #
    if lWant != luGet:
        #
        lProblems.append( 'lZipLongest()' )
        #
    #
    tWant = tuple( lWant )
    #
    tuGet = tZipLongest( ['a', 'b', 'c', 'd', 'e'], iRange(6) )
    #
    if tWant != tuGet:
        #
        lProblems.append( 'tZipLongest()' )
        #
    #
    #
    #
    sayTestResult( lProblems )