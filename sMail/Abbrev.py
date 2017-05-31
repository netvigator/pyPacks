#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# sMail functions Abbrev Abbreviations
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
# Copyright 2010-2014 Rick Graves
#

'''
http://www.usps.com/ncsc/lookups/usps_abbreviations.html
from File.Get import getListFromFileLines
from File.Write import putListInTemp

lStates = getListFromFileLines( 'states.txt' )
from String.Output import BetterTitle
lStateCodes = []
for i in r@nge( 0, len(lStates), 2 ):
  sState = BetterTitle( lStates[i] )
  sCode  = lStates[i+1]
  lStateCodes.append( ( sCode, sState ) )

putListInTemp( lStateCodes )

lAbbrevs = getListFromFileLines( 'states.txt' )

setAbbrevs = set( [] )
for s in lAbbrevs:
    s.strip()
    l = s.split()
    if len( l ) <= 1: continue
    if '*' in l[-1]: del l[-1]
    if l[0] == l[-1]: continue
    setAbbrevs.add( ( l[0], l[-1] ) )
    if len( l ) <= 2: continue
    if l[-1] == l[-2]: continue
    setAbbrevs.add( ( l[-2], l[-1] ) )

l = list( setAbbrevs )
l.sort()
putListInTemp( l )


'''
from Dict.Get           import getReverseDictGotUniqueItems
from String.Transform   import getSwapper

tCodesStates = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AS', 'American Samoa'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('DC', 'District of Columbia'),
    ('FM', 'Federated States of Micronesia'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('GU', 'Guam'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MH', 'Marshall Islands'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('MP', 'Northern Mariana Islands'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PW', 'Palau'),
    ('PA', 'Pennsylvania'),
    ('PR', 'Puerto Rico'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VI', 'Virgin Islands'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming') )

dCodesStates = dict( tCodesStates )


dAbbrevProvincesCA = dict(
    AB = 'Alberta',
    BC = 'British Columbia',
    MB = 'Manitoba',
    NB = 'New Brunswick',
    NL = 'Newfoundland and Labrador',
    NT = 'Northwest Territories',
    NS = 'Nova Scotia',
    NU = 'Nunavut',
    ON = 'Ontario',
    PE = 'Prince Edward Island',
    QC = 'Quebec',
    SK = 'Saskatchewan',
    YT = 'Yukon' )

dProvinceCAAbbrev = getReverseDictGotUniqueItems( dAbbrevProvincesCA )

dCodesProvAbbrevCA = dict(
    A = 'NL',
    B = 'NS',
    C = 'PE',
    E = 'NB',
    G = 'QC',
    H = 'QC',
    J = 'QC',
    K = 'ON',
    L = 'ON',
    M = 'ON',
    N = 'ON',
    P = 'ON',
    R = 'MB',
    S = 'SK',
    T = 'AB',
    V = 'BC',
    X = 'NT',
    Y = 'YT' )
#    X = 'NU',


def getCodeGotProvinceCA( sProv ):
    #
    return dProvinceCAAbbrev.get( sProv, '?!' )


def getProvinceAbbrevOffCodeCA( sCode ):
    #
    return dCodesProvAbbrevCA.get( sCode, '??' )



def getAbbrevOffProvinceOrCodeCA( sProv, sCode ):
    #
    sAbbrev = getCodeGotProvinceCA( sProv )
    #
    if sAbbrev == '?!':
        #
        sAbbrev = getProvinceAbbrevOffCodeCA( sCode[ : 1 ] )
        #
    #
    return sAbbrev




def getStateGotCode( sCode ):
    #
    return dCodesStates.get( sCode.upper(), '' )


def getStateCodeDict():
    #
    from Iter.Get import getIterSwapValueKey
    #
    return dict( getIterSwapValueKey( tCodesStates ) )


dStatesCodes = getStateCodeDict()


def getCodeGotState( sState ):
    #
    '''
    pass state name
    return 2-letter state code
    '''
    #
    from String.Output import BetterTitle
    #
    sCode = dStatesCodes.get( sState.upper(), '' )
    #
    if not sCode: sCode = dStatesCodes.get( BetterTitle( sState ), '' )
    #
    return sCode


def getCodeGotStateOrCode( sState ):
    #
    if len( sState ) == 2:
        sReturnState = sState
    else:
        sReturnState = getCodeGotState( sState )
    #
    return sReturnState



