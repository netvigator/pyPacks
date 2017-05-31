#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Utility functions Combos combinatorial.py
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; __either version 2 of the License, or
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
"""
inspired by combinatorial.py
Text Processing in Python
by David Mertz
2003
function names beginning with double underscores are originals from the book
upper case function names are new, enhanced
1) utilize shortcutting and/or
2) accept any number of input functions as excess positional args
   instead of requiring a list or tuple as in the originals.
"""

from operator       import mul, add
from copy           import copy

from six.moves      import reduce as Reduce

from Collect.Query  import get1stTrue, get1stFalse
from Iter.AllVers   import iMap, tMap
#from Utils.Both2n3 import Reduce

#__apply_each = lambda fns, args=[]: m@p( apply, fns, [args]*len(fns))

__apply_each = lambda fns, args=[]: [ fn( *copy( args ) ) for fn in fns ]

def _applyEach( lFuncs, lArgs = [] ):
    #
    # return m@p( apply, lFuncs, lArgs * len( lFuncs ) )
    #
    for Function in lFuncs: yield Function( *copy( lArgs ) )

__bools = lambda l: tMap( bool, l )

__bool_each = lambda fns, args=[]: __bools( __apply_each( fns, args ) )

__conjoin = lambda fns, args=[]: Reduce( mul, __bool_each( fns, args ) )

def _Conjoin( lFuncs, lArgs = [] ):
    #
    return get1stFalse( _applyEach( lFuncs, lArgs ) ) is None

def _all(iterable): return get1stFalse( iterable ) is None

try:
    #
    all( ( 1, 1, 1 ) ) # new in 2.5
    #
    All = all
    #
except:
    #
    #def all(iterable):
        #for element in iterable:
            #if not element:
                #return False
        #return True
    #
    All = _all # importable in versions prior to 2.5


__all = lambda fns: lambda arg, fns=fns: __conjoin( fns, (arg,) )

#All_ = lambda *fns: lambda arg, fns=fns: _Conjoin( fns, (arg,) )

def All_( *fns ):
    #
    def f( arg, fns=fns ):
        #
        return _Conjoin( fns, (arg,) )
    #
    return f


# both = lambda f, g: __all( ( f, g ) )

def Both_( f, g ): return All_( f, g )

# and_ = lambda f, g: lambda x, f=f, g=g: f(x) and g(x)


def _any(iterable): return get1stTrue( iterable ) is not None

try:
    any( ( 1, 1, 1 ) ) # new in 2.5
    Any = any
except:
    #
    #def any(iterable):
        #for element in iterable:
            #if element:
                #return True
        #return False
    #
    Any = _any # importable in versions prior to 2.5



def No( iterable, fCondition = bool ):
    #
    from Collect.Query import get1stThatMeets
    #
    return get1stThatMeets( iterable, fCondition = fCondition ) is None



__disjoin = lambda fns, args = []: Reduce( add, __bool_each( fns, args ) )

__some = lambda fns: lambda arg, fns=fns: __disjoin( fns, (arg,) )

__either = lambda f, g: __some( ( f, g ) )

def _Disjoin( lFuncs, lArgs = [] ):
    #
    return get1stTrue( _applyEach( lFuncs, lArgs ) ) is not None

#Any_ = lambda *fns: lambda arg, fns=fns: _Disjoin( fns, (arg,) )

def Any_( *fns ):
    #
    def f( arg, fns=fns ):
        #
        return _Disjoin( fns, (arg,) )
    #
    return f


#Either = lambda f, g: Any_( f, g )

def Either( f, g ):
    #
    return Any_( f, g )



def getComboMeets( dCombos, setInclude, fCombo = All_ ):
    #
    '''
    this is a test function factory
    in many cases, a combination function can be hard coded
    but this function allows the combination to be made "on the fly"
    such as via parameter or configuration file
    
    pass 
    1) a dictionary of test functions (key = name, value = function)
    2) a collection containing the names of the functions desired
    
    returns a combination function
    
    self test code includes a simple example
    '''
    #
    lInclude = [ dCombos[ sInclude ]
                 for sInclude in dCombos
                 if  sInclude in setInclude ]
    #
    iIncludeLen = len( lInclude )
    #
    sMsg        = None
    isInclude   = None
    #
    if  iIncludeLen != len( setInclude ):
        #
        sMsg = 'error in Include set, did not find all tests to include'
        #
    elif iIncludeLen == 1:
        #
        isInclude = lInclude[0]
        #
    elif iIncludeLen: # 2 or more
        #
        isInclude = fCombo( *lInclude )
        #
    else: # not iIncludeLen
        #
        sMsg = 'error in Include set, must specify tests to include'
        #
    #
    return isInclude, sMsg


def getComboMeetsAll( dCombos, setInclude ):
    #
    '''
    this is a test function factory
    in many cases, a combination function can be hard coded
    but this function allows the combination to be made "on the fly"
    such as via parameter or configuration file
    
    pass 
    1) a dictionary of test functions (key = name, value = function)
    2) a collection containing the names of the functions desired
    
    returns a combination function
    
    self test code includes a simple example
    '''
    #
    return getComboMeets( dCombos, setInclude )


