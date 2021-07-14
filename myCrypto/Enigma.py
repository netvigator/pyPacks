#!/home/rick/bin/pythonTest
# -*- coding: utf-8 -*-
#
# myCrypto functions Enigma
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
CHAR_RANGE = 1 + MAX_CHAR - MIN_CHAR


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


def _getCutAt( iBigNumb, iEncryptLen, bWantCloserToCenter = False ):
    #
    # if iCutAt = zero, the deck/string will be cut in the middle
    # if iCutAt < zero, the deck/string will be cut closer to the front
    # if iCutAt > zero, the deck/string will be cut closer to the end
    #
    iCutAt       = iBigNumb % iEncryptLen - ( iEncryptLen // 2 )
    #
    iLen         = iEncryptLen # want to keep below lines < 80 chars
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
        return i < 1 or i >= iEncryptLen
    #
    if isNotWithin( tCutPosition[0] ) or isNotWithin( tCutPosition[1] ):
        #
        iCutAt   = iCutAt // 2
        #
    #
    if bWantCloserToCenter and iCutAt > iEncryptLen // 4:
        #
        iCutAt   = iCutAt // 2
        #
    #
    return iCutAt


oFilePhraseStats = AscStats( sFilePhrase )


def _getMoreAscStats(
            sStatsPhrase, sEncrypt, iBoostTotal = 0, iDifference = None ):
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
    if oFilePhraseStats.sString == sStatsPhrase:
        #
        o           = oFilePhraseStats
        #
    else:
        #
        o           = AscStats( sStatsPhrase )
    #
    if iDifference is None:
        #
        iDifference = o.iDifference
        #
    #
    iUseTotal       = o.iTotal + iBoostTotal
    #
    iBigNumb        = max( iDifference, ( iUseTotal - iDifference ) )
    #
    iMinNumb        = min( iDifference, ( iUseTotal - iDifference ) )
    #
    iEncryptLen     = len( sEncrypt )
    #
    bWantCloserToCenter = iBoostTotal # and isOdd( o.iTotal )
    #
    o.iCutAt0       = _getCutAt( iBigNumb,  iEncryptLen, bWantCloserToCenter )
    #
    o.iCutAt1       = _getCutAt( iUseTotal, iEncryptLen, bWantCloserToCenter )
    #
    o.iCutAt2       = _getCutAt( iMinNumb,  iEncryptLen, bWantCloserToCenter )
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
    if bStepIncrement:
        #
        iIncrement = -1 if bBackStep else 1
        #
        def getIncrement( i ): return iIncrement * ( i % 8 )
        #
    else:
        #
        def getIncrement( i ): return 0
        #
    #
    def getNewChar( sChar, iThis ):
        #
        i = 255 + iOffset + getIncrement( iThis ) - ord( sChar )
        #
        return chr( i % 256 )
    #
    lNewChars = lMap( getNewChar, sOrig, iRange( len( sOrig ) ) )
    #
    if bBackwards: lNewChars.reverse()
    #
    return ''.join( lNewChars )





def FlipCase( sText, bAlternate = False ):
    #
    r'''
    if bAlternate = False aBcDeF becomes AbCdEf
    if bAlternate = True  aBcDeF becomes ABCDEF
    BUT
    now that this code is accomodating new lines,
    \n & \r should not be swapped to \N or \R !!!!
    '''
    #
    lParts = oFinderCRorLFnMore.split(   sText )
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
    if len( lParts ) > 1:
        #
        lNewLs = oFinderCRorLFnMore.findall( sText )
        #
        lCorrect = []
        #
        iStart   = 0
        #
        for i in range( len( lParts ) ):
            #
            lCorrect.append( sFlipped[ iStart : iStart + len( lParts[i] ) ] )
            #
            iStart += len( lParts[i] )
            #
            if len( lNewLs ) > i:
                #
                lCorrect.append( lNewLs[i] )
                #
                iStart += len( lNewLs[i] )
                #
            #
        #
        sFlipped = ''.join( lCorrect )
        #
    #
    return sFlipped




def _getThisShifted( iThis, iShift ):
    #
    '''
    want characters from space 32 to tilde ~ 126 inclusive
    range of 95 (126 - 32) + 1 (want inclusive)
    The USA keyboard has 47 keys that yield ASCII characters,
      and the output of each is varied by Shift
    add one more: space (spacebar)
    _getThisShifted( 32, 92 ) returns 124 |
    _getThisShifted( 32, 93 ) returns 125 }
    _getThisShifted( 32, 94 ) returns 126 ~
    _getThisShifted( 32, 95 ) returns  32 space
    _getThisShifted( 32, 96 ) returns  33 !
    _getThisShifted( 32, 97 ) returns  34 "
    '''
    #
    iShiftTo = iThis + iShift
    #
    return iShiftTo if iShiftTo <= MAX_CHAR else iShiftTo - CHAR_RANGE



def _getShiftedPutBack( iThis, iShift ):
    #
    '''
    undo for _getThisShifted
    want characters from space 32 to tilde ~ 126 inclusive
    range of 95 (126 - 32) + 1 (want inclusive)
    The USA keyboard has 47 keys that yield ASCII characters,
      and the output of each is varied by Shift
    add one more: space (spacebar)
    _getShiftedPutBack(  35,  1 ) returns  34 "
    _getShiftedPutBack(  35,  2 ) returns  33 !
    _getShiftedPutBack(  35,  3 ) returns  32 space
    _getShiftedPutBack(  35,  4 ) returns 126 ~
    _getShiftedPutBack(  35,  5 ) returns 125 }
    _getShiftedPutBack(  35,  6 ) returns 124 |
    '''
    #
    iShiftTo = iThis - iShift
    #
    return iShiftTo if iShiftTo >= MIN_CHAR else iShiftTo + CHAR_RANGE





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




def _shuffleEncrypted( sEncrypted, oPassPhraseStats, bPutBack = False ):
    #
    # bShuffleEncrypted is True
    #
    iBoostTotal     = oPassPhraseStats.iTotal
    iPassPhDiff     = oPassPhraseStats.iDifference
    #
    oEncrStats      = _getMoreAscStats(
                        sEncrypted, sEncrypted, iBoostTotal, iPassPhDiff )
    #
    iEncrTotal      = oEncrStats.iTotal
    #
    iBigInteger     = iEncrTotal + iBoostTotal
    #
    if bPutBack:
        #
        if isOdd( iBigInteger ):
            #
            sEncrypted = getTextReversed( sEncrypted )
            #
        #
        iCutAtIn    = oEncrStats.iCutAt1
        iCutAtOut   = oEncrStats.iCutAt2
        #
        # deck of cards will return to original order
        # after 8 perfect shuffles!
        #
        iShufflesIn = ( iBigInteger % 3 ) + 1
        iShufflesOut= ( iBigInteger % 5 ) + 1
        #
    else:
        #
        iCutAtIn    = oEncrStats.iCutAt2
        iCutAtOut   = oEncrStats.iCutAt1
        #
        # deck of cards will return to original order
        # after 8 perfect shuffles!
        #
        iShufflesIn = ( iBigInteger % 5 ) + 1
        iShufflesOut= ( iBigInteger % 3 ) + 1
        #
    #
    iCutAtMid       = oEncrStats.iCutAt0
    #
    iShufflesMid    = ( iBigInteger % 4 ) + 1
    #
    sConverted      = ShuffleAndCut(
                            ShuffleAndCut(
                                    ShuffleAndCut(
                                        sEncrypted,
                                        bPutBack,
                                        iShuffles  = iShufflesIn,
                                        iCutOffset = iCutAtIn ),
                            bPutBack,
                            iShuffles  = iShufflesMid,
                            iCutOffset = iCutAtMid ),
                        bPutBack,
                        iShuffles  = iShufflesOut,
                        iCutOffset = iCutAtOut )
    #
    oFinalStats = AscStats( sConverted )
    #
    if isOdd( iBigInteger ) and not bPutBack:
        #
        sConverted = getTextReversed( sConverted )
        #
    #
    return sConverted




def Encrypt( sThis,
             sPassPhrase        = sFilePhrase,
             iRevThis           = True,
             iRevPassPhrase     = False,
             getCharsShifted    = _getCharsShifted,
             bShuffleEncrypted  = False ):
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
    oPassPhraseStats = _getMoreAscStats( sPassPhrase, sThis )
    #
    iCutAt0          = oPassPhraseStats.iCutAt0
    iCutAt1          = oPassPhraseStats.iCutAt1
    #
    if iRevThis is None:
        #
        iRevThis    = oPassPhraseStats.iTotal
        #
    #
    if iRevPassPhrase is None:
        #
        iRevPassPhrase = oPassPhraseStats.iDifference
        #
    #
    sConverted  = ShuffleAndCut(
                        _getTextReversedMaybe(
                            ShuffleAndCut( sThis, iCutOffset = iCutAt0 ),
                            iRevThis ),
                    iCutOffset = iCutAt1 )
    #
    # Encrypt STEP 2 shift all characters
    #
    iPassPhraseNumb = max(
                oPassPhraseStats.iDifference,
                ( oPassPhraseStats.iTotal - oPassPhraseStats.iDifference ) )
    #
    sConverted  = getCharsShifted(
                        sConverted,
                        _getThisShifted,
                        sPassPhrase,
                        iPassPhraseNumb,
                        iRevPassPhrase )
    #
    # Encrypt STEP 3 shuffle encrypted characters (if applicable)
    #
    if bShuffleEncrypted:
        #
        sConverted = _shuffleEncrypted( sConverted, oPassPhraseStats )
        #
    #
    return sConverted



def Encrypt2( sThis, sPassPhrase = sFilePhrase ):
    #
    return Encrypt( sThis,
                    sPassPhrase,
                    iRevThis          = None,
                    iRevPassPhrase    = None,
                    getCharsShifted   = _getCharsShifted2,
                    bShuffleEncrypted = True )



def EncryptNone( sEncryptThis ):
    #
    ''' backward compatability '''
    #
    sConverted  = ShuffleAndCut(
                    getTextReversed( ShuffleAndCut( sEncryptThis ) ) )
    #
    oPassPhraseStats      = AscStats( sConverted )
    #
    iUseOffset  = ( oPassPhraseStats.iLength % 4 ) - \
                  ( oPassPhraseStats.iDifference % 8 )
    #
    sConverted  = DescendChars( sConverted, iUseOffset )
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
                sPassPhrase       = sFilePhrase,
                iRevThis          = True,
                iRevPassPhrase    = False,
                getCharsShifted   = _getCharsShifted,
                bShuffleEncrypted = False ):
    #
    # Decrypt STEP -3 undo shuffle encrypted characters (if applicable)
    #
    oPassPhraseStats    = _getMoreAscStats( sPassPhrase, sDecryptThis )
    #
    if bShuffleEncrypted:
        #
        sDecryptThis    = _shuffleEncrypted(
                            sDecryptThis, oPassPhraseStats, bPutBack = True )
        #
    #
    # Decrypt STEP -2 shift all characters
    #
    if iRevThis is None:
        #
        iRevThis = oPassPhraseStats.iTotal
        #
    #
    if iRevPassPhrase is None:
        #
        iRevPassPhrase = oPassPhraseStats.iDifference
        #
    #
    iPassPhraseNumb = oPassPhraseStats.iTotal - oPassPhraseStats.iDifference
    #
    sConverted  = getCharsShifted(
                        sDecryptThis,
                        _getShiftedPutBack,
                        sPassPhrase,
                        iPassPhraseNumb,
                        iRevPassPhrase )
    #
    iCutAt0     = oPassPhraseStats.iCutAt0
    iCutAt1     = oPassPhraseStats.iCutAt1
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
                    iRevThis          = None,
                    iRevPassPhrase    = None,
                    getCharsShifted   = _getCharsShifted2,
                    bShuffleEncrypted = True )



