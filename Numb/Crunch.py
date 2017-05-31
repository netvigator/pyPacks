#!/usr/bin/pythonTest
#
# Number functions Crunch specialized number crunchers
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
# Copyright 2012-2016 Rick Graves
#
bDebugPrint         = False
bTurnOnDebugPrint   = False

def getHourlyRateForNow( iMaxPerDay, iTotalLast24hrs, sFirstRequestTime, bWantLocal = False ):
    #
    from Time.Delta import getIsoDateTimeNowPlus as getNowPlus
    from Time.Delta import getDeltaDaysFromISOs  as getDeltaDays
    #
    iRateForNow = 0
    #
    iHourlyRate = iMaxPerDay / 24
    #
    sNow        = getNowPlus( iDays =  0, bWantLocal = bWantLocal )
    sYesterday  = getNowPlus( iDays = -1, bWantLocal = bWantLocal )
    #
    if not ( iTotalLast24hrs and sFirstRequestTime ):
        #
        # just started
        #
        iRateForNow = iMaxPerDay / 24
        #
        if bDebugPrint:
            print3( 'not ( iTotalLast24hrs and sFirstRequestTime )' )
        #
    elif sFirstRequestTime < sYesterday:
        #
        # running for more than one day
        #
        fDivideBy2      = ( iHourlyRate +
                ( iMaxPerDay - iTotalLast24hrs ) ) / 2.0
        #
        fDivideBy3      = ( iHourlyRate + iHourlyRate +
                ( iMaxPerDay - iTotalLast24hrs ) ) / 3.0
        #
        fDoubleHourly   = iHourlyRate * 2.0
        #
        fMaxLess        = iMaxPerDay - ( iTotalLast24hrs + 1 )
        #
        iRateForNow = min(
            fDivideBy2,
            fDivideBy3,
            fDoubleHourly,
            fMaxLess )
        #
        if bDebugPrint:
            print3( 'sFirstRequestTime < sYesterday' )
            print3( 'fDivideBy2     :', fDivideBy2 )
            print3( 'fDivideBy3     :', fDivideBy3 )
            print3( 'fDoubleHourly  :', fDoubleHourly )
            print3( 'fMaxLess       :', fMaxLess )
            print3( 'iMaxPerDay     :', iMaxPerDay )
            print3( 'iTotalLast24hrs:', iTotalLast24hrs )
        #
    else:
        #
        # still the first day but after startup
        #
        fHoursSinceStart = 24.0 * getDeltaDays( sFirstRequestTime, sNow )
        #
        fHoursRemaining  = 24.0 - fHoursSinceStart
        #
        iRateForNow = min(
            iHourlyRate * 2.0,
            iMaxPerDay - ( iTotalLast24hrs + 1 ) )
        #
        if fHoursRemaining > 0:
            #
            iRateForNow = min(
                iRateForNow,
                ( iMaxPerDay - iTotalLast24hrs ) / fHoursRemaining )
        #
        if bDebugPrint:
            print3( 'else' )
        #
    #
    if iRateForNow < 0: iRateForNow = 0
    #
    return int( round( iRateForNow ) )