def getComboMeetsAny( dCombos, setInclude ):
    #
    '''
    this is a test function factory
    in many cases, a combination function can be hard coded
    but this function allows the combination to be made "on the fly"
    such as via parameter or configuration file
    
    pass 
    1) a dictionary of test functions (key = name, value = function)
    2) a collection containing the names of the functions desired
    
    returns a combination function
    
    self test code includes a simple example
    '''
    #
    return getComboMeets( dCombos, setInclude, fCombo = Any_ )



if __name__ == "__main__":
    #
    from Numb.Test      import isEven, isOdd
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    f = lambda n: n**2 > 10
    g = lambda n: 38/n > 10
    h = lambda n: n**3 > 10
    #
    # n __apply_each( (f,g,h), [n] )
    # 1 [False, True, False]
    # 2 [False, True, False]
    # 3 [False, True, True ]
    # 4 [True,  False,True ]
    #
    if __apply_each( (f,g), [2] ) != [ False, True ]:
        #
        lProblems.append( '__apply_each()' )
        #
    if tuple( _applyEach( (f,g), [2] ) ) != ( False, True ):
        #
        lProblems.append( '_applyEach()' )
        #
    #
    t = ( 10, 'a', 3.14159, 0 )
    #
    if __bools( t ) != ( True, True, True, False ):
        #
        lProblems.append( '__bools()' )
        #
    #
    if __bool_each( (f,g), [2] ) != ( False, True ):
        #
        lProblems.append( '__bool_each()' )
        #
    if __conjoin( (g,h), [2] ) or not __conjoin( (g,h), [3] ):
        #
        lProblems.append( '__conjoin()' )
        #
    #
    if _Conjoin( (g,h), [2] ) or not _Conjoin( (g,h), [3] ):
        #
        lProblems.append( '_Conjoin()' )
        #
    #
    if not _all( ( 1, 1, 1 ) ) or _all( ( 1, 0, 1 ) ):
        #
        lProblems.append( '_all()' )
        #
    #
    fTest = __all( ( f, h ) )
    #
    if fTest( 2 ) or not fTest( 4 ):
        #
        lProblems.append( '__all()' )
        #
    #
    # f = lambda n: n**2 > 10
    # g = lambda n: 38/n > 10
    # h = lambda n: n**3 > 10
    #
    fTest = All_( f, h )
    #
    if fTest( 2 ) or not fTest( 4 ):
        #
        lProblems.append( 'All_()' )
        #
    #
    fTest = Both_( f, h )
    #
    if fTest( 2 ) or not fTest( 4 ):
        #
        lProblems.append( 'Both()' )
        #
    #
    if not _any( ( 0, 1, 0 ) ) or _any( ( 0, 0, 0 ) ):
        #
        lProblems.append( '_any()' )
        #
    #
    fTest = Any_( f, g )
    #
    if No( ( False, False, True ) ):
        #
        lProblems.append( 'No() something was True' )
        #
    #
    if not No( ( False, False, False ) ):
        #
        lProblems.append( 'No() nothing was True' )
        #
    #
    if not fTest( 2 ):
        #
        lProblems.append( 'Any_() false negative' )
        #
    #
    fTest = Any_( f, h )
    #
    if fTest( 2 ):
        #
        lProblems.append( 'Any_() false positive' )
        #
    #
    fTest = Either( f, g )
    #
    if not fTest( 2 ):
        #
        lProblems.append( 'Either() false negative' )
        #
    #
    fTest = Either( f, h )
    #
    if fTest( 2 ):
        #
        lProblems.append( 'Either() false positive' )
        #
    #
    def isBigggerThan5( n ): return n > 5
    def isSmallerThan9( n ): return n < 9
    #
    # isEven, isOdd
    #
    dTests = dict(
                BigggerThan5 = isBigggerThan5,
                SmallerThan9 = isSmallerThan9,
                Even         = isEven,
                Odd          = isOdd )
    #
    isTest, Msg = getComboMeetsAll(
                    dTests, ( 'BigggerThan5', 'SmallerThan9', 'Odd' ) )
    #
    if isTest( 10 ) or isTest( 4 ) or isTest( 8 ):
        #
        lProblems.append( 'getComboMeetsAll() tests should fail' )
        #
    #
    if not isTest( 7 ):
        #
        lProblems.append( 'getComboMeetsAll() test should pass' )
        #
    #
    isTest, Msg = getComboMeetsAll(
                    dTests, ( 'spam', 'toast', 'eggs' ) )
    #
    if isTest is not None:
        #
        lProblems.append( 'getComboMeetsAll() no valid tests in list' )
        #
    #
    isTest, Msg = getComboMeetsAll(
                    dTests, ( 'spam', 'SmallerThan9', 'Odd' ) )
    #
    if isTest is not None:
        #
        lProblems.append( 'getComboMeetsAll() one valid test in list' )
        #
    #
    isTest, Msg = getComboMeetsAny(
                    dTests, ( 'BigggerThan5', 'Odd' ) )
    #
    if isTest( 0 ) or isTest( 2 ) or isTest( 4 ):
        #
        lProblems.append( 'getComboMeetsAny() tests should fail' )
        #
    #
    if not ( isTest( 1 ) and isTest( 3 ) and isTest( 5 ) and isTest( 6 ) ):
        #
        lProblems.append( 'getComboMeetsAny() all tests should pass' )
        #
    #
    sayTestResult( lProblems )