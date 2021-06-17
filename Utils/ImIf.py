#!/home/rick/bin/pythonTest
# -*- coding: utf-8 -*-
#
# intermediate If function aka Conditional expressions or ternary operator
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
# Copyright 2004-2021 Rick Graves
#
'''
Conditional expressions (sometimes called a “ternary operator”)
New in version 2.5
This ImIf module is obsolete!
it is better to use conditional expressions than to call this!
'''

try:
    from ..Utils.Version    import isVersAtLeast
except ( ValueError, ImportError ):
    from Utils.Version      import isVersAtLeast

if isVersAtLeast( "2.5" ):
    #
    def ImIf( bCondition, uTrue, uFalse ):  # Immediate If
        #
        return uTrue if bCondition else uFalse
    #
else:
    #
    def ImIf( bCondition, uTrue, uFalse ):  # Immediate If
        #
        return ( uTrue, uFalse )[ not bCondition ]





if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if      ImIf( 0, 'abc', '123' ) != '123' or \
            ImIf( 1, 'abc', '123' ) != 'abc':
        #
        lProblems.append( 'ImIf()' )
        #
    if ImIf( 0, 1, 2 ) != 2 or ImIf( 1, 1, 2 ) != 1:
        #
        lProblems.append( 'ImIf()' )
        #
    #


    #
    sayTestResult( lProblems )
