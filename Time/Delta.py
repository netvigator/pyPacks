#!/home/rick/.local/bin/pythonTest
# -*- coding: utf-8 -*-
#
# time functions Delta
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

from bisect             import bisect_left, bisect_right
from datetime           import datetime, date
from time               import time, localtime
try:
    from .Clock         import getSecsSinceEpoch
    from .Convert       import getIsoDateTimeStrFromSecs, getDateTimeObjFromString
    from .Output        import getNowIsoDateTimeStr, sayIsoDateTimeLocal
    from ..Time         import _iSecsPerDay, _sFormatISOdate # in __init__.py
except ( ValueError, ImportError ):
    from Time.Clock     import getSecsSinceEpoch
    from Time.Convert   import getIsoDateTimeStrFromSecs, getDateTimeObjFromString
    from Time.Output    import getNowIsoDateTimeStr, sayIsoDateTimeLocal
    from Time           import _iSecsPerDay, _sFormatISOdate # in __init__.py



_tMagnitudes    = ( 1e-3, 1,  60,     3600, _iSecsPerDay, _iSecsPerDay * 24 )
_tMultiplyBy    = ( 1e6,  1e3, 1, 1.0 / 60,  1.0 / 3600, 1.0 / _iSecsPerDay )
_tSayIncrement  = ( 'microseconds',
                    'milliseconds',
                    'seconds',
                    'minutes',
                    'hours',
                    'days' )

_bDebugPrint        = False
_bTurnOnDebugPrint  = False

def getDurationUnits( nSayTime ):
    #
    #
    iWhich = bisect_right( _tMagnitudes, nSayTime )
    #
    return _tMultiplyBy[ iWhich ], _tSayIncrement[ iWhich ]



def getDuration( nSince = 0, nNow = None ):
    #
    """
    Normally you pass a time-since-epoch number from the past,
    function returns number of seconds since then.
    Also possible to pass two time-since-epoch numbers, and function
    returns number of seconds duration between them.
    """
    #
    #
    if nNow is None:
        #
        nNow    = time()
        #
    #
    nDuration   = nNow - nSince
    #
    return nDuration



def _getSecsPlusDHMS( fSecs, iDays = 0, iHours = 0, iMins = 0, iSecs = 0 ):
    #
    """
    pass seconds (float) plus number of days, hours, minutes & seconds
    returns seconds adjusted by days, hours, minutes & seconds passed
    """
    #
    return int(
        fSecs +
        ( iDays * 24 * 3600 ) +
        ( iHours * 3600 ) +
        ( iMins * 60 ) +
          iSecs )



def getSecsNowPlusDHMS(
        iDays       = 0,
        iHours      = 0,
        iMins       = 0,
        iSecs       = 0,
        bWantLocal  = True ):
    #
    #
    getTime = time if bWantLocal else getSecsSinceEpoch
    #
    return _getSecsPlusDHMS( getTime(), iDays, iHours, iMins, iSecs )




def getIsoDateTimeNowPlus(
        iDays       = 0,
        iHours      = 0,
        iMins       = 0,
        iSecs       = 0,
        bWantLocal  = True ):
    #
    #
    iWhen = getSecsNowPlusDHMS(
                iDays, iHours, iMins, iSecs, bWantLocal = bWantLocal )
    #
    return getIsoDateTimeStrFromSecs( iWhen, bWantLocal = 1 ) # don't adjust twice



def _getIsoDateTimeSecsPlus( fSecs,
        iDays       = 0,
        iHours      = 0,
        iMins       = 0,
        iSecs       = 0,
        bWantLocal  = True ):
    #
    #
    iWhen           = _getSecsPlusDHMS( fSecs, iDays, iHours, iMins, iSecs )
    #
    return getIsoDateTimeStrFromSecs( iWhen, bWantLocal = 1 )



def getIsoDateFromIsoDatePlus( sDate, iDays = 0 ):
    #
    # this is a dummy to allow the function below to compile without error,
    # will be overwritten in the following function
    #
    pass 



