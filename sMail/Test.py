#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# SnailMail sMail functions Test
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
# Copyright 2010-2016 Rick Graves
#

#( oFinderStateName,
#  oFinderStateCode,
#  oFinderStateBoth,
# _oFinderNewYorkNY ) = _getStateFinders()

# Abbrev.py also has getStateFinder() and getStateCodeFinder()


from sMail.Abbrev   import dCodesProvAbbrevCA
from String.Find    import getFinder, getFinderFindAll, getSeqWordBounds

class Finished( Exception ): pass

_s1stLetterCodeCA = ''.join( dCodesProvAbbrevCA )

oPCodeFinderCA  = getFinderFindAll( 
                  r'\b[%s][\do][a-z][ -]?\w{3}\b' % _s1stLetterCodeCA )

oPOBoxFinder    = getFinder(
    r'\b(p.? *o.? *box *\d+|pob *\d+|box *\d+|pobox *\d+)' )

oCareOfFinder   = getFinderFindAll( r'\bc/?o |in care of|care of' )


def _getStateFinders():
    #
    from Collect.Get    import unZip
    from Dict.Get       import getValueIter
    from sMail.Abbrev   import tCodesStates
    #
    lCodes, lNames  = unZip( tCodesStates )
    #
    dStates = dict( tCodesStates )
    #
    dStates[ 'WA' ] = 'Washington(?!,? DC)'
    #
    sNames          = getSeqWordBounds( getValueIter( dStates ) )
    #
    sCodes          = getSeqWordBounds( lCodes )
    #
    oFinderStateName = getFinderFindAll( sNames )
    #
    oFinderStateCode = getFinderFindAll( sCodes )
    #
    oFinderStateBoth = getFinderFindAll( '%s|%s' % ( sCodes, sNames ) )
    #
    tNYC = ( 
        'New York',
        'NY',
        'NYC' )
    #
    oFinderNewYorkNY = getFinderFindAll( getSeqWordBounds( tNYC ) )
    #
    t = oFinderStateName, oFinderStateCode, oFinderStateBoth, oFinderNewYorkNY
    #
    return t


( oFinderStateName,
  oFinderStateCode,
  oFinderStateBoth,
 _oFinderNewYorkNY ) = _getStateFinders()


# Abbrev.py also has getStateFinder() and getStateCodeFinder()


# TimeTrial shows this tests is a little faster than Finder test
#hasValid = not (    '34002'  <= sZip <= '34099' or \
#                    '09001'  <= sZip <= '09898' or \
#                    '96201'  <= sZip <= '96698' )

isOverseasZip = \
    getFinderFindAll(
        '^'
        '(340(0[2-9]|[1-9]\d)|'
         '09(?:0(?:0[1-9]|[1-9]\d)|[1-7]\d{2}|8[0-8]\d|89[0-8])|'
         '96(?:6(?:[0-8]\d|9[0-8])|[3-5]\d{2}|2(?:0[1-9]|[1-9]\d)))',
        bCaseSensitive = True )


oPCodeStrictCA  = getFinderFindAll(
                  r'\b[%s]\d[A-Z] \d[A-Z]\d\b' % _s1stLetterCodeCA,
                  bCaseSensitive = True )


_oFindRR = getFinderFindAll( 'R.?R.?\d' )




def isOverseasZipOk2Drop0( s ):
    #
    if len( s ) == 4 and s.isdigit():
        #
        s = '0%s' % s
        #
    #
    return isOverseasZip( s )


def isZipCode( sZip, bMissingDashOK = True ):
    #
    from String.Get import getTextBefore
    #
    if type( sZip ) == int:
        #
        sZip5 = '%05d' % sZip
        #
    else:
        #
        sZip5 = str( sZip )
        #
    #
    if bMissingDashOK and ' ' in sZip5:
        #
        sZip5 = sZip5.replace( ' ', '-' )
        #
    #
    if '-' in sZip5: sZip5 = getTextBefore( sZip5, '-' )
    #
    try:
        #
        if len( sZip5 ) not in ( 5, 9 ): raise Finished
        #
        bZipCode = sZip5.isdigit()
        #
    except Finished:
        #
        bZipCode = False
        #
    #
    return bZipCode


def isNotZipCode( sZip ):
    #
    return not isZipCode( sZip )



def isZipPlus4( sZip ):
    #
    from String.Eat import eatAlphaOffEnd
    from String.Get import getTextAfter
    #
    sZip = eatAlphaOffEnd( ''.join( sZip.split() ) )
    #
    try:
        #
        if not ( '-' in sZip or ( len( sZip ) == 9 and sZip.isdigit() ) ):
            raise Finished
        #
        if not isZipCode( sZip ):   raise Finished
        #
        if '-' in sZip:
            sPlus4 = getTextAfter( sZip, '-' )
            bZipPlus4 = len( sPlus4 ) == 4 and sPlus4.isdigit()
        else:
            bZipPlus4 = True
        #
        #
    except Finished:
        #
        bZipPlus4 = False
        #
    #
    return bZipPlus4


