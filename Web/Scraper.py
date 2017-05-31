#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions Scraper web scrapers
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
# Copyright 2010-2016 Rick Graves
#
# example applications in sMail.GetInfo
#
from os.path        import join
from time           import time

from six            import print_ as print3

from Dir.Get        import sTempDir
from String.Test    import getHasSubstrTester
from Object.Get     import SequencerClass
from Utils.Get      import getTrue

oSequencer = SequencerClass()

isRetryConnect = getHasSubstrTester( '(Internal Server Error|Connection refused|Proxy Error)' )
#
class ScraperClass( object ):
    #
    def __init__( self, oSequencer, sLogFile = None ):
        #
        self.Sequencer = oSequencer
        #
        self.fPriorCall  =  0
        self.iWantWait   =  5
        self.bWantLog    =  False
        self.iSequence   = -1
        self.bGetCookie  =  False
        self.sLogFile    = sLogFile
        #
        self.lDurations  = []
    #
    def getWait( self ):
        #
        fSince = time() - self.fPriorCall
        #
        if fSince > self.iWantWait:
            #
            fWait   = 0
            #
        else:
            #
            fWait   = self.iWantWait - fSince
            #
        return fWait


    def _delayMaybe( self, iMore = 0 ):
        #
        from time import sleep
        #
        if self.Sequencer is not None:
            #
            self.iSequence = self.Sequencer.getNextInSeq()
        #
        fSince = time() - self.fPriorCall
        #
        if fSince <= iMore + self.iWantWait - 1:
            #
            fSnooze = iMore + self.iWantWait - fSince
            #print3( 'will snooze for %5.2f seconds ...' % fSnooze )
            sleep( fSnooze )

    def _writeResults( self, sHTML ):
        #
        from File.Write     import WriteText2File
        from Time.Output    import getNowIsoDateTimeFileNameSafe
        #
        t = ( self.__class__.__name__, getNowIsoDateTimeFileNameSafe() )
        #
        sOutFile = join( sTempDir, '%s_%s.html' % t )
        #
        WriteText2File( sHTML, sOutFile )
        #
        return sOutFile

    def _appendDuration( self, fDuration, fEnd ):
        #
        # keeping last 20 requests
        #
        self.lDurations.append( ( fDuration, fEnd ) )
        #
        while len( self.lDurations ) > 20:
            #
            del self.lDurations[0]
            #

    def getAvgDuration( self ):
        #
        from bisect import bisect_left
        #
        from Numb.Get import getSumOffList
        #
        fAvg = 0
        #
        fNow = time()
        #
        while self.lDurations and fNow - self.lDurations[0][1] > 3600:
            #
            # delete if more than one hour old
            #
            del self.lDurations[0]
            #
        if self.lDurations:
            #
            # only consider last 10 minutes
            #
            fAvg = 0
            #
            lEndTimes = [ t[1] for t in self.lDurations ]
            #
            iNotTooOld = bisect_left( lEndTimes, time() - 600 )
            #
            lNotTooOld = self.lDurations[ iNotTooOld : ]
            #
            if lNotTooOld:
                #
                fTotal = getSumOffList( [ t[0] for t in lNotTooOld ] )
                #
                fAvg = fTotal / len( lNotTooOld )
        #
        return fAvg

    def getWaitAddAvgDuration( self ):
        #
        from Numb.Get import getFloatHalfRound
        #
        return '%04.1f' % round(
            (   self.getWait() +
                getFloatHalfRound( self.getAvgDuration() ) ), 2 )

    def getWaitDurationAndSeq( self ):
        #
        return ( self.getWaitAddAvgDuration(), self.iSequence )

    def doLog( self, sLine, sLogFile = None ):
        #
        from File.Write     import openAppendClose
        from Time.Output    import getNowIsoDateTimeStr
        #
        if self.bWantLog:
            #
            if sLogFile is None: sLogFile = self.__class__.__name__
            #
            sFileName = join( sTempDir, '%s.log' % sLogFile )
            #
            sNow = getNowIsoDateTimeStr()
            #
            sLine = '%s %s' % ( sNow, sLine )
            #
            openAppendClose( sLine, sFileName )

    def isRetryResult( self, sHTML ):
        #
        from String.Test import hasSubstring
        #
        bRetry = False
        #
        if      len( sHTML ) < 100 and isRetryConnect( sHTML ):
            #
            bRetry = True
            #
        if sHTML == 'opener object got wiped':
            #
            bRetry = True
            #
        if          hasSubstring( sHTML, '<!DOCTYPE HTML ' ) and \
                not hasSubstring( sHTML, '</body>'):
            #
            bRetry = True
            #
        #
        return bRetry


