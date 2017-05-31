#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# time functions Convert
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

class FormatMismatchError( Exception ): pass

class Finished( Exception ): pass

sFormatISOdateTime  = '%Y-%m-%d %H:%M:%S'
sFormatISOdate      = '%Y-%m-%d'
sFormatIsoNoSecs    = '%Y-%m-%d %H:%M'
sFormatDateAm       = '%m/%d/%Y'
sFormatDateAmShort  = '%m/%d/%y'
sFormatDateEu       = '%d/%m/%Y'
sFormatISONoSpace   = '%Y-%m-%d_%H.%M.%S'
sFormatNatureUSA    = '%d %m %Y'
sFormatUSAdateTime  = '%m/%d/%Y %I:%M:%S %p'

from String.Find    import getFinder
from Time.Output    import getNowIsoDateTimeStr

_oApacheDelimiters = getFinder( '[/: ]' )

_dMonthNames = dict(
    Jan =  1,
    Feb =  2,
    Mar =  3,
    Apr =  4,
    May =  5,
    Jun =  6,
    Jul =  7,
    Aug =  8,
    Sep =  9,
    Oct = 10,
    Nov = 11,
    Dec = 12 )


def getMonthNumOffName( sMonth ):
    #
    sNumb = ''
    #
    iMonth = _dMonthNames.get( sMonth[:3].title() )
    #
    if iMonth:
        #
        sNumb = '%02d' % iMonth
        #
    #
    return sNumb


def getIsoDateTimeFromObj( oDateTime ):
    #
    return oDateTime.strftime( sFormatISOdateTime )


def getIsoDateTimeStrFromSecs(
        fSecsSinceEpoch = None, bWantLocal = True, sFormat = sFormatISOdateTime ):
    #
    from time           import strftime, gmtime, time, localtime
    #
    from Utils.ImIf     import ImIf
    #
    getTime             = ImIf( bWantLocal, localtime, gmtime )
    #
    if fSecsSinceEpoch   is None: fSecsSinceEpoch = time()
    #
    tSayTime            = getTime( fSecsSinceEpoch )
    #
    return strftime( sFormat, tSayTime )



def getIsoDateTimeStrFromSecsNoSpace(
        fSecsSinceEpoch = None, bWantLocal = True, sFormat = sFormatISONoSpace ):
    #
    return getIsoDateTimeStrFromSecs( fSecsSinceEpoch, bWantLocal, sFormat  )




def getNormalDateFromSecs( fSecsSinceEpoch = None, bWantLocal = True ):
    #
    sFormat = '%d %B %Y'
    #
    return getIsoDateTimeStrFromSecs( fSecsSinceEpoch, bWantLocal, sFormat = sFormat )


def getTimeFromISODateTime( sDateTime = getNowIsoDateTimeStr() ):
    #
    # not used anywhere
    #
    return sDateTime[ 11 :    ]


def getHrMinFromISODateTime( sDateTime = getNowIsoDateTimeStr() ):
    #
    # not used anywhere
    #
    return sDateTime[ 11 : 16 ]



def getDateTimeTupleFromString( sDateTime, sFormat = sFormatISOdateTime ):
    #
    from time           import strptime, tzname
    #
    if '_' in sDateTime: sDateTime = sDateTime.replace( '_', ' ' )
    #
    if sDateTime[ -3 : ] in tzname:
        #
        sDateTime   = sDateTime[ : -4 ]
        #
    #
    return strptime( sDateTime, sFormat )




def getSecsSinceEpochFromString(
            sDateTime,
            sFormat     = sFormatISOdateTime,
            bAdjust2UTC = False ):
    #
    # sFormatDateAm
    #
    from time           import mktime, timezone
    from Utils.ImIf     import ImIf
    #
    tDateTime           = getDateTimeTupleFromString( sDateTime, sFormat )
    #
    iAdjust4TZ          = ImIf( bAdjust2UTC, timezone, 0 )
    #
    return int( mktime( tDateTime ) ) + iAdjust4TZ




