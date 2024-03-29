#!/home/rick/.local/bin/pythonTest
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
#   http://www.gnu.org/licenses/
#
# Copyright 2004-2023 Rick Graves
#

from datetime   import datetime, timedelta
from time       import gmtime, localtime, mktime
from time       import strftime, strptime, time, tzname, timezone


try:
    from ..Iter.AllVers import lMap, getEnumerator
    from ..Object       import Finished
    from ..String.Find  import getRegExObj
    from ..Time         import (
            _sFormatISOdateTime,
            _sFormatISOdate,
            _sFormatDateAm,
            _sFormatDateAmShort,
            _sFormatISONoSpace,
            _sFormatNatureUSA,
            _sFormatUSAdateTime,
            _sFormatEbay_DateTime,
            _dMonthsNamesShort ) # explicit imports better than implicit
except ( ValueError, ImportError ):
    from Iter.AllVers   import lMap, getEnumerator
    from Object         import Finished
    from String.Find    import getRegExObj
    from Time           import (
            _sFormatISOdateTime,
            _sFormatISOdate,
            _sFormatDateAm,
            _sFormatDateAmShort,
            _sFormatISONoSpace,
            _sFormatNatureUSA,
            _sFormatUSAdateTime,
            _sFormatEbay_DateTime,
            _dMonthsNamesShort ) # explicit imports better than implicit



class FormatMismatchError( Exception ): pass



_oApacheDelimiters = getRegExObj( '[/: ]' )


def getMonthNumOffName( sMonth ):
    #
    sNumb = ''
    #
    iMonth = _dMonthsNamesShort.get( sMonth[:3].title() )
    #
    if iMonth:
        #
        sNumb = '%02d' % iMonth
        #
    #
    return sNumb


def getIsoDateTimeFromObj( oDateTime, sFormat = _sFormatISOdateTime ):
    #
    return oDateTime.strftime( sFormat )


def getIsoDateTimeStrFromSecs(
        fSecsSinceEpoch = None, bWantLocal = True, sFormat = _sFormatISOdateTime ):
    #
    #
    getTime             = localtime if bWantLocal else gmtime
    #
    if fSecsSinceEpoch is None: fSecsSinceEpoch = time()
    #
    tSayTime            = getTime( fSecsSinceEpoch )
    #
    return strftime( sFormat, tSayTime )



def getIsoDateTimeStrFromSecsNoSpace(
        fSecsSinceEpoch = None, bWantLocal = True, sFormat = _sFormatISONoSpace ):
    #
    return getIsoDateTimeStrFromSecs( fSecsSinceEpoch, bWantLocal, sFormat  )




def getNormalDateFromSecs( fSecsSinceEpoch = None, bWantLocal = True ):
    #
    sFormat = '%d %B %Y'
    #
    return getIsoDateTimeStrFromSecs( fSecsSinceEpoch, bWantLocal, sFormat = sFormat )




def getDateTimeTupleFromString( sDateTime, sFormat = _sFormatISOdateTime ):
    #
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
            sFormat     = _sFormatISOdateTime,
            bAdjust2UTC = False ):
    #
    #
    tDateTime           = getDateTimeTupleFromString( sDateTime, sFormat )
    #
    iAdjust4TZ          = timezone if bAdjust2UTC else 0
    #
    return int( mktime( tDateTime ) ) + iAdjust4TZ




def getDateTimeObjFromString(
            sDateTime,
            sFormat     = _sFormatISOdateTime,
            bAdjust2UTC = False,
            oTimeZone   = None ):
    #
    tDateTime       = getDateTimeTupleFromString( sDateTime, sFormat )
    #
    lDateTime       = list( tDateTime[ : 6 ] )
    #
    lDateTime.extend( [ 0, oTimeZone ] )
    #
    oDateTimeObj    = datetime( *lDateTime )
    #
    iAdjust4TZ  = timezone if bAdjust2UTC else 0
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
        sFormatIn = _sFormatNatureUSA, sFormatWant = _sFormatISOdateTime ):
    #
    '''
    handles coversions from formats such as 17 Jan 2014
    returns string date in desired format
    '''
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
    elif sFormatIn == _sFormatNatureUSA:
        #
        # strip leading / trailing blanks
        #
        lParts = [ s for s in _oApacheDelimiters.split( sDate ) if s ]
        #
        for i, sPart in getEnumerator( lParts ):
            #
            sPartTitlized = sPart[:3].title()
            #
            if sPartTitlized in _dMonthsNamesShort:
                #
                lParts[ i ] = str( _dMonthsNamesShort[ sPartTitlized ] )
                #
                break
                #
            #
        #
        sNewDate = ' '.join( lParts )
        #
    else:
        #
        pass # raise NotImplementedError
    #
    #
    tDate = strptime( sNewDate, sFormatIn )
    #
    return strftime( sFormatWant, tDate )[ : 10 ]



def getOtherTimeDatefromISO( sTimeStamp, sFormat = _sFormatUSAdateTime ):
    #
    #
    oDateTime = getDateTimeObjFromString( sTimeStamp )
    #
    return oDateTime.strftime( sFormat )



