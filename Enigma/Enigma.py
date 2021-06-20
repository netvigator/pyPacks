#!/home/rick/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Crypto functions Enigma
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
# Copyright 2004-2021 Rick Graves
#
# file known as Encrypt until 2019-03-29
#
'''
sTest                   = 'The quick brown fox jumped over the lazy dog.'

EncryptNone(sTest)      = '\x1ffPrTvWgW.EkW{~pGoLg#hR&DbMqJiZ&Nz!V#gMt\x1fuFx#'

EncryptLiteNone(sTest)  = 'Y=REjqRp=KurB=cVRbgIelZhuS{bOMhDG=t==nW==ABqX'

XOREncrypt( sTest )     = '3c0d094c1e1d0c0f074f0a17031b01480303144f0210' +
                          '011c0a0c45031a0a1a4518040a48090d16164801030b41'

getRot13( sTest )       = 'Gur dhvpx oebja sbk whzcrq bire gur ynml qbt.'

with pass phrase        = 'See Dick. See Jane. See Spot. See Spot run.'

Encrypt(sTest)          = 'DWXr&bqPwtK_Ph:MTermSKHlCXUj.oNe: 7Y^tuXln.:U'

EncryptLite(sTest)      = '|]dxX=H<G5aVIxdZErc3hNTOUu>uG:=MK.M},="5d;Z.S'

'''

from os.path                import join, dirname, realpath
from platform               import system
from string                 import punctuation, digits
from string                 import ascii_lowercase as lowercase
from string                 import ascii_uppercase as uppercase

try:
    from ..String.Find      import oFinderCRorLF, oFinderCRorLFnMore
    from ..String.Replace   import getTextReversed
    from ..String.Stats     import AscStats
    from ..String.Transform import TranslatorFactory, getSwapper
    from ..Collect.Cards    import ShuffleAndCut, getCutPosition
    from ..File.Get         import getFileContent
    from ..File.Test        import isFileThere
    from ..Iter.AllVers     import iMap, lMap, tMap, iZip, iRange
    from ..Numb.Test        import isOdd
    from ..Utils.Both2n3    import print3
except ( ValueError, ImportError ):
    from String.Find        import oFinderCRorLF, oFinderCRorLFnMore
    from String.Replace     import getTextReversed
    from String.Stats       import AscStats
    from String.Transform   import TranslatorFactory, getSwapper
    from Collect.Cards      import ShuffleAndCut, getCutPosition
    from File.Get           import getFileContent
    from File.Test          import isFileThere
    from Iter.AllVers       import iMap, lMap, tMap, iZip, iRange
    from Numb.Test          import isOdd
    from Utils.Both2n3      import print3


# want characters from space 32 to tilde ~ 126 inclusive
MIN_CHAR =  32
MAX_CHAR = 126


_sSafe          =  punctuation.replace( '\\', ' ' ) + digits

changePunct     = TranslatorFactory( _sSafe, getTextReversed( _sSafe ) )

sFilePhrase     = None

sThisLocation   = dirname(realpath(__file__))

if system() == 'Windows':
    sPassPhraseFileName =  'enigma-info' # leading dots not allowed
else:
    sPassPhraseFileName = '.enigma-info' # leading dots are allowed

sPassPhraseFileSpec = join( sThisLocation, sPassPhraseFileName )

sMsg = None

if __name__ == "__main__":
    #
    # need sFilePhrases for testing
    #
    # even total, odd  difference
    sFilePhrase     = 'See Dick. See Jane. See Spot. See Spot run.'
    #
    # odd  total, even difference
    sFilePhraseOdd  = 'See Dick. See Jane. See Spot. See Spot run!'
    #
elif isFileThere( sPassPhraseFileSpec ):
    #
    sFilePhrase = getFileContent( sPassPhraseFileSpec )
    l = [ s for s in oFinderCRorLF.split( sFilePhrase ) if s ]
    sFilePhrase = ''.join( l ).strip()
    #
    if not sFilePhrase:
        #
        sMsg = ( 'the file named "%s" in %s is empty, '
                 'it should contain your secret passphrase'
               % ( sPassPhraseFileName, sThisLocation ) )
        #
    elif len( sFilePhrase ) < 10:
        sMsg = ( 'the passphrase in "%s" in %s is short, '
                 'a longer secret passphrase would be better'
               % ( sPassPhraseFileName, sThisLocation ) )
        #

if not isFileThere( sPassPhraseFileSpec ) and sMsg is None:
    #
    sMsg = ( 'best to have a file named "%s" '
             'in %s, it can contain your secret passphrase'
           % ( sPassPhraseFileName, sThisLocation ) )
    #

if sMsg:
    #
    print3('')
    print3( sMsg )
    print3('')


