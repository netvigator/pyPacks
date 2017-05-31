#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions Test
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

from String.Transform   import getTranslatorStr
from String.Dumpster    import KeepDotsDigitsClass

sHexQuadDigitsOnly  = getTranslatorStr( '0123456789abcdefxABCDEFX'  )
sHexQuadDigitsDots  = getTranslatorStr( '0123456789abcdefxABCDEFX.' )

oKeepDotsDigits     = KeepDotsDigitsClass()

class Failure( Exception ): pass

class InRangeDotQuadBaseClass( list ):
    #

    def getHostsForISP( self ):
        #
        from Iter.AllVers import iMap
        #
        lQuads  = self.getExampleQuadList()
        #
        lHosts  = iMap( getHostName, lQuads )
        #
        return RemoveDupes( lHosts )

    def getExampleQuad( self, iStart = None ):
        #
        from Web.Quads import getDotQuadFromValue
        #
        if iStart is None:
            #
            if self.hasAnyDotQuad():
                #
                iStart  = self[0]
                #
            else:
                #
                iStart  = 0
                #
        #
        sQuad   = getDotQuadFromValue( iStart + 88 )
        #
        return sQuad

    def getExampleQuadList( self ):
        #
        from Collect.Get    import getValueIterOffItems as getValues
        from Iter.AllVers   import iFilter, lMap
        from Numb.Test      import isEven
        #
        def EvenOnly( t ): return isEven( t[0] )
        #
        lStarts = getValues( iFilter( EvenOnly, enumerate( self ) ) )
        #
        return lMap( self.getExampleQuad, lStarts )


class InRangeDotQuadClass( InRangeDotQuadBaseClass ):
    #
    """This class holds one or more pairs of begin/end DotQuadresses
    in a single list.  The list is in order, smallest to biggest.
    First in the list (position 0) would be the start of the first range,
    and next (position 1) would be the after the end of the first range.
    And so on.  If a DotQuad to be tested would fall between 0 and 1,
    the bisect function would insert it in position 1.
    See the Python page on bisect.
    So if bisect returns 1 or another odd number, the DotQuad to be tested
    would fall within a begin/end pair -- in a range.  If bisect returns 0
    or an even number, the DotQuad to be tested would fall outside a
    begin/end pair -- outside of a range.
    """
    #
    def __init__( self, sDotQuadRangeOK ):
        #
        from Iter.AllVers import lMap
        from Web.Quads import getDotQuad4Sort, getClassCNetBegEnd, \
                            getClassCNetRangeBegEnd
        #
        lDotQuadRanges = sDotQuadRangeOK.replace( ' ', '' ).split( ',' )
        #
        lDotQuadRanges = lMap( getDotQuad4Sort, lDotQuadRanges )
        #
        lDotQuadRanges.sort()
        #
        #
        for sThisRange in lDotQuadRanges:
            #
            sBeg, sEnd = '', ''
            #
            if '-' in sThisRange:  # explicity range
                #
                lBegEnd = sThisRange.split( '-' )
                #
                if      len( lBegEnd ) == 2 and \
                        isDotQuad( lBegEnd[ 0 ] ) and isDotQuad( lBegEnd[ -1 ] ):
                    #
                    sBeg, sEnd = getClassCNetRangeBegEnd( lBegEnd[ 0 ], lBegEnd[ -1 ] )
                    #
                #
            else:                           # implied Class C range
                #
                if isDotQuad( sThisRange ):
                    #
                    sBeg, sEnd = getClassCNetBegEnd( sThisRange )
                    #
            #
            if sBeg and sEnd:
                #
                self._addRange( sBeg, sEnd )


    def _addRange( self, sBeg, sEnd ):
        #
        from bisect     import bisect_right, insort_right
        from Numb.Test  import isEven
        from Web.Quads  import getQuadValue
        #
        iBeg4Sort   = getQuadValue( sBeg )
        iEnd4Sort   = getQuadValue( sEnd ) + 1
        #
        if iEnd4Sort == 0: sEnd4Sort = getQuadValue( '255.255.255.256' ) # fudge
        #
        iBegInsert  = bisect_right( self, iBeg4Sort )
        iEndInsert  = bisect_right( self, iEnd4Sort )
        #
        if      isEven( iBegInsert ) and isEven( iEndInsert ) and \
                iBegInsert == iEndInsert:
            #
            insort_right( self, iBeg4Sort )
            insort_right( self, iEnd4Sort )


    def hasAnyDotQuad( self ):
        #
        return bool( self )


    def isQuadInRange( self, sDotQuad ):
        #
        from bisect     import bisect_right
        from Web.Quads  import getQuadValue
        from Numb.Test  import isOdd
        #
        return isOdd( bisect_right( self, getQuadValue( sDotQuad ) ) )


    def getRanges( self ):
        #
        # lBegEnd = m@p( getDotQuadFromDotQuad4Sort, self )
        #
        from Iter.AllVers   import iMap, iRange, iZip
        from Web.Quads  import getDotQuadFromValue as getQ
        #
        iLen    = len( self )
        #
        lBegs   = iMap( getQ, [ self[i]     for i in iRange( 0, iLen, 2 ) ] )
        lEnds   = iMap( getQ, [ self[i] - 1 for i in iRange( 1, iLen, 2 ) ] )
        #
        lQuadRanges = [ '%s-%s' % t for t in iZip( lBegs, lEnds ) ]
        #
        return ','.join( lQuadRanges )




