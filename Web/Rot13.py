#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions Rot13
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

from six.moves.urllib.parse import quote, unquote

from String.Encrypt import getRot13

def getDecodeRot13( s ):
    #
    # not used anywhere yet
    #
    #from Utils.Both2n3  import unquote
    #
    return unquote( getRot13( s ) )




def getEncodeRot13( s ):
    #
    # not used anywhere yet
    #
    #from Utils.Both2n3  import quote
    #
    return getRot13( quote( s ) )



def getPhpDecodeRot13( s ):
    #
    # not used anywhere yet
    #
    #from Utils.Both2n3  import unquote
    #
    return getRot13( unquote( s.replace( '%25', '%' ) ) )



def getPhpEncodeRot13( s ):
    #
    # not used anywhere yet
    #
    #from Utils.Both2n3  import quote
    #
    return quote( getRot13( s ) ).replace( '%', '%25' )






if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    sTest   = 'How now 10 brown cows!'
    #
    sRot13  = 'Ubj%20abj%2010%20oebja%20pbjf%21'
    #
    sPhp13  = 'Ubj%2520abj%252010%2520oebja%2520pbjf%2521'
    #
    if getDecodeRot13( sRot13 ) != sTest:
        #
        lProblems.append( 'getDecodeRot13()' )
        #
    if getEncodeRot13( sTest ) != sRot13:
        #
        lProblems.append( 'getEncodeRot13()' )
        #
    if getPhpDecodeRot13( sPhp13 ) != sTest:
        #
        lProblems.append( 'getPhpDecodeRot13()' )
        #
    if getPhpEncodeRot13( sTest ) != sPhp13:
        #
        lProblems.append( 'getPhpEncodeRot13()' )
        #


    #
    sayTestResult( lProblems )