def getDateTimeObjFromString(
            sDateTime,
            sFormat     = sFormatISOdateTime,
            bAdjust2UTC = False ):
    #
    from time           import timezone
    from Utils.ImIf     import ImIf
    from datetime       import datetime, timedelta
    #
    tDateTime       = getDateTimeTupleFromString( sDateTime, sFormat )
    #
    lDateTime       = list( tDateTime[ : 6 ] )
    #
    lDateTime.extend( [ 0, None ] )
    #
    oDateTimeObj    = datetime( *lDateTime )
    #
    iAdjust4TZ  = ImIf( bAdjust2UTC, timezone, 0 )
    #
    oAdjust4TZ  = timedelta( seconds = iAdjust4TZ )
    #
    return oDateTimeObj + oAdjust4TZ



def getSecsFromDuration( sHrsMinSec ):
    #
    '''
    converts string 00:00:00 into integer seconds
    '''
    #
    from Iter.AllVers import lMap
    #
    lParts = lMap( int, sHrsMinSec.split( ":" ) )
    #
    iSecs = lParts[0] * 3600
    #
    if len( lParts ) > 1: iSecs += lParts[1] * 60
    #
    if len( lParts ) > 2: iSecs += lParts[2]
    #
    return iSecs



def getDurationFromSecs( iSecs ):
    #
    '''
    converts xseconds into string 00:00:00
    seconds can be integer or float
    see also getSayDurationAsDaysHrsMinsSecs in Time.Output
    '''
    #
    iHrs,  iSecs = divmod( round( iSecs ), 3600 )
    iMins, iSecs = divmod(        iSecs,     60 )
    #
    return '%02d:%02d:%02d' % ( iHrs, iMins, iSecs )






def getIsoOffApacheDateTime( sDateTime ):
    #
    '''
    sApacheDateTime = '23/Sep/2012:06:40:18 +0800'
    '''
    lParts = _oApacheDelimiters.split( sDateTime )
    #
    sD, sMonth, sY, sH, sMins, sS, sOffset = lParts
    #
    sMonth = getMonthNumOffName( sMonth )
    #
    return '%s-%s-%s %s:%s:%s' % ( sY, sMonth, sD, sH, sMins, sS )



def getIsoOffApacheDate( sDate ):
    #
    '''
    sApacheDate = '23-Sep-2012'
    default display date format on directory listing
    '''
    lParts = sDate.split( '-' )
    #
    sD, sMonth, sY = lParts
    #
    sMonth = getMonthNumOffName( sMonth )
    #
    return '%s-%s-%s' % ( sY, sMonth, sD )




def getIsoDateFromOther( sDate,
        sFormatIn = sFormatNatureUSA, sFormatWant = sFormatISOdateTime ):
    #
    '''
    handles coversions from formats such as 17 Jan 2014
    returns string date in desired format
    '''
    from time           import strptime, strftime
    #
    from Iter.AllVers   import getEnumerator
    #
    sNewDate = sDate
    #
    setDelimitersGot = frozenset( _oApacheDelimiters.findall( sDate     ) )
    setDelimitFormat = frozenset( _oApacheDelimiters.findall( sFormatIn ) )
    #
    if setDelimitersGot != setDelimitFormat:
        #
        raise FormatMismatchError
        #
    elif sFormatIn == sFormatNatureUSA:
        #
        # strip leading / trailing blanks
        #
        lParts = [ s for s in _oApacheDelimiters.split( sDate ) if s ]
        #
        for i, sPart in getEnumerator( lParts ):
            #
            sPartTitlized = sPart[:3].title()
            #
            if sPartTitlized in _dMonthNames:
                #
                lParts[ i ] = str( _dMonthNames[ sPartTitlized ] )
                #
                break
                #
            #
        #
        sNewDate = ' '.join( lParts )
                
    else:
        #
        raise NotImplementedError
    #
    #
    tDate = strptime( sNewDate, sFormatIn )
    #
    return strftime( sFormatWant, tDate )[ : 10 ]



def getOtherTimeDatefromISO( sTimeStamp, sFormat = sFormatUSAdateTime ):
    #
    from Time.Convert import getDateTimeObjFromString
    #
    oDateTime = getDateTimeObjFromString( sTimeStamp )
    #
    return oDateTime.strftime( sFormat )



def getDateTimeUSAfromISO( sTimeStamp, sFormat = sFormatUSAdateTime ):
    #
    return getOtherTimeDatefromISO( sTimeStamp, sFormat )


