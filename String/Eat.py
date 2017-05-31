#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# string functions Eat
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
# Copyright 2004-2016 Rick Graves
#
from String.Test    import isAsciiAlpha, isAsciiDigit


def _eatOffOneEnd( sText, sEatThese = '',
        fEatThese = None, bEatOffFront = True, bEatOffBoth = False ):
    #
    """
    This is the generic program,
    it is normally only called by specific implementations below.
    """
    #
    from String.Get import getTheseCharsOffOneEnd
    #
    iEat = len(
        getTheseCharsOffOneEnd( sText, sEatThese, fEatThese, bEatOffFront ) )
    #
    if bEatOffFront or bEatOffBoth:
        #
        sText   = sText[ iEat : ]
        #
        if bEatOffBoth:
            #
            iEat = len(
                getTheseCharsOffOneEnd( sText, sEatThese, fEatThese, False ) )
            #
        #
    if bEatOffBoth or not bEatOffFront:
        #
        if iEat: sText = sText[ : - iEat ]
        #
    #
    return sText


def eatCharsOffBeg( sText, sEatThese = '', fEatThese = None ):
    #
    return _eatOffOneEnd( sText, sEatThese, fEatThese, bEatOffFront = True )


def eatCharsOffEnd( sText, sEatThese = '', fEatThese = None ):
    #
    return _eatOffOneEnd( sText, sEatThese, fEatThese, bEatOffFront = False )


def eatCharsOffBothEnds( sText, sEatThese = '', fEatThese = None ):
    #
    return _eatOffOneEnd( sText, sEatThese,
        fEatThese, bEatOffFront = False, bEatOffBoth = True )


def eatPunctuationBegAndEnd( sFrag ):
    #
    from String.Test  import isPunctuation
    #
    return eatCharsOffEnd(
                eatCharsOffBeg( sFrag, fEatThese = isPunctuation ), fEatThese = isPunctuation )



def eatPunctuationEnd( sFrag ):
    #
    from String.Test  import isPunctuation
    #
    return eatCharsOffEnd( sFrag, fEatThese = isPunctuation )



def eatPunctAndSpacesOffEnd( sFrag ):
    #
    from String.Test  import isPunctOrSpace
    #
    return eatCharsOffEnd( sFrag, fEatThese = isPunctOrSpace )


def eatPunctAndSpacesOffBegAndEnd( sFrag ):
    #
    from String.Test  import isPunctOrSpace
    #
    return eatCharsOffEnd(
                eatCharsOffBeg( sFrag, fEatThese = isPunctOrSpace ), fEatThese = isPunctOrSpace )


def eatFrontNonAlpha( sText ):
    #
    def fEatThese( sChar ): return not isAsciiAlpha( sChar )
    #
    return _eatOffOneEnd( sText, fEatThese = fEatThese )


def eatFrontNonDigits( sText ):
    #
    from String.Test import isNotDigit
    #
    return _eatOffOneEnd( sText, fEatThese = isNotDigit )


def eatBackNonDigits( sText ):
    #
    from String.Test import isNotDigit
    #
    return _eatOffOneEnd( sText, fEatThese = isNotDigit, bEatOffFront = False )


def eatFrontNonAlphaNum( sText ):
    #
    def fEatThese( sChar ): return not (
        isAsciiAlpha( sChar ) or
        isAsciiDigit( sChar ) )
    #
    return _eatOffOneEnd( sText, fEatThese = fEatThese )



def eatFrontNonAlphaNumButKeepLF( sText ):
    #
    def fEatThese( sChar ): return not (
        isAsciiAlpha( sChar ) or
        isAsciiDigit( sChar ) or
        sChar == '\n' )
    #
    return _eatOffOneEnd( sText, fEatThese = fEatThese )



def eatEndNonAlphaNum( sText ):
    #
    #def fEatThese( sChar ): return not ( sChar.isalpha() or sChar.isdigit() )
    def fEatThese( sChar ):
        return not (
            isAsciiAlpha( sChar ) or
            isAsciiDigit( sChar ) )
    #
    return _eatOffOneEnd( sText, fEatThese = fEatThese, bEatOffFront = False )



def eatNonAlphaNumBothEnds( sText ):
    #
    return eatEndNonAlphaNum( eatFrontNonAlphaNum( sText ) )


def eatNonAlphaBothEnds( sText ):
    #
    return eatEndNonAlpha( eatFrontNonAlpha( sText ) )


def eatAlphaOffEnd( sText ):
    #
    return eatCharsOffEnd( sText, fEatThese = isAsciiAlpha )
    


setCRLF = frozenset( ( '\n', '\r' ) )

def _gotCRLF( sChar ): return sChar in setCRLF


def eatEndCRLF( sText ):
    #
    return _eatOffOneEnd( sText, fEatThese = _gotCRLF, bEatOffFront = False )


def eatBegCRLF( sText ):
    #
    return _eatOffOneEnd( sText, fEatThese = _gotCRLF )



def eatEndAlpha( sText ):
    #
    def fEatThese( sChar ): return sChar.isalpha()
    #
    return _eatOffOneEnd( sText, fEatThese = fEatThese, bEatOffFront = False )



def eatEndNonAlpha( sText ):
    #
    def fEatThese( sChar ): return not isAsciiAlpha( sChar )
    #
    return _eatOffOneEnd( sText, fEatThese = fEatThese, bEatOffFront = False )


def eatFrontDigits( sText ):
    #
    from String.Test  import isDigit
    #
    return _eatOffOneEnd( sText, fEatThese = isDigit )


def eatEndDigits( sText ):
    #
    from String.Test  import isDigit
    #
    return _eatOffOneEnd( sText, fEatThese = isDigit, bEatOffFront = False )


def eatWhiteSpaceBothEnds( sText ):
    #
    from string import whitespace
    #
    return _eatOffOneEnd(
            _eatOffOneEnd( sText, whitespace ),
                            whitespace, bEatOffFront = False )


def eatWhiteSpaceFront( sText ):
    #
    from string import whitespace
    #
    return _eatOffOneEnd( sText, whitespace )


def eatEndSpaces( sText ):
    #
    from String.Test  import isSpace
    #
    return _eatOffOneEnd( sText, fEatThese = isSpace, bEatOffFront = False )





def _getFrontCharOff( s, sDigit ):
    #
    while s.startswith( sDigit ):
        #
        s = s[ 1 : ]
        #
    #
    return s


def eatFrontZeros( s ):
    #
    return _getFrontCharOff( s, '0' )


def eatFrontOnes( s ):
    #
    return _getFrontCharOff( s, '1' )



_setZeroOne = frozenset( ( '0', '1' ) )


def eatFrontZerosOnes( s ):
    #
    while s and s[0] in _setZeroOne:
        #
        s = s[ 1 : ]
        #
    #
    return s


def eatFrontOneByOne( sOrig, sEat ):
    #
    from String.Get import getTextAfter
    #
    sRest = sOrig
    #
    for c in sEat:
        #
        sRest = getTextAfter( sRest, c )
        #
    #
    return sRest


if __name__ == "__main__":
    #
    from string import digits, whitespace
    from string import ascii_lowercase as lowercase
    from string import ascii_uppercase as uppercase
    #
    from six            import print_ as print3
    #
    from Iter.AllVers   import iZip, iMap, tMap
    from String.Get     import getStringInRange
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    def fEatThese( s ): return not s.isalpha()
    #
    sLeft = _eatOffOneEnd( lowercase + digits,
                            fEatThese = fEatThese, bEatOffFront = False )
    #
    if sLeft != lowercase:
        #
        print3( 'sLeft:', sLeft )
        lProblems.append( '_eatOffOneEnd()' )
        #
    #
    if eatCharsOffBeg( lowercase, 'lkjihgfedcba' ) != 'mnopqrstuvwxyz':
        #
        lProblems.append( 'eatTheseCharsOffBeg()' )
        #
    if eatCharsOffEnd( lowercase, 'zyxwvutsrqponm' ) != 'abcdefghijkl':
        #
        lProblems.append( 'eatTheseCharsOffEnd()' )
        #
    #
    if eatCharsOffBothEnds( '/abc/', '/' ) != 'abc':
        #
        # print3( eatCharsOffBothEnds( '/abc/', '/' ) )
        lProblems.append( 'eatCharsOffBothEnds() remove' )
        #
    #
    if eatCharsOffBothEnds( 'abc', '/' ) != 'abc':
        #
        lProblems.append( 'eatCharsOffBothEnds() nothing to remove' )
        #
    #
    #
    if eatPunctuationBegAndEnd( ',-./0123456789:;' ) != '0123456789':
        #
        lProblems.append( 'RemovePunctuationBegAndEnd()' )
        #
    #
    # getStringInRange( 32, 91 ) =
    # ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    #
    if eatPunctuationEnd( ',-./0123456789:;' ) != ',-./0123456789':
        #
        lProblems.append( 'eatPunctuationEnd()' )
        #
    #
    
    if eatPunctAndSpacesOffEnd( ',-./0123456789: ; ' ) != ',-./0123456789':
        #
        lProblems.append( 'eatPunctAndSpacesOffEnd()' )
        #
    #
    if eatPunctAndSpacesOffBegAndEnd( ', -./0123456789: ; ' ) != '0123456789':
        #
        lProblems.append( 'eatPunctAndSpacesOffBegAndEnd()' )
        #
    #
    s32to90 = getStringInRange( 32, 91 )
    #
    if eatFrontNonAlpha( s32to90 ) != uppercase:
        #
        lProblems.append( 'eatFrontNonAlpha()' )
        #
    if eatFrontNonAlphaNum( s32to90 ) != '0123456789:;<=>?@' + uppercase:
        #
        lProblems.append( 'eatFrontNonAlphaNum()' )
        #
    if      eatFrontNonAlphaNumButKeepLF( '\n' + s32to90 ) != '\n' + s32to90 or \
            eatFrontNonAlphaNumButKeepLF( '\r' + s32to90 ) != '0123456789:;<=>?@' + uppercase:
        #
        lProblems.append( 'eatFrontNonAlphaNumButKeepLF()' )
        #
    #
    # getStringInRange( 48, 65 ) = '0123456789:;<=>?@'
    #
    if      eatEndNonAlphaNum( lowercase + whitespace ) != lowercase:
        #
        print3( eatEndNonAlphaNum( lowercase + whitespace ) )
        lProblems.append( 'eatEndNonAlphaNum( lowercase + whitespace )' )
        #
    #
    if eatEndNonAlphaNum( getStringInRange( 97, 256 ) ) != lowercase:
        #
        s = eatEndNonAlphaNum( getStringInRange( 97, 256 ) )
        #
        #
        print3( tMap( str, iMap( ord, ( s[0], s[-1] ) ) ) )
        lProblems.append( 'eatEndNonAlphaNum( getStringInRange( 97, 256 ) )' )
        #
    #
    if eatEndNonAlphaNum( getStringInRange( 48,  65 ) ) != digits:
        #
        print3( eatEndNonAlphaNum( getStringInRange( 48,  65 ) ) )
        lProblems.append( 'eatEndNonAlphaNum( getStringInRange( 48,  65 ) )' )
        #
    #
    # print3( 'getStringInRange( 65, 123 )', '= ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz' )
    # print3( 'getStringInRange( 32,  97 )', '''= !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`''' )
    #
    if      eatNonAlphaNumBothEnds( getStringInRange( 32, 256 ) ) != getStringInRange( 48, 123 ) or \
            eatNonAlphaNumBothEnds( getStringInRange( 32,  97 ) ) != getStringInRange( 48,  91 ):
        #
        #print3( eatNonAlphaNumBothEnds( getStringInRange( 32, 256 ) ) )
        #print3( eatNonAlphaNumBothEnds( getStringInRange( 32,  97 ) ) )
        lProblems.append( 'eatNonAlphaNumBothEnds()' )
        #
    if eatNonAlphaBothEnds( getStringInRange( 32,  97 ) ) != uppercase:
        #
        lProblems.append( 'eatNonAlphaBothEnds()' )
        #
    if eatAlphaOffEnd( '1234abcd' ) != '1234':
        #
        lProblems.append( 'eatAlphaOffEnd()' )
        #
    #
    if eatEndCRLF( '\r\n' + uppercase + '\r\n' ) != '\r\n' + uppercase:
        #
        lProblems.append( 'eatEndCRLF()' )
        #
    if eatBegCRLF( '\r\n' + uppercase + '\r\n' ) != uppercase + '\r\n':
        #
        lProblems.append( 'eatBegCRLF()' )
        #
    #
    # getStringInRange( 65, 123 ) = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz'
    #
    if eatEndAlpha( getStringInRange( 65, 123 ) ) != uppercase + '[\\]^_`':
        #
        lProblems.append( 'eatEndAlpha()' )
        #
    if eatEndNonAlpha( getStringInRange( 97, 256 ) ) != lowercase:
        #
        print3( eatEndNonAlpha( getStringInRange( 97, 256 ) ) )
        lProblems.append( 'eatEndNonAlpha()' )
        #
    #
    # getStringInRange( 48, 65 ) = '0123456789:;<=>?@'
    #
    if eatFrontDigits( getStringInRange( 48, 65 ) ) != ':;<=>?@':
        #
        lProblems.append( 'eatFrontDigits()' )
        #
    #
    # getStringInRange( 32,  58 ) = ' !"#$%&\'()*+,-./0123456789'
    #
    if eatEndDigits( getStringInRange( 32,  58 ) ) != ' !"#$%&\'()*+,-./':
        #
        lProblems.append( 'eatEndDigits()' )
        #
    #
    if eatWhiteSpaceBothEnds(
            whitespace + lowercase + whitespace ) != lowercase:
        #
        lProblems.append( 'eatWhiteSpaceBothEnds()' )
        #
    #
    if eatWhiteSpaceFront(
            whitespace + lowercase + whitespace ) != \
                         lowercase + whitespace:
        #
        lProblems.append( 'eatWhiteSpaceFront()' )
        #
    #
    if      eatEndSpaces( '\t\n\x0b\x0c\r ' ) != '\t\n\x0b\x0c\r' or \
            eatEndSpaces( 'abc'             ) != 'abc':
        #
        lProblems.append( 'eatEndSpaces()' )
        #
    #
    if eatFrontNonDigits( '-206-632-9929' ) != '206-632-9929':
        #
        lProblems.append( 'eatFrontNonDigits()' )
        #
    #
    if eatBackNonDigits( '123xzy' ) != '123':
        #
        lProblems.append( 'eatBackNonDigits()' )
        #
    #
    sOrig   = '1-2-3-4-5-6-7-8-9'
    sEat    = '123'
    #
    if eatFrontOneByOne( sOrig, sEat ) != '-4-5-6-7-8-9':
        #
        lProblems.append( 'eatFrontOneByOne()' )
        #
    #
    #
    #
    #
    sayTestResult( lProblems )