class PosterScraperClass( ScraperClass ):
    #
    def __init__( self, oSequencer, sLogFile = None ):
        #
        super( PosterScraperClass, self ).__init__( oSequencer, sLogFile = sLogFile )
        #
        self.bWantLog = True

    #
    def _getHTML( self, **dPostData ):
        #
        from Time.Output    import getNowIsoDateTimeStr
        from Web.Get        import getPostResults
        #
        self._delayMaybe()
        #
        if self.sLogFile:
            #
            sLine = 'starting getPostResults() in %s' % self.__class__.__name__
            #
            sNow = getNowIsoDateTimeStr()
            #
            sLine = '%s %s' % ( sNow, sLine )
            #
            self.doLog( sLine, sLogFile = self.sLogFile )
            #
        fStart = time()
        #
        iTry = 0
        #
        while iTry < 3:
            #
            iTry += 1
            #
            sHTML = getPostResults(
                self.sURL,
                dPostData,
                sReferer   = self.sReferer,
                bGetCookie = self.bGetCookie )
                #
            if not self.isRetryResult( sHTML ):
                #
                break
                #
            #
        #
        fEnd = time()
        #
        if self.sLogFile:
            #
            sLine = 'ended    getPostResults() in %s' % self.__class__.__name__
            #
            sNow = getNowIsoDateTimeStr()
            #
            sLine = '%s %s' % ( sNow, sLine )
            #
            self.doLog( sLine, sLogFile = self.sLogFile )
            #
        self.fPriorCall = fEnd
        #
        fDuration = fEnd - fStart
        #
        self._appendDuration( fDuration, fEnd )
        #
        return sHTML


class getterScraperClass( ScraperClass ):
    #
    def __init__( self, oSequencer, sLogFile = None ):
        #
        super( getterScraperClass, self ).__init__( oSequencer, sLogFile = sLogFile )
        #
        self.bWantLog = True

    #
    def _getHTML( self, **dParams ):
        #
        from Time.Output    import getNowIsoDateTimeStr
        from Web.Get        import getGetPageHtml
        #
        self._delayMaybe()
        #
        fStart = time()
        #
        if self.sLogFile:
            #
            sLine = 'starting getPostResults() in %s' % self.__class__.__name__
            #
            sNow = getNowIsoDateTimeStr()
            #
            sLine = '%s %s' % ( sNow, sLine )
            #
            self.doLog( sLine, sLogFile = self.sLogFile )
            #
        iTry = 0
        #
        while iTry < 3:
            #
            iTry += 1
            #
            sHTML = getGetPageHtml(
                self.sURL,
                dParams,
                sReferer   = self.sReferer,
                bGetCookie = self.bGetCookie )
            #
            if not self.isRetryResult( sHTML ):
                #
                break
                #
            #
        #
        fEnd = time()
        #
        if self.sLogFile:
            #
            sLine = 'ended    getPostResults() in %s' % self.__class__.__name__
            #
            sNow = getNowIsoDateTimeStr()
            #
            sLine = '%s %s' % ( sNow, sLine )
            #
            self.doLog( sLine, sLogFile = self.sLogFile )
            #
        self.fPriorCall = fEnd
        #
        fDuration = fEnd - fStart
        #
        self._appendDuration( fDuration, fEnd )
        #
        return sHTML


def getWaitDurationsQuickerOnTop( l ):
    #
    from Iter.AllVers import iRange
    #
    lWaitDurations = []
    #
    for i in iRange( len( l ) ):
        #
        o = l[i]
        #
        sWaitDuration = str( o.getWaitDurationAndSeq() )
        #
        lWaitDurations.append( ( sWaitDuration, i ) )
        #
    #
    lWaitDurations.sort()
    #
    return lWaitDurations


def getFastest( lScraperObjs, fFilter = getTrue ):
    #
    from Iter.AllVers import tFilter
    #
    oFastest = None
    #
    lWaitDurations = \
        getWaitDurationsQuickerOnTop(
            tFilter( fFilter, lScraperObjs ) )
    #
    if lWaitDurations:
        #
        iIndex = lWaitDurations[ 0 ][ 1 ]
        #
        oFastest = lScraperObjs[ iIndex ]
        #
    #
    return oFastest


if __name__ == "__main__":
    #
    print3( 'this takes a while because the must be a pause between requests ...' )
    #
    from random import random, shuffle
    from time   import sleep
    #
    from Iter.AllVers   import iRange
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    getInfo             = ScraperClass( oSequencer )
    #
    if getInfo.getWait() != 0:
        #
        lProblems.append( 'getInfo.getWait() wait should be zero' )
        #
    #
    getInfo.__class__.fPriorCall = time()
    #
    sleep( 2 )
    #
    iMustWait = getInfo.getWait()
    #
    if 2 > iMustWait > 4:
        #
        lProblems.append( 'getInfo.getWait() got wait of %s' % iMustWait )
        #
    #
    lScrapers = []
    #
    for i in iRange(10):
        #
        o = ScraperClass( oSequencer )
        #
        o._delayMaybe() # calls sequencer
        #
        fEnd = time()
        #
        for j in iRange(5):
            #
            o._appendDuration( ( 2 * random() ), ( fEnd - j ) )
        #
        lScrapers.append( o )

    #
    shuffle( lScrapers ) # makes the index different from the sequence
    #
    lTuples = getWaitDurationsQuickerOnTop( lScrapers )
    #
    lStrings = [ str( t ) for t in lTuples ]
    #
    print3( '\n'.join( lStrings ) )
    #
    oFastest = getFastest( lScrapers )
    #
    if not oFastest is lScrapers[ lTuples[0][1] ]:
        #
        lProblems.append( 'getFastest()' )
        #
    #
    sayTestResult( lProblems )