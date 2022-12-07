#!/home/rick/.local/bin/pythonTest
# -*- coding: utf-8 -*-
#
# time functions Date
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

from calendar           import weekday
from datetime           import datetime, timedelta

try:
    from .Output        import getNowIsoDateTimeStr
    from ..Iter.AllVers import iMap
except ( ValueError, ImportError ):
    from Time.Output    import getNowIsoDateTimeStr
    from Iter.AllVers   import iMap


def getDateFromISODateTime( sDateTime = getNowIsoDateTimeStr() ):
    #
    return sDateTime[    : 10 ]


def getIntegerDOW( iYear, iMonth, iDay ):
    #
    """Get DOW, Sunday is 0, Monday is 1, etc.  Pass Year, Month, Day."""
    #
    #
    #
    iYear, iMonth, iDay = iMap( int, ( iYear, iMonth, iDay ) )
    #
    iDOW                = weekday( iYear, iMonth, iDay ) + 1
    #
    if iDOW >= 7: iDOW = 0
    #
    return iDOW



def getDOWfromISO( sDate ):
    #
    sYear, sMonth, sDay = sDate[:10].split( '-' )
    #
    return getIntegerDOW( sYear, sMonth, sDay )



def getPriorWeekday( oDate ):
    #
    oReturn = oDate # Objects of these types are immutable.
    #
    oOneDay = timedelta( days = 1 )
    #
    # weekday() day of the week as an integer,
    # where Monday is 0 and Sunday is 6
    #
    while oReturn.weekday() > 4:
        #
        oReturn -= oOneDay
        #
    #
    return oReturn



if __name__ == "__main__":
    #
    from time           import time
    from datetime       import date
    #
    from Collect.Test   import allMeet
    from Collect.Filter import RemoveDupes
    from Iter.AllVers   import tMap, tRange
    from Numb.Get       import getAdder
    from Time.Convert   import getIsoDateTimeStrFromSecs
    from Time.Delta     import getIsoDateTimeFromIsoDateTimePlus
    from Time.Test      import isISOdatetime
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    iNow    = int( time() )
    sNow    = getIsoDateTimeStrFromSecs( iNow )
    #
    if not isISOdatetime( getDateFromISODateTime( sNow ) + ' 08:08:08' ):
        #
        lProblems.append( 'getDateFromISODateTime()' )
        #
    #
    tDays = tRange( 1, 8 ) # 1 - 7
    #
    def getDOW4April( iDay ): return getIntegerDOW( 2007, 4, iDay ) # 1 April 2007 was Sunday
    #
    tDOWs = tMap( getDOW4April, tDays ) # should be 0 - 6
    #
    oSubtractOne = getAdder( -1 )
    #
    if tMap( oSubtractOne, tDays ) != tDOWs:
        #
        lProblems.append( 'getIntegerDOW()' )
        #
    #
    def getISOs4Week( iPlusDay ): return getIsoDateTimeFromIsoDateTimePlus( sNow, iPlusDay )
    #
    tISOs4Week = tMap( getISOs4Week, tDOWs ) # list of 7 ISOdatetimes, now, tomorrow, etc.
    #
    tDOWsFromNow = tMap( getDOWfromISO, tISOs4Week ) # list of 7 DOWs, today, tomorrow, etc.
    #
    def GotDOW( iDay ): return iDay in tDOWs
    #
    if not allMeet( tDOWsFromNow, GotDOW ) or len( RemoveDupes( tDOWsFromNow ) ) != 7:
        #
        lProblems.append( 'getDOWfromISO()' )
        #
    #
    oOneDay = timedelta( days = 1 )
    #
    oTodayLess0 = date.today()
    oTodayLess1 = oTodayLess0 - oOneDay
    oTodayLess2 = oTodayLess1 - oOneDay
    oTodayLess3 = oTodayLess2 - oOneDay
    oTodayLess4 = oTodayLess3 - oOneDay
    oTodayLess5 = oTodayLess4 - oOneDay
    oTodayLess6 = oTodayLess5 - oOneDay
    #
    lObjects = [ oTodayLess0,
                 oTodayLess1,
                 oTodayLess2,
                 oTodayLess3,
                 oTodayLess4,
                 oTodayLess5,
                 oTodayLess6 ]
    #
    lDays = [ getPriorWeekday( o ).weekday() for o in lObjects ]
    #
    lDays.sort()
    #
    if lDays != [0, 1, 2, 3, 4, 4, 4]:
        #
        lProblems.append( 'getPriorWeekday()' )
        #
    #
    #
    sayTestResult( lProblems )
