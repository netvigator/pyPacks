#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Iter functions AllVers
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

'''
the aim is to provide python iterators
that will work in all supported versions
(2.4 through 3.n)
'''
from Utils.Version  import PYTHON3, isVersAtLeast

_bAtLeast2dot6 = isVersAtLeast( '2.6' )


# 2.4 tee

#
# builtins
# 2.2 iter
# 2.3 enumerate
# 2.6 next
#
# itertools
# 2.6 chain
# 2.6 combinations
# 2.3 count
# 2.3 cycle
# 2.3 dropwhile
# 2.4 groupby
# 2.3 ifilter
# 2.3 ifilterfalse
# 2.3 imap
# 2.3 islice
# 2.3 izip
# 2.6 izip_longest
# 2.6 permutations
# 2.6 product
# 2.3 repeat
# 2.3 starmap
# 2.3 takewhile
# 2.4 tee
#


if PYTHON3:
    #
    imap = map
    #
    def lMap( function, *iterables ):
        #
        return list( map( function, *iterables ) )
    #
    def tMap( function, *iterables ):
        #
        return tuple( map( function, *iterables ) )
    #
else:
    #
    lMap = map
    #
    try:
        #
        from itertools import imap
        #
        def tMap( function, *iterables ):
            #
            return tuple( imap( function, *iterables ) )
    #
    except ImportError:
        #
        def imap(function, *iterables):
            iterables = map(iter, iterables)
            while True:
                args = [i.next() for i in iterables]
                if function is None:
                    yield tuple(args)
                else:
                    yield function(*args)
        #
        def tMap( function, *iterables ):
            #
            return tuple( map( function, *iterables ) )

iMap = imap


if PYTHON3:
    #
    izip = zip
    #
    def lZip( *iterables ):
        #
        return list( zip( *iterables ) )
    #
    def tZip( *iterables ):
        #
        return tuple( zip( *iterables ) )
    #
else:
    #
    lZip = zip
    #
    try:
        #
        from itertools import izip
        #
        def tZip( *iterables ):
            #
            return tuple( izip( *iterables ) )
        #
    except ImportError:
        #
        def izip(*iterables):
            iterables = imap(iter, iterables)
            while iterables:
                result = [i.next() for i in iterables]
                yield tuple(result)
        #
        def tZip( *iterables ):
            #
            return tuple( zip( *iterables ) )
        #

iZip = izip


if PYTHON3:
    #
    iFilter = filter
    #
    def lFilter( function, iterable ):
        #
        return list( filter( function, iterable ) )
    #
    def tFilter( function, iterable ):
        #
        return tuple( filter( function, iterable ) )
    #
else:
    #
    lFilter = filter
    #
    try:
        #
        from itertools import ifilter
        #
        def tFilter( function, iterable ):
            #
            return tuple( ifilter( function, iterable ) )
        #
    except ImportError:
        #
        def ifilter( function, iterable ):
            #
            if function is None: function = bool
            #
            for item in iterable:
                #
                if function( item ):
                    #
                    yield item
        #
        def tFilter( function, iterable ):
            #
            return tuple( filter( function, iterable ) )
        #
    #
    iFilter = ifilter



if PYTHON3:
    #
    from itertools import filterfalse
    #
    iFilterFalse = filterfalse
    #
else:
    #
    try:
        #
        from itertools import ifilterfalse
        #
    except ImportError:
        #
        def ifilterfalse(predicate, iterable):
            if predicate is None:
                predicate = bool
            for x in iterable:
                if not predicate(x):
                    yield x
    #
    iFilterFalse = ifilterfalse


def lFilterFalse( function, iterable ):
    #
    return list( iFilterFalse( function, iterable ) )


def tFilterFalse( function, iterable ):
    #
    return tuple( iFilterFalse( function, iterable ) )



if PYTHON3:
    #
    # def iRange( ):
    #
    iRange = range
    #
    def lRange( *args ):
        #
        return list( range( *args ) )
    #
else:
    #
    iRange = xrange
    #
    lRange = range


def tRange( *args ):
    #
    return tuple( iRange( *args ) )


def iReverseRange( iStart ):
    #
    # aka RevRange()
    '''
    list( iRange(10)        ) yields [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    list( iReverseRange(10) ) yields [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    
    this is useful for stepping across list elements from last to first
    '''
    #
    return iRange( iStart - 1, -1, -1 )



def _getEnumeratorYielding( seq, start = 0 ):
    #
    i = start
    #
    for u in seq:
        #
        yield i, u
        #
        i += 1