def getIsoDateTimeFromIsoDateTimePlus( sDateTime,
        iDays       = 0,
        iHours      = 0,
        iMins       = 0,
        iSecs       = 0,
        bWantLocal  = True ):
    #
    try: # moving this to the top breaks this package!
        from .Convert     import getSecsSinceEpochFromString
    except ( ValueError, ImportError ): # maybe circular import issue
        from Time.Convert import getSecsSinceEpochFromString
    #
    if (    iHours == 0 and
            iMins  == 0 and
            iSecs  == 0 and
            len( sDateTime ) == 10 ):
        #
        # if only the date is passed to this function
        # it can work on just the date
        #
        sDateTimePlus = getIsoDateFromIsoDatePlus( sDateTime, iDays )
        #
    else:
        #
        iBaseSecs = getSecsSinceEpochFromString( sDateTime )
        #
        sDateTimePlus = _getIsoDateTimeSecsPlus( iBaseSecs, iDays, iHours, iMins, iSecs, bWantLocal = bWantLocal )
        #
    #
    return sDateTimePlus


    
def getIsoDateFromIsoDatePlus( sDate, iDays = 0 ):
    #
    sDateTime = '%s 12:00:00' % sDate[:10]
    #
    sDateTimePlus = getIsoDateTimeFromIsoDateTimePlus( sDateTime, iDays )
    #
    return sDateTimePlus[:10]


def getDeltaDaysFromObjs( oOlder, oNewer = None ):
    #
    #
    if oNewer is None: oNewer = datetime.now(tz=None)
    #
    oDelta      = oNewer - oOlder
    #
    fDeltaSecs  = (
        oDelta.days * _iSecsPerDay +
        oDelta.seconds +
        round( oDelta.microseconds / 1000000.0 ) )
    #
    #
    return float( fDeltaSecs ) / _iSecsPerDay



# getDeltaDaysFromISOs      needs ISO date times
# getDeltaDaysFromStrings   needs ISO date times and rounds the return
# getDeltaDaysFromDates     needs ISO date w/o times

def getDeltaDaysFromISOs( sOlder, sNewer = None ):
    #
    """
    pass earlier, later ISO date-times
    This works the same as getDeltaDaysFromStrings
    but does not round off the answer,
    getDeltaDaysFromStrings does.
    getDeltaDaysFromDates returns days between dates.
    """
    #
    #
    if sNewer is None: sNewer = getNowIsoDateTimeStr()
    #
    oNewer  = getDateTimeObjFromString( sNewer )
    oOlder  = getDateTimeObjFromString( sOlder )
    #
    if _bDebugPrint:
        print3( 'oNewer:', repr( oNewer ) )
        print3( 'oOlder:', repr( oOlder ) )
    #
    return getDeltaDaysFromObjs( oOlder, oNewer )



def getDeltaDaysFromSecs( iOlder, iNewer = None ):
    #
    '''
    getDeltaDaysFromISOs      needs ISO date times
    getDeltaDaysFromStrings   needs ISO date times and rounds the return
    getDeltaDaysFromDates     needs ISO date w/o times
    '''
    #
    if iNewer is None: iNewer = time()
    #
    oNewer      = datetime.fromtimestamp( iNewer)
    #
    oOlder      = datetime.fromtimestamp( iOlder )
    #
    oDelta      = oNewer - oOlder
    #
    fDeltaSecs  = (
        oDelta.days * _iSecsPerDay +
        oDelta.seconds +
        round( oDelta.microseconds / 1000000.0 ) )
    #
    #
    return float( fDeltaSecs ) / _iSecsPerDay



def getDeltaDaysFromStrings( sEarlier, sLater = None, iDigitsAfterDot = 0 ):
    #
    """
    pass earlier, later ISO date-times
    This works the same as getDeltaDaysFromISOs
    but rounds off the answer,
    getDeltaDaysFromISOs does not.
    getDeltaDaysFromDates returns days between dates.
    NOTE this now defaults to integer output
    if you want a rounded float, pass iDigitsAfterDot
    """
    #
    try: # moving this to the top breaks this package!
        from .Convert   import getSecsSinceEpochFromString
    except ( ValueError, ImportError ): # maybe circular import issue
        from Convert    import getSecsSinceEpochFromString
    #
    if sLater is None:
        #
        tLater  = None
        #
    else:
        #
        tLater  = getSecsSinceEpochFromString( sLater )
        #
    #
    tEarlier    = getSecsSinceEpochFromString( sEarlier )
    #
    fDeltaDays  = getDeltaDaysFromSecs( tEarlier, tLater )
    #
    uReturn     = round( fDeltaDays, iDigitsAfterDot )
    #
    if iDigitsAfterDot == 0:
        #
        uReturn = int( uReturn )
        #
    #
    return uReturn



