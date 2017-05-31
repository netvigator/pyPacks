#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# string functions PhoneNos phone numbers
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

'''
is the string a phone number or not?

'''

from string             import digits

from six                import print_ as print3

from String.Dumpster    import getDigitsOnly
from String.Find        import getFinderFindAll
from String.Test        import getHasSubstrTester                                                                                            
from Utils.Config       import getConfDict, getSetFrozenOffCommaString
from Utils.Config       import fixAllLevel2sUnderLevel1
from Utils.Combos       import All_
from Dict.Get           import getValueIter

bDebugPrint             = False

hasExtension = getHasSubstrTester( '( x|ext|#)' )



dStateInfo          = getConfDict('state_info.conf')
dCountryCodesMore   = getConfDict('country_codes.conf')

dCountryCodes       = dCountryCodesMore['main']

# setNoAmNumbPlanCountries = getSetFrozenOffCommaString( dCountryCodesMore['NANP']['countries'] )


        #'prepend-missing-numb'      : getBoolOffYesNoTrueFalse,
        #'mobile-number-length'      : int,

dConfValueFixers    = {
        'area_codes'        : getSetFrozenOffCommaString,
        'United Kingdom'    : getSetFrozenOffCommaString,
        }
        #'Canada'            : getSetFrozenOffCommaString,
        #'Caribbean'         : getSetFrozenOffCommaString,


fixAllLevel2sUnderLevel1( dStateInfo,        dConfValueFixers )

fixAllLevel2sUnderLevel1( dCountryCodesMore, dConfValueFixers )

setNoAmNumbPlanCountries = dCountryCodesMore['NANP']['countries']

class Finished( Exception ): pass

def _getCountryCodeFinder():
    #
    from Dict.Get   import getItemTuple, getValueIter
    #
    for k, v in getItemTuple( dCountryCodes ):
        #
        if '-' in v:
            #
            # Caribbean countries on USA phone system with own area codes
            #
            dCountryCodes[ k ] = v.replace( '-', '' )
            #
        elif ', ' in v: # satelite phone service
            #
            del dCountryCodes[ k ]
    #
    
    gotCountryCode = getFinderFindAll(
                        '^%s' % '|^'.join( getValueIter( dCountryCodes ) ) )
    #
    return gotCountryCode

_gotCountryCode = _getCountryCodeFinder()





def getCodeGotCountry( sCountry ):
    #
    return dCountryCodes.get( sCountry.lower(), None )



setCountryCodes = frozenset( dCountryCodes.values() )

def isCountryCode( s ):
    #
    return s in setCountryCodes


def _getDictIddCodeCountry():
    #
    from Dict.Get import getReverseDict
    #
    dIddCodesCountries = getReverseDict( dCountryCodes )
    #
    return dIddCodesCountries



dIddCodesCountries = _getDictIddCodeCountry()




def getCountryListGotIddCode( sIddCode ):
    #
    lCountries = []
    #
    if sIddCode in dIddCodesCountries:
        #
        lCountries = [ s.title() for s in dIddCodesCountries[ sIddCode ] ]
        #
    #
    return lCountries



isInvalid = \
    getFinderFindAll(
        'same|none|unknown|dontwant|unlisted|no listing|no phone|to be added|do not have' )

def isMaybeValid( sPhone ): return not isInvalid( sPhone )

setNotAvailable = frozenset( ( 'n/a', 'not available', 'na' ) )


def getAreaCodeSet():
    #
    setCodes = set( () )
    #
    for setState in getValueIter( dStateInfo.get('area_codes') ):
        #
        setCodes.update( setState )
    #
    return frozenset( setCodes )

setAreaCodesUSA = getAreaCodeSet()



def _isAreaCodeForCountry( sAreaCodeMaybe, setAreaCodes = setAreaCodesUSA ):
    #
    return sAreaCodeMaybe in setAreaCodes


def isAreaCodeForUSA( sAreaCodeMaybe ):
    #
    return _isAreaCodeForCountry( sAreaCodeMaybe )





def getOtherCodeSet( sArea ):
    #
    sCodes = ','.join( getValueIter( dCountryCodesMore.get( sArea ) ) )
    #
    return frozenset( sCodes.replace( ' ', '' ).split(',') )


setAreaCodesCanada    = getOtherCodeSet( 'Canada'    )
setAreaCodesCaribbean = getOtherCodeSet( 'Caribbean' )


def getStateAbbreviationDict():
    #
    from Dict.Get       import getDictOffPairOfLists, getKeyIter
    from Iter.AllVers   import iMap
    from String.Get     import getLower, getUpper
    #
    dAbbreviationsStates = dStateInfo.get('abbreviations')
    #
    iAbbreviations  = iMap( getUpper, getKeyIter(   dAbbreviationsStates ) )
    iStates         = iMap( getLower, getValueIter( dAbbreviationsStates ) )
    #
    return getDictOffPairOfLists( iStates, iAbbreviations )


def getAreaCodeStateAbbrevDict():
    #
    from Dict.Get       import getDictOffPairOfLists
    from Dict.Get       import getKeyIter
    #
    dStatesAbbreviations = getStateAbbreviationDict()
    #
    dStatesCodeStrings = dStateInfo.get('area_codes')
    #
    dCodesStates = {}
    #
    for sState in getKeyIter( dStatesCodeStrings ):
        #
        tCodes = tuple( dStatesCodeStrings.get( sState ) )
        #
        if isinstance( dStatesAbbreviations.get( sState ), str ):
            sAbbrev = dStatesAbbreviations.get( sState ).upper()
            #
            dCodesStates.update(
                getDictOffPairOfLists ( tCodes, [ sAbbrev ] * len( tCodes ) ) )
        else:
            print3( 'is "%s" a state?' % sState )
    #
    return dCodesStates

dCodesStateAbbrevs = getAreaCodeStateAbbrevDict()

fFindPhoneUSA   = getFinderFindAll( '\A1?(?:[2-9]\d{2}){2}\d{4}\Z' )


_setUsaLongNumbers = frozenset( ( 10, 11 ) )


def isFormatOrLikeUSA( sPhoneOrig ):
    #
    from String.Eat     import eatFrontZeros
    from String.Test    import getNumberPattern
    #
    lNumberPattern  = getNumberPattern( sPhoneOrig )
    #
    lNumberPattern[0:0] = [ 0, 0, 0 ]
    #
    sPhoneDigits    = getDigitsOnly( sPhoneOrig )
    #
    bLikePhoneUSA   = False
    #
    bFormatLikeUSA = False
    #
    #print3( lNumberPattern )
    #
    if bDebugPrint:
        print3( '' )
        print3( 'lNumberPattern:', lNumberPattern )
        print3( 'sPhoneDigits:', sPhoneDigits )
    #
    try:
        if not fFindPhoneUSA( eatFrontZeros( sPhoneDigits ) ):
            #
            if bDebugPrint:
                print3( 'fFindPhoneUSA() returned False' )
            #
            raise Finished
            #
        if not sPhoneDigits[ -10 : -7 ] in setAreaCodesUSA:
            #
            if bDebugPrint:
                print3( sPhoneDigits[ -10 : -7 ], 'area code digits not found!' )
            #
            raise Finished
            #
        if  lNumberPattern[ -1 ] in  _setUsaLongNumbers:
            #
            # 8005551212 or 18005551212 
            #
            if bDebugPrint:
                print3( 'lNumberPattern[ -1 ] in  _setUsaLongNumbers!' )
            #
            bLikePhoneUSA = True
            #
        elif ( lNumberPattern[ -3 ] == 1 and
               lNumberPattern[ -2 ] == 3 and
               lNumberPattern[ -1 ] == 7 ):
            #
            # 1 800 5551212 
            #
            if bDebugPrint:
                print3( 'number pattern ends with 1, 3, 7' )
            #
            bLikePhoneUSA  = True
            #
            bFormatLikeUSA = True
            #
        elif ( lNumberPattern[ -3 ] == 3 and
               lNumberPattern[ -2 ] == 3 and
               lNumberPattern[ -1 ] == 4 ):
            #
            # 800 555-1212 
            #
            if bDebugPrint:
                print3( 'number pattern ends with 3, 3, 4' )
            #
            bLikePhoneUSA  = True
            #
            bFormatLikeUSA = True
            #
        elif lNumberPattern[ -2 ] == 3 and lNumberPattern[ -1 ] == 7:
            #
            # 800 5551212 
            #
            bLikePhoneUSA = True
            #
        elif lNumberPattern[ -2 ] == 6 and lNumberPattern[ -1 ] == 4:
            #
            # 800555 1212 
            #
            bLikePhoneUSA = True
            #
        #
    except Finished:
        pass
    #
    return bLikePhoneUSA, bFormatLikeUSA



def isFormatLikeUSA( sPhoneOrig ):
    #
    bLikePhoneUSA, bFormatLikeUSA = isFormatOrLikeUSA( sPhoneOrig )
    #
    return bFormatLikeUSA


def isLikePhoneUSA( sPhoneOrig ):
    #
    bLikePhoneUSA, bFormatLikeUSA = isFormatOrLikeUSA( sPhoneOrig )
    #
    return bLikePhoneUSA



def isAreaCodeFromState( sAreaCode, sState ):
    #
    return sState.upper() == dCodesStateAbbrevs.get( sAreaCode )


def getStateGotAreaCode( sAreaCode ):
    #
    return dCodesStateAbbrevs.get( sAreaCode, 'not a USA area code' )










setZeroOne = frozenset( ( '0', '1' ) )




def _getAreaCodeAndDigits( sPhone ):
    #
    sPhoneDigits = getDigitsOnly( sPhone )
    #
    sAreaCode = sPhoneDigits[ -10 : -7 ]
    #
    return sAreaCode, sPhoneDigits



def getNumberDropExtension( sPhone ):
    #
    from String.Eat     import eatBackNonDigits
    #
    lExtension = hasExtension( sPhone )
    #
    if lExtension:
        #
        sPhone = eatBackNonDigits( sPhone[ : sPhone.index( lExtension[0] ) ] )
        #
    #
    return sPhone




def getDigitCount( sPhone ):
    #
    sPhoneDigits = getDigitsOnly( getNumberDropExtension( sPhone ) )
    #
    return len( sPhoneDigits )





def getAreaCode( sPhone ):
    #
    sAreaCode, sPhoneDigits = _getAreaCodeAndDigits( sPhone )
    #
    return sAreaCode




def isPhoneFromState( sPhone, sState ):
    #
    sAreaCode, sPhoneDigits = _getAreaCodeAndDigits( sPhone )
    #
    return  sPhoneDigits[ -7 : -6 ] not in setZeroOne and \
            isAreaCodeFromState( sAreaCode, sState )




def _getPhoneDigits( sPhone ):
    #
    from String.Dumpster    import oKeepDigitsOnly, getWhiteWiped
    #
    sDigitsSpaces           = oKeepDigitsOnly.Dump( sPhone )
    #
    return getWhiteWiped( sDigitsSpaces ), sDigitsSpaces


def _getZerosOffEnd( sPhone ):
    #
    from String.Get import getTheseCharsOffOneEnd
    #
    def isZero( s ): return s == '0'
    #
    return getTheseCharsOffOneEnd( sPhone, fGetIfMeets = isZero, bEatOffFront = False )


def isBogusPhone( sPhone, bExplain = False ):
    #
    from sys            import exc_info
    #
    from String.Test    import isInOrder
    #
    bBogus              = True
    #
    if sPhone.startswith( '011' ):
        # strip IDD prefix
        sPhone = sPhone[ 3 : ]
        #
    #
    sPhone = sPhone.strip()
    #
    try:
        #
        sDigits, sDigitsSpaces = _getPhoneDigits( sPhone )
        #
        iDigits         = len( sDigits )
        #
        if iDigits      < 5:
            raise Finished( 'fewer than 5 digits' )
        #
        if isInOrder( sDigits ):
            raise Finished( 'digits are in order' )
        #
        lCountryCode = _gotCountryCode( sDigits )
        #
        if lCountryCode:
            #
            sCountryCode = lCountryCode[0]
            #
            sRemains = sDigits [ len( sCountryCode ) : ]
            #
            if len( sRemains ) >= 5 and  isInOrder( sRemains ):
                raise Finished( 'digits after country code are in order' )
            #
        #
        if sDigits.endswith( '5551212' ):
            raise Finished( 'USA directory assistance number' )
        #
        setDigits       = frozenset( tuple( sDigits ) )
        #
        if len( setDigits ) < iDigits // 4:
            raise Finished( 'few digits repeated' )
        #
        #print3( 'len( setDigits ):', len( setDigits ) )
        #print3( 'iDigits:', iDigits )
        #print3( 'iDigits // 3:', iDigits / 3 )
        #
        iEndingZeros    = len( _getZerosOffEnd( sDigits ) )
        #
        #print3( 'iEndingZeros:', iEndingZeros )
        if iDigits - iEndingZeros <= 0:
            raise Finished( 'absolutely too many ending zeros' )
        #
        #print3( '' ) 
        #print3( 'setDigits:', setDigits ) 
        #print3( 'len( setDigits ):', len( setDigits ) )
        #print3( 'iEndingZeros:', iEndingZeros )
        #print3( 'len( setDigits ) - iEndingZeros:', len( setDigits ) - iEndingZeros )
        #print3( 'iDigits:', iDigits ) 
        #print3( 'iDigits // 5:', iDigits // 5 ) 
        #print3( '1 + len( setDigits ) - iEndingZeros < iDigits // 5:', 1 + len( setDigits ) - iEndingZeros < iDigits // 5 ) 
        #
        if 1 + len( setDigits ) - iEndingZeros < iDigits // 5:
            raise Finished( 'relatively too many ending zeros' )
        #
        sLast = sDigits[-1]
        #
        if sDigits[ -5 : ] == sLast * 5:
            raise Finished( 'ending repeats too many of same digit' )
        #            
        bBogus          = False
        #
    except Finished:
        #
        if bExplain:
            #
            error, msg, traceback = exc_info()
            #
            print3( sPhone, msg )
            #
    #
    return bBogus


def isPhoneNotBogus( sPhone ):
    #
    return not isBogusPhone( sPhone )


def isAvailable( s ): return not s.lower() in setNotAvailable

isValidPhone    = All_( isMaybeValid, isAvailable, isPhoneNotBogus )

isPhoneNo       = All_( isMaybeValid, isAvailable )



def _isPhone4Country(
        sPhone, sCountryCode, tLenMinMax, iAreaCodeLen = 0, setPrefix = (),
        bDropLocalZeroForIDD = False, bPrefixVaries = False ):
    #
    from Iter.AllVers   import iRange
    from String.Eat     import eatFrontNonDigits
    from String.Test    import hasAnyAlpha
    #
    bPhone4Country = False
    #
    sPhoneOrig = sPhone
    #
    # if sPhone.startswith( '+'   ): sPhone = eatFrontNonDigits( sPhone[1:] )
    #
    if bDebugPrint:
        print3( '' )
        print3( '' )
        print3( '_isPhone4Country()' )
        #
    if sPhone.startswith( '011' ): sPhone = eatFrontNonDigits( sPhone[3:] )
    #
    if hasAnyAlpha( sPhone ):
        #
        lExtension = hasExtension( sPhone )
        #
        if lExtension:
            #
            sPhone = sPhone[ : sPhone.index( lExtension[0] ) ]
        #
    #
    try:
        #
        sPhone, sDigitsSpaces = _getPhoneDigits( sPhone )
        #
        if bDebugPrint:
            print3( 'sPhone:', sPhone )
            print3( 'sDigitsSpaces: ', sDigitsSpaces )
            #
        #
        if sPhoneOrig.startswith( '+' ):
            #
            sNext = eatFrontNonDigits(
                        sPhoneOrig[ 1 : ] )[ : len( sCountryCode ) ]
            #
            if sNext != sCountryCode:
                #
                if bDebugPrint:  print3( 'sNext != sCountryCode' )
                sDigits, sDigitsSpaces = _getPhoneDigits( sPhone )
                raise Finished
                #
            #
        if sPhone.startswith(sCountryCode):
            #
            sPhone = eatFrontNonDigits( sPhone[len(sCountryCode):] )
            #
        #
        if bDebugPrint: 
            print3( 'bDropLocalZeroForIDD:', bDropLocalZeroForIDD )
            print3( 'sPhone.startswith( "0" ):', sPhone.startswith( '0' ) )
        if bDropLocalZeroForIDD and not sPhone.startswith( '0' ):
            #
            sPhone = '0%s' % sPhone
            #
        #
        sDigits, sDigitsSpaces = _getPhoneDigits( sPhone )
        #
        iDigitLen = len( sDigits )
        #
        if bDebugPrint:
            print3( 'sDigits: ', sDigits )
            print3( 'iDigitLen: ', iDigitLen )
            #
        #
        if iDigitLen < min( tLenMinMax ) or iDigitLen > max( tLenMinMax ):
            #
            if bDebugPrint: print3( 'iDigitLen < min( tLenMinMax )' )
            raise Finished
            #
        #
        if iAreaCodeLen and setPrefix:
            #
            sAreaCode = sDigits[ -iDigitLen : iAreaCodeLen - iDigitLen ]
            #
            if sAreaCode[0] in setPrefix:
                #
                if bDebugPrint: print3( 'sAreaCode[0] in setPrefix' )
                raise Finished
                #
            if sAreaCode not in setPrefix:
                #
                if bDebugPrint:
                    print3( 'sAreaCode not in setPrefix' )
                    print3( 'sAreaCode: ', sAreaCode )
                raise Finished
                #
            #
        elif bPrefixVaries and setPrefix:
            #
            bValidPrefix = False
            #
            for iLen in iRange( 3, 7 ): # (3, 4, 5, 6)
                #
                if sPhone[ : iLen ] in setPrefix:
                    #
                    bValidPrefix = True
                    #
                    if bDebugPrint:
                        print3( 'sPhone[ : iLen ] in setPrefix' )
                        print3( 'sPhone[ : iLen ]: ', sPhone[ : iLen ] )
                    #
                    break
                    #
                #
            #
            if not bValidPrefix:
                if bDebugPrint:
                    print3( 'sPhone[ : iLen ] not in setPrefix' )
                raise Finished
            #
            #
        elif setPrefix:
            #
            sExample = tuple( setPrefix )[0]
            #
            if sPhone[ : len( sExample  ) ] not in setPrefix:
                #
                if bDebugPrint: 
                    print3( 'sPhone[ : len( sExample  ) ] not in setPrefix' )
                    print3( 'sPhone[ : len( sExample  ) ]:', sPhone[ : len( sExample  ) ] )
                raise Finished
                #
        #
    #
    except Finished:
        #
        if bDebugPrint:
            print3( 'Finished was raised' )
        #
    else:
        #
        bPhone4Country = True
        if bDebugPrint:
            print3( 'Finished not raised, bPhone4Country set to True' )
        #
    #
    return bPhone4Country, sDigits


_setNoAmNumbPlanProhibitedFirst = frozenset( tuple( '01' ) )



def isPhoneUSA( sPhone ):
    #
    bPhone4Country, sDigits = _isPhone4Country(
                                sPhone, '1', ( 10, ), 3,
                                setPrefix = setAreaCodesUSA )
    #
    return (    bPhone4Country and
                sDigits[ -7 : -6 ] not in _setNoAmNumbPlanProhibitedFirst )


def isPhoneHK( sPhone ):
    #
    bPhone4Country, sDigits = _isPhone4Country( sPhone, '852', ( 8, ) )
    #
    return bPhone4Country


def isPhoneCanada( sPhone ):
    #
    bPhone4Country, sDigits = _isPhone4Country( sPhone, '1', ( 10, ), 3, setPrefix = setAreaCodesCanada )
    #
    return bPhone4Country and sDigits[ -7 : -6 ] not in _setNoAmNumbPlanProhibitedFirst


def isPhoneCaribbean( sPhone ):
    #
    bPhone4Country, sDigits = _isPhone4Country( sPhone, '1', ( 10, ), 3, setPrefix = setAreaCodesCaribbean )
    #
    return bPhone4Country and sDigits[ -7 : -6 ] not in _setNoAmNumbPlanProhibitedFirst


def isPhoneNoAmDialingPlan( sPhone ):
    #
    # North American Dialing Plan
    #
    return (    isPhoneUSA(       sPhone ) or
                isPhoneCanada(    sPhone ) or
                isPhoneCaribbean( sPhone ) )


def hasObviousOtherCountryCode(
        sPhoneOrig, sPhoneDigits, sThisCountryDialingCode,
        lNumberPattern, lPatternNumbers ):
    #
    from copy           import copy
    #
    from String.Eat     import eatFrontZerosOnes
    from String.Get     import getTextAfter
    from String.Test    import getNumberPattern, hasAnyDigits
    #
    if sThisCountryDialingCode is None:
        sThisCode       = ''
    else:
        sThisCode       = sThisCountryDialingCode
    sOtherCountryCode   = ''
    sLessDigits         = ''
    #
    lNumbers = copy( lPatternNumbers )
    lPattern = copy( lNumberPattern  )
    #
    if bDebugPrint:
        print3( 'sPhoneOrig:  ', sPhoneOrig  )
        print3( 'sThisCountryDialingCode: ', sThisCode )
        print3( 'lNumbers: ', lNumbers )
        print3( 'lPattern: ', lPattern )
    #
    if sPhoneOrig and not lPattern:
        #
        lPattern  = getNumberPattern( sPhoneOrig )
        #
    #
    if sPhoneOrig and not lNumbers:
        #
        iStart = 0
        #
        for iLen in lPattern:
            #
            lNumbers.append( sPhoneDigits[ iStart : iStart + iLen ] )
            #
            iStart += iLen
            #
    #
    if not lNumbers:
        #
        pass
        #
    elif lNumbers[0] == '011':
        #
        del lNumbers[0]
        del lPattern[0]
        #
    elif lNumbers[0] != '1':
        #
        lNumbers[0] = eatFrontZerosOnes( lNumbers[0] )
        lPattern[0] = len( lNumbers[0] )
        #
    #
    if lNumbers and not lNumbers[0]:
        #
        del lNumbers[0]
        del lPattern[0]
        #
    #
    if sPhoneDigits: sLessDigits = eatFrontZerosOnes( sPhoneDigits )
    #
    if bDebugPrint:
        print3( 'lNumbers: ', lNumbers )
    try:
        #
        if not hasAnyDigits( sPhoneOrig ):
            #
            raise Finished
            #
        elif False and sThisCode == '1':
            #
            raise Finished
            #
        elif (  sThisCode != '1' and
                (  sPhoneDigits[ : len( sThisCode ) ] == sThisCode or
                    sLessDigits[  : len( sThisCode ) ] == sThisCode ) ):
            #
            raise Finished
            #
        elif    (   sPhoneOrig.startswith( '+' ) and
                    isCountryCode( lPattern[0] ) ):
            #
            sOtherCountryCode = lPattern[0]
            #
            if bDebugPrint:
                print3( 'sOtherCountryCode: ', sOtherCountryCode )
            #
            raise Finished
            #
        #
        bCountryCodeFirst2 = isCountryCode( sLessDigits[ : 2 ] )
        bCountryCodeFirst3 = isCountryCode( sLessDigits[ : 3 ] )
        bCountryCodeFirst4 = isCountryCode( sLessDigits[ : 4 ] )
        #
        if bDebugPrint:
            print3( 'bCountryCodeFirst2: ', bCountryCodeFirst2 )
            print3( 'bCountryCodeFirst3: ', bCountryCodeFirst3 )
            print3( 'bCountryCodeFirst4: ', bCountryCodeFirst4 )
        #
        bLongPatternNumbers0 = len( lNumbers[0] ) > 4
        #
        if  (   bCountryCodeFirst2 or
                bCountryCodeFirst3 or
                bCountryCodeFirst4 ):
            #
            if (    bCountryCodeFirst2 and
                    (   sLessDigits[ : 2 ] == lNumbers[0] or
                        bLongPatternNumbers0 ) ):
                #
                sOtherCountryCode = sLessDigits[ : 2 ]
                #
                if bDebugPrint:
                    print3( 'sLessDigits[ : 2 ] == lNumbers[0]' )
                #
            elif (  bCountryCodeFirst3 and
                    (   sLessDigits[ : 3 ] == lNumbers[0] or
                        bLongPatternNumbers0 ) ):
                #
                sOtherCountryCode = sLessDigits[ : 3 ]
                #
                if bDebugPrint:
                    print3( 'sLessDigits[ : 3 ] == lNumbers[0]' )
                #
            elif (  bCountryCodeFirst4 and
                    (   sLessDigits[ : 4 ] == lNumbers[0] or
                        bLongPatternNumbers0 ) ):
                #
                sOtherCountryCode = sLessDigits[ : 4 ]
                #
                if bDebugPrint:
                    print3( 'sLessDigits[ : 4 ] == lNumbers[0]' )
                #
            else:
                #
                if bDebugPrint:
                    print3( 'lNumbers[0]: ', lNumbers[0] )
                #
                raise Finished
                #
        #
        if bDebugPrint:
            print3( 'sOtherCountryCode: ', sOtherCountryCode )
        #
        #   
        #
        #
        lParts = sPhoneOrig.split()
        #
        if len( lParts ) == 1:
            #
            lParts = sPhoneOrig.split( '-' )
            #
        #
        bObviousOtherCountryCode = (
            lParts and
            lParts[0] in ( '011', '001' ) and
            sThisCode != lParts[1] and
            isCountryCode( lParts[1] ) )
        #
        if bObviousOtherCountryCode:
            #
            sOtherCountryCode = lParts[1]
            #
            raise Finished
        #
        #
    except Finished: pass
    #
    #
    return sOtherCountryCode
    

_setPrefixesUK = frozenset( ( '01', '02', '07' ) )

_setPrefixesUK = dCountryCodesMore['United Kingdom']['phone_prefixes']

def isPhoneUK( sPhone ):
    #
    bPhone4Country, sDigits = _isPhone4Country(
            sPhone, '44', (11,), iAreaCodeLen = 0, setPrefix = _setPrefixesUK,
            bDropLocalZeroForIDD = True, bPrefixVaries = True )
    #
    return bPhone4Country




digitsFinder = getFinderFindAll(   '\d+'  )
othersFinder = getFinderFindAll( '[^\d]+' )


def getDigitsOtherObject( sPhone ):
    #
    from Iter.AllVers   import iRange
    from Object.Get     import ValueContainer
    #
    lDigits = digitsFinder( sPhone )
    lOthers = othersFinder( sPhone )
    #
    if lDigits and sPhone.startswith( lDigits[0] ):
        #
        lEven   = lDigits
        lOdds   = lOthers
        #
        tParts  = ( 'd', 'o' )
        #
    else:
        #
        lEven   = lOthers
        lOdds   = lDigits
        #
        tParts  = ( 'o', 'd' )
        #
    #
    lParts = [''] * 2 * max( len( lDigits ), len( lOthers ) )
    lWhich = [''] * len( lParts  )
    #
    if len( lOdds) < len( lEven ):
        #
        lOdds.append( '' )
    #
    for i in iRange( len( lEven ) ):
        #
        lParts[     2 * i ] = lEven[ i ]
        lParts[ 1 + 2 * i ] = lOdds[ i ]
        #
        lWhich[     2 * i ] = tParts[ 0 ]
        lWhich[ 1 + 2 * i ] = tParts[ 1 ]
        #
        #
    #
    if not lOdds[ -1 ]:
        #
        del lParts[ -1 ]
        del lWhich[ -1 ]
        del lOdds[   -1 ]
        #
    #
    oReturn = ValueContainer(
        lDigits = lDigits,
        lOthers = lOthers,
        lParts  = lParts,
        lWhich  = lWhich )
    #
    return oReturn
        








if __name__ == "__main__":
    #
    from sys import argv
    #
    from Collect.Query  import get1stThatFails, get1stThatMeets
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    args = argv[ 1 : ]
    #
    if args and args[0] == 'debug':
        #
        bDebugPrint = True
        #
    #
    sCountry = 'Germany'
    #
    if getCodeGotCountry( sCountry ) != '49':
        #
        lProblems.append( 'getCodeGotCountry() Germany' )
        #
    #
    sCountry = 'Canada'
    #
    if getCodeGotCountry( sCountry ) != '1':
        #
        lProblems.append( 'getCodeGotCountry() Canada' )
        #
    #
    sCountry = 'United States'
    #
    if getCodeGotCountry( sCountry ) != '1':
        #
        lProblems.append( 'getCodeGotCountry() suggest you change USA to United States' )
        #
    #
    
    if _gotCountryCode( '1206 286-2181' ) != ['1']:
        #
        lProblems.append( '_gotCountryCode() USA number' )
        #
    #
    if _gotCountryCode( '852 9876-5432' ) != ['852']:
        #
        lProblems.append( '_gotCountryCode() HK number' )
        #
    #
    '''
    # 
    '''
    sTest       = 'aABabcABCDabcdeABCDEF'
    #
    if      not fFindPhoneUSA( '12064079702' ) or \
            not fFindPhoneUSA(  '2064079702' ) or \
                fFindPhoneUSA(  '0890181075' ) or \
                fFindPhoneUSA( '66890181075' ):
        #
        lProblems.append( 'fFindPhoneUSA()' )
        #
    #
    if not fFindPhoneUSA( '12019845835' ):
        #
        lProblems.append( 'fFindPhoneUSA() 12019845835' )
        #
    #
    if      not isLikePhoneUSA( '12064079702' ) or \
            not isLikePhoneUSA(  '2064079702' ) or \
                isLikePhoneUSA(  '0890181075' ) or \
                isLikePhoneUSA( '66890181075' ) or \
                isLikePhoneUSA( '19994079602' ):
        #
        # no area code 999
        #
        lProblems.append( 'isLikePhoneUSA()' )
        #
    #
    
    if not isLikePhoneUSA( '917 696 0477' ):
        #
        lProblems.append( 'isLikePhoneUSA() 917 696 0477' )
        #
    #
    if not isLikePhoneUSA( '001 201 9845835' ):
        #
        lProblems.append( 'isLikePhoneUSA() 001 201 9845835' )
        #
    #
        
    if          isAreaCodeFromState( '212','PA' ) or \
            not isAreaCodeFromState( '212','NY' ):
        #
        lProblems.append( 'isAreaCodeFromState()' )
        #
    #
    if          isPhoneFromState( '12062862181','PA' ) or \
                isPhoneFromState(  '2062862181','PA' ) or \
            not isPhoneFromState( '12062862181','WA' ) or \
            not isPhoneFromState(  '2062862181','WA' ):
        #
        lProblems.append( 'isPhoneFromState()' )
        #
    #
    if isBogusPhone( '6073519826' ):
        #
        lProblems.append( 'isBogusPhone() NY number should not be bogus' )
        #
    #
    if isBogusPhone( '011494393969600' ):
        #
        lProblems.append( 'isBogusPhone() long DE number should not be bogus' )
        #
    #
    if isBogusPhone( '642.08' ):
        #
        lProblems.append( 'isBogusPhone() minimal DE number should not be bogus' )
        #
    #
    if isBogusPhone( '206 632-9929' ):
        #
        lProblems.append( 'isBogusPhone() valid USA number should not be bogus' )
        #
    #
    if not isBogusPhone( 'Unknown'             ):
        #
        lProblems.append( 'isBogusPhone() all alpha' )
        #
    #
    if not isBogusPhone(         '9876-5432'   ):
        #
        lProblems.append( 'isBogusPhone() digits in sequence' )
        #
    #
    if not isBogusPhone( '011 852 9876-5432'   ):
        #
        lProblems.append( 'isBogusPhone() digits in sequence with country code' )
        #
    #
    if not isBogusPhone(    '7 777 777 7777'   ):
        #
        lProblems.append( 'isBogusPhone() repeating digits' )
        #
    #
    if not isBogusPhone(        '4151540000'   ):
        #
        lProblems.append( 'isBogusPhone() Mexican favorite' )
        #
    #
    if not isBogusPhone(                 '1'   ):
        #
        lProblems.append( 'isBogusPhone() one digit only' )
        #
    #
    if not isBogusPhone(                  ''   ):
        #
        lProblems.append( 'isBogusPhone() blank' )
        #
    #
    if not isBogusPhone(  '               "'   ):
        #
        lProblems.append( 'isBogusPhone() double quote' )
        #
    #
    if      not isBogusPhone(        '0705551212'   ):
        #
        lProblems.append( 'isBogusPhone() Netherlands directory assistance' )
        #
    #
    # 4151540000  in Mexico 43 times
    # 4151520000  in Mexico 12 times
    #
    # 0705551212  in Netherlands 17 times
    # 0205551212  in Netherlands 15 times
    #
    # 39055503131 in Italy 12 times
    #
    # 020 7722 0101 in UK 11 times
    #
    # 49 36601 82260 in Germany 10 times
    #
    # 2688-8854     in India 23 times
    # 91-11-2688-8854 in India 12 times
    #
    # 31-417-3190 in South Korea 8 times
    #
    #
    if not isPhoneUSA( '1-206-632-9929' ):
        #
        lProblems.append( 'isPhoneUSA() starts with 1 dash separates' )
        #
    #
    if not isPhoneUSA(   '206-632-9929' ):
        #
        lProblems.append( 'isPhoneUSA() starts w area code dash separates' )
        #
    #
    if not isPhoneUSA(   '(206) 632-9929' ):
        #
        lProblems.append( 'isPhoneUSA() starts w area code dash separates' )
        #
    #
    if not isPhoneUSA(   '212-410-9633' ):
        #
        lProblems.append( 'isPhoneUSA() NYC number' )
        #
    #
    if isPhoneUSA(   '212-010-9633' ):
        #
        lProblems.append( 'isPhoneUSA() cannot begin with 0 or 1' )
        #
    #
    if not isLikePhoneUSA( '212-410-9633' ):
        #
        lProblems.append( 'isLikePhoneUSA() NYC number' )
        #
    #
    if     isPhoneUSA(   '08 9018 1075' ):
        #
        lProblems.append( 'isPhoneUSA() Thailand number' )
        #
    #
    if False and not isPhoneCanada( '1-416-538-1352' ):
        #
        lProblems.append( 'isPhoneCanada() starts with 1 dash separates' )
        #
    #
        
    if      not isValidPhone( '12062862181' ) or \
                isValidPhone( 'same'        ) or \
                isValidPhone( 'n/a'         ):
        #
        lProblems.append( 'isValidPhone()' )
        #
    #
    tValidPhonesHK = (
        '85291925529',
        '2530 0728',
        '6532-3831 x6483',
        '852-2848-5360',
        '852 2813 1204',
        '+852 6330 3505',
        '60814418',
        '852 966-77-149',
        '011 852 9360-6310',
        '(852) 90421365',
        '011 852 2888 1210', )
    #
    if get1stThatFails( tValidPhonesHK, isPhoneHK ):
        #
        lProblems.append( 'isPhoneHK() %s' %
                            get1stThatFails( tValidPhonesHK, isPhoneHK ) )
        #
    #
    tInvalidPhonesHK = (
        '135-0109-9234',
        '7034963251',
        '1-732-333-4616',
        '+86-13911180425',
        '14016883174', )
    #
    if get1stThatMeets( tInvalidPhonesHK, isPhoneHK ):
        #
        lProblems.append( 'isPhoneHK() %s' %
                            get1stThatMeets( tInvalidPhonesHK, isPhoneHK ) )
        #
    #
    if getStateGotAreaCode( '212' ) != 'NY':
        #
        lProblems.append( 'getStateGotAreaCode() 212' )
        #
    if getStateGotAreaCode( '206' ) != 'WA':
        #
        lProblems.append( 'getStateGotAreaCode() 206' )
        #
    if getStateGotAreaCode( '717' ) != 'PA':
        #
        lProblems.append( 'getStateGotAreaCode() 717' )
        #
    if getStateGotAreaCode( '202' ) != 'DC':
        #
        lProblems.append( 'getStateGotAreaCode() 202' )
        #
        #
    #
    if isCountryCode( 'xyz' ):
        #
        lProblems.append( 'isCountryCode() xyz' )
        #
    #
    if isCountryCode( 'xyz' ):
        #
        lProblems.append( 'isCountryCode() xyz' )
        #
    #
    if not isCountryCode( '49' ):
        #
        lProblems.append( 'isCountryCode() 49 Germany' )
        #
    #
    sPhoneOrig              = '+447924406909'
    sPhoneDigits            = '447924406909'
    sThisCountryDialingCode = '39'
    #
    sOtherCountryCode = hasObviousOtherCountryCode(
            sPhoneOrig, sPhoneDigits, sThisCountryDialingCode, [], [] )
    #
    if sOtherCountryCode != '44':
        #
        lProblems.append( 'hasObviousOtherCountryCode() +447924406909 Italy' )
        #
    #
    sPhoneOrig = '+1 212 555-1212'
    #
    bLikePhoneUSA, bFormatLikeUSA = isFormatOrLikeUSA( sPhoneOrig )
    #
    if not bFormatLikeUSA:
        #
        lProblems.append( 'isFormatOrLikeUSA() +1 212 555-1212' )
        #
    #
    sPhoneOrig = '12125551212'
    #
    bLikePhoneUSA, bFormatLikeUSA = isFormatOrLikeUSA( sPhoneOrig )
    #
    if bFormatLikeUSA:
        #
        lProblems.append( 'isFormatOrLikeUSA() 12125551212' )
        #
    #
    sPhoneOrig = '+1 212 5551212'
    #
    bLikePhoneUSA, bFormatLikeUSA = isFormatOrLikeUSA( sPhoneOrig )
    #
    if not bFormatLikeUSA:
        #
        lProblems.append( 'isFormatOrLikeUSA() +1 212 5551212' )
        #
    #
    sPhoneOrig = '212555-1212'
    #
    bLikePhoneUSA, bFormatLikeUSA = isFormatOrLikeUSA( sPhoneOrig )
    #
    if not bLikePhoneUSA:
        #
        lProblems.append( 'bLikePhoneUSA() 212555-1212' )
        #
    #
    if bFormatLikeUSA:
        #
        lProblems.append( 'isFormatOrLikeUSA() 212555-1212' )
        #
    #
    sPhoneOrig              = '0207 737 0107'
    #
    if bFormatLikeUSA:
        #
        lProblems.append( 'isFormatOrLikeUSA() 0207 737 0107' )
        #
    #
    sPhoneOrig              = '917 696 0477'
    #
    bLikePhoneUSA, bFormatLikeUSA = isFormatOrLikeUSA( sPhoneOrig )
    #
    if not bFormatLikeUSA:
        #
        lProblems.append( 'isFormatOrLikeUSA() 917 696 0477' )
        #
    #
    bLikePhoneUSA, bFormatLikeUSA = isFormatOrLikeUSA( sPhoneOrig )
    #
    if 'Canada' not in setNoAmNumbPlanCountries:
        #
        lProblems.append( 'setNoAmNumbPlanCountries Canada should be in' )
        #
    #
    if 'Thailand' in setNoAmNumbPlanCountries:
        #
        lProblems.append( 'setNoAmNumbPlanCountries Thailand should not be in' )
        #
    #
    sPhone = '+1 212 555-1212'
    #
    if isPhoneCanada( sPhone ):
        #
        lProblems.append( 'isPhoneCanada() NYC # should not be in' )
        #
    #
    if isPhoneCaribbean( sPhone ):
        #
        lProblems.append( 'isPhoneCaribbean() NYC # should not be in' )
        #
    #
    sPhone = '+1 709 555-1212'
    #
    if not isPhoneCanada( sPhone ):
        #
        lProblems.append( 'isPhoneCanada() 709 should be in' )
        #
    #
    sPhone = '19376603668'
    # 
    if isPhoneCanada( sPhone ):
        #
        lProblems.append( 'isPhoneCanada() 937 is OH, should be out' )
        #
    #
    sPhone = '19376603668'
    #
    bLikePhoneUSA, bFormatLikeUSA = isFormatOrLikeUSA( sPhone )
    #
    if not bLikePhoneUSA:
        #
        lProblems.append( 'bLikePhoneUSA() 19376603668' )
        #
    #
    sPhone = '202957-0088'
    #
    bLikePhoneUSA, bFormatLikeUSA = isFormatOrLikeUSA( sPhone )
    #
    if not bLikePhoneUSA:
        #
        lProblems.append( 'bLikePhoneUSA() 202957-0088' )
        #
    #
    sAreaCodeMaybe  = '206' # Seattle
    #
    if not isAreaCodeForUSA( sAreaCodeMaybe ):
        #
        lProblems.append( 'isAreaCodeForUSA() 206 Seattle' )
        #
    #
    sAreaCodeMaybe  = '236' # British Columba
    #
    if isAreaCodeForUSA( sAreaCodeMaybe ):
        #
        lProblems.append( 'isAreaCodeForUSA() 236 BC' )
        #
    #
    sPhoneOrig              = '001 0049 171 363 7987'
    sPhoneDigits            = '00100491713637987'
    sThisCountryDialingCode = '49'
    #
    sOtherCountryCode = hasObviousOtherCountryCode(
            sPhoneOrig, sPhoneDigits, sThisCountryDialingCode, [], [] )
    #
    if sOtherCountryCode != '':
        #
        print3( 'sOtherCountryCode: ', sOtherCountryCode ) 
        lProblems.append( 'hasObviousOtherCountryCode() 001 0049 171 363 7987 Germany' )
        #
    #
    sPhoneOrig              = '011 4 32763441'
    sPhoneDigits            = '011432763441'
    sThisCountryDialingCode = '33'
    #
    sOtherCountryCode = hasObviousOtherCountryCode(
            sPhoneOrig, sPhoneDigits, sThisCountryDialingCode, [], [] )
    #
    if sOtherCountryCode != '':
        #
        print3( 'sOtherCountryCode: ', sOtherCountryCode ) 
        lProblems.append( 'hasObviousOtherCountryCode() 011 4 32763441 France' )
        #
    #
    sPhoneOrig              = '+223 301688'
    sPhoneDigits            = '223 301688'
    sThisCountryDialingCode = '33'
    #
    sOtherCountryCode = hasObviousOtherCountryCode(
            sPhoneOrig, sPhoneDigits, sThisCountryDialingCode, [], [] )
    #
    if sOtherCountryCode != '223':
        #
        print3( 'sOtherCountryCode: ', sOtherCountryCode ) 
        lProblems.append( 'hasObviousOtherCountryCode() +223 301688 France' )
        #
    #
    sPhoneOrig              = '0041 7879818044'
    sPhoneDigits            = '00417879818044'
    sThisCountryDialingCode = '44'
    #
    sOtherCountryCode = hasObviousOtherCountryCode(
            sPhoneOrig, sPhoneDigits, sThisCountryDialingCode, [], [] )
    #
    if sOtherCountryCode != '41':
        #
        lProblems.append( 'hasObviousOtherCountryCode() 0041 7879818044 UK' )
        #
    #
    sPhoneOrig              = '011447924406909'
    sPhoneDigits            = '011447924406909'
    sThisCountryDialingCode = '39'
    #
    sOtherCountryCode = hasObviousOtherCountryCode(
            sPhoneOrig, sPhoneDigits, sThisCountryDialingCode, [], [] )
    #
    if sOtherCountryCode != '44':
        #
        lProblems.append( 'hasObviousOtherCountryCode() 011447924406909 Italy' )
        #
    #
    sPhoneOrig              = '33631126088'
    sPhoneDigits            = '33631126088'
    sThisCountryDialingCode = '33'
    #
    sOtherCountryCode = hasObviousOtherCountryCode(
            sPhoneOrig, sPhoneDigits, sThisCountryDialingCode, [], [] )
    #
    if sOtherCountryCode != '':
        #
        print3( 'sOtherCountryCode: ', sOtherCountryCode ) 
        lProblems.append( 'hasObviousOtherCountryCode() 33631126088 France' )
        #
    '''
    #
    '''
    #
    sPhoneOrig              = '011 250 353-9685'
    sPhoneDigits            = '0112503539685'
    sThisCountryDialingCode = '1'
    #
    sOtherCountryCode = hasObviousOtherCountryCode(
            sPhoneOrig, sPhoneDigits, sThisCountryDialingCode, [], [] )
    #
    if sOtherCountryCode != '250':
        #
        print3( 'sOtherCountryCode: ', sOtherCountryCode ) 
        lProblems.append( 'hasObviousOtherCountryCode() 011 250 353-9685 Canada' )
        #
    #
    sPhoneOrig              = '001-40-22697638'
    sPhoneDigits            = '0014022697638'
    sThisCountryDialingCode = '49'
    #
    sOtherCountryCode = hasObviousOtherCountryCode(
            sPhoneOrig, sPhoneDigits, sThisCountryDialingCode,
            [3, 2, 8], ['001', '40', '22697638'] )
    #
    if sOtherCountryCode != '40':
        #
        lProblems.append( 'hasObviousOtherCountryCode() 001-40-22697638 Italy' )
        #
    #
    if isPhoneNoAmDialingPlan( sPhoneOrig ):
        #
        lProblems.append( 'isPhoneNoAmDialingPlan() 001-40-22697638' )
    #
    sPhone = '+1 201-984-5835'
    #
    sAreaCode = getAreaCode( sPhone )
    #
    if sAreaCode != '201':
        #
        lProblems.append( 'getAreaCode() +1 201-984-5835' )
        #
    #
    sPhone = '334 9583672'
    #
    if isFormatLikeUSA( sPhone ):
        #
        lProblems.append( 'isFormatLikeUSA() 334 9583672' )
        #
    #
    sPhone = '334 9583672'
    #
    if hasExtension( sPhone ):
        #
        lProblems.append( 'hasExtension() no extension' )
        #
    #
    if not isPhoneNo( sPhone ):
        #
        lProblems.append( 'isPhoneNo( %s )' % sPhone )
        #
    #
    sPhone = '334 9583672 # 123'
    #
    if not hasExtension( sPhone ):
        #
        lProblems.append( 'hasExtension() has extension' )
        #
    #
    if not isPhoneNo( sPhone ):
        #
        lProblems.append( 'isPhoneNo( %s )' % sPhone )
        #
    #
    sPhone = '334 9583672 x 123'
    lExtension = hasExtension( sPhone )
    #
    if not lExtension:
        #
        print3( 'lExtension:', lExtension )
        lProblems.append( 'hasExtension() has extension' )
        #
    #
    sPhone = '334 9583672 Mx 123'
    lExtension = hasExtension( sPhone )
    #
    if lExtension:
        #
        print3( 'lExtension:', lExtension )
        lProblems.append( 'hasExtension() not an extension' )
        #
    #
    sPhone = '334 9583672 x 123'
    #
    if getDigitCount( sPhone ) != 10:
        #
        print3( "getDigitCount( '334 9583672 x 123' ):", getDigitCount( sPhone ) )
        lProblems.append( 'getDigitCount() has extension' )
        #
    #
    sPhone = '+1 201-984-5835'
    #
    if getDigitCount( sPhone ) != 11:
        #
        print3( "getDigitCount( '+1 201-984-5835' ):", getDigitCount( sPhone ) )
        lProblems.append( 'getDigitCount() no extension' )
        #
    #
    if not isPhoneNoAmDialingPlan( sPhone ):
        #
        lProblems.append( 'isPhoneNoAmDialingPlan() +1 201-984-5835' )
    #
    #
    if not isPhoneNo( sPhone ):
        #
        lProblems.append( 'isPhoneNo( %s )' % sPhone )
        #
    #
    sPhone = 'spam and eggs'
    #
    if getDigitCount( sPhone ) != 0:
        #
        lProblems.append( 'getDigitCount() all alpha' )
        #
    #
    if isValidPhone( sPhone ):
        #
        lProblems.append( 'isValidPhone( %s )' % sPhone )
        #
    #
    #
    sPhone = '334 9583672 x 123'
    #
    if getNumberDropExtension( sPhone ) != '334 9583672':
        #
        lProblems.append( 'getNumberDropExtension()' )
        #
    #
    #
    sPhone = '+250 3539685'
    #
    if isPhoneNoAmDialingPlan( sPhone ):
        #
        lProblems.append( 'isPhoneNoAmDialingPlan() +250 3539685' )
    #
    #
    if isPhoneCanada( sPhone ):
        #
        lProblems.append( 'isPhoneCanada() +250 3539685' )
    #
    if not isPhoneNo( sPhone ):
        #
        lProblems.append( 'isPhoneNo( %s )' % sPhone )
        #
    #
    sPhone = '+1 345 555-1212'
    #
    if not isPhoneCaribbean( sPhone ):
        #
        lProblems.append( 'isPhoneCaribbean() 345 should be in' )
        #
    #
    sPhone = '604-264-7570' # BC Canada number
    #
    if not isFormatOrLikeUSA( sPhone ):
        #
        lProblems.append( 'isFormatOrLikeUSA() 604-264-7570' )
        #
    #
    #
    sPhone = '8030430150'
    #
    if isPhoneNoAmDialingPlan( sPhone ):
        #
        lProblems.append( 'isPhoneNoAmDialingPlan() 8030430150' )
        #
    #
    sPhone = '020 5555 5555'
    #
    if not isBogusPhone( sPhone ):
        #
        lProblems.append( 'isBogusPhone() 020 5555 5555' )
        #
    #
    if not isPhoneNo( sPhone ):
        #
        lProblems.append( 'isPhoneNo( %s )' % sPhone )
        #
    #
    sPhone = '0041 218282000'
    #
    if isBogusPhone( sPhone, bExplain = True ):
        #
        lProblems.append( 'isBogusPhone() 0041 218282000' )
        #
    #
    if not isPhoneNo( sPhone ):
        #
        lProblems.append( 'isPhoneNo( %s )' % sPhone )
        #
    #
    sPhone = '011 44 20 7033 0000'
    #
    if isBogusPhone( sPhone, bExplain = True ):
        #
        lProblems.append( 'isBogusPhone() 011 44 20 7033 0000' )
        #
    #
    #
    sPhone = '(781) 062-2337'
    #
    if isFormatLikeUSA( sPhone ):
        #
        lProblems.append( 'isFormatLikeUSA() (781) 062-2337' )
        #
    #
    if not isPhoneNo( sPhone ):
        #
        lProblems.append( 'isPhoneNo( %s )' % sPhone )
        #
    #
    sPhone = '01483 273 0890'
    #
    if isPhoneUK( sPhone ):
        #
        lProblems.append( 'isPhoneUK() 01483 273 0890 too many digits' )
        #
    #
    sPhone = '403-381-8691'
    #
    if isPhoneUK( sPhone ):
        #
        lProblems.append( 'isPhoneUK() 403-381-8691 Calgary AB' )
        #
    #
    if not isPhoneNo( sPhone ):
        #
        lProblems.append( 'isPhoneNo( %s )' % sPhone )
        #
    #
    sPhone = '0048505490185'
    #
    if isPhoneUK( sPhone ):
        #
        lProblems.append( 'isPhoneUK() 0048505490185 Polish' )
        #
    #
    sPhone = '20777948973'
    #
    if isPhoneUK( sPhone ):
        #
        lProblems.append( 'isPhoneUK() 20777948973 UK missing zero too many digits' )
        #
    #
    sPhone = '1415-738 7369'
    #
    if isPhoneUK( sPhone ):
        #
        lProblems.append( 'isPhoneUK() 1415-738 7369 CA' )
        #
    #
    sPhone = '02392356713'
    #
    if not isPhoneUK( sPhone ):
        #
        lProblems.append( 'isPhoneUK() 02392356713 UK London land line' )
        #
    #
    sPhone = '(0)747 222 4322'
    #
    if not isPhoneUK( sPhone ):
        #
        lProblems.append( 'isPhoneUK() (0)747 222 4322 UK mobile' )
        #
    #
    sPhone = '+44 (0)747 222 4322'
    #
    if not isPhoneUK( sPhone ):
        #
        lProblems.append( 'isPhoneUK() +44 (0)747 222 4322 UK mobile' )
        #
    #
    sPhone = '011 44 (0)747 222 4322'
    #
    if not isPhoneUK( sPhone ):
        #
        lProblems.append( 'isPhoneUK() 011 44 (0)747 222 4322 UK mobile' )
        #
    #
    if not isPhoneNo( sPhone ):
        #
        lProblems.append( 'isPhoneNo( %s )' % sPhone )
        #
    #
    sPhone = '20777948973'
    #
    #
    sIddCode = '1'
    #
    lWant   = ['Canada', 'United States']
    lGot    = getCountryListGotIddCode( sIddCode )
    lGot.sort()
    #
    if lGot != lWant:
        #
        lProblems.append( 'getCountryListGotIddCode() 1' )
        #
        # print3( getCountryListGotIddCode( sIddCode ) )
    #
    #
    sIddCode = '49'
    #
    l = ['Germany']
    #
    if getCountryListGotIddCode( sIddCode ) != l:
        #
        lProblems.append( 'getCountryListGotIddCode() 49' )
        #
    #
    sCountry = 'Kosovo'
    #
    if getCodeGotCountry( sCountry ) != '381':
        #
        lProblems.append( 'getCodeGotCountry() Kosovo' )
        #
    #
    sPhone = '4169244082'
    #
    if not isPhoneCanada( sPhone ):
        #
        lProblems.append( 'isPhoneCanada() 4169244082' )
        #
    #
    if not isPhoneNoAmDialingPlan( sPhone ):
        #
        lProblems.append( 'isPhoneNoAmDialingPlan() 4169244082' )
        #
    #
    if not isPhoneNo( sPhone ):
        #
        lProblems.append( 'isPhoneNo( %s )' % sPhone )
        #
    #
    sPhone = '3223749262'
    #
    if isPhoneNoAmDialingPlan( sPhone ):
        #
        lProblems.append( 'isPhoneNoAmDialingPlan() ' + sPhone )
        #
    #
    sPhone = '++49-(0)-6131 - 475556'
    #
    oPhone = getDigitsOtherObject( sPhone )
    #
    lDigits = ['49', '0', '6131', '475556']
    lOthers = ['++', '-(', ')-', ' - ']
    lParts  = ['++', '49', '-(', '0', ')-', '6131', ' - ', '475556']
    lWhich  = ['o', 'd', 'o', 'd', 'o', 'd', 'o', 'd']
    #
    if (    oPhone.lDigits != lDigits or
            oPhone.lOthers != lOthers or
            oPhone.lParts  != lParts  or
            oPhone.lWhich  != lWhich  ):
        #
        lProblems.append( 'getDigitsOtherObject() ' + sPhone )
        #
    #
    sPhone = '++49-(0)-6131 - 475556 x'
    #
    oPhone = getDigitsOtherObject( sPhone )
    #
    #
    #
    '''
    '''
    sayTestResult( lProblems )