class DotQuadOKClass( InRangeDotQuadBaseClass ):
    #
    """Polymorphic substitute for InRangeDotQuadClass
    when looking for one and only one DotQuad."""
    #
    def __init__( self, sDotQuad = None ):
        #
        from Web.Quads      import getDotQuad
        #
        self.sDotQuad = getDotQuad( sDotQuad )

    def isQuadInRange( self, sDotQuad ):
        #
        from Web.Quads      import getDotQuad
        #
        return  isDotQuad( sDotQuad ) and \
                getDotQuad( sDotQuad, bOverOK = True ) == self.sDotQuad

    def hasAnyDotQuad( self ):
        #
        return isDotQuad( self.sDotQuad )

    def getRanges( self ):
        #
        return self.sDotQuad

    def getExampleQuad( self, iStart = None ):
        #
        return self.sDotQuad


def getDotQuad4IspTester( sOKDotQuad4ThisISP ):
    #
    if ',' in sOKDotQuad4ThisISP or '-' in sOKDotQuad4ThisISP:
        #
        # got a range for this ISP
        #
        oDotQuads4ISP   = InRangeDotQuadClass( sOKDotQuad4ThisISP )
        #
    else:
        #
        oDotQuads4ISP   = DotQuadOKClass(      sOKDotQuad4ThisISP )
        #
    #
    return oDotQuads4ISP




def _isQuadValueWithinValidRange( iInteger ):
    return 0 <= iInteger < 256


def _areInValidDotQuadRange( tDotQuad, bOverOK = False ):
    #
    from Collect.Test       import AllMeet
    #
    if bOverOK:
        #
        return (
            AllMeet( tDotQuad[ 1 : ], _isQuadValueWithinValidRange ) and
                     tDotQuad[ 0 ] < 257                             and
                   ( tDotQuad[ 0 ] < 256 or tDotQuad[ -1 ] == 0 ) )
    else:
        #
        return AllMeet( tDotQuad, _isQuadValueWithinValidRange )



def _areDotQuadEndsValid( tDotQuad, bExtremesOK = False ):
    #
    lBothEnds = ( tDotQuad[0], tDotQuad[3] )
    #
    return bExtremesOK or not ( 0 in lBothEnds or 255 in lBothEnds )



def isDotQuadNotLocal( tDotQuad ):
    #
    bLocal  = \
        tDotQuad[0] == 10  or \
        tDotQuad[0] == 127 or \
        ( tDotQuad[0] == 172 and tDotQuad[1] >= 16 and tDotQuad[1] <= 32 ) or \
        ( tDotQuad[0] == 192 and tDotQuad[1] == 168 )
    #
    return not bLocal