def getStateCode( sMessy ):
    #
    from sMail.Test import oFinderStateCode
    #
    lCodes = oFinderStateCode( sMessy )
    #
    sStateCode = ''
    #
    if lCodes:
        #
        sStateCode = lCodes[0]
        #
    #
    return sStateCode


def getStateName( sMessy ):
    #
    '''
    extract state name from messy HTML
    '''
    #
    from sMail.Test import oFinderStateName
    #
    sMessy = sMessy.replace( '&nbsp;', ' ' )
    #
    lStates = oFinderStateName( sMessy )
    #
    sState = ''
    #
    if lStates:
        #
        sState = lStates[0]
        #
    #
    return sState

# Military Postal Service Agency (MPSA)
setMPSA = frozenset( ( 'AA', 'AE', 'AP' ) )


# https://www.usps.com/send/official-abbreviations.htm
# pls others on top

# taken out because of google geocoding confusion:
#    ('SUMMIT', 'SMT'),
#    ('MISSION', 'MSN'),
#    ('RIVER', 'RIV'),
#    ('TRAIL', 'TRL'),
#    ('TRAILS', 'TRL'),
#    ('KEY', 'KY'),
#    ('KEYS', 'KYS'),
#    ('CAMP', 'CP'),
#    ('MILL', 'ML'),
#    ('VALLEY', 'VLY'),
#    ('VALLEYS', 'VLYS'),
#    ('VISTA', 'VIS'),
#    ('WELL', 'WL'),
#    ('WELLS', 'WLS')
#    ('BEACH', 'BCH'),
#    ('BEND', 'BND'),
#    ('CLUB', 'CLB'),
#    ('DAM', 'DM'),
#    ('FALLS', 'FLS'),
#    ('FORD', 'FRD'),
#    ('FORDS', 'FRDS'),
#    ('FORG', 'FRG'),
#    ('FORGE', 'FRG'),
#    ('FORGES', 'FRGS'),
#    ('FORK', 'FRK'),
#    ('FORKS', 'FRKS'),
#    ('HILL', 'HL'),
#    ('HILLS', 'HLS'),
#    ('MANOR', 'MNR'),
#    ('MANORS', 'MNRS'),
#    ('NECK', 'NCK'),
#    ('PINE', 'PNE'),
#    ('PINES', 'PNES'),
#    ('PLAZA', 'PLZ'),
#    ('PLZA', 'PLZ'),
#    ('RANCH', 'RNCH'),
#    ('RANCHES', 'RNCH'),
#    ('REST', 'RST'),
#    ('STATION', 'STA'),
#    ('STATN', 'STA'),
#    ('STN', 'STA'),
#    ('FOREST', 'FRST'),
#    ('FORESTS', 'FRST'),

