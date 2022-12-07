#!/home/rick/.local/bin/pythonTest
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
#   http://www.gnu.org/licenses/
#
# Copyright 2004-2023 Rick Graves
#
#
from time               import time

from six                import print_ as print3

try:
    from ..Iter.AllVers import iRange, tFilter
except ( ValueError, ImportError ):
    from Iter.AllVers   import iRange, tFilter


def _sayClockTimeCPU( tBefore, sSay ):
    tNow = clock()
    print3( '%s: %s' % ( sSay, tNow - tBefore ) )
    return tNow


def _callOverAndOver( iterCallsPerSet, TimeThis, args, kwargs ):
    #
    # each repetition has multiple calls
    #
    for iCall in iterCallsPerSet: TimeThis( *args, **kwargs )
    #


def _timer( iCallsPerSet, iSets, TimeThis, args, kwargs ):
    #
    # iCallsPerSet is the number of times the function is call on each repetition
    # to test consistency,
    #
    #
    iCallsPerSet    = int( iCallsPerSet )
    #
    iterCallsPerSet = iRange( iCallsPerSet )
    #
    lResults    = [ 0 ] * iSets
    #
    for iThisSet in iRange( iSets ):
        #
        tBeg    = time()
        #
        _callOverAndOver( iterCallsPerSet, TimeThis, args, kwargs )
        #
        tEnd    = time()
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


def _definedTrial( iCallsPerSet, iSets, TimeThis, args, kwargs ):
    #
    try: # moving this to the top breaks this package!
        from ..String.Output    import ReadableNo
        from ..Time.Delta   import getDurationUnits
    except ( ValueError, ImportError ): # maybe circular import issue
        from String.Output      import ReadableNo
        from Time.Delta     import getDurationUnits
    #
    lTimeList   = _timer( iCallsPerSet, iSets, TimeThis, args, kwargs )
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
        print3( 'per set (with', \
            ReadableNo( iCallsPerSet ), 'calls per set)' )
    else:
        print3( 'per set (only one call per set)' )
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



def TimeTrial( TimeThis, *args, **kwargs ):
    #
    """
    TimeTrial your programs.
    Pass your program as the first argument, the other arguments follow.
    timeit was new in 2.6, this works in all versions
    """
    #
    #
    bProceed            = True
    #
    iWantObjs           = 0
    #
    iCallsPerSet        = kwargs.pop( 'iCallsPerSet', None )
    iSets               = kwargs.pop( 'iSets',        None )
    #
    bClock1st           = False # use time as first timer
    #
    if iCallsPerSet is None or iSets is None:
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
        tBeg                = time()
        #
        TimeThis( *args, **kwargs )
        #
        tEnd                = time()
        #
        nDuration           = tEnd - tBeg # "time" duration
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
    _definedTrial( iCallsPerSet, iSets, TimeThis, args, kwargs )
    #
    return iCallsPerSet, iSets




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
    iCallsPerSet, iSets = TimeTrial( getSequencePairsThisWithNext, tNumbs )
    #
    from Iter.Get import getSequencePairsThisWithNext
    #
    print3( '\nusing Iter.Get.getSequencePairsThisWithNext ...' )
    #
    TimeTrial( getSequencePairsThisWithNext, tNumbs,
              iCallsPerSet=iCallsPerSet, iSets=iSets)
