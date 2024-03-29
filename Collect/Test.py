#!/home/rick/.local/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Collection functions Test
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
# Copyright 2004-2023 Rick Graves
#
from bisect import bisect_right

try:
    from .Query         import get1stTrue
    from ..Iter.AllVers import iMap
except ( ValueError, ImportError ):
    from Collect.Query  import get1stTrue
    from Iter.AllVers   import iMap

def isListOrTuple( u ):
    #
    return isinstance( u, ( list, tuple ) )


def isSequence( u ):
    #
    #return isListOrTuple( u ) or isinstance( u, str )
    return isinstance( u, ( list, tuple, str ) )


def isSet( u ):
    #
    return isinstance( u, ( set, frozenset ) )


def isCollection( u ):
    #
    return isSequence( u ) or isSet( u )


def hasSomething( seq ):
    #
    """
    this stops testing after finding one list member that evaluates as true.
    """
    #
    #
    return bool( get1stTrue( seq ) )


def hasNothing( seq ):
    #
    """
    this stops testing after finding one list member that evaluates as true.
    """
    #
    return not hasSomething( seq )



def _hasAny( iterable ):
    '''
    any(iterable) -> bool
    Return True if bool(x) is True for any x in the iterable.
    any() built-in was new in 2.5
    hasAny is a substitute for 2.4 or earlier
    '''
    for element in iterable:
        if element:
            return True
    return False


try:
    any( range(5) ) # any() built-in was new in 2.5
    hasAny = any
except:
    hasAny = _hasAny



def isStingLike( uTest ):
    #
    try:                uTest + ''
    except TypeError:   return False
    else:               return True


def _isIterableObsolete( uTest ):
    #
    try: iter # iter was new in 2.2
    except:
        try:
            for x in uTest:
                return True
            else:
                return True
        except:
            return False
    else:
        try:    iter( uTest )
        except: return False
        else:   return True


def isIterable( uTest ): # was named isLoopable
    #
    try:    iter( uTest )
    except: return False
    else:   return True


def isScaler( uTest ):
    #
    return isStingLike( uTest ) or not isIterable( uTest )



def _isEqual(    lA, lB ): return lA == lB

def _isNotEqual( lA, lB ): return lA != lB


def isInSortedList( uItem, lList, fEquality = _isEqual ):
    #
    # from original Python cookbook -- list must be sorted!
    #
    #
    if not isinstance( lList, list ):
        raise TypeError( 'sequence must be a list' )
    #
    iInsertHere = bisect_right( lList, uItem )
    #
    return fEquality( lList[ iInsertHere - 1 : iInsertHere ], [ uItem ] )



def isNotInSortedList( uItem, lList ):
    #
    # from original Python cookbook -- list must be sorted!#
    #
    #                    note the equality tester is _isNotEqual
    return isInSortedList( uItem, lList, fEquality = _isNotEqual )



def isEmpty( u ):
    #
    return u is None or len( u ) == 0



def hasNoEmpties( lSeq ):
    #
    return not hasAnyEmpty( lSeq )


def isAllEmpty( lSeq ):
    #
    #
    return allMeet( lSeq, isEmpty )


def hasNonEmpty( lSeq ):
    #
    return not isAllEmpty( lSeq )


def getHasTester( collect, bGetHasTester = True ):
    #
    """
    This returns a tester for whether an item is in something,
    so you must pass the something.
    This program will try to copy the something,
    so the calling program cannot change the something for accurate results.
    getHasNotTester calls this and is used more widely
    """
    #
    #
    try:
        #
        lList       = list( collect )
        #
        lList.sort()
        #
        if bGetHasTester:
            #
            hasTest = isInSortedList
            #
        else: # tester for not in list
            #
            hasTest = isNotInSortedList
            #
        #
        def hasMember( uTest ): return hasTest( uTest, lList )
        #
    except:
        #
        if bGetHasTester:
            #
            def hasMember( uTest ): return uTest in collect
            #
        else: # tester for not in list
            #
            def hasMember( uTest ): return not uTest in collect
            #
        #
    #
    return hasMember



def getHasNotTester( collect ):
    #
    """
    This returns a tester for whether an item is not in something.
    """
    #
    return getHasTester( collect, bGetHasTester = False )




def isSeq1SubsetOfSeq2( seq1, seq2, bStrict = False ):
    #
    setSeq1 = frozenset( seq1 )
    #
    setSeq2 = frozenset( seq2 )
    #
    return setSeq1.issubset( setSeq2 )