tAbbreviations = (
    ('NORTH', 'N'),
    ('SOUTH', 'S'),
    ('EAST', 'E'),
    ('WEST', 'W'),
    ('NO', 'N'),
    ('SO', 'S'),
    ('ALLEE', 'ALY'),
    ('ALLEY', 'ALY'),
    ('ALLY', 'ALY'),
    ('ANEX', 'ANX'),
    ('ANNEX', 'ANX'),
    ('ANNX', 'ANX'),
    ('APARTMENT', 'APT'),
    ('ARCADE', 'ARC'),
    ('AV', 'AVE'),
    ('AVEN', 'AVE'),
    ('AVENU', 'AVE'),
    ('AVENUE', 'AVE'),
    ('AVN', 'AVE'),
    ('AVNUE', 'AVE'),
    ('BASEMENT', 'BSMT'),
    ('BAYOO', 'BYU'),
    ('BAYOU', 'BYU'),
    ('BLUF', 'BLF'),
    ('BLUFF', 'BLF'),
    ('BLUFFS', 'BLFS'),
    ('BOT', 'BTM'),
    ('BOTTM', 'BTM'),
    ('BOTTOM', 'BTM'),
    ('BOUL', 'BLVD'),
    ('BOULEVARD', 'BLVD'),
    ('BOULV', 'BLVD'),
    ('BRANCH', 'BR'),
    ('BRDGE', 'BRG'),
    ('BRIDGE', 'BRG'),
    ('BRNCH', 'BR'),
    ('BROOK', 'BRK'),
    ('BROOKS', 'BRKS'),
    ('BUILDING', 'BLDG'),
    ('BURG', 'BG'),
    ('BURGS', 'BGS'),
    ('BYPA', 'BYP'),
    ('BYPAS', 'BYP'),
    ('BYPASS', 'BYP'),
    ('BYPS', 'BYP'),
    ('CANYN', 'CYN'),
    ('CANYON', 'CYN'),
    ('CAPE', 'CPE'),
    ('CAUSEWAY', 'CSWY'),
    ('CAUSWAY', 'CSWY'),
    ('CEN', 'CTR'),
    ('CENT', 'CTR'),
    ('CENTER', 'CTR'),
    ('CENTERS', 'CTRS'),
    ('CENTR', 'CTR'),
    ('CENTRE', 'CTR'),
    ('CIRC', 'CIR'),
    ('CIRCL', 'CIR'),
    ('CIRCLE', 'CIR'),
    ('CIRCLES', 'CIRS'),
    ('CLIFF', 'CLF'),
    ('CLIFFS', 'CLFS'),
    ('CMP', 'CAMP'),
    ('CNTER', 'CTR'),
    ('CNTR', 'CTR'),
    ('CNYN', 'CYN'),
    ('COMMON', 'CMN'),
    ('COMMONS', 'CMNS'),
    ('CORNER', 'COR'),
    ('CORNERS', 'CORS'),
    ('COURSE', 'CRSE'),
    ('COURT', 'CT'),
    ('COURTS', 'CTS'),
    ('COVE', 'CV'),
    ('COVES', 'CVS'),
    ('CRCL', 'CIR'),
    ('CRCLE', 'CIR'),
    ('CREEK', 'CRK'),
    ('CRESCENT', 'CRES'),
    ('CREST', 'CRST'),
    ('CROSSING', 'XING'),
    ('CROSSROAD', 'XRD'),
    ('CROSSROADS', 'XRDS'),
    ('CRSENT', 'CRES'),
    ('CRSNT', 'CRES'),
    ('CRSSING', 'XING'),
    ('CRSSNG', 'XING'),
    ('CURVE', 'CURV'),
    ('DALE', 'DL'),
    ('DEPARTMENT', 'DEPT'),
    ('DIV', 'DV'),
    ('DIVIDE', 'DV'),
    ('DRIV', 'DR'),
    ('DRIVE', 'DR'),
    ('DRIVES', 'DRS'),
    ('DRV', 'DR'),
    ('DVD', 'DV'),
    ('ESTATE', 'EST'),
    ('ESTATES', 'ESTS'),
    ('EXP', 'EXPY'),
    ('EXPR', 'EXPY'),
    ('EXPRESS', 'EXPY'),
    ('EXPRESSWAY', 'EXPY'),
    ('EXPW', 'EXPY'),
    ('EXTENSION', 'EXT'),
    ('EXTENSIONS', 'EXTS'),
    ('EXTN', 'EXT'),
    ('EXTNSN', 'EXT'),
    ('FERRY', 'FRY'),
    ('FIELD', 'FLD'),
    ('FIELDS', 'FLDS'),
    ('FLAT', 'FLT'),
    ('FLATS', 'FLTS'),
    ('FLOOR', 'FL'),
    ('FRST', 'FOREST'),
    ('FORG', 'FORGE'),
    ('FORK', 'FRK'),
    ('FORKS', 'FRKS'),
    ('FORT', 'FT'),
    ('FREEWAY', 'FWY'),
    ('FREEWY', 'FWY'),
    ('FRONT', 'FRNT'),
    ('FRRY', 'FRY'),
    ('FRT', 'FT'),
    ('FRWAY', 'FWY'),
    ('FRWY', 'FWY'),
    ('GARDEN', 'GDN'),
    ('GARDENS', 'GDNS'),
    ('GARDN', 'GDN'),
    ('GATEWAY', 'GTWY'),
    ('GATEWY', 'GTWY'),
    ('GATWAY', 'GTWY'),
    ('GLEN', 'GLN'),
    ('GLENS', 'GLNS'),
    ('GRDEN', 'GDN'),
    ('GRDN', 'GDN'),
    ('GRDNS', 'GDNS'),
    ('GREEN', 'GRN'),
    ('GREENS', 'GRNS'),
    ('GROV', 'GRV'),
    ('GROVE', 'GRV'),
    ('GROVES', 'GRVS'),
    ('GTWAY', 'GTWY'),
    ('HANGAR', 'HNGR'),
    ('HARB', 'HBR'),
    ('HARBOR', 'HBR'),
    ('HARBORS', 'HBRS'),
    ('HARBR', 'HBR'),
    ('HAVEN', 'HVN'),
    ('HEIGHTS', 'HTS'),
    ('HIGHWAY', 'HWY'),
    ('HIGHWY', 'HWY'),
    ('HIWAY', 'HWY'),
    ('HIWY', 'HWY'),
    ('HLLW', 'HOLW'),
    ('HOLLOW', 'HOLW'),
    ('HOLLOWS', 'HOLW'),
    ('HOLWS', 'HOLW'),
    ('HRBOR', 'HBR'),
    ('HT', 'HTS'),
    ('HWAY', 'HWY'),
    ('INLET', 'INLT'),
    ('ISLAND', 'IS'),
    ('ISLANDS', 'ISS'),
    ('ISLND', 'IS'),
    ('ISLNDS', 'ISS'),
    ('JCTION', 'JCT'),
    ('JCTN', 'JCT'),
    ('JCTNS', 'JCTS'),
    ('JUNCTION', 'JCT'),
    ('JUNCTIONS', 'JCTS'),
    ('JUNCTN', 'JCT'),
    ('JUNCTON', 'JCT'),
    ('KNOL', 'KNL'),
    ('KNOLL', 'KNL'),
    ('KNOLLS', 'KNLS'),
    ('LAKE', 'LK'),
    ('LAKES', 'LKS'),
    ('LANDING', 'LNDG'),
    ('LANE', 'LN'),
    ('LDGE', 'LDG'),
    ('LIGHT', 'LGT'),
    ('LIGHTS', 'LGTS'),
    ('LNDNG', 'LNDG'),
    ('LOAF', 'LF'),
    ('LOBBY', 'LBBY'),
    ('LOCK', 'LCK'),
    ('LOCKS', 'LCKS'),
    ('LODG', 'LDG'),
    ('LODGE', 'LDG'),
    ('LOWER', 'LOWR'),
    ('MEADOW', 'MDW'),
    ('MEADOWS', 'MDW'),
    ('MEADOWS', 'MDWS'),
    ('MEDOWS', 'MDWS'),
    ('MILLS', 'MLS'),
    ('MISSN', 'MISSION'),
    ('MNT', 'MT'),
    ('MNTAIN', 'MTN'),
    ('MNTN', 'MTN'),
    ('MNTNS', 'MTNS'),
    ('MOTORWAY', 'MTWY'),
    ('MOUNT', 'MT'),
    ('MOUNTAIN', 'MTN'),
    ('MOUNTAINS', 'MTNS'),
    ('MOUNTIN', 'MTN'),
    ('MSSN', 'MISSION'),
    ('MTIN', 'MTN'),
    ('OFFICE', 'OFC'),
    ('ORCHARD', 'ORCH'),
    ('ORCHRD', 'ORCH'),
    ('OVERPASS', 'OPAS'),
    ('PARKS', 'PARK'),
    ('PARKWAY', 'PKWY'),
    ('PARKWAYS', 'PKWY'),
    ('PARKWY', 'PKWY'),
    ('PASSAGE', 'PSGE'),
    ('PENTHOUSE', 'PH'),
    ('PKWAY', 'PKWY'),
    ('PKWYS', 'PKWY'),
    ('PKY', 'PKWY'),
    ('PLACE', 'PL'),
    ('PLAIN', 'PLN'),
    ('PLAINS', 'PLNS'),
    ('PLZA', 'PLAZA'),
    ('POINT', 'PT'),
    ('POINTS', 'PTS'),
    ('PORT', 'PRT'),
    ('PORTS', 'PRTS'),
    ('PRAIRIE', 'PR'),
    ('PRR', 'PR'),
    ('RAD', 'RADL'),
    ('RADIAL', 'RADL'),
    ('RADIEL', 'RADL'),
    ('RAPID', 'RPD'),
    ('RAPIDS', 'RPDS'),
    ('RDGE', 'RDG'),
    ('RIDGE', 'RDG'),
    ('RIDGES', 'RDGS'),
    ('RIV', 'RIVER'),
    ('RIVR', 'RIVER'),
    ('RNCHS', 'RANCHES'),
    ('ROAD', 'RD'),
    ('ROADS', 'RDS'),
    ('ROOM', 'RM'),
    ('ROUTE', 'RTE'),
    ('RVR', 'RIVER'),
    ('SHOAL', 'SHL'),
    ('SHOALS', 'SHLS'),
    ('SHOAR', 'SHR'),
    ('SHOARS', 'SHRS'),
    ('SHORE', 'SHR'),
    ('SHORES', 'SHRS'),
    ('SKYWAY', 'SKWY'),
    ('SPACE', 'SPC'),
    ('SPNG', 'SPG'),
    ('SPNGS', 'SPGS'),
    ('SPRING', 'SPG'),
    ('SPRINGS', 'SPGS'),
    ('SPRNG', 'SPG'),
    ('SPRNGS', 'SPGS'),
    ('SPURS', 'SPUR'),
    ('SQR', 'SQ'),
    ('SQRE', 'SQ'),
    ('SQRS', 'SQS'),
    ('SQU', 'SQ'),
    ('SQUARE', 'SQ'),
    ('SQUARES', 'SQS'),
    ('STA', 'STATION' ),
    ('STATN', 'STATION'),
    ('STN', 'STATION'),
    ('STR', 'ST'),
    ('STRAV', 'STRA'),
    ('STRAVEN', 'STRA'),
    ('STRAVENUE', 'STRA'),
    ('STRAVN', 'STRA'),
    ('STREAM', 'STRM'),
    ('STREET', 'ST'),
    ('STREETS', 'STS'),
    ('STREME', 'STRM'),
    ('STRT', 'ST'),
    ('STRVN', 'STRA'),
    ('STRVNUE', 'STRA'),
    ('SUITE', 'STE'),
    ('SMT', 'SUMMIT'),
    ('SUMIT', 'SUMMIT'),
    ('SUMITT', 'SUMMIT'),
    ('TERR', 'TER'),
    ('TERRACE', 'TER'),
    ('THROUGHWAY', 'TRWY'),
    ('TRACE', 'TRCE'),
    ('TRACES', 'TRCE'),
    ('TRACK', 'TRAK'),
    ('TRACKS', 'TRAK'),
    ('TRAFFICWAY', 'TRFY'),
    ('TRL', 'TRAIL'),
    ('TRL', 'TRAILS'),
    ('TRAILER', 'TRLR'),
    ('TRK', 'TRAK'),
    ('TRKS', 'TRAK'),
    ('TRLRS', 'TRLR'),
    ('TRLS', 'TRAILS'),
    ('TRNPK', 'TPKE'),
    ('TUNEL', 'TUNL'),
    ('TUNLS', 'TUNL'),
    ('TUNNEL', 'TUNL'),
    ('TUNNELS', 'TUNL'),
    ('TUNNL', 'TUNL'),
    ('TURNPIKE', 'TPKE'),
    ('TURNPK', 'TPKE'),
    ('UNDERPASS', 'UPAS'),
    ('UNION', 'UN'),
    ('UNIONS', 'UNS'),
    ('UPPER', 'UPPR'),
    ('VDCT', 'VIA'),
    ('VIADCT', 'VIA'),
    ('VIADUCT', 'VIA'),
    ('VALLY', 'VALLEY'),
    ('VIEW', 'VW'),
    ('VIEWS', 'VWS'),
    ('VILL', 'VLG'),
    ('VILLAG', 'VLG'),
    ('VILLAGE', 'VLG'),
    ('VILLAGES', 'VLGS'),
    ('VILLE', 'VL'),
    ('VILLG', 'VLG'),
    ('VILLIAGE', 'VLG'),
    ('VIST', 'VISTA'),
    ('VLLY', 'VALLEY'),
    ('VST', 'VISTA'),
    ('VSTA', 'VISTA'),
    ('WALKS', 'WALK') )


