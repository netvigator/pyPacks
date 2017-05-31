#!/usr/bin/pythonTest
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
#   http://www.gnu.org/licenses/gpl.html
#
# Copyright 2004-2011 Rick Graves
#


sFormatISO          = '%Y-%m-%d %H:%M:%S'

from Time.Output    import getNowIsoDateTimeStr

def getDateFromISODateTime( sDateTime = getNowIsoDateTimeStr() ):
    #
    return sDateTime[    : 10 ]


def getIntegerDOW( iYear, iMonth, iDay ):
    #
    """Get DOW, Sunday is 0, Monday is 1, etc.  Pass Year, Month, Day."""
    #
    from calendar import weekday
    #
    from Iter.AllVers import iMap
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






if __name__ == "__main__":
    #
    from time           import time
    from datetime       import datetime
    #
    from Collect.Test   import AllMeet
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
    if not AllMeet( tDOWsFromNow, GotDOW ) or len( RemoveDupes( tDOWsFromNow ) ) != 7:
        #
        lProblems.append( 'getDOWfromISO()' )
        #
    #
    sayTestResult( lProblems )