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

from Time.Convert import sFormatISOdateTime


class Finished( Exception ): pass


def isISOdatetime( sDateTime ):
    #
    # '2005-07-24 11:28:34'
    #
    from time import strptime
    #
    bGotStringDate      = False
    #
    try:
        #
        sDateTime      += ' ' # tests for string date
        #
        sDateTime       = sDateTime.strip()
        #
        if len( sDateTime ) != 19:
            #
            raise Finished
            #
        #
        tDate           = strptime( sDateTime, sFormatISOdateTime )
        #
        bGotStringDate = \
            (   tDate[1] <= 12 and
                tDate[2] <= 60 and
                tDate[3] <= 24 and
                tDate[4] <= 60 and
                tDate[5] <= 60      )
    #
    except: pass
    #
    return bGotStringDate



def isISOdate( sDate ):
    #
    # '2005-07-24 11:28:34'
    #
    try:
        #
        bISOdate = isISOdatetime( sDate + ' 11:28:34' )
        #
    except:
        #
        bISOdate = False
        #
    #
    return bISOdate



def areSecsClose( iTime1, iTime2, iDeltaOK = 61 ):
    #
    return abs( iTime1 - iTime2 ) <= iDeltaOK



def isDateSomewhere( sDate, sFormat ):
    #
    from Time.Convert import getSecsSinceEpochFromString
    #
    bSomeDate = False
    #
    lParts = sDate.split( '/' )
    #
    if len( lParts ) == 3:
        #
        lLens = [ len( s ) for s in lParts ]
        #
        if max( lLens ) <= 4 and 1 <= min( lLens ) <= 2:
            #
            try:
                #
                getSecsSinceEpochFromString( sDate, sFormat )
                #
                bSomeDate = True
                #
            except ValueError:
                #
                pass
                #
            except:
                #
                raise
                #
            #
        #
    #
    return bSomeDate
    
   
def isDateUSA( sDate ):
    #
    from Time.Convert import sFormatDateAm
    #
    return isDateSomewhere( sDate, sFormatDateAm )



def isDateTimeUSA( sDateTime ):
    #
    from Time.Convert import getDateTimeObjFromString, sFormatUSAdateTime
    #
    bDateTimeOK = True
    #
    try:
        #
        getDateTimeObjFromString( sDateTime, sFormatUSAdateTime )
        #
    except ValueError:
        #
        bDateTimeOK = False
        #
    #
    return bDateTimeOK



def isDateEuro( sDate ):
    #
    from Time.Convert import sFormatDateEu
    #
    return isDateSomewhere( sDate, sFormatDateEu )





if __name__ == "__main__":
    #
    from time import time
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if not isISOdatetime( '2008-04-17 14:28:28' ):
        #
        lProblems.append( 'isISOdatetime() passed real thing' )
        #
    #
    if isISOdatetime( '2008-04-17x14:28:28' ):
        #
        lProblems.append( 'isISOdatetime() passed fake' )
        #
    #
    if isISOdatetime( time() ):
        #
        lProblems.append( 'isISOdatetime() integer time' )
        #
    #
    if not isISOdate( '2008-04-17' ):
        #
        lProblems.append( 'isISOdate()' )
        #
    #
    iNow    = time()
    iBefore = iNow - 65.0
    iRecent = iNow - 5.0
    #
    if areSecsClose( iNow, iBefore ) or areSecsClose( iBefore, iNow ):
        #
        lProblems.append( 'areSecsClose() times not close' )
        #
    #
    if not ( areSecsClose( iNow, iRecent ) and
             areSecsClose( iRecent, iNow ) ):
        #
        lProblems.append( 'areSecsClose() close times' )
        #
    #
    s = '12/21/1951'
    #
    if not isDateUSA( s ):
        #
        lProblems.append( 'isDateUSA() dob' )
        #
    #
    if isDateEuro( s ):
        #
        lProblems.append( 'isDateEuro() USA style' )
        #
    #
    s = '22/1/1951'
    #
    if isDateUSA( s ):
        #
        lProblems.append( 'isDateUSA() euro style' )
        #
    #
    if not isDateEuro( s ):
        #
        lProblems.append( 'isDateEuro() euro style' )
        #
    #
    sDateTime = '01/26/2012 05:58:24 PM'
    #
    if not isDateTimeUSA( sDateTime ):
        #
        lProblems.append( 'isDateTimeUSA() %s' % sDateTime )
        #
    #
    sDateTime = '26/01/2012 17:58:24'
    #
    if isDateTimeUSA( sDateTime ):
        #
        lProblems.append( 'isDateTimeUSA() %s' % sDateTime )
        #
    #
    #
    sayTestResult( lProblems )