tMoreAbbrevs = (
    ('UNIVERSITY', 'U'),
    ('UNIV', 'U') )

dAbbrevs = dict( [ ( r'\b%s\b' % t[0], t[1] ) for t in tAbbreviations ] )

getAbbreviate = getSwapper(
                    dAbbrevs,
                    bIgnoreCase = True,
                    bEscape = False )

dMoreAbbrevs = dict( [ ( r'\b%s\b' % t[0], t[1] ) for t in tAbbreviations ] )
dMoreAbbrevs.update(
               dict( [ ( r'\b%s\b' % t[0], t[1] ) for t in tMoreAbbrevs ] ) )


getAbbreviateMore = \
    getSwapper(
        dMoreAbbrevs,
        bIgnoreCase = True,
        bEscape = False )



def _getAddressPartsFinder():
    #
    from String.Find    import getFinderFindAll, getSeqWordBounds
    #
    iAbbrevs = len( tAbbreviations )
    #
    lAddressParts = [ None ] * 2 * iAbbrevs
    #
    for i, t in enumerate( tAbbreviations ):
        #
        lAddressParts[ i            ] = t[0]
        lAddressParts[ i + iAbbrevs ] = t[1]
    #
    lAddressParts.append( r'\d[-\d\w]*' )
    #
    return getFinderFindAll( getSeqWordBounds( lAddressParts ) )


