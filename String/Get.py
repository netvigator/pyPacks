#!/home/rick/.local/bin/pythonTest
# -*- coding: utf-8 -*-
#
# string functions get
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
#   http://www.gnu.org/licenses/
#
# Copyright 2004-2023 Rick Graves
#
from itertools              import takewhile
from gzip                   import GzipFile
from random                 import shuffle, randint
from string                 import digits, ascii_letters as letters
from zlib                   import decompress

from six                    import BytesIO, print_ as print3

try:
    from .Count             import CountSplit
    from .Dumpster          import ( DumpYouNameItClass, oKeepAlphaSpaces,
                                     oKeepAlphaDigitsSpacesHash,
                                     getDigitsOnly )
    from .Find              import getRegExObj
    from .Split             import ( SplitRegular, SplitRight, SplitC,
                                     SplitRightC, getWhiteCleaned )
    from .Test              import ( getItemFoundInString, isDigit,
                                     hasAlphaNumsOnly, isDigitOrDotOnly,
                                     isAlphaNumOrDot, isQuote, isPunctuation,
                                     isAsciiAlpha, getNumberPattern,
                                     isStrongPasswordChar, isStrongPassword )
    from ..Collect.Get      import getSequencePairsThisWithNext
    from ..Collect.Query    import get1stThatMeets
    from ..Iter.AllVers     import iMap, iRange, iFilter, lMap, tMap
    from ..Utils.Combos     import Any_
    from ..Utils.TimeTrial  import TimeTrial
except ( ValueError, ImportError ):
    from String.Count       import CountSplit
    from String.Dumpster    import ( DumpYouNameItClass, oKeepAlphaSpaces,
                                     oKeepAlphaDigitsSpacesHash,
                                     getDigitsOnly )
    from String.Find        import getRegExObj
    from String.Split       import ( SplitRegular, SplitRight, SplitC,
                                     SplitRightC, getWhiteCleaned )
    from String.Test        import ( getItemFoundInString, isDigit,
                                     hasAlphaNumsOnly, isDigitOrDotOnly,
                                     isAlphaNumOrDot, isQuote, isPunctuation,
                                     isAsciiAlpha, getNumberPattern,
                                     isStrongPasswordChar, isStrongPassword )
    from Collect.Get        import getSequencePairsThisWithNext
    from Collect.Query      import get1stThatMeets
    from Iter.AllVers       import iMap, iRange, iFilter, lMap, tMap
    from Utils.Combos       import Any_
    from Utils.TimeTrial    import TimeTrial


_dumpDotsCommas = DumpYouNameItClass( ',.' )


try:
    from string import upper, lower # deprciated in 2.7 and omitted from 3.n
    getUpper = upper
    getLower = lower
except ImportError:
    def getUpper( s ): return s.upper()
    def getLower( s ): return s.lower()



_oParensSearcherObj = getRegExObj( r'(?:\().*?(?:\))' )


def getParensParts( s ):
    #
    lAllInParens = _oParensSearcherObj.findall( s )
    lNotInParens = _oParensSearcherObj.split(   s )
    #
    return ''.join( lAllInParens ), ' () '.join( lNotInParens )



def getStringInRange( iLo, iHi ):
    #
    #
    return ''.join( iMap( chr, iRange( iLo, iHi ) ) )


def getTextAfter( sString, sBefore, iWhichOne=1, fSplit = SplitRegular ):
    #
    """
    Performs case sensitive operations!
    """
    #
    lParts      = fSplit( sString, sBefore )
    #
    del lParts[ : iWhichOne ]
    #
    return sBefore.join( lParts )




def getTextAfterC( sString, sBefore, iWhichOne=1 ):
    #
    """
    Performs operations that are not case sensitive!
    """
    #
    return getTextAfter( sString, sBefore, iWhichOne, SplitC )



def getTextAfterLast( sString, sBefore, fSplit = SplitRight ):
    #
    """
    Performs case sensitive operations!
    could be tweaked to work better with SplitRightC
    """
    #
    if fSplit == SplitRight:
        lParts = fSplit( sString, sBefore, 1 )
    else:
        lParts = fSplit( sString, sBefore )
    #
    return lParts[ -1 ]



def getTextAfterLastC( sString, sBefore ):
    #
    """
    Performs operations that are not case sensitive!
    """
    #
    return getTextAfterLast( sString, sBefore, SplitRightC )



def getTextBefore(
        sString, sAfter, iWhichOne=1, fSplit = SplitRegular,
        bWantEmptyIfNoAfter = True ):
    #
    """
    Performs case sensitive operations!
    """
    #
    lParts  = fSplit( sString, sAfter )
    #
    if bWantEmptyIfNoAfter and len( lParts ) <= iWhichOne: return ''
    #
    del lParts[ iWhichOne : ]
    #
    return sAfter.join( lParts )



def getTextBeforeC( sString, sAfter, iWhichOne=1, fSplit = SplitC, bWantEmptyIfNoAfter = True ):
    #
    """
    Performs operations that are not case sensitive!
    """
    #
    return getTextBefore( sString, sAfter, iWhichOne, SplitC, bWantEmptyIfNoAfter )



def getTextBeforeLast( sString, sAfter, fSplit = SplitRegular ):
    #
    """
    Performs case sensitive operations!
    """
    #
    lParts  = fSplit( sString, sAfter )
    #
    if lParts: del lParts[ -1 ]
    #
    return sAfter.join( lParts )



