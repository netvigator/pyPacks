#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions get
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
from six.moves.urllib.error     import HTTPError, URLError
from six.moves.urllib.request   import urlopen, build_opener, install_opener
from six.moves.urllib.parse     import urlencode
from six.moves.http_client      import BadStatusLine

#from Utils.Both2n3             import BadStatusLine, HTTPError, URLError


def _getPageHandle( sURL ):
    #
    """Gets page HTML, but with synchronous (blocking) operation.
    If cannot get page, returns None."""
    #
    #from Utils.Both2n3 import urlopen
    #
    try:
        #
        hPage   = urlopen( sURL )
        #
    except:
        #
        hPage   = None
        #
    #
    return hPage


def getPageUrlOffURL( sURL ):
    #
    """
    gets page URL, but with synchronous (blocking) operation.
    If cannot get page, returns None.
    """
    #
    hPage = _getPageHandle( sURL )
    #
    if hPage is None:
        #
        sURL   = None
        #
    else:
        #
        sURL   = hPage.geturl()
        #
        hPage.close()
        #
    #
    return sURL



def _getFrameText(
        sHTML, lFrameSpecs, sURL, dSendHeaders, sCookie, tProxy , oFindBeg, oFindEnd = None ):
    #
    from copy           import deepcopy
    #
    from Collect.Get    import getListFromNestedLists
    from Iter.AllVers   import lMap, iZip
    from String.Get     import getTextAfter
    from Web.Address    import UrlJoinBrowserStyle, _getLinksMakeOver
    from Web.HTML       import getBodyOnly
    from Web.Links      import getLinkOffHref
    #
    lFrameSpecs = [ getLinkOffHref( sFrame )            for sFrame in lFrameSpecs ]
    #
    lFrameSpecs = [ sFrame for sFrame in lFrameSpecs
                    if not sFrame.startswith( '<' ) ]
    #
    if lFrameSpecs:
        #
        lFrameSpecs = [ UrlJoinBrowserStyle( sURL, sFrame )
                        for sFrame in lFrameSpecs ]
        #
        dSendHeads  = deepcopy( dSendHeaders )
        #
        dSendHeads[ 'Referer' ] = sURL
        #
        if sCookie: dSendHeads[ 'Cookie'    ] = sCookie
        #
        lFrameText  = [ getPageHTML2( sFrame, dSendHeads, tProxy )[ 0 ]
                        for sFrame in lFrameSpecs ]
        #
        def getBodyThenDoLinks( t ):
            #
            sHTML, sFrameURL = t
            #
            return _getLinksMakeOver( getBodyOnly( sHTML ), sFrameURL )
        #
        lFrameText  = lMap( getBodyThenDoLinks, iZip( lFrameText, lFrameSpecs ) )
        #
        if oFindEnd is None:
            #
            # lFrameText[ 0 : 0 ] =  '' # put '' in front
            #
            lParts  = oFindBeg.split( sHTML )
            #
            sFirst  = lParts[ 0 ]
            #
            if lParts: del lParts[ 0 ]
            #
            def getRest( s ): return getTextAfter( s, '>' )
            #
            lParts  = lMap( getRest, lParts )
            #
            lParts[ 0 : 0 ] = [ sFirst ] # put back
            #
        else:
            #
            lParts  = oFindEnd.split( sHTML )
            #
            lParts  = [ oFindBeg.split( sPart )[ 0 ] for sPart in lParts ]
            #
        #
        lFrameText.append( '' )
        #
        lWhole      = getListFromNestedLists( iZip( lParts, lFrameText ) )
        #
        sHTML = ''.join( lWhole )
        #
    #
    # convert links
    #
    return sHTML




