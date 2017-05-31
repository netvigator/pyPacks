#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Utility functions TimeTrial
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
#
from six import print_ as print3

def _sayClockTimeCPU( tBefore, sSay ):
    from time import clock
    tNow = clock()
    print3( '%s: %s' % ( sSay, tNow - tBefore ) )
    return tNow



def _callOverAndOver( iterCallsPerSet, TimeThis, args, kwargs ):
    #
    # each repetition has multiple calls
    #
    for iCall in iterCallsPerSet: TimeThis( *args, **kwargs )
    #


def _timer( getNow, iCallsPerSet, iSets, TimeThis, args, kwargs ):
    #
    # iCallsPerSet is the number of times the function is call on each repetition
    # to test consistency,
    #
    from Iter.AllVers import iRange
    #
    iCallsPerSet    = int( iCallsPerSet )
    #
    iterCallsPerSet = iRange( iCallsPerSet )
    #
    lResults    = [ 0 ] * iSets
    #
    for iThisSet in iRange( iSets ):
        #
        tBeg    = getNow()
        #
        _callOverAndOver( iterCallsPerSet, TimeThis, args, kwargs )
        #
        tEnd    = getNow()
        #
        lResults[ iThisSet ] = tEnd - tBeg
        #
    #
    lResults.sort()
    #
    return lResults


def _getGoodInt( nOne2Ten ):
    #
    if   nOne2Ten < 1.6:
        #
        iGoodInt    = 1
        #
    elif nOne2Ten < 3.9:
        #
        iGoodInt    = 2
        #
    elif nOne2Ten < 7.9:
        #
        iGoodInt    = 5
        #
    else:
        #
        iGoodInt    = 10
        #

    return iGoodInt


def _definedTrial( getNow, iCallsPerSet, iSets, TimeThis, args, kwargs ):
    #
    from Iter.AllVers   import tFilter
    from String.Output  import ReadableNo
    from Time.Delta     import getDurationUnits
    #
    lTimeList   = _timer( getNow, iCallsPerSet, iSets, TimeThis, args, kwargs )
    #
    fCallsPerSet = float( iCallsPerSet )
    #
    nMaxTime    = max( lTimeList ) / fCallsPerSet
    #
    iMultiplyBy, sIncrements = getDurationUnits( nMaxTime )
    #
    iMultiplyBy = iMultiplyBy / fCallsPerSet
    #
    print3( sIncrements, end = ' ' )
    #
    if iCallsPerSet > 1:
        print3( 'per call (with', \
            ReadableNo( iCallsPerSet ), 'calls per repetition)' )
    else:
        print3( 'per call (only one call per repetition)' )
    #
    for nTime in lTimeList:
        #
        print3( "%5.2f" % (nTime * iMultiplyBy ), end = ' ' )
        #
    #
    tTimeList = tFilter( bool, lTimeList ) # if f > 0
    #
    if tTimeList: # len( lTimeList ) > 0
        #
        if max( tTimeList ) / min( tTimeList ) > 1.01:
            #
            print3( "\nthe max is bigger than the min by a factor of", \
                "%3.1f" % ( max( tTimeList ) / min( tTimeList ) ) )
    #




def _setClock( bUseClockNotTime = False ):
    #
    if bUseClockNotTime:
        #
        from time import clock as getNow
        #
    else:
        #
        from time import time as getNow
    #
    return getNow



def _sayClock( bUseClockNotTime ):
    #
    from Utils.ImIf import ImIf
    #
    return ImIf( bUseClockNotTime, 'clock', 'time' )




def TimeTrial( TimeThis, *args, **kwargs ):
    #
    """
    TimeTrial your programs.
    Pass your program as the first argument, the other arguments follow.
    timeit was new in 2.6, this works in all versions
    """
    #
    from Iter.AllVers   import iRange
    #
    bProceed            = True
    #
    iWantObjs           = 0
    #
    try:
        #
        TimeThis( *args, **kwargs )
        #
    except TypeError:
        #
        print3( "%s cannot unpack the params!" % TimeThis.__name__ )
        #
        return
        #
    #
    print3( 'working ...' )
    #
    # time the function using both clock and time
    #
    getNow              = _setClock( False ) # use time
    #
    tBeg                = getNow()
    #
    TimeThis( *args, **kwargs )
    #
    tEnd                = getNow()
    #
    nDuration           = tEnd - tBeg # "time" duration
    #
    getNow              = _setClock( True ) # use clock
    #
    tBeg                = getNow()
    #
    TimeThis( *args, **kwargs )
    #
    tEnd                = getNow()
    #
    bClock1st           = False # use time as first timer
    #
    if tEnd - tBeg > nDuration: # if "clock" gave a longer duration than "time"
        #
        nDuration       = tEnd - tBeg
        #
        bClock1st       = True # use "clock" as first timer
        #
    #
    getNow              = _setClock( bClock1st )
    #
    nTargetSecs         =   1.0 # shoot for completing the sets in one sec
    #
    iSets               =   10
    #
    nSecsPerRepetition  =   nTargetSecs  / iSets
    #
    iCallsPerSet        =   nSecsPerRepetition // nDuration
    #
    for iPower in iRange( 8, -1, -1 ): # 8 to 0
        #
        if iCallsPerSet >= 10**iPower:
            #
            iCallsPerSet = \
                _getGoodInt( iCallsPerSet // 10**iPower ) * 10**iPower
            #
            break
        #
    #
    if iCallsPerSet < 1: iCallsPerSet = 1
    #
    print3( "using", _sayClock( bClock1st ), "for a timer:" )
    _definedTrial( getNow, iCallsPerSet, iSets, TimeThis, args, kwargs )
    #
    print3( "\nusing", _sayClock( not bClock1st ), "for a timer:" )
    getNow = _setClock( not bClock1st )
    _definedTrial( getNow, iCallsPerSet, iSets, TimeThis, args, kwargs )
    print3( '\npython docs say clock is better for time trials (!?)' )




if __name__ == "__main__":
    #
    from Iter.AllVers import tRange
    #
    lProblems = []
    #
    tNumbs = tRange( 100 )
    #
    from Collect.Get import getSequencePairsThisWithNext
    #
    print3( '\nusing Collect.Get.getSequencePairsThisWithNext ...' )
    #
    TimeTrial( getSequencePairsThisWithNext, tNumbs )
    #
    from Iter.Get import getSequencePairsThisWithNext
    #
    print3( '\nusing Iter.Get.getSequencePairsThisWithNext ...' )
    #
    TimeTrial( getSequencePairsThisWithNext, tNumbs )