if __name__ == "__main__":
    #
    from sys import argv
    #
    from six            import print_ as print3
    #
    from Numb.Test      import areClose
    from Time.Delta     import getIsoDateTimeNowPlus as getNowPlus
    from Utils.Result   import sayTestResult
    #
    args = argv[ 1 : ]
    #
    if args and args[0] == 'debug':
        #
        bTurnOnDebugPrint = True
        #
    #
    lProblems = []
    #
    iMaxPerDay          = 2500
    #
    iTotalLast24hrs     = 0
    sFirstRequestTime   = ''
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime )
    #
    if iRateForNow != int( iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() starting condition' )
        #
    #
    sFirstRequestTime = getNowPlus( iDays = -2, bWantLocal = False )
    #
    iTotalLast24hrs   = int( iMaxPerDay * 23.0 / 24 )
    #
    bDebugPrint = bTurnOnDebugPrint
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime )
    #
    if not areClose( iRateForNow, iMaxPerDay / 24.0 ):
        #
        print3( 'iRateForNow, iMaxPerDay / 24 :', iRateForNow, iMaxPerDay / 24 )
        lProblems.append( 'getHourlyRateForNow() UTC after one day, regular batches' )
        #
    #
    bDebugPrint = False
    #
    iTotalLast24hrs   = iMaxPerDay * 10 / 24
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime )
    #
    if not areClose( iRateForNow, 2 * iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() UTC after one day, batches were short' )
        #
    #
    iTotalLast24hrs   = int( iMaxPerDay * 23.5 / 24 )
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime )
    #
    if not areClose( iRateForNow, 0.5 * iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() UTC after one day, batches were long' )
        #
    #
    iTotalLast24hrs   = int( iMaxPerDay * 21 / 24 )
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime )
    #
    if not areClose( iRateForNow, 1.67 * iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() UTC after one day, batches were a little short' )
        #
    #
    sFirstRequestTime = getNowPlus( iHours = -12, bWantLocal = False )
    #
    iTotalLast24hrs   = iMaxPerDay * 12 / 24
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime )
    #
    if not areClose( iRateForNow, iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() UTC half way thru day 1, batches were regular' )
        #
    #
    iTotalLast24hrs   = iMaxPerDay * 6 / 24
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime )
    #
    if not areClose( iRateForNow, 1.5 * iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() UTC half way thru day 1, batches were short' )
        #
    #
    iTotalLast24hrs   = iMaxPerDay * 15 / 24
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime )
    #
    if not areClose( iRateForNow, 0.75 * iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() UTC half way thru day 1, batches were long' )
        #
    #
    sFirstRequestTime = getNowPlus( iHours = -4, bWantLocal = False )
    #
    iTotalLast24hrs   = iMaxPerDay * 4 / 24
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime )
    #
    if not areClose( iRateForNow, iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() UTC 4 hrs thru day 1, batches were regular' )
        #
    #
    iTotalLast24hrs   = iMaxPerDay * 2 / 24
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime )
    #
    if not areClose( iRateForNow, 1.1 * iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() UTC 4 hrs thru day 1, batches were short' )
        #
    #
    iTotalLast24hrs   = iMaxPerDay * 6 / 24
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime )
    #
    if not areClose( iRateForNow, 0.9 * iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() UTC 4 hrs thru day 1, batches were long' )
        #
    #
    sFirstRequestTime = getNowPlus( iHours = -20, bWantLocal = False )
    #
    iTotalLast24hrs   = iMaxPerDay * 20 / 24
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime )
    #
    if not areClose( iRateForNow, iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() UTC 20 hrs thru day 1, batches were regular' )
        #
    #
    iTotalLast24hrs   = iMaxPerDay * 15 / 24
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime )
    #
    if not areClose( iRateForNow, 2 * iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() UTC 20 hrs thru day 1, batches were short' )
        #
    #
    iTotalLast24hrs   = iMaxPerDay * 22 / 24
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime )
    #
    if not areClose( iRateForNow, 0.5 * iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() UTC 20 hrs thru day 1, batches were long' )
        #
    #
    #
    # now use local times
    #
    #
    sFirstRequestTime = getNowPlus( iDays = -2, bWantLocal = True )
    #
    iTotalLast24hrs   = int( round( iMaxPerDay * 23.0 / 24 ) )
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime,
                    bWantLocal = True )
    #
    if not areClose( iRateForNow, int( round( iMaxPerDay / 24.0 ) ) ):
        #
        lProblems.append( 'getHourlyRateForNow() local, after one day, regular batches' )
        #
    #
    iTotalLast24hrs   = iMaxPerDay * 10 / 24
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime,
                    bWantLocal = True )
    #
    if not areClose( iRateForNow, 2 * iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() local, after one day, batches were short' )
        #
    #
    iTotalLast24hrs   = int( iMaxPerDay * 23.5 / 24 )
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime,
                    bWantLocal = True )
    #
    if not areClose( iRateForNow, 0.5 * iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() local, after one day, batches were long' )
        #
    #
    iTotalLast24hrs   = int( iMaxPerDay * 21 / 24 )
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime,
                    bWantLocal = True )
    #
    if not areClose( iRateForNow, 1.67 * iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() local, after one day, batches were a little short' )
        #
    #
    sFirstRequestTime = getNowPlus( iHours = -12, bWantLocal = True )
    #
    iTotalLast24hrs   = iMaxPerDay * 12 / 24
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime,
                    bWantLocal = True )
    #
    if not areClose( iRateForNow, iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() local, half way thru day 1, batches were regular' )
        #
    #
    iTotalLast24hrs   = iMaxPerDay * 6 / 24
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime,
                    bWantLocal = True )
    #
    if not areClose( iRateForNow, 1.5 * iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() local, half way thru day 1, batches were short' )
        #
    #
    iTotalLast24hrs   = iMaxPerDay * 15 / 24
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime,
                    bWantLocal = True )
    #
    if not areClose( iRateForNow, 0.75 * iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() local, half way thru day 1, batches were long' )
        #
    #
    sFirstRequestTime = getNowPlus( iHours = -4, bWantLocal = True )
    #
    iTotalLast24hrs   = iMaxPerDay * 4 / 24
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime,
                    bWantLocal = True )
    #
    if not areClose( iRateForNow, iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() local, 4 hrs thru day 1, batches were regular' )
        #
    #
    iTotalLast24hrs   = iMaxPerDay * 2 / 24
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime,
                    bWantLocal = True )
    #
    if not areClose( iRateForNow, 1.1 * iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() local, 4 hrs thru day 1, batches were short' )
        #
    #
    iTotalLast24hrs   = iMaxPerDay * 6 / 24
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime,
                    bWantLocal = True )
    #
    if not areClose( iRateForNow, 0.9 * iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() local, 4 hrs thru day 1, batches were long' )
        #
    #
    sFirstRequestTime = getNowPlus( iHours = -20, bWantLocal = False )
    #
    iTotalLast24hrs   = iMaxPerDay * 20 / 24
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime,
                    bWantLocal = False )
    #
    if not areClose( iRateForNow, iMaxPerDay / 24 ):
        #
        print3( 'iRateForNow    :', iRateForNow     )
        print3( 'iMaxPerDay / 24:', iMaxPerDay / 24 )
        lProblems.append( 'getHourlyRateForNow() local, 20 hrs thru day 1, batches were regular' )
        #
    #
    iTotalLast24hrs   = iMaxPerDay * 15 / 24
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime,
                    bWantLocal = False )
    #
    if not areClose( iRateForNow, 2 * iMaxPerDay / 24 ):
        #
        print3( 'iRateForNow       :',     iRateForNow     )
        print3( '2* iMaxPerDay / 24:', 2 * iMaxPerDay / 24 )
        lProblems.append( 'getHourlyRateForNow() local, 20 hrs thru day 1, batches were short' )
        #
    #
    iTotalLast24hrs   = iMaxPerDay * 22 / 24
    #
    iRateForNow = getHourlyRateForNow(
                    iMaxPerDay, iTotalLast24hrs, sFirstRequestTime,
                    bWantLocal = False )
    #
    if not areClose( iRateForNow, 0.5 * iMaxPerDay / 24 ):
        #
        lProblems.append( 'getHourlyRateForNow() local, 20 hrs thru day 1, batches were long' )
        #
    #
    sayTestResult( lProblems )