def _getEnumeratorZipOrYield( seq, start = 0 ):
    #    
    from Collect.Test import isSequence
    #    
    if isSequence( seq ):
        #
        return iZip( iRange( start, start + len( seq ) ), seq )
        #
    else:
        #
        return _getEnumeratorYielding( seq, start = start )
        #


def getEnumerator( seq, start = 0 ):
    #
    '''
    like built in enumerate
    but enumerate did not support the start param until 2.6
    '''
    #
    if start == 0:
        #
        return enumerate( seq )
        #
    elif _bAtLeast2dot6:
        #
        return enumerate( seq, start )
        #
    else:
        #
        return _getEnumeratorZipOrYield( seq, start = start )
        #



try:
    #
    from itertools import chain
    #
except ImportError:
    #
    def chain(*iterables):
        for it in iterables:
            for element in it:
                yield element





def _combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list( range(r) )
    yield tuple( [ pool[i] for i in indices ] )
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple( [ pool[i] for i in indices ] )

try:
    #
    # New in version 2.6
    #
    from itertools import combinations
    #
    getCombinations = combinations
    #
except:
    #
    getCombinations = _combinations


try:
    #
    from itertools import combinations_with_replacement
    #
except ImportError:
    #
    pass




try:
    #
    from itertools import repeat
    #
except ImportError:
    #
    def repeat(object, times=None):
        if times is None:
            while True:
                yield object
        else:
            for i in iRange(times):
                yield object



try:
    #
    from itertools import starmap
    #
except ImportError:
    #
    def starmap(function, iterable):
        iterable = iter(iterable)
        while True:
            yield function(*iterable.next())




def _zip_longest( *args, **kwds ):
    #
    '''
    _zip_longest('ABCD', 'xy', fillvalue='-') --> Ax By C- D-
    '''
    #
    fillvalue = kwds.get('fillvalue') # defaults to None if no fillvalue
    def sentinel(counter = ([fillvalue]*(len(args)-1)).pop):
        yield counter()         # yields the fillvalue, or raises IndexError
    fillers = repeat(fillvalue)
    iters = [chain(it, sentinel(), fillers) for it in args]
    try:
        for tup in iZip(*iters):
            yield tup
    except IndexError:
        pass

try:
    #
    # New in version 2.6
    #
    from itertools import izip_longest as iZipLongest
    #
except ImportError:
    #
    iZipLongest = _zip_longest


def _permutations(iterable, r=None):
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210
    pool = tuple(iterable)
    n = len(pool)
    # r = n if r is None else r
    if r is None: r = n
    if r > n:
        return
    indices = list( range(n) )
    cycles = list( range(n, n-r, -1) )
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return


try:
    #
    from itertools import permutations # new in 2.6
    #
except ImportError:
    #
    permutations = _permutations


def _product(*args, **kwds):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = list( map(tuple, args) ) * kwds.get('repeat', 1)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

try:
    #
    # New in version 2.6
    #
    from itertools import product
    #
except ImportError:
    #
    product = _product