def isNotZipPlus4( sZip ):
    #
    return not isZipPlus4( sZip )


def isOverseasZipStringTest( sZip, bLeadingZeroDropOK = True ):
    #
    # Armed Forces - Americas
    # Armed Forces - Europe
    # Armed Forces - Pacific
    #
    from sMail.Zips import putZerosBackInFront
    #
    if '-' in sZip:
        #
        lParts = sZip.split( '-' )
        #
        sZip = lParts[0].strip()
    #
    if bLeadingZeroDropOK and len( sZip ) < 5 and sZip.isdigit():
        #
        sZip = putZerosBackInFront( sZip )
        #
    #
    return  '34002'  <= sZip <= '34099' or \
            '09001'  <= sZip <= '09898' or \
            '96201'  <= sZip <= '96698'



def isZipInState( sZip, sState ):
    #
    from Utils.ImIf import ImIf
    #
    from sMail.Zips import dZipRange4State, dZipRange4Code
    #
    hasValid    = False
    #
    if sZip and sState and (
            sState in dZipRange4Code or
            sState in dZipRange4State ):
        #
        dStateZips  = ImIf(
            sState in dZipRange4State,
                dZipRange4State, dZipRange4Code )
        #
        dZipLimits = dStateZips.get( sState )
        #
        hasValid = dZipLimits['min' ] <= sZip <= dZipLimits['max' ]
        #
        if not hasValid and 'more' in dZipLimits:
            #
            for d in dZipLimits['more']:
                #
                hasValid = d['min' ] <= sZip <= d['max' ]
                #
                if hasValid:
                    break
                #
        #
    if hasValid:
        #
        hasValid = not isOverseasZipStringTest( sZip )
    #
    return hasValid



def isZipNotInState( sZip, sState ):
    #
    return not isZipInState( sZip, sState )


def _getExampleZips():
    #
    from Iter.AllVers import iRange
    #
    for i in iRange( 1, 100000 ):
        #
        sZip = '%05d-1234' % i
        #
        yield sZip


def _allZipsStringTest():
    #
    for sZip in _getExampleZips():
        #
        isOverseasZipStringTest( sZip )


def _allZipsFinderTest():
    #
    for sZip in _getExampleZips():
        #
        isOverseasZip( sZip )


def isPOBoxAddress( sAdd ):
    #
    from String.Dumpster import getAlphaNumClean
    #
    sAdd = getAlphaNumClean( sAdd )
    #
    return oPOBoxFinder.findall( sAdd )


def isResidenceAddress( sAdd ):
    #
    return not isPOBoxAddress( sAdd )



def _isZipLike( s, bDroppedLeadingZeroOK  ):
    #
    sTest = s.strip()
    #
    iLen = len( sTest )
    #
    iMinOK = 5 - int( bDroppedLeadingZeroOK )
    #
    return ( 5 >= iLen >= iMinOK ) and sTest.isdigit()



def isZipLike( s, bDroppedLeadingZeroOK = True ):
    #
    from Iter.AllVers     import tMap
    from String.Transform import StripString
    #
    bZipLike = 0
    #
    lParts = s.strip().split( '-' )
    #
    if len( lParts ) == 1:
        #
        bZipLike = _isZipLike( s, bDroppedLeadingZeroOK  )
        #
    elif len( lParts ) == 2:
        #
        tParts = tMap( StripString, lParts )
        #
        bZipLike = (
            _isZipLike( tParts[0], bDroppedLeadingZeroOK  ) and
            ( _isZipLike( tParts[1], bDroppedLeadingZeroOK  ) or not tParts[1] ) )
        #
    #
    return bZipLike



def isZipLikeStrict( s ):
    #
    return isZipLike( s, bDroppedLeadingZeroOK = False )



def isApoZip( s ):
    #
    from sMail.Zips import dApoZipCountry
    #
    lParts = s.split( '-' )
    #
    return lParts[0].strip() in dApoZipCountry



def isApoZipPlusNot4OK( s ):
    #
    from sMail.Zips import dApoZipCountry
    #
    return s in dApoZipCountry
    
    


def _getTestZips():
    #
    from random         import random, shuffle
    #
    from Dict.Get       import getKeyList
    from Iter.AllVers   import iRange
    from sMail.Zips     import dApoZipCountry
    #
    lTestZips = getKeyList( dApoZipCountry )
    #
    iApoZips = len( lTestZips )
    #
    for i in iRange( iApoZips ):
        #
        lTestZips[i] = '%s-1234' % lTestZips[i]
        #
    #
    while len( lTestZips ) < ( 10 * iApoZips ):
        #
        sZip = '%s-1234' % str( random() )[6:11]
        #
        if not ( isApoZip( sZip ) or isOverseasZipStringTest( sZip ) ):
            #
            lTestZips.append( sZip )
        #
    #
    shuffle( lTestZips )
    #
    return lTestZips, iApoZips