def getOtherDatefromISO( sDate, sFormat = sFormatISOdate ):
    #
    from Time.Convert import getDateTimeObjFromString
    #
    oDateTime = getDateTimeObjFromString( sDate, sFormatISOdate )
    #
    return oDateTime.strftime( sFormat )


def getDateUSAfromISO( sDate, sFormat = sFormatDateAm ):
    #
    return getOtherDatefromISO( sDate, sFormat )



def getIsoDateTimeFromOther( sDateTime, sFormat = sFormatUSAdateTime ):
    #
    from Time.Convert import getDateTimeObjFromString
    #
    oDateTime = getDateTimeObjFromString( sDateTime, sFormat )
    #
    return getIsoDateTimeFromObj( oDateTime )





def getIsoDateTimeFromOtherStr( sDate, sFormat = sFormatUSAdateTime ):
    #
    from Time.Convert import getDateTimeObjFromString
    #
    oDateTime = getDateTimeObjFromString( sDate, sFormat )
    #
    sISO = getIsoDateTimeFromObj( oDateTime )
    #
    return sISO



def getIsoDateFromOtherStr( sDate, sFormat = sFormatDateAmShort ):
    #
    sISO = getIsoDateTimeFromOtherStr( sDate, sFormat )
    #
    return sISO[ : 10 ]



def getIsoDateFromUSAdate( sDate ):
    #
    try:
        if not sDate:
            sISO = ''
            raise Finished
        try:
            sISO = getIsoDateFromOtherStr( sDate, sFormatDateAm      )
            raise Finished
        except ValueError:
            sISO = getIsoDateFromOtherStr( sDate, sFormatDateAmShort )
    #
    except Finished: pass
    #
    return sISO




def getIsoDateTimeFromUSAdateTime( sDateTime ):
    #
    try:
        if not sDateTime:
            sISO = ''
            raise Finished
        try:
            sISO = getIsoDateTimeFromOther( sDateTime, sFormatUSAdateTime )
            raise Finished
        except ValueError:
            pass
        try:
            # two digit year, drop seconds, no AM/PM
            sISO = getIsoDateTimeFromOther( sDateTime, '%m/%d/%y %H:%M' )
            raise Finished
        except ValueError:
            pass
        try:
            # try 4 digit year, no seconds, no AM/PM
            sISO = getIsoDateTimeFromOther( sDateTime, '%m/%d/%Y %H:%M' )
            raise Finished
        except ValueError:
            raise
    #
    except Finished: pass
    #
    return sISO




