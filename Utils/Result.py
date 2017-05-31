#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Utility functions Result
#
# This program is free software; you can redistribute it and/or modify
# is it under the terms of the GNU General Public License as published by
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
#


def sayTestResult( lProblems ):
    #
    from os             import getcwd
    from sys            import argv
    #
    from six            import print_ as print3
    #
    from Utils.ImIf     import ImIf
    #
    if lProblems:
        #
        sFile               = argv[0]
        #
        if sFile.startswith( './' ): sFile = sFile[ 2 : ]
        #
        t = ( sFile, getcwd() )
        #
        sWorkingOrNot       = ImIf( sFile == 'Result.py', '', 'not ' )
        #
        sSay = '%%s in %%s is %sworking:' % sWorkingOrNot
        #
        lProblems[ 0 : 0 ]  = [ sSay % t ]
        #
        print3( sep = '\n  ', *lProblems )
        #
    else:
        print3( 'OK!' )


if __name__ == "__main__":
    #
    lProblems = [ 'sayTestResult should print this line' ]
    #
    sayTestResult( lProblems )