def containsAll( seq1, seq2 ):
    #
    """Check whether sequence1 contains all of the items in sequence2."""
    #
    # alternate name: hasAllIn( seq1, seq2 )
    #    
    return isSeq1SubsetOfSeq2( seq2, seq1 )



def containsAny( seq1, seq2 ):
    #
    """Check whether sequence1 contains any of the items in sequence2.
    the 1st param (seq) must have a __contains__ method
    dict, list, tuple & set are all OK
    the 2nd param (set) can be any iterable
    """
    #
    # alternate name: hasAnyIn( seq1, seq2 )
    #
    return True in iMap( seq1.__contains__, seq2 )




def allMeet( seq, pred = bool ):
    """
    Returns True if pred(x) is True for every element in the iterable
    (lazily, via shortcutting).
    """
    #
    #
    return False not in iMap( pred, seq )


def BothMeet( seq, pred = bool ):
    """
    Returns True if pred(x) is True for at least one element in the iterable
    (lazily, via shortcutting).
    """
    #
    return allMeet(seq, pred)


def NoneMeet( seq, pred = bool ): # name cannot be None!
    """
    Returns True if pred(x) is False for every element in the iterable
    (lazily, via shortcutting).
    """
    #
    #
    return True not in iMap( pred, seq )


def AnyMeet( seq, pred = bool ):
    """
    Returns True if pred(x) is True for any element in the iterable
    (lazily, via shortcutting).
    """
    #
    #
    return True in iMap( pred, seq )




def hasAnyEmpty( lSeq ):
    #
    return AnyMeet( lSeq, isEmpty )



class EndsWithableMixin( object ):
    #
    def endswith( self, seq ):
        #
        return self[ - len( seq ) : ] == seq


class TupleEndsWithable( EndsWithableMixin, tuple ): pass

class ListEndsWithable( EndsWithableMixin, list ): pass



