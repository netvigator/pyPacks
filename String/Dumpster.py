#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# string functions Dumpster
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
# Copyright 2004-2014 Rick Graves
#

from string import punctuation, whitespace, ascii_letters as letters

class DumpsterClass( object ):
    #
    """
    Text dumpster to assist text processing.
    """
    #
    def __init__( self, sKeepThese = '', sDumpThese = '' ):
        #
        from Utils.Both2n3  import maketrans
        from Collect.Test   import getHasNotTester
        from Iter.AllVers   import iFilter, iMap, iRange
        #
        if sKeepThese:
            #
            sKeepThese = sKeepThese.replace( ' ', '' ) # do not need space
            #
            lCharsAll   = iMap( chr, iRange( 0, 256 ) )# python leaves 256 off, which is what we want
            #
            # take out the ones to keep
            #
            isDumpThis  = getHasNotTester( list( sKeepThese ) )
            #
            iterDumpThese  = iFilter( isDumpThis, lCharsAll )
            #
            sDumpThese  = ''.join( iterDumpThese )
            #
        else:
            #
            sDumpThese = sDumpThese.replace( ' ', '' ) # do not need space
            #
        #
        self.sTransStr = maketrans( sDumpThese, ''.ljust( len( sDumpThese ) ) )


    def Dump( self, sText ):
        #
        from Utils.Both2n3 import translate
        #
        return translate( sText, self.sTransStr )



class KeepDotsDigitsClass( DumpsterClass ):
    #
    """
    Text dumpster to assist getting Dot Addresses from text.
    """
    #
    def __init__( self ):
        #
        DumpsterClass.__init__( self, '01234567890.' )





class KeepYouNameItClass( DumpsterClass ):
    #
    """
    User defined text dumpster.
    """
    #
    def __init__( self, sKeepChars = '' ):
        #
        DumpsterClass.__init__( self, sKeepChars, '' )


class DumpYouNameItClass( DumpsterClass ):
    #
    """
    User defined text dumpster.
    """
    #
    def __init__( self, sDumpChars = '' ):
        #
        DumpsterClass.__init__( self, '', sDumpChars )



def getWhiteWiped( s ):
    #
    lParts = s.split()
    #
    return ''.join( lParts )

getWhiteDumped = getWhiteWiped


oKeepDigitsOnly = KeepYouNameItClass( '0123456789' )


def getDigitsOnly( s ):
    #
    '''Note this function also wipes white space
    (Dump and Keep classes replace with spaces one for one).'''
    #
    if type( s ) == bytes:
        #
        s = s.decode( 'utf-8' )
        #
    #
    sDigitsSpaces = oKeepDigitsOnly.Dump( s )
    #
    return getWhiteWiped( sDigitsSpaces )


oKeepAlphaOnly = KeepYouNameItClass( letters )

oKeepAlphaSpaces = KeepYouNameItClass( letters + ' ' )

oKeepAlphaDigitsSpacesHash = KeepYouNameItClass( letters + ' 01234567890#' )

oKeepPunctuation = KeepYouNameItClass( punctuation )


def getPunctuation( s ):
    #
    return getWhiteWiped( oKeepPunctuation.Dump( s ) )


def getAlphaOnly( s ):
    #
    '''Note this function also wipes white space
    (Dump and Keep classes replace with spaces one for one).'''
    #
    sAlphaSpaces = oKeepAlphaOnly.Dump( s )
    #
    return getWhiteWiped( sAlphaSpaces )


_oKeepAlphaDigitsOnly = KeepYouNameItClass( letters + '0123456789' )

def getAlphaNumClean( s ):
    #
    from String.Split import getWhiteCleaned
    #
    sAlphaNumSpaces = _oKeepAlphaDigitsOnly.Dump( s )
    #
    return getWhiteCleaned( sAlphaNumSpaces )




def getChoppedOff( sHaystack, sNeedle ):
    #
    '''
    chops off the last occurance of a character and everything after
    '''
    iLoc = sHaystack.rfind( sNeedle )
    #
    if iLoc > -1:
        #
        sHaystack = sHaystack[ : iLoc ]
        #
    #
    return sHaystack



if __name__ == "__main__":
    #
    from string import digits
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    oKeepDotsDigits = KeepDotsDigitsClass()
    #
    if oKeepDotsDigits.Dump( 'abcde.012345' ) != '     .012345':
        #
        lProblems.append( 'KeepDotsDigitsClass()' )
        #
    #
    if getDigitsOnly( 'ABCabc.-+0123\n:;<>|!@#$%^&*' ) != '0123':
        #
        lProblems.append( 'getDigitsOnly()' )
        #
    #
    oDumpAlpha = DumpYouNameItClass( letters )
    #
    if      oDumpAlpha.Dump( 'abc' ) != '   ' or \
            oDumpAlpha.Dump( 'a1b2c3d4e5' ) != ' 1 2 3 4 5':
        #
        lProblems.append( 'DumpYouNameItClass()' )
        #
    #
    oKeepAlpha = KeepYouNameItClass( letters )
    #
    if oKeepAlpha.Dump( 'a1b2c3d4e5' ) != 'a b c d e ':
        #
        lProblems.append( 'KeepYouNameItClass()' )
        #
    #
    if getWhiteWiped( ' a b c \n' ) != 'abc':
        #
        lProblems.append( 'getWhiteWiped()' )
        #
    #
    sGotWhite = '''
    a         b
    c         d
    e         f
    '''
    #
    if getWhiteWiped( sGotWhite ) != 'abcdef':
        #
        lProblems.append( 'getWhiteWiped()' )
        #
    #
    if getAlphaOnly( '1a2b3c4d5e' ) != 'abcde':
        #
        lProblems.append( 'getAlphaOnly()' )
        #
    #
    if getAlphaNumClean( 'P.O. Box' ) != 'P O Box':
        #
        lProblems.append( 'getAlphaNumClean()' )
        #
    #
    if getChoppedOff( digits * 2, '6' ) != digits + '012345':
        #
        lProblems.append( 'getChoppedOff()' )
        #
    #
    if getPunctuation( 'P.O. Box' ) != '..':
        #
        lProblems.append( 'getPunctuation()' )
        #
    #
    #
    #
    sayTestResult( lProblems )