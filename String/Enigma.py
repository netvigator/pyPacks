#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# string functions Enigma
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
# Copyright 2004-2019 Rick Graves
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

from os.path            import join, dirname, realpath
from platform           import system
from string             import punctuation, digits

from Collect.Cards      import ShuffleAndCut, getCutPosition
from File.Get           import getFileContent
from File.Test          import isFileThere
from Iter.AllVers       import iRange
from Numb.Test          import isEven, isOdd
from String.Find        import oFinderCRorLF
from String.Replace     import getTextReversed
from String.Stats       import AscStats
from String.Transform   import TranslatorFactory
from Utils.Both2n3      import print3

sSafe   =  punctuation.replace( '\\', ' ' ) + digits

changePunct = TranslatorFactory( sSafe, getTextReversed( sSafe ) )

sFilePhrase = None

sThisLocation       = dirname(realpath(__file__))

if system() == 'Windows':
    sPassPhraseFileName =  'enigma-info' # leading dots not allowed
else:
    sPassPhraseFileName = '.enigma-info' # leading dots are allowed

sPassPhraseFileSpec = join( sThisLocation, sPassPhraseFileName )

sMsg = None

if __name__ == "__main__":
    #
    # need a sFilePhrase for testing
    #
    sFilePhrase = 'See Dick. See Jane. See Spot. See Spot run.'
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
else:
    #
    sMsg = ( 'best to have a file named "%s" '
             'in %s, it can contain your secret passphrase'
           % ( sPassPhraseFileName, sThisLocation ) )
    #

if sMsg is not None:
    #
    print3('')
    print3( sMsg )
    print3('')




