#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# time functions Output
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

sFormatISO      = '%Y-%m-%d %H:%M:%S'
_iSecsPerDay    = 24 * 3600

bDebugPrint         = False
bTurnOnDebugPrint   = False

from String.Replace import getManyOldWithManyNewSwapper


_dSafeForFileName   = { ' ' : '_', ':' : '.' } # Windows chokes on colons

_oGetSafe4FileName  = getManyOldWithManyNewSwapper( _dSafeForFileName )


def sayGMT( tNowGMT = None, sFormat = sFormatISO, sBetween = ' ' ):
    #
    from time       import strftime
    from Time.Clock import getTupleGMT
    #
    if tNowGMT is None:
        #
        tNowGMT    = getTupleGMT()
        #
    else:
        #
        if len( tNowGMT ) == 8:
            #
            tNowGMT = list( tNowGMT )[ : 8 ]
            #
            tNowGMT.extend( [ 0, 0 ] )
        #
    #
    sSayGMT = strftime( sFormat, tNowGMT )
    #
    if sBetween != ' ':
        #
        sSayGMT = sSayGMT.replace( ' ', sBetween )
        #
    #
    return sSayGMT 



def sayLocalTime( tNowGMT = None, sFormat = '%a, %d %b %Y, %H:%M:%S' ):
    #
    from time import strftime, localtime, tzname
    #
    if tNowGMT is None:    tNowGMT    = localtime()
    #
    return strftime( sFormat + ' ' + tzname[-1], tNowGMT )



def sayIsoDateTimeLocal( tNowGMT = None ):
    #
    return sayLocalTime( sFormat = sFormatISO, tNowGMT = tNowGMT )




def sayLocalTimeOnly( tNowGMT = None ):
    #
    sSayTime = sayLocalTime( tNowGMT )
    #
    return sSayTime.split( ', ' )[ -1 ]


def sayLocalDateNoTime( tNowGMT = None ):
    #
    sSayTime = sayLocalTime( tNowGMT )
    #
    lSayTime = sSayTime.split( ', ' )[ : -1 ]
    #
    return ', '.join( lSayTime )



def getNowIsoDateTimeStr( bWantLocal = True ):
    #
    from Time.Convert import getIsoDateTimeStrFromSecs
    #
    return getIsoDateTimeStrFromSecs( bWantLocal = bWantLocal )



def getNowIsoDateOnly( bWantLocal = True ):
    #
    from Time.Convert import getIsoDateTimeStrFromSecs
    #
    sDateTime = getIsoDateTimeStrFromSecs( bWantLocal = bWantLocal )
    #
    lParts = sDateTime.split()
    #
    return lParts[0]



def getNowIsoDateTimeFileNameSafe( bWantLocal = True ):
    #
    sNow = getNowIsoDateTimeStr( bWantLocal )
    #
    return _oGetSafe4FileName( sNow )



def getNowIsoDateTimeNoSpacesNoSeconds( bWantLocal = True ):
    #
    sNow = getNowIsoDateTimeStr( bWantLocal )
    #
    return sNow[ : 16 ].replace( ' ', '_' )


def getIsoDateTimeNowPlusNoSpaces(
        iDays       = 0,
        iHours      = 0,
        iMins       = 0,
        iSecs       = 0,
        bWantLocal  = True ):
    #
    '''
    get ISO Date Time No Spaces From Secs from now
    if params are positive, returns future time
    if params are negative, returns time in the past
    '''
    #
    from Time.Delta import getIsoDateTimeNowPlus
    #
    sTime = getIsoDateTimeNowPlus(
        iDays       = iDays,
        iHours      = iHours,
        iMins       = iMins,
        iSecs       = iSecs,
        bWantLocal  = bWantLocal )
    #
    return sTime.replace( ' ', '_' )


def getIsoDateTimeNoSpacesFromSecsFromNow( fSecsFromNow, bWantLocal = True ):
    #
    '''
    get ISO Date Time No Spaces From Secs from now
    if fSecsFromNow is positive, returns future time
    if fSecsFromNow is negative, returns time in the past
    '''
    #
    return getIsoDateTimeNowPlusNoSpaces(
                iSecs = fSecsFromNow, bWantLocal = bWantLocal )



def getSayDurationAsDecimal( nSince = 0, nNow = None ):
    #
    from String.Output  import ReadableNo
    from Time.Delta     import getDuration, getDurationUnits
    #
    nDuration           = getDuration( nSince, nNow )
    #
    iMultiplyBy, sIncrements = getDurationUnits( nDuration )
    #
    fSay                = nDuration * iMultiplyBy
    #
    iDecimals           = 2
    #
    if fSay >= 100:
        #
        iDecimals       = 0
        #
    elif fSay >= 10:
        #
        iDecimals       = 1
        #
    #
    return '%s %s' % \
        ( ReadableNo( fSay, iWantDecimals=iDecimals ), sIncrements )