if __name__ == "__main__":
    #
    from time           import time
    from Test           import isISOdatetime
    from datetime       import datetime
    #
    from six            import print_ as print3
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if getMonthNumOffName( 'jan' ) != '01':
        #
        lProblems.append( 'getMonthNumOffName() short Jan' )
        #
    #
    if getMonthNumOffName( 'december' ) != '12':
        #
        lProblems.append( 'getMonthNumOffName() long Dec' )
        #
    #
    iNow        = int( time() )
    sNow        = getIsoDateTimeStrFromSecs( iNow )
    oNow        = datetime.fromtimestamp( iNow )
    sNoSpace    = getIsoDateTimeStrFromSecsNoSpace( iNow )
    #
    if getIsoDateTimeFromObj( oNow ) != getIsoDateTimeStrFromSecs( iNow ):
        #
        lProblems.append( 'getIsoDateTimeFromObj()' )
        #
    if not isISOdatetime( getIsoDateTimeStrFromSecs( iNow ) ):
        #
        lProblems.append( 'getIsoDateTimeStrFromSecs()' )
        #
    if getTimeFromISODateTime( sNow ) != sNow[ -8 : ]:
        #
        lProblems.append( 'getTimeFromISODateTime()' )
        #
    if getHrMinFromISODateTime( sNow ) != sNow[ -8 : -3 ]:
        #
        lProblems.append( 'getHrMinFromISODateTime()' )
        #
    if      getSecsSinceEpochFromString( sNow ) < 1176833194 or \
            getSecsSinceEpochFromString( sNow ) > 2000000000:
        #
        lProblems.append( 'getSecsSinceEpochFromString()' )
        #
    #
    lParts = tuple( sNow.split() )
    #
    sReconstitute = '%s_%s' % lParts
    #
    if sNoSpace != sReconstitute.replace( ':', '.' ):
        #
        print3( sNoSpace, lParts )
        lProblems.append( 'getIsoDateTimeStrFromSecsNoSpace()' )
        #
    #    
    tNow = getDateTimeTupleFromString( sNow )
    #
    if len( tNow ) != 9:
        #
        lProblems.append( 'getDateTimeTupleFromString()' )
        #
    if repr( getDateTimeObjFromString( sNow ) ) != 'datetime.datetime' + repr( tNow[ : 6 ] ):
        #
        lProblems.append( 'getDateTimeObjFromString()' )
        #
    #
    if getSecsFromDuration( '01:01:01' ) != 3661:
        #
        lProblems.append( 'getSecsFromDuration()' )
        #
    #
    if getDurationFromSecs( getSecsFromDuration( '01:01:01' ) ) != '01:01:01':
        #
        lProblems.append( 'getDurationFromSecs()' )
        #
    #
    sApacheDateTime = '23/Sep/2012:06:40:18 +0800'
    #
    if getIsoOffApacheDateTime( sApacheDateTime ) != '2012-09-23 06:40:18':
        #
        lProblems.append( 'getIsoOffApacheDateTime()' )
        #
    #
    sApacheDate = '23-Sep-2012'
    #
    if getIsoOffApacheDate( sApacheDate ) != '2012-09-23':
        #
        lProblems.append( 'getIsoOffApacheDate()' )
        #
    #
    if getIsoDateFromOther( '17 Jan 2014' ) != '2014-01-17':
        #
        lProblems.append( 'getIsoDateFromOther() "17 Jan 2014"' )
        #
    #
    if getIsoDateFromOther( ' 17 Jan 2014 ' ) != '2014-01-17':
        #
        lProblems.append( 'getIsoDateFromOther() " 17 Jan 2014 "' )
        #
    #
    if getIsoDateFromOther( ' 17 January 2014 ' ) != '2014-01-17':
        #
        lProblems.append( 'getIsoDateFromOther() " 17 January 2014 "' )
        #
    #
    if getDateTimeUSAfromISO( '2009-04-24 08:02:41' ) != '04/24/2009 08:02:41 AM':
        #
        lProblems.append( 'getDateTimeUSAfromISO() "2009-04-24 08:02:41"' )
        #
    #
    if getDateTimeUSAfromISO( '2009-01-27 19:34:33' ) != '01/27/2009 07:34:33 PM':
        #
        lProblems.append( 'getDateTimeUSAfromISO() "2009-01-27 19:34:33"' )
        #
    #
    if getDateUSAfromISO( '2009-01-27' ) != '01/27/2009':
        #
        print3( getDateUSAfromISO( '2009-01-27' ) )
        lProblems.append( 'getDateUSAfromISO() "2009-01-27"' )
        #
    #
    sExpectDateTime = '2008-06-30 10:29:00'
    #
    if getIsoDateTimeFromOther(
            '06/30/2008 10:29:00 AM' ) != sExpectDateTime:
        #
        lProblems.append( 'getIsoDateTimeFromOther() "06/30/2008 10:29:00 AM"' )
        #
    #
    if getIsoDateTimeFromUSAdateTime(
            '06/30/2008 10:29:00 AM' ) != sExpectDateTime:
        #
        lProblems.append( 'getIsoDateTimeFromUSAdateTime() "06/30/2008 10:29:00 AM"' )
        #
    #
    sNBdateTime = '6/11/12 0:00'
    #
    if getIsoDateTimeFromUSAdateTime( sNBdateTime ) != '2012-06-11 00:00:00':
        #
        lProblems.append( 'getIsoDateTimeFromUSAdateTime() "%s"' % sTryDate )
        #
    #
    #
    sTryDate = sNBdateTime[ : -5 ]
    #
    if getIsoDateFromUSAdate( sTryDate ) != '2012-06-11':
        #
        lProblems.append( 'getIsoDateFromUSAdate() "%s"' % sTryDate )
        #
    #
    #
    # sNBdateTime = '06/11/12 0:00'
    #
    # print3( 'getIsoDateFromUSAdate( "%s" ):' % sTryDate, getIsoDateFromUSAdate( sTryDate ) )
    #
    #
    sayTestResult( lProblems )