def DecryptNone( sDecryptThis ):
    #
    sConverted  = DescendChars( FlipCase( sDecryptThis, True ), 0, 1 )
    #
    oPassPhraseStats      = AscStats( sConverted )
    #
    iUseOffset  = ( oPassPhraseStats.iLength % 4 ) - \
                  ( oPassPhraseStats.iDifference % 8 )
    #
    sConverted  = DescendChars( sConverted, iUseOffset )
    #
    return _getShuffleCutReverseShuffleCut( sConverted, 0, 0 )



def XOREncrypt( sText, sPassword = 'hello' ):
    #
    #
    lText       = iMap( ord, sText     )
    tPassword   = tMap( ord, sPassword )
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
            sPassPhrase         = sFilePhrase,
            iRevThis            = True,
            iRevPassPhrase      = False,
            getCharsShifted     = _getCharsShifted,
            bShuffleEncrypted   = False ):
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
    oPassPhraseStats  = _getMoreAscStats( sPassPhrase, sThis )
    #
    if iRevThis is None:
        #
        iRevThis = oPassPhraseStats.iTotal
        #
    #
    if iRevPassPhrase is None:
        #
        iRevPassPhrase = oPassPhraseStats.iDifference
        #
    #
    iPassPhraseNumb = oPassPhraseStats.iTotal - oPassPhraseStats.iDifference
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
    iCutAt1 = oPassPhraseStats.iCutAt1
    #
    sConverted = _getShuffleShiftReverseFlipPunctuate(
                        sThis, getShifted, iCutAt1, iRevThis )
    #
    if bShuffleEncrypted:
        #
        sConverted = _shuffleEncrypted( sConverted, oPassPhraseStats )
        #
    #
    return sConverted


def EncryptLite2( sThis, sPassPhrase = sFilePhrase ):
    #
    return EncryptLite(
                    sThis,
                    sPassPhrase,
                    iRevThis          = None,
                    iRevPassPhrase    = None,
                    getCharsShifted   = _getCharsShifted2,
                    bShuffleEncrypted = True )



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
                 getCharsShifted    = _getCharsShifted,
                 bShuffleEncrypted  = False ):
    #
    oPassPhraseStats  = _getMoreAscStats( sPassPhrase, sThis )
    #
    if bShuffleEncrypted:
        #
        sThis = _shuffleEncrypted(
                            sThis, oPassPhraseStats, bPutBack = True )
        #
    #
    if iRevThis is None:
        #
        iRevThis = oPassPhraseStats.iTotal
        #
    #
    if iRevPassPhrase is None:
        #
        iRevPassPhrase = oPassPhraseStats.iDifference
        #
    #
    iPassPhraseNumb = oPassPhraseStats.iTotal - oPassPhraseStats.iDifference
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
    iCutAt1 = oPassPhraseStats.iCutAt1
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
                    iRevThis          = None,
                    iRevPassPhrase    = None,
                    getCharsShifted   = _getCharsShifted2,
                    bShuffleEncrypted = True )



def DecryptLiteNone( sThis ):
    #
    getShifted  = getRot13
    #
    return _getPunctuateFlipReverseShiftShuffleCut( sThis, getShifted, 0 )




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
        lSayMore.append( 'has a single quote' )
        #
    elif bGotDoubleQuote:
        #
        lSayMore.append( 'has a double quote' )
        #
    #
    if bGotBackSlash:
        #
        lSayMore.append(
                'has a backslash character, must test, might not work' )
        #
    #
    if bGodDoubleSpace:
        #
        lSayMore.append(
                'has double spaces, HTML compresses, need a warning' )
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
    # return sOut

def pDL( s ):
    sOut = DecryptLite( s )
    print3( sOut )
    # return sOut

def pD2( s ):
    sOut = Decrypt2( s )
    print3( sOut )
    # return sOut

def pDL2( s ):
    sOut = DecryptLite2( s )
    print3( DecryptLite2( s ) )
    # return sOut



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
        print( 'sTest:    ',     sTest )
        print( 'Encrypted:', sEncryptedH )
        print( 'Decrypted:', sDecryptedH )
        #
        lProblems.append( 'Decrypt2( Encrypt2( "%s" ) )' % sTest )
        #
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
    sEncryptedOdd = EncryptLite( sTest,         sFilePhraseOdd )
    sDecryptedOdd = DecryptLite( sEncryptedOdd, sFilePhraseOdd )
    #
    if sDecryptedOdd != sTest:
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
    if sDecryptedOdd != sTest:
        #
        lProblems.append( 'DecryptLite2( EncryptLite2( "%s" ) )' % sTest )
        #
    #
    sEncryptedOdd = EncryptLite2( sTest,         sFilePhraseOdd )
    sDecryptedOdd = DecryptLite2( sEncryptedOdd, sFilePhraseOdd )
    #
    if sDecryptedOdd != sTest:
        #
        print3( 'sEncryptedOdd:', sEncryptedOdd )
        print3( 'sDecryptedOdd:', sDecryptedOdd )
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
    #
    sTest = 'The cat \\ in the hat.'
    #
    sEncrypted = EncryptLite2( sTest )
    sDecrypted = DecryptLite2( sEncrypted )
    #
    if sDecrypted != sTest:
        #
        print3( sEncrypted )
        print3( sDecrypted )
        lProblems.append( 'DecryptLite2( EncryptLite2( "%s" ) )' % sTest )
        #
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
    #
    iShift = 95 % CHAR_RANGE
    #
    if _getThisShifted( 32, iShift ) != 32:
        #
        lProblems.append( '_getThisShifted( 32, 0 )' )
        #
    #
    iShift = 96 % CHAR_RANGE
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
        ' -- has both single and double quotes *AND* has a backslash character, '
            'must test, might not work',
        ' -- has both single and double quotes',
        ' -- has a single quote *AND* has a backslash character, '
            'must test, might not work',
        ' -- has a double quote *AND* has a backslash character, '
            'must test, might not work',
        ' -- has a single quote',
        ' -- has a double quote',
        ' -- has a backslash character, must test, might not work',
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
        print3( 'sTestCRLF =' )
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
    sTestOrig = ( 'Bullwinkle J Moose\n8888 8888 8888 8888\n' +
                '8888888888888888\n08/28\n888' )
    #
    sTestEncr = Encrypt( sTestOrig )
    #
    if Decrypt( sTestEncr ) != sTestOrig:
        #
        print3( 'a) sTestOrig =' )
        print3( sTestOrig )
        lProblems.append( 'Decrypt( Encrypt( "sTestOrig" ) )' )
        #
    #
    if (    sTestEncr !=
            '''}}/3"c$@kk}}87y'}jek}}nSp(-FJkB}8S)^-8@.'''
            ''''FuU}8\_SkF\@Y}89NT}F0KB}8kZ^''' ):
        #
        print3( 'b) sTestEncr =' )
        print3( sTestEncr )
        lProblems.append( 'Encrypt( "sTestOrig" )' )
        #
    #
    sTestEncr = Encrypt2( sTestOrig )
    #
    if Decrypt2( sTestEncr ) != sTestOrig:
        #
        print3( 'sTestOrig =' )
        print3( sTestOrig )
        lProblems.append( 'Decrypt2( Encrypt2( "sTestOrig" ) )' )
        #
    #
    if (    sTestEncr !=
            '''8q}z)}+89}k"}s(iu\}F.{uk%B'V}8k$:}'''
        r'''&)@{8}TPaT\(?$9}}o'lk$}FaB8kB9}n}\n''' ):
        #
        print3( 'c) sTestEncr =' )
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
            r'''gnJUg;vciw02pg0"UT@cqoU8#=gGqL\tgR0U6g"'''
            r'''gXqFa"m3g0gr"Q=p+p"uggUFr\QjD#''' ):
        #
        print3( 'd) sTestEncr =' )
        print3( sTestEncr )
        lProblems.append( 'EncryptLite2( "sTestEncr" )' )
    #
    #
    sTestEncr = sEncryptedH
    #
    oPassPhraseStats = _getMoreAscStats( sFilePhrase, sTestEncr )
    #
    sShuffled = _shuffleEncrypted( sTestEncr, oPassPhraseStats )
    sPutBack  = _shuffleEncrypted( sShuffled, oPassPhraseStats, bPutBack = True )
    #
    if sTestEncr != sPutBack:
        #
        print3( 'e) sTestEncr =' )
        print3( sTestEncr )
        lProblems.append( '_shuffleEncrypted(( "sTestEncr" )' )
        #
    #
    #
    sSeq = '0123456789ABCDEF'
    #
    sShuffled = _shuffleEncrypted( sSeq,      oPassPhraseStats )
    sPutBack  = _shuffleEncrypted( sShuffled, oPassPhraseStats, bPutBack = True )
    #
    if sSeq != sPutBack:
        #
        print3( 'sSeq = ' )
        print3( sSeq )
        lProblems.append( '_shuffleEncrypted(( "sTestEncr" )' )
        #
    #
    iEncryptLen = len( sSeq )
    #
    lCuts = [ _getCutAt( i, iEncryptLen ) for i in range( 2 * len( sSeq ) ) ]
    #
    iHalfLen = iEncryptLen // 2
    #
    if max( lCuts ) > iHalfLen or min( lCuts ) < - iHalfLen:
        #
        lProblems.append( '_getCutAt() beyond max/min' )
        #
    #
    if      max( lCuts ) not in (  iHalfLen,  iHalfLen - 1 ) or \
            min( lCuts ) not in ( -iHalfLen, -iHalfLen + 1 ):
        #
        print3( iHalfLen, max( lCuts ), min( lCuts ) )
        lProblems.append( '_getCutAt() close enough to max/min' )
        #
    #
    sText = r'abcd\nefgh\rijkl'
    #
    sGot    = FlipCase( sText )
    sExpect = r'ABCD\nEFGH\rIJKL'
    #
    if sGot != sExpect:
        print3( sGot )
        lProblems.append( 'FlipCase() w new lines no alternate' )
        #
    #
    sGot    = FlipCase( sText, bAlternate = True )
    sExpect = r'AbCd\nEfGh\rIjKl'
    if sGot != sExpect:
        print3( sGot )
        lProblems.append( 'FlipCase() w new lines & w alternate' )
        #
    #
    doPasswordAnalysis = False
    #
    if doPasswordAnalysis:
        #
        tPasswords = (
            'My_Great_Password', # no special characters
            'My_Great_Passw0rd', # 0 for o
            'My_Great_P@ssword', # @ for 2nd a
            'My_Gr3at_Password', # 3 for e
            'My_Great_P@ssw0rd', # 0 for o & @ for 2nd a
            'My_Gr3at_Passw0rd', # 0 for o & 3 for e
            'My_Gr3at_P@ssword', # @ for 2nd a & 3 for e
            )
        #
        sPhrase = ( 'Look, Bullwinkle! A message in a bottle! - '
                    'Fan mail from some flounder? - '
                    'No! This is what I really call a message!' )
        #
        sPhrase = 'Bullwinkle is a dope!'
        #
        tCiphers = tuple( [ Encrypt2(s,sPhrase) for s in tPasswords ] )
        #
        iCipherLen = len( tCiphers[0] )
        #
        dColsInCommon = {}
        #
        print3( '         Modulus' )
        print3( 'No Total 5 4 3 2 password          -> encrypted' )
        for i in range( len( tPasswords ) ):
            #
            oX = AscStats( tPasswords[i] )
            oY = AscStats( tCiphers[i] )
            #
            iTotal = oX.iTotal + oY.iTotal
            #
            for j in range( i + 1, len( tPasswords ) ):
                #
                iInCommon = 0
                #
                for k in range( iCipherLen ):
                    #
                    iInCommon += int( tCiphers[i][k] == tCiphers[j][k] )
                    #
                #
                dColsInCommon[ ( i, j ) ] = iInCommon
                #
            #
            print3( "%03d" % i,
                iTotal, iTotal%5, iTotal%4, iTotal%3, iTotal%2,
                tPasswords[i], '->', tCiphers[i] )
            #
        #
        from pprint import pprint
        #
        tRowPairs = tuple( dColsInCommon.keys() )
        #
        for t in tRowPairs:
            #
            if dColsInCommon[ t ] < 3:
                #
                del dColsInCommon[ t ]
                #
            #
        #
        pprint( dColsInCommon )
    #
    #
    sayTestResult( lProblems )