def _getApoCityStateZipFinder():
    #
    return getFinderFindAll(
            '(?:^| )'
           '((?:a|d|f)po,* +(a(?:a|e|(?:p|o)))*,* +.*\d{5}'
            '(?:-\d{4})*)' )


isApoCityStateZip = _getApoCityStateZipFinder()


def doesApoZipMatchCountry( sZip, sCountry ):
    #
    from sMail.Zips import getApoCountryOffZip
    #
    uCountry = getApoCountryOffZip( sZip )
    #
    if isinstance( uCountry, str ):
        #
        bGotMatch = sCountry == uCountry
        #
    else:
        #
        bGotMatch = sCountry in uCountry
        #
    #
    return bGotMatch




def _OverSeasZipTimeTrial():
    #
    from Iter.AllVers       import tFilter
    from Utils.TimeTrial    import TimeTrial
    #
    lTestZips, iApoZips = _getTestZips()
    #
    # slowest
    def ApoZipTrial( lTestZips ):
        return tFilter( isApoZip, lTestZips )
    #
    # runner up and a close 2nd
    def OverseasZipStringTestTrial( lTestZips ):
        return tFilter( isOverseasZipStringTest, lTestZips )
    #
    # fastest
    def OverseasZipTrial( lTestZips ):
        return tFilter( isOverseasZipOk2Drop0, lTestZips )
    #
    TimeTrial( ApoZipTrial, lTestZips )
    TimeTrial( OverseasZipStringTestTrial, lTestZips )
    TimeTrial( OverseasZipTrial, lTestZips )


def isPostalCodeCA( s ):
    #
    from sMail.Get      import getCodeCA
    #
    return getCodeCA( s )


def isPostalCodeCorrectCA( s ):
    #
    from sMail.Get import getCodeCA
    #
    sCode = getCodeCA( s )
    #
    return oPCodeStrictCA( sCode )


def isPostCodeOk4ProvinceCA( sCode, sProvince ):
    #
    from sMail.Abbrev   import dCodesProvAbbrevCA, dProvinceCAAbbrev, \
                    dAbbrevProvincesCA
    #
    if sProvince not in dAbbrevProvincesCA:
        #
        sProvince = dProvinceCAAbbrev.get( sProvince )
        #
    #
    sCode0 = sCode[0].upper()
    #
    return ( dCodesProvAbbrevCA.get( sCode0, '??' ) == sProvince or
             ( sCode0 == 'X' and sProvince == 'NU' ) )



def isPostalCodeAU( s ): # Australia
    #
    return s.isdigit() and len( s ) == 4


def isStateCode( s ):
    #
    from sMail.Zips import dZipRange4Code
    #
    return s.upper() in dZipRange4Code


def _getPartsOffAdds( *args ):
    #
    s = ' '.join( args ).strip()
    #
    lParts = s.split()
    #
    return lParts


def isNFAddImprovable( lParts ):
    #
    sNFAddImprovable = ''
    #
    s = ' '.join( lParts )
    #
    if len( lParts ) == 1:
        #
        pass
        #
    #
    #
    return sNFAddImprovable


def isInsufficientAdd( *args ):
    #
    bInsufficientAdd = False
    #
    lParts  = _getPartsOffAdds( *args )
    #
    s = ' '.join( lParts )
    #
    try:
        if len( lParts ) > 1:   raise Finished
        #
        if _oFindRR( s ):       raise Finished
        #
        bInsufficientAdd = True
        #
        sNFAddImprovable = isNFAddImprovable( lParts )
        #
    #
    except Finished:
        #
        pass
        #
    #
    return bInsufficientAdd and not sNFAddImprovable





def isStateAfterCity( sCity ):
    #
    '''
    pass a city string
    if the state is in there,
    function will return it
    if not, returns empty string
    '''
    sStateAfterCity = ''
    #
    lStates = oFinderStateBoth( sCity )
    #
    if lStates:
        #
        lNewYorkNY = _oFinderNewYorkNY( sCity )
        #
        if len( lNewYorkNY ) == 2:
            #
            sStateAfterCity = lStates[ -1 ]
            #
        else:
            #
            if len( lStates ) == 2 and lStates[0] == lStates[1]:
                del lStates[1]
            else:
                lStates = [ s for s in lStates if not sCity.startswith( s ) ]
            #
            if lStates:
                #
                sState = lStates[ -1]
                #
                if len( sState ) >= 2 and len( sCity ) > 1.5 * len( sState ):
                    #
                    sStateAfterCity = sState 
                    #
                #
            #
        #
    #
    return sStateAfterCity





