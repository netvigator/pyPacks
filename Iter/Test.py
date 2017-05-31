#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Iter functions Test
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



def isIterator( u ):
    #
    from Utils.Version import PYTHON3, PYTHON2
    #
    setDir = frozenset( dir( u ) )
    #
    return '__iter__' in setDir and (
        ( PYTHON2 and   'next'   in setDir ) or
        ( PYTHON3 and '__next__' in setDir ) )


def _getIterableTypes():
    #
    from Iter.Get    import iRevRange
    from Utils.Get   import getTrue
    #
    # range objects can be used over and over
    # some others cannot
    #
    iRange      = iRevRange(5)
    tRange      = tuple( range(5) )
    iMap        = map( int,         tRange )
    iZip        = zip( range(5),    tRange )
    iFilter     = filter( getTrue,  tRange )
    iList       = list(             tRange )
    iSet        = set(           tRange )
    iSetFroze   = frozenset(     tRange )
    iDict       = { 'a' : 1, 'b' : 2, 'c' : 3 }
    iString     = 'abc'
    #
    # must use native built ins to test here!
    #
    tTypes = map( type, (
        iRange, iMap, iZip, iFilter,
        iList, tRange, iSet, iSetFroze,
        iDict, iString,
        iDict.keys(), iDict.values() ) )
    #
    return tuple( frozenset( tTypes ) )

tIterableTypes = _getIterableTypes()


def isIterable( u ):
    #
    return isinstance( u, tIterableTypes ) or isIterator( u )




if __name__ == "__main__":
    #
    from Iter.AllVers   import iMap
    from Iter.Get       import iRevRange, lRevRange, tRevRange
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    lTest       = lRevRange( 5 )
    tTest       = tRevRange( 5 )
    setTest     = set( lTest )
    iterTest    = iMap( str, tTest )
    iRange      = iRevRange( 5 )
    #
    if not isIterator( iterTest ):
        #
        lProblems.append( 'isIterator()' )
        #
    if      not ( isIterable( setTest  ) and
                  isIterable( lTest    ) and
                  isIterable( iterTest ) and
                  isIterable( iRange   ) and
                  isIterable( tTest    ) ):
        #
        lProblems.append( 'isIterable()' )
        #

    #
    sayTestResult( lProblems )