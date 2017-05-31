#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# time functions ebayEndTime
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
'''
convert ebay's time left to the local time

you do not need to quote time left

accepts these time left formats and others

"5d 09h 18m", "4 days 9 hours", "09h 18m", "9 hours 12 mins"
'''
#

def _eatFrontS( sTime ):
    #
    if sTime.startswith( 's ' ):
        #
        sTime = sTime[ 1 : ]
        #
    #
    return sTime.strip()



def _getDurations( sTimeLeft, sUnitLong, sUnitShort ):
    #
    from String.Get     import getTextBeforeC, getTextAfterC
    #
    sTimeLeft = sTimeLeft.replace( '(', '' ).replace( ')', '' )
    #
    sLongs  = getTextBeforeC( sTimeLeft, sUnitLong  ).strip()
    sRest   = getTextAfterC(  sTimeLeft, sUnitLong  )
    #
    sRest   = _eatFrontS( sRest )
    #
    sShorts = getTextBeforeC( sRest,     sUnitShort )
    #
    sShorts = _eatFrontS( sShorts )
    #
    iLongs  = int( sLongs  )
    #
    iShorts = int( sShorts )
    #
    return iLongs, iShorts




def getIsoDateTimeOffEbayTimeLeft( sTimeLeft, bSayDOW = True, sNow = None ):
    #
    """
    ebay gives time left as "1d 09h 18m" or "4 days 9 hours".
    This does the time arithmetic in the local time zone.
    This could be made more robust by accepting more day/hour/minute strings.
    """
    #
    from Time.Output    import getNowIsoDateTimeStr, getTextDowOffIntDow
    from Time.Date      import getDOWfromISO
    from Time.Delta     import getIsoDateTimeNowPlus, getIsoDateTimeFromIsoDateTimePlus
    #
    iDays, iHours, iMins = 0, 0, 0
    #
    if 'day' in sTimeLeft:
        #
        iDays, iHours   = _getDurations( sTimeLeft, 'day', 'hour' )
        #
    elif 'hour' in sTimeLeft:
        #
        iHours, iMins   = _getDurations( sTimeLeft, 'hour', 'min' )
        #
    else:
        #
        lTimeLeft       = sTimeLeft.split()
        #
        for sTimePart in lTimeLeft:
            #
            try:
                #
                iUnits  = int( sTimePart[ : -1 ] )
                #
                if   sTimePart.endswith( 'd' ): iDays   = iUnits
                elif sTimePart.endswith( 'h' ): iHours  = iUnits
                elif sTimePart.endswith( 'm' ): iMins   = iUnits
                #
            except:
                #
                pass
                #
            #
        #
    #
    if sNow is None:
        sEndDateTime    = getIsoDateTimeNowPlus(                   iDays, iHours, iMins )
    else:
        sEndDateTime    = getIsoDateTimeFromIsoDateTimePlus( sNow, iDays, iHours, iMins )
    #
    #
    if bSayDOW:
        #
        iDOW        = getDOWfromISO( sEndDateTime )
        #
        sDOW        = getTextDowOffIntDow( iDOW )
        #
        sEndDateTime= '%s, %s' % ( sDOW, sEndDateTime )
        #
    #
    return sEndDateTime






if __name__ == "__main__":
    #
    from sys     import argv
    #
    from six     import print_ as print3
    #
    args = argv[ 1 : ]
    #
    if args:
        print3( getIsoDateTimeOffEbayTimeLeft( ' '.join( args )  ) )
    else:
        #
        print3( 'Usage: EbayEndTime {time left}' )