def getDateTimeUSAfromISO( sTimeStamp, sFormat = _sFormatUSAdateTime ):
    #
    return getOtherTimeDatefromISO( sTimeStamp, sFormat )


def getOtherDatefromISO( sDate, sFormat = _sFormatISOdate ):
    #
    oDateTime = getDateTimeObjFromString( sDate, _sFormatISOdate )
    #
    return oDateTime.strftime( sFormat )


def getDateUSAfromISO( sDate, sFormat = _sFormatDateAm ):
    #
    return getOtherDatefromISO( sDate, sFormat )



def getIsoDateTimeFromOther( sDateTime, sFormat = _sFormatUSAdateTime ):
    #
    oDateTime = getDateTimeObjFromString( sDateTime, sFormat )
    #
    return getIsoDateTimeFromObj( oDateTime )





def getIsoDateTimeFromOtherStr( sDate, sFormat = _sFormatUSAdateTime ):
    #
    oDateTime = getDateTimeObjFromString( sDate, sFormat )
    #
    sISO = getIsoDateTimeFromObj( oDateTime )
    #
    return sISO



def getDateTimeObjFromIsoDateStr(
            sDate,
            sFormat     = _sFormatISOdateTime,
            bAdjust2UTC = False,
            oTimeZone   = None ):
    #
    if len( sDate ) == 10:
        #
        sDateTime = '%s 00:00:00' % sDate
        #
    else:
        #
        sDateTime = sDate
        #
    #
    return getDateTimeObjFromString(
            sDateTime, sFormat, bAdjust2UTC, oTimeZone )



def getIsoDateFromOtherStr( sDate, sFormat = _sFormatDateAmShort ):
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
            sISO = getIsoDateFromOtherStr( sDate, _sFormatDateAm      )
            raise Finished
        except ( ValueError, ImportError ):
            sISO = getIsoDateFromOtherStr( sDate, _sFormatDateAmShort )
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
            sISO = getIsoDateTimeFromOther( sDateTime, _sFormatUSAdateTime )
            raise Finished
        except ( ValueError, ImportError ):
            pass
        try:
            # two digit year, drop seconds, no AM/PM
            sISO = getIsoDateTimeFromOther( sDateTime, '%m/%d/%y %H:%M' )
            raise Finished
        except ( ValueError, ImportError ):
            pass
        try:
            # try 4 digit year, no seconds, no AM/PM
            sISO = getIsoDateTimeFromOther( sDateTime, '%m/%d/%Y %H:%M' )
            raise Finished
        except ( ValueError, ImportError ):
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
    #
    sExpect = 'datetime.datetime' + repr( tNow[ : 6 ] )
    #
    if repr( getDateTimeObjFromString( sNow ) ) != sExpect:
        #
        print( 'got   :', repr( getDateTimeObjFromString( sNow ) ) )
        print( 'expect:', sExpect )
        lProblems.append( 'getDateTimeObjFromString()' )
        #
    #
    sDateTimeStrRepr   = (
            repr( getDateTimeObjFromIsoDateStr( sNow[:10] ) ) )
    sDateTimeStrExpect = (
            'datetime.datetime' + repr( tNow[ : 6 ] )[:13] + ' 0, 0)' )
    #
    if sDateTimeStrRepr!= sDateTimeStrExpect:
        #
        from difflib import ndiff
        print3( 'sNow:', sNow )
        print3( 'repr( tNow[ : 6 ] )[:13] ):',
                '"%s"' % repr( tNow[ : 6 ] )[:13] )
        print3( 'type( sDateTimeStrRepr   ):', type( sDateTimeStrRepr ) )
        print3( 'type( sDateTimeStrExpect ):', type( sDateTimeStrExpect ) )
        print3( '\n'.join(ndiff([sDateTimeStrRepr], [sDateTimeStrExpect])) )
        print3( 'repr( getDateTimeObjFromIsoDateStr( sNow[:10] ) )        :',
                 '"%s"' % repr( getDateTimeObjFromIsoDateStr( sNow[:10] ) ) )
        print3( "'datetime.datetime' + repr( tNow[ : 6 ] )[:13] + ' 0, 0)':",
                '"datetime.datetime' + repr( tNow[ : 6 ] )[:13] + ' 0, 0)"' )
        print3()
        #
        lProblems.append( 'getDateTimeObjFromIsoDateStr()' )
        #
    #
    sDateTime = "2017-12-15T05:22:47.000Z"
    #
    oDateTime = getDateTimeObjFromString( sDateTime, _sFormatEbay_DateTime )
    #
    if oDateTime != datetime( 2017, 12, 15, 5, 22, 47, 0 ):
        #
        lProblems.append( 'getDateTimeObjFromString() w ebay format' )
        #
    #
    sDateTimeGot = getIsoDateTimeFromObj( oDateTime, _sFormatEbay_DateTime )
    #
    if sDateTimeGot != sDateTime:
        #
        print( 'got   :', repr( sDateTimeGot ) )
        print( 'expect:', repr( sDateTime    ) )
        #
        lProblems.append( 'getIsoDateTimeFromObj() w ebay format' )
        #
    #
    #
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
