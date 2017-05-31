#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions Cookie
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


def getCookieFromDict( dReceiveHeaders ):
    #
    sCookie     = dReceiveHeaders.get( 'set-cookie', '' )
    #
    return sCookie.split( ';' )[0]



if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    dReceived = { 'set-cookie' : 'abcde01234', 'refered-by' : 'www.google.com' }
    #
    if getCookieFromDict( dReceived ) != 'abcde01234':
        #
        lProblems.append( 'getCookieFromDict()' )
        #


    #
    sayTestResult( lProblems )