def getDeltaDaysFromDates( sEarlier, sLater = None ):
    #
    """
    pass earlier, later ISO dates (no time component)
    This works the same as getDeltaDaysFromISOs
    but rounds off the answer,
    getDeltaDaysFromISOs does not.
    """
    #
    #
    sTime       = ' 12:00:00'
    #
    if sLater is None: sLater = sayIsoDateTimeLocal()[:10]
    #
    sEarlier    += sTime
    sLater      += sTime
    #
    iDeltaDays  = getDeltaDaysFromStrings( sEarlier, sLater, 0 )
    #
    return iDeltaDays



def getDeltaYearsFromDates( sEarlier, sLater = None ):
    #
    '''
    getDeltaDaysFromISOs      needs ISO date times
    getDeltaDaysFromStrings   needs ISO date times and rounds the return
    getDeltaDaysFromDates     needs ISO date w/o times
    '''
    #
    return getDeltaDaysFromDates( sEarlier, sLater ) / 365.25




def getAgeOffDOB( uDOB, sFormatDate = _sFormatISOdate, uToday = None ):
    #
    if isinstance( uDOB, str ):
        #
        oDOB = getDateTimeObjFromString( uDOB, sFormatDate ).date()
        #
    else:
        #
        oDOB = uDOB
        #
    #
    if uToday is None:
        #
        oToday = date.today()
        #
    elif isinstance( uToday, str ):
        #
        oToday = getDateTimeObjFromString( uToday, sFormatDate ).date()
        #
    else:
        #
        oToday = uToday
        #
    #
    iAge = oToday.year - oDOB.year
    #
    if (        oToday.month == oDOB.month == 2 and
              ( oToday.day == 28 and oDOB.day == 29 ) ):
        #
        pass
        #
    elif (      oToday.month <  oDOB.month or
              ( oToday.month == oDOB.month and
                oToday.day   <  oDOB.day ) ):
        #
        iAge -= 1
        #
    #
    return iAge