oAddressPartsFinder = _getAddressPartsFinder()


def _getStreetFinder():
    #
    from String.Find    import getFinderFindAll, getSeqWordBounds
    #
    tStreets = (
        '\d+',
        '[NESW]{1}',
        'NE|SE|NW|SW',
        'ALY',
        'AVE',
        'BLVD',
        'BYP',
        'CSWY',
        'CIR',
        'CT',
        'CIR',
        'DR',
        'EXPY',
        'HWY',
        'LN',
        'MTWY',
        'PKWY',
        'PL',
        'RD',
        'RTE',
        'ST',
        'TER',
        'TRAIL',
        'TPKE',
        'Camino' )
    #
    return getFinderFindAll( getSeqWordBounds( tStreets ) )


oStreetFinder = _getStreetFinder()




if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if getAbbreviate( '1231 North 48th street' ) != '1231 N 48th ST':
        #
        lProblems.append( 'getAbbreviate()' )
        #
    #
    if getStateGotCode( 'wa' ) != 'Washington' or getStateGotCode('zz'):
        #
        lProblems.append( 'getStateGotCode()' )
        #
    #
    if      getCodeGotState('district of columbia') != 'DC' or \
            getCodeGotState('zz') or \
            getCodeGotState(''):
        #
        lProblems.append( 'getCodeGotState()' )
        #
    #
    if getCodeGotStateOrCode( 'Washington' ) != 'WA':
        #
        lProblems.append( 'getCodeGotStateOrCode() Washington state' )
        #
    #
    if getCodeGotStateOrCode( 'WA' ) != 'WA':
        #
        lProblems.append( 'getCodeGotStateOrCode() WA state' )
        #
    #
    if getStateName( 'abcde Washington xyz ' ) != 'Washington':
        #
        lProblems.append( 'getStateName() Washington state' )
        #
    #
    if getStateName( 'abcde xyz ' ) != '':
        #
        lProblems.append( 'getStateName() no state' )
        #
    #
    if getStateCode( '(panybnjcdemt WA) xyz ' ) != 'WA':
        #
        lProblems.append( 'getStateCode() valid state' )
        #
    #
    if getStateCode( 'panybnjcdemt xyz ' ) != '':
        #
        lProblems.append( 'getStateCode() invalid state' )
        #
    #
    if getAbbrevOffProvinceOrCodeCA( 'British Columbia', "V7J OA3" ) != 'BC':
        #
        lProblems.append( 'getAbbrevOffProvinceOrCodeCA() valid province and code' )
        #
    #
    if getAbbrevOffProvinceOrCodeCA( '', "V7J OA3" ) != 'BC':
        #
        lProblems.append( 'getAbbrevOffProvinceOrCodeCA() no Province Code only' )
        #
    #
    if getAbbrevOffProvinceOrCodeCA( 'British Quebec', "D7J OA3" ) != '??':
        #
        lProblems.append( 'getAbbrevOffProvinceOrCodeCA() invalid data' )
        #
    #
    if oAddressPartsFinder(
            'South Washington Park Ave' ) != ['South', 'Park', 'Ave']:
        #
        lProblems.append( 'oAddressPartsFinder() South Washington Park Ave' )
        #
    #
    if oStreetFinder(
            'South Washington Park Ave' ) != ['Ave']:
        #
        lProblems.append( 'oStreetFinder() South Washington Park Ave' )
        #
    #
    if oStreetFinder( '1231 N 48th St' ) != ['1231', 'N', 'St']:
        #
        lProblems.append( 'oStreetFinder() 1231 N 48th St' )
        #
    #
    #
    sayTestResult( lProblems )
