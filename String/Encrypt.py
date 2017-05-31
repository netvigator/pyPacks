#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# string functions Encrypt
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
# Copyright 2004-2017 Rick Graves
#
'''
sTest                = 'The quick brown fox jumped over the lazy dog.'

Encrypt( sTest )     = '\x1ffPrTvWgW.EkW{~pGoLg#hR&DbMqJiZ&Nz!V#gMt\x1fuFx#'

EncryptLite( sTest ) = 'Y=REjqRp=KurB=cVRbgIelZhuS{bOMhDG=t==nW==ABqX'

XOREncrypt( sTest )  = '3c0d094c1e1d0c0f074f0a17031b01480303144f0210' +
                       '011c0a0c45031a0a1a4518040a48090d16164801030b41'

getRot13( sTest )    = 'Gur dhvpx oebja sbk whzcrq bire gur ynml qbt.'

'''

from string             import punctuation, digits

from Collect.Cards      import ShuffleAndCut
from String.Replace     import getTextReversed
from String.Transform   import TranslatorFactory

sSafe   =  punctuation.replace( '\\', ' ' ) + digits

changePunct = TranslatorFactory( sSafe, getTextReversed( sSafe ) )



def DescendChars( sOrig,
        iOffset         = False,
        bStepIncrement  = False,
        bBackStep       = False,
        bBackwards      = False ):
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





def Encrypt( sEncryptThis, bUnEncrypt = False ):
    #
    from String.Stats   import AscStats
    #
    if bUnEncrypt:
        #
        sConverted  = DescendChars( FlipCase( sEncryptThis, True ), 0, 1 )
        #
    else: # Encrypt
        #
        # sConverted   = sEncryptThis
        sConverted  = ShuffleAndCut(
                        getTextReversed( ShuffleAndCut( sEncryptThis ) ) )
        #
    #
    oStats          = AscStats( sConverted )
    #
    iUseOffset      = ( oStats.iLength % 4 ) - ( oStats.iDifference % 8 )
    #
    sConverted      = DescendChars( sConverted, iUseOffset )
    #
    if bUnEncrypt:
        #
        # pass
        sConverted  = ShuffleAndCut(
                        getTextReversed( ShuffleAndCut( sConverted, 1 ) ), 1 )
        #
    else: # Encrypt
        #
        sConverted  = FlipCase( DescendChars( sConverted, 0, 1 ), True )
        #
    #
    #
    #
    return sConverted



def Decrypt( sThis ):
    #
    return Encrypt( sThis, bUnEncrypt = True )




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



def EncryptLite( sThis ):
    #
    sConverted  = ShuffleAndCut(
                    getRot13(
                        getTextReversed(
                            FlipCase(
                                changePunct( sThis ), True ) ) ) )
    #
    return sConverted



def DecryptLite( sThis ):
    #
    sConverted  = changePunct(
                    FlipCase(
                        getTextReversed(
                            getRot13(
                                ShuffleAndCut( sThis, 1 ) ) ), True ) )
    #
    return sConverted




def getYahooHtmlDecrypted( s, bLite = True ):
    #
    '''
    default is lite
    pass False as 2nd param to use heavy
    '''
    from Web.HTML import getTextgotYahooHTML
    #
    sFixed = getTextgotYahooHTML( s )
    #
    # sFixed = sFixed[ 1 : ][ 0 : -1 ] # strip quote chars
    #
    sFixed = sFixed.replace( "\\", '' ) # don't want \ chars
    #
    if bLite:
        fDecription = DecryptLite
    else:
        fDecription = Decrypt
    #
    
    return fDecription( sFixed )




if __name__ == "__main__":
    #
    from string         import digits
    from string         import ascii_letters   as letters
    from string         import ascii_lowercase as lowercase
    from string         import ascii_uppercase as uppercase
    #
    from six            import print_ as print3
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
    sTest = 'The cat in the hat.'
    #
    if      Encrypt( Encrypt( sTest ), bUnEncrypt = True ) != sTest or \
                     Encrypt( sTest ) == sTest:
        #
        lProblems.append( 'Encrypt( "%s" )' % sTest )
        #
    if      DecryptLite( EncryptLite( sTest ) ) != sTest or \
                         EncryptLite( sTest )   == sTest:
        #
        lProblems.append( 'EncryptLite( "%s" )' % sTest )
        #
    if Decrypt( Encrypt( sTest ) ) != sTest:
        #
        lProblems.append( 'Decrypt( "%s" )' % sTest )
        #
    if DecryptLite( EncryptLite( sTest ) ) != sTest:
        #
        lProblems.append( 'DecryptLite( "%s" )' % sTest )
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
    # &#39;*g$fh%bA%Yt&#39;
    # to
    # Tung6550Sol
    #
    # also need to convert
    # &amp;quot;&amp;#39;***&amp;amp;!%%***&amp;amp;((&amp;#39;&amp;quot;
    # to
    # &quot;&#39;***&amp;!%%***&amp;((&#39;&quot;
    #
    sOrig   = '&#39;*g$fh%bA%Yt&#39;'
    sWant   = 'Tung6550Sol'
    #
    sGot    = getYahooHtmlDecrypted( sOrig )
    #
    if sGot != sWant:
        #
        print3( 'want: ', sWant )
        print3( 'got:  ', sGot  ) 
        lProblems.append( 'getYahooHtmlDecrypted()' )
        #
    #
    sOrig   = '&#39;*g$fh%bA%Yt&#39;'.replace( '&', '&amp;' )
    sWant   = 'Tung6550Sol'
    #
    sGot    = getYahooHtmlDecrypted( sOrig )
    #
    if sGot != sWant:
        #
        print3( 'want: ', sWant )
        print3( 'got:  ', sGot  ) 
        lProblems.append( 'getYahooHtmlDecrypted()' )
        #
    #
    sOrig   = '&#39;_@Mpz5HxJ&quot;7&#39;'
    sWant   = 'em8Bp3t$bnY'
    #
    sGot    = getYahooHtmlDecrypted( sOrig, bLite = False )
    #
    if sGot != sWant:
        #
        print3( 'want: ', sWant )
        print3( 'got:  ', sGot  ) 
        lProblems.append( 'getYahooHtmlDecrypted() not lite' )
        #
    #
    sayTestResult( lProblems )