def _getCutAt( iBigNumb, iEncryptThisLen ):
    #
    # if iCutAt = zero, the deck/string will be cut in the middle
    # if iCutAt < zero, the deck/string will be cut closer to the front
    # if iCutAt > zero, the deck/string will be cut closer to the end
    #
    iCutAt       = iBigNumb % iEncryptThisLen - ( iEncryptThisLen // 2 )
    #
    iLen         = iEncryptThisLen # want to keep below lines < 80 chars
    #
    # getCutPosition returns the regular index position where to cut
    # the first character of the string has regular index position of zero
    #
    tCutPosition = (
            getCutPosition( iLen, bPutBack = True,  iOffset = iCutAt ),
            getCutPosition( iLen, bPutBack = False, iOffset = iCutAt ) )
    #
    def isNotWithin( i ):
        # want a cut position > 0 and before the end of the deck/string
        return i < 1 or i >= iEncryptThisLen
    #
    if isNotWithin( tCutPosition[0] ) or isNotWithin( tCutPosition[1] ):
        #
        iCutAt   = iCutAt // 2
        #
    #
    return iCutAt


def _getMoreAscStats( sPassPhrase, iEncryptThisLen ):
    #
    '''
    consider zero to be the middle position in the string,
    this function should return an object with property iCutAt,
    iCutAt being zero or a signed integer about zero,
    used to decide where to cut the cards/characters in the string.
    if iCutAt = zero, the deck/string will be cut in the middle
    if iCutAt < zero, the deck/string will be cut closer to the front
    if iCutAt > zero, the deck/string will be cut closer to the end
    getCutPosition returns the regular index position where to cut
    the first character of the string has regular index position of zero
    properties of the default object:
    AscStats.iDifference
    AscStats.iLength
    AscStats.iMin
    AscStats.iMax
    AscStats.iTotal
    '''
    #
    o           = AscStats( sPassPhrase )
    #
    iBigNumb    = max( o.iDifference, ( o.iTotal - o.iDifference ) )
    #
    o.iCutAt0   = _getCutAt( iBigNumb, iEncryptThisLen )
    #
    o.iCutAt1   = _getCutAt( o.iTotal, iEncryptThisLen )
    #
    return o




def DescendChars( sOrig,
        iOffset         = 0,
        bStepIncrement  = False,
        bBackStep       = False,
        bBackwards      = False ):
    #
    '''
    chr(101)+chr(102)+chr(103) becomes chr(154)+chr(153)+chr(152)
    '''
    #
    #
    def getIncrement( i ): return 0
    #
    if bStepIncrement:
        #
        iIncrement  = ( -1, 1 )[ not bBackStep ]
        # returns -1 if bBackStep, 1 if not
        #
        def getIncrement( i ): return iIncrement * ( i % 8 )
        #
    #
    def getNewChar( sChar, iThis ):
        #
        i = ( 255 + iOffset + getIncrement( iThis ) - ord( sChar ) )
        #
        return chr( i % 256 )
    #
    lNewChars       = lMap( getNewChar, sOrig, iRange( len( sOrig ) ) )
    #
    if bBackwards: lNewChars.reverse()
    #
    return ''.join( lNewChars )



def FlipCase( sText, bAlternate = False ):
    #
    '''
    if bAlternate = False aBcDeF becomes AbCdEf
    if bAlternate = True  aBcDeF becomes ABCDEF
    '''
    #
    #
    if bAlternate:
        #
        def getFlip( s, i ):
            #
            if i % 2:
                return s
            else:
                return s.swapcase()
        #
        sFlipped    = ''.join(
                        iMap( getFlip, sText, iRange( len( sText ) ) ) )
        #
    else:
        #
        sFlipped    = sText.swapcase()
        #
    #
    return sFlipped



def _getShift( iSeed ):
    #
    '''
    want characters from space 32 to tilde ~ 126 inclusive
    range of 94 (126 - 32)
    The USA keyboard has 47 keys that yield ASCII characters,
      and the output of each is varied by Shift
    a number above the range must wrap around to the beginning
    _getShift(  93 ) returns 93
    _getShift(  94 ) returns 94
    _getShift(  95 ) returns  0
    _getShift(  96 ) returns  1
    _getShift(  97 ) returns  2
    see docstring for _getThisShifted
    '''
    #
    iUseRange = 1 + MAX_CHAR - MIN_CHAR
    #
    return iSeed % iUseRange



def _getThisShifted( iThis, iShift ):
    #
    '''
    want characters from space 32 to tilde ~ 126 inclusive
    range of 94 (126 - 32)
    The USA keyboard has 47 keys that yield ASCII characters,
      and the output of each is varied by Shift
    _getThisShifted( 32, 92 ) returns 124
    _getThisShifted( 32, 93 ) returns 125
    _getThisShifted( 32, 94 ) returns 126
    _getThisShifted( 32, 95 ) returns  32
    _getThisShifted( 32, 96 ) returns  33
    _getThisShifted( 32, 97 ) returns  34
    '''
    #
    if iShift + iThis > MAX_CHAR:
        #
        iShift += MIN_CHAR - MAX_CHAR - 1
        #
    #
    return iThis + iShift


def _getShiftedPutBack( iThis, iShift ):
    #
    '''
    undo for _getThisShifted
    want characters from space 32 to tilde ~ 126 inclusive
    range of 94 (126 - 32)
    The USA keyboard has 47 keys that yield ASCII characters,
      and the output of each is varied by Shift
    _getShiftedPutBack(  35,  1 ) returns  34
    _getShiftedPutBack(  35,  2 ) returns  33
    _getShiftedPutBack(  35,  3 ) returns  32
    _getShiftedPutBack(  35,  4 ) returns 126
    _getShiftedPutBack(  35,  5 ) returns 125
    _getShiftedPutBack(  35,  6 ) returns 124
    '''
    #
    if iThis - iShift < MIN_CHAR:
        #
        iShift -= 1 + MAX_CHAR - MIN_CHAR
        #
    #
    return iThis - iShift






def _getCharsShifted(
            sShiftThis,
            getShifted,
            sPassPhrase,
            iPassPhraseNumb,
            iRevPassPhrase  = False,
            bLongPassPhrase = False ):
    #
    iShiftThisLen   = len( sShiftThis )
    #
    lThisShifted    = [ None ] * iShiftThisLen
    #
    lPassPhrase     = list( sPassPhrase )
    #
    iMakeLonger     = 1
    #
    iPassPhraseLen  = len( sPassPhrase )
    #
    if iShiftThisLen > iPassPhraseLen:
        #
        iMakeLonger = 1 + iShiftThisLen // iPassPhraseLen
        #
    #
    if bLongPassPhrase:
        #
        iMakeLonger *= 2
    #
    if iMakeLonger > 1:
        #
        # make pass phrase longer, have more choice on where to begin
        #
        lPassPhrase *= iMakeLonger
        #
    #
    if isOdd( iRevPassPhrase ):
        #
        lPassPhrase.reverse()
        #
    #
    if bLongPassPhrase:
        #
        # have more choice on where to begin
        #
        iPassPhraseStartAt = iPassPhraseNumb % iPassPhraseLen
        #
    else:
        #
        iPassPhraseStartAt = \
                iPassPhraseNumb % ( len( lPassPhrase ) - iShiftThisLen )
        #
    #
    iOrigPassPhraseLen = len( lPassPhrase )
    #
    if iPassPhraseStartAt > 0:
        #
        del lPassPhrase[ : iPassPhraseStartAt ]
        #
    #
    for i in iRange( iShiftThisLen ):
        #
        lThisShifted[i] = chr(
                            getShifted(
                                ord( sShiftThis [i] ),
                                ord( lPassPhrase[i] ) - MIN_CHAR ) )
        #
    #
    return ''.join( lThisShifted )



def _getCharsShifted2(
            sShiftThis,
            getShifted,
            sPassPhrase,
            iPassPhraseNumb,
            iRevPassPhrase  = None ):
    #
    return _getCharsShifted(
            sShiftThis,
            getShifted,
            sPassPhrase,
            iPassPhraseNumb,
            iRevPassPhrase,
            bLongPassPhrase = True )



def _getTextReversedMaybe( s, i ):
    #
    if isOdd( i ):
        return getTextReversed( s )
    else:
        return s


def Encrypt( sThis,
             sPassPhrase     = sFilePhrase,
             iRevThis        = True,
             iRevPassPhrase  = False,
             getCharsShifted = _getCharsShifted ):
    #
    # Encrypt STEP 0 handle multi line strings
    #
    if oFinderCRorLF.search( sThis ):
        #
        # code works with printable characters, but CR & LF are not printable
        # so convert
        # CR (1 char) to \r (2 chars) and LF (1 char) to \n (2 chars)
        #
        sThis   = sThis.replace( '\n', r'\n' ).replace( '\r', r'\r' )
        #
    #
    # Encrypt STEP 1 shuffle & cut, maybe reverse, shuffle & cut
    #
    oStats      = _getMoreAscStats( sPassPhrase, len( sThis ) )
    #
    iCutAt0     = oStats.iCutAt0
    iCutAt1     = oStats.iCutAt1
    #
    if iRevThis is None:
        #
        iRevThis = oStats.iTotal
        #
    #
    if iRevPassPhrase is None:
        #
        iRevPassPhrase = oStats.iDifference
        #
    #
    sConverted  = ShuffleAndCut(
                        _getTextReversedMaybe(
                            ShuffleAndCut( sThis, iCutOffset = iCutAt0 ),
                            iRevThis ),
                    iCutOffset = iCutAt1 )
    #
    # Encrypt STEP  2 shift all characters
    #
    iPassPhraseNumb = max(
                oStats.iDifference,
                ( oStats.iTotal - oStats.iDifference ) )
    #
    sConverted  = getCharsShifted(
                        sConverted,
                        _getThisShifted,
                        sPassPhrase,
                        iPassPhraseNumb,
                        iRevPassPhrase )
    #
    return sConverted


def Encrypt2( sThis, sPassPhrase = sFilePhrase ):
    #
    return Encrypt( sThis,
                    sPassPhrase,
                    iRevThis        = None,
                    iRevPassPhrase  = None,
                    getCharsShifted = _getCharsShifted2 )


def EncryptNone( sEncryptThis ):
    #
    ''' backward compatability '''
    #
    sConverted  = ShuffleAndCut(
                    getTextReversed( ShuffleAndCut( sEncryptThis ) ) )
    #
    oStats          = AscStats( sConverted )
    #
    iUseOffset      = ( oStats.iLength % 4 ) - ( oStats.iDifference % 8 )
    #
    sConverted      = DescendChars( sConverted, iUseOffset )
    #
    sConverted  = FlipCase( DescendChars( sConverted, 0, 1 ), True )
    #
    return sConverted



def _getShuffleCutReverseShuffleCut(
            sConverted, iCutAt0, iCutAt1, iRevThis = True, iRevPassPhrase = False ):
    #
    return ShuffleAndCut(
                    _getTextReversedMaybe(
                        ShuffleAndCut( sConverted, True, iCutOffset = iCutAt1 ),
                        iRevThis ),
                True, iCutOffset = iCutAt0 )


def Decrypt(    sDecryptThis,
                sPassPhrase     = sFilePhrase,
                iRevThis        = True,
                iRevPassPhrase  = False,
                getCharsShifted = _getCharsShifted ):
    #
    # Decrypt STEP -2 shift all characters
    #
    oStats      = _getMoreAscStats( sPassPhrase, len( sDecryptThis ) )
    #
    if iRevThis is None:
        #
        iRevThis = oStats.iTotal
        #
    #
    if iRevPassPhrase is None:
        #
        iRevPassPhrase = oStats.iDifference
        #
    #
    iPassPhraseNumb = oStats.iTotal - oStats.iDifference
    #
    sConverted  = getCharsShifted(
                        sDecryptThis,
                        _getShiftedPutBack,
                        sPassPhrase,
                        iPassPhraseNumb,
                        iRevPassPhrase )
    #
    iCutAt0     = oStats.iCutAt0
    iCutAt1     = oStats.iCutAt1
    #
    #
    # Encrypt STEP -1 shuffle & cut, reverse, shuffle & cut
    #
    sReturn = _getShuffleCutReverseShuffleCut(
                    sConverted, iCutAt0, iCutAt1, iRevThis )
    #
    # handle multi line strings
    #
    if oFinderCRorLFnMore.search( sReturn ):
        #
        sReturn = sReturn.replace( r'\r', '\r' ).replace( r'\n', '\n' )
        #
    #
    return sReturn



def Decrypt2( sThis, sPassPhrase = sFilePhrase ):
    #
    return Decrypt( sThis,
                    sPassPhrase,
                    iRevThis        = None,
                    iRevPassPhrase  = None,
                    getCharsShifted = _getCharsShifted2 )



def DecryptNone( sDecryptThis ):
    #
    sConverted  = DescendChars( FlipCase( sDecryptThis, True ), 0, 1 )
    #
    oStats      = AscStats( sConverted )
    #
    iUseOffset  = ( oStats.iLength % 4 ) - ( oStats.iDifference % 8 )
    #
    sConverted  = DescendChars( sConverted, iUseOffset )
    #
    return _getShuffleCutReverseShuffleCut( sConverted, 0, 0 )



def XOREncrypt( sText, sPassword = 'hello' ):
    #
    #
    lText       = iMap( ord, list( sText     ) )
    tPassword   = tMap( ord, list( sPassword ) )
    #
    iPasswords  = 1 + ( len( sText ) // len( sPassword ) )
    #
    lPairs      = iZip( lText, tPassword * iPasswords )
    #
    lText       = [ '%02x' % ( iText ^ iPassword, )
                    for iText, iPassword
                    in lPairs ]
    #
    return ''.join( lText )



def XORdecript( sText, sPassword = 'hello' ):
    #
    #
    lChrPairs   = [ ''.join( t ) for t in
                        iZip(   list( sText[ 0 : : 2 ] ),
                                list( sText[ 1 : : 2 ] ) ) ]
    #
    lChrNumbs   = [ int( s, 16 ) for s in lChrPairs ]
    #
    tPassword   = tMap( ord, tuple( sPassword ) )
    #
    iPasswords  = 1 + ( len( sText ) // len( sPassword ) )
    #
    lChrs       = [ chr( iChr ^ iPass )
                    for iChr, iPass
                    in  iZip( lChrNumbs, tPassword * iPasswords ) ]
    #
    return ''.join( lChrs )



def _getRot13Swapper():
    #
    #
    sTo     = ''.join( (    lowercase[ 13 : ],
                            lowercase[ : 13 ],
                            uppercase[ 13 : ],
                            uppercase[ : 13 ] ) )
    #
    sFrom   = ''.join( ( lowercase, uppercase ) )
    #
    return getSwapper( iZip( sFrom, sTo ) )


oSwapRot13 = _getRot13Swapper()





def getRot13( sText ):
    #
    return oSwapRot13( sText )



def _getShuffleShiftReverseFlipPunctuate(
            sThis, getShifted, iCutAt, iRevThis = True, iRevPassPhrase = False ):
    #
    return ShuffleAndCut(
                getShifted(
                    _getTextReversedMaybe(
                        FlipCase( changePunct( sThis ), True ),
                        iRevThis )
                ), iCutOffset = iCutAt )


def EncryptLite(
            sThis,
            sPassPhrase     = sFilePhrase,
            iRevThis        = True,
            iRevPassPhrase  = False,
            getCharsShifted = _getCharsShifted ):
    #
    # handle multi line strings
    #
    if oFinderCRorLF.search( sThis ):
        #
        # code works with printable characters, but CR & LF are not printable
        # so convert
        # CR (1 char) to \r (2 chars) and LF (1 char) to \n (2 chars)
        #
        sThis   = sThis.replace( '\n', r'\n' ).replace( '\r', r'\r' )
        #
    #
    oStats  = _getMoreAscStats( sPassPhrase, len( sThis ) )
    #
    if iRevThis is None:
        #
        iRevThis = oStats.iTotal
        #
    #
    if iRevPassPhrase is None:
        #
        iRevPassPhrase = oStats.iDifference
        #
    #
    iPassPhraseNumb = oStats.iTotal - oStats.iDifference
    #
    def getShifted( sShiftThis ):
        #
        return getCharsShifted(
                    sShiftThis,
                    _getThisShifted,
                    sPassPhrase,
                    iPassPhraseNumb,
                    iRevPassPhrase )
        #
    #
    iCutAt1 = oStats.iCutAt1
    #
    return _getShuffleShiftReverseFlipPunctuate(
                sThis, getShifted, iCutAt1, iRevThis )


def EncryptLite2( sThis, sPassPhrase = sFilePhrase ):
    #
    return EncryptLite(
                    sThis,
                    sPassPhrase,
                    iRevThis        = None,
                    iRevPassPhrase  = None,
                    getCharsShifted = _getCharsShifted2 )



def EncryptLiteNone( sThis ):
    #
    getShifted  = getRot13
    #
    return _getShuffleShiftReverseFlipPunctuate( sThis, getShifted, 0 )


def _getPunctuateFlipReverseShiftShuffleCut(
            sThis, getShifted, iCutAt1, iRevThis = True, iRevPassPhrase = False ):
    #
    return changePunct(
                FlipCase(
                _getTextReversedMaybe(
                    getShifted(
                        ShuffleAndCut( sThis, 1, iCutOffset = iCutAt1 ) ),
                    iRevThis ), 1 ) )


def DecryptLite( sThis,
                 sPassPhrase        = sFilePhrase,
                 iRevThis           = True,
                 iRevPassPhrase     = False,
                 getCharsShifted    = _getCharsShifted ):
    #
    oStats  = _getMoreAscStats( sPassPhrase, len( sThis ) )
    #
    if iRevThis is None:
        #
        iRevThis = oStats.iTotal
        #
    #
    if iRevPassPhrase is None:
        #
        iRevPassPhrase = oStats.iDifference
        #
    #
    iPassPhraseNumb = oStats.iTotal - oStats.iDifference
    #
    def getShifted( sShiftThis ):
        #
        return getCharsShifted(
                    sShiftThis,
                    _getShiftedPutBack,
                    sPassPhrase,
                    iPassPhraseNumb,
                    iRevPassPhrase )
    #
    iCutAt1 = oStats.iCutAt1
    #
    sReturn = _getPunctuateFlipReverseShiftShuffleCut(
                    sThis, getShifted, iCutAt1, iRevThis, iRevPassPhrase )
    #
    # handle multi line strings
    #
    if oFinderCRorLFnMore.search( sReturn ):
        #
        sReturn = sReturn.replace( r'\r', '\r' ).replace( r'\n', '\n' )
        #
    #
    return sReturn



def DecryptLite2( sThis, sPassPhrase = sFilePhrase ):
    #
    return DecryptLite(
                    sThis,
                    sPassPhrase,
                    iRevThis        = None,
                    iRevPassPhrase  = None,
                    getCharsShifted = _getCharsShifted2 )



def DecryptLiteNone( sThis ):
    #
    getShifted  = getRot13
    #
    return _getPunctuateFlipReverseShiftShuffleCut( sThis, getShifted, 0 )



#def getYahooHtmlDecrypted( s, bLite = True ):
    ##
    #'''
    #default is lite
    #pass False as 2nd param to use heavy
    #'''
    #from Web.HTML import getTextgotYahooHTML
    ##
    #sFixed = getTextgotYahooHTML( s )
    ##
    ## sFixed = sFixed[ 1 : ][ 0 : -1 ] # strip quote chars
    ##
    #sFixed = sFixed.replace( "\\", '' ) # don't want \ chars
    ##
    #if bLite:
        #fDecription = DecryptLite
    #else:
        #fDecription = Decrypt
    ##
    #return fDecription( sFixed, sPassPhrase = None )



def _getSayMore(
        bGotSingleQuote, bGotDoubleQuote, bGotBackSlash, bGodDoubleSpace,
        bMultiLineOrig = False ):
    #
    sSayMore = ''
    lSayMore = []
    #
    if bGotSingleQuote and bGotDoubleQuote:
        #
        lSayMore.append( 'has both single and double quotes' )
        #
    elif bGotSingleQuote:
        #
        lSayMore.append( 'has single quote' )
        #
    elif bGotDoubleQuote:
        #
        lSayMore.append( 'has double quote' )
        #
    #
    if bGotBackSlash:
        #
        lSayMore.append( 'has backslash character, must test, might not work' )
        #
    #
    if bGodDoubleSpace:
        #
        lSayMore.append( 'has double spaces, HTML compresses, need a warning' )
        #
    #
    if lSayMore:
        #
        sSayMore = ' *AND* '.join( lSayMore )
        #
    #
    if sSayMore and not bMultiLineOrig:
        #
        sSayMore = ' -- ' + sSayMore
        #
    #
    return sSayMore


def _printOut(  sOrig,
                sPassPhrase = sFilePhrase,
                fEncryptH = Encrypt2,
                fEncryptL = EncryptLite2 ):
    #
    if sOrig is None:
        #
        print3( '\ncalling script must return a value, not just print!!!\n' )
        #
    #
    bMultiLineOrig = oFinderCRorLF.search( sOrig )
    #
    sBackSlash      = chr( 92 )
    sDoubleBack     = sBackSlash * 2
    #
    sEncryptedH     = fEncryptH( sOrig, sPassPhrase )
    sEncryptedL     = fEncryptL( sOrig, sPassPhrase )
    #
    bGotSingleH     = "'" in sEncryptedH
    bGotDoubleH     = '"' in sEncryptedH
    #
    bGotSingleL     = "'" in sEncryptedL
    bGotDoubleL     = '"' in sEncryptedL
    #
    bGotBackSlashH  = sBackSlash in sEncryptedH
    bGotBackSlashL  = sBackSlash in sEncryptedL
    #
    bGodDoubleSpaceH= "  " in sEncryptedH
    bGodDoubleSpaceL= "  " in sEncryptedL
    #
    sSayMoreH       = _getSayMore(
            bGotSingleH, bGotDoubleH, bGotBackSlashH, bGodDoubleSpaceH,
            bMultiLineOrig )
    sSayMoreL       = _getSayMore(
            bGotSingleL, bGotDoubleL, bGotBackSlashL, bGodDoubleSpaceL,
            bMultiLineOrig )
    #
    sEncryptedH2 = sEncryptedL2 = ''
    sRawH = sRawL = ' '
    #
    if bGotBackSlashH:
        #
        sEncryptedH2 = sEncryptedH.replace( sBackSlash, sDoubleBack )
        #
        sRawH = 'r'
        #
    #
    if bGotBackSlashL:
        #
        sEncryptedL2 = sEncryptedL.replace( sBackSlash, sDoubleBack )
        #
        sRawL = 'r'
        #
    #
    if "'" in sEncryptedH and '"' in sEncryptedH:
        #
        sQuoteH = '"""' if sEncryptedH.endswith( "'" ) else "'''"
        #
    else:
        #
        sQuoteH = '"' if "'" in sEncryptedH else "'"
        #
    #
    if "'" in sEncryptedL and '"' in sEncryptedL:
        #
        sQuoteL = '"""' if sEncryptedL.endswith( "'" ) else "'''"
        #
    else:
        #
        sQuoteL = '"' if "'" in sEncryptedL else "'"
        #
    #
    if bMultiLineOrig:
        #
        sSayOrig = 'original:' # ends here
        #
    elif max( len( sQuoteH ), len( sQuoteL  ) ) == 1:
        #
        sSayOrig = 'original:           ' # ends here
        #
    else:
        #
        sSayOrig = 'original:             ' # ends here
        #
    #
    if bMultiLineOrig:
        #
        print3( sSayOrig )
        print3( sOrig )
        #
    else:
        #
        print3( sSayOrig, sOrig )
        #
    #
    sSayHeavy   = '%s%s%s%s' % (
                    sRawH, sQuoteH, sEncryptedH, sQuoteH )
    #
    if bMultiLineOrig:
        #
        print3( 'encrypted heavy:' )
        print3( sSayHeavy.strip() )
        print3( sSayMoreH.strip() )
        #
        if sEncryptedH2:
            #
            print3( 'backslash doubled:' )
            print3( '%s%s%s' % ( sQuoteH, sEncryptedH2, sQuoteH ) )
            #
        #
    else:
        #
        print3( 'encrypted heavy:   %s%s' % ( sSayHeavy, sSayMoreH ) )
        #
        if sEncryptedH2:
            #
            print3( 'backslash doubled:  %s%s%s' %
                    ( sQuoteH, sEncryptedH2, sQuoteH ) )
            #
        #
    #
    sSayLite    = '%s%s%s%s' % (
                    sRawL, sQuoteL, sEncryptedL, sQuoteL )
    #
    if bMultiLineOrig:
        #
        print3( 'encrypted lite:' )
        print3( sSayLite.strip() )
        print3( sSayMoreL.strip() )
        #
        if sEncryptedL2:
            #
            print3( 'backslash doubled:' )
            print3( '%s%s%s' % ( sQuoteL, sEncryptedL2, sQuoteL ) )
            #
        #
    else:
        #
        print3( 'encrypted lite:    %s%s' % ( sSayLite, sSayMoreL ) )
        #
        if sEncryptedL2:
            #
            print3( 'backslash doubled:  %s%s%s' %
                    ( sQuoteL, sEncryptedL2, sQuoteL ) )
            #
        #
    #
    print3( '%s -- %s' % ( sSayHeavy.strip(), sSayLite.strip() ) )


def None2Enigma( sThis ):
    #
    sOrig = DecryptNone( sThis )
    #
    _printOut( sOrig )


def None2EnigmaLite( sThis ):
    #
    sOrig = DecryptLiteNone( sThis )
    #
    _printOut( sOrig )


def EncryptBoth( sThis,
                sPassPhrase = sFilePhrase,
                fEncryptH = Encrypt,
                fEncryptL = EncryptLite ):
    #
    _printOut( sThis, sPassPhrase )

def EncryptBoth2( sThis, sPassPhrase = sFilePhrase ):
    #
    _printOut( sThis, sPassPhrase )


def pD( s ):
    sOut = Decrypt( s )
    print3( sOut )
    return sOut 

def pDL( s ):
    sOut = DecryptLite( s )
    print3( sOut )
    return sOut

def pD2( s ):
    sOut = Decrypt2( s )
    print3( sOut )
    return sOut

def pDL2( s ):
    sOut = DecryptLite2( s )
    print3( DecryptLite2( s ) )
    return sOut



E, D, EB = Encrypt2, pD, EncryptBoth2
D2, DL2  = pD2, pDL2
EL, DL   = EncryptLite, pDL
DN, DLN  = DecryptNone, DecryptLiteNone
EN, ELN  = EncryptNone, EncryptLiteNone



if __name__ == "__main__":
    #
    from string         import ascii_letters   as letters
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if DescendChars( lowercase ) != \
            '\x9e\x9d\x9c\x9b\x9a\x99\x98\x97\x96\x95\x94\x93\x92\x91' + \
            '\x90\x8f\x8e\x8d\x8c\x8b\x8a\x89\x88\x87\x86\x85':
        #
        lProblems.append( 'DescendChars()' )
        #
    if    ( FlipCase( lowercase ) != uppercase or \
            FlipCase( uppercase ) != lowercase or \
            FlipCase( lowercase, bAlternate = True ) != 
                                    'AbCdEfGhIjKlMnOpQrStUvWxYz' or \
            FlipCase( uppercase, bAlternate = True ) != 
                                    'aBcDeFgHiJkLmNoPqRsTuVwXyZ' ):
        #
        lProblems.append( 'FlipCase()' )
        #
    #
    sTest = 'The cat in the hat.'
    #
    if DecryptNone( EncryptNone( sTest ) ) != sTest:
        #
        lProblems.append( 'DecryptNone( EncryptNone( "%s" ) )' % sTest )
        #
    if DecryptLiteNone( EncryptLiteNone( sTest ) ) != sTest:
        #
        lProblems.append( 'DecryptLiteNone( EncryptLiteNone( "%s" ) )' % sTest )
        #
    if Decrypt( Encrypt( sTest ) ) != sTest:
        #
        lProblems.append( 'Decrypt( Encrypt( "%s" ) )' % sTest )
        #
    #
    sEncryptedH = Encrypt2( sTest )
    sDecryptedH = Decrypt2( sEncryptedH )
    #
    if sDecryptedH != sTest:
        #
        print( 'Encrypted:', sEncryptedH )
        print( 'Decrypted:', sDecryptedH )
        #
        lProblems.append( 'Decrypt2( Encrypt2( "%s" ) )' % sTest )
        #
    #
    if DecryptLite( EncryptLite( sTest ) ) != sTest:
        #
        lProblems.append( 'DecryptLite( EncryptLite( "%s" ) )' % sTest )
        #
    #
    sEncryptedEven = EncryptLite( sTest )
    #
    if DecryptLite( sEncryptedEven )!= sTest:
        #
        lProblems.append( 'DecryptLite( EncryptLite( "%s" ) )' % sTest )
        #
    #
    sEncryptedOdd = EncryptLite( sTest, sFilePhraseOdd )
    #
    if DecryptLite( sEncryptedOdd, sFilePhraseOdd  )!= sTest:
        #
        lProblems.append( 'DecryptLite( EncryptLite( "%s" ) ) with Odd pass phrase' % sTest )
        #
    #
    setCommonChars = frozenset(
        [ c for c in sEncryptedOdd
          if c in sEncryptedEven ] )
    #
    if len( setCommonChars ) > len( sTest ) // 2:
        #
        lProblems.append( 'chars in common, DecryptLite( EncryptLite( "%s" ) ) with Odd pass phrase' % sTest )
        #
    #
    sEncryptedEven = EncryptLite2( sTest )
    #
    if DecryptLite2( sEncryptedEven )!= sTest:
        #
        lProblems.append( 'DecryptLite2( EncryptLite2( "%s" ) )' % sTest )
        #
    #
    sEncryptedOdd = EncryptLite2( sTest, sFilePhraseOdd )
    #
    if DecryptLite2( sEncryptedOdd, sFilePhraseOdd  )!= sTest:
        #
        lProblems.append( 'DecryptLite2( EncryptLite2( "%s" ) ) with Odd pass phrase' % sTest )
        #
    #
    setCommonChars = set( [] )
    #
    for c in sEncryptedOdd:
        if c in sEncryptedEven:
            setCommonChars.add( c )
    #
    if len( setCommonChars ) > ( 1 + len( sTest ) ) // 2:
        #
        lProblems.append( 'chars in common, DecryptLite2( EncryptLite2( "%s" ) ) with Odd pass phrase' % sTest )
        #
    #
    #
    if XOREncrypt( sTest ) != '3c0d094c0c09114c0501481104094f00041842':
        #
        lProblems.append( 'XOREncrypt()' )
        #
    if XORdecript( XOREncrypt( sTest ) ) != sTest:
        #
        lProblems.append( 'XORdecript()' )
        #
    #
    if      getRot13( getRot13( sTest ) ) != sTest or \
                      getRot13( sTest ) == sTest:
        #
        lProblems.append( 'getRot13()' )
        #
    #
    sTest = 'The cat \\ in the hat.'
    #
    if DecryptNone( EncryptNone( sTest ) ) != sTest:
        #
        lProblems.append( 'DecryptNone( EncryptNone( "%s" ) )' % sTest )
        #
    if DecryptLiteNone( EncryptLiteNone( sTest ) ) != sTest:
        #
        lProblems.append( 'DecryptLiteNone( EncryptLiteNone( "%s" ) )' % sTest )
        #
    #
    if Decrypt( Encrypt( sTest ) ) != sTest:
        #
        lProblems.append( 'Decrypt( Encrypt( "%s" ) )' % sTest )
        #
    if DecryptLite( EncryptLite( sTest ) ) != sTest:
        #
        lProblems.append( 'DecryptLite( EncryptLite( "%s" ) )' % sTest )
        #
    #
    if Decrypt2( Encrypt2( sTest ) ) != sTest:
        #
        lProblems.append( 'Decrypt2( Encrypt2( "%s" ) )' % sTest )
        #
    if DecryptLite2( EncryptLite2( sTest ) ) != sTest:
        #
        lProblems.append( 'DecryptLite2( EncryptLite2( "%s" ) )' % sTest )
        #
    #
    sTest = 'The cat \x8e in the hat.'
    #
    if DecryptNone( EncryptNone( sTest ) ) != sTest:
        #
        lProblems.append( 'DecryptNone( EncryptNone( "%s" ) )' % sTest )
        #
    if DecryptLiteNone( EncryptLiteNone( sTest ) ) != sTest:
        #
        lProblems.append( 'DecryptLiteNone( EncryptLiteNone( "%s" ) )' % sTest )
        #
    #
    # strings including extended ASCII chars might not decrypt!!!
    #
    sDecryptedHeavy = Decrypt(     Encrypt(     sTest ) )
    sDecryptedLite  = DecryptLite( EncryptLite( sTest ) )
    #
    if  sDecryptedHeavy[:8] != sTest[:8] and sDecryptedHeavy[9:] != sTest[9:]:
        #
        lProblems.append( 'Decrypt( Encrypt( "%s" ) )' % sTest )
        #
    if sDecryptedLite[:8] != sTest[:8] and sDecryptedLite[9:] != sTest[9:]:
        #
        lProblems.append( 'DecryptLite( EncryptLite( "%s" ) )' % sTest )
        #
    #
    if (    _getShift(  88 ) != 88 or
            _getShift(  89 ) != 89 or
            _getShift(  90 ) != 90 or
            _getShift(  91 ) != 91 or
            _getShift(  92 ) != 92 or
            _getShift(  93 ) != 93 or
            _getShift(  94 ) != 94 or
            _getShift(  95 ) !=  0 or
            _getShift(  96 ) !=  1 or
            _getShift(  97 ) !=  2 or
            _getShift(  98 ) !=  3 or
            _getShift(  99 ) !=  4 or
            _getShift( 100 ) !=  5 ):
        #
        lProblems.append( '_getShift( 88 - 100 )' )
        #
    #
    iShift = _getShift( 95 )
    #
    if _getThisShifted( 32, iShift ) != 32:
        #
        lProblems.append( '_getThisShifted( 32, 0 )' )
        #
    #
    iShift = _getShift( 96 )
    #
    if _getThisShifted( 32, iShift ) != 33:
        #
        lProblems.append( '_getThisShifted( 32, 1 )' )
        #
    #
    if (    _getThisShifted( 32, 92 ) != 124 or
            _getThisShifted( 32, 93 ) != 125 or
            _getThisShifted( 32, 94 ) != 126 or
            _getThisShifted( 32, 95 ) !=  32 or
            _getThisShifted( 32, 96 ) !=  33 or
            _getThisShifted( 32, 97 ) !=  34 or
            _getThisShifted( 32, 98 ) !=  35 ):
        #
        lProblems.append( '_getThisShifted( 32, 92 - 98 )' )
        #
    #
    if (    _getShiftedPutBack( 124, 92 ) !=  32 or
            _getShiftedPutBack( 125, 93 ) !=  32 or
            _getShiftedPutBack( 126, 94 ) !=  32 or
            _getShiftedPutBack(  32,  0 ) !=  32 or
            _getShiftedPutBack(  33,  1 ) !=  32 or
            _getShiftedPutBack(  34,  2 ) !=  32 or
            _getShiftedPutBack(  35,  3 ) !=  32 ):
        #
        lProblems.append( '_getShiftedPutBack( various, 92 - 94, 0 - 3 )' )
        #
    #
    if (    _getShiftedPutBack(  35,  0 ) !=  35 or
            _getShiftedPutBack(  35,  1 ) !=  34 or
            _getShiftedPutBack(  35,  2 ) !=  33 or
            _getShiftedPutBack(  35,  3 ) !=  32 or
            _getShiftedPutBack(  35,  4 ) != 126 or
            _getShiftedPutBack(  35,  5 ) != 125 or
            _getShiftedPutBack(  35,  6 ) != 124 ):
        #
        lProblems.append( '_getShiftedPutBack( 35, various )' )
        #
    #
    #
    sGreatPW = 'Gr34tP@55w0rd'
    #
    if Decrypt( Encrypt( sGreatPW ) ) != sGreatPW:
        #
        lProblems.append( 'encrypt/decrypt great password' )
        #
    #
    if Decrypt2( Encrypt2( sGreatPW ) ) != sGreatPW:
        #
        lProblems.append( 'encrypt2/decrypt2 great password' )
        #
    #
    if DecryptLite( EncryptLite( sGreatPW ) ) != sGreatPW:
        #
        lProblems.append( 'encrypt lite/decrypt lite great password' )
        #
    #
    if Decrypt( Encrypt( sGreatPW, 'abc' ), 'abc' ) != sGreatPW:
        #
        lProblems.append( 'encrypt/decrypt great password short passphrase' )
        #
    #
    if DecryptLite( EncryptLite( sGreatPW, 'abc' ), 'abc' ) != sGreatPW:
        #
        lProblems.append(
            'encrypt lite /decrypt lite great password short passphrase' )
        #
    #
    tAll = (( True, True, True, False),
            ( True, True, False,False),
            ( True, False,True, False),
            ( False,True, True, False),
            ( True, False,False,False),
            ( False,True, False,False),
            ( False,False,True, False),
            ( False,False,False,True ),
            ( False,False,False,False) )
    #
    lResults = [ _getSayMore( *t ) for t in tAll ]
    #
    lExpect = [
        ' -- has both single and double quotes *AND* has backslash character, '
            'must test, might not work',
        ' -- has both single and double quotes',
        ' -- has single quote *AND* has backslash character, '
            'must test, might not work',
        ' -- has double quote *AND* has backslash character, '
            'must test, might not work',
        ' -- has single quote',
        ' -- has double quote',
        ' -- has backslash character, must test, might not work',
        ' -- has double spaces, HTML compresses, need a warning',
        '' ]
    #
    if lResults != lExpect:
        #
        sSayProblem = '_getSayMore()'
        #
        if len( lResults ) == len( lExpect ):
            #
            for i in range( len( lResults ) ):
                if lResults[i] != lExpect[i]:
                    print3( 'lResults[%s]:' % i, lResults[i] )
                    print3( 'lExpect [%s]:' % i, lExpect [i] )
            #
        else:
            #
            sSayProblem = '_getSayMore(): lengths of lResults & lExpect differ'
            #
        #
        lProblems.append( sSayProblem )
        #
    #
    sTest = 'line 1\nline 2\nline 3'
    #
    if Decrypt( Encrypt( sTest ) ) != sTest:
        #
        print3( 'sTest = ' )
        print3( sTest )
        lProblems.append( 'Decrypt( Encrypt( "sTest" ) )' )
        #
    if DecryptLite( EncryptLite( sTest ) ) != sTest:
        #
        print3( 'sTest = ' )
        print3( sTest )
        lProblems.append( 'DecryptLite( EncryptLite( "sTest" ) )' )
        #
    #
    if Decrypt2( Encrypt2( sTest ) ) != sTest:
        #
        print3( 'sTest = ' )
        print3( sTest )
        lProblems.append( 'Decrypt2( Encrypt2( "sTest" ) )' )
        #
    if DecryptLite2( EncryptLite2( sTest ) ) != sTest:
        #
        print3( 'sTest = ' )
        print3( sTest )
        lProblems.append( 'DecryptLite2( EncryptLite2( "sTest" ) )' )
        #
    #
    sTestCRLF = 'line 1\r\nline 2\r\nline 3'
    #
    if Decrypt( Encrypt( sTestCRLF ) ) != sTestCRLF:
        #
        print3( 'sTestCRLF = ' )
        print3( sTestCRLF )
        lProblems.append( 'Decrypt( Encrypt( "sTestCRLF" ) )' )
        #
    if DecryptLite( EncryptLite( sTestCRLF ) ) != sTestCRLF:
        #
        print3( 'sTestCRLF = ' )
        print3( sTestCRLF )
        lProblems.append( 'DecryptLite( EncryptLite( "sTestCRLF" ) )' )
        #
    #
    if Decrypt2( Encrypt2( sTestCRLF ) ) != sTestCRLF:
        #
        print3( 'sTestCRLF = ' )
        print3( sTestCRLF )
        lProblems.append( 'Decrypt2( Encrypt2( "sTestCRLF" ) )' )
        #
    if DecryptLite2( EncryptLite2( sTestCRLF ) ) != sTestCRLF:
        #
        print3( 'sTestCRLF = ' )
        print3( sTestCRLF )
        lProblems.append( 'DecryptLite2( EncryptLite2( "sTestCRLF" ) )' )
        #
    #
    sTestOrig = 'Bullwinkle J Moose\n8888 8888 8888 8888\n8888888888888888\n08/28\n888'
    #
    sTestEncr = Encrypt( sTestOrig )
    #
    if Decrypt( sTestEncr ) != sTestOrig:
        #
        print3( 'sTestOrig = ' )
        print3( sTestOrig )
        lProblems.append( 'Decrypt( Encrypt( "sTestOrig" ) )' )
        #
    #
    if (    sTestEncr !=
            '''}}/3"c$@kk}}87y'}jek}}nSp(-FJkB}8S)^-'''
            '''8@.'FuU}8\_SkF\@Y}89NT}F0KB}8kZ^''' ):
        #
        print3( 'sTestEncr = ' )
        print3( sTestEncr )
        lProblems.append( 'Encrypt( "sTestOrig" )' )
        #
    #
    sTestEncr = Encrypt2( sTestOrig )
    #
    if Decrypt2( sTestEncr ) != sTestOrig:
        #
        print3( 'sTestOrig = ' )
        print3( sTestOrig )
        lProblems.append( 'Decrypt2( Encrypt2( "sTestOrig" ) )' )
        #
    #
    if (    sTestEncr !=
            '''k8B}}8F}na98}}9\F${V\8}}?@'u+n$()Bi}}'''
            '''k\&%()9lT}kszB'a:u}}koP${"q8}Tk.''' ):
        #
        print3( 'sTestEncr = ' )
        print3( sTestEncr )
        lProblems.append( 'Encrypt2( "sTestOrig" )' )
    #
    sTestEncr = EncryptLite2( sTestOrig )
    #
    if DecryptLite2( sTestEncr ) != sTestOrig:
        #
        print3( 'sTestOrig = ' )
        print3( sTestOrig )
        lProblems.append( 'DecryptLite2( EncryptLite2( "sTestOrig" ) )' )
        #
    #
    if (    sTestEncr !=
            '''rNoqUpgQU8ar00p;=mQU6pcGgD@"uwLggqX'''
            '''g2t"JUFFgR=g#"\\"U+vg3jTg"iq0#Cgg0\\''' ):
        #
        print3( 'sTestEncr = ' )
        print3( sTestEncr )
        lProblems.append( 'EncryptLite2( "sTestOrig" )' )
    #
    #
    sayTestResult( lProblems )
