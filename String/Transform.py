#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# string functions Transform
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
# Copyright 2004-2012 Rick Graves
#


def getTranslatorStr( sOld, sNew = None ):
    #
    from Utils.Both2n3 import maketrans
    #
    if sNew is None: sNew = ''.ljust( len( sOld ) )
    #
    return maketrans( sOld, sNew )




def TranslatorFactory( sOld, sNew = None ):
    #
    from Utils.Both2n3 import translate
    #
    sTranslatorStr  = getTranslatorStr( sOld, sNew )
    #
    def getTranslated( sOrig ):
        #
        return translate( sOrig, sTranslatorStr )
        #
    #
    return getTranslated




def getRemoveMulitNewLinesFinder( iWantLines = 1 ):
    #
    from Find import getFinder
    #
    iFindHowMany = iWantLines + 1
    #
    oMultiNewLineFinder = getFinder(
                            '\n{%s,}' % iFindHowMany,
                            bCaseSensitive = True,
                            bMultiLine = True )
    #
    return oMultiNewLineFinder


def getRemoveMulitNewLines( sString, oMultiNewLineFinder, iWantLines = 1 ):
    #
    sWantLines = '\n' * iWantLines
    #
    return oMultiNewLineFinder.sub( sWantLines, sString )




def SubstChars( sOrig, sOld = '', sNew = '' ):
    #
    """
    Perform two or more single-character substitutions in one pass FAST.
    example: sModified = SubstChars( sOrig, "ABCDE", "!@#$%" )
    This would substitute ! for A, @ for B, # for C, etc.
    This performs CASE-SENSITIVE substitutions.
    """
    #
    from Utils.Both2n3 import translate
    #
    sTransStr   = getTranslatorStr( sOld, sNew )
    #
    return translate( sOrig, sTransStr )




def getSpacesForChars( sOrig, sDumpThese = '' ):
    #
    return SubstChars( sOrig, sDumpThese, ''.ljust( len( sDumpThese ) ) )


def _stripEscapes( s ):
    #
    lParts = s.split( '\\' )
    #
    if len( lParts ) > 1:
        #
        if lParts[0]:   s = lParts[0]
        else:           s = lParts[1][1:]
        #
    #
    return s


def getSwapper( dReplace,
                bIgnoreCase = False, bEscape = True, bMultiLine = False ):
    #
    from re import compile as REcompile
    from re import escape, IGNORECASE, MULTILINE
    #
    from Iter.AllVers   import iMap, iZip
    from Dict.Get       import getKeyIter, getItemIter, getValueIter
    #
    dReplace        = dict( dReplace )
    #
    oFlags = 0
    #
    if bIgnoreCase:
        #
        oFlags = IGNORECASE
        #
    if bMultiLine:
        #
        oFlags = oFlags | MULTILINE
        #
    if bEscape:
        #
        dNewReplace = dReplace
        #
    else:
        #
        dNewReplace = dict( iZip( iMap( _stripEscapes, dReplace ),
                                  getValueIter( dReplace ) ) )
        #
    #
    if bIgnoreCase:
        #
        dNewReplace = dict( [ ( sKey.lower(), sValue )
                              for sKey, sValue
                              in getItemIter( dNewReplace ) ] )
        #
        if bEscape:
            rX = REcompile( '|'.join( iMap( escape, dReplace ) ), oFlags )
        else:
            rX = REcompile( '|'.join( getKeyIter( dReplace ) ), oFlags )
        #
        def getReplacement( sFound ): return dNewReplace[ sFound.lower() ]
        #
    else:
        #
        if bEscape:
            rX = REcompile( '|'.join( iMap( escape, dReplace ) ), oFlags )
        else:
            rX = REcompile( '|'.join( getKeyIter( dReplace ) ), oFlags )
        #
        def getReplacement( sFound ): return dNewReplace[ sFound ]
        #
    #
    def SwapOne( uMatch ): return getReplacement( uMatch.group(0) )
    #
    def Swapper( sText ):  return rX.sub( SwapOne, sText )
    #
    return Swapper



def RemoveMany( sText, lReplace ):
    #
    from String.Replace import ReplaceManyOldWithBlanks
    #
    return ReplaceManyOldWithBlanks( sText, lReplace, bJustRemove = True )




