#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Object functions Test
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
# Copyright 2004-2011 Rick Graves
#

def isMutable( u ):
    #
    return isinstance( u, ( list, dict, set ) )


def hasPropertyValue( oObj, sProperty ):
    #
    bHasValue = False
    #
    try:
        bHasValue = sProperty in oObj.__dict__
    except AttributeError:
        try:
            bHasValue = sProperty in oObj
        except TypeError:
            pass
    #
    return bHasValue


def isNone(    u ): return u is     None

def isNotNone( u ): return u is not None



if __name__ == "__main__":
    #
    lProblems = []
    #
    from Object.Get     import ValueContainer
    from Utils.Result   import sayTestResult
    #

    if          isMutable( 'abc' ) or \
           not( isMutable( [] ) and isMutable( {} ) and isMutable( set( [] ) ) ):
        #
        lProblems.append( 'isMutable()' )
        #
    #
    dTest = dict( foo = 1, bar = 8 )
    #
    oTest = ValueContainer(   foo = 1, bar = 8 )
    #
    if          hasPropertyValue( oTest, 'spam' ) or \
                hasPropertyValue( dTest, 'spam' ) or \
           not( hasPropertyValue( oTest, 'foo'  ) or
                hasPropertyValue( dTest, 'bar'  ) ):
        #
        lProblems.append( 'hasPropertyValue()' )
        #
    if isNone( 'abc' ) or not isNone( None ):
        #
        lProblems.append( 'isNone()' )
        #
    if isNotNone( None ) or not isNotNone( 'abc' ):
        #
        lProblems.append( 'isNotNone()' )
        #

    #
    sayTestResult( lProblems )