def _isValidQuad( sDotQuad,
        bLocalDotQuadOK = True, bExtremesOK = True, bOverOK = False, bIsDotQuad = False, bIsHexQuad = False ):
    #
    from Web.Quads      import getQuadTuple
    #
    tDotQuad            = getQuadTuple( sDotQuad, bIsDotQuad = bIsDotQuad, bIsHexQuad = bIsHexQuad )
    #
    bValidDotQuad       = False
    #
    if len( tDotQuad ) == 4:
        #
        bValidDotQuad   = (
                _areInValidDotQuadRange( tDotQuad, bOverOK       ) and
                (   bExtremesOK     or
                    _areDotQuadEndsValid(tDotQuad, bExtremesOK ) ) and
                (   bLocalDotQuadOK or
                    isDotQuadNotLocal(   tDotQuad ) ) )
    #
    return bValidDotQuad


def isDotQuadValid( sDotQuad, bLocalDotQuadOK = True, bExtremesOK = True, bOverOK = False ):
    #
    # used in external programs
    #
    return _isValidQuad( sDotQuad, bLocalDotQuadOK, bExtremesOK, bOverOK, bIsDotQuad = True )



def hasDotQuad( s, bLocalDotQuadOK = True, bExtremesOK = True, bOverOK = False ):
    #
    """
    Tests whether there is a dot quad in a string.
    """
    #
    from Collect.Query import get1stThatMeets
    #
    def isValidQuad( s ):
        #
        return _isValidQuad( s,
                    bLocalDotQuadOK = bLocalDotQuadOK,
                    bExtremesOK     = bExtremesOK,
                    bOverOK         = bOverOK,
                    bIsDotQuad      = True )
    #
    sTestThis   = oKeepDotsDigits.Dump( s )
    #
    return bool( get1stThatMeets( sTestThis.split(), isValidQuad ) )




def isValidNonLocalQuad( sAnyQuad ):
    #
    return _isValidQuad( sAnyQuad, bLocalDotQuadOK = False )



def isDotQuad( sMayBeDotQuad, bLocalDotQuadOK = True, bExtremesOK = True, bOverOK = False ):
    #
    from Web.Quads import getDotQuad
    #
    return getDotQuad( sMayBeDotQuad, bLocalDotQuadOK, bExtremesOK, bOverOK )


def isHexQuad( sAnyQuad, bFormCheckOnly = False ):
    #
    from Iter.AllVers import iMap
    #
    bOK = False # if it looks like a dot quad, it probably is a dot quad
    #
    if not isDotQuad( sAnyQuad, bLocalDotQuadOK = True, bExtremesOK = True ):
        #
        iAnyQuadLen = len( sAnyQuad )
        #
        bGotX       = sAnyQuad.lower().count( 'x' ) == 4
        #
        iMaxLen     = max( iMap( len, sAnyQuad.split( '.' ) ) )
        #
        bOK =   (   (   hasHexQuadDigitsOnly( sAnyQuad ) and
                        (   (     bGotX and iAnyQuadLen >= 12 and iAnyQuadLen <= 16 ) or
                            ( not bGotX and iAnyQuadLen >=  4 and iAnyQuadLen <=  8 ) ) )
                    or
                    (   hasHexQuadDigitsDots( sAnyQuad ) and
                        (   (     bGotX and iAnyQuadLen >= 15 and iAnyQuadLen <= 19 ) or
                            ( not bGotX and iAnyQuadLen >=  7 and iAnyQuadLen <= 11 ) ) ) )
        #
        bOK = bOK and (
                bFormCheckOnly or
                _isValidQuad( sAnyQuad, bLocalDotQuadOK = True, bExtremesOK = True, bIsHexQuad = True ) )
        #
    #
    return bOK
#
#


def isInPortRange( iPortMaybe ):
    #
    return iPortMaybe >= 0 and \
           iPortMaybe <  65536


def isPort( uShouldBePort ):
    #
    sShouldBePort    = str( uShouldBePort )
    #
    return sShouldBePort.isdigit() and isInPortRange( int( sShouldBePort ) )


