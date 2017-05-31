#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Utility Progress text progress meter
#
#   This library is free software; you can redistribute it and/or
#   modify it under the terms of the GNU Lesser General Public
#   License as published by the Free Software Foundation; either
#   version 2.1 of the License, or (at your option) any later version.
#
#   This library is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public
#   License along with this library; if not, write to the
#      Free Software Foundation, Inc.,
#      59 Temple Place, Suite 330,
#      Boston, MA  02111-1307  USA
#
# This program was inspired by progress.py,
# a part of urlgrabber, a high-level cross-protocol url-grabber
# urlgrabber is Copyright 2002-2004 Michael D. Stenner, Ryan Tomayko
#
# Copyright 2008-2017 Rick Graves
#
#

from sys             import stderr
from time            import time
from math            import log
#
from String.Output   import ReadableNo


class DummyMeter( object ):
    #
    def __init__(self, fo=stderr, use_hours=0, use_days=0):
        #
        pass
        #
    def start(self, iSize=None, sOnLeft=None, sLineB4 = None ):
        #
        pass
        #
    def update(self, iDone, fNow=None):
        #
        pass
        #
    def end(self, iDone, fNow=None):
        #
        pass
        #


class BaseMeter( object ):
    def __init__(self):
        self.fUpdatePeriod  = 1.0 # seconds
        self.sOnLeft        = None
        self.iSize          = None
        self.fStartTime     = None
        self.iLastDone      = 0
        self.fLastUpdate    = 0
        self.re = RateEstimator()

    def start(self, iSize=None, sOnLeft=None, sLineB4 = None ):
        self.sOnLeft        = sOnLeft
        #iSize = None #########  TESTING
        self.iSize          = iSize
        fNow                = time() # returns a float
        self.fStartTime     = fNow
        self.re.start(iSize, fNow)
        self.iLastDone      = 0
        if sLineB4:         self.fo.write( sLineB4 + '\n' )
        self._do_start(fNow)
        self.update( 0, fNow )

    def _do_start(self, fNow=None):
        pass

    def update(self, iDone, fNow=None):
        # for a real gui, you probably want to override and put a call
        # to your mainloop iteration function here
        if fNow is None: fNow = time() # returns a float
        if (fNow >= self.fLastUpdate + self.fUpdatePeriod) or \
               not self.fLastUpdate:
            self.re.update(iDone, fNow)
            self.iLastDone      = iDone
            self.fLastUpdate    = fNow
            self._do_update(iDone, fNow)

    def _do_update(self, iDone, fNow=None):
        pass

    def end(self, iDone, fNow=None):
        if fNow is None: fNow = time() # returns a float
        self.re.update(iDone, fNow)
        self.iLastDone      = iDone
        self.fLastUpdate    = fNow
        self._do_end(iDone, fNow)

    def _do_end(self, iDone, fNow=None):
        pass



class TextMeter(BaseMeter):
    def __init__(self, fo=stderr, use_hours=0, use_days=0):
        BaseMeter.__init__(self)
        self.fo         = fo
        self.sOutFormat = '\r%-26.26s %3i%% |%-25.25s|'
        sMoreFormat =  ' %7s %8s'
        if use_days:
            self.sOutFormat = '\r%-18.18s %3i%% |%-25.25s|'
            sMoreFormat = ' %7s %16s'
        self.sOutFormat +=sMoreFormat
        self.use_hours  = use_hours
        self.use_days   = use_days
        fTime           = time() # returns a float

    def _do_update(self, iDone, fNow=None):
        etime = self.re.elapsed_time()
        fetime = format_time(etime, self.use_hours, self.use_days)
        fread = ReadableNo(iDone)
        #self.iSize = None
        sOnLeft = self.sOnLeft
        if self.iSize is None:
            out = '\r%-60.60s    %8s %s ' % \
                  (sOnLeft, fread, fetime)
        else:
            rtime = self.re.remaining_time()
            frtime = format_time(rtime, self.use_hours, self.use_days)
            frac = self.re.fraction_read()
            bar = '='*int(25 * frac)

            out = self.sOutFormat % \
                  ( sOnLeft, frac*100, bar, fread, frtime )

        self.fo.write(out)
        self.fo.flush()

    def _do_end(self, iDone, fNow=None):
        total_time = format_time(
                self.re.elapsed_time(), self.use_hours, self.use_days)
        iSizeFinal = ReadableNo(iDone)
        sOnLeft = self.sOnLeft
        if self.iSize is None:
            out = '\r%-60.60s    %8s %s ' % \
                  (sOnLeft, iSizeFinal, total_time)
        else:
            bar = '='*25
            out = self.sOutFormat  % \
                  ( sOnLeft, 100, bar, iSizeFinal, total_time )
        self.fo.write(out + '\n' )
        self.fo.flush()



######################################################################
# support classes and functions

