#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# string functions Paragraph
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
# http://www.gnu.org/licenses/gpl.html
#
# Copyright 2004-2015 Rick Graves
#

from String.Find import getFinder

_oMultiLinesFinder = getFinder( '\n\n\n+',
        bCaseSensitive = True, bMultiLine = True )


def getTextMakeParagraphs( sText = '', *sFileSpec, **kwargs ):
    # sFile = join( sTempDir, 'temp.txt' )
    #
    from File.Get         import getFileContent
    from File.Spec        import getFullSpecDefaultOrPassed
    from Iter.AllVers     import iMap
    from String.Eat       import eatWhiteSpaceFront
    from String.Transform import getSpace4NewLine
    #
    sFile = getFullSpecDefaultOrPassed( *sFileSpec, **kwargs )
    #
    if not sText: sText = getFileContent( sFile )
    #
    sText = sText.replace( '\r', '\n' )
    #
    sText = _oMultiLinesFinder.sub( '\n\n', sText )
    #
    lText = sText.split( '\n\n' )
    #
    def getSpaceEatFrontWhite( s ):
        return eatWhiteSpaceFront( getSpace4NewLine( s ) )
    #
    lText = iMap( getSpaceEatFrontWhite, lText )
    #
    sText = '\n\n'.join( lText )
    #
    return sText.replace( '  ', ' ' )





def _getRamdomText( iWantWords = 250, *sFileSpec, **kwargs ):
    # sDict = '/etc/dictionaries-common/words' ):
    #
    from random         import randint
    #
    from Iter.AllVers   import tFilter, iRange
    from File.Get       import getContent
    from File.Spec      import getFullSpecDefaultOrPassed
    from Test           import is1stCharAlpha
    from Collect.Test   import AllMeet
    #
    if 'sDefault' not in kwargs: kwargs['sDefault'] = '/etc/dictionaries-common/words'
    #
    sDict = getFullSpecDefaultOrPassed( *sFileSpec, **kwargs )
    #
    def isAlphaOnly( s ):
        #
        def isAlpha( s ): return s.isalpha()
        #
        if "'" in s:
            #
            lParts = s.split( "'" )
            #
            return AllMeet( lParts, isAlpha )
        else:
            #
            return isAlpha( s )
        #
    #
    def isWantedWord( s ): return is1stCharAlpha( s ) and isAlphaOnly( s )
    #
    tWords = tFilter( isWantedWord, getContent( sDict ).split() )
    #
    iWords = len( tWords )
    #
    def RandWord():
        #
        return tWords[ randint( 0, iWords ) ]
    #
    def RandSentence():
        #
        sSent = ' '.join( [ RandWord() for i in iRange( randint( 4, 15 ) ) ] ) + '. '
        #
        if sSent.endswith( "'s. " ):
            #
            sSent = sSent[ : -5 ] +  '. '
            #
        return sSent.capitalize()
    #
    def RandParagraph():
        #
        return ''.join( [ RandSentence() for i in iRange( randint( 1, 10 ) ) ] ) + '\n\n'
    #
    sOut    = ''
    #
    while len( sOut.split() ) < iWantWords:
        #
        sOut += RandParagraph()
    #
    return sOut


def _getShortLines( sOrig ):
    #
    # from Iter.AllVers   import iMap
    from String.Get import getCharsOffEnd
    #
    lWords = sOrig.split( ' ' )
    #
    lLines = [ '' ]
    #
    for sWord in lWords:
        #
        if sWord.startswith( '\n\n' ):
            #
            lLines[ -1 ] += '\n'
            #
            lLines.append( sWord[ 2 : ] + ' ' )
            #
            continue
        #
        sWord += ' '
        #
        if len( sWord ) + len( lLines[ -1 ] ) <= 51:
            #
            lLines[ -1 ] += sWord
            #
        else:
            #
            lLines.append( sWord )
            #
        #
    #
    def StripSpaces( s ):
        #
        sEnd = getCharsOffEnd( s, ' ' )
        #
        if sEnd:
            #
            return s[ : - len( sEnd ) ]
        else:
            return s
    #
    # lWords = iMap( StripSpaces, lLines )
    #
    sShortLines = '\n'.join( lLines )
    #
    return sShortLines







if __name__ == "__main__":
    #
    from File.Write     import MakeTemp
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    sOrig   = _getRamdomText()
    #
    sFixed  = getTextMakeParagraphs( _getShortLines( sOrig ) )
    #
    if sFixed.rstrip() != sOrig.rstrip():
        #
        MakeTemp( sOrig + '\n\n\n\n' + sFixed )
        #
        lProblems.append( 'getTextMakeParagraphs()' )
        #
    #
    sayTestResult( lProblems )