def isLookingLikeAnAddress( sPart, sNewAdd ):
    #
    from sMail.Abbrev import oAddressPartsFinder
    from String.Test  import hasAnyDigits
    #
    lParts = sNewAdd.split()
    #
    iPartAt = -1
    #
    bLooksLineAnAdd = False
    #
    if ' ' in sPart:
        #
        l = sPart.split()
        #
        sPart = l[0]
        #
    #
    if sPart in lParts: iPartAt = lParts.index( sPart )
    #
    if iPartAt > 1:
        #
        bLooksLineAnAdd = (
            hasAnyDigits( lParts[ iPartAt - 1 ] ) or
            hasAnyDigits( lParts[ iPartAt - 2 ] ) )
        #
    elif iPartAt > 0:
        #
        bLooksLineAnAdd = lParts[ iPartAt - 1 ].isdigit()
    #
    if not bLooksLineAnAdd and iPartAt > -1:
        #
        lAddParts = oAddressPartsFinder( sNewAdd )
        #
        if lAddParts:
            #
            lPartsWhere = [ lParts.index( s ) for s in lAddParts if s in lParts ]
            #
            bLooksLineAnAdd = lPartsWhere and lPartsWhere[-1] > iPartAt
    #
    #
    return bLooksLineAnAdd


def isStateInAdd( tStateInAdd, sNewAdd ):
    #
    from sMail.Test import isLookingLikeAnAddress
    #
    bStateInAdd = False
    #
    lStateInAdd = [ s.title() for s in tStateInAdd ]
    #
    sNewAdd = sNewAdd.title()
    #
    for sState in lStateInAdd:
        #
        if (    sState + ' Ave'   in sNewAdd or
                sState + ' St'    in sNewAdd or
                sState + ' Lane'  in sNewAdd or
                sState + ' Drive' in sNewAdd or
                sState + ' Rd'    in sNewAdd or
                sState + ' Ap'    in sNewAdd or
                sState + ' Lane'  in sNewAdd or
                sState + ' Pl'    in sNewAdd or
                sState + ' Blvd'  in sNewAdd or
                sState + ' Sq'    in sNewAdd or
                sState + ' #'     in sNewAdd or
                sState + ' Univ'  in sNewAdd or
                sState + ' Milit' in sNewAdd or
                'University Of ' + sState
                                   in sNewAdd ):
            pass
        elif isLookingLikeAnAddress( sState, sNewAdd ):
            pass
        else:
            bStateInAdd = True
            break
    #
    return bStateInAdd



def isCityInAdd( sCity, sAdd ):
    #
    bCityInAdd = sCity.upper() in sAdd.upper()
    #
    sCity, sAdd = sCity.title(), sAdd.title()
    #
    if (    sCity + ' University' in sAdd or
            sCity + ' College'    in sAdd or
            sCity + ' Ap'         in sAdd or
            sCity + ' Blvd'       in sAdd or
            sCity + ' Community'  in sAdd or
            sCity + ' Ave'        in sAdd or
            sCity + ' Road'       in sAdd or
            sCity + ' St'         in sAdd or
            sCity + ' Rd'         in sAdd or
            sCity + ' Heights'    in sAdd or
            'University Of ' + sCity in sAdd ):
        #
        bCityInAdd = False
        #
    #elif (    sAdd == sCity or
              #sAdd.startswith( sCity ) or
              #sAdd.endswith( sCity ) ):
        ##
        #bCityInAdd = True
        ##
    ##
    #elif ',' in sAdd and sAdd.find( ',' ) < sAdd.find( sCity ):
        ##
        #bCityInAdd = True
        #
    return bCityInAdd