def getSayDurationAsDaysHrsMinsSecs( nSince = 0, nNow = None ):
    #
    """
    Normally you pass a time-since-epoch number from the past,
    function returns string showing days hours seconds ago.
    Also possible to pass two time-since-epoch numbers, and function
    returns string showing days hours seconds duration between them.
    """
    #
    from Iter.AllVers   import tMap
    from Numb.Output    import getSayLessThanOne
    from String.Output  import Plural
    from String.Eat     import eatCharsOffEnd
    from Time.Delta     import getDuration
    #
    nDuration           = getDuration( nSince, nNow )
    #
    tConstants          = ( _iSecsPerDay, 3600, 60, 1 )
    #
    lDurationParts      = []
    #
    nRemainder          = nDuration
    #
    for iConstant in tConstants:
        #
        iUnits, nRemainder = divmod( nRemainder, iConstant )
        #
        lDurationParts.append( iUnits )
        #
    #
    if (    lDurationParts[ 2 ] or
            lDurationParts[ 1 ] or
            lDurationParts[ 0 ] ):
        #
        # got days and/or hours and/or minutes
        #
        lDurationParts = tMap( int, lDurationParts )
        #
    #
    iDays               = lDurationParts[ 0 ]
    iHours              = lDurationParts[ 1 ]
    iMins               = lDurationParts[ 2 ]
    iSecs               = lDurationParts[ 3 ]
    #
    if      nDuration == 0.0:
        #
        sSayDuration    = '0.0 seconds'
        #
    elif    not( iDays or iHours or iMins or iSecs ):
        #
        sSayDuration    = '%s seconds' % eatCharsOffEnd(
                getSayLessThanOne( nRemainder ), '0' )
        #
    elif (  not( iDays or iHours or iMins ) and
                    iSecs == 1 and nRemainder < 0.02 ):
        #
        sSayDuration    = '1.0 second'
        #
    elif    not( iDays or iHours or iMins ) and iSecs <= 2:
        #
        sSayDuration    = '%s seconds' % eatCharsOffEnd(
                '%0.2f' % float( iSecs + nRemainder ), '0' )
        #
    elif    not( iDays or iHours or iMins ) and iSecs <= 10:
        #
        sSayDuration    = '%0.1f seconds' % float( iSecs + nRemainder )
        #
    elif    not( iDays or iHours or iMins ):
        #
        sSayDuration    = '%s seconds' % iSecs
        #
    elif    not( iDays or iHours          ):
        #
        sSayDuration    = '%s min%s %s sec%s' % (
                iMins, Plural( iMins ), iSecs , Plural( iSecs  ) )
        #
    elif    not( iDays                    ):
        #
        sSayDuration    = '%s h %s m %s s' % ( iHours, iMins, iSecs )
        #
    else:
        #
        sSayDuration    = '%s d %s h %s m' % ( iDays, iHours, iMins )
        #
    #
    return sSayDuration



def getIsoDate( fSecsSinceEpoch = None, bWantLocal = True ):
    #
    """
    call with no arguments and it returns current, local date in ISO string format.
    can pass seconds since epoch to get date for that time.
    """
    #
    from Time.Convert   import getIsoDateTimeStrFromSecs
    #
    sSayDate    = getIsoDateTimeStrFromSecs(
                        fSecsSinceEpoch, bWantLocal = bWantLocal )
    #
    return sSayDate[ : 10 ]



def getNormalDate( fSecsSinceEpoch = None, bWantLocal = True ):
    #
    """
    call with no arguments and it returns current, local date in ISO string format.
    can pass seconds since epoch to get date for that time.
    """
    #
    from Time.Convert    import getNormalDateFromSecs
    #
    return getNormalDateFromSecs( fSecsSinceEpoch, bWantLocal )




def _getDaysTuple():
    #
    from locale import DAY_1, DAY_2, DAY_3, DAY_4, DAY_5, DAY_6, DAY_7
    #
    return ( DAY_1, DAY_2, DAY_3, DAY_4, DAY_5, DAY_6, DAY_7 )


_tDaysOfWeek = _getDaysTuple()
    

def getTextDowOffIntDow( iDOW ):
    #
    from locale import nl_langinfo
    #
    return nl_langinfo( _tDaysOfWeek[ iDOW ] )