def isDotQuadWithPort( uMayBeDotQuad, bLocalOK = True ):
    #
    if type( uMayBeDotQuad ) == tuple:
        #
        lParts = uMayBeDotQuad
        #
    else:
        #
        lParts = uMayBeDotQuad.split( ':' )
        #
    #
    return len( lParts ) == 2 and \
            isPort( lParts[ 1 ] ) and \
            _isValidQuad( lParts[ 0 ], bLocalDotQuadOK = bLocalOK )



def isNonLocalDotQuadWithPort( uMayBeDotQuad ):
    #
    return isDotQuadWithPort( uMayBeDotQuad, bLocalOK = False )



def isDotQuadPortTuple( tDotQuadPort ):
    #
    bIsDotQuadPortTuple        = False
    #
    if type( tDotQuadPort ) == tuple and len( tDotQuadPort ) == 2:
        #
        #
        bIsDotQuadPortTuple    = isPort( tDotQuadPort[ 1 ] ) and isDotQuad( tDotQuadPort[ 0 ] )
        #
    #
    return bIsDotQuadPortTuple



def isDotQuadPortAfterCleanup( s ):
    #
    from String.Test        import hasDigitAndDot
    from String.Eat         import eatPunctuationBegAndEnd
    #
    bDotQuadPort        = False
    #
    if hasDigitAndDot( s ):
        #
        bDotQuadPort    = isDotQuadWithPort( eatPunctuationBegAndEnd( s ) )
    #
    return bDotQuadPort




def hasDotQuadWithPort( sMaybeIP ):
    #
    """
    returns True if text contains any DotQuad with Port
    """
    #
    from Collect.Query import get1stThatMeets
    #
    return bool(
            get1stThatMeets(
                sMaybeIP.split(), isDotQuadPortAfterCleanup ) )




def hasDomainNameValidCharsOnly( sDomainName ):
    #
    from string import digits
    from string import ascii_lowercase as lowercase
    #
    from String.Transform import getSpacesForChars
    #
    if ' ' in sDomainName: return False
    #
    sDomainName = sDomainName.lower()
    #
    sSpaces     = getSpacesForChars( sDomainName, lowercase + digits + '-.+' )
    #
    sWhatsLeft  = sSpaces.replace( ' ', '' )    # get rid of spaces
    #
    return not sWhatsLeft



def _allDomainNameTests( sDomainName ):
    #
    from Web.Address import setTopLevelDomains, setMiniDomains
    from Web.Country import dCountryCodes
    #
    if not hasDomainNameValidCharsOnly( sDomainName ):
        #
        raise Failure
    #
    tParts      = tuple( sDomainName.split('.') )
    #
    if len( tParts ) < 2:
        #
        raise Failure
    #
    for sPart in tParts:
        #
        if len( sPart ) == 0:
            #
            raise Failure
    #
    if tParts[-1]:
        #
        if not tParts[-1][0].isalpha() or len( tParts[-1] ) < 2:
            #
            raise Failure
            #
        #
    #
    #if not tParts[-2][0].isalpha(): # 163.com is OK
        ##
        #raise Failure
    #
    if not (    tParts[-1] in setTopLevelDomains or
                tParts[-1] in dCountryCodes ):
        #
        raise Failure
        #
    #
    if  (   False and
            len( tParts ) > 2           and
            tParts[-1] in dCountryCodes and not
            ( tParts[-2] in setTopLevelDomains or
              tParts[-2] in setMiniDomains ) ):
        #
        # cannot catch these,
        # there are too many countries doing various naming schemes
        #
        raise Failure
        #
    #
    iBaseName = -2
    #
    if      tParts[-1] in dCountryCodes and \
          ( tParts[-2] in setTopLevelDomains or tParts[-2] in setMiniDomains ) and \
            len( tParts ) > 2:
        #
        iBaseName = -3
    #
    sBaseName = tParts[ iBaseName ]
    #
    if len( sBaseName ) > 63:
        #
        raise Failure
    #
    if sBaseName.startswith( '-' ) or sBaseName.endswith( '-' ):
        #
        raise Failure
    #
    return


