#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Mail functions Abbreviations
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
'''
from sMail.Abbrev   import getCodeGotState
from Dict.Get       import getItemIter



# valid zips note Virginia and DC overlap
# good reference 2012-06-03 http://www.mongabay.com/igapo/zip_codes/
dZipRange4State = \
    dict( (
      ( 'Washington DC',        ( { 'min' : '20000', 'max' : '20599' } ) ),
      ( 'Alabama',              ( { 'min' : '35000', 'max' : '36999' } ) ),
      ( 'Alaska',               ( { 'min' : '99500', 'max' : '99999' } ) ),
      ( 'American Samoa',       ( { 'min' : '96799', 'max' : '96799' } ) ),
      ( 'Arizona',              ( { 'min' : '85000', 'max' : '86999' } ) ),
      ( 'Arkansas',             ( { 'min' : '71600', 'max' : '72999' } ) ),
      ( 'California',           ( { 'min' : '90000', 'max' : '96699' } ) ),
      ( 'Colorado',             ( { 'min' : '80000', 'max' : '81999' } ) ),
      ( 'Connecticut',          ( { 'min' : '06000', 'max' : '06999' } ) ),
      ( 'Delaware',             ( { 'min' : '19700', 'max' : '19999' } ) ),
      ( 'District of Columbia', ( { 'min' : '20000', 'max' : '20599' } ) ),
      ( 'Florida',              ( { 'min' : '32000', 'max' : '34999' } ) ),
      ( 'Georgia',              ( { 'min' : '30000', 'max' : '31999' } ) ),
      ( 'Guam',                 ( { 'min' : '96910', 'max' : '96932' } ) ),
      ( 'Hawaii',               ( { 'min' : '96700', 'max' : '96999' } ) ),
      ( 'Idaho',                ( { 'min' : '83200', 'max' : '83999' } ) ),
      ( 'Illinois',             ( { 'min' : '60000', 'max' : '62999' } ) ),
      ( 'Indiana',              ( { 'min' : '46000', 'max' : '47999' } ) ),
      ( 'Iowa',                 ( { 'min' : '50000', 'max' : '52999' } ) ),
      ( 'Kansas',               ( { 'min' : '66000', 'max' : '67999' } ) ),
      ( 'Kentucky',             ( { 'min' : '40000', 'max' : '42999' } ) ),
      ( 'Louisiana',            ( { 'min' : '70000', 'max' : '71599' } ) ),
      ( 'Maine',                ( { 'min' : '03900', 'max' : '04999' } ) ),
      ( 'Maryland',             ( { 'min' : '20600', 'max' : '21999' } ) ),
      ( 'Massachusetts',        ( { 'min' : '01000', 'max' : '02799' } ) ),
      ( 'Michigan',             ( { 'min' : '48000', 'max' : '49999' } ) ),
      ( 'Minnesota',            ( { 'min' : '55000', 'max' : '56999' } ) ),
      ( 'Mississippi',          ( { 'min' : '38600', 'max' : '39999' } ) ),
      ( 'Missouri',             ( { 'min' : '63000', 'max' : '65999' } ) ),
      ( 'Montana',              ( { 'min' : '59000', 'max' : '59999' } ) ),
      ( 'Nebraska',             ( { 'min' : '68000', 'max' : '69999' } ) ),
      ( 'Nevada',               ( { 'min' : '88900', 'max' : '89999' } ) ),
      ( 'New Hampshire',        ( { 'min' : '03000', 'max' : '03899' } ) ),
      ( 'New Jersey',           ( { 'min' : '07000', 'max' : '08999' } ) ),
      ( 'New Mexico',           ( { 'min' : '87000', 'max' : '88899' } ) ),
      ( 'New York',             ( { 'min' : '10000', 'max' : '14999' } ) ),
      ( 'North Carolina',       ( { 'min' : '27000', 'max' : '28999' } ) ),
      ( 'North Dakota',         ( { 'min' : '58000', 'max' : '58999' } ) ),
      ( 'Northern Mariana Islands',
                                ( { 'min' : '96950', 'max' : '96952' } ) ),
      ( 'Ohio',                 ( { 'min' : '43000', 'max' : '45999' } ) ),
      ( 'Oklahoma',             ( { 'min' : '73000', 'max' : '74999' } ) ),
      ( 'Oregon',               ( { 'min' : '97000', 'max' : '97999' } ) ),
      ( 'Pennsylvania',         ( { 'min' : '15000', 'max' : '19699' } ) ),
      ( 'Puerto Rico',          ( { 'min' : '00600', 'max' : '00999' } ) ),
      ( 'Rhode Island',         ( { 'min' : '02800', 'max' : '02999' } ) ),
      ( 'South Carolina',       ( { 'min' : '29000', 'max' : '29999' } ) ),
      ( 'South Dakota',         ( { 'min' : '57000', 'max' : '57999' } ) ),
      ( 'Tennessee',            ( { 'min' : '37000', 'max' : '38599' } ) ),
      ( 'Texas',                ( { 'min' : '75000', 'max' : '79999' } ) ),
      ( 'Utah',                 ( { 'min' : '84000', 'max' : '84999' } ) ),
      ( 'Vermont',              ( { 'min' : '05000', 'max' : '05999' } ) ),
      ( 'Virginia',             ( { 'min' : '22000', 'max' : '24699' } ) ),
      ( 'Virgin Islands',       ( { 'min' : '00801', 'max' : '00851' } ) ),
      ( 'Washington',           ( { 'min' : '98000', 'max' : '99499' } ) ),
      ( 'West Virginia',        ( { 'min' : '24700', 'max' : '26999' } ) ),
      ( 'Wisconsin',            ( { 'min' : '53000', 'max' : '54999' } ) ),
      ( 'Wyoming',              ( { 'min' : '82000', 'max' : '83199' } ) ) ) )

# http://en.wikipedia.org/wiki/ZIP_code
dZipRange4State['Virginia' ]['more'] = [{ 'min' : '20100', 'max' : '20199'}]
dZipRange4State['New York' ]['more'] = [{ 'min' : '06390', 'max' : '06399'}]
dZipRange4State['Texas'    ]['more'] = [{ 'min' : '88500', 'max' : '88599'}]
dZipRange4State['Arkansas' ]['more'] = [{ 'min' : '65733', 'max' : '65733'}]
dZipRange4State['Tennessee']['more'] = [{ 'min' : '42223', 'max' : '42223'}]


dZipRange4Code = dict(
      [ ( getCodeGotState( t[0] ), t[1] )
        for t
        in getItemIter( dZipRange4State ) ] )

del dZipRange4Code[ '' ]




def _getMinMax( d ):
    #
    return d['min'], d['max']

lZipRangeMinMaxCode = []

#
def _getZipRefLists():
    #
    from Collect.Get    import unZip
    from Iter.AllVers   import tMap
    #
    for t in getItemIter( dZipRange4Code ):
        #
        sStateCode, d = t
        #
        sMin, sMax = _getMinMax( d )
        #
        lZipRangeMinMaxCode.append( ( sMin, sMax, sStateCode ) )
        #
        if 'more' in d:
            #
            for d in d['more']:
                #
                sMin, sMax = _getMinMax( d )
                #
                lZipRangeMinMaxCode.append( ( sMin, sMax, sStateCode ) )
                #
            #
        #
    #
    lZipRangeMinMaxCode.sort()
    #
    lMinMins,  lMinMaxes, lMinStates = unZip( lZipRangeMinMaxCode )
    #
    return tMap( tuple,
          ( lZipRangeMinMaxCode,
            lMinMins,
            lMinMaxes ) )

( _tZipRangeMinMaxCode,
  _tMinMins,
  _tMinMaxes ) = _getZipRefLists()


def getStateGotZip( sZip ):
    #
    from bisect import bisect_left
    #
    from sMail.Test import isZipPlus4
    #
    if isZipPlus4( sZip ): sZip = sZip[ : 5 ]
    #
    iStartAt = bisect_left( _tMinMins, sZip )
    #
    if iStartAt > len( _tMinMins ) - 1: iStartAt = len( _tMinMins ) - 1
    #
    while iStartAt > 0:
        #
        if _tMinMins[ iStartAt ] > sZip:
            #
            iStartAt = iStartAt - 1
            #
        else:
            #
            break
            #
        #
    #
    iThis = max( iStartAt - 1, 0 )
    #
    lHits = []
    #
    while sZip >= _tMinMins[ iThis ]:
        #
        if sZip <= _tMinMaxes[ iThis ]:
            #
            lHits.append( lZipRangeMinMaxCode[ iThis ] )
            #
        #
        iThis += 1
        #
        if iThis == len( _tMinMins ): break
    #
    sStateCode = ''
    #
    if len( lHits ) == 1:
        #
        sStateCode = lHits[0][2]
        #
    elif len( lHits ) > 1:
        #
        lByRange = [ ( int(t[1]) - int(t[0]), t )  for t in lHits ]
        #
        lByRange.sort()
        #
        sStateCode = lByRange[0][1][2]
        #
    #
    return sStateCode
            
        


# updates 2015-01-08
# fetched from http://www.apoaddress.com/aponumber.html
# dead
# check http://www.freebizadsweb.com/apofpolist.asp
# defunct
# more up to date http://www5.apobox.com/zip_restrictions.php
# not found
# 09011 09372 & 96303 are kludges, not verified
#

dApoZipCountry = \
    {   '09007' : 'Germany',
        '09009' : 'Germany',
        '09011' : 'Germany',
        '09012' : 'Germany',
        '09013' : 'Germany',
        '09014' : 'Germany',
        '09021' : 'Germany',
        '09028' : 'Germany',
        '09031' : 'Germany',
        '09033' : 'Germany',
        '09034' : 'Germany',
        '09036' : 'Germany',
        '09042' : 'Germany',
        '09045' : 'Germany',
        '09046' : 'Germany',
        '09050' : 'Germany',
        '09053' : 'Germany',
        '09054' : 'Germany',
        '09056' : 'Germany',
        '09058' : 'Germany',
        '09059' : 'Germany',
        '09060' : 'Germany',
        '09063' : 'Germany',
        '09067' : 'Germany',
        '09069' : 'Germany',
        '09074' : 'Germany',
        '09076' : 'Germany',
        '09080' : 'Germany',
        '09081' : 'Germany',
        '09086' : 'Germany',
        '09089' : 'Germany',
        '09090' : 'Germany',
        '09094' : 'Germany',
        '09095' : 'Germany',
        '09096' : 'Germany',
        '09098' : 'Germany',
        '09099' : 'Germany',
        '09100' : 'Germany',
        '09102' : 'Germany',
        '09103' : 'Germany',
        '09104' : 'Germany',
        '09107' : 'Germany',
        '09110' : 'Germany',
        '09112' : 'Germany',
        '09114' : 'Germany',
        '09123' : 'Germany',
        '09126' : 'Germany',
        '09128' : 'Germany',
        '09131' : 'Germany',
        '09136' : 'Germany',
        '09137' : 'Germany',
        '09138' : 'Germany',
        '09139' : 'Germany',
        '09140' : 'Germany',
        '09142' : 'Germany',
        '09143' : 'Germany',
        '09154' : 'Germany',
        '09165' : 'Germany',
        '09166' : 'Germany',
        '09169' : 'Germany',
        '09172' : 'Germany',
        '09173' : 'Germany',
        '09175' : 'Germany',
        '09177' : 'Germany',
        '09180' : 'Germany',
        '09182' : 'Germany',
        '09183' : 'Germany',
        '09185' : 'Germany',
        '09186' : 'Germany',
        '09211' : 'Germany',
        '09212' : 'Germany',
        '09213' : 'Germany',
        '09214' : 'Germany',
        '09225' : 'Germany',
        '09226' : 'Germany',
        '09227' : 'Germany',
        '09229' : 'Germany',
        '09237' : 'Germany',
        '09244' : 'Germany',
        '09245' : 'Germany',
        '09250' : 'Germany',
        '09252' : 'Germany',
        '09262' : 'Germany',
        '09263' : 'Germany',
        '09264' : 'Germany',
        '09265' : 'Germany',
        '09266' : 'Germany',
        '09267' : 'Germany',
        '09302' : 'Kuwait',
        '09303' : 'Kuwait',
        '09304' : 'Kuwait',
        '09305' : 'Kuwait',
        '09306' : 'Kuwait',
        '09306' : 'Kuwait',
        '09309' : 'Qatar',
        '09310' : frozenset( ( 'Afghanistan', 'Iraq' ) ),
        '09312' : 'Iraq',
        '09313' : 'Iraq',
        '09314' : 'Afghanistan',
        '09315' : 'Iraq',
        '09320' : 'Afghanistan',
        '09330' : 'Kuwait',
        '09331' : 'Iraq',
        '09332' : 'Iraq',
        '09333' : 'Iraq',
        '09334' : 'Iraq',
        '09336' : 'Kuwait',
        '09337' : 'Kuwait',
        '09338' : 'Iraq',
        '09340' : 'Kosovo',
        '09342' : 'Iraq',
        '09344' : 'Iraq',
        '09347' : 'Iraq',
        '09348' : 'Iraq',
        '09351' : 'Iraq',
        '09354' : frozenset( ( 'Afghanistan', 'Germany' ) ),
        '09355' : 'Afghanistan',
        '09356' : 'Afghanistan',
        '09359' : 'Iraq',
        '09366' : 'Kuwait',
        '09368' : 'Iraq',
        '09372' : 'Afghanistan',
        '09375' : 'Iraq',
        '09378' : 'Iraq',
        '09384' : 'Iraq',
        '09391' : 'Iraq',
        '09393' : 'Iraq',
        '09397' : 'Germany',
        '09399' : 'Germany',
        '09421' : 'United Kingdom',
        '09432' : 'Iraq',
        '09447' : 'United Kingdom',
        '09454' : 'United Kingdom',
        '09456' : 'United Kingdom',
        '09459' : 'United Kingdom',
        '09461' : 'United Kingdom',
        '09463' : 'United Kingdom',
        '09464' : 'United Kingdom',
        '09468' : 'United Kingdom',
        '09469' : 'United Kingdom',
        '09470' : 'United Kingdom',
        '09494' : 'United Kingdom',
        '09496' : 'United Kingdom',
        '09498' : 'United Kingdom',
        '09508' : 'Cuba',
        '09601' : 'Italy',
        '09603' : 'Italy',
        '09604' : 'Italy',
        '09609' : 'Italy',
        '09610' : 'Italy',
        '09612' : 'Italy',
        '09613' : 'Italy',
        '09617' : 'Italy',
        '09618' : 'Italy',
        '09619' : 'Italy',
        '09620' : 'Italy',
        '09621' : 'Italy',
        '09622' : 'Italy',
        '09623' : 'Italy',
        '09624' : 'Italy',
        '09625' : 'Italy',
        '09626' : 'Italy',
        '09627' : 'Italy',
        '09628' : 'Italy',
        '09630' : 'Italy',
        '09631' : 'Italy',
        '09636' : 'Italy',
        '09638' : 'Italy',
        '09642' : 'Spain',
        '09643' : 'Spain',
        '09644' : 'Spain',
        '09645' : 'Spain',
        '09647' : 'Spain',
        '09649' : 'Spain',
        '09703' : 'Netherlands',
        '09704' : 'Greenland',
        '09705' : 'Belgium',
        '09706' : 'Norway',
        '09707' : 'Norway',
        '09708' : 'Belgium',
        '09709' : 'Netherlands',
        '09710' : 'Belgium',
        '09711' : 'Netherlands',
        '09713' : 'Belgium',
        '09714' : 'Belgium',
        '09715' : 'Netherlands',
        '09716' : 'Denmark',
        '09717' : 'Netherlands',
        '09718' : 'Morocco',
        '09720' : 'Portugal',
        '09721' : frozenset( ('Finland', 'Russian Federation', 'Switzerland' ) ),
        '09722' : 'Denmark',
        '09723' : 'Finland',
        '09724' : 'Belgium',
        '09725' : 'Iceland',
        '09726' : 'Portugal',
        '09728' : 'Iceland',
        '09732' : 'Canada',
        '09733' : 'Canada',
        '09734' : 'Iraq',
        '09735' : 'Canada',
        '09749' : 'Romania',
        '09777' : 'France',
        '09788' : 'Bosnia',
        '09779' : 'Bosnia',
        '09780' : 'Bosnia',
        '09789' : 'Bosnia',
        '09790' : 'Monaco',
        '09791' : 'France',
        '09793' : 'Hungary',
        '09802' : 'Saudi Arabia',
        '09803' : 'Saudi Arabia',
        '09809' : 'Saudi Arabia',
        '09810' : 'Saudi Arabia',
        '09811' : 'Saudi Arabia',
        '09812' : 'Pakistan',
        '09814' : 'Pakistan',
        '09819' : 'Turkey',
        '09821' : 'Turkey',
        '09822' : 'Turkey',
        '09823' : 'Turkey',
        '09824' : 'Adana Turkey',
        '09827' : 'Turkey',
        '09828' : 'Congo',
        '09830' : 'Israel',
        '09831' : 'Kenya',
        '09832' : 'Egypt',
        '09833' : 'Egypt',
        '09834' : 'Bahrain',
        '09835' : 'Egypt',
        '09836' : 'Cyprus',
        '09837' : 'United Arab Emirates',
        '09838' : 'Bahrain',
        '09839' : 'Egypt',
        '09841' : 'Greece',
        '09842' : 'Greece',
        '09844' : 'Greece',
        '09852' : 'Saudi Arabia',
        '09853' : 'United Arab Emirates',
        '09855' : 'Kuwait',
        '09858' : 'Saudi Arabia',
        '09865' : 'Greece',
        '09868' : 'Egypt',
        '09871' : 'Saudi Arabia',
        '09880' : 'Kuwait',
        '09882' : 'Saudi Arabia',
        '09888' : 'Kuwait',
        '09889' : 'Kuwait',
        '09890' : 'Oman',
        '09892' : 'Jordan',
        '09898' : 'Qatar',
        '34002' : 'Panama',
        '34020' : 'Costa Rica',
        '34021' : 'Nicaragua',
        '34022' : 'Honduras',
        '34023' : 'El Salvador',
        '34024' : 'Guatemala',
        '34025' : 'Belize',
        '34030' : 'Brazil',
        '34031' : 'Peru',
        '34032' : 'Bolivia',
        '34033' : 'Chile',
        '34034' : 'Argentina',
        '34035' : 'Uruguay',
        '34036' : 'Paraguay',
        '34037' : 'Venezuela',
        '34038' : 'Colombia',
        '34039' : 'Ecuador',
        '34040' : 'Puerto Rico',
        '34041' : 'Dominican Republic',
        '34042' : 'Honduras',
        '34050' : 'Puerto Rico',
        '34053' : 'Puerto Rico',
        '34055' : 'Barbados',
        '34058' : 'Bahamas',
        '34076' : 'Ecuador',
        '34078' : 'Haiti',
        '34079' : 'Aruba',
        '96201' : 'South Korea',
        '96203' : 'South Korea',
        '96204' : 'South Korea',
        '96205' : 'South Korea',
        '96206' : 'South Korea',
        '96207' : 'South Korea',
        '96208' : 'South Korea',
        '96212' : 'South Korea',
        '96213' : 'South Korea',
        '96214' : 'South Korea',
        '96215' : 'South Korea',
        '96217' : 'South Korea',
        '96218' : 'South Korea',
        '96219' : 'South Korea',
        '96220' : 'South Korea',
        '96221' : 'South Korea',
        '96224' : 'South Korea',
        '96251' : 'South Korea',
        '96257' : 'South Korea',
        '96258' : 'South Korea',
        '96259' : 'South Korea',
        '96260' : 'South Korea',
        '96262' : 'South Korea',
        '96264' : 'South Korea',
        '96266' : 'South Korea',
        '96267' : 'South Korea',
        '96269' : 'South Korea',
        '96271' : 'South Korea',
        '96275' : 'South Korea',
        '96276' : 'South Korea',
        '96278' : 'South Korea',
        '96283' : 'South Korea',
        '96284' : 'South Korea',
        '96297' : 'South Korea',
        '96303' : 'Japan',
        '96306' : 'Japan',
        '96309' : 'Japan',
        '96310' : 'Japan',
        '96311' : 'Japan',
        '96313' : 'Japan',
        '96319' : 'Japan',
        '96321' : 'Japan',
        '96322' : 'Japan',
        '96323' : 'Japan',
        '96326' : 'Japan',
        '96328' : 'Japan',
        '96330' : 'Japan',
        '96336' : 'Japan',
        '96337' : 'Japan',
        '96338' : 'Japan',
        '96339' : 'Japan',
        '96343' : 'Japan',
        '96347' : 'Japan',
        '96348' : 'Japan',
        '96349' : 'Japan',
        '96350' : 'Japan',
        '96351' : 'Japan',
        '96362' : 'Japan',
        '96365' : 'Japan',
        '96367' : 'Japan',
        '96368' : 'Japan',
        '96370' : 'Japan',
        '96372' : 'Japan',
        '96373' : 'Japan',
        '96374' : 'Japan',
        '96375' : 'Japan',
        '96376' : 'Japan',
        '96377' : 'Japan',
        '96378' : 'Japan',
        '96379' : 'Japan',
        '96384' : 'Japan',
        '96386' : 'Japan',
        '96387' : 'Japan',
        '96388' : 'Japan',
        '96401' : 'Australia',
        '96490' : 'British Indian Ocean Territory',
        '96507' : 'Singapore',
        '96511' : 'Canada',
        '96515' : 'Philippines',
        '96517' : 'Philippines',
        '96520' : 'Indonesia',
        '96521' : 'Hong Kong',
        '96522' : 'Hong Kong',
        '96530' : 'Australia',
        '96531' : 'New Zealand',
        '96534' : 'Singapore',
        '96535' : 'Malaysia',
        '96536' : 'Guam',
        '96537' : 'Guam',
        '96538' : 'Guam',
        '96540' : 'Guam',
        '96541' : 'Guam',
        '96542' : 'Guam',
        '96543' : 'Guam',
        '96546' : 'Thailand',
        '96548' : 'Australia',
        '96549' : 'Australia',
        '96551' : 'Australia',
        '96553' : 'Australia',
        '96554' : 'Australia',
        '96555' : 'Marshall Island',
        '96557' : 'Marshall Island',
        '96595' : 'British Indian Ocean Territory',
        '96598' : 'Antarctica',
        '96599' : 'Antarctica',
        '96602' : 'Japan',
        '96603' : 'Japan',
        '96604' : 'Japan',
        '96606' : 'Japan',
        '96613' : 'Kuwait' }




def putZerosBackInFront( sZip ):
    #
    '''
    putZerosBackInFront puts the dropped zero back
    pass 9824, returns 09824
    '''
    #
    if sZip and len( sZip ) < 5 and sZip.isdigit():
        #
        sZip = '%05d' % int( sZip )
    #
    return sZip


def getApoCountryOffZip( sZip ):
    #
    from sMail.Get  import getZip5GotZipPlus4
    from sMail.Test import isZipPlus4
    #
    if isZipPlus4( sZip ): sZip = getZip5GotZipPlus4( sZip )
    #
    sZip = putZerosBackInFront( sZip )
    #
    return dApoZipCountry.get( sZip, '' )



def getZipLike( s ):
    #
    from sMail.Test import isZipLike
    #
    if isZipLike( s ):
        sReturn = s
    else:
        sReturn = ''
    #
    return sReturn




if __name__ == "__main__":
    #
    from six            import print_ as print3
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if putZerosBackInFront( '9824' ) != '09824':
        #
        lProblems.append( 'putZerosBackInFront() put zero back in front' )
        #
    #
    if putZerosBackInFront( '09824' ) != '09824':
        #
        lProblems.append( 'putZerosBackInFront() orig zip correct' )
        #
    #
    dWA = { 'min' : '98000', 'max' : '99499' }
    #
    if dZipRange4State[ 'Washington' ] != dWA:
        #
        lProblems.append( 'dZipRange4State()' )
        #
    #
    if dZipRange4Code[ 'WA' ] != dWA:
        #
        lProblems.append( 'dZipRange4Code()' )
        #
    #
    if getApoCountryOffZip( '09888' ) != 'Kuwait':
        #
        lProblems.append( 'getApoCountryOffZip() valid zip' )
        #
    #
    if getApoCountryOffZip( '09888' ) != 'Kuwait':
        #
        lProblems.append( 'getApoCountryOffZip() valid zip' )
        #
    #
    if getApoCountryOffZip( '9618' ) != 'Italy':
        #
        lProblems.append( 'getApoCountryOffZip() valid zip' )
        #
    #
    if getApoCountryOffZip( '01000' ):
        #
        lProblems.append( 'getApoCountryOffZip() invalid zip' )
        #
    #
    if getApoCountryOffZip( '09888-1234' ) != 'Kuwait':
        #
        lProblems.append( 'getApoCountryOffZip() valid ZipPlus4' )
        #
    #
    if getZipLike( '09888-1234' ) != '09888-1234' or getZipLike( 'abc' ) != '':
        #
        print3( getZipLike( '09888-1234' ) )
        print3( getZipLike( 'abc' ) )
        lProblems.append( 'getZipLike()' )
        #
    #
    tStatesZips = (
        ('AK', '99749'),
        ('AL', '35999'),
        ('AR', '72299'),
        ('AS', '96799'),
        ('AZ', '85999'),
        ('CA', '93349'),
        ('CO', '80999'),
        ('CT', '06499'),
        ('DC', '20299'),
        ('DE', '19849'),
        ('FL', '33499'),
        ('GA', '30999'),
        ('GU', '96921'),
        ('HI', '96849'),
        ('IA', '51499'),
        ('ID', '83599'),
        ('IL', '61499'),
        ('IN', '46999'),
        ('KS', '66999'),
        ('KY', '41499'),
        ('LA', '70799'),
        ('MA', '01899'),
        ('MD', '21299'),
        ('ME', '04449'),
        ('MI', '48999'),
        ('MN', '55999'),
        ('MO', '64499'),
        ('MP', '96951'),
        ('MS', '39299'),
        ('MT', '59499'),
        ('NC', '27999'),
        ('ND', '58499'),
        ('NE', '68999'),
        ('NH', '03449'),
        ('NJ', '07999'),
        ('NM', '87949'),
        ('NV', '89449'),
        ('NY', '12499'),
        ('OH', '44499'),
        ('OK', '73999'),
        ('OR', '97499'),
        ('PA', '17349'),
        ('PR', '00664'),
        ('RI', '02899'),
        ('SC', '29499'),
        ('SD', '57499'),
        ('TN', '37799'),
        ('TX', '77499'),
        ('UT', '84499'),
        ('VA', '23349'),
        ('VI', '00814'),
        ('VT', '05499'),
        ('WA', '98749'),
        ('WI', '53999'),
        ('WV', '25849'),
        ('WY', '82599') )
    #
    lMisses = [ t for t in tStatesZips if getStateGotZip( t[1] ) != t[0] ]
    #
    if lMisses:
        #
        lProblems.append( 'getStateGotZip()' )
        #
    #
    #
    #
    sayTestResult( lProblems )