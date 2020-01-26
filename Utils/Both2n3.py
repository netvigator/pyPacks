#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Utility Both2n3
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
# Copyright 2009-2020 Rick Graves
#
# here, must use built in map -- cannot import iMap

from os.path    import join, basename
from sys        import getdefaultencoding

sDefaultEncoding = getdefaultencoding()



def print3_n_2( *args, **kwargs ):
    #
    from sys import stdout
    #
    sep     = kwargs.pop( 'sep',  ' '    )
    beg     = kwargs.pop( 'beg',  ''     )
    end     = kwargs.pop( 'end',  '\n'   )
    file    = kwargs.pop( 'file', stdout )
    flush   = kwargs.pop( 'flush', False )
    #
    if kwargs: raise TypeError( 'extra keywords: %s' % kwargs )
    #
    if isinstance( beg, int ): beg = ' ' * beg
    #
    # here, must use built in map -- cannot import iMap
    #
    file.write( '%s%s%s' % ( beg, sep.join( map( str, args ) ), end ) )


def sayYouNeedSix():
    #
    print3_n_2( "************************" )
    print3_n_2( "************************" )
    print3_n_2( 'You need to install six!' )
    print3_n_2( "## 'pip install six'  ##" )
    print3_n_2( "************************" )
    print3_n_2( "************************" )
    #

try:
    #
    from six import print_ as print3
    #
except ImportError:
    #
    sayYouNeedSix()
    #
    raise


'''

This comment is so I can find it!

def getNext( o ):
    #
    from six import next
    #
    return next( o )

also iRange and the like are in Iter.AllVers

'''

from six import PY2 as PYTHON2
from six import PY3 as PYTHON3


if PYTHON3:
    #
    translate = str.translate
    maketrans = str.maketrans
    #
else:
    #
    from string import translate, maketrans


if PYTHON3:
    #
    def getZeroFilled( s, i ): return s.zfill( i )
    #
else:
    #
    from string import zfill as getZeroFilled


if PYTHON3:
    #
    from pathlib import Path
    #
    def getThisFileSpec( sFileName ):
        #
        return join( Path( sFileName ).parent.absolute(),
                     basename( sFileName ) )
    #
else:
    #
    from os.path import dirname, abspath
    #
    def getThisFileSpec( sFileName ):
        #
        return join( dirname( os.path.abspath( sFileName ) ),
                     basename( sFileName ) )
        #
    #
#


from six import integer_types

setNumberTypes = frozenset( [ float, bool ] + list( integer_types ) )




if PYTHON3:
    #
    def getBytes( s, encoding = sDefaultEncoding ):
        #
        if isinstance( s, str ):
            #
            return bytes( s, encoding )
            #
        else:
            #
            return s
            #
    
    def getStrGotBytes( u, encoding = sDefaultEncoding ):
        #
        if isinstance( u, str ):
            #
            sReturn = u
            #
        else:
            #
            sReturn = u.decode( encoding = encoding )
            #
        #
        return sReturn

    def getEncoded( s, sEncoding = 'utf-8' ):
        #
        '''
        Encoding is the process of translating a string of characters 
        into its raw bytes form, according to a desired encoding name.
        '''
        #
        return s.encode( encoding = sEncoding )


    def getDecoded( b, sEncoding = 'utf-8' ):
        #
        '''
        Decoding is the process of translating a raw string of bytes 
        into is character string form, according to its encoding name.
        '''
        #
        return b.decode( encoding = sEncoding )


