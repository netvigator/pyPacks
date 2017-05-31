#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# SnailMail sMail functions get
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
from String.Find import getFinderFindAll, getFinder

oZipPlus4Finder  = getFinderFindAll( r'\d{5}-?\d{4}',
                                            bCaseSensitive = True )

oZip5Finder      = getFinderFindAll( r'\b\d{5}\b(?!\-)',
                                            bCaseSensitive = True )

oZipsAllFinder   = getFinderFindAll( r'\b\d{5}-?\d{4}\b|\b\d{5}\b(?!\-)',
                                            bCaseSensitive = True )

_oFloorFinder    = getFinderFindAll(
        r'\b(fl(?:oor)? ?\d+)|'
        r'\b((?:\d*1st|\d*2nd|\d*3rd|\d+th|ground) ?(?:fl|floor))\b' )

oUnitFinder      = getFinder(
        r"((?:(?:#)|\b(?:unit|apt\.?|ste\.?)) *"
        r"[a-zA-Z]? *[-#]? *\d* *[-a-zA-Z]{0,2})\b" )



def getCodeFromString( s, oFinder ):
    #
    lCodes = oFinder( s )
    #
    sCode = ''
    #
    if lCodes: sCode = lCodes[0]
    #
    return sCode


def getZipPlus4( s ):
    #
    '''extract zip+4 from jumble of text'''
    #
    return getCodeFromString( s, oZipPlus4Finder )


def getZip5( s ):
    #
    return getCodeFromString( s, oZip5Finder )


def getZipAny( s ):
    #
    return getCodeFromString( s, oZipsAllFinder )


def getCodeCA( s ):
    #
    from sMail.Test      import oPCodeFinderCA
    from String.Dumpster import getWhiteWiped
    #
    sCode = getCodeFromString( getWhiteWiped( s ), oPCodeFinderCA ).upper()
    #
    if sCode:
        #
        sCode = '%s %s' % ( sCode[ : 3 ], sCode[ -3 : ] )
        #
        if sCode[1] == 'O': # letter O not zero
            #
            sCode = '%s0%s' % ( sCode[ 0 ], sCode[ 2 : ] )
    #
    return sCode



def getZipPlus4Separates( sZipPlus4 ):
    #
    from sMail.Test import isZipPlus4
    #
    sZip5   = sZipPlus4
    sPlus4  = ''
    #
    if isZipPlus4( sZipPlus4 ):
        #
        if '-' in sZipPlus4:
            sZip5, sPlus4 = sZipPlus4.split( '-' )
        else:
            sZip5  = sZipPlus4[ :  5 ]
            sPlus4 = sZipPlus4[ -4 : ]
        #
    #
    return sZip5, sPlus4



def getZip5GotZipPlus4( sZipPlus4 ):
    #
    sZip5, sPlus4 = getZipPlus4Separates( sZipPlus4 )
    #
    return sZip5


def getZipPlus4offSeparates( *args ):
    #
    if len( args ) == 2 and args[1]:
        #
        sZipPlus4 = '-'.join( args )
        #
    else:
        #
        sZipPlus4 = args[0]
        #
    #
    return sZipPlus4



def getProperZipPlus4( sZip ):
    #
    return getZipPlus4offSeparates( *getZipPlus4Separates( sZip ) )



def getCleanName( sName ):
    #
    '''
    ported from eMail.Get
    '''
    #
    from Iter.AllVers   import iMap
    from String.Get     import getTitleizedIfNeeded
    from String.Replace import getSpaceForWhiteAlsoStrip
    #
    sName = getSpaceForWhiteAlsoStrip( sName )
    #
    lName = sName.split()
    #
    return ' '.join( iMap( getTitleizedIfNeeded, lName ) )



def _getCountryFunctionDict():
    #
    from sMail.Test import \
                isPostalCodeCA, \
                isPostalCodeCorrectCA, \
                isPostCodeOk4ProvinceCA
    #
    d = dict(   isPostalCode            = isPostalCodeCA,
                isPostalCodeCorrect     = isPostalCodeCorrectCA,
                isPostCodeOk4Province   = isPostCodeOk4ProvinceCA,
                getPostCodeBetter       = getCodeCA )
    #
    dCountryFunctions = { 'Canada'    : d }
    #
    return dCountryFunctions


