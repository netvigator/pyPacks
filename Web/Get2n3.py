#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions Get2n3 python 2 and 3 compatible
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
# Copyright 2004-2017 Rick Graves
#
# self test needs internet connection and will access python.org

from socket                     import error as SocketError
from sys                        import exc_info

from six                        import print_ as print3
from six.moves.urllib.error     import URLError
from six.moves.urllib           import request as Request
from six.moves.urllib.request   import urlopen

from Dir.Get        import sTempDir
from Utils.Config   import getConfDict
#from Utils.Both2n3 import URLError

dConf   = getConfDict( 'Get2n3.conf' )


#def getBytes( s, encoding = getdefaultencoding() ): return s

'''
to self test without any internet connection,
pass params "no internet" (without the quotes)
'''

class getPage( object ):
    #
    def __init__( self,
            bUseCookie  = True,
            sFileDir    = sTempDir,
            sUserAgent  = 'default',
            bAcceptGzip = False,
            iSecsPause  = 0,
            **kwargs ):
        #
        if sUserAgent == 'default':
            #
            sUserAgent = dConf.get( 'main' ).get( 'user-agent' )
        #
        self.bUseCookie     = bUseCookie
        self.sCookieFileSpec= ''
        self.oCookieJar     = None
        self.sFileDir       = sFileDir
        self.sUserAgent     = sUserAgent
        self.bAcceptGzip    = bAcceptGzip
        self.iSecsPause     = iSecsPause

        self.iRecentRequest = 0

        
    def getHtml( self, sURL ):
        #
        sHTML, oHeaders, dResult = self.getHtmlAndResults( sURL )
        #
        return sHTML


    def getCookieOffHomePage( self, sURL ):
        #
        from Web.Address import getUrlDropPathQuery
        #
        sHome = getUrlDropPathQuery( sURL )
        #
        sHTML, oHeaders, dResult = self.getHtmlAndResults( sHome )
        #
        sReturn = 'OK'
        #
        if dResult['sComment']:
            #
            sReturn = '%(sComment)s, %(sErrorCode)s, %(sReason)s' % dResult
            #
        #
        return sReturn


    def getHtmlAndResults( self, sURL ):
        #
        from time           import time, sleep
        #
        from String.Get     import getUnGzippedOrContent
       #from Utils.Both2n3  import Request, urlopen
        #
        oRequest = Request( sURL )
        #
        if self.sUserAgent:
            #
            oRequest.add_header( "User-Agent", self.sUserAgent )
        #
        if self.bAcceptGzip:
            #
            oRequest.add_header( "Accept-Encoding", 'gzip' )
        #
        oCookieJar = self._getCookieJar( sURL )
        #
        self._addCookie( oCookieJar, oRequest )
        #
        sHTML = ''
        #
        oReceiveHeaders     = None
        sRealURL            = sURL
        sReason = sErrorCode = sComment = ''
        #
        iNow = self.iSecsPause and time() # fetch time() if iSecsPause > 0
        #
        if (    self.iSecsPause and
                self.iRecentRequest and
                self.iRecentRequest + self.iSecsPause - iNow > 0 ):
            #
            sleep( self.iRecentRequest + self.iSecsPause - iNow )
            #
        #
        self.iRecentRequest = time()
        #
        try:
            #
            oPage = urlopen( oRequest )
            #
        except URLError:
            #
            error, msg, traceback = exc_info()
            #
            if hasattr(msg, 'reason'):
                sComment    = 'We failed to reach the server.'
                sReason     = msg.reason
            elif hasattr(msg, 'code'):
                sComment    = 'The server couldn\'t fulfill the request.'
                sErrorCode  = str( msg.code )
            #
        except SocketError:
            #
            error, msg, traceback = exc_info()
            #
            sComment        = 'We hit a socket error on open.'
            sReason         = str( msg )
            #
        except Exception:
            #
            error, msg, traceback = exc_info()
            #
            sComment        = 'We hit some unknown error.'
            sReason         = str( msg )
            #
        else:
            #
            try:
                #
                self._getOneCookie( oCookieJar, oPage, oRequest )
                sHTML           = oPage.read()
                oReceiveHeaders = oPage.info()
                oPage.close()
                self._saveCookie()
                #
            except (ValueError, SocketError):
                #
                error, msg, traceback = exc_info()
                sComment        = 'We hit a socket error on read.'
                sReason         = str( msg )
        #
        dResult = dict(
                    sReason     = sReason,
                    sErrorCode  = sErrorCode,
                    sComment    = sComment,
                    sRealURL    = sRealURL )
        #
        if self.bAcceptGzip and sHTML:
            #
            sHTML = getUnGzippedOrContent( sHTML )
        #
        return sHTML, oReceiveHeaders, dResult


    def _getCookieJar( self, sURL ):
        #
        from os.path        import join
        #
        from Utils.Both2n3  import FileCookieJar
        #
        oCookieJar = self.oCookieJar
        #
        sCookieFileName = self._getCookieFileName( sURL )
        #
        sCookieFileSpec = join( self.sFileDir, sCookieFileName )
        #
        if self.bUseCookie and (
                self.oCookieJar is None or
                sCookieFileSpec != self.sCookieFileSpec ):
            #
            oCookieJar = FileCookieJar()
            #
            try:
                oCookieJar.load( sCookieFileSpec )
            except Exception:
                pass
            #
            self.oCookieJar     = oCookieJar
            self.sCookieFileSpec  = sCookieFileSpec
            #
        #
        return oCookieJar


    def _addCookie( self, oCookieJar, oRequest ):
        #
        if self.bUseCookie:
            #
            oCookieJar.add_cookie_header( oRequest )


    def _getOneCookie( self, oCookieJar, oPage, oRequest ):
        #
        if self.bUseCookie:
            #
            oCookieJar.extract_cookies( oPage, oRequest )


    def _saveCookie( self ):
        #
        if self.bUseCookie and self.oCookieJar is not None:
            #
            self.oCookieJar.save( self.sCookieFileSpec )


    def _getCookieFileName( self, sURL ):
        #
        from Web.Address import getDomainOffURL
        #
        sBase = getDomainOffURL( sURL )
        #
        return '%s.cookie' % sBase


    def getParams( self, dParams ):
        #
        from six.moves.urllib.parse import quote_plus
        #
        from Dict.Get       import getItemIter
       #from Utils.Both2n3  import quote_plus
        #
        sParams = '&'.join( [ '%s=%s' %
            ( kv[0], quote_plus( kv[1] ) )
                for kv in getItemIter( dParams )
                if kv[1] ] )
        #
        return sParams