if __name__ == "__main__":
    #
    lProblems = []
    #
    from sys            import argv
    from time           import gmtime, time
    #
    from six            import print_ as print3
    #
    from Iter.AllVers   import tMap
    from String.Find    import getTextInQuotes
    from Time.Delta     import getDeltaDaysFromISOs
    from Time.Test      import isISOdatetime
    from Time.Clock     import getTupleGMT
    from Time.Convert   import getIsoDateTimeStrFromSecs, getDateTimeTupleFromString, \
                               getSecsSinceEpochFromString
    from Utils.Result   import sayTestResult
    #
    tNineZeros  = gmtime( pow(10,9) )
    iNow        = time()
    sNow        = getIsoDateTimeStrFromSecs( iNow )
    tNowGMT     = getTupleGMT()
    #
    args = argv[ 1 : ]
    #
    if args and args[0] == 'debug':
        #
        bTurnOnDebugPrint = True
        #
    #
    if sayGMT( tNineZeros ) != '2001-09-09 01:46:40':
        #
        lProblems.append( 'sayGMT()' )
        #
    if sayLocalTime( tNowGMT, sFormat = '%a, %d %b %Y, %H:%M:%S' ) != \
            sayLocalTime( getDateTimeTupleFromString(
            sayLocalTime( tNowGMT, sFormat = '%a, %d %b %Y, %H:%M:%S' ),
                    sFormat = '%a, %d %b %Y, %H:%M:%S' ),
                    sFormat = '%a, %d %b %Y, %H:%M:%S' ):
        #
        lProblems.append( 'sayLocalTime()' )
        #
    if  not isISOdatetime( sayIsoDateTimeLocal( tNineZeros )[ : -4 ] ) or \
            sayIsoDateTimeLocal( tNowGMT ) != \
            sayIsoDateTimeLocal( getDateTimeTupleFromString( sayIsoDateTimeLocal( tNowGMT ) ) ):
        #
        lProblems.append( 'sayIsoDateTimeLocal()' )
        #
    if len( sayLocalTimeOnly( tNineZeros ) ) != 12:
        #
        lProblems.append( 'sayLocalTimeOnly()' )
        #
    if len( sayLocalDateNoTime( tNineZeros ) ) != 16:
        #
        lProblems.append( 'sayLocalDateNoTime()' )
        #
    if (    not isISOdatetime( getNowIsoDateTimeStr( bWantLocal = True  ) ) or
            not isISOdatetime( getNowIsoDateTimeStr( bWantLocal = False ) ) or
            abs( getSecsSinceEpochFromString(
                    getIsoDateTimeStrFromSecs(
                        getSecsSinceEpochFromString(
                            getNowIsoDateTimeStr() ) ) ) -
                 getSecsSinceEpochFromString( getNowIsoDateTimeStr() ) ) > 2 ):
        #
        lProblems.append( 'getNowIsoDateTimeStr()' )
        #
    sSpace = getNowIsoDateTimeStr()
    sNone  = getNowIsoDateTimeFileNameSafe()
    sNoSec = getNowIsoDateTimeNoSpacesNoSeconds()
    #
    if sSpace.replace( ' ', '_' ).replace( ':', '.' ) != sNone:
        #
        print3( 'getNowIsoDateTimeStr():         ', sSpace )
        print3( 'getNowIsoDateTimeFileNameSafe():', sNone  )
        #
        lProblems.append( 'getNowIsoDateTimeFileNameSafe()' )
        #
    #
    #
    sTomorrow  = getIsoDateTimeNoSpacesFromSecsFromNow(  24 * 3600 )
    sYesterday = getIsoDateTimeNoSpacesFromSecsFromNow( -24 * 3600 )
    #
    fYesterday2Tomorrow = getDeltaDaysFromISOs( sYesterday, sTomorrow )
    #
    bDebugPrint = bTurnOnDebugPrint
    #
    if abs( 2.0 - fYesterday2Tomorrow ) == 2.0 - 1.9583333333333333:
        #
        if bDebugPrint:
            print3( 'daylight savings change? bWantLocal = True' )
        #
    elif fYesterday2Tomorrow != 2.0:
        #
        lProblems.append( 'getIsoDateTimeNoSpacesFromSecsFromNow()' )
        #
    #
    bDebugPrint = False
    #
    tHistory = [ iNow - 10, iNow - 100, iNow - 1000, iNow - 10000, iNow - 100000 ]
    #
    def getHistoryDecimal( iThen ): return getSayDurationAsDecimal( iThen, iNow )
    #
    if tMap( getHistoryDecimal, tHistory ) != \
            ('10.0 seconds', '1.66 minutes', '16.6 minutes', '2.77 hours', '1.15 days'):
        #
        lProblems.append( 'getSayDurationAsDecimal()' )
        #
    #
    def getHistoryText( iThen ): return getSayDurationAsDaysHrsMinsSecs( iThen, iNow )
    #
    lOutput  = tMap( getHistoryText, tHistory )
    lWantOut = ('10.0 seconds', '1 min 40 secs', '16 mins 40 secs', '2 h 46 m 40 s', '1 d 3 h 46 m')
    #
    if lOutput != lWantOut:
        #
        print3( 'lWantOut:', lWantOut )
        print3( 'lOutput: ', lOutput )
        #
        lProblems.append( 'getSayDurationAsDaysHrsMinsSecs()' )
        #
    if getIsoDate( iNow ) != sNow[ : 10 ]:
        #
        lProblems.append( 'getIsoDate()' )
        #
    #
    if tMap( getTextDowOffIntDow, ( 0, 1, 2, 3, 4, 5, 6 ) ) != \
            (   'Sunday',
                'Monday',
                'Tuesday',
                'Wednesday',
                'Thursday',
                'Friday',
                'Saturday' ):
        #
        lProblems.append( 'getTextDowOffIntDow()' )
        #
    #
    sayTestResult( lProblems )