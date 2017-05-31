#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# string functions Encrypt getEncrypted
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
# Copyright 2012-2016 Rick Graves
#
'''
call from shell

must decrypt from python cuz bash is confused by some characters

from String.Encrypt import DecryptLite

DecryptLite( {triple quotes}{string}{triple quotes} )

'''

if __name__ == "__main__":
    #
    from sys            import argv
    #
    from six            import print_ as print3
    #
    from String.Encrypt import EncryptLite
    #
    args = argv[ 1 : ]
    #
    if args:
        print3( EncryptLite( args[0] ) )
    else:
        #
        print3( 'Usage: getEncrypted {string}' )
        print3( ' put {string} in quotes if it contains any white space' )
        print3( ' must decrypt in python cuz bash gets confused by its special characters' )
        print3( ' from String.Encrypt import DecryptLite' )
        print3( ' DecryptLite( {triple quotes}{string}{triple quotes} )' )