def getTextBeforeLastC( sString, sAfter ):
    #
    """
    Performs operations that are not case sensitive!
    """
    #
    return getTextBeforeLast( sString, sAfter, SplitC )



def getTextWithin(
        sString, sBefore, sAfter='', iWhichOne=1, bAfterOptional=0, fSplit = SplitRegular ):
    #
    """
    get Text Within delimiters.
    By default, performs case sensitive operations!
    aka getTextBetween
    """
    #
    return getTextBefore(
                getTextAfter( sString, sBefore, iWhichOne, fSplit ),
                sAfter, 1, fSplit, bWantEmptyIfNoAfter = not bAfterOptional )



def getTextWithinFinders( sString, oFindBefore, oFindAfter ):
    #
    sWithin = None
    #
    lBeforeAfterBefore = oFindBefore.split( sString )
    #
    if len( lBeforeAfterBefore ) > 1:
        #
        lBeforeAfterAfter = oFindAfter.split( lBeforeAfterBefore[1] )
        #
        if len( lBeforeAfterAfter ) > 1:
            #
            sWithin = lBeforeAfterAfter[0]
            #
        #
    #
    return sWithin




def getTextWithinC( sString, sBefore, sAfter='', iWhichOne=1, bAfterOptional=0 ):
    #
    return getTextWithin( sString, sBefore, sAfter, iWhichOne, bAfterOptional, SplitC )




def getTextAfterDropNewLine( sString, sBefore, iWhichOne=1, fSplit = SplitRegular ):
    #
    sString = getTextAfter( sString, sBefore, iWhichOne=iWhichOne, fSplit = fSplit )
    #
    return sString.strip().split( '\n' )[ 0 ]

getTextAfterDropNewLine = getTextAfterDropNewLine


def getTextAfterItem( sString, lItems ):
    #
    """
    You pass a whole list of string items to look for in the main string.
    It returns the text after the first string item found in the main string.
    """
    #
    #
    sItem = getItemFoundInString( sString, lItems )
    #
    sAfter = ''
    #
    if sItem != '':
        #
        sAfter = getTextAfter( sString, sItem )
        #
    #
    return sAfter




def getLastDigits( sString, iDigitsMax = 3 ):
    #
    """
    get the last several characters on the end of a string, if they are digits.
    """
    #
    sDigits = getDigitsOffEnd( sString )
    #
    return sDigits[ - iDigitsMax : ]




def getOneLine( sText, iWhich, sNewLine = '\n' ):
    #
    lLines  = sText.split( sNewLine )
    #
    sLine   = ''
    #
    if abs( iWhich ) < len( lLines ) or iWhich == - len( lLines ):
        #
        sLine = lLines[ iWhich ]
    #
    if sLine.endswith( '\r' ): sLine = sLine[ : -1 ]
    #
    return sLine




def getFirstLine( sText, sNewLine = '\n' ):
    #
    return getOneLine( sText, 0, sNewLine )



def getLastLine( sText, sNewLine = '\n' ):
    #
    return getOneLine( sText, -1, sNewLine )




def getTheseCharsOffOneEnd( sText, sGetThese = None, fGetIfMeets = None, bEatOffFront = True ):
    #
    """
    This is the generic program,
    it is normally only called by specific implementations below.
    """
    #
    #
    if sText == '': return ''
    #
    if sGetThese:
        #
        def fGetIfMeets( s ): return s in sGetThese
        #
    #
    #
    if bEatOffFront:
        lText   = sText
    else:
        lText   = list( sText )
        lText.reverse()
    #
    lGet        = takewhile( fGetIfMeets, lText )
    #
    if not bEatOffFront:
        lGet    = list( lGet )
        lGet.reverse()
    #
    return ''.join( lGet )


def getCharsOffBeg( sText, sGetThese = None, fGetIfMeets = None ):
    #
    return getTheseCharsOffOneEnd( sText, sGetThese, fGetIfMeets, bEatOffFront = True )


def getCharsOffEnd( sText, sGetThese = None, fGetIfMeets = None ):
    #
    return getTheseCharsOffOneEnd( sText, sGetThese, fGetIfMeets, bEatOffFront = False )


def getDigitsOffBeg( sText ):
    #
    #
    return getTheseCharsOffOneEnd( sText, fGetIfMeets = isDigit, bEatOffFront = True )


def getDigitsOffEnd( sText ):
    #
    #
    return getTheseCharsOffOneEnd( sText, fGetIfMeets = isDigit, bEatOffFront = False )



def _isDgigitOrDash( c ):
    #
    #
    return isDigit( c ) or c == '-'


def getDigitsAndDashOffEnd( sText ):
    #
    return getTheseCharsOffOneEnd( sText, fGetIfMeets = _isDgigitOrDash, bEatOffFront = False )


def getLineNo4SubStr( sSubStr, sText ):
    #
    #
    iLineNo     = -1
    #
    lParts      = sText.split( sSubStr )
    #
    if len( lParts ) > 1:
        #
        iLineNo = CountSplit( lParts[0], '\n' )
        #
    #
    return iLineNo



def _getOnlySomeChars( sText, fCharsOK ):
    #
    #
    iterText    = iFilter( fCharsOK, sText )
    #
    return ''.join( iterText )



def getAlphaNumsOnly(           sText ):
    #
    #
    return _getOnlySomeChars( sText, hasAlphaNumsOnly )

