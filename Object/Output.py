#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# object functions Output
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
# Copyright 2020 Rick Graves
#

import pprint

try:
    from ..Object.Get   import ValueContainerCanPrint as ValueContainer
except ( ValueError, ImportError ):
    from   Object.Get   import ValueContainerCanPrint as ValueContainer

from Utils.Both2n3      import PYTHON3

if PYTHON3:
    
    # python 2 pprint does not have _dispatch
    # this implementation only works in python 3

    class ValueContainerPrettyPrinter( pprint.PrettyPrinter ):

        _dispatch = pprint.PrettyPrinter._dispatch.copy()

        def _pprint_ValueContainer(self, object, stream, indent, allowance, context, level):
            stream.write('ValueContainer(')
            self._format(object.foo, stream, indent, allowance + 1,
                        context, level)
            self._format(object.bar, stream, indent, allowance + 1,
                        context, level)
            stream.write(')')

        _dispatch[ValueContainer.__repr__] = _pprint_ValueContainer


if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    oTest1 = ValueContainer( a = 1, b = 2, c = 3 )
    oTest2 = ValueContainer( a = 7, b = 8, c = 9 )
    #
    oComplex = dict( xyz = [oTest1,oTest1], abc = [] )
    #
    sOut = pprint.pformat( oComplex )
    sExpect = '''{'abc': [],
 'xyz': [
{   'a': 1,
    'b': 2,
    'c': 3},
         
{   'a': 1,
    'b': 2,
    'c': 3}]}'''
    #
    if PYTHON3 and sOut != sExpect:
        #
        lProblems.append( 'pprint( ValueContainer )' )
        #
    #
    sayTestResult( lProblems )