def _getMoreAscStats( s, iStringLen ):
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
    '''
    #
    o            = AscStats( s )
    #
    iCutAt       = o.iTotal % iStringLen - ( iStringLen // 2 )
    #
    tCutPosition = ( getCutPosition( s, bPutBack = True,  iOffset = iCutAt ),
                     getCutPosition( s, bPutBack = False, iOffset = iCutAt ) )
    #
    def isNotWithin( i ):
        # want a cut position > 0 and before the end of the deck/string
        return i < 1 or i >= len( s )
    #
    if isNotWithin( tCutPosition[0] ) or isNotWithin( tCutPosition[1] ):
        #
        iCutAt   = iCutAt // 2
        #
    #
    o.iCutAt     = iCutAt
    #
    return o


def _getAlternatingChars( uOne, uTwo ):
    #
    '''
    s1 = 'abcde'
    s2 = 'ABCDEFG'
    _getAlternatingChars( s1, s2 ) returns:
    'aAbBcCdDeE'
    '''
    #
    lOne = list( uOne )
    lTwo = list( uTwo )
    #
    if len( lOne ) > len( lTwo ):
        #
        iMakeLonger = ( len( lOne ) // len( lTwo ) ) + 1
        #
        lTwo = lTwo * iMakeLonger
        #
    #
    lOut = []
    #
    for i in iRange( len( lOne ) ):
        #
        lOut.extend( [ lOne[i], lTwo[i] ] )
        #
    #
    return ''.join( lOut )



def _getFirstCharThenAlternate( s, fChoose = isEven ):
    #
    '''
    s = 'ABCDEFGhIjKlMnOp'
    _getFirstCharThenAlternate( s )
    returns
    'ACEGIKMO'
    '''
    #
    lOut = []
    #
    for i in iRange( len( s ) ):
        #
        if fChoose( i ):
            #
            lOut.append( s[i] )
            #
        #
    #
    return ''.join( lOut )




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
    from Iter.AllVers import lMap, iRange
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
    from Iter.AllVers import iMap, iRange
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



def _getShift( iSeed, iMax = 126 ):
    #
    '''
    want characters space 32 & above
    do not normally want chars higher than 126
    _getShift(  93 ) returns 93
    _getShift(  94 ) returns 94
    _getShift(  95 ) returns  0
    _getShift(  96 ) returns  1
    _getShift(  97 ) returns  2
    see docstring for _getThisShifted
    '''
    #
    iUseRange = iMax - 31
    #
    return iSeed % iUseRange


def _getThisShifted( iThis, iShift, iMax = 126 ):
    #
    '''
    want characters space 32 & above
    do not normally want chars higher than 126
    _getThisShifted( 32, 92 ) returns 124
    _getThisShifted( 32, 93 ) returns 125
    _getThisShifted( 32, 94 ) returns 126
    _getThisShifted( 32, 95 ) returns  32
    _getThisShifted( 32, 96 ) returns  33
    _getThisShifted( 32, 97 ) returns  34
    '''
    #
    if iShift + iThis > iMax:
        #
        iShift += 31 - iMax
        #
    #
    return iShift + iThis


def _getThisUnShifted( iThis, iShift, iMax = 126 ):
    #
    '''
    undo for _getThisShifted
    want characters space 32 & above
    do not normally want chars higher than 126
    _getThisUnShifted(  35,  1 ) returns  34
    _getThisUnShifted(  35,  2 ) returns  33
    _getThisUnShifted(  35,  3 ) returns  32
    _getThisUnShifted(  35,  4 ) returns 126
    _getThisUnShifted(  35,  5 ) returns 125
    _getThisUnShifted(  35,  6 ) returns 124
    '''
    #
    if iThis - iShift < 32:
        #
        iShift -= iMax - 31
        #
    return iThis - iShift



def _getCharsShifted( sShiftThis, getShifted, sPassPhrase ):
    #
    lThisShifted = [ None ] * len( sShiftThis )
    #
    lPassPhrase = list( sPassPhrase )
    #
    if len( sShiftThis ) > len( sPassPhrase ):
        #
        iMore = 1 + len( sShiftThis ) // len( sPassPhrase )
        #
        lPassPhrase *= iMore
        #
    #
    for i in iRange( len( sShiftThis ) ):
        #
        lThisShifted[i] = chr(
                            getShifted(
                                ord( sShiftThis[i]  ),
                                ord( lPassPhrase[i] ) - 32 ) )
        #
    #
    return ''.join( lThisShifted )




def Encrypt( sEncryptThis, sPassPhrase = sFilePhrase ):
    #
    # Encrypt STEP 1 shuffle & cut, reverse, shuffle & cut
    #
    oStats      = _getMoreAscStats( sPassPhrase, len( sEncryptThis ) )
    #
    iCutAt      = oStats.iCutAt
    #
    sConverted  = ShuffleAndCut(
                    getTextReversed(
                        ShuffleAndCut(
                            sEncryptThis ) ), iCutOffset = iCutAt )
    #
    # Encrypt STEP  2 shift all characters
    #
    sConverted  = _getCharsShifted(
                        sConverted, _getThisShifted, sPassPhrase )
    #
    return sConverted



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



def _getShuffleCutReverseShuffleCut( sConverted, iCutAt ):
    #
    return ShuffleAndCut(
                getTextReversed(
                    ShuffleAndCut(
                        sConverted, True, iCutOffset = iCutAt ) ), True )


def Decrypt( sDecryptThis, sPassPhrase = sFilePhrase ):
    #
    # Decrypt STEP -2 shift all characters
    #
    oStats      = _getMoreAscStats( sPassPhrase, len( sDecryptThis ) )
    #
    sConverted  = _getCharsShifted(
                        sDecryptThis, _getThisUnShifted, sPassPhrase )
    #
    iCutAt      = oStats.iCutAt
    #
    #
    # Encrypt STEP -1 shuffle & cut, reverse, shuffle & cut
    #
    return _getShuffleCutReverseShuffleCut( sConverted, iCutAt )



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
    iCutAt      = 0
    #
    return _getShuffleCutReverseShuffleCut( sConverted, iCutAt )



def XOREncrypt( sText, sPassword = 'hello' ):
    #
    from Iter.AllVers   import iMap, tMap, iZip
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
    from Iter.AllVers   import iMap, tMap, iZip
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
    from string import ascii_lowercase as lowercase
    from string import ascii_uppercase as uppercase
    #
    from Iter.AllVers     import iZip
    from String.Transform import getSwapper
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



def _getShuffleShiftReverseFlipPunctuate( sThis, getShifted, iCutAt ):
    #
    return ShuffleAndCut(
                getShifted(
                getTextReversed(
                FlipCase(
                changePunct( sThis ), True ) ) ), iCutOffset = iCutAt )


def EncryptLite( sThis, sPassPhrase = sFilePhrase ):
    #
    oStats    = _getMoreAscStats( sPassPhrase, len( sThis ) )
    #
    def getShifted( sShiftThis ):
        #
        return _getCharsShifted(
                    sShiftThis, _getThisShifted, sPassPhrase )
        #
    #
    iCutAt      = oStats.iCutAt
    #
    return _getShuffleShiftReverseFlipPunctuate( sThis, getShifted, iCutAt )



def EncryptLiteNone( sThis ):
    #
    getShifted  = getRot13
    #
    iCutAt      = 0
    #
    return _getShuffleShiftReverseFlipPunctuate( sThis, getShifted, iCutAt )


def _getPunctuateFlipReverseShiftShuffleCut( sThis, getShifted, iCutAt ):
    #
    return changePunct(
                FlipCase(
                getTextReversed(
                getShifted(
                ShuffleAndCut( sThis, 1, iCutOffset = iCutAt ) ) ), 1 ) )


def DecryptLite( sThis, sPassPhrase = sFilePhrase ):
    #
    oStats    = _getMoreAscStats( sPassPhrase, len( sThis ) )
    #
    def getShifted( sShiftThis ):
        #
        return _getCharsShifted(
                    sShiftThis, _getThisUnShifted, sPassPhrase )
    #
    #
    iCutAt      = oStats.iCutAt
    #
    #
    return _getPunctuateFlipReverseShiftShuffleCut( sThis, getShifted, iCutAt )



def DecryptLiteNone( sThis ):
    #
    getShifted  = getRot13
    #
    iCutAt      = 0
    #
    return _getPunctuateFlipReverseShiftShuffleCut( sThis, getShifted, iCutAt )



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




if __name__ == "__main__":
    #
    from string         import digits
    from string         import ascii_letters   as letters
    from string         import ascii_lowercase as lowercase
    from string         import ascii_uppercase as uppercase
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
    if DecryptLite( EncryptLite( sTest ) ) != sTest:
        #
        lProblems.append( 'DecryptLite( EncryptLite( "%s" ) )' % sTest )
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
    # &#39;*g$fh%bA%Yt&#39;
    # to
    # Tung6550Sol
    #
    # also need to convert
    # &amp;quot;&amp;#39;***&amp;amp;!%%***&amp;amp;((&amp;#39;&amp;quot;
    # to
    # &quot;&#39;***&amp;!%%***&amp;((&#39;&quot;
    #
    #sOrig   = '&#39;*g$fh%bA%Yt&#39;'
    #sWant   = 'Tung6550Sol'
    ##
    #sGot    = getYahooHtmlDecrypted( sOrig )
    ##
    #if sGot != sWant:
        ##
        #print3( 'want: ', sWant )
        #print3( 'got:  ', sGot  ) 
        #lProblems.append( 'getYahooHtmlDecrypted()' )
        ##
    ##
    #sOrig   = '&#39;*g$fh%bA%Yt&#39;'.replace( '&', '&amp;' )
    #sWant   = 'Tung6550Sol'
    ##
    #sGot    = getYahooHtmlDecrypted( sOrig )
    ##
    #if sGot != sWant:
        ##
        #print3( 'want: ', sWant )
        #print3( 'got:  ', sGot  ) 
        #lProblems.append( 'getYahooHtmlDecrypted()' )
        ##
    ##
    #sOrig   = '&#39;_@Mpz5HxJ&quot;7&#39;'
    #sWant   = 'em8Bp3t$bnY'
    ##
    #sGot    = getYahooHtmlDecrypted( sOrig, bLite = False )
    ##
    #if sGot != sWant:
        ##
        #print3( 'want: ', sWant )
        #print3( 'got:  ', sGot  ) 
        #lProblems.append( 'getYahooHtmlDecrypted() not lite' )
        ##
    #
    s1 = 'abcde'
    s2 = 'ABCDEFG'
    #
    sWant   = 'aAbBcCdDeE'
    sGot = _getAlternatingChars( s1, s2 )
    #
    if sGot != sWant:
        #
        print3( 'want: ', sWant )
        print3( 'got:  ', sGot  ) 
        lProblems.append( '_getAlternatingChars( s1, s2 )' )
        #
    #
    s2 = 'ABCDEFGhIjKlMnOp'
    #
    sGot = _getAlternatingChars( s1, s2 )
    #
    if sGot != sWant:
        #
        print3( 'want: ', sWant )
        print3( 'got:  ', sGot  ) 
        lProblems.append( '_getAlternatingChars( s1, s2 longer )' )
        #
    #
    sGot = _getFirstCharThenAlternate( s2 )
    #
    sWant   = 'ACEGIKMO'
    #
    if sGot != sWant:
        #
        print3( 'want: ', sWant )
        print3( 'got:  ', sGot  ) 
        lProblems.append( '_getFirstCharThenAlternate( s2 )' )
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
    if (    _getThisUnShifted( 124, 92 ) !=  32 or
            _getThisUnShifted( 125, 93 ) !=  32 or
            _getThisUnShifted( 126, 94 ) !=  32 or
            _getThisUnShifted(  32,  0 ) !=  32 or
            _getThisUnShifted(  33,  1 ) !=  32 or
            _getThisUnShifted(  34,  2 ) !=  32 or
            _getThisUnShifted(  35,  3 ) !=  32 ):
        #
        lProblems.append( '_getThisUnShifted( various, 92 - 98 )' )
        #
    #
    if (    _getThisUnShifted(  35,  0 ) !=  35 or
            _getThisUnShifted(  35,  1 ) !=  34 or
            _getThisUnShifted(  35,  2 ) !=  33 or
            _getThisUnShifted(  35,  3 ) !=  32 or
            _getThisUnShifted(  35,  4 ) != 126 or
            _getThisUnShifted(  35,  5 ) != 125 or
            _getThisUnShifted(  35,  6 ) != 124 ):
        #
        lProblems.append( '_getThisUnShifted( 35, various )' )
        #
    #
    sGreatPw = 'Gr34tP@55w0rd'
    #
    if Decrypt( Encrypt( sGreatPw ) ) != sGreatPw:
        #
        lProblems.append( 'encrypt/decrypt great password' )
        #
    #
    if DecryptLite( EncryptLite( sGreatPw ) ) != sGreatPw:
        #
        lProblems.append( 'encrypt lite /decrypt lite great password' )
        #
    #
    sayTestResult( lProblems )