def getDigitsAndDotsOnly(       sText ):
    #
    #
    return _getOnlySomeChars( sText, isDigitOrDotOnly )

def getAlphaNumsAndDotsOnly(    sText ):
    #
    #
    return _getOnlySomeChars( sText, isAlphaNumOrDot  )



def getInSingleQuotes( sValue, sQuote = "'" ):
    #
    """
    Puts single quotes around the argument.
    """
    #
    return "%s%s%s" % ( sQuote, str( sValue ), sQuote )



def getInDoubleQuotes( sValue ):
    #
    """
    Puts double quotes around the argument.
    """
    #
    return getInSingleQuotes( sValue, sQuote = '"' )


_sQuoteChars = '"' + "'"

def getCharsInQuotesAndQuote( s ):
    #
    #
    #
    sInQuotes, sFirstQuote, s2ndQuote = '', '', ''
    #
    sFirstQuote         = get1stThatMeets( s, isQuote )
    #
    if sFirstQuote:
        #
        sInQuotes       = getTextWithin( s, sFirstQuote, sFirstQuote )
        #
        if not sInQuotes:
            #
            s2ndQuote   = _sQuoteChars[ not _sQuoteChars.find( sFirstQuote ) ]
            #
            sInQuotes   = getTextWithin( s, s2ndQuote, s2ndQuote )
            #
            sFirstQuote = s2ndQuote
        #
    #
    return sInQuotes, sFirstQuote




def getContentOutOfSingleQuotes( s ):
    #
    if s.count( "'" ) >= 2:
        #
        s = getTextWithin( s, "'", "'" )
        #
    #
    return s



def getContentOutOfDoubleQuotes( s ):
    #
    if s.count( '"' ) >= 2:
        #
        s = getTextWithin( s, '"', '"' )
        #
    #
    return s



def getContentOutOfQuotes( s ):
    #
    sInQuotes, sFirstQuote = getCharsInQuotesAndQuote( s )
    #
    if not sFirstQuote: sInQuotes = s
    #
    return sInQuotes



def getEmptyString4None( uValue ):
    #
    if uValue is None:
        #
        uValue = ''
        #
    #
    return uValue


def getCharNotIn( s, iRangeEnd = 256, iRangeBeg = 1 ):
    #
    #
    for i in iRange( iRangeBeg, iRangeEnd ):
        #
        if chr( i ) not in s:
            #
            break
        #
    #
    return chr( i )



def getFrozenStringSetNotCaseSensitive( seq ):
    #
    #
    return frozenset( iMap( getLower, seq ) )


def getBackslashEscaped( sOrig ):
    #
    lParts = sOrig.split( chr(92) )
    #
    sDouble = 2 * chr(92)
    #
    return sDouble.join( lParts )



def getTitleized( s ):
    #
    # see BetterTitle in String.Output
    #
    return s.title()



def getTitleizedIfNeeded( s ):
    #
    if s.islower() or s.isupper():
        #
        s = s.title()
        #
    #
    return s


def getLowerStripPunc( s ):
    #
    #
    sNew = oKeepAlphaSpaces.Dump( s.lower() )
    #
    return getWhiteCleaned( sNew )


def getStripPuncKeepHashOnly( s ):
    #
    #
    sNew = oKeepAlphaDigitsSpacesHash.Dump( s )
    #
    return getWhiteCleaned( sNew )


def getStringsBetDelims( sString, sBefore, sAfter='' ):
    #
    '''
    returns a generator
    maybe you are looking for getTextWithin
    '''
    #
    lBetweens = []
    #
    lParts = sString.split( sBefore )
    #
    if lParts:
        #
        del lParts[0]
        #
    if sAfter:
        #
        getText = getTextBefore
        #
    else:
        #
        def getText( s, sAfter ): return s
        #
    #
    for s in lParts:
        #
        yield getText( s, sAfter )



def getStripped( s ): return s.strip()



def getWhatIs( c ):
    #
    #
    sWhatIs = 'other'
    #
    if c.isupper():          sWhatIs = 'upper'
    elif c.islower():        sWhatIs = 'lower'
    elif c.isdigit():        sWhatIs = 'digit'
    elif isPunctuation( c ): sWhatIs = 'punctuation'
    #
    return sWhatIs



setPairsNeedSpace = frozenset( (
    ( 'lower', 'upper' ),
    ( 'punctuation', 'digit' ), ( 'punctuation', 'lower' ), ( 'punctuation', 'upper' ),
    ( 'other', 'digit' ), ( 'other', 'lower' ), ( 'other', 'upper' ) ) )

setPairsNeedSpaceMaybe = frozenset( ( ( 'digit', 'upper' ), ( 'digit', 'lower' ) ) )


setWantBefore = frozenset( list( '#([{' ) )
setWantAfter  = frozenset( list( '!)]}' ) )

tOrdinalEnds = ( 'th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th' )

setOrdinalEnds= frozenset( tOrdinalEnds )

def _getWantSpaceWhere( c ):
    #
    # '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    #
    #
    sWhere = 'after'
    if isPunctuation( c ):
        sWhere = 'both'
        if   c in setWantBefore: sWhere = 'before'
        elif c in setWantAfter:  sWhere = 'after'
    #
    return sWhere

def _getPairsNeedSpace( t ): return t in setPairsNeedSpace

def _getPairsNeedSpaceMaybe( t ): return t in setPairsNeedSpaceMaybe