else: # PYTHON2
    #
    def getBytes( s, encoding = sDefaultEncoding ): return s


    def getStrGotBytes( u, encoding = sDefaultEncoding ):
        #
        # sReturn = str( getDecoded( u, sEncoding = encoding ) )
        #
        return u


    def getEncoded( s, sEncoding = 'utf-8' ):
        #
        '''
        Encoding is the process of translating a string of characters 
        into its raw bytes form, according to a desired encoding name.
        '''
        #
        if isinstance( s, str ):
            uReturn = unicode( s, sEncoding )
        else:
            uReturn = s
        #
        return uReturn


    def getDecoded( b, sEncoding = 'utf-8' ):
        #
        '''
        Decoding is the process of translating a raw string of bytes 
        into is character string form, according to its encoding name.
        '''
        #
        try:
            sReturn = b.decode( sEncoding )
        except UnicodeEncodeError:
            sReturn = b.encode( sEncoding ).decode( sEncoding )
        #
        return sReturn

    '''
    Encoding is the process of translating a string of characters
    into its raw bytes form, according to a desired encoding name.

    Decoding is the process of translating a raw string of bytes
    into is character string form, according to its encoding name.
    '''


# http://python-future.org/compatible_idioms.html
# urllib module
# urllib is the hardest module to use from Python 2/3 compatible code.

# Python 2 and 3: alternative 4 (modified)
if PYTHON3:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
else:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError

try:
    from collections import OrderedDict
except ImportError:
    try: # moving this to the top breaks this package!
        from ..Dict.Get import OrderedDictBackport as OrderedDict
    except ( ValueError, ImportError ): # maybe circular import issue
        from Dict.Get   import OrderedDictBackport as OrderedDict


if __name__ == "__main__":
    #
    from io             import StringIO
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if getZeroFilled( '1', 3 ) != '001':
        #
        lProblems.append( 'getZeroFilled()' )
        #
    #
    o = iter( range(5) )
    #
    uBytes = getBytes( 'spam' )
    #
    if PYTHON3 and type( uBytes ) != type( b'spam' ):
        #
        lProblems.append( 'getBytes() python3' )
        #
        print3( 'type( uBytes  ):', type( uBytes ) )
        print3( "type( b'spam' ):", type( b'spam') )
        #
    if PYTHON2 and type( uBytes ) != type( 'spam' ):
        #
        lProblems.append( 'getBytes() python2' )
        #
    #
    b = b'spam'
    #
    if type( getStrGotBytes( b ) ) != type( 'spam' ):
        #
        lProblems.append( 'getStrGotBytes() fed bytes' )
        #
    #
    sOrig = 'Göttingen'
    #
    sNew = getStrGotBytes(
            getBytes( sOrig, encoding = 'utf-8' ), encoding = 'utf-8' )
    #
    if sNew != sOrig:
        #
        lProblems.append( 'getStrGotBytes() fed getBytes() utf-8' )
        #
    #
    sNew = getStrGotBytes(
            getBytes( sOrig, encoding = 'latin-1' ), encoding = 'latin-1' )
    #
    if sNew != sOrig:
        #
        lProblems.append( 'getStrGotBytes() fed getBytes() latin-1' )
        #
    #
    bOrig = b'G\xc3\xb6ttingen'
    #
    bNew = getBytes(
            getStrGotBytes( bOrig, encoding = 'utf-8' ), encoding = 'utf-8' )
    #
    if bNew != bOrig:
        #
        lProblems.append( '() getBytes fed getStrGotBytes() utf-8' )
        #
    #
    uOrig = getStrGotBytes( getEncoded( sOrig ) )
    #
    uNew  = getDecoded( bOrig )
    #
    # getEncoded( 
    #
    if uNew != uOrig:
        #
        lProblems.append( 'getEncoded() fed getDecoded() utf-8' )
        #
        print3( 'uOrig:', uOrig )
        print3( 'uNew: ', uNew  )
    #
    if PYTHON2:
        uText = u'ꀀ' + u'abcd' + u'\u07b4'
    else:
        uText = chr(40960) + 'abcd' + chr(1972)
    #
    getEncoded( uText )
    #
    result = StringIO()
    print3_n_2( 'abc', file = result )
    #
    if result.getvalue() != 'abc\n':
        #
        lProblems.append( 'print3_n_2() StringIO instance as file param' )
        #
    #
    result = StringIO()
    print3_n_2( 'abc', beg = 3, file = result )
    #
    if result.getvalue() != '   abc\n':
        #
        lProblems.append( 'print3_n_2() StringIO instance as file param' )
        #
    #
    sayTestResult( lProblems )