if __name__ == "__main__":
    #
    from random         import random, shuffle
    #
    from six            import print_ as print3
    #
    from Collect.Query  import get1stThatFails
    from Iter.AllVers   import iMap, tMap, tFilter
    from Collect.Test   import AllMeet
    from Utils.Result   import sayTestResult
    from sMail.Zips     import dApoZipCountry
    from sMail.Get      import getCountryFunctions
    #
    lProblems = []
    #
    if not oPOBoxFinder.findall( 'po box 133' ):
        #
        lProblems.append( 'oPOBoxFinder() po box 133' )
        #
    #
    if not oPOBoxFinder.findall( 'p o box 133' ):
        #
        lProblems.append( 'oPOBoxFinder() p o box 133' )
        #
    #
    if not oPOBoxFinder.findall( 'abc po box 133' ):
        #
        lProblems.append( 'oPOBoxFinder() abc po box 133' )
        #
    #
    if oPOBoxFinder.findall( '143 E. Pulaski St. P.O. Box 100' ) != ['P.O. Box 100']:
        #
        lProblems.append( 'oPOBoxFinder() 143 E. Pulaski St. P.O. Box 100' )
        #
    #
    #
    if not isPOBoxAddress( 'p.o. box 123' ):
        #
        lProblems.append( 'isPOBoxAddress() p.o. box 133' )
        #
    #
    if not isPOBoxAddress( 'pobox 123' ):
        #
        lProblems.append( 'isPOBoxAddress() pobox 133' )
        #
    #
    if not isPOBoxAddress( 'box 123' ):
        #
        lProblems.append( 'isPOBoxAddress() box 133' )
        #
    #
    if not isPOBoxAddress( 'cmr 480 box 445' ):
        #
        lProblems.append( 'isPOBoxAddress() cmr 480 box 445' )
        #
    #
    if not oCareOfFinder( 'c/o GE II Distribution' ):
        #
        lProblems.append( 'oCareOfFinder() c/o positive' )
        #
    #
    if not oCareOfFinder( 'co GE II Distribution' ):
        #
        lProblems.append( 'oCareOfFinder() co positive' )
        #
    #
    if not oCareOfFinder( 'in care of/Saunders' ):
        #
        lProblems.append( 'oCareOfFinder() in care of/' )
        #
    #
    if oCareOfFinder( '1231 N 48th St' ):
        #
        lProblems.append( 'oCareOfFinder() negative' )
        #
    #
    if isZipInState( '10101', 'VA' ):
        #
        lProblems.append( 'isZipInState()' )
        #
    #
    if isZipInState( '10101', '' ):
        #
        lProblems.append( 'isZipInState()' )
        #
    #
    if isZipInState( '', 'VA' ):
        #
        lProblems.append( 'isZipInState()' )
        #
    #
    if not isZipInState( '20101', 'VA' ):
        #
        lProblems.append( 'isZipInState()' )
        #
    #
    if not isZipInState( '23001', 'VA' ):
        #
        lProblems.append( 'isZipInState()' )
        #
    #
    if not isZipInState( '06399','New York' ):
        #
        lProblems.append( 'isZipInState()' )
        #
    #
    if not isZipInState( '10101','New York' ):
        #
        lProblems.append( 'isZipInState()' )
        #
    #
    for sZip in _getExampleZips():
        #
        bOverseasZipString =  isOverseasZipStringTest( sZip )
        bOverseasZipFinder = isOverseasZip( sZip )
        #
        if bOverseasZipString and not bOverseasZipFinder:
            #
            lProblems.append( '%s isOverseasZipStringTest( sZip ) and not isOverseasZip( sZip )' % sZip )
            #
        #
        if not bOverseasZipString and bOverseasZipFinder:
            #
            lProblems.append( '%s not isOverseasZipStringTest( sZip ) and isOverseasZip( sZip )' % sZip )
            #
        #
    #
    if get1stThatFails( _getExampleZips(), isZipCode ):
        #
        lProblems.append( 'isZipCode() example zip' )
        #
    #
    if isZipCode( 'abcde' ):
        #
        lProblems.append( 'isZipCode() invalid zip' )
        #
    #
    if isZipCode( '2205' ):
        #
        lProblems.append( 'isZipCode() leading zero missing NOT OK' )
        #
    #
    if not isZipCode( '981036625' ):
        #
        lProblems.append( 'isZipCode() zip+4 but no dash' )
        #
    #
    if not isZipPlus4( '98103-6625' ):
        #
        lProblems.append( 'isZipPlus4() valid zip' )
        #
    #
    if not isZipPlus4( '981036625' ):
        #
        lProblems.append( 'isZipPlus4() valid zip but no dash' )
        #
    #
    if not isZipPlus4( '98103 - 6625' ):
        #
        lProblems.append( 'isZipPlus4() valid zip with spaces' )
        #
    #
    if isZipPlus4( '98103' ):
        #
        lProblems.append( 'isZipPlus4() zip5' )
        #
    #
    if isZipPlus4( '98103-' ):
        #
        lProblems.append( 'isZipPlus4() zip5 with hyphen' )
        #
    #
    if isZipPlus4( '98103-abcd' ):
        #
        lProblems.append( 'isZipPlus4() zip5 with letters' )
        #
    #
    if isZipPlus4( 'abcde' ):
        #
        lProblems.append( 'isZipPlus4() invalid zip' )
        #
    #
    if not isZipPlus4( '98103-6625R' ):
        #
        lProblems.append( 'isZipPlus4() allow letters on end' )
        #
    #
    for sZip in dApoZipCountry:
        #
        if not isOverseasZipStringTest( sZip ):
            #
            lProblems.append(
                'isOverseasZipStringTest() %s '
                'is not recognized as overseas zip' % sZip )
            #
        #
    #
    sAdd1 = 'PO Box 888'
    sAdd2 = '1231 N 48th St'
    sAdd3 = 'Box 888'
    #
    if isResidenceAddress( sAdd1 ) or isResidenceAddress( sAdd3 ):
        #
        lProblems.append( 'isResidenceAddress() box address' )
        #
    #
    if not isResidenceAddress( sAdd2 ):
        #
        lProblems.append( 'isResidenceAddress() street address' )
        #
    #
    tZipLike = ( '1234', '99999', '88888-1234', '1234 ',
                 ' 99999 ', ' 88888 - 1234 ', '88888-' )
    tZipFake = ( '234', '888888', '206-555-1212' )
    #
    if False in iMap( isZipLike, tZipLike ):
        #
        lProblems.append( 'isZipLike() valid zip' )
        #
    #
    if True in iMap( isZipLike, tZipFake ):
        #
        lProblems.append( 'isZipLike() invalid zip' )
        #
    #
    if AllMeet( iMap( isZipLikeStrict, tZipLike ) ):
        #
        lProblems.append( 'isZipLike() missing front 0 no good' )
        #
    #
    if isApoZip( '98103' ) or not isApoZip( '96546' ):
        #
        lProblems.append( 'isApoZip() 9\'s' )
        #
    #
    if isApoZip( '02215' ) or not isApoZip( '09036' ):
        #
        lProblems.append( 'isApoZip() 0\'s' )
        #
    #
    lTestZips, iApoZips = _getTestZips()
    #
    if len( tFilter( isApoZip, lTestZips ) ) != iApoZips:
        #
        lProblems.append( 'isApoZip() filtered list' )
        #
    #    
    if len( tFilter( isOverseasZipStringTest, lTestZips ) ) != iApoZips:
        #
        lProblems.append( 'isOverseasZipStringTest() filtered list' )
        #
    #
    if len( tFilter( isOverseasZip, lTestZips ) ) != iApoZips:
        #
        lProblems.append( 'isOverseasZip() filtered list' )
        #
    #
    if isApoCityStateZip( 'Seattle  WA  99105-6625' ):
        #
        lProblems.append( 'isApoCityStateZip() non APO city state zip' )
        #
    #
    if not isApoCityStateZip( 'FPO, AP 96515-1200' ):
        #
        lProblems.append( 'isApoCityStateZip() APO city state zip' )
        #
    #
    if not isApoCityStateZip( 'PSC BOX 2 APO AP 1058  KUNSAN AB  96264' ):
        #
        lProblems.append( 'isApoCityStateZip() APO city state zip with AB' )
        #
    #
    if not isApoCityStateZip( 'KAIA JC CJ6 SSG AMNOC  APO  09320' ):
        #
        lProblems.append( 'isApoCityStateZip() Afghanistan APO address' )
        #
    #
    if not isApoCityStateZip( 'AFSN-NEA BOX#289, UNIT 15704  Camp Carrol  (Korea)  APO AO 96260' ) :
        #
        lProblems.append( 'isApoCityStateZip() Korea APO address' )
        #
    #
    if doesApoZipMatchCountry( '96375', 'Cuba' ):
        #
        lProblems.append( 'doesApoZipMatchCountry() country does not match zip' )
        #
    #
    if not doesApoZipMatchCountry( '09721', 'Finland' ):
        #
        lProblems.append( 'doesApoZipMatchCountry() Finland shares with Russia' )
        #
    #
    if not doesApoZipMatchCountry( '09721', 'Russian Federation' ):
        #
        lProblems.append( 'doesApoZipMatchCountry() Russia shares with Finland' )
        #
    #
    if not doesApoZipMatchCountry( '09720', 'Portugal' ):
        #
        lProblems.append( 'doesApoZipMatchCountry() 09720 is for Portugal' )
        #
    #
    if not doesApoZipMatchCountry( '09720', 'Portugal' ):
        #
        lProblems.append( 'doesApoZipMatchCountry() 09720 is for Portugal' )
        #
    #
    if not doesApoZipMatchCountry( '96217', 'South Korea' ):
        #
        lProblems.append( 'doesApoZipMatchCountry() 96217 is for Korea' )
        #
    #
    sCanada = '''"34189";"Owen Sound";"Ontario";"N4K 3A3";"Canada";"295 8th avenue east";NULL'''
    #
    if oPCodeFinderCA( sCanada ) != ['N4K 3A3']:
        #
        lProblems.append( 'oPCodeFinderCA() in string' )
        #
    #
    if oPCodeFinderCA( 'N4K 3A3' ) != ['N4K 3A3']:
        #
        lProblems.append( 'oPCodeFinderCA() code only' )
        #
    #
    if isPostalCodeCA( '09720' ):
        #
        lProblems.append( 'isPostalCodeCA() invalid as CA postal code' )
        #
    #
    if not isPostalCodeCA( 'N4K 3A3' ):
        #
        lProblems.append( 'isPostalCodeCA() valid CA postal code' )
        #
    #
    if isPostalCodeCA( 'D4K 3A3' ):
        #
        lProblems.append( 'isPostalCodeCA() invalid 1st letter in CA postal code' )
        #
    #
    if (    isPostalCodeCA( "8V8 1Z6"  ) or
            isPostalCodeCA( "T3C #l1"  ) or
            isPostalCodeCA( "Ma4Y 2S2" ) or
            isPostalCodeCA( "QCHK22J5" ) or
            isPostalCodeCA( "MY 1H5"   ) ):
        #
        lProblems.append( 'isPostalCodeCA() several invalid codes' )
        #
    #
    if not oPCodeStrictCA( 'N4K 3A3' ):
        #
        lProblems.append( 'oPCodeStrictCA() valid CA postal code' )
        #
    #
    if oPCodeStrictCA( 'N4K A3A' ):
        #
        lProblems.append( 'oPCodeStrictCA() invalid CA postal code' )
        #
    #
    if not isPostalCodeCorrectCA( 'N4K 3A3' ):
        #
        lProblems.append( 'isPostalCodeCorrectCA() valid CA postal code' )
        #
    #
    if isPostalCodeCorrectCA( 'N4K A3A' ):
        #
        lProblems.append( 'isPostalCodeCorrectCA() invalid CA postal code' )
        #
    #
    if isPostCodeOk4ProvinceCA( 'V3J 4V5', 'Ontario' ):
        #
        lProblems.append( 'isPostCodeOk4ProvinceCA() BC code for Ontario' )
        #
    #
    #
    if not isPostCodeOk4ProvinceCA( 'V3J 4V5', 'BC' ):
        #
        lProblems.append( 'isPostCodeOk4ProvinceCA() BC code BC abbreviation' )
        #
    #
    #
    if not isPostCodeOk4ProvinceCA( 'V3J 4V5', 'British Columbia' ):
        #
        lProblems.append( 'isPostCodeOk4ProvinceCA() BC code BC spelled out' )
        #
    #
    dCountryFunctions = getCountryFunctions( 'Canada' )
    #
    isPostalCodeCorrect     = dCountryFunctions.get( 'isPostalCodeCorrect'   )
    isPostCodeOk4Province   = dCountryFunctions.get( 'isPostCodeOk4Province' )
    isPostalCode            = dCountryFunctions.get( 'isPostalCode'          )
    #
    if not isPostalCodeCorrect( 'N4K 3A3' ):
        #
        lProblems.append( 'getCountryFunctions isPostalCodeCorrect() valid CA postal code' )
        #
    #
    if isPostCodeOk4Province( 'V3J 4V5', 'Ontario' ):
        #
        lProblems.append( 'getCountryFunctions isPostCodeOk4Province() BC code for Ontario' )
        #
    #
    if not isPostalCode( 'N4K 3A3' ):
        #
        lProblems.append( 'getCountryFunctions isPostalCode() valid CA postal code' )
        #
    #
    dCountryFunctions = getCountryFunctions( 'Hong Kong' )
    #
    isPostalCodeCorrect     = dCountryFunctions.get( 'isPostalCodeCorrect'   )
    isPostCodeOk4Province   = dCountryFunctions.get( 'isPostCodeOk4Province' )
    isPostalCode            = dCountryFunctions.get( 'isPostalCode'          )
    #
    if not isPostalCodeCorrect( 'N4K 3A3' ):
        #
        lProblems.append( 'getCountryFunctions isPostalCodeCorrect() any HK postal code is valid' )
        #
    #
    if not isPostCodeOk4Province( 'V3J 4V5', 'Ontario' ):
        #
        lProblems.append( 'getCountryFunctions isPostCodeOk4Province() all HK codes OK for all provinces' )
        #
    #
    if not isPostalCode( 'N4K 3A3' ):
        #
        lProblems.append( 'getCountryFunctions isPostalCode() any HK postal code is valid' )
        #
    #
    if not isPostalCodeAU( '7000' ):
        #
        lProblems.append( 'isPostalCodeAU() Tasmania' )
        #
    #
    if isPostalCodeAU( 'N4K 3A3' ):
        #
        lProblems.append( 'isPostalCodeAU() Canada code' )
        #
    #
    if isStateCode( 'xyz' ) or not isStateCode( 'wa' ):
        #
        lProblems.append( 'isStateCode()' )
        #
    #
    if not isNFAddImprovable( [ 'RR1', ] ):
        #
        # lProblems.append( 'isNFAddImprovable() RR + digit is OK' )
        #
        pass
    #
    if not isInsufficientAdd( '209', '' ):
        #
        lProblems.append( 'isInsufficientAdd() insufficient' )
        #
    #
    if isInsufficientAdd( '1231 n 48th st', '' ):
        #
        lProblems.append( 'isInsufficientAdd() sufficient' )
        #
    #
    if isInsufficientAdd( 'RR1', '' ):
        #
        lProblems.append( 'isInsufficientAdd() RR1' )
        #
    #
    if isInsufficientAdd( 'R.R.1', '' ):
        #
        lProblems.append( 'isInsufficientAdd() RR1' )
        #
    #
    tCitiesStates = (
        'Seattle Washington',
        'Memphis TN',
        'Long Beach, CA',
        'Philadelphia PA',
        'New York, NY',
        'NYC, NY',
        'New York, New York' )
    #
    if '' in tMap( isStateAfterCity, tCitiesStates ):
        #
        print3( tMap( isStateAfterCity, tCitiesStates ) )
        lProblems.append( 'isStateAfterCity() positives' )
        #
    #print3( isStateAfterCity( 'Seattle Washington' ) )
    #print3( oFinderStateName( 'Seattle Washington' ) )
    #
    if not isStateAfterCity( 'Dix Hills New York' ):
        #
        lProblems.append( 'isStateAfterCity() town in NY state' )
        #
    #
    if isStateAfterCity( 'Seattle' ):
        #
        lProblems.append( 'isStateAfterCity() negative' )
        #
    #
    if isStateAfterCity( 'La Conner' ):
        #
        lProblems.append( 'isStateAfterCity() La Conner' )
        #
    #
    if not isStateAfterCity( 'COLORADO SPRINGS COLORADO' ):
        #
        lProblems.append( 'isStateAfterCity() COLORADO SPRINGS COLORADO' )
        #
    #
    if isStateAfterCity( 'COLORADO' ):
        #
        lProblems.append( 'isStateAfterCity() COLORADO' )
        #
    #
    if not oFinderStateBoth( 'COLORADO' ):
        #
        lProblems.append( 'oFinderStateBoth() COLORADO' )
        #
    #
    #
    if oFinderStateName( 'abcde Washington xyz ' )[0] != 'Washington':
        #
        lProblems.append( 'oFinderStateName() Washington state' )
        #
    #
    if oFinderStateName( 'abcde Washington, DC xyz ' ):
        #
        lProblems.append( 'oFinderStateName() finding DC w comma' )
        #
    #
    if oFinderStateName( 'abcde Washington DC xyz ' ):
        #
        lProblems.append( 'oFinderStateName() finding DC no comma' )
        #
    #
    if oFinderStateName( 'abcde xyz ' ) != []:
        #
        lProblems.append( 'oFinderStateName() no state' )
        #
    #
    if oFinderStateCode( '(panybnjcdemt WA) xyz ' )[0] != 'WA':
        #
        lProblems.append( 'oFinderStateCode() valid state' )
        #
    #
    if oFinderStateCode( 'panybnjcdemt xyz ' ) != []:
        #
        lProblems.append( 'oFinderStateCode() no state' )
        #
    #
    sPart, sNewAdd = 'KY', '5528 KY Route 114 Apt 20'
    #
    if not isLookingLikeAnAddress( sPart, sNewAdd ):
        #
        lProblems.append( 'isLookingLikeAnAddress() KY' )
        #
    #
    sPart, sNewAdd = 'Washington', '11408 Washington Place C  Los angeles Ca'
    #
    if not isLookingLikeAnAddress( sPart, sNewAdd ):
        #
        lProblems.append( 'isLookingLikeAnAddress() Washington Place' )
        #
    #
    sPart, sNewAdd = 'Co', '11617 Co Rd 633'
    #
    if not isLookingLikeAnAddress( sPart, sNewAdd ):
        #
        lProblems.append( 'isLookingLikeAnAddress() Co Rd' )
        #
    #
    sPart, sNewAdd = 'Washington', 'South Washington Park Ave'
    #
    if not isLookingLikeAnAddress( sPart, sNewAdd ):
        #
        lProblems.append( 'isLookingLikeAnAddress() South Washington Park Ave' )
        #
    #
    sPart, sNewAdd = 'Virginia', '91534   Virginia Gardens'
    #
    if not isLookingLikeAnAddress( sPart, sNewAdd ):
        #
        lProblems.append( 'isLookingLikeAnAddress() 91534 Virginia Gardens' )
        #
    #
    if isStateInAdd( ('Kentucky',), '302 Brockton Eastern Kentucky University' ):
        #
        lProblems.append( 'isStateInAdd() Kentucky University' )
        #
    #
    if isStateInAdd( ('Colorado',), 'University of Colorado' ):
        #
        lProblems.append( 'isStateInAdd() University of Colorado' )
        #
    #
    if isStateInAdd( ('Washington',), '11408 Washington Place C. Los angeles Ca' ):
        #
        lProblems.append( 'isStateInAdd() 11408 Washington Place' )
        #
    #
    if not isStateInAdd( ('Ca',), '11408 Washington Place C. Los angeles Ca' ):
        #
        lProblems.append( 'isStateInAdd() Los angeles Ca' )
        #
    #
    sCity, sAdd = 'Bala-Cynwyd', '26 Chestnut Ave. Bala-Cynwyd, PA 19004'
    #
    if not isCityInAdd( sCity, sAdd ):
        #
        lProblems.append( 'isCityInAdd() Bala-Cynwyd' )
        #
    #
    #
    # _OverSeasZipTimeTrial()
    #isOverseasZipOk2Drop0
    #
    sayTestResult( lProblems )