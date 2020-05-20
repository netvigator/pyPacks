#!/home/rick/bin/pythonTest
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
#   http://www.gnu.org/licenses/
#
# Copyright 2004-2020 Rick Graves
#
from copy import deepcopy

try:
    from ..Iter.AllVers     import iZip
    from ..Iter.Get         import getIterSwapValueKey as _getIterSwapValueKey
    from ..Object.Test      import isMutable
    from ..Utils.Version    import PYTHON3
except ( ValueError, ImportError ):
    from Iter.AllVers       import iZip
    from Iter.Get           import getIterSwapValueKey as _getIterSwapValueKey
    from Object.Test        import isMutable
    from Utils.Version      import PYTHON3


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
    return dict( iZip( lKeys, lValues ) ) # dict() new in 2.2



def _getTypicalValueIter( uTypicalValue = None ):
    #
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
    This is done CAREFULLY where the original values may be 
    lists, tuples or strings."""
    #
    lValueuKeys = []
    #
    for uKey, uValue in getItemIter( dOrig ):
        #
        if type( uValue ) in ( tuple, list ):
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

    getDictSubset( dOrig, 'a', 'b', 'c' ) returns
    nNew as {'a': 1, 'b': 2, 'c': 3}

    getDictSubset( dOrig, 'c', 'f', 'z' ) returns
    nNew as { 'c': 3, 'f': 6 }

    getDictSubset( dOrig, 'z' ) returns
    nNew as {}
    '''
    #
    dNew = {}
    #
    for k in args:
        #
        if k in dOrig:
            #
            dNew[ k ] = dOrig.get( k )
            #
        #
    #
    return dNew


def getAnyKey( d ):
    #
    '''maybe most useful where you have a dict, you know it only has one key 
    but you do not know exactly what that key is.'''
    #
    anyKey = None
    #
    l = list( d.keys() )
    #
    if l: anyKey = l[0]
    #
    return anyKey



def getAnyValue( d ):
    #
    '''maybe most useful where you have a dict, you know it only has one item,
    and you want the value not the key.'''
    #
    anyValue = None
    #
    l = list( d.values() )
    #
    if l: anyValue = l[0]
    #
    return anyValue



# from http://code.activestate.com/recipes/576693/
# Backport of OrderedDict() class that runs on Python 2.4, 2.5, 2.6, 2.7 and pypy.
# Passes Python2.7's test suite and incorporates all the latest updates.


try:
    from _abcoll import KeysView, ValuesView, ItemsView
except ImportError:
    pass


class OrderedDictBackport(dict):
    'Dictionary that remembers insertion order'
    # An inherited dict maps keys to values.
    # The inherited dict provides __getitem__, __len__, __contains__, and get.
    # The remaining methods are order-aware.
    # Big-O running times for all methods are the same as for regular dictionaries.

    # The internal self.__map dictionary maps keys to links in a doubly linked list.
    # The circular doubly linked list starts and ends with a sentinel element.
    # The sentinel element never gets deleted (this simplifies the algorithm).
    # Each link is stored as a list of length three:  [PREV, NEXT, KEY].

    def __init__(self, *args, **kwds):
        '''Initialize an ordered dictionary.  Signature is the same as for
        regular dictionaries, but keyword arguments are not recommended
        because their insertion order is arbitrary.

        '''
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        try:
            self.__root
        except AttributeError:
            self.__root = root = []                     # sentinel node
            root[:] = [root, root, None]
            self.__map = {}
        self.__update(*args, **kwds)

    def __setitem__(self, key, value, dict_setitem=dict.__setitem__):
        'od.__setitem__(i, y) <==> od[i]=y'
        # Setting a new item creates a new link which goes at the end of the linked
        # list, and the inherited dictionary is updated with the new key/value pair.
        if key not in self:
            root = self.__root
            last = root[0]
            last[1] = root[0] = self.__map[key] = [last, root, key]
        dict_setitem(self, key, value)

    def __delitem__(self, key, dict_delitem=dict.__delitem__):
        'od.__delitem__(y) <==> del od[y]'
        # Deleting an existing item uses self.__map to find the link which is
        # then removed by updating the links in the predecessor and successor nodes.
        dict_delitem(self, key)
        link_prev, link_next, key = self.__map.pop(key)
        link_prev[1] = link_next
        link_next[0] = link_prev

    def __iter__(self):
        'od.__iter__() <==> iter(od)'
        root = self.__root
        curr = root[1]
        while curr is not root:
            yield curr[2]
            curr = curr[1]

    def __reversed__(self):
        'od.__reversed__() <==> reversed(od)'
        root = self.__root
        curr = root[0]
        while curr is not root:
            yield curr[2]
            curr = curr[0]

    def clear(self):
        'od.clear() -> None.  Remove all items from od.'
        try:
            for node in self.__map.itervalues():
                del node[:]
            root = self.__root
            root[:] = [root, root, None]
            self.__map.clear()
        except AttributeError:
            pass
        dict.clear(self)

    def popitem(self, last=True):
        '''od.popitem() -> (k, v), return and remove a (key, value) pair.
        Pairs are returned in LIFO order if last is true or FIFO order if false.

        '''
        if not self:
            raise KeyError('dictionary is empty')
        root = self.__root
        if last:
            link = root[0]
            link_prev = link[0]
            link_prev[1] = root
            root[0] = link_prev
        else:
            link = root[1]
            link_next = link[1]
            root[1] = link_next
            link_next[0] = root
        key = link[2]
        del self.__map[key]
        value = dict.pop(self, key)
        return key, value

    # -- the following methods do not depend on the internal structure --

    def keys(self):
        'od.keys() -> list of keys in od'
        return list(self)

    def values(self):
        'od.values() -> list of values in od'
        return [self[key] for key in self]

    def items(self):
        'od.items() -> list of (key, value) pairs in od'
        return [(key, self[key]) for key in self]

    def iterkeys(self):
        'od.iterkeys() -> an iterator over the keys in od'
        return iter(self)

    def itervalues(self):
        'od.itervalues -> an iterator over the values in od'
        for k in self:
            yield self[k]

    def iteritems(self):
        'od.iteritems -> an iterator over the (key, value) items in od'
        for k in self:
            yield (k, self[k])

    def update(*args, **kwds):
        '''od.update(E, **F) -> None.  Update od from dict/iterable E and F.

        If E is a dict instance, does:           for k in E: od[k] = E[k]
        If E has a .keys() method, does:         for k in E.keys(): od[k] = E[k]
        Or if E is an iterable of items, does:   for k, v in E: od[k] = v
        In either case, this is followed by:     for k, v in F.items(): od[k] = v

        '''
        if len(args) > 2:
            raise TypeError('update() takes at most 2 positional '
                            'arguments (%d given)' % (len(args),))
        elif not args:
            raise TypeError('update() takes at least 1 argument (0 given)')
        self = args[0]
        # Make progressively weaker assumptions about "other"
        other = ()
        if len(args) == 2:
            other = args[1]
        if isinstance(other, dict):
            for key in other:
                self[key] = other[key]
        elif hasattr(other, 'keys'):
            for key in other.keys():
                self[key] = other[key]
        else:
            for key, value in other:
                self[key] = value
        for key, value in kwds.items():
            self[key] = value

    __update = update  # let subclasses override update without breaking __init__

    __marker = object()

    def pop(self, key, default=__marker):
        '''od.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised.

        '''
        if key in self:
            result = self[key]
            del self[key]
            return result
        if default is self.__marker:
            raise KeyError(key)
        return default

    def setdefault(self, key, default=None):
        'od.setdefault(k[,d]) -> od.get(k,d), also set od[k]=d if k not in od'
        if key in self:
            return self[key]
        self[key] = default
        return default

    def __repr__(self, _repr_running={}):
        'od.__repr__() <==> repr(od)'
        call_key = id(self), _get_ident()
        if call_key in _repr_running:
            return '...'
        _repr_running[call_key] = 1
        try:
            if not self:
                return '%s()' % (self.__class__.__name__,)
            return '%s(%r)' % (self.__class__.__name__, self.items())
        finally:
            del _repr_running[call_key]

    def __reduce__(self):
        'Return state information for pickling'
        items = [[k, self[k]] for k in self]
        inst_dict = vars(self).copy()
        for k in vars(OrderedDict()):
            inst_dict.pop(k, None)
        if inst_dict:
            return (self.__class__, (items,), inst_dict)
        return self.__class__, (items,)

    def copy(self):
        'od.copy() -> a shallow copy of od'
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        '''OD.fromkeys(S[, v]) -> New ordered dictionary with keys from S
        and values equal to v (which defaults to None).

        '''
        d = cls()
        for key in iterable:
            d[key] = value
        return d

    def __eq__(self, other):
        '''od.__eq__(y) <==> od==y.  Comparison to another OD is order-sensitive
        while comparison to a regular mapping is order-insensitive.

        '''
        if isinstance(other, OrderedDict):
            return len(self)==len(other) and self.items() == other.items()
        return dict.__eq__(self, other)

    def __ne__(self, other):
        return not self == other

    # -- the following methods are only used in Python 2.7 --

    def viewkeys(self):
        "od.viewkeys() -> a set-like object providing a view on od's keys"
        return KeysView(self)

    def viewvalues(self):
        "od.viewvalues() -> an object providing a view on od's values"
        return ValuesView(self)

    def viewitems(self):
        "od.viewitems() -> a set-like object providing a view on od's items"
        return ItemsView(self)


try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = OrderedDictBackport


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
    dIntegerKeys = { 0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e',
                     5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j'}
    #
    if getDictOffPairOfLists( tTest0, tTestA ) != dIntegerKeys:
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
        lProblems.append( 'getDictSubset() has all' )
        #
    #
    tMaybe = ( 'c', 'f', 'z' )
    dWant  = dict( c = 3, f = 6 )
    #
    if getDictSubset( dOrig, *tMaybe ) != dWant:
        #
        lProblems.append( 'getDictSubset() has some' )
        #
    #
    if getAnyKey( dOrig ) not in dOrig:
        #
        lProblems.append( 'getAnyKey() key should be in there' )
        #
    #
    if getAnyKey( {} ) in dOrig:
        #
        lProblems.append( 'getAnyKey() no key not in there' )
        #
    #
    if getAnyKey( dOrig ) in dIntegerKeys:
        #
        lProblems.append( 'getAnyKey() key definitely not in there' )
        #
    #
    setOrigValues = frozenset( dOrig.values() )
    #
    if getAnyValue( dOrig ) not in setOrigValues:
        #
        lProblems.append( 'getAnyValues() value should be in there' )
        #
    #
    if getAnyValue( {} ) in setOrigValues:
        #
        lProblems.append( 'getAnyValue() no value not in there' )
        #
    #
    setIntegerKeyValues = frozenset( dIntegerKeys.values() )
    #
    if getAnyValue( dOrig ) in setIntegerKeyValues:
        #
        lProblems.append( 'getAnyValue() value definitely not in there' )
        #
    #
    l = [ t for t in OrderedDictBackport(
            [('a', 1), ('b', 2), ('c', 3), ('d', 4)]).iteritems() ]
    #
    if l != [('a', 1), ('b', 2), ('c', 3), ('d', 4)]:
        #
        lProblems.append( 'OrderedDictBackport()' )
        #
    #
    sayTestResult( lProblems )