def StripString( sText ): return sText.strip()



def StripLines( sText ):
    #
    from Iter.AllVers import iMap
    #
    lLines          = sText.split( '\n' )
    #
    lLines          = iMap( StripString, lLines )
    #
    sText           = '\n'.join( lLines )
    #
    return sText



def getSpace4NewLine( s ): return s.replace( '\n', ' ' )



def _getWhiteReArranged( sLine ):
    #
    sBase = ''
    #
    if '\n' in sLine or '\r' in sLine:
        #
        sBase = '\n'
    #
    return sBase.rjust( len( sLine ) )

def _getWhiteCompressed( sLine ):
    #
    if '\n' in sLine or '\r' in sLine:
        #
        sLine   = '\n'
    #
    return sLine



def _getStringWantLen( lParts, iLen ):
    #
    return ''.join( lParts ).ljust( iLen )

def _getStringWantShort( lParts, iLen  ):
    #
    return ''.join( lParts )


def _getCompressed( s ): return ''

def _getAddNewLine( s ):
    if len( s ) > 0:
        return '\n'.ljust( len( s ) )
    return ''


def getLinesTrimmed( sText, bKeepLen = False ):
    #
    """
    blank lines get obliterated
    """
    #
    from String.Eat import eatEndSpaces
    #
    # from time import clock
    #
    # tBefore = clock()
    #
    if bKeepLen:
        #
        #                 _getWhiteReArranged()
        getWhite        = _getWhiteReArranged
        #
        #                 _getStringWantLen()
        getString       = _getStringWantLen
        #
        #                 _getAddNewLine()
        getFirstBlank   = _getAddNewLine
        #
    else: # do not care about keeping character positions
        #
        #                 _getWhiteCompressed()
        getWhite        = _getWhiteCompressed
        #
        #                 _getStringWantShort()
        getString       = _getStringWantShort
        #
        #                 _getCompressed()
        getFirstBlank   = _getCompressed
        #
    #
    lNonWhite           = sText.split()
    #
    lReconstitute       = [ '' ] * ( 1 + ( 2 * len( lNonWhite ) ) )
    #
    iToHere = iNext     = 0
    #
    for i, sThis in enumerate( lNonWhite ):
        #
        iThisLen        = len( sThis )
        #
        iTextAt         = sText.find( sThis, iToHere )
        #
        lReconstitute[ 2 * i ] = \
            getWhite( sText[ iToHere : iTextAt ] )
        #
        lReconstitute[ 2 * i + 1 ] = sThis
        #
        iToHere         = iTextAt + iThisLen
        #
    #
    lReconstitute[  0 ] = getFirstBlank( lReconstitute[ 0 ] )
    #
    # tBefore = SayClock( tBefore, 'getGlobalReplaceWithSwapper' )
    #
    lReconstitute[ -1 ] = '\n' # put return on end
    #
    return getString( lReconstitute, len( sText ) )