if __name__ == "__main__":
    #
    from datetime       import datetime
    from time           import time
    from sys            import argv
    #
    from six            import print_ as print3
    #
    from Iter.AllVers   import tMap
    from Numb.Test      import isEven, isInteger
    from Time.Test      import isISOdatetime
    from Time.Convert   import getSecsSinceEpochFromString
    from Time.Convert   import getIsoDateTimeStrFromSecs
    from Utils.Result   import sayTestResult
    #
    args = argv[ 1 : ]
    #
    if args and args[0] == 'debug':
        #
        _bTurnOnDebugPrint = True
        #
    #
    lProblems = []
    #
    def getHalf( n ):
        if isInteger( n ) and ( n > 9 or isEven( n ) ):
            return n/2
        else:
            return n/2.0
    #
    tLessMags   = tMap( getHalf, _tMagnitudes )
    #
    if      getDurationUnits( tLessMags[0] ) != (
                    1000000.0,             'microseconds'  ) or \
            getDurationUnits( tLessMags[1] ) != (
                    1000.0,                'milliseconds'  ) or \
            getDurationUnits( tLessMags[2] ) != (
                    1,                     'seconds'       ) or \
            getDurationUnits( tLessMags[3] ) != (
                    0.016666666666666666,  'minutes'       ) or \
            getDurationUnits( tLessMags[4] ) != (
                    0.00027777777777777778,'hours'         ) or \
            getDurationUnits( tLessMags[5] ) != (
                    1.1574074074074073e-05,'days'          ):
        #
        lProblems.append( 'getDurationUnits()' )
        #
    #
    iNow        = int( time() )
    sNow        = getIsoDateTimeStrFromSecs( iNow )
    #
    def getBeforeAndNow( n ): return iNow - n, iNow
    #
    tDurations = tMap( getBeforeAndNow, _tMagnitudes )
    #
    if      getDuration( *tDurations[0] ) != 0.00099992752075195312 or \
            getDuration( *tDurations[1] ) !=                    1.0 or \
            getDuration( *tDurations[2] ) !=                   60.0 or \
            getDuration( *tDurations[3] ) !=                 3600.0 or \
            getDuration( *tDurations[4] ) !=                86400.0 or \
            getDuration( *tDurations[5] ) !=              2073600.0:
        #
        lProblems.append( 'getDuration()' )
        #
    if _getSecsPlusDHMS( iNow, iDays = 1, iHours = 1, iMins = 1, iSecs = 1 ) != iNow + 90061:
        #
        lProblems.append( '_getSecsPlusDHMS()' )
        #
    if getSecsNowPlusDHMS( 1, 1, 1, 1 ) - int( time() ) != 90061:
        #
        lProblems.append( 'getSecsNowPlusDHMS()' )
        #
    if not isISOdatetime( getIsoDateTimeNowPlus( 1, 1, 1, 1 ) ):
        #
        lProblems.append( 'getIsoDateTimeNowPlus() correctly formatted' )
        #
    #
    sYesterday = getIsoDateTimeNowPlus( -1 )
    sTomorrow  = getIsoDateTimeNowPlus(  1 )
    #
    _bDebugPrint = _bTurnOnDebugPrint
    #
    fYesterday2Tomorrow = getDeltaDaysFromISOs( sYesterday, sTomorrow )
    #
    if abs( 2.0 - fYesterday2Tomorrow ) == 2.0 - 1.9583333333333333:
        #
        if _bDebugPrint:
            print3( 'daylight savings change? bWantLocal = True' )
        #
    elif fYesterday2Tomorrow != 2.0:
        #
        print3( 'sYesterday, sTomorrow:', sYesterday, sTomorrow )
        print3( 'expecting 2.0, got %s' % fYesterday2Tomorrow )
        lProblems.append( 'getDeltaDaysFromISOs() local yesterday and today' )
        #
    #
    sYesterday = getIsoDateTimeNowPlus( -1, bWantLocal = False )
    sTomorrow  = getIsoDateTimeNowPlus(  1, bWantLocal = False )
    #
    fYesterday2Tomorrow = getDeltaDaysFromISOs( sYesterday, sTomorrow )
    #
    if abs( 2.0 - fYesterday2Tomorrow ) == 2.0 - 1.9583333333333333:
        #
        if _bDebugPrint:
            print3( 'daylight savings change? bWantLocal = False' )
        #
    elif fYesterday2Tomorrow != 2.0:
        #
        lProblems.append( 'getDeltaDaysFromISOs() UTC yesterday and today' )
        #
    #
    if getSecsSinceEpochFromString(
            _getIsoDateTimeSecsPlus( iNow, 1, 1, 1, 1 ) ) - iNow != 90061:
        #
        lProblems.append( '_getIsoDateTimeSecsPlus()' )
        #
    if getIsoDateTimeFromIsoDateTimePlus(
            getIsoDateTimeFromIsoDateTimePlus(
                        sNow, 1,  1,  1,  1 ),
                             -1, -1, -1, -1 ) != sNow or \
            getIsoDateTimeFromIsoDateTimePlus(
                        sNow, 1,  1,  1,  1 ) == sNow:
        #
        lProblems.append( 'getIsoDateTimeFromIsoDateTimePlus()' )
        #
    #
    iNow        = int( time() )
    #
    oOlder = datetime.fromtimestamp( iNow - _iSecsPerDay )
    #
    if getDeltaDaysFromObjs( oOlder ) - 1 > 0.0001:
        #
        lProblems.append( 'getDeltaDaysFromObjs()' )
        #
    #
    sNow    = getIsoDateTimeStrFromSecs( iNow )
    #
    sToday    = sNow[ : 10 ]
    sTomorrow = getIsoDateTimeFromIsoDateTimePlus( sNow, 1 )[ : 10 ]
    #
    if getIsoDateFromIsoDatePlus( sToday, 1 ) != sTomorrow:
        #
        lProblems.append( 'getIsoDateFromIsoDatePlus()' )
        #
    #
    if getIsoDateTimeFromIsoDateTimePlus( sToday, 1 ) != sTomorrow:
        #
        lProblems.append( 'getIsoDateTimeFromIsoDateTimePlus( [date only] )' )
        #
    #
    sOlder  = getIsoDateTimeFromIsoDateTimePlus( sNow, -1,  -1,  -1,  -1 )
    #
    fNowLessOlder = getDeltaDaysFromISOs( sOlder, sNow )
    #
    fDelta = 1.0423726851851851 - 1.0007060185185186
    #
    if abs( 1.0423726851851851 - fNowLessOlder ) == fDelta:
        #
        if _bDebugPrint:
            print3( 'daylight savings change? getDeltaDaysFromISOs()' )
        #
    elif fNowLessOlder != 1.0423726851851851:
        #
        print3( 'expecting 1.0423726851851851, got %s' % fNowLessOlder )
        #
        lProblems.append( 'getDeltaDaysFromISOs() '
                          'less 1 each day, hour, minute, second' )
        #
    #
    fDelta = 8.5 - 8.458333333333334
    
    fEightPlusDaysAgo = getDeltaDaysFromSecs(
                                iNow - ( 8.5 * _iSecsPerDay ), iNow )
    #
    if abs( 8.5 - fEightPlusDaysAgo ) == fDelta:
        #
        if _bDebugPrint:
            print3( 'daylight savings change? 8.5 days of seconds ago' )
        #
    elif fEightPlusDaysAgo != 8.5:
        #
        print3( 'expecting 8.5, got %s' % fEightPlusDaysAgo )
        #
        lProblems.append( 'getDeltaDaysFromSecs() 8.5 days of seconds ago' )
        #
    #
    fNowLessOlder = getDeltaDaysFromStrings( sOlder, sNow, 2 )
    #
    #print3( 1.04 - fNowLessOlder )
    if _bDebugPrint and abs( 1.04 - fNowLessOlder ) - 0.04 < .00001:
        #
        print3( 'daylight savings change? getDeltaDaysFromStrings()' )
        #
    elif fNowLessOlder != 1.04:
        #
        print3( 'expecting 1.04, got %s' % fNowLessOlder )
        #
        lProblems.append( 'getDeltaDaysFromStrings()' )
        #
    #
    iNowLessOlder = getDeltaDaysFromStrings(
                            sOlder, sNow, iDigitsAfterDot = 0 )
    #
    if iNowLessOlder != 1:
        #
        lProblems.append( 'getDeltaDaysFromStrings(iDigitsAfterDot = 0)' )
        #
    #
    _bDebugPrint = False
    #
    if getDeltaDaysFromDates( '2008-10-18', '2008-11-02' ) != 15:
        #
        lProblems.append( 'getDeltaDaysFromDates() earlier & later' )
        #
    if getDeltaDaysFromDates( '2008-10-18' ) < 200:
        #
        lProblems.append( 'getDeltaDaysFromDates() earlier only' )
        #
    #
    #
    iOldTimer = iNow - ( 50.5 * 365.25 * 24 * 3600 )
    #
    sDOB = getIsoDateTimeStrFromSecs( iOldTimer )[ : 10 ]
    #
    iAge = getAgeOffDOB( sDOB )
    #
    if iAge != 50:
        #
        lProblems.append( 'getAgeOffDOB( seconds date )' )
        #
    #
    #
    s50YrsAgoYesterday  = '%s%s' % (
            int( sYesterday[:4] ) - 50, sYesterday[4:10] )
    s50YrsAgoTomorrow   = '%s%s' % (
            int( sTomorrow [:4] ) - 50, sTomorrow [4:10] )
    #
    if getAgeOffDOB( s50YrsAgoYesterday ) != 50:
        #
        lProblems.append( 'getAgeOffDOB( s50YrsAgoYesterday )' )
        #
    #
    if getAgeOffDOB( s50YrsAgoTomorrow ) != 49:
        #
        lProblems.append( 'getAgeOffDOB( s50YrsAgoTomorrow )' )
        #
    #
    sLeapYearBD = '1972-02-29'
    sToday      = '2020-02-27'
    #
    if getAgeOffDOB( sLeapYearBD, uToday = sToday ) != 47:
        #
        lProblems.append( 'getAgeOffDOB( sLeapYearBD )' )
        #
    #
    sToday      = '2020-02-28'
    #
    if getAgeOffDOB( sLeapYearBD, uToday = sToday ) != 48:
        #
        lProblems.append( 'getAgeOffDOB( sLeapYearBD )' )
        #
    #
    #
    sToday      = '2020-03-01'
    #
    if getAgeOffDOB( sLeapYearBD, uToday = sToday ) != 48:
        #
        lProblems.append( 'getAgeOffDOB( sLeapYearBD )' )
        #
    #
    #
    sayTestResult( lProblems )
