#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# dir functions Test
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
# Copyright 2004-2015 Rick Graves
#

def isDirThere( sDir ):
    #
    from os import access, F_OK
    #
    return access( sDir, F_OK )


def isDirWritable( sDir ):
    #
    from os import access, W_OK
    #
    return access( sDir, W_OK )


def isDirThereAndWritable( sDir ):
    #
    return isDirThere( sDir ) and isDirWritable( sDir )


if __name__ == "__main__":
    #
    from Dir.Get        import sTempDir
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if isDirThere( '/xyz' ) or not isDirThere( sTempDir ):
        #
        lProblems.append( 'isDirThere()' )
        #
    #
    if isDirWritable( '/root' ) or not isDirWritable( sTempDir ):
        #
        lProblems.append( 'isDirWritable()' )
        #

    #
    sayTestResult( lProblems )