_dCountryFunctions = _getCountryFunctionDict()


def getCountryFunctions( sCountry ):
    #
    from Utils.Get import getTrue
    #
    def returnParam( sParam ): return sParam
    #
    dDefault = dict(
            isPostalCode            = getTrue,
            isPostalCodeCorrect     = getTrue,
            isPostCodeOk4Province   = getTrue,
            getPostCodeBetter       = returnParam )
    #
    return _dCountryFunctions.get( sCountry, dDefault )





def getCareOfRemainder( s ):
    #
    from String.Get      import getTextAfter
    from String.Test     import hasAnyDigits
    #
    sRest = ''
    #
    sDigit = hasAnyDigits( s )
    #
    if ',' in s:
        #
        sRest = getTextAfter( s, ',' )
        #
    elif ';' in s:
        #
        sRest = getTextAfter( s, ';' )
        #
    elif '-' in s:
        #
        sRest = getTextAfter( s, '-' )
        #
    elif sDigit:
        #
        sRest = '%s%s' % ( sDigit, getTextAfter( s, sDigit ) )
        #
    #
    return sRest.strip()



def getFloor( sAddress ):
    #
    from Collect.Get import getLongest
    #
    sFloor = ''
    #
    lFloor = _oFloorFinder( sAddress )
    #
    if lFloor:
        #
        sFloor = getLongest( lFloor[0] )
        #
    #
    return sFloor



def getAptOrUnitNumb( s ):
    #
    from Collect.Get import getLongest
    #
    sUnit = ''
    #
    lUnit = oUnitFinder.findall( s )
    #
    if lUnit:
        #
        sUnit = getLongest( lUnit )
        #
        if sUnit == s:
            #
            lParts = s.split()
            #
            sUnit = lParts[0]
            #
        else:
            #
            sUnit = sUnit.strip()
            #
    #
    return sUnit
    




