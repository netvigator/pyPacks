#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Collection functions Query
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
# shamelessly copied from
# Named Tuples (Python recipe)
# http://code.activestate.com/recipes/500261/

from operator       import itemgetter as _itemgetter
from keyword        import iskeyword as _iskeyword
import sys as _sys
from sys            import exc_info

from six            import print_ as print3

from Utils.Version  import PYTHON3

if PYTHON3:
    from Utils.Exec3 import doExec3 as Exec
    basestring = str
else:
    from Utils.Exec2 import doExec2 as Exec

def _NamedTuple(typename, field_names, verbose=False, rename=False):
    """
    Returns a new subclass of tuple with named fields.
    """

    # Parse and validate the field names.  Validation serves two purposes,
    # generating informative error messages and preventing template injection attacks.
    if isinstance(field_names, basestring):
        field_names = field_names.replace(',', ' ').split() # names separated by whitespace and/or commas
    field_names = tuple(map(str, field_names))
    if rename:
        names = list(field_names)
        seen = set()
        for i, name in enumerate(names):
            if (not min(c.isalnum() or c=='_' for c in name) or _iskeyword(name)
                or not name or name[0].isdigit() or name.startswith('_')
                or name in seen):
                    names[i] = '_%d' % i
            seen.add(name)
        field_names = tuple(names)
    for name in (typename,) + field_names:
        if not min(c.isalnum() or c=='_' for c in name):
            raise ValueError('Type names and field names can only contain alphanumeric characters and underscores: %r' % name)
        if _iskeyword(name):
            raise ValueError('Type names and field names cannot be a keyword: %r' % name)
        if name[0].isdigit():
            raise ValueError('Type names and field names cannot start with a number: %r' % name)
    seen_names = set()
    for name in field_names:
        if name.startswith('_') and not rename:
            raise ValueError('Field names cannot start with an underscore: %r' % name)
        if name in seen_names:
            raise ValueError('Encountered duplicate field name: %r' % name)
        seen_names.add(name)

    # Create and fill-in the class template
    numfields = len(field_names)
    argtxt = repr(field_names).replace("'", "")[1:-1]   # tuple repr without parens or quotes
    reprtxt = ', '.join('%s=%%r' % name for name in field_names)
    template = '''class %(typename)s(tuple):
        '%(typename)s(%(argtxt)s)' \n
        __slots__ = () \n
        _fields = %(field_names)r \n
        def __new__(_cls, %(argtxt)s):
            return _tuple.__new__(_cls, (%(argtxt)s)) \n
        @classmethod
        def _make(cls, iterable, new=tuple.__new__, len=len):
            'Make a new %(typename)s object from a sequence or iterable'
            result = new(cls, iterable)
            if len(result) != %(numfields)d:
                raise TypeError('Expected %(numfields)d arguments, got %%d' %% len(result))
            return result \n
        def __repr__(self):
            return '%(typename)s(%(reprtxt)s)' %% self \n
        def _asdict(self):
            'Return a new dict which maps field names to their values'
            return dict(zip(self._fields, self)) \n
        def _replace(_self, **kwds):
            'Return a new %(typename)s object replacing specified fields with new values'
            result = _self._make(map(kwds.pop, %(field_names)r, _self))
            if kwds:
                raise ValueError('Got unexpected field names: %%r' %% kwds.keys())
            return result \n
        def __getnewargs__(self):
            return tuple(self) \n\n''' % locals()
    for i, name in enumerate(field_names):
        template += '        %s = _property(_itemgetter(%d))\n' % (name, i)
    if verbose:
        print3( template )

    # Execute the template string in a temporary namespace
    namespace = dict(_itemgetter=_itemgetter, __name__='_NamedTuple_%s' % typename,
                     _property=property, _tuple=tuple)
    try:
        Exec( template, namespace )
    except SyntaxError:
        #
        error, msg, traceback = exc_info()
        raise SyntaxError( msg + ':\n' + template)
        #
    result = namespace[typename]

    # For pickling to work, the __module__ variable needs to be set to the frame
    # where the named tuple is created.  Bypass this step in enviroments where
    # sys._getframe is not defined (Jython for example) or sys._getframe is not
    # defined for arguments greater than 0 (IronPython).
    try:
        result.__module__ = _sys._getframe(1).f_globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        pass

    return result



try:
    #
    from collections import namedtuple
    #
except ImportError:
    #
    namedtuple = _NamedTuple



if __name__ == '__main__':
    # verify that instances can be pickled
    try:
        from cPickle import loads, dumps
    except ImportError:
        from  pickle import loads, dumps
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    Point = _NamedTuple('Point', 'x, y', not True)
    p = Point(x=10, y=20)
    assert p == loads(dumps(p, -1))

    # test and demonstrate ability to override methods
    class Point(_NamedTuple('Point', 'x y')):
        @property
        def hypot(self):
            return (self.x ** 2 + self.y ** 2) ** 0.5
        def __str__(self):
            return 'Point: x=%6.3f y=%6.3f hypot=%6.3f' % (self.x, self.y, self.hypot)

    for p in Point(3,4), Point(14,5), Point(9./7,6):
        # print3( p )
        pass

    class Point(_NamedTuple('Point', 'x y')):
        'Point class with optimized _make() and _replace() without error-checking'
        _make = classmethod(tuple.__new__)
        def _replace(self, _map=map, **kwds):
            return self._make(_map(kwds.get, ('x', 'y'), self))

    # print3( Point(11, 22)._replace(x=100) )
    #
    Point = _NamedTuple('Point', 'x y')
    #
    if Point.__doc__ != 'Point(x, y)':
        #
        lProblems.append( 'Point.__doc__' )
        #
    #
    p = Point(11, y=22)
    #
    if p[0] + p[1] != 33:
        #
        lProblems.append( 'cannot indexable like a plain tuple' )
        #
    #
    x, y = p
    #
    if ( x, y ) != (11, 22):
        #
        lProblems.append( 'cannot unpack like a regular tuple' )
        #
    #
    if p.x + p.y != 33:
        #
        lProblems.append( 'cannot access fields by name' )
        #
    #
    d = p._asdict()
    #
    if d['x'] != 11:
        #
        lProblems.append( 'cannot convert to a dictionary' )
        #
    #
    
    #
    if str( Point(**d) ) != 'Point(x=11, y=22)':
        #
        lProblems.append( 'cannot convert from a dictionary' )
        #
    # 
    # _replace() is like str.replace() but targets named fields
    #
    if str( p._replace(x=100) ) != 'Point(x=100, y=22)':
        #
        lProblems.append( '_replace() not working' )
        #
    #
    sayTestResult( lProblems )