def putSpacesInMixed( s ):
    #
    '''
    putSpacesInMixed( '4045CumerladAve#88' ) returns '4045 Cumerlad Ave #88'
    '''
    #
    lWhat = iMap( getWhatIs, s )
    #
    tPairs = getSequencePairsThisWithNext( lWhat )
    #
    lBreakOrNot = lMap( _getPairsNeedSpace, tPairs )
    #
    tBreakMaybe = tMap( _getPairsNeedSpaceMaybe, tPairs )
    #
    if Any_( tBreakMaybe ):
        #
        for i in iRange( len( tBreakMaybe ) ):
            #
            if not tBreakMaybe[i]: continue
            #
            sNextTwo = s[ i+1 : i+3 ].lower()
            #
            if not ( sNextTwo in tOrdinalEnds and \
                     sNextTwo == tOrdinalEnds[ int( s[ i ] ) ] ):
                #
                lBreakOrNot[i] = 1
    #
    lContent = list( s )
    #
    iContentLen = len( lContent )
    #
    for i in iRange( iContentLen - 2, -1, -1 ):
        #
        if lBreakOrNot[ i ]:
            #
            sWantWhere = _getWantSpaceWhere( lContent[ i ] )
            #
            if sWantWhere in ( 'after', 'both' ):
                #
                lContent[ i + 1 : i + 1 ] = [ ' ' ]
            #
            if sWantWhere in ( 'before', 'both' ):
                #
                lContent[ i : i ] = [ ' ' ]
    #
    return ' '.join( ''.join( lContent ).strip().split() )