if __name__ == "__main__":
    #
    from string import digits, whitespace, punctuation
    from string import ascii_letters   as letters
    from string import ascii_lowercase as lower
    from string import ascii_uppercase as upper
    #
    #
    from Iter.AllVers   import iZip
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    sTest   = letters + lower + upper + digits + whitespace + punctuation
    #
    sLinesXtras = ( letters + '\n\n' +
                    lower + '\n\n\n' +
                    upper + '\n\n\n\n' +
                    digits + '\n\n\n\n\n' +
                    whitespace + '\n\n\n\n\n\n\n\n' +
                    punctuation )
    #
    sLinesPlain = ( letters + '\n' +
                    lower + '\n' +
                    upper + '\n' +
                    digits + '\n' +
                    whitespace + '\n' +
                    punctuation )
    #
    sLinesLessW = ( letters + '\n' +
                    lower + '\n' +
                    upper + '\n' +
                    digits + '\n' +
                    punctuation )
    #
    sSameLength = ( letters + ' \n' +
                    lower + '  \n' +
                    upper + '   \n' +
                    digits + '                  \n' +
                    punctuation )
    #
    # getTranslatorStr() puts up a facade for maketrans, so is not tested here
    #
    BlankUpper      = TranslatorFactory( upper )
    #
    sBlanks         = ''.ljust(26)
    #
    if BlankUpper( sTest ) != \
            ( 2 * ( lower + sBlanks ) ) + digits + whitespace + punctuation:
        #
        lProblems.append( 'TranslatorFactory()' )
        #
    #
    oMultiNewLineFinder = getRemoveMulitNewLinesFinder()
    #
    if getRemoveMulitNewLines(
            sLinesXtras, oMultiNewLineFinder ) != sLinesPlain:
        #
        lProblems.append( 'getRemoveMulitNewLines()' )
        #
    #
    if SubstChars( upper, sOld = 'EDCBA', sNew = '!@#$%' ) != '%$#@!' + upper[ 5 : ]:
        #
        lProblems.append( 'SubstChars()' )
        #
    #
    if getSpacesForChars( sTest, '9876543210' ) != \
            letters + lower + upper + ''.ljust(10) + whitespace + punctuation:
        #
        lProblems.append( 'getSpacesForChars()' )
        #
    #
    lUpper  = list( upper )
    lUpper.reverse()
    #
    lLower  = list( lower )
    lLower.reverse()
    #
    lNumbs  = list( digits * 3 )[ : 26 ]
    lNumbs.reverse()
    #
    oSwapLower4Upper = getSwapper( iZip( lUpper, lLower ), bIgnoreCase = False )
    oSwapNumbs4Alpha = getSwapper( iZip( lUpper, lNumbs ), bIgnoreCase = True )
    #
    sResult          = ( digits * 11 )[ : 26 ]
    sResult          *= 4
    sResult          += digits + whitespace + punctuation
    #
    if oSwapLower4Upper( sTest ) != \
            lower + lower + lower + lower + digits + whitespace + punctuation:
        #
        lProblems.append( 'getSwapper() concatenated comparison' )
        #
    #
    if oSwapNumbs4Alpha( sTest ) != sResult:
        #
        lProblems.append( 'getSwapper() sResult comparison' )
        #
    #
    sStuff = 'city, state and zip and statements'
    tSubs = (
        (   '\\band\\b',
            'y' ),
        (   'street address',
            'direccion' ),
        (   'city',
            'ciudad' ),
        (   '\\bstate\\b',
            'estado' ),
        (   'zip',
            'codigo postal' ) )
    #
    oHTMLnttSwapper      = getSwapper( tSubs, bEscape = False )
    #
    if oHTMLnttSwapper( sStuff ) != 'ciudad, estado y codigo postal y statements':
        #
        lProblems.append( 'getSwapper() remove escapes' )
        #
    #
    if RemoveMany( sTest, ( digits, upper, lower ) ) != whitespace + punctuation:
        #
        lProblems.append( 'RemoveMany()' )
        #
    #
    if StripString( 'abc' + whitespace ) != 'abc':
        #
        lProblems.append( 'StripString()' )
        #
    #
    if StripLines( sSameLength ) != '\n'.join( ( letters, lower, upper, digits, punctuation ) ):
        #
        lProblems.append( 'StripLines()' )
        #
    #
    if getSpace4NewLine( sLinesLessW ) != ' '.join( ( letters, lower, upper, digits, punctuation ) ):
        #
        lProblems.append( 'getSpace4NewLine()' )
        #
    #
    sTest = ''' \nMary had a little lamb.
                  Today we have spam, toast and eggs.
                  How now brown cow.

             '''
    #
    sSameLen = getLinesTrimmed( sTest, bKeepLen = True )
    sShorter = getLinesTrimmed( sTest               )
    #
    sTrimmed = 'Mary had a little lamb.\n' \
               'Today we have spam, toast and eggs.\nHow now brown cow.\n'
    #
    if      len( sTest ) != len( sSameLen ) or \
            sSameLen.find( 'Mary had a little lamb.' ) != \
               sTest.find( 'Mary had a little lamb.' ) or \
            sSameLen.find( 'How now brown cow.'      ) != \
               sTest.find( 'How now brown cow.'      ) or \
            sShorter != sTrimmed:
        #
        lProblems.append( 'getLinesTrimmed()' )
        #
    #
    #
    sayTestResult( lProblems )