if __name__ == "__main__":
    #
    from string import ascii_letters   as letters
    from string import ascii_uppercase as uppercase
    #
    #
    from Iter.AllVers   import iRange, lRange, tRange
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if not ( isListOrTuple( () ) and isListOrTuple( [] ) ):
        #
        lProblems.append( 'isListOrTuple()' )
        #
    #
    if            isSequence( 10 ) or  isSequence( 2. ) or \
            not ( isSequence( '' ) and isSequence( [] ) and isSequence( () ) ):
        #
        lProblems.append( 'isSequence()' )
        #
    #
    setTest = set( iRange(9) )
    #
    if not isCollection( setTest ):
        #
        lProblems.append( 'isCollection()' )
        #
    if not isSet( setTest ):
        #
        lProblems.append( 'isSet()' )
        #
    if hasSomething( [ None ] * 10 ) or not hasSomething( tRange(9) ):
        #
        lProblems.append( 'hasSomething()' )
        #
    if hasNothing( tRange(9) ) or not hasNothing( [ None ] * 10 ):
        #
        lProblems.append( 'hasNothing()' )
        #
    if not _hasAny( ( 0, 0, 0, 1 ) ):
        #
        lProblems.append( '_hasAny() got a True' )
        #
    #
    if     _hasAny( ( 0, 0, 0, 0 ) ):
        #
        lProblems.append( '_hasAny() got no Trues' )
        #
    #
    if isStingLike( [] ) or not isStingLike( 'abc' ):
        #
        lProblems.append( 'isStingLike()' )
        #
    if            isIterable( 9 ) or \
            not ( isIterable( '' ) and isIterable( [] ) and isIterable( () ) ):
        #
        lProblems.append( 'isIterable()' )
        #
    if isScaler( [] ) or not isScaler( '' ):
        #
        lProblems.append( 'isScaler()' )
        #
    if          isInSortedList( 10, lRange(9) ) or \
            not isInSortedList(  5, lRange(9) ):
        #
        lProblems.append( 'isInSortedList()' )
        #
    if          isNotInSortedList(  5, lRange(9) ) or \
            not isNotInSortedList( 10, lRange(9) ):
        #
        lProblems.append( 'isNotInSortedList()' )
        #
    if     AnyMeet( ( [ 'x' ], 'abc', { 'a' : 5 }, ( 1, )   ), isEmpty ) or \
       not allMeet( ( [],      '',    {},          ()       ), isEmpty ):
        #
        lProblems.append( 'isEmpty()' )
        #
    if      not hasAnyEmpty( ( [ 'x' ], 'abc', { 'a' : 5 }, ()     ) ) or \
                hasAnyEmpty( ( [ 'x' ], 'abc', { 'a' : 5 }, ( 1, ) ) ):
        #
        lProblems.append( 'hasAnyEmpty()' )
        #
    if          hasNoEmpties( ( [ 'x' ], 'abc', { 'a' : 5 }, ()   ) ) or \
            not hasNoEmpties( ( [ 'x' ], 'abc', { 'a' : 5 }, ( 1, ) ) ):
        #
        lProblems.append( 'hasNoEmpties()' )
        #
    if          isAllEmpty( ( [],      '',    {},          ( 1, )   ) ) or \
            not isAllEmpty( ( [],      '',    {},          ()       ) ):
        #
        lProblems.append( 'isAllEmpty()' )
        #
    if          hasNonEmpty( ( [],      '',    {},          ()       ) ) or \
            not hasNonEmpty( ( [],      '',    {},          ( 1, )   ) ):
        #
        lProblems.append( 'hasNonEmpty()' )
        #
    hasAlpha    = getHasTester(    letters )
    hasAlphaNot = getHasNotTester( letters )
    #
    if hasAlpha( '1' ) or not hasAlpha( 'a' ):
        #
        lProblems.append( 'getHasTester()' )
        #
    if hasAlphaNot( 'a' ) or not hasAlphaNot( '1' ):
        #
        lProblems.append( 'getHasNotTester()' )
        #
    if          isSeq1SubsetOfSeq2( letters, uppercase ) or \
            not isSeq1SubsetOfSeq2( uppercase, letters ) or \
            not isSeq1SubsetOfSeq2( letters, letters ):
        #
        lProblems.append( 'isSeq1SubsetOfSeq2()' )
        #
    #
    #
    if      not containsAll( letters, uppercase ) or \
                containsAll( uppercase, letters ):
        #
        # """Check whether sequence contains all of the items in the set."""
        #
        lProblems.append( 'containsAll()' )
        #
    if      not containsAny( letters, '01234e' ) or \
                containsAny( letters, '012345' ):
        #
        # """Check whether sequence contains any of the items in the set."""
        #
        lProblems.append( 'containsAny() letters compared with string' )
        #
    tLetters = tuple( letters )
    #
    if      not containsAny( tLetters, '01234e' ) or \
                containsAny( tLetters, '012345' ):
        #
        # """Check whether sequence contains any of the items in the set."""
        #
        lProblems.append( 'containsAny() tLetters compared with string' )
        #
    if      not containsAny( tLetters, tuple( '01234e' ) ) or \
                containsAny( tLetters, tuple( '012345' ) ):
        #
        # """Check whether sequence contains any of the items in the set."""
        #
        lProblems.append( 'containsAny() tLetters compared with tuple( string )' )
        #
    fTest = bool
    #
    if allMeet( iRange( 10 ), fTest ) or not allMeet( iRange( 1, 10 ), fTest ):
        #
        lProblems.append( 'All()' )
        #
    if BothMeet( ( 0, 1 ), fTest ) or not BothMeet( ( 1, 2 ), fTest ):
        #
        lProblems.append( 'Both()' )
        #
    if NoneMeet( iRange( 10 ), fTest ) or not NoneMeet( [ 0 ] * 10, fTest ):
        #
        lProblems.append( 'No()' )
        #
    #
    if AnyMeet( [ 0 ] * 10, fTest ) or not AnyMeet( iRange( 10 ), fTest ):
        #
        lProblems.append( 'Any()' )
        #
    #
    t = TupleEndsWithable( range(9) )
    #
    if not t.endswith( (6,7,8) ):
        #
        lProblems.append( 'TupleEndsWithable( range(9) ).endswith( (6,7,8)' )
        #
    #
    if t.endswith( (6,7) ):
        #
        lProblems.append( 'TupleEndsWithable( range(9) ).endswith( (6,7)' )
        #
    #
    l = ListEndsWithable( range(9) )
    #
    if not l.endswith( [6,7,8] ):
        #
        lProblems.append( 'ListEndsWithable( range(9) ).endswith( [6,7,8]' )
        #
    #
    if l.endswith( [6,7] ):
        #
        lProblems.append( 'ListEndsWithable( range(9) ).endswith( [6,7]' )
        #
    #
    sayTestResult( lProblems )