def getHtmlAndResults( sURL ):
    #
    oGetter = getPage(
                bUseCookie  = False,
                bAcceptGzip = True )
    #
    sHTML, oHeaders, dResult = oGetter.getHtmlAndResults( sURL )
    #
    return sHTML, oHeaders, dResult






class getPageForNoInternet( getPage ):
    #
    def __init__( self,
            bUseCookie  = True,
            sFileDir    = sTempDir,
            sUserAgent  = 'default',
            bAcceptGzip = False,
            iSecsPause  = 0,
            uFakeResp   = 100,
            **kwargs ):
        #
        self.uFakeResp = uFakeResp
        #
        super( getPageForNoInternet, self ).__init__(
                    bUseCookie  = bUseCookie,
                    sUserAgent  = sUserAgent,
                    bAcceptGzip = bAcceptGzip,
                    iSecsPause  = iSecsPause,
                    **kwargs )
        #
    def getHtmlAndResults( self, sURL ):
        #
        from copy   import deepcopy
        from time   import sleep, time
        #
        from Object.Get import Null
        #
        iNow = self.iSecsPause and time() # fetch time() if iSecsPause > 0
        #
        if self.iSecsPause:
            #
            if self.iRecentRequest:
                print3( 'iRecentRequest was %s seconds ago' %
                        round( iNow - self.iRecentRequest, 2 ) )
                print3( 'recent request plus pause is %s seconds from now' %
                        round( self.iRecentRequest + self.iSecsPause - iNow, 2 ) )
            else:
                print3( 'iRecentRequest not set yet' )
            
        if (    self.iSecsPause and
                self.iRecentRequest and
                self.iRecentRequest + self.iSecsPause - iNow > 0 ):
            #
            print3( 'will pause for %s seconds' %
                    round( self.iRecentRequest + self.iSecsPause - iNow, 2 ) )
            iStartPause = time()
            sleep( self.iRecentRequest + self.iSecsPause - iNow )
            print3( 'pause finished, pause duration was %s seconds' %
                    round( time() - iStartPause, 2 ) )
            #
        elif self.iRecentRequest:
            print3( 'no pause this time' )
            print3( 'iRecentRequest was %s seconds ago' %
                    round( iNow - self.iRecentRequest, 2 ) )
            print3( 'iRecentRequest + iSecsPause - iNow: %s' %
                    round( self.iRecentRequest + self.iSecsPause - iNow, 2 ) )

        #
        self.iRecentRequest = time()
        #
        sleep( 0.5 )
        #
        dResult = dict(
            sComment   = '',
            sErrorCode = '',
            sReason    = '' )
        #
        return deepcopy( self.uFakeResp ), Null(), dResult

    
if __name__ == "__main__":
    #
    from pprint         import pprint
    from string         import ascii_letters
    from sys            import argv
    #
    from six.moves.urllib.parse import unquote_plus
    #
    from Object.Get     import getDictOffObject
   #from Utils.Both2n3  import unquote_plus
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    args = argv[ 1 : ]
    #
    if 'no' in args and 'internet' in args:
        #
        oUsePageGetter = getPageForNoInternet
        #
    else:
        #
        oUsePageGetter = getPage
        #
    #
    sURL        = 'http://www.python.org/'
    #
    oGetter = oUsePageGetter()
    #
    sCookieFileName = oGetter._getCookieFileName( sURL )
    #
    if sCookieFileName != 'python.org.cookie':
        #
        lProblems.append( '_getCookieFileName() returned %s' % sCookieFileName )
        #
    #
    dParams = dict( 
        appid  = "PqueyE7k",
        addr   = "1231 N 48th St",
        city   = "Seattle",
        state  = "WA",
        postal = "98103",
        flags  = "J" )
    #
    sParams = oGetter.getParams( dParams )
    #
    lParams = [ s.split( '=' ) for s in sParams.split( '&' ) ]
    lParams = [ ( k, unquote_plus( v ) ) for (k,v) in lParams ]
    #
    if dict( lParams ) != dParams:
        #
        lProblems.append( 'getParams()' )
        pprint( dParams )
        pprint( dict( lParams ) )
        #
    #
    sFake = ' '.join( [ ascii_letters ] * ( 1 + ( 5000 / len( ascii_letters ) ) ) )
    #
    # ### fake is only used if "no internet" params are passed to self test ###
    #
    oGetter = oUsePageGetter( iSecsPause = 2, uFakeResp = sFake )
    #
    print3( '\n' )
    print3( 'http://www.python.org/' )
    sHTML, oHeaders, dResult = oGetter.getHtmlAndResults( 'http://www.python.org/' )
    #
    if len( sHTML ) < 5000:
        #
        print3( 'dResult:' )
        pprint( getDictOffObject( dResult  ) )
        #
        if oHeaders:
            print3( 'oHeaders:' )
            pprint( oHeaders )
        #
        lProblems.append( 'getHtmlAndResults() did not fetch the page' )
        #
    #
    print3( '\n' )
    print3( 'http://www.democratsabroad.org/' )
    sHTML, oHeaders, dResult = oGetter.getHtmlAndResults( 'http://www.democratsabroad.org/' )
    print3( '\n' )
    print3( 'http://www.powergrab.org/' )
    sHTML, oHeaders, dResult = oGetter.getHtmlAndResults( 'http://www.powergrab.org/' )
    print3( '\n' )
    print3( 'http://www.anonymitytest.com/' )
    sHTML, oHeaders, dResult = oGetter.getHtmlAndResults( 'http://www.anonymitytest.com/' )
    print3( '\n' )
    #
    sURL = ( 'http://www.google.com/search?q=athens+time+zone&hl=en&gbv=1'
        '&prmd=ivnsofd&ei=UR9PT5G8EKyyiQf2kcDbCw&sa=N&gs_sm=3'
        '&gs_upl=155378309l155378309l0l155378649l1l1l0l0l0l0l219l219l2-1l1l0'
        '&oq=athens+time+zone&aq=f&aqi=g1g-v6g-j1g-b2&aql=' )
    #
    oGetter = oUsePageGetter()
    #
    sResult = oGetter.getCookieOffHomePage( sURL )
    #
    if sResult != 'OK':
        #
        lProblems.append( 'getCookieOffHomePage() returned %s' % sResult )
        #
    #
    sayTestResult( lProblems )
    # self must access python.org and https://writerep.house.gov/