def getPageHTML2(
        sURL, dSendHeaders = {}, tProxy = ('', -1 ), doFrames = True, bUnZip = True ):
    #
    """
    This one returns dReceiveHeaders and the page HTML.
    gets page HTML (content) and other stuff,
    but with synchronous (blocking) operation.
    If cannot get page, returns empty string.
    """
    #
    from String.Get     import getUnZipped
    from String.Test    import isGzipped
   #from Utils.Both2n3  import Request, urlopen, build_opener, install_opener, URLError
    from Web.Address    import UrlMustHaveSchemeAndPath
    from Web.HTML       import oFindFrameBeg, oFindiFrameEnd, oFindiFrameBeg, \
                            oFindFrameSpec
    from Web.Zip        import getCompressedOffChunks
    #
    sURL                = UrlMustHaveSchemeAndPath( sURL )
    #
    sHTML               = ''
    dReceiveHeaders     = {}
    #
    sProxy              = ''
    #
    sRealURL            = sURL
    #
    sReason = sErrorCode = sComment = ''
    #
    if tProxy != ('', -1 ) and isDotQuadPortTuple( tProxy ):
        #
        # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/456195
        #
        sProxy          = '%s:%s' % tProxy
        #
        opener  = build_opener(
                    ConnectHTTPHandler( proxy = sProxy ), ConnectHTTPSHandler( proxy = sProxy ) )
        #
        install_opener(opener)
        #
    #
    try:
        #
        oRequest        = Request( sURL, headers = dSendHeaders )
        #
        oPage           = urlopen( oRequest )
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
            sHTML           = oPage.read()
            dReceiveHeaders = oPage.info()
            sRealURL        = oPage.geturl()
        except (ValueError, SocketError):
            error, msg, traceback = exc_info()
            sComment        = 'We hit a socket error on read.'
            sReason         = str( msg )
        #
    #
    dResult = dict(
                sReason     = sReason,
                sErrorCode  = sErrorCode,
                sComment    = sComment,
                sRealURL    = sRealURL )
    #
    if bUnZip and (
                dReceiveHeaders.get( 'content-encoding' ) == 'gzip' or
                isGzipped( sHTML ) ):
        #
        bUnZipped, sHTML = getUnZipped( sHTML )
        #
        if not bUnZipped and \
                dReceiveHeaders.get( 'transfer-encoding' ) == 'chunked':
            #
            sHTML       = getCompressedOffChunks( sHTML )
            #
            bUnZipped, sHTML = getUnZipped( sHTML )
            #
        #
    #
    if sHTML and doFrames:
        #
        liFrames        = oFindiFrameBeg.findall( sHTML )
        lFrames         = oFindFrameBeg.findall(  sHTML )
        #
        sCookie         = dReceiveHeaders.get( 'cookie' )
        #
        if liFrames:
            #
            liFrameSpecs = [ lFrame[ 1 ] for lFrame in
                                [ oFindFrameSpec.split( sFrame ) for sFrame in liFrames ]
                                if len( lFrame ) > 1 ]
            #
            sHTML = _getFrameText(
                        sHTML, liFrameSpecs, sURL, dSendHeaders, sCookie, tProxy,
                        oFindiFrameBeg, oFindiFrameEnd )
            #
        #
        if lFrames:
            #
            lParts      = oFindFrameBeg.split( sHTML )
            #
            if lParts: del lParts[ 0 ]
            #
            lFrameSpecs     = [ lFrame[ 1 ] for lFrame in
                                [ oFindFrameSpec.split( sPart ) for sPart in lParts ]
                                if len( lFrame ) > 1 ]
            #
            sHTML = _getFrameText(
                        sHTML, lFrameSpecs, sURL, dSendHeaders, sCookie, tProxy, oFindFrameBeg )
            #
    #
    return sHTML, dReceiveHeaders, dResult



def getContentHeadersResult(
        sURL,
        sReferrer       = '',
        bMozilla        = True,
        bShowError      = False,
        bWantHeader     = True,
        doFrames        = True,
        doReDirect      = True,
        iRecursive      = False,
        tProxy          = ('', -1),
        sCookie         = '',
        sSpoofForwarded = '',
        sSpoofCacheCtrl = '',
        sSpoofHttpVia   = '',
        bPrintError     = True,
        bCacheContentOK = True,
        bZipOK          = True,
        dLines          = {},
        bUnZip          = True,
        sAccept         = "Accept: text/javascript, text/html, application/xml, text/xml */*",
        **dMoreLines ):
    #
    dHeaders = {
        'User-Agent'        :
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.19) Gecko/2010040119 Ubuntu/8.04 (hardy) Firefox/3.0.19',
        }
    #
    if sReferrer        : dHeaders[ 'Referer'   ] = sReferrer
    #
    if sCookie          : dHeaders[ 'Cookie'    ] = sCookie
    #
    if sSpoofForwarded  : dHeaders[ 'X-Forwarded-For'   ] = sSpoofForwarded
    if sSpoofCacheCtrl  : dHeaders[ 'Cache-Control'     ] = sSpoofCacheCtrl
    if sSpoofHttpVia    : dHeaders[ 'Via'               ] = sSpoofHttpVia
    #
    dHeaders.update( dLines     )
    dHeaders.update( dMoreLines )
    #
    bViaProxy   = False
    #
    if tProxy != ('', -1 ) and isDotQuadPortTuple( tProxy ):
        #
        tConnectTo  = tProxy
        #
        bViaProxy   = True
        #
    if not bCacheContentOK:
        #
        dHeaders[ 'Pragma' ] = 'no-cache'
        #
    if bZipOK:
        #
        dHeaders[ 'Accept-Encoding' ] = 'gzip,deflate'
        #
    if bViaProxy:
        #
        dHeaders[ 'Keep-Alive'       ] = '300'
        dHeaders[ 'Proxy-Connection' ] = 'Keep-Alive'
        #
    else:
        #
        dHeaders[ 'Connection'       ] = 'Keep-Alive'
        #
    #
    dHeaders[ 'Accept' ]                = sAccept
    #
    # sHTML, dReceiveHeaders, dResult = getPageHTML2( sURL, dHeaders, tProxy )
    #
    return getPageHTML2( sURL, dHeaders, tProxy,
                bUnZip = bUnZip,
                doFrames = doFrames )



def getPageContent(
        sURL,
        sReferrer       = '',
        bMozilla        = True,
        bShowError      = False,
        bWantHeader     = True,
        doFrames        = True,
        doReDirect      = True,
        iRecursive      = False,
        tProxy          = ('', -1),
        sCookie         = '',
        sSpoofForwarded = '',
        sSpoofCacheCtrl = '',
        sSpoofHttpVia   = '',
        bPrintError     = True,
        bCacheContentOK = True,
        bZipOK          = True,
        bUnZip          = True,
        dLines          = {},
        sAccept         = "Accept: text/javascript, text/html, application/xml, text/xml */*",
        **dMoreLines ):
    #
    sHTML, dReceiveHeaders, dResult = \
        getContentHeadersResult(
            sURL,
            sReferrer       = sReferrer,
            bMozilla        = bMozilla,
            bShowError      = bShowError,
            bWantHeader     = bWantHeader,
            doFrames        = doFrames,
            doReDirect      = doReDirect,
            iRecursive      = iRecursive,
            tProxy          = tProxy,
            sCookie         = sCookie,
            sSpoofForwarded = sSpoofForwarded,
            sSpoofCacheCtrl = sSpoofCacheCtrl,
            sSpoofHttpVia   = sSpoofHttpVia,
            bPrintError     = bPrintError,
            bCacheContentOK = bCacheContentOK,
            bZipOK          = bZipOK,
            bUnZip          = bUnZip,
            dLines          = dLines,
            sAccept         = sAccept,
            **dMoreLines )
        #
    return sHTML




def getDotQuadFromDomain( sDomain ):
    #
    from socket import gethostbyname, gaierror
    #
    sDotQuad     = ''
    #
    try:
        #
        sDotQuad = gethostbyname( sDomain )
        #
    except gaierror:
        #
        sDotQuad = ''
        #
    except: # what else is there?
        #
        sDotQuad = ''
        #
    #
    return sDotQuad



def getDotQuadFromURL( sURL ):
    #
    from Web.Address import getDomainOffURL
    #
    sDomain     = getDomainOffURL( sURL )
    #
    return getDotQuadFromDomain( sDomain )



def getDotQuadPortFromUrlPort( uShouldBeUrlPort ):
    #
    from Web.Address    import getHostPortPathQuery
    from Web.Test       import isDomainNameOrDotQuad, isDotQuad, \
                           isDomainNameOrDotQuadWithPort, isPort
    #
    tDotQuadPort        = ( '', -1 )
    sDotQuadOrURL       = ''
    sPort               = ''
    #
    if type( uShouldBeUrlPort ) == type( () ):
        #
        sHost           = uShouldBeUrlPort[ 0 ]
        iPort           = uShouldBeUrlPort[ 1 ]
        #
    else:
        #
        sHost, iPort, sPath, sQuery = getHostPortPathQuery( uShouldBeUrlPort )
        #
    #
    sPort               = str( iPort )
    #
    if isDomainNameOrDotQuad( sHost ) and isPort( sPort ):
        #
        if isDotQuad( sHost ):
            #
            sDotQuad    = sDotQuadOrURL
            #
        else:
            #
            sDotQuad    = getDotQuadFromDomain( sHost )
            #
        #
        tDotQuadPort    = ( sDotQuad, iPort )
        #
        #
    #
    return tDotQuadPort





def getHostFromDotQuad( sDotQuad, bWantBlankIfHostSameAsDotQuad = False ):
    #
    from socket import getfqdn
    #
    try:
        #
        sHost   = getfqdn( sDotQuad )
        #
    except:
        #
        sHost   = ''
        #
    #
    if bWantBlankIfHostSameAsDotQuad and sHost == sDotQuad:
        #
        sHost   = ''
        #
    #
    return sHost



def _getOpenRead( oOpener, *args ):
    #
    oResp = oOpener( *args )
    #
    sResults = oResp.read()
    #
    return sResults


def getPostResults(
        sURL,
        dPostData,
        sUserAgent = 'Mozilla/5.0 (X11; U; Linux i686; en-US; ' \
            'rv:1.9.0.19) Gecko/2010040119 Ubuntu/8.04 (hardy) Firefox/3.0.19',
        sReferer   = '',
        bGetCookie = False ):
    #
    from time import sleep
    #
    from six.moves.http_cookiejar   import CookieJar
    from six.moves.urllib.request   import HTTPCookieProcessor
    #
    from Iter.AllVers               import iRange
   #from Utils.Both2n3      import build_opener, urlencode, CookieJar, \
    #                            HTTPCookieProcessor
    from Utils.TimeLimit            import TimeLimitWrap, TimeOverExcept
    #
    cj = CookieJar()
    #
    sPostData = urlencode( dPostData )
    #
    opener = build_opener( HTTPCookieProcessor(cj))
    #
    opener.addheaders.append( ( 'User-agent', sUserAgent ) )
    #
    bProceed = bNewOpener = True
    #
    if bGetCookie and sReferer:
        #
        bProceed = i = 0
        #
        while i < 2: # try 2 times
            #
            i += 1
            #
            try:
                #
                sResults = TimeLimitWrap( 20, _getOpenRead, opener.open, sReferer )
                #
                # sResults = oResp.read()
                #
                bProceed = True
                #
                break
                #
            except TimeOverExcept:
                #
                sResults = 'TimeOverExcept: took too long %s times.' % ( i + 1 )
                #
                opener = None
                #
                if i < 2: sleep( 1 )
                #
            except (    HTTPError,
                        URLError,
                        BadStatusLine,
                        SocketError,
                        ValueError ):
                #
                error, msg, traceback = exc_info()
                #
                sResults = str( msg )
                #
            except AttributeError: # opener got wiped
                #
                opener = build_opener(HTTPCookieProcessor(cj))
                #
                opener.addheaders.append( ( 'User-agent', sUserAgent ) )
                #
                if bNewOpener: i -= 1
                #
                bNewOpener = False
                #
            except ( StopIteration, GeneratorExit, KeyboardInterrupt, SystemExit ):
                #
                raise
                #
            except Exception: # StandardError
                #
                error, msg, traceback = exc_info()
                #
                sResults = str( msg )
                #
        if bProceed:
            #
            sleep(1)
        #
    #
    if bProceed:
        #
        if sReferer:
            opener.addheaders.append( ( 'Referer',    sReferer   ) )
        #
        for i in iRange(3): # try 3 times
            #
            try:
                #
                sResults = TimeLimitWrap(
                            20, _getOpenRead, opener.open, sURL, sPostData )
                #
                # sResults = oResp.read()
                #
                break
            #
            except TimeOverExcept:
                #
                sResults = 'TimeOverExcept: took too long %s times.' % ( i + 1 )
                #
                opener = None
                #
                if i < 2: sleep( 1 )
                #
            except ( HTTPError,
                     URLError,
                     BadStatusLine,
                     SocketError,
                     ValueError ):
                #
                error, msg, traceback = exc_info()
                #
                sResults = str( msg )
                #
            except AttributeError: # opener got wiped
                #
                error, msg, traceback = exc_info()
                #
                sResults = 'opener object got wiped, %s' % str( msg )
                #
            except ( StopIteration, GeneratorExit, KeyboardInterrupt, SystemExit ):
                #
                raise
                #
            except Exception: # StandardError
                #
                error, msg, traceback = exc_info()
                #
                sResults = str( msg )
                #
            #
        #
    #
    return sResults

# getPostResultsAndPlain and getPostResultsPlain moved to pGrab


def _getCodeAndState( sStateCode ):
    #
    # for testing getPostResults()
    #
    from sMail.Abbrev import getStateGotCode
    #
    sStateName          = getStateGotCode( sStateCode )
    #
    sCodeAndState       = ''
    #
    if sStateName:
        #
        sCodeAndState   = '%s%s ' % ( sStateCode, sStateName )
        #
    #
    return sCodeAndState



def getGetPageHtmlSimple( sURL, dParams ):
    #
    #
    # UNTESTED!
    #
    #
    
    #from Utils.Both2n3   import urlopen, urlencode
    from time            import sleep
    #
    from Iter.AllVers    import iRange
    from Utils.TimeLimit import TimeLimitWrap, TimeOverExcept
    #
    sParams = urlencode( dParams )
    #
    sUseURL = sURL
    #
    if '%' in sURL:
        #
        sUseURL = sURL % sParams
        #
    #
    for i in iRange(3): # try 3 times
        #
        try:
            #
            sResults = TimeLimitWrap( 20, _getOpenRead, urlopen, sUseURL )
            #
            # sResults = fPage.read()
            #
            break
        #
        except TimeOverExcept:
            #
            sResults = 'TimeOverExcept: took too long %s times.' % ( 1 + i )
            #
            if i < 2: sleep( 1 )
            #
        except (    HTTPError,
                    URLError,
                    BadStatusLine,
                    SocketError,
                    ValueError ):
            #
            error, msg, traceback = exc_info()
            #
            sResults = str( msg )
            #
        except ( StopIteration, GeneratorExit, KeyboardInterrupt, SystemExit ):
            #
            raise
            #
        except Exception: # StandardError
            #
            error, msg, traceback = exc_info()
            #
            sResults = str( msg )
            #
    #
    return sResults


def getGetPageHtml(
        sURL,
        dParams,
        sUserAgent = 'Mozilla/5.0 (X11; U; Linux i686; en-US; ' \
            'rv:1.9.0.19) Gecko/2010040119 Ubuntu/8.04 (hardy) Firefox/3.0.19',
        sReferer   = '',
        bGetCookie = False ):
    #
    #
    # gets form variables
    #
    #
    from time import sleep
    #
    from Iter.AllVers    import iRange
   #from Utils.Both2n3   import build_opener, urlencode, CookieJar, \
    #                        HTTPCookieProcessor
    from Utils.TimeLimit import TimeLimitWrap, TimeOverExcept
    #
    cj = CookieJar()
    #
    sParams = urlencode( dParams )
    #
    # print3( unquote_plus( sParams ) )
    #
    opener = build_opener(HTTPCookieProcessor(cj))
    #
    opener.addheaders.append( ( 'User-agent', sUserAgent ) )
    #
    bProceed = bNewOpener = True
    #
    if bGetCookie and sReferer:
        #
        bProceed = i = 0
        #
        while i < 2: # try 3 times
            #
            i += 1
            #
            try:
                #
                sResults = TimeLimitWrap( 20, _getOpenRead, opener.open, sReferer )
                #
                # sResults = oResp.read()
                #
                bProceed = True
                #
                break
            #
            except TimeOverExcept:
                #
                sResults = 'TimeOverExcept: took too long %s times.' % ( 1 + i )
                #
                opener = None
                #
                if i < 2: sleep( 1 )
                #
            except (    HTTPError,
                        URLError,
                        BadStatusLine,
                        SocketError,
                        ValueError ):
                #
                error, msg, traceback = exc_info()
                #
                sResults = str( msg )
                #
            except AttributeError: # opener got wiped
                #
                opener = build_opener(HTTPCookieProcessor(cj))
                #
                opener.addheaders.append( ( 'User-agent', sUserAgent ) )
                #
                if bNewOpener: i -= 1
                #
                bNewOpener = False
                #
            except ( StopIteration, GeneratorExit, KeyboardInterrupt, SystemExit ):
                #
                raise
                #
            except Exception: # StandardError
                #
                error, msg, traceback = exc_info()
                #
                sResults = str( msg )
                #
        if bProceed:
            #
            sleep(1)
        #
    #
    if bProceed:
        #
        if sReferer:
            opener.addheaders.append( ( 'Referer',    sReferer   ) )
        #
        for i in iRange(3): # try 3 times
            #
            try:
                #
                sResults = TimeLimitWrap( 20, _getOpenRead, opener.open, sURL % sParams )
                #
                # sResults = oResp.read()
                #
                break
            #
            except TimeOverExcept:
                #
                sResults = 'TimeOverExcept: took too long %s times.' % ( 1 + i )
                #
                opener = None
                #
                if i < 2: sleep( 1 )
                #
            except ( HTTPError,
                     URLError,
                     BadStatusLine,
                     SocketError,
                     ValueError ):
                #
                error, msg, traceback = exc_info()
                #
                sResults = str( msg )
                #
            except AttributeError: # opener got wiped
                #
                sResults = 'opener object got wiped'
                #
            except ( StopIteration, GeneratorExit, KeyboardInterrupt, SystemExit ):
                #
                raise
                #
            except Exception: # StandardError
                #
                error, msg, traceback = exc_info()
                #
                sResults = str( msg )
                #
        #
    return sResults


if __name__ == "__main__":
    #
    from os.path        import join
    #
    from Dir.Get        import sTempDir
    from File.Write     import WriteText2File
    from sMail.Abbrev   import getStateGotCode
    from String.Get     import getTextWithin
    from Utils.Result   import sayTestResult
    from Web.Address    import getDomainOffURL
    #
    lProblems = []
    #
    sURL        = 'http://www.python.org/'
    #
    if getPageUrlOffURL( 'http://www.python.org' ) != 'http://www.python.org':
        #
        lProblems.append( 'getPageUrlOffURL()' )
        #
    #
    dHeaders = {
        'User-Agent'        : 'Mozilla/5.0 (X11; U; Linux i686; en-US; ' \
            'rv:1.9.0.19) Gecko/2010040119 Ubuntu/8.04 (hardy) Firefox/3.0.19',
        'Referer'           : 'http://www.perl.org/',
        'Pragma'            : 'no-cache',
        'Accept-Encoding'   : 'gzip,deflate',
        'Keep-Alive'        : '300',
        'Proxy-Connection'  : 'Keep-Alive' }
    #
    sHTML, dReceiveHeaders, dResult = getPageHTML2( sURL, dHeaders )
    #
    if len( sHTML ) < 5000:
        #
        print3( dReceiveHeaders )
        print3()
        print3( dResult )
        #
        lProblems.append( 'getPageHTML2()' )
        #
    sHTML = getPageContent( sURL )
    #
    if len( sHTML ) < 5000:
        #
        lProblems.append( 'getPageContent()' )
        #
    #
    # if 0:
    sHTML = getGetPageHtmlSimple( sURL, dHeaders )
    #
    sOutFile = join( sTempDir, 'simple.html' )
    #
    WriteText2File( sHTML, sOutFile )
    #
    if getDotQuadFromDomain( 'python.org' ) != '82.94.164.162':
        #
        lProblems.append( 'getDotQuadFromDomain()' )
        #
    if getDotQuadFromURL( 'http://www.python.org' ) != \
            '82.94.164.162':
        #
        lProblems.append( 'getDotQuadFromURL()' )
        #
    if getDotQuadPortFromUrlPort(
            'http://www.python.org:80/' ) != ('82.94.164.162', 80):
        #
        lProblems.append( 'getDotQuadPortFromUrlPort()' )
        #
    if getDomainOffURL( getHostFromDotQuad( '82.94.237.218' ) ) != 'python.org':
        #
        lProblems.append( 'getHostFromDotQuad()' )
        #
    #
    sReferer    = 'https://writerep.house.gov/writerep/welcome.shtml'
    sURL        = 'https://writerep.house.gov/htbin/wrep_findrep'
    #
    dInfo = dict(
        zip     = '98103',
        state   = _getCodeAndState( 'WA' ),
        plusfour= '',
        submit  = "Submit It" )
    #
    sHTML = getPostResults(
        sURL,
        dInfo,
        sReferer = sReferer,
        bGetCookie = True )
    #
    sTextBefore = "Serving "
    sTextAfter  = " District"
    #
    sDist = getTextWithin( sHTML, sTextBefore, sTextAfter )
    #
    sLess = getTextWithin( sHTML, '<head>', '</head>' )
    #
    sRefer = getTextWithin( sLess, ' URL=', '">' )
    #
    if      sDist  == "Washington State's 7th" or \
            sRefer == "https://forms.house.gov/mcdermott/webforms/contact.shtml":
        #
        pass
        #
    else:
        #
        lProblems.append( 'getPostResults()' )
        #
        if len( sHTML ) < 100:
            #
            lProblems.append( sHTML )
            #
        else:
            #
            sOutFile = join( sTempDir, 'HouseDotGov_PostTest.html' )
            #
            WriteText2File( sHTML, sOutFile )
            #
            lProblems.append( '  HTML in %s' % sOutFile )
        #
    #
    sURL = 'http://www.zip-codes.com/search.asp?%s'
    sReferer = 'http://www.zip-codes.com/zip-plus-4-database.asp'
    dParams = {
        'fld-address'   : '1231 n 48th st',
        'fld-city2'     : 'seattle',
        'fld-state2'    : 'wa',
        'srch.x' : '0', 'srch.y' : '0' }
    #
    sHTML = getGetPageHtml(
        sURL, dParams, sReferer = sReferer, bGetCookie = True )
    #
    if not '98103-6625' in sHTML:
        #
        lProblems.append( 'getGetPageHtml()' )
        #
        if len( sHTML ) < 100:
            #
            lProblems.append( sHTML )
            #
        #
    #
    #
    sayTestResult( lProblems )
    # self must access python.org and https://writerep.house.gov/