def _getRandomChars( seq, iHowMany = 10 ):
    #
    '''
    get ramdom characters off a sequence
    '''
    #
    #
    l = list( seq )
    #
    if 3 * iHowMany > len( l ):
        #
        l = l * ( ( iHowMany * 3 // len( l ) ) +
                  ( iHowMany * 3 %  len( l ) > 0 ) )
        #
    #
    shuffle( l )
    #
    iLen = len( l )
    #
    iStart = int( ( iLen / 2 ) - ( iHowMany * 1.5 ) )
    #
    lGot = l[ iStart : iStart + ( iHowMany * 3 ) : 3 ]
    #
    shuffle( lGot )
    #
    return ''.join( lGot )


def _getLettersAndNumbers():
    #
    #
    l = list( digits)
    l.extend( list( letters ) )
    l.extend( list( digits  ) )
    #
    return l


_LettersAndNumbers = _getLettersAndNumbers()


def _getRandomAlphaNums( iHowMany = 10 ):
    #
    '''
    get ramdom ASCII letters & digits
    '''
    #
    return _getRandomChars( _LettersAndNumbers, iHowMany )


    

def _getRandomChar( isWanted = None, tRange = ( 33, 126 ) ):
    #
    #
    if isWanted is None: isWanted = isAsciiAlpha
    #
    while True:
        #
        s = chr( randint( *tRange ) )
        #
        if isWanted( s ): break
        #
    #
    return s



def getRandomChars( iHowMany = 10, isWanted = None, tRange = ( 33, 126 ) ):
    #
    '''
    get ramdom characters
    function defaults to ASCII letters & digits
    you get these if isWanted is not passed or is None
    '''
    #
    #
    lReturn = [ None ] * iHowMany
    #
    for i in iRange( iHowMany ):
        #
        lReturn[i] = _getRandomChar( isWanted, tRange )
        #
    #
    return ''.join( lReturn )


def getRandomAlphaNums( iHowMany = 10 ):
    #
    '''
    get ramdom ASCII letters & digits
    '''
    #
    return getRandomChars( iHowMany )



def getRandomDigits( iHowMany = 10 ):
    #
    '''getRandomDigits in Numbs.Get is a lot faster
    '''
    #
    #
    return getRandomChars( iHowMany, isDigit, ( 48, 57 ) )



def getRandomStrongPassword( iHowMany = 10 ):
    #
    '''
    get ramdom ASCII letters & digits
    '''
    #
    #
    lChars = []
    #
    if iHowMany < 6: iHowMany = 6
    #
    while True:
        #
        lChars.append( _getRandomChar( isStrongPasswordChar ) )
        #
        if len( lChars ) < iHowMany: continue
        #
        sTest = ''.join( lChars[ -iHowMany : ] )
        #
        if isStrongPassword( sTest ): break
        #
    #
    return sTest
        
    
def getUnGzipped( sCompressed ):
    #
    #
    sStream         = BytesIO( sCompressed )
    #
    oZipper         = GzipFile( fileobj = sStream )
    #
    bUnZipped       = True
    sContent        = ''
    #
    try:
        #
        sContent    = oZipper.read() # zip sometimes chokes
        #
    except:
        #
        bUnZipped   = False
        #
    #
    return bUnZipped, sContent



def getUnZipped( s ):
    #
    #
    bGzipped = True
    #
    try:
        #
        s = decompress( s )
        #
    except:
        #
        bGzipped = False
        #
    return bGzipped, s



def getUnZippedOrContent( s ):
    #
    bGzipped, s = getUnZipped( s )
    #
    return s


def getUnGzippedOrContent( s ):
    #
    bGzipped, s = getUnGzipped( s )
    #
    return s



def getWhiteCleanedDumpDotsCommas( s ):
    #
    #
    return getWhiteCleaned( _dumpDotsCommas.Dump( s ) )



def getPatternNumbers( sOrig, lPattern = [] ):
    #
    #
    try:
        sOrig = sOrig.encode( 'ascii' )
    except UnicodeDecodeError:
        #
        l = [ ' ' ] * len( sOrig )
        #
        for i in iRange( len( sOrig ) ):
            #
            if sOrig[i].isdigit():
                #
                l[i] = sOrig[i]
                #
            #
        #
        sOrig = ''.join( l )
        #
    #
    if sOrig and not lPattern:
        #
        lPattern  = getNumberPattern( sOrig )
        #
    #
    lPatternNumbers = []
    #
    iStart = 0
    #
    sDigits = getDigitsOnly( sOrig )
    #
    for iLen in lPattern:
        #
        if iLen:
            #
            lPatternNumbers.append( sDigits[ iStart : iStart + iLen ] )
            #
            iStart += iLen
        #
    #
    return lPatternNumbers



def getUpToLenSplitOnWhite( s, iMaxLen ):
    #
    sReturn = s
    #
    if len( s ) > iMaxLen:
        
        l = s.split()
        
        if len( l[0] ) > iMaxLen:
            sReturn = s[:iMaxLen]
        else:
            iLen = -1
            lParts = []
            for sPart in l:
                iLen += 1 + len( sPart )
                lParts.append( sPart )
                if iLen > iMaxLen: break
            #
            sReturn = ' '.join( lParts[ : -1 ] )
            #
        #
    return sReturn


# https://stackoverflow.com/questions/21605526/how-to-create-raw-string-from-string-variable-in-python
def str_to_raw(s):
    raw_map = {8:r'\b', 7:r'\a', 12:r'\f', 10:r'\n', 13:r'\r', 9:r'\t', 11:r'\v'}
    return r''.join(i if ord(i) > 32 else raw_map.get(ord(i), i) for i in s)


_dRawMap = {8:r'\b', 7:r'\a', 12:r'\f', 10:r'\n', 13:r'\r', 9:r'\t', 11:r'\v'}

def getRawGotStr(sOrig):
    #
    return r''.join( [ _dRawMap.get( ord(c), c ) for c in sOrig ] )



def _doTimeTrial():
    #
    #
    sOrig = "C:\Documents and Settings\b_zz\Desktop\fy_file"
    #
    #
    print3( '\ndoing str_to_raw() ...\n' )
    #
    iCallsPerSet, iSets = TimeTrial( str_to_raw, sOrig )
    #
    print3( '\ndoing getRawGotStr() ...\n' )
    #
    TimeTrial( getRawGotStr, sOrig,
                        iCallsPerSet = iCallsPerSet, iSets = iSets )
    #



if __name__ == "__main__":
    #
    from string         import digits, whitespace, punctuation
    from string         import ascii_letters   as letters
    from string         import ascii_uppercase as uppercase
    from string         import ascii_lowercase as lowercase
    #
    from six            import print_ as print3
    #
    from Iter.AllVers   import tMap
    from Utils.Result   import sayTestResult
    #
    #
    lProblems = []
    #
    #print3( 'length of lProblems: ', len( lProblems ) )
    #
    tStrs   = ( letters, lowercase, uppercase, digits, whitespace, punctuation )
    sTest   = digits + lowercase + digits + uppercase + digits
    sLines  = '\n'.join( ( digits, lowercase, digits, uppercase, digits ) )
    sSome   = lowercase + digits + uppercase
    #
    sPuncTextPunc   = '; abcde: '
    sNotWanted      = whitespace + punctuation
    #
    def notWanted( c ): return c in sNotWanted
    #
    if getUpper( lowercase ) != uppercase:
        #
        lProblems.append( 'getUpper( lowercase )' )
        #
    #        
    if getLower( uppercase ) != lowercase:
        #
        lProblems.append( 'getLower( uppercase )' )
        #
    #        
    if getStringInRange( 48, 58 ) != digits:
        #
        print3( getStringInRange( 48, 57 ) )
        lProblems.append( 'getStringInRange()' )
        #
    #
    if      getTextAfter( letters, 'UVW' ) != 'XYZ' or \
            getTextAfter( sTest, '456', 3      ) != '789':
        #
        lProblems.append( 'getTextAfter()' )
        #
    if      getTextAfterC( letters, 'UVW', 2 ) != 'XYZ':
        #
        lProblems.append( 'getTextAfterC()' )
        #
    if getTextAfterLast( letters, 'UVW' ) != 'XYZ':
        #
        lProblems.append( 'getTextAfterLast()' )
        #
    if getTextAfterLastC( letters, 'uvw' ) != 'XYZ':
        #
        lProblems.append( 'getTextAfterLastC()' )
        #
    #
    sMessy = '''(('NY', 'CITY', '', ''), {'status': 'OK', 'results': [{'geometry': {'location_type': 'APPROXIMATE', 'bounds': {'northeast': {'lat': 40.915241299999998, 'lng': -73.700271999999998}, 'southwest': {'lat': 40.495908, 'lng': -74.259087899999997}}, 'viewport': {'northeast': {'lat': 40.849534200000001, 'lng': -73.749854299999996}, 'southwest': {'lat': 40.578896399999998, 'lng': -74.262091900000001}}, 'location': {'lat': 40.7143528, 'lng': -74.005973099999991}}, 'address_components': [{'long_name': 'New York', 'types': ['locality', 'political'], 'short_name': 'New York'}, {'long_name': 'New York', 'types': ['administrative_area_level_2', 'political'], 'short_name': 'New York'}, {'long_name': 'New York', 'types': ['administrative_area_level_1', 'political'], 'short_name': 'NY'}, {'long_name': 'United States', 'types': ['country', 'political'], 'short_name': 'US'}], 'formatted_address': 'New York, NY, USA', 'types': ['locality', 'political']}]})'''
    #
    sMessy = getTextAfter( sMessy, "'location'" )
    sMessy = getTextAfter( sMessy, "{" )
    #
    if getTextBefore( sMessy, '}' ) != \
            ''''lat': 40.7143528, 'lng': -74.005973099999991''':
        #
        lProblems.append( 'getTextBefore() double braces on end 1' )
        #
    s = '''"'lat': 40.7143528, 'lng': -74.005973099999991}},'''
    #
    if getTextBefore( s, '}' ) != \
            '''"'lat': 40.7143528, 'lng': -74.005973099999991''':
        #
        print3( getTextBefore( s, '}' ) )
        lProblems.append( 'getTextBefore() double braces on end 2' )
        #
    if getTextBefore( letters, 'ABC' ) != lowercase:
        #
        lProblems.append( 'getTextBefore()' )
        #
    if getTextBeforeC( sTest, 'z0123456789A' ) != '0123456789abcdefghijklmnopqrstuvwxy':
        #
        lProblems.append( 'getTextBeforeC()' )
        #
    if getTextBeforeLast( sTest, '0' ) != digits + lowercase + digits + uppercase:
        #
        lProblems.append( 'getTextBeforeLast()' )
        #
    if getTextBeforeLastC( sTest, 'abc' ) != digits + lowercase + digits:
        #
        lProblems.append( 'getTextBeforeLastC()' )
        #
    if      getTextWithin( sTest, digits, digits    ) != lowercase or \
            getTextWithin( sTest, digits, digits, 2 ) != uppercase or \
            getTextWithin( sTest, 'xyz',  'ABC'     ) != digits          or \
            getTextWithin( sTest, 'abc',  'ghi'     ) != 'def'           or \
            getTextWithin( sTest, 'abc',  'GHI'     ) != 'defghijklmnopqrstuvwxyz0123456789ABCDEF':
        #
        lProblems.append( 'getTextWithin()' )
        #
    if      getTextWithinC( sTest, 'abc', 'GHI'    ) != 'def' or \
            getTextWithinC( sTest, 'abc', 'GHI', 2 ) != 'DEF':
        #
        lProblems.append( 'getTextWithinC()' )
        #
    #
    if      getTextAfterDropNewLine( sLines, '01234' ) != '56789' or \
            getTextAfterDropNewLine( sLines, 'abc'   ) != 'defghijklmnopqrstuvwxyz':
        #
        lProblems.append( 'getTextAfterDropNewLine()' )
        #
    if getTextAfterItem( sTest, ( '!@#', '$%^', 'XYZ' ) ) != digits:
        #
        lProblems.append( 'getTextAfterItem()' )
        #
    if getLastDigits( sTest, iDigitsMax = 4 ) != '6789':
        #
        lProblems.append( 'getLastDigits()' )
        #
    if getOneLine( sLines, 4 ) != digits:
        #
        lProblems.append( 'getOneLine()' )
        #
    if getFirstLine( sLines ) != digits:
        #
        lProblems.append( 'getFirstLine()' )
        #
    if getLastLine( sLines ) != digits:
        #
        lProblems.append( '()' )
        #
    #
    if      getTheseCharsOffOneEnd( sPuncTextPunc, sNotWanted, bEatOffFront = True ) != '; ' or \
            getTheseCharsOffOneEnd( sPuncTextPunc, sNotWanted, bEatOffFront = False ) != ': ':
        #
        lProblems.append( 'getTheseCharsOffOneEnd() chars excluded' )
        #
    #
    if      getTheseCharsOffOneEnd( sPuncTextPunc, fGetIfMeets = notWanted, bEatOffFront = True ) != '; ' or \
            getTheseCharsOffOneEnd( sPuncTextPunc, fGetIfMeets = notWanted, bEatOffFront = False ) != ': ':
        #
        lProblems.append( 'getTheseCharsOffOneEnd() function excluded' )
        #
    
    if getCharsOffBeg( sPuncTextPunc, sNotWanted ) != '; ':
        #
        lProblems.append( 'getCharsOffBeg()' )
        #
    if getCharsOffEnd( sPuncTextPunc, sNotWanted ) != ': ':
        #
        lProblems.append( '()' )
        #
    if getDigitsOffBeg( sTest ) != digits:
        #
        lProblems.append( 'getDigitsOffBeg()' )
        #
    if getDigitsOffEnd( sTest ) != digits:
        #
        lProblems.append( 'getDigitsOffEnd()' )
        #
    if getDigitsAndDashOffEnd( 'Seattle  WA  98103-6625' ) != '98103-6625':
        #
        lProblems.append( 'getDigitsAndDashOffEnd() zip + 4 on end' )
        #
    if getDigitsAndDashOffEnd( 'Seattle  WA  98103' ) != '98103':
        #
        lProblems.append( 'getDigitsAndDashOffEnd() zip5 on end' )
        #
    if getDigitsAndDashOffEnd( 'Seattle  WA  ' ):
        #
        lProblems.append( 'getDigitsAndDashOffEnd() nothing on end' )
        #
    #
    if getLineNo4SubStr( 'ABC', sLines ) != 3:
        #
        lProblems.append( 'getLineNo4SubStr()' )
        #
    if      getAlphaNumsOnly( sTest               ) != sTest or \
            getAlphaNumsOnly( sTest + punctuation ) != sTest:
        #
        lProblems.append( 'getAlphaNumsOnly()' )
        #
    if getDigitsAndDotsOnly( sTest + punctuation ) != ( digits * 3 ) + '.':
        #
        lProblems.append( 'getDigitsAndDotsOnly()' )
        #
    if getAlphaNumsAndDotsOnly( sTest + punctuation ) != sTest + '.':
        #
        lProblems.append( 'getAlphaNumsAndDotsOnly()' )
        #
    if getInSingleQuotes( digits ) != "'" + digits + "'":
        #
        lProblems.append( 'getInSingleQuotes()' )
        #
    if getInDoubleQuotes( digits ) != '"' + digits + '"':
        #
        lProblems.append( 'getInSingleQuotes()' )
        #
    if getCharsInQuotesAndQuote( ' " how now brown cow\' " abc ' ) != \
            (" how now brown cow' ", '"'):
        #
        lProblems.append( 'getCharsInQuotesAndQuote()' )
        #
    #
    if      getEmptyString4None( None )  != '' or \
            getEmptyString4None( 'abc' ) != 'abc':
        #
        lProblems.append( 'getEmptyString4None()' )
        #
    #
    if      getContentOutOfSingleQuotes(
                "'how now brown cow'  abc " ) != "how now brown cow" or \
            getContentOutOfDoubleQuotes( 'abc' ) != 'abc':
        #
        lProblems.append( 'getContentOutOfSingleQuotes()' )
        #
    #
    if      getContentOutOfDoubleQuotes(
                ' " how now brown cow\' " abc ' ) != " how now brown cow' " or \
            getContentOutOfDoubleQuotes( 'abc' ) != 'abc':
        #
        lProblems.append( 'getContentOutOfDoubleQuotes()' )
        #
    #
    if      getContentOutOfQuotes(
                ' " how now brown cow\' " abc ' ) != " how now brown cow' " or \
            getContentOutOfQuotes( 'abc' ) != 'abc':
        #
        # DbApi.Connect()
        # NetObjects()
        #print3( getContentOutOfQuotes( ' " how now brown cow\' " abc ' ) )
        #print3( getContentOutOfQuotes( 'abc' ) )
        lProblems.append( 'getContentOutOfQuotes()' )
        #
    if      ord( getCharNotIn(          'abc' ) ) != 1 or \
            ord( getCharNotIn( chr(1) + 'abc' ) ) != 2:
        #
        lProblems.append( 'getCharNotIn()' )
        #
    if      getFrozenStringSetNotCaseSensitive( lowercase ) != \
            getFrozenStringSetNotCaseSensitive( uppercase ):
        #
        lProblems.append( 'getFrozenStringSetNotCaseSensitive()' )
        #
    #
    if getBackslashEscaped( r'c:\temp\temp.txt' ) != r'c:\\temp\\temp.txt':
        #
        lProblems.append( 'getBackslashEscaped()' )
        #
    #
    if      (   getTitleizedIfNeeded( 'Jane' ),
                getTitleizedIfNeeded( 'JANE' ),
                getTitleizedIfNeeded( 'jane' )
            ) != ( 'Jane', 'Jane', 'Jane' ):
        #
        lProblems.append( "getTitleizedIfNeeded( 'Jane' )" )
        #
    #
    if getTitleizedIfNeeded( 'JanE' ) != 'JanE':
        #
        lProblems.append( "getTitleizedIfNeeded( 'JanE' )" )
        #
    #
    sJunk = '12345(abcd)6789(efgh)10234(ijklm)5678'
    #
    tBetweens = tuple( getStringsBetDelims( sJunk, '(', ')' ) )
    #
    if tBetweens != ( 'abcd', 'efgh', 'ijklm' ):
        #
        lProblems.append( "getStringsBetDelims()" )
        #
    #
    if tMap( getWhatIs, '4045CumerladAve#88' ) != \
            ('digit', 'digit', 'digit', 'digit',
            'upper', 'lower', 'lower', 'lower', 'lower', 'lower', 'lower', 'lower',
            'upper', 'lower', 'lower',
            'punctuation', 'digit', 'digit'):
        #
        lProblems.append( "getWhatIs()" )
        #
    #
    if putSpacesInMixed( '4045CumerladAve#88' ) != '4045 Cumerlad Ave #88':
        #
        lProblems.append( "putSpacesInMixed()" )
        #
    #
    if putSpacesInMixed( '4045CumerladAve' ) != '4045 Cumerlad Ave':
        #
        lProblems.append( "putSpacesInMixed() no space address" )
        #
    #
    if putSpacesInMixed( "123rd Street West" ) != "123rd Street West":
        #
        lProblems.append( "putSpacesInMixed() normal adress spaces OK" )
        #
    #
    if putSpacesInMixed( "123Street West" ) != "123 Street West":
        #
        lProblems.append( "putSpacesInMixed() normal adress but space missing" )
        #
    if putSpacesInMixed( "123rdStreetWest" ) != "123rd Street West":
        #
        lProblems.append( "putSpacesInMixed() normal adress no spaces" )
        #
    #
    if (    len( getRandomAlphaNums(  ) ) != 10 or
            len( getRandomAlphaNums(88) ) != 88 ):
        #
        lProblems.append( "getRandomAlphaNums() right length" )
        #
    #
    if not getRandomAlphaNums(88).isalnum():
        #
        lProblems.append( "getRandomAlphaNums() something not AlphaNum" )
        #
    #
    if (    len( _getRandomAlphaNums(  ) ) != 10 or
            len( _getRandomAlphaNums(88) ) != 88 ):
        #
        lProblems.append( "_getRandomAlphaNums()" )
        #
    #
    
    if (    len( getRandomDigits(  ) ) != 10 or
            len( getRandomDigits(88) ) != 88 ):
        #
        lProblems.append( "getRandomDigits() right length" )
        #
    #
    if not getRandomDigits(88).isdigit():
        #
        lProblems.append( "getRandomDigits() something not a digit" )
        #
    #
    if (    len( getRandomStrongPassword(  ) ) != 10 or
            len( getRandomStrongPassword(88) ) != 88 ):
        #
        lProblems.append( "getRandomStrongPassword()" )
        #
    #
    if getLowerStripPunc( ' St. Johns  ' ) != 'st johns':
        #
        lProblems.append( "getLowerStripPunc()" )
        #
    #
    if getStripPuncKeepHashOnly( ' St. Johns #3' ) != 'St Johns #3':
        #
        print3( getStripPuncKeepHashOnly( ' St. Johns #3' ) )
        lProblems.append( "getStripPuncKeepHashOnly()" )
        #
    #
    if getWhiteCleanedDumpDotsCommas( ' St. Johns, #3 ' ) != 'St Johns #3':
        #
        print3( getWhiteCleanedDumpDotsCommas( 'St Johns #3' ) )
        lProblems.append( "getWhiteCleanedDumpDotsCommas()" )
        #
    #
    sPhone = '+1 (206) 632-9929'
    lWant  = [ '1', '206', '632', '9929' ]
    #
    if getPatternNumbers( sPhone ) != lWant:
        #
        lProblems.append( 'getPatternNumber() just the string' )
        #
    #
    if getPatternNumbers( sPhone, [ 1, 3, 3, 4 ] ) != lWant:
        #
        lProblems.append( 'getPatternNumber() string and list' )
        #
    #
    sShort = 'abc def'
    #
    if getUpToLenSplitOnWhite( sShort, 76 ) != sShort:
        #
        lProblems.append( 'getUpToLenSplitOnWhite( sShort, 76 )' )
        #
    #
    sLong  = (  'aaaa bbbb cccc ddddd eee fffffff ggggggg hhhhhh '
                'iiiii jjjjj kkk llllll mmmm nnnn oooo pppp qqqqq '
                'rrrr sss ttttt uuuu vvvv www xxxxx yyy zzzzz' )
    #
    sExpect = ( 'aaaa bbbb cccc ddddd eee fffffff ggggggg hhhhhh '
                'iiiii jjjjj kkk llllll mmmm' )
    #
    if getUpToLenSplitOnWhite( sLong, 76 ) != sExpect:
        #
        lProblems.append( 'getUpToLenSplitOnWhite( sLong, 76 )' )
        #
    #
    sOrig = "C:\Documents and Settings\b_zz\Desktop\fy_file"
    sWant = 'C:\\Documents and Settings\\b_zz\\Desktop\\fy_file'
    #
    if getRawGotStr( sOrig ) != sWant:
        #
        lProblems.append( 'getRawGotStr("%s")' % sOrig )
        #
    #
    #
    sIn, sOut = getParensParts( sLong )
    #
    if sIn:
        #
        lProblems.append( 'getParensParts() nothing in parens' )
        #
    #
    if sOut != sLong:
        #
        lProblems.append( 'getParensParts() no parens' )
        #
    #
    #
    s = (   "4x KT61 ( 6AG6 G ) tubes HALTRON ( M.O.V. ) - "
            "NOS (~  6V6G / EL33 /  EL3 ) KT 61" )
    #
    sIn, sOut = getParensParts( s )
    #
    if sIn != '( 6AG6 G )( M.O.V. )(~  6V6G / EL33 /  EL3 )':
        #
        lProblems.append( 'getParensParts() in parens' )
        #
    #
    if sOut != '4x KT61  ()  tubes HALTRON  ()  - NOS  ()  KT 61':
        #
        lProblems.append( 'getParensParts() not in parens' )
        #
    #
    # getTextWithinFinders( sString, oFindBefore, oFindAfter )
    #
    oFindBefore = getRegExObj( 'ddddd '   )
    oFindAfter  = getRegExObj( ' fffffff' )
    #
    sGot = getTextWithinFinders( sLong, oFindBefore, oFindAfter )
    #
    if sGot != 'eee':
        #
        lProblems.append( 'getTextWithinFinders() found text' )
        #
    #
    oFindNotFound = getRegExObj( 'wxyz' )
    #
    if getTextWithinFinders( sLong, oFindNotFound, oFindAfter ) is not None:
        #
        lProblems.append( 'getTextWithinFinders() not found before' )
        #
    #
    if getTextWithinFinders( sLong, oFindBefore, oFindNotFound ) is not None:
        #
        lProblems.append( 'getTextWithinFinders() not found after' )
        #
    #
    #
    sayTestResult( lProblems )
