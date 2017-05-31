#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# string functions Convert bytes <-> string Python3 but Python2 compatible
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

'''

from six import print_ as print3

bDebutPrint = False
#
class Finished( Exception ): pass


def getString( u, encoding = 'utf-8' ):
    #
    sReturn = u
    #
    try:
        #
        if isinstance( u, str ):
            #
            raise Finished
            #
        #
        sReturn = str( u, encoding = encoding )
        #
    except TypeError:
        #
        sReturn = str( u )
        #
    except ( Finished, UnicodeEncodeError ):
        #
        pass
        #
    #
    return sReturn



def _AsciiOneByOne( s ):
    #
    from Iter.AllVers   import iRange
    from String.Replace import getSpaceForWhiteAlsoStrip
    from String.Test    import isASCII_128
    #
    l = [ ' ' ] * len( s )
    #
    for i in iRange( len( s ) ):
        #
        if isASCII_128( s[i] ):
            #
            l[i] = s[i]
            #
        #
    #
    s = ''.join( l ).strip()
    #
    return getSpaceForWhiteAlsoStrip( s )



def getUnicodeOut( s ):
    #
    from unicodedata    import normalize
    #
    from String.Test    import hasAscii_128_Only
    try:
        #
        sReturn = getString( normalize( 'NFKD', s ).encode('ascii','ignore') )
        #
    except TypeError:
        #
        sReturn = s # all ascii
        #
        if bDebutPrint:
            #
            print3( 'got TypeError, must be all ascii' )
            #
        #
    except UnicodeDecodeError:
        #
        # choke!
        #
        sReturn = _AsciiOneByOne( s )
        #
        if bDebutPrint:
            #
            print3( 'got UnicodeDecodeError, called _AsciiOneByOne()' )
            #
        #
    else:
        #
        if bDebutPrint:
            #
            print3( "normalize( 'NFKD', s ).encode('ascii','ignore') "
                    "returned %s" % sReturn )
            #
        #
    #
    if not hasAscii_128_Only( sReturn ):
        #
        sReturn = _AsciiOneByOne( sReturn )
        #
        if bDebutPrint:
            #
            print3( 'not hasAscii_128_Only(sReturn), called _AsciiOneByOne()' )
            #
        #
    #
    return sReturn


if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    from Utils.Version  import PYTHON3
    #
    lProblems = []
    #
    s = '대한민국 서울특별시 종로구 종로6가 69'
    #
    if getString( s ) != s:
        #
        lProblems.append( 'getString() when string passed, should return string' )
        #
    #
    if PYTHON3:
        #
        sB = '종로6가 69'.encode('utf-8')
        #
        if getString( sB ) != "종로6가 69":
            #
            lProblems.append( 'getString() python3 when bytes passed, should return string' )
            #
        #
    else:
        #
        s = '종로6가 69'
        #
        if getString( s ) != s:
            #
            lProblems.append( 'getString() python 2 when string passed, should return string' )
            #
        #
        u = unicode( 'abcdefg' )
        #
        if getString( u ) != 'abcdefg':
            #
            lProblems.append( 'getString() python 2 when unicode passed, should return string' )
            #
        #
    #
    s = '대한민국 서울특별시 종로구 종로6가 69'
    #
    if _AsciiOneByOne( s ) != '6 69':
        #    
        lProblems.append( '_AsciiOneByOne()' )
        #
    #
    
    #
    sPhone = u'416 961 3455Â'
    #
    bDebutPrint = not True
    #
    sWant   = '416 961 3455A'
    sResult = getUnicodeOut( sPhone )
    #  
    if sResult != sWant:
        #
        print3( 'expecting %s, got %s' % ( sWant, sResult ) )
        lProblems.append( 'getUnicodeOut()' )
        #
    #
    bDebutPrint = False
    #
    #
    #
    sayTestResult( lProblems )