class RateEstimator:
    def __init__(self, timescale=5.0):
        self.timescale = timescale

    def start(self, total=None, fNow=None):
        if fNow is None: fNow = time() # returns a float
        self.total = total
        self.fStartTime = fNow
        self.iLastDone      = 0
        self.ave_rate = None

    def update(self, iDone, fNow=None):
        if fNow is None: fNow = time() # returns a float
        if iDone == 0:
            # if we just started this file, all bets are off
            self.fLastUpdate = fNow
            self.iLastDone      = 0
            self.ave_rate = None
            return

        #print3( 'times', fNow, self.fLastUpdate )
        time_diff = fNow         - self.fLastUpdate
        read_diff = iDone - self.iLastDone
        self.fLastUpdate = fNow
        self.iLastDone = iDone
        self.ave_rate = self._GetRollingAverage(\
            time_diff, read_diff, self.ave_rate, self.timescale)
        #print3( 'results', time_diff, read_diff, self.ave_rate )

    #####################################################################
    # result meth0ds
    def average_rate(self):
        "get the average transfer rate (in bytes/second)"
        return self.ave_rate

    def elapsed_time(self):
        "the time between the start of the transfer and the most recent update"
        return self.fLastUpdate - self.fStartTime

    def remaining_time(self):
        "estimated time remaining"
        if not self.ave_rate or not self.total: return None
        return (self.total - self.iLastDone) / self.ave_rate

    def fraction_read(self):
        """the fraction of the data that has been read
        (can be None for unknown transfer iSize)"""
        if self.total is None: return None
        elif self.total == 0: return 1.0
        else: return float(self.iLastDone)/self.total

    #########################################################################
    # support meth0ds
    def _GetRollingAverage(self, time_diff, read_diff, last_ave, timescale):
        """a temporal rolling average performs smooth averaging even when
        updates come at irregular intervals.  This is performed by scaling
        the "epsilon" according to the time since the last update.
        Specifically, epsilon = time_diff / timescale

        As a general rule, the average will take on a completely new value
        after 'timescale' seconds."""
        epsilon = time_diff / timescale
        if epsilon > 1: epsilon = 1.0
        return self._rolling_ave(time_diff, read_diff, last_ave, epsilon)

    def _rolling_ave(self, time_diff, read_diff, last_ave, epsilon):
        """perform a "rolling average" iteration
        a rolling average "folds" new data into an existing average with
        some weight, epsilon.  epsilon must be between 0.0 and 1.0 (inclusive)
        a value of 0.0 means only the old value (initial value) counts,
        and a value of 1.0 means only the newest value is considered."""

        try:
            recent_rate = read_diff / time_diff
        except ZeroDivisionError:
            recent_rate = None
        if last_ave is None: return recent_rate
        elif recent_rate is None: return last_ave

        # at this point, both last_ave and recent_rate are numbers
        return epsilon * recent_rate  +  (1 - epsilon) * last_ave

    def _round_remaining_time(self, rt, fStartTime=15.0):
        """round the remaining time, depending on its iSize
        If rt is between n*fStartTime and (n+1)*fStartTime round downward
        to the nearest multiple of n (for any counting number n).
        If rt < fStartTime, round down to the nearest 1.
        For example (for fStartTime = 15.0):
         2.7  -> 2.0
         25.2 -> 25.0
         26.4 -> 26.0
         35.3 -> 34.0
         63.6 -> 60.0
        """

        if rt < 0: return 0.0
        shift = log( rt/fStartTime ) // math.log(2)
        rt = int(rt)
        if shift <= 0: return rt
        return float(int(rt) >> shift << shift)


def format_time(seconds, use_hours=0, use_days=0):
    if seconds is None or seconds < 0:
        if use_days:  return '-- days --:--:--'
        if use_hours: return '--:--:--'
        else:         return '--:--'
    else:
        seconds = int(seconds)
        minutes = seconds // 60
        seconds = seconds % 60
        if use_hours or use_days:
            hours   = minutes // 60
            minutes = minutes % 60
        if use_days:
            days    = hours // 24
            hours   = hours % 24
            # if minutes > 30: hours += 1
        if use_days:
            return '%2i days %02i:%02i:%02i' % (days, hours, minutes, seconds)
        elif use_hours:
            return '%02i:%02i:%02i' % (hours, minutes, seconds)
        else:
            return '%02i:%02i' % (minutes, seconds)



if __name__ == "__main__":
    #
    from sys            import stdout
    from time           import sleep
    #
    from Iter.AllVers   import iRange
    #
    oProgressMeter  = DummyMeter()
    #
    if stdout.isatty():
        #
        oProgressMeter = TextMeter()
        #
    #
    iSeq    = 0
    iLen    = 100
    #
    sLineB4 = 'passing the time ...'
    sOnLeft = "%s %s" % ( ReadableNo( iLen ), 'fast ticks' )
    #
    oProgressMeter.start( iLen , sOnLeft, sLineB4 )
    #
    for iThis in iRange( iLen - 1 ):
        #
        sleep( 0.1 )
        #
        iSeq  += 1
        #
        oProgressMeter.update( iSeq )
        #
        #
        #
    #
    oProgressMeter.end( iLen )
    #
    sleep( 1 )
    # use_hours=0, use_days=
    #
    oProgressMeter  = DummyMeter( use_hours = True )
    #
    if stdout.isatty():
        #
        oProgressMeter = TextMeter( use_hours = True )
        #
    #
    iSeq            = 0
    iLen            = 18005
    #
    sOnLeft       = "%s %s" % ( ReadableNo( iLen ), 'slow ticks' )
    #
    oProgressMeter.start( iLen , sOnLeft, sLineB4 )
    #
    for iThis in iRange( iLen - 1 ):
        #
        sleep( 1 )
        #
        iSeq  += 1
        #
        oProgressMeter.update( iSeq )
        #
        if iThis > 10:
            break
        #
    #
    oProgressMeter.end( iLen )
    #
    sleep( 1 )
    #
    oProgressMeter  = DummyMeter( use_days = True )
    #
    if stdout.isatty():
        #
        oProgressMeter = TextMeter( use_days = True )
        #
    #
    iSeq            = 0
    iLen            = 172815
    #
    sOnLeft       = "%s %s" % ( ReadableNo( iLen ), 'slow ticks' )
    #
    oProgressMeter.start( iLen , sOnLeft, sLineB4 )
    #
    for iThis in iRange( iLen - 1 ):
        #
        sleep( 1 )
        #
        iSeq  += 1
        #
        oProgressMeter.update( iSeq )
        #
        if iThis > 20:
            break
        #
    #
    oProgressMeter.end( iLen )
    #
