#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# intermediate If function
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



def ImIf( bCondition, uTrue, uFalse ):  # Immediate If
    #
    return ( uTrue, uFalse )[ int( not bCondition ) ]



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