if __name__ == "__main__":
    #
    from six            import print_ as print3
    #
    from Iter.AllVers   import lMap
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    lStrRange = lMap( str, range(5) )
    #
    if lStrRange != ['0', '1', '2', '3', '4']:
        #
        lProblems.append( 'lMap()' )
        #
    #
    tStrRange = tMap( str, range(5) )
    #
    if tStrRange != ( '0', '1', '2', '3', '4' ):
        #
        lProblems.append( 'tMap()' )
        #
    if tuple( iMap( str, range(5) ) ) != ( '0', '1', '2', '3', '4' ):
        #
        lProblems.append( 'iMap()' )
        #
    if lZip( tStrRange, range(5) ) != \
            [ ('0',0), ('1',1), ('2',2), ('3',3), ('4',4) ]:
        #
        lProblems.append( 'lZip()' )
        #
    #
    if tZip( tStrRange, range(5) ) != \
            ( ('0',0), ('1',1), ('2',2), ('3',3), ('4',4) ):
        #
        lProblems.append( 'tZip()' )
        #
    #
    if tuple( iZip( tStrRange, range(5) ) ) != \
            ( ('0',0), ('1',1), ('2',2), ('3',3), ('4',4) ):
        #
        lProblems.append( 'iZip()' )
        #
    #
    if tuple( iFilter( bool, range(5) ) ) != ( 1, 2, 3, 4 ):
        #
        lProblems.append( 'iFilter()' )
        #
    #
    if tFilter( bool, range(5) ) != ( 1, 2, 3, 4 ):
        #
        lProblems.append( 'tFilter()' )
        #
    #
    if lFilter( bool, range(5) ) != [ 1, 2, 3, 4 ]:
        #
        lProblems.append( 'lFilter()' )
        #
    #
    #
    if tuple( iFilterFalse( bool, range(5) ) ) != ( 0, ):
        #
        lProblems.append( 'iFilterFalse()' )
        #
    #
    if tFilterFalse( bool, range(5) ) != ( 0, ):
        #
        lProblems.append( 'tFilterFalse()' )
        #
    #
    if lFilterFalse( bool, range(5) ) != [ 0, ]:
        #
        lProblems.append( 'lFilterFalse()' )
        #
    #
    #
    if tuple( iRange( 5, 10, 2 ) ) != tuple( range( 5, 10, 2 ) ):
        #
        lProblems.append( 'iRange()' )
        #
    #
    if lRange( 5, 10, 2 ) != list( range( 5, 10, 2 ) ):
        #
        lProblems.append( 'lRange()' )
        #
    #
    if tRange( 5, 10, 2 ) != tuple( range( 5, 10, 2 ) ):
        #
        lProblems.append( 'tRange()' )
        #
    #
    if tuple( iReverseRange(10) ) != ( 9, 8, 7, 6, 5, 4, 3, 2, 1, 0 ):
        #
        lProblems.append( 'iReverseRange()' )
        #
    #
    if tuple( _getEnumeratorYielding( ('a', 'b', 'c', 'd', 'e') ) ) != \
            ( ( 0, 'a'), ( 1, 'b'), ( 2, 'c'), ( 3, 'd'), ( 4, 'e') ):
        #
        lProblems.append( '_getEnumeratorYielding()' )
        #
    #
    if tuple( _getEnumeratorZipOrYield( ('a', 'b', 'c', 'd', 'e') ) ) != \
            ( ( 0, 'a'), ( 1, 'b'), ( 2, 'c'), ( 3, 'd'), ( 4, 'e') ):
        #
        lProblems.append( '_getEnumeratorZipOrYield()' )
        #
    #
    if tuple( getEnumerator( ('a', 'b', 'c', 'd', 'e') ) ) != \
            ( ( 0, 'a'), ( 1, 'b'), ( 2, 'c'), ( 3, 'd'), ( 4, 'e') ):
        #
        lProblems.append( 'getEnumerator()' )
        #
    #
    tWantCombos = ( ( 'A', 'B' ),
                    ( 'A', 'C' ),
                    ( 'A', 'D' ),
                    ( 'B', 'C' ),
                    ( 'B', 'D' ),
                    ( 'C', 'D' ) )
    #
    if tuple( _combinations( 'ABCD', 2 ) ) != tWantCombos:
        #
        print3( tuple( _combinations( 'ABCD', 2 ) ) )
        lProblems.append( '_combinations()' )
        #
    #
    if tuple( getCombinations( 'ABCD', 2 ) ) != tWantCombos:
        #
        lProblems.append( 'getCombinations()' )
        #
    #
    #
    #
    tWant = ( ('a', 0), ('b', 1), ('c', 2), ('d', 3), ('e', 4), (None, 5) )
    #
    tuGet = tuple( _zip_longest( ['a', 'b', 'c', 'd', 'e'], iRange(6) ) )
    #
    if tWant != tuGet:
        #
        lProblems.append( '_zip_longest()' )
        #
    #
    sGet    = ' '.join( [ ''.join( t ) for t in _permutations('ABCD', 2) ] )
    #
    sWant   = 'AB AC AD BA BC BD CA CB CD DA DB DC'
    #
    if sGet != sWant:
        #
        lProblems.append( '_permutations()' )
        #
    #
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    #
    sGet    = ' '.join( [ ''.join( t ) for t in _product('ABCD', 'xy') ] )
    #
    sWant   = 'Ax Ay Bx By Cx Cy Dx Dy'
    #
    if sGet != sWant:
        #
        lProblems.append( '_product() no repeat' )
        #
    #
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    #
    sGet    = ' '.join( [ ''.join( map( str, t ) )
                          for t
                          in _product(range(2), repeat=3) ] )
    #
    sWant   = '000 001 010 011 100 101 110 111'
    #
    if sGet != sWant:
        #
        print3( sGet )
        lProblems.append( '_product() with repeat' )
        #
    #
    #
    #
    sayTestResult( lProblems )