if __name__ == "__main__":
    #
    from six            import print_ as print3
    #
    from Collect.Get    import getLongest
    from Iter.AllVers   import tMap, tFilter
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    sTable = '''<TABLE BORDER><TR><TD ALIGN=CENTER><B>Your Input</B>
                <TD ALIGN=CENTER><B>Search Result</B>
                <TR><TD>1231 n 48th st<BR>seattle WA <TD>1231 N 48th St<BR>
                Seattle WA 98103-6625</TABLE>'''
    #
    if oZipPlus4Finder( sTable ) != [ '98103-6625' ]:
        #
        lProblems.append( 'oZipPlus4Finder()' )
        #
    #
    if oZipsAllFinder( sTable ) != [ '98103-6625' ]:
        #
        lProblems.append( 'oZipsAllFinder()' )
        #
    #
    if oZip5Finder( sTable ) != []:
        #
        lProblems.append( 'oZip5Finder() zip+4' )
        #
    #
    if oZip5Finder( 'Seattle WA 98103 USA' ) != [ '98103' ]:
        #
        lProblems.append( 'oZip5Finder() zip5' )
        #
    #
    if getZipPlus4( sTable ) != '98103-6625':
        #
        lProblems.append( 'getZipPlus4()' )
        #
    #
    if getZip5( 'Seattle WA 98103 USA' ) != '98103':
        #
        lProblems.append( 'getZip5()' )
        #
    #
    if getZipAny( 'Seattle WA 98103 USA' ) != '98103':
        #
        lProblems.append( 'getZipAny() zip5' )
        #
    #
    if getZipAny( sTable ) != '98103-6625':
        #
        lProblems.append( 'getZipAny() zip+4' )
        #
    #
    if getZipPlus4Separates( '98103-6625' ) != ( '98103', '6625' ):
        #
        lProblems.append( 'getZipPlus4Separates() sent zip+4' )
        #
    #
    if getZipPlus4Separates( '981036625' ) != ( '98103', '6625' ):
        #
        lProblems.append( 'getZipPlus4Separates() sent zip+4' )
        #
    #
    if getZipPlus4Separates( '98103' ) != ( '98103', '' ):
        #
        lProblems.append( 'getZipPlus4Separates() sent zip5' )
        #
    #
    if      getZip5GotZipPlus4( '98103'      ) != '98103' or \
            getZip5GotZipPlus4( '98103-6625' ) != '98103':
        #
        lProblems.append( 'getZip5GotZipPlus4()' )
        #
    #
    if getZipPlus4offSeparates( '98103', '6625' ) != '98103-6625':
        #
        lProblems.append( 'getZipPlus4offSeparates()' )
        #
    #
    if getProperZipPlus4( '981036625' ) != '98103-6625':
        #
        lProblems.append( 'getProperZipPlus4()' )
        #
    #
    sCanada = """"34189";"Owen Sound";"Ontario";"N4K 3A3";"Canada";"295 8th avenue east";NULL"""
    #
    if getCodeCA( sCanada ) != 'N4K 3A3':
        #
        lProblems.append( 'getCodeCA() in string' )
        #
    #
    if getCodeCA( 'n4k3a3' ) != 'N4K 3A3':
        #
        lProblems.append( 'getCodeCA() add space and make upper' )
        #
    #
    if getCodeCA( 'n4k-3a3' ) != 'N4K 3A3':
        #
        lProblems.append( 'getCodeCA() remove dash' )
        #
    #
    if getCodeCA( 'n4ka 3a' ) != 'N4K A3A':
        #
        lProblems.append( 'getCodeCA() space in wrong place' )
        #
    #
    if getCodeCA( 'nok-3a3' ) != 'N0K 3A3':
        #
        lProblems.append( 'getCodeCA() letter O not zero' )
        #
    #
    if getCleanName( "frederick heath, jr. " ) != "Frederick Heath, Jr.":
        #
        lProblems.append( 'getCleanName()' )
        #
    #
    dCountryFunctions = getCountryFunctions( 'Canada' )
    #
    getPostCodeBetter = dCountryFunctions.get( 'getPostCodeBetter' )
    #
    if getPostCodeBetter( 'nok-3a3' ) != 'N0K 3A3':
        #
        lProblems.append( '_getCountryFunctionDict.get getCodeCA() letter O not zero' )
        #
    #
    #
    tRemainders = tMap( getCareOfRemainder,
        (   'c/o Gloria Robertson 3001 Rte. 130',
            'c/o Donley, 609 West Lyon Farm Drive',
            'c/o Bennet; 3261 Cape Cod Ct.',
            'c/o Berlow-Stolls, 500 E. 77th Str.',
            'c/o GE II Distribution',
            'c/o Palm Beach County Courthouse, 205 North Dixie Highway',
            'C/O DAVID R GARNER, RT. 56' ) )
    #
    tWantAdds = (
        '3001 Rte. 130',
        '609 West Lyon Farm Drive',
        '3261 Cape Cod Ct.',
        '500 E. 77th Str.',
        '',
        '205 North Dixie Highway',
        'RT. 56' )
    #
    if tRemainders != tWantAdds:
        #
        lProblems.append( 'getCareOfRemainder()' )
        #
    #
    if getLongest( _oFloorFinder( '3rd fl' )[0] ) != '3rd fl':
        #
        lProblems.append( '_oFloorFinder() 3rd fl' )
        #
    #
    if getLongest( _oFloorFinder( '21st floor' )[0] ) != '21st floor':
        #
        lProblems.append( '_oFloorFinder() 21st floor' )
        #
    #
    if getLongest( _oFloorFinder( '9th fl' )[0] ) != '9th fl':
        #
        lProblems.append( '_oFloorFinder() 9th fl' )
        #
    #
    if getLongest( _oFloorFinder( 'ground fl' )[0] ) != 'ground fl':
        #
        lProblems.append( '_oFloorFinder() ground fl' )
        #
    #
    if getLongest( _oFloorFinder( '2ndfloor' )[0] ) != '2ndfloor':
        #
        lProblems.append( '_oFloorFinder() 2ndfloor' )
        #
    #
    tNegatives = tMap( _oFloorFinder, tWantAdds )
    #
    if tFilter( bool, tNegatives ):
        #
        # print tNegatives
        lProblems.append( '_oFloorFinder() negatives' )
        #
    #
    if getFloor( '1231 N 48th St, 3rd fl' ) != '3rd fl':
        #
        lProblems.append( 'getFloor() 3rd fl' )
        #
    #
    if getFloor( '1231 N 48th St, 21st floor' ) != '21st floor':
        #
        lProblems.append( 'getFloor() 21st floor' )
        #
    #
    if getFloor( '1231 N 48th St, 9th fl') != '9th fl':
        #
        lProblems.append( 'getFloor() 9th fl' )
        #
    #
    if getFloor( '1231 N 48th St, 2ndfloor' ) != '2ndfloor':
        #
        lProblems.append( 'getFloor() 2ndfloor' )
        #
    #
    if getFloor( '283 St Pauls Ave Fl 3' ) != 'Fl 3':
        #
        lProblems.append( 'getFloor() Fl 3' )
        #
    #
    if getFloor(
            "257 Comelison Avenue- 4th Floor, Hudson County Plaza"
            ) != '4th Floor':
        #
        lProblems.append( 'getFloor() 4th Floor' )
        #
    #
    tNegatives = tMap( getFloor, tWantAdds )
    #
    if tFilter( bool, tNegatives ):
        #
        # print tNegatives
        lProblems.append( 'getFloor() negatives' )
        #
    #
    if getAptOrUnitNumb( "117 (not absolutely sure) Stensen St." ):
        print3( getAptOrUnitNumb( "117 (not absolutely sure) Stensen St." ) )
        lProblems.append( 'getAptOrUnitNumb() 117 (not absolutely sure) Stensen St' )
        #
    #
    if getAptOrUnitNumb( '158 BALTIC ST; #3' ) != '#3':
        print3( getAptOrUnitNumb( '158 BALTIC ST; #3' ) )
        lProblems.append( 'getAptOrUnitNumb() #number' )
        #
    #
    if getAptOrUnitNumb( '900 S LAMAR BLVD APT 313' ) != 'APT 313':
        #
        lProblems.append( 'getAptOrUnitNumb() apt number' )
        #
    #
    if getAptOrUnitNumb( '6724 RAMBLEWOOD DR APT L' ) != 'APT L':
        #
        lProblems.append( 'getAptOrUnitNumb() apt L' )
        #
    #
    if getAptOrUnitNumb( '20 E 35TH ST APT 11-J' ) != 'APT 11-J':
        #
        lProblems.append( 'getAptOrUnitNumb() apt 11-J' )
        #
    #
    if getAptOrUnitNumb( '684 WASHINGTON ST #3A' ) != '#3A':
        #
        lProblems.append( 'getAptOrUnitNumb() #3A' )
        #
    #
    if getAptOrUnitNumb( '2531 S 248TH ST #A - 15' ) != '#A - 15':
        #
        lProblems.append( 'getAptOrUnitNumb() #A - 15' )
        #
    #
    if getAptOrUnitNumb( '6116 S GREENWOOD AVE UNIT #D' ) != 'UNIT #D':
        #
        lProblems.append( 'getAptOrUnitNumb() UNIT #D' )
        #
    #
    if getAptOrUnitNumb( '#F210, 939 Buena Vista SE' ) != '#F210':
        #
        lProblems.append( 'getAptOrUnitNumb() unit on front' )
        #
    #
    if getAptOrUnitNumb( '#F210 939 BUENA VIS SE' ) != '#F210':
        #
        lProblems.append( 'getAptOrUnitNumb()unit on front' )
        #
    #
    if getAptOrUnitNumb(
            "Apt T2, 6622 Bonnie Ridge Drive, Mt Washington"
            ) != 'Apt T2':
        #
        lProblems.append( 'getAptOrUnitNumb() alphanum unit' )
        #
    #
    if getAptOrUnitNumb(
            "Hopkinson House, Apt. 2113, 602 Washington Square South"
            ) != 'Apt. 2113':
        #
        lProblems.append( 'getAptOrUnitNumb() alphanum unit' )
        #
    #
    if getAptOrUnitNumb(
            "120 Country Club Drive #42 Village at Incline Condos"
            ) != '#42':
        #
        lProblems.append( 'getAptOrUnitNumb() #42 Village at Incline Condos' )
        #
    #
    if getFloor(
            "257 Comelison Avenue- 4th Floor, Hudson County Plaza"
            ) != '4th Floor':
        #
        print3( getFloor(
            "257 Comelison Avenue- 4th Floor, Hudson County Plaza" ) )
        lProblems.append( 'getFloor() in the middle' )
        #
    #
    # _oFloorFinder( '61 Groove St. 1st Floor' )
    #
    sayTestResult( lProblems )
