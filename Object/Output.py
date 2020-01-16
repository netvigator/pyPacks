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
    from ..Object.Get       import ValueContainerCanPrint as ValueContainer
    from ..Utils.Both2n3    import PYTHON3, print3
except ( ValueError, ImportError ):
    from   Object.Get       import ValueContainerCanPrint as ValueContainer
    from   Utils.Both2n3    import PYTHON3, print3


if PYTHON3:
    
    # python 2 pprint does not have _dispatch
    # this implementation only works in python 3

    class ValueContainerPrettyPrinter( pprint.PrettyPrinter ):

        _dispatch = pprint.PrettyPrinter._dispatch.copy()

        def _pprint_ValueContainer(
                self, object, stream, indent, allowance, context, level ):
            stream.write('ValueContainer(')
            for s in vars(object):
                stream.write( '\n%s: ' % s )
                self._format( object.__dict__[s],
                              stream, indent, allowance + 1, context, level )
            stream.write( ')' )

        _dispatch[ValueContainer.__repr__] = _pprint_ValueContainer


    CustomPPrint = ValueContainerPrettyPrinter()

else:

    CustomPPrint = pprint.PrettyPrinter()


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
    sOut = CustomPPrint.pformat( oComplex )
    sExpect = '''{'abc': [],
 'xyz': [
{   'a': 1,
    'b': 2,
    'c': 3},
         
{   'a': 1,
    'b': 2,
    'c': 3}]}'''
    #
    if sOut != sExpect:
        #
        lProblems.append( 'pprint( complex object with ValueContainer inside)' )
        #
    #
    oTest = ValueContainer( a = 'one two three four five six seven eight',
                            b = 'alpha beta gamma delta epsilon zeta eta' )
    #
    if PYTHON3:
        sExpect = '''ValueContainer(
a: 'one two three four five six seven eight'
b: 'alpha beta gamma delta epsilon zeta eta')'''
    else:
        sExpect = '''\n{   'a': 'one two three four five six seven eight',
    'b': 'alpha beta gamma delta epsilon zeta eta'}'''
    #
    sOut = CustomPPrint.pformat( oTest )
    #
    if sOut != sExpect:
        #
        print(sOut)
        lProblems.append( 'pprint( ValueContainer )' )
        #
    #
    sayTestResult( lProblems )