def isDomainName( sDomainName ):
    #
    #
    try:
        #
        _allDomainNameTests( sDomainName )
        #
    except Failure:
        #
        bisDomainName  = False
        #
    else:
        #
        bisDomainName  = True
    #
    return bisDomainName



def isDomainNameOrDotQuad( sMayBe ):
    #
    return isDotQuad( sMayBe ) or isDomainName( sMayBe )



def isDomainNameOrDotQuadWithPort( sMayBe ):
    #
    bisDomainNameOrDotQuadWithPort  = False
    #
    lParts = sMayBe.split( ':' )
    #
    if len( lParts ) == 2 and isPort( lParts[ 1 ] ):   # easy ones
        #
        if isDotQuad( lParts[ 0 ] ) or isDomainName( lParts[ 0 ] ):
            #
            bisDomainNameOrDotQuadWithPort  = True
    #
    return bisDomainNameOrDotQuadWithPort



def hasAt( sFrag ): return '@' in sFrag



def isURL( sURL, bAnySchemeOK = True, bSecureHttpOK = True, bNoSchemeOK = False ):
    #
    from Web.Address    import UrlSplitMore
    from eMail.Test     import isEmailAddress
    #
    sScheme, sUser, sPassword, sHost, sPort, sPath, sQuery, sFragmentID = \
        UrlSplitMore( sURL )
    #
    return  isDomainName( sHost ) and \
            ( sScheme.startswith( 'http' ) or bAnySchemeOK ) and \
            ( sScheme or
                ( bNoSchemeOK and not sScheme and not isEmailAddress( sURL ) ) )


def isLazyURL( sURL, bAnySchemeOK = True, bSecureHttpOK = True ):
    #
    '''a Lazy URL would be python.org
    function also returns True for non-lazy URLs
    '''
    return isURL(   sURL,
                    bAnySchemeOK  = bAnySchemeOK,
                    bSecureHttpOK = bSecureHttpOK,
                    bNoSchemeOK   = True )


def isHttpURL( sURL, bSecureHttpOK = False  ):
    #
    return isURL( sURL, bAnySchemeOK = False ) == 'http'



def isStartsWithHTTP( sHTML ): return sHTML.startswith( 'http://' )



def hasHexQuadDigitsOnly( sMaybeHexQuad ):
    #
    from Utils.Both2n3 import translate
    #
    return translate( sMaybeHexQuad, sHexQuadDigitsOnly ).strip() == ''
#
#
def hasHexQuadDigitsDots( sMaybeHexQuad ):
    #
    from Utils.Both2n3 import translate
    #
    return translate( sMaybeHexQuad, sHexQuadDigitsDots ).strip() == ''
#
#


if __name__ == "__main__":
    #
    from six            import print_ as print3
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    oDotRange = InRangeDotQuadClass(
                    '8.88.0.0 - 8.188.255.255, 18.8.8.0 - 18.8.18.255' )
    #
    if      not oDotRange.hasAnyDotQuad() or \
            not oDotRange.isQuadInRange( '8.188.8.188' ) or \
            not oDotRange.isQuadInRange( '18.8.18.188' ) or \
                oDotRange.isQuadInRange( '8.8.188.188' ) or \
                oDotRange.getRanges() != \
                    '8.88.0.0-8.188.255.255,18.8.8.0-18.8.18.255':
        #
        print3( 'oDotRange.hasAnyDotQuad():', oDotRange.hasAnyDotQuad() )
        print3( "oDotRange.isQuadInRange( '8.188.8.188' ):", oDotRange.isQuadInRange( '8.188.8.188' ) )
        print3( "oDotRange.isQuadInRange( '18.8.18.188' ):", oDotRange.isQuadInRange( '18.8.18.188' ) )
        print3( "oDotRange.isQuadInRange( '8.8.188.188' ):", oDotRange.isQuadInRange( '8.8.188.188' ) )
        print3( 'oDotRange.getRanges():', oDotRange.getRanges() )
        lProblems.append( 'InRangeDotQuadClass()' )
        #
    #
    oDotQuad = DotQuadOKClass( '18.18.18.18' )
    #
    if      not oDotQuad.hasAnyDotQuad() or \
            not oDotQuad.isQuadInRange( '18.18.18.18' ) or \
                oDotQuad.isQuadInRange( '8.8.188.188' ) or \
                oDotQuad.getRanges() != '18.18.18.18':
        #
        lProblems.append( 'DotQuadOKClass()' )
        #
    if  (       _areInValidDotQuadRange( ( 255,255,255,256 )       ) or
            not _areInValidDotQuadRange( (   0,  0,  0,  0 )       ) or
            not _areInValidDotQuadRange( ( 192,168,188,188 )       ) or
                _areInValidDotQuadRange( ( 256,255,255,255 ), True ) or
            not _areInValidDotQuadRange( ( 256,255,255,  0 ), True ) ):
        #
        # bOverOK
        #
        lProblems.append( '_areInValidDotQuadRange()' )
        #
    if  (       _areDotQuadEndsValid( ( 255,255,255,255 )       ) or
                _areDotQuadEndsValid( (   0,  0,  0,  0 )       ) or
            not _areDotQuadEndsValid( ( 254,255,255,  0 ), True ) or
            not _areDotQuadEndsValid( ( 254,255,255,255 ), True ) or
            not _areDotQuadEndsValid( ( 255,255,255,  0 ), True ) or
            not _areDotQuadEndsValid( ( 255,255,255,255 ), True ) ):
        #
        # bExtremesOK
        #
        lProblems.append( '_areDotQuadEndsValid()' )
        #
    #
    #
    if      not _isValidQuad( '0xbc0xbc0x80x12', bIsHexQuad = True ) or \
            not _isValidQuad( 'bcbc0812',        bIsHexQuad = True ) or \
            not _isValidQuad( 'bc.bc.8.12',      bIsHexQuad = True ) or \
            not _isValidQuad( '188.148.8.18',    bIsDotQuad = True ) or \
                _isValidQuad( 'www.python.org',  bIsDotQuad = True ) or \
                _isValidQuad( '188.188.8.256',   bIsDotQuad = True ) or \
                _isValidQuad( '256.255.255.255'):
        #
        lProblems.append( '_isValidQuad()' )
        #
    #
    if  (       isDotQuadNotLocal( (  10,  0,  0,  1 ) ) or
                isDotQuadNotLocal( ( 127,  0,  0,  1 ) ) or
                isDotQuadNotLocal( ( 172, 16,  0,  1 ) ) or
                isDotQuadNotLocal( ( 172, 32,  0,  1 ) ) or
                isDotQuadNotLocal( ( 192,168,  0,  1 ) ) or
            not isDotQuadNotLocal( ( 188, 88, 88, 88 ) ) or
            not isDotQuadNotLocal( ( 172, 15,  0,  1 ) ) or
            not isDotQuadNotLocal( ( 172, 33,  0,  1 ) ) ):
        #
        lProblems.append( 'isDotQuadNotLocal()' )
        #
    if  (   not isDotQuadValid( '192.168.8.188', bLocalDotQuadOK = True  ) or
            not isDotQuadValid( '188.188.8.255', bExtremesOK     = True  ) or
            not isDotQuadValid( '256.000.0.000', bOverOK         = True  ) or
            not isDotQuadValid( '188.188.8.188', bLocalDotQuadOK = False ) or
            not isDotQuadValid( '188.188.8.188', bExtremesOK     = False ) or
                isDotQuadValid( '188.188.8.256', bExtremesOK     = False ) or
                isDotQuadValid( '192.168.8.188', bLocalDotQuadOK = False ) or
                isDotQuadValid( '256.000.0.000', bOverOK         = False ) ):
        #
        lProblems.append( 'isDotQuadValid()' )
        #
    #
    if      not hasDotQuad( 'abc 192.168.8.188; xyz' ) or \
                hasDotQuad( 'abc                xyz' ):
        #
        lProblems.append( 'hasDotQuad()' )
        #
    #
    if      not isValidNonLocalQuad( '188.188.8.255' ) or \
                isValidNonLocalQuad( '192.168.8.188' ):
        #
        lProblems.append( 'isValidNonLocalQuad()' )
        #
    if  (   not isDotQuad( '192.168.8.188', bLocalDotQuadOK = True  ) or
            not isDotQuad( '188.188.8.255', bExtremesOK     = True  ) or
            not isDotQuad( '256.000.0.000', bOverOK         = True  ) or
            not isDotQuad( '188.188.8.188', bLocalDotQuadOK = False ) or
            not isDotQuad( '188.188.8.188', bExtremesOK     = False ) or
                isDotQuad( '188.188.8.256', bExtremesOK     = False ) or
                isDotQuad( '192.168.8.188', bLocalDotQuadOK = False ) or
                isDotQuad( '256.000.0.000', bOverOK         = False ) ):
        #
        lProblems.append( 'isDotQuad()' )
        #
    if      not isHexQuad( '0xbc0xbc0x80x12' ) or \
            not isHexQuad( 'bc.bc.8.12'      ) or \
                isHexQuad( '192.168.8.188'   ):
        #
        lProblems.append( 'isHexQuad()' )
        #
    if      not isInPortRange(     0 ) or \
            not isInPortRange(   256 ) or \
            not isInPortRange( 65535 ) or \
                isInPortRange( 65536 ):
        #
        lProblems.append( 'isInPortRange()' )
        #
    if      not isPort(     '0' ) or \
            not isPort( '65535' ) or \
                isPort(   'abc' ) or \
                isPort(    '-1' ):
        #
        lProblems.append( 'isPort()' )
        #
    if      not isDotQuadWithPort( '192.168.8.88:8000' ) or \
                isDotQuadWithPort( '192.168.8.88' )      or \
            not isDotQuadWithPort( ('192.168.8.88',8000) ) or \
                isDotQuadWithPort( ('192.168.8.88',) ):
        #
        lProblems.append( 'isDotQuadWithPort()' )
        #
    if          isNonLocalDotQuadWithPort( '192.168.8.88:8000' ) or \
                isNonLocalDotQuadWithPort( '192.168.8.88' )         or \
            not isNonLocalDotQuadWithPort( '200.168.8.88:8000' ) or \
                isNonLocalDotQuadWithPort( '200.168.8.88' )         or \
                isNonLocalDotQuadWithPort( ('192.168.8.88',8000) ) or \
                isNonLocalDotQuadWithPort( ('192.168.8.88',) )     or \
            not isNonLocalDotQuadWithPort( ('200.168.8.88',8000) ) or \
                isNonLocalDotQuadWithPort( ('200.168.8.88',) ):
        #
        lProblems.append( 'isNonLocalDotQuadWithPort()' )
        #
    if      not isDotQuadPortTuple( ( '192.168.8.88',8000 ) ) or \
                isDotQuadPortTuple( ( 'abc', 'def' ) ):
        #
        lProblems.append( 'isDotQuadPortTuple()' )
        #
    #
    sOne = 'abc def 123 192.168.8.88:8000 xyz ABC 8888'
    sTwo = 'abc 192.168.8.88 def 123 8000 xyz ABC 8888'
    #
    if      not hasDotQuadWithPort( sOne ) or \
                hasDotQuadWithPort( sTwo ):
        #
        lProblems.append( 'hasDotQuadWithPort()' )
        #
    if      not hasDomainNameValidCharsOnly( 'www.python.org' ) or \
                hasDomainNameValidCharsOnly( '!@#$%^&*()_-=;' ):
        #
        lProblems.append( 'hasDomainNameValidCharsOnly()' )
        #
    if      not isDomainName( 'python.org' ) or \
                isDomainName( 'John Q. Public' ):
        #
        lProblems.append( 'isDomainName()' )
        #
    #
    if not  (   isDomainName( 'google.com.au'   ) and
                isDomainName( 'redcross.org.au' ) and
                isDomainName( 'abc.net.au'      ) and
                isDomainName( 'yahoo.co.uk'     ) and
                isDomainName( 'ait.ac.th'       ) and
                isDomainName( 'katsuki.ed.jp'   ) and
                isDomainName( 'neustar.us'      ) ):
        #
        lProblems.append( 'isDomainName( .au co.uk .ac.th .jp .us )' )
        #
    #
    if not isDomainName( 'google.dom.au' ):
        #
        # cannot catch this typo!
        #
        lProblems.append( 'isDomainName( google.dom.au )' )
        #
    #
    if      not isDomainNameOrDotQuad( 'python.org'    ) or \
            not isDomainNameOrDotQuad( '188.188.8.188' ) or \
                isDomainNameOrDotQuad( 'John Q. Public'):
        #
        lProblems.append( 'isDomainNameOrDotQuad()' )
        #
    if      not isDomainNameOrDotQuadWithPort( 'python.org:81'    ) or \
            not isDomainNameOrDotQuadWithPort( '188.188.8.188:81' ) or \
                isDomainNameOrDotQuadWithPort( 'python.org'       ) or \
                isDomainNameOrDotQuadWithPort( '188.188.8.188'    ) or \
                isDomainNameOrDotQuadWithPort( 'John Q. Public'   ):
        #
        lProblems.append( 'isDomainNameOrDotQuadWithPort()' )
        #
    if not hasAt( 'help@python.org' ) or hasAt( 'John Q. Public' ):
        #
        lProblems.append( 'hasAt()' )
        #
    if      not isURL( 'http://www.python.org/help/' ) or \
                isURL( 'John Q. Public' ):
        #
        lProblems.append( 'isURL()' )
        #
    if      not isHttpURL( 'http://www.python.org/help/' ) or \
                isHttpURL( 'https://www.python.org/help/' ) or \
                isHttpURL( 'ftp://www.python.org/help/' ) or \
                isHttpURL( 'John Q. Public' ):
        #
        lProblems.append( 'isHttpURL()' )
        #
    if      not isLazyURL( 'python.org/help/' ) or \
            not isLazyURL( 'python.org'       ) or \
                isLazyURL( '188.188.8.188'    ):
        #
        lProblems.append( 'isLazyURL()' )
        #
    if      not isStartsWithHTTP( 'http://www.python.org/help/' ) or \
                isStartsWithHTTP(        'www.python.org/help/' ):
        #
        lProblems.append( 'isStartsWithHTTP()' )
        #
    if      not hasHexQuadDigitsOnly( '0xbc0xbc0x80x100' ) or \
                hasHexQuadDigitsOnly( '188.188.8.188' ):
        #
        lProblems.append( 'hasHexQuadDigitsOnly()' )
        #
    if      not hasHexQuadDigitsDots( 'bc.bc.8.100'   ) or \
            not hasHexQuadDigitsDots( '188.188.8.188' ) :
        #
        lProblems.append( 'hasHexQuadDigitsDots()' )
        #
    #
    oDotQuads4IspMulti = \
        getDotQuad4IspTester(
            '58.136.48.0 - 58.136.48.255,'
            '58.136.93.0 - 58.136.93.255,'
            '58.136.102.0- 58.136.102.255,'
            '203.146.0.0 - 203.146.255.255' )
    #
    oDotQuads4IspSingle = getDotQuad4IspTester( '192.168.8.88' )
    #
    if      not oDotQuads4IspMulti.isQuadInRange( '58.136.48.88' ) or \
                oDotQuads4IspMulti.isQuadInRange( '58.136.98.88' ):
        #
        lProblems.append( 'getDotQuad4IspTester()' )
        #
    #
    if      not oDotQuads4IspSingle.isQuadInRange( '192.168.8.88' ) or \
                oDotQuads4IspSingle.isQuadInRange( '192.168.8.48' ):
        #
        lProblems.append( 'getDotQuad4IspTester()' )
        #
    #
    #
    sayTestResult( lProblems )