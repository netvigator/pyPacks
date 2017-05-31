#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# string functions Test
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

from string import digits, punctuation
from string import ascii_lowercase as lowercase
from string import ascii_uppercase as uppercase

from String.Transform   import TranslatorFactory

class Finished( Exception ): pass

setQuoteChars   = frozenset( '"\'' ) # '"' + "'"

setAsciiAlpha   = frozenset( lowercase + uppercase )
setAsciiDigit   = frozenset( digits )
setPunctuation  = frozenset( punctuation )
setPuncAndSpace = frozenset( punctuation + ' ' )
setNonAlphaNums = frozenset( '~!@#$%^&*()_+-=?/' )
setDigitsPuncSp = frozenset( digits + punctuation + ' ' )

def _getASCII_128():
    #
    from Iter.AllVers import iRange
    #
    l = []
    #
    for i in iRange( 128 ):
        #
        l.append( chr( i ) )
        #
    #
    return frozenset( l )

_setASCII_128 = _getASCII_128()


def isAsciiAlpha( c ):
    # xyz
    return c.isalpha() and c in setAsciiAlpha

def isAsciiDigit( c ):
    # xyz
    return c.isdigit() and c in setAsciiDigit


def hasAnyAlpha( sString ):
    #
    if isinstance( sString, tuple ) or isinstance( sString, list ):
        #
        sString = repr( sString )
        #
    #
    return sString.upper() != sString.lower()

def hasAlphaOnly(   sChar   ):  return sChar.isalpha()

def isNotDot(       sChar   ):  return sChar[ 0 ] != '.'

def hasDigitsOnly(  sChar   ):  return sChar.isdigit()


def isDigit(        sChar   ):  return sChar.isdigit()

def isNotDigit(     sChar   ):  return not sChar.isdigit()


def isDot(          sChar   ):  return sChar == '.'

def isDigitOrDot(   sChar   ):  return sChar.isdigit() or sChar == '.'

def isASCII_128(    sChar   ):  return sChar in _setASCII_128

def isDigitPunctOrSpace( sChar ): return sChar in setDigitsPuncSp


def hasAnyDigits( sString ):
    #
    from Collect.Query  import get1stThatMeets
    #
    return get1stThatMeets( sString, isDigit )


def hasNoDigits( sString ): return not hasAnyDigits( sString )


def hasDigitAndDot( sFrag ):
    #
    return  '.' in sFrag and hasAnyDigits( sFrag )


def _isNotDigitOrDot( s ):
    #
    return not isDigitOrDot( s )


def hasDigitsAndDotsOnly( sFrag ):
    #
    from Collect.Query  import get1stThatMeets
    #
    return get1stThatMeets( sFrag, _isNotDigitOrDot ) is None


def hasAscii_128_Only( sFrag ):
    #
    from Collect.Query  import get1stThatFails
    #
    return get1stThatFails( sFrag, isASCII_128 ) is None


def isPunctuation( sChar ):
    #
    return sChar in setPunctuation

def isPunctOrSpace( sChar ):
    #
    return sChar in setPuncAndSpace


def hasNoLower(   sText ): return sText and sText == sText.upper()

def hasNoUpper(   sText ): return sText and sText == sText.lower()

def hasAnyUpper(  sText ): return sText != sText.lower()

def hasAnyLower(  sText ): return sText != sText.upper()

def hasAllUpper(  sText ): return sText.isupper()

def hasAllLower(  sText ): return sText.islower()



def hasAnyPunct(  sText ):
    pass



def hasMixedCase( sText ):
    return sText != sText.lower() and sText != sText.upper()

def isPasswordNonAlphaNum( s ):
    #
    return s in setNonAlphaNums


def _hasAnyPasswordNonAlphaNums( sString ):
    #
    from Collect.Query  import get1stThatMeets
    #
    return get1stThatMeets( sString, isPasswordNonAlphaNum )


def isStrongPassword( sText ):
    #
    return (    hasMixedCase( sText ) and
                hasAnyDigits( sText ) and
                _hasAnyPasswordNonAlphaNums( sText ) )


def isStrongPasswordChar( s ):
    #
    return s.isalnum() or isPasswordNonAlphaNum( s )



def getItemFoundInString( sString, lItems ):
    #
    """
    pass a string and a list of (smaller) strings.
    return the first item in the list that is a substring of the string.
    return empty string if no item is ffound in the string.
    """
    #
    from Collect.Query  import get1stThatMeets
    #
    def isFoundInString( s ): return s in sString
    #
    sReturn = get1stThatMeets( lItems, isFoundInString )
    #
    if sReturn is None: sReturn = ''
    #
    return sReturn



def AnyItemFoundInString( sString, lItems ):
    #
    return bool( getItemFoundInString( sString, lItems ) )




def isQuote1stChar( sString ):
    #
    return len( sString ) > 1 and sString[  0 ] in setQuoteChars

def isQuoteLastChar( sString ):
    #
    return len( sString ) > 1 and sString[ -1 ] in setQuoteChars


def isStringQuoted( sString ):
    #
    return (    len( sString ) > 1 and
                sString[ 0 ] == sString[ -1 ] and
                sString[ 0 ] in setQuoteChars )




def EndsWithCharsIgnoreWhite( sText, sLookFor = '', bCaseSensitive = False ):
    #
    """
    strip the trailing white space before applying the endswith test.
    """
    bEndsWith           = False
    #
    if bCaseSensitive:
        #
        bEndsWith   = sText.rstrip().endswith( sLookFor )
        #
    elif not bCaseSensitive:
        #
        bEndsWith   = sText.rstrip().lower().endswith( sLookFor.lower() )
        #
    #
    return bEndsWith


def is1stCharAlpha(   sStr  ): return sStr[ 0 : 1 ].isalpha()

def hasAlphaNumsOnly( sChar ): return sChar.isalnum()

def isDigitOrDotOnly( sChar ): return sChar.isdigit() or sChar == '.'

def isAlphaNum(       sChar ): return sChar.isalnum()

def isAlphaNumOrDot(  sChar ): return sChar.isalnum() or sChar == '.'


def isInQuotesSingle( uValue ):
    #
    '''
    Strict! string must start and end with single quote chars.
    '''
    #
    return  isinstance( uValue, str ) and \
            uValue.startswith( "'" )  and \
            uValue.endswith( "'" )



def isInQuotesDouble( uValue ):
    #
    '''
    Strict! string must start and end with double quote chars.
    '''
    #
    return  isinstance( uValue, str ) and \
            uValue.startswith( '"' )  and \
            uValue.endswith( '"' )


def isInQuotesEither( uValue ):
    #
    '''
    Strict! string must start and end with quote chars.
    '''
    #
    return isInQuotesSingle( uValue ) or isInQuotesDouble( uValue )


def almostEndsWith( sText, sLookFor, iDropMax = 5 ):
    #
    """
    almostEndsWith( 'abcdefghijk', 'ghi' ) returns True
    """
    #
    from Iter.AllVers import iRange
    #
    bAlmostEndsWith         = False
    #
    for i in iRange( iDropMax ):
        #
        if sText[ : -1 * ( 1 + i ) ].endswith( sLookFor ):
            #
            bAlmostEndsWith = True
            #
            break
        #
    #
    return bAlmostEndsWith



def endsWithDigit( sText ):
    #
    return type( sText ) == str and len( sText ) > 0 and sText[ -1 ].isdigit()



def hasSubstring( sHayStack, sNeedle, bCaseSensitive = False ):
    #
    """
    Default search not case sensitive.
    Regards the built in "in" operator:
    In Python versions before 2.3, the needle had to be a string of length 1.
    In Python 2.3 and beyond, the needle may be a string of any length.
    """
    #
    bNoCase         = False
    bInvalidInput   = False
    #
    try:
        #
        if not bCaseSensitive:
            #
            sNeedleLower = sNeedle.lower()
            #
            bNoCase = sNeedle.upper() == sNeedleLower
            #
        #
    except Exception:
        #
        bInvalidInput = True
        #
    #
    # bCaseSensitive bNoCase
    #
    if bInvalidInput:
        #
        return False
        #
    elif bNoCase or bCaseSensitive:
        #
        return sNeedle in sHayStack
        #
    else:
        #
        return sNeedle.lower() in sHayStack.lower()




def isQuote( sChar ): return sChar in setQuoteChars


def isString   ( u ): return     isinstance( u, str )

def isNotString( u ): return not isinstance( u, str )


def isStringLike( u ):
    #
    bString = True
    #
    try:
        u += ''
    except:
        bString = False
    #
    return bString


def isNotStringLike( u ): return not isStringLike( u )


def isEmptyString(       s ): return s == ''

def isStringNotEmpty(    s ): return bool( s )

def isStringAndNotEmpty( s ): return bool( s ) and type( s ) == str


def getStartsWithSomethingTester( sStart ):
    #
    def ThisStartsWith( s ): return s.startswith( sStart )
    #
    return ThisStartsWith


def getEndsWithSomethingTester( sStart ):
    #
    # not used anywhere
    #
    def ThisEndsWith( s ): return s.endswith( sStart )
    #
    return ThisEndsWith


def getMemberInAnyOfTtester( uStart, iWhich = 0 ):
    #
    def MemberInAnyOf( sTest ):
        #
        bReturn = False
        #
        if sTest:
            #
            bReturn = sTest[ iWhich ] in uStart
        #
        return bReturn
        #
    #
    return MemberInAnyOf


def getStartsWithAnyOfTtester( uStart ):
    #
    '''returns tester to test whether string
    starts with any single character in uEnd --
    emphasis on single character
    '''
    #
    StartsWithAnyOf = getMemberInAnyOfTtester( uStart, 0 )
    #
    return StartsWithAnyOf


def getEndsWithAnyOfTtester( uEnd ):
    #
    '''returns tester to test whether string
    ends with any single character in uEnd --
    emphasis on single character
    '''
    #
    EndsWithAnyOf = getMemberInAnyOfTtester( uEnd, -1 )
    #
    return EndsWithAnyOf


def getHasSubstringTester( sSubstring, bCaseSensitive = False ):
    #
    """
    Returns a function that will test whether strings contain a fixed substring
    """
    #
    def isSubstringInThisString( sString ):
        return hasSubstring( sString, sSubstring, bCaseSensitive )
    #
    return isSubstringInThisString


def isSpace( s ):
    #
    return s and s.replace( ' ', '' ) == ''


def isInOrder( s ):
    #
    from Iter.AllVers   import iMap, iRange    
    #
    try:
        #
        if len( s ) <= 1:                       raise Finished
        #
        sBeg    = s[  0 ]
        sEnd    = s[ -1 ]
        #
        if sBeg == sEnd:                        raise Finished
        #
        iBeg    = ord( sBeg )
        iEnd    = ord( sEnd )
        #
        if abs( iEnd - iBeg ) + 1 != len( s ):  raise Finished
        #
        if iBeg > iEnd:
            #
            iStep = -1
            #
            iEnd  -= 1
            #
        else:
            #
            iStep = 1
            #
            iEnd  += 1
            #
        #
        sTest = ''.join( iMap( chr, iRange( iBeg, iEnd, iStep ) ) )
        #
        bInOrder = sTest == s
        #
    except Finished:
        #
        bInOrder = False
        #
    #
    return bInOrder



def _startsWithOneOfManually( sToTest, tTryThese ):
    #
    '''pass string and typle of possible starting strings
    returns whether string starts witn any of possible ending strings
    startswith() accepts tuple starting with python 2.5'''
    #
    from Collect.Query  import get1stThatMeets
    #
    def isToTestStartsWith( s ): return sToTest.startswith( s )
    #
    return bool( get1stThatMeets( tTryThese, isToTestStartsWith ) )


try:
    #
    'abc'.startswith( ( 'a', 'c' ) )
    #
    def startsWithOneOf( sToTest, tTryThese ):
        #
        "startswith() accepts tuple starting with python 2.5"
        #
        return sToTest.startswith( tTryThese )
    #
except:
    #
    startsWithOneOf = _startsWithOneOfManually



def _endsWithOneOfManually( sToTest, tTryThese ):
    #
    '''pass string and typle of possible ending strings
    returns whether string ends witn any of possible ending strings
    endswith() accepts tuple starting with python 2.5'''
    #
    from Collect.Query  import get1stThatMeets
    #
    def isToTestEndsWith( s ): return sToTest.endswith( s )
    #
    return bool( get1stThatMeets( tTryThese, isToTestEndsWith ) )


try:
    #
    'abc'.endswith( ( 'a', 'c' ) )
    #
    def endsWithOneOf( sToTest, tTryThese ):
        #
        "endswith() accepts tuple starting with python 2.5"
        #
        return sToTest.endswith( tTryThese )
    #
except:
    #
    endsWithOneOf = _endsWithOneOfManually


def getHasSubstrTester( sPattern ):
    #
    '''pass a regex pattern, function returns tester;
    this is a factory returning a tester for the pattern
    '''
    from String.Find import getFinderFindAll
    #
    fFinder = getFinderFindAll( sPattern )
    #
    def hasSubstrTester( s ):
        #
        return fFinder( s )
    #
    return hasSubstrTester


def areWordsClose( sWord1, sWord2 ):
    #
    from Iter.AllVers import iRange, iZip, lZip
    #
    bClose = False
    #
    if sWord1 and sWord2:
        #
        sWord1 = sWord1.lower()
        sWord2 = sWord2.lower()
        #
        setWord1 = frozenset( list( sWord1 ) )
        setWord2 = frozenset( list( sWord2 ) )
        #
        iWord1Len = len( sWord1 )
        iWord2Len = len( sWord2 )
        #
        fRatio = abs( 1.0 - ( float( iWord1Len ) / iWord2Len ) )
        #
        iMinLen = min( iWord1Len, iWord2Len )
        iMaxLen = max( iWord1Len, iWord2Len )
        #
        iDifference = abs( iWord1Len - iWord2Len )
        #
        setCharPosns1 = frozenset(
                            lZip( sWord1, iRange(   iWord1Len    ) ) + \
                            lZip( sWord1, iRange( - iWord1Len, 0 ) ) )
        setCharPosns2 = frozenset(
                            lZip( sWord2, iRange(   iWord2Len    ) ) + \
                            lZip( sWord2, iRange( - iWord2Len, 0 ) ) )
        #
        haveOverlap = iDifference < iMinLen // 3 and \
            len( setCharPosns1.intersection( setCharPosns2 ) ) >= iMinLen
        #
        haveSubsets =   setWord1.issubset( setWord2 ) or \
                        setWord2.issubset( setWord1 )
        #
        iSplitAt = iMinLen // 2
        #
        haveStartsOrEndsWith = False
        #
        if iSplitAt > 1:
            #
            haveStartsOrEndsWith = \
                sWord1.startswith( sWord2[ : iSplitAt   ] ) or \
                sWord2.startswith( sWord1[ : iSplitAt   ] ) or \
                sWord1.endswith(   sWord2[  -iSplitAt : ] ) or \
                sWord2.endswith(   sWord1[  -iSplitAt : ] )
        #
        bClose =    fRatio < .3 and \
                    haveStartsOrEndsWith and \
                    ( haveSubsets or haveOverlap )
        #
    #
    return bClose



def isGzipped( s ):
    #
    from zlib import decompress
    #
    bGzipped = True
    #
    try:
        #
        decompress( s )
        #
    except:
        #
        bGzipped = False
        #
    return bGzipped









_getBlanksForDigits = TranslatorFactory( '0123456789' )





def getNumberPattern( s, transBlankCharsOfInterest = _getBlanksForDigits ):
    #
    lParts = [ str( chrs) for chrs in s.split() ]
    #
    sX = 'X'.join( map( str, lParts ) )
    #
    sBlanks = transBlankCharsOfInterest( sX )
    #
    lDigits = []
    #
    sEatPhone = sBlanks
    #
    while sEatPhone:
        #
        while sEatPhone and sEatPhone[0] != ' ':
            #
            sEatPhone = sEatPhone[ 1 : ]
            #
        #
        lDigits.append( len( sEatPhone ) - len( sEatPhone.lstrip() ) )
        #
        sEatPhone = sEatPhone.lstrip()
        #
    #
    return lDigits




if __name__ == "__main__":
    #
    from string         import ascii_lowercase as lowercase
    from string         import digits
    from zlib           import compress
    #
    from six            import print_ as print3
    #
    from Collect.Query  import get1stThatFails, get1stThatMeets
    from Iter.AllVers   import iFilter
    from String.Get     import getStringInRange
    from Utils.Result   import sayTestResult
    from Utils.Version  import PYTHON3
    #
    lProblems = []
    #
    s = getStringInRange( 97, 256 )
    #
    sLess = ''.join( iFilter( isAsciiAlpha, s ) )
    #
    if sLess != lowercase:
        #
        lProblems.append( 'isAsciiAlpha()' )
        #
    #
    s = getStringInRange( 8, 158 )
    #
    sLess = ''.join( iFilter( isAsciiDigit, s ) )
    #
    if sLess != digits:
        #
        lProblems.append( 'isAsciiDigit()' )
        #
    
    if not( hasAnyAlpha( '012e45' ) and not hasAnyAlpha( '012345' ) ):
        #
        lProblems.append( 'hasAnyAlpha()' )
        #
    if hasAlphaOnly( 'ab3de' ) or not hasAlphaOnly( 'abcde' ):
        #
        lProblems.append( 'hasAlphaOnly()' )
        #
    if not( isNotDot(      'a'     ) and not isNotDot(        '.' ) ):
        #
        lProblems.append( 'isNotDot()' )
        #
    if not( hasDigitsOnly( '012345') and not hasDigitsOnly(   '012E45' ) ):
        #
        lProblems.append( 'hasDigitsOnly()' )
        #
    if not( isDigit(         '2'  ) and not isDigit(         'a' ) ):
        #
        lProblems.append( 'isDigit()' )
        #
        #
    if not( isDot(           '.' ) and not isDot(           'a' ) ):
        #
        lProblems.append( 'isDot()' )
        #
    if not( isDigitOrDot( '2' ) and isDigitOrDot( '.' ) and not isDigitOrDot( 'a' ) ):
        #
        lProblems.append( 'isDigitOrDot()' )
        #
    if not( hasAnyDigits( 'abcd3' ) and not hasAnyDigits( 'abcde' ) ):
        #
        lProblems.append( 'hasAnyDigits()' )
        #
    if hasNoDigits( 'abcd3' ) or not hasNoDigits( 'abcde' ):
        #
        lProblems.append( 'hasNoDigits()' )
        #
    if not( hasDigitAndDot( '1.2.3.4' ) and not hasDigitAndDot( '1-2-3-4' ) and not hasDigitAndDot( 'a.b.c.d' ) ):
        #
        lProblems.append( 'hasDigitAndDot()' )
        #
    if not(     hasDigitsAndDotsOnly( '1.2.3.4' ) and \
            not hasDigitsAndDotsOnly( '1-2-3-4' ) and \
            not hasDigitsAndDotsOnly( 'a.b.c.d' ) ):
        #
        lProblems.append( 'hasDigitsAndDotsOnly()' )
        #
    if not( isPunctuation( ';' ) and not isPunctuation( 'a' ) ):
        #
        lProblems.append( 'isPunctuation()' )
        #
    #
    if not( isPunctOrSpace( ';' ) and not isPunctOrSpace( 'a' ) ):
        #
        lProblems.append( 'isPunctOrSpace() punctuation' )
        #
    if not( isPunctOrSpace( ' ' ) and not isPunctOrSpace( 'a' ) ):
        #
        lProblems.append( 'isPunctOrSpace() space' )
        #
    if not( hasNoLower( 'ABCDE' ) and not hasNoLower( 'ABCdE' ) ):
        #
        lProblems.append( 'hasNoLower()' )
        #
    #
    if hasAnyUpper( 'abcde' ) or not hasAnyUpper( 'abCde' ):
        #
        lProblems.append( 'hasAnyUpper()' )
        #
    #
    if          hasMixedCase( 'ABCDE' ) or \
                hasMixedCase( 'abcde' ) or \
            not hasMixedCase( 'abCde' ):
        #
        lProblems.append( 'hasMixedCase()' )
        #
    #
    sTest = 'abcdefghijk'
    #
    if not(     getItemFoundInString( sTest, ( 'wx', 'xy', 'bc' ) ) == 'bc' and \
            not getItemFoundInString( sTest, ( 'wx', 'xy', 'yz' ) ) ):
        #
        lProblems.append( 'getItemFoundInString()' )
        #
    if not(     AnyItemFoundInString( sTest, ( 'wx', 'xy', 'ab' ) ) and \
            not AnyItemFoundInString( sTest, ( 'wx', 'xy', 'yz' ) ) ):
        #
        lProblems.append( 'AnyItemFoundInString()' )
        #
    if not( isQuote1stChar( "'how now'" ) and not isQuote1stChar( "how now" ) ):
        #
        lProblems.append( 'isQuote1stChar()' )
        #
    if not isQuoteLastChar( "'how now'" ) and not isQuoteLastChar( "how now" ):
        #
        lProblems.append( 'isQuoteLastChar()' )
        #
    if not(     EndsWithCharsIgnoreWhite( 'abcde ', 'DE', bCaseSensitive = False ) and \
                EndsWithCharsIgnoreWhite( 'abcde ', 'de', bCaseSensitive = True ) and \
            not EndsWithCharsIgnoreWhite( 'abcde ', 'DE', bCaseSensitive = True ) and \
            not EndsWithCharsIgnoreWhite( 'ABCDE ', 'cd', bCaseSensitive = False ) ):
        #
        lProblems.append( 'EndsWithCharsIgnoreWhite()' )
        #
    if not( hasAlphaNumsOnly( 'abcdefghijk012345' ) and not hasAlphaNumsOnly( 'abcdefghijk012345;' ) ):
        #
        lProblems.append( 'hasAlphaNumsOnly()' )
        #
    if not(     isDigitOrDotOnly( '1' ) and \
                isDigitOrDotOnly( '.' ) and \
            not isDigitOrDotOnly( 'a' ) and \
            not isDigitOrDotOnly( ';' ) ):
        #
        lProblems.append( 'isDigitOrDotOnly()' )
        #
    if not(     isAlphaNumOrDot( 'a' ) and isAlphaNumOrDot( '2' ) and isAlphaNumOrDot( '.' ) and \
            not isAlphaNumOrDot( ';' ) ):
        #
        lProblems.append( 'isAlphaNumOrDot()' )
        #
    #
    if not( isInQuotesSingle( "'abcde'" ) and not isInQuotesSingle( '"abcde"' ) ):
        #
        lProblems.append( 'isInQuotesSingle()' )
        #
    if not(     almostEndsWith( 'abcdefghijk', 'fg', iDropMax = 5 ) and \
            not almostEndsWith( 'abcdefghijk', 'de', iDropMax = 5 ) ):
        #
        lProblems.append( 'almostEndsWith()' )
        #
    if not( endsWithDigit( 'abcdefghijk012345' ) and not endsWithDigit( '012345abcdefghijk' ) ):
        #
        lProblems.append( 'endsWithDigit()' )
        #
    if not(     hasSubstring( 'abcdefghijk012345', 'GHI', bCaseSensitive = False ) and \
                hasSubstring( 'abcdefghijk012345', 'ghi', bCaseSensitive = True ) and \
                hasSubstring( 'abcdefghijk012345', 'G',   bCaseSensitive = False ) and \
                hasSubstring( 'abcdefghijk012345', 'g',   bCaseSensitive = True ) and \
            not hasSubstring( 'abcdefghijk012345', 'GhI', bCaseSensitive = True ) and \
            not hasSubstring( 'abcdefghijk012345', 'Gh1', bCaseSensitive = False ) and \
            not hasSubstring( 'abcdefghijk012345', 'l',   bCaseSensitive = True ) ):
        #
        lProblems.append( 'hasSubstring()' )
        #
    if not( isQuote( '"' ) and isQuote( "'" ) and not isQuote( 'a' ) ):
        #
        lProblems.append( 'isQuote()' )
        #
    if not( isString   ( 'abcde' ) and not isString( 12345 ) ):
        #
        lProblems.append( 'isString()' )
        #
    if not( isNotString( 12345 ) and not isNotString( 'abcde' ) ):
        #
        lProblems.append( 'isNotString()' )
        #
    #
    if isStringLike( 12345 ):
        #
        lProblems.append( 'isStringLike() passed integer' )
        #
    if not isStringLike( 'abcde' ):
        #
        lProblems.append( 'isStringLike() passed string' )
        #
    if not( isEmptyString( '' ) and not isEmptyString( 'a' ) ):
        #
        lProblems.append( 'isEmptyString()' )
        #
    if not( isStringNotEmpty( 'abc' ) and not isStringNotEmpty( '' ) ):
        #
        lProblems.append( 'isStringNotEmpty()' )
        #
    if not(     isStringAndNotEmpty( 'abc' ) and \
            not isStringAndNotEmpty(  123  ) and \
            not isStringAndNotEmpty(  ''   ) ):
        #
        lProblems.append( 'isStringAndNotEmpty()' )
        #
    #
    oTestABC = getStartsWithSomethingTester( 'ABC' )
    #
    if not( oTestABC( 'ABCEFGHIJKL' ) and not oTestABC( '0ABCEFGHIJKL' ) ):
        #
        lProblems.append( 'getStartsWithSomethingTester()' )
        #
    #
    oTestABC = getHasSubstringTester( 'ABC' )
    #
    if not( oTestABC( '012345ABCEFGHIJKL' ) and not oTestABC( '012345A6BCEFGHIJKL' ) ):
        #
        lProblems.append( 'getHasSubstringTester()' )
        #
    #
    oTestJKL = getEndsWithSomethingTester( 'JKL' )
    #
    if not ( oTestJKL( 'ABCEFGHIJKL' ) and not oTestJKL( 'ABCEFGHIJKL0' ) ):
        #
        lProblems.append( 'getEndsWithSomethingTester()' )
        #
    #
    oTestAorBorC = getStartsWithAnyOfTtester( 'ABC' )
    #
    if not ( oTestAorBorC( 'CEFGHIJKL' ) and not oTestAorBorC( 'FGHIJKL' ) ):
        #
        lProblems.append( 'getStartsWithAnyOfTtester()' )
        #
    #
    oTestJorKorL = getEndsWithAnyOfTtester( 'JKL' )
    #
    if not ( oTestJorKorL( 'ABCEFGHIJKL' ) and not oTestJorKorL( 'ABCEFGHIJKL0' ) ):
        #
        lProblems.append( 'getEndsWithAnyOfTtester()' )
        #
    #
    #
    if isSpace( ' abc ' ) or not isSpace( '  ' ):
        #
        lProblems.append( 'isSpace()' )
        #
    #
    if          isInOrder( 'exayza' ) or \
            not isInOrder( 'abcdef' ) or \
            not isInOrder( 'fedcba' ):
        #
        lProblems.append( 'isInOrder()' )
        #
    #
    if          endsWithOneOf( 'abc', ( 'x', 'y', 'z' ) ) or \
            not endsWithOneOf( 'abc', ( 'a', 'b', 'c' ) ):
        #
        lProblems.append( 'endsWithOneOf()' )
        #
    #
    if          startsWithOneOf( 'abc', ( 'x', 'y', 'z' ) ) or \
            not startsWithOneOf( 'abc', ( 'a', 'b', 'c' ) ):
        #
        lProblems.append( 'endsWithOneOf()' )
        #
    #
    if          _endsWithOneOfManually( 'abc', ( 'x', 'y', 'z' ) ) or \
            not _endsWithOneOfManually( 'abc', ( 'a', 'b', 'c' ) ):
        #
        lProblems.append( '_endsWithOneOfManually()' )
        #
    #
    if          _startsWithOneOfManually( 'abc', ( 'x', 'y', 'z' ) ) or \
            not _startsWithOneOfManually( 'abc', ( 'a', 'b', 'c' ) ):
        #
        lProblems.append( '_startsWithOneOfManually()' )
        #
    #
    hasAbcOrXyx = getHasSubstrTester( '(abc|xyz)' )
    #
    if not ( hasAbcOrXyx( '890_abcdefgh' ) and hasAbcOrXyx( 'tuvwxyz_123' ) ):
        #
        lProblems.append( 'getHasSubstrTester() should find substring' )
        #
    #
    if hasAbcOrXyx( 'cdefghijkl' ):
        #
        lProblems.append( 'getHasSubstrTester() substring not in string' )
        #
    #
    if          areWordsClose( 'alphabet', 'zenophobia' ) or \
            not areWordsClose( "Moorehead", "Moorhead" ):
        #
        lProblems.append( 'areWordsClose()' )
        #
    #
    if not areWordsClose( "Pryor", "Prior" ):
        #
        lProblems.append( 'areWordsClose() Pryor Prior' )
        #
    #
    if not areWordsClose( "Brookyln", "Brooklyn" ):
        #
        lProblems.append( 'areWordsClose() Brookyln' )
        #
    #
    if (        isStrongPassword( 'mysecretpassword' ) or
            not isStrongPassword( 'AbCd0123$' ) ):
        #
        lProblems.append( 'isStrongPassword()' )
        #
    #
    s1 = "spam, toast and eggs"
    #
    if PYTHON3: s1 = s1.encode()
    #
    s2 = compress( s1 )
    #
    if isGzipped( s1 ):
        #
        lProblems.append( 'isGzipped() uncompress false positive' )
        #
    #
    if not isGzipped( s2 ):
        #
        lProblems.append( 'isGzipped() did not detect compressed string' )
        #
    #
    sPhone = '+1 (206) 632-9929'
    #
    if _getBlanksForDigits( sPhone ) != '+  (   )    -    ':
        #
        lProblems.append( '_keepLeadingZero() Germany should be No' )
        #
    #
    if getNumberPattern( sPhone ) != [ 1, 3, 3, 4 ]:
        #
        lProblems.append( 'getNumberPattern()' )
        #
    #
    if  (       isStringQuoted(  'xyz'  ) or
            not isStringQuoted( '"xyz"' ) or
                isStringQuoted(  '"'    ) ):
        #
        lProblems.append( 'isStringQuoted()' )
        #
    #
    l = []
    #
    l.extend( setQuoteChars   )
    l.extend( setAsciiAlpha   )
    l.extend( setAsciiDigit   )
    l.extend( setPuncAndSpace )
    l.extend( setNonAlphaNums )
    #
    if get1stThatFails( l, isASCII_128 ):
        #
        lProblems.append( 'isASCII_128() long list' )
        #
    #
    s = '416 961 3455Â'
    #
    if isASCII_128( s[-1] ):
        #
        lProblems.append( 'isASCII_128() single character' )
        #
    #
    if get1stThatMeets( setAsciiAlpha, isDigitPunctOrSpace ):
        #
        lProblems.append( 'isDigitPunctOrSpace() setAsciiAlpha' )
        #
    #
    if get1stThatFails( digits + punctuation + ' ', isDigitPunctOrSpace ):  
        #
        lProblems.append( 'isDigitPunctOrSpace() digits + punctuation' )
        #
    #
    if not hasAscii_128_Only( l ):
        #
        lProblems.append( 'hasAscii_128_Only() long list' )
        #
    #
    if hasAscii_128_Only( s ):
        #
        lProblems.append( 'hasAscii_128_Only() string with funny ending' )
        #
    #
    
    sayTestResult( lProblems )