#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions getRaw
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
import asyncore, socket

from six            import print_ as print3

from Dict.Get       import getItemIter
from Utils.Version  import PYTHON3


class getPageSocket(asyncore.dispatcher):
    #
    def __init__(   self,
                    sURL,
                    sReferrer       = '',
                    bMozilla        = False,
                    tProxy          = ('', -1 ),
                    sCookie         = '',
                    sSpoofForwarded = '',
                    sSpoofCacheCtrl = '',
                    sSpoofHttpVia   = '',
                    bPrintError     = True,
                    bZipOK          = True,
                    bCacheContentOK = True,
                    dLines          = {},
                    **dMoreLines ):
        #
        # import socket handled globally above
        #
        # asyncore.dispatcher.__init__(self)
        # getting
        # TypeError: unbound method __init__() must be called with
        # dispatcher instance as first argument (got getPageSocket instance instead)
        # workaround here:
        #
        from sys        import exc_info
        #
        from Address    import getTuple4Socket
        #
        asyncore.dispatcher.__dict__['__init__'](self)
        #
        sHost, iPort, sPath, sQuery = getTuple4Socket( sURL )
        #
        tConnectTo  = (sHost, iPort)
        #
        bViaProxy   = False
        #
        if tProxy != ('', -1 ) and isDotQuadPortTuple( tProxy ):
            #
            tConnectTo  = tProxy
            #
            bViaProxy   = True
            #
        #
        dMoreLines.update( dLines )
        #
        # self.tConnectTo = tConnectTo
        self.sURL       = sURL
        self.buffer     = ''
        self.path       = sPath
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( tConnectTo )
        self.lContent   = []
        self.bPrintError= bPrintError
        #
        self.dMoreLines = dMoreLines
        #
        self.buffer     = \
                getRequestHeader(
                        sHost,
                        sPath,
                        sQuery,
                        bMozilla        = bMozilla,
                        sReferrer       = sReferrer,
                        bViaProxy       = bViaProxy,
                        sCookie         = sCookie,
                        sSpoofForwarded = sSpoofForwarded,
                        sSpoofCacheCtrl = sSpoofCacheCtrl,
                        sSpoofHttpVia   = sSpoofHttpVia,
                        bZipOK          = bZipOK,
                        bCacheContentOK = bCacheContentOK,
                        dLines          = dMoreLines )
        #
        #
    def handle_connect(self):
        #
        pass
        #
    def handle_read(self):
        #
        try:
            #
            sData = self.recv(8192)
            ## self.sContent += sData
            #
        except socket.error:
            #
            error, msg, traceback = exc_info()
            #
            if self.bPrintError:
                print3( 'got socket error for:', self.sURL, msg )
            #
        else:
            #
            try:
                self.lContent.append( sData )
            except:
                self.lContent = [ sData ]
            #
            #
        #
    def writable(self):
        return bool(self.buffer)
        #
    def handle_write(self):
        #
        iStartLen   = len( self.buffer )
        #
        try:
            #
            sent = self.send(self.buffer)
            #
        except socket.error:
            #
            error, msg, traceback = exc_info()
            #
            if self.bPrintError:
                print3( 'got socket error for:', self.sURL, msg )
            #
        else:
            #
            self.buffer = self.buffer[sent:]
            #
        #
    def handle_close(self):
        #
        self.close()



def OldgetRequestHeader(
        sHost,
        sPath           = '/',
        sQuery          = '',
        bViaProxy       = False,
        sCookie         = '',
        bZipOK          = True,
        sSpoofForwarded = '',
        sSpoofCacheCtrl = '',
        sSpoofHttpVia   = '',
        bMozilla        = False,
        sReferrer       = '',
        bCacheContentOK = True,
        dLines          = {},
        **dMoreLines ):
    #
    # called here and in TestProxies
    #
    from Web.Address    import getPathQueryCombo, getURLfromHostPathQuery
    #
    if not sPath: sPath = '/'
    #
    sBrowser        = 'Mozilla/5.0 (compatible; PowerBrowser/2.0; Linux) KHTML/3.4.1 (like Gecko)'
    #
    if bMozilla:
        #
        sBrowser    = \
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.10) Gecko/20050722 CentOS/1.7.10-1.4.1.centos4'
    #
    if bViaProxy:
        #
        sGetThis = getURLfromHostPathQuery( sHost, sPath, sQuery )
        #
    else:
        #
        sGetThis = getPathQueryCombo( sPath, sQuery )
        #
    #
    sUserAgent  = 'User-Agent: %s' % sBrowser
    #
    sAccept     = 'Accept: %s' % (
    'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5' )
    #
    iSubVersion     = 1
    #
    # if bViaProxy:
    #     #
    #     iSubVersion = 0
    #     #
    #
    lHeaderLines    = [
        'GET %s HTTP/1.%s' % ( sGetThis, iSubVersion ),
        'Host: %s' % sHost,
        sUserAgent,
        sAccept,
        'Accept-Language: en-us,en;q=0.5' ] # 'http://',
    #
    if sCookie:
        #
        lHeaderLines.append( 'Cookie: %s' % sCookie )
        #
    if bZipOK:
        #
        sZip    = 'gzip'
        #
        if bMozilla: sZip = 'gzip,deflate'
        #
        lHeaderLines.append( 'Accept-Encoding: %s' % sZip )
        #
    #
    lHeaderLines.append( 'Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7' )
    #
    if sReferrer:
        #
        lHeaderLines.append( 'Referer: %s' % sReferrer.strip() )
        #
    #
    if sSpoofForwarded:
        #
        lHeaderLines.append( 'X-Forwarded-For: %s' % sSpoofForwarded )
        #
    #
    if sSpoofCacheCtrl:
        #
        lHeaderLines.append( 'Cache-Control: %s' % sSpoofCacheCtrl )
        #
    #
    if sSpoofHttpVia:
        #
        lHeaderLines.append( 'Via: %s' % sSpoofHttpVia )
        #
    #
    if bViaProxy:
        #
        lHeaderLines.append( 'Keep-Alive: 300' )
        lHeaderLines.append( 'Proxy-Connection: Keep-Alive' )
        #
    else:
        #
        lHeaderLines.append( 'Connection: Keep-Alive' )
        #
    #
    if not bCacheContentOK:
        #
        lHeaderLines.append( 'Pragma: no-cache' )
        #
    #
    dMoreLines.update( dLines )
    #
    lHeaderLines.extend( [ '%s: %s' % t for t in getItemIter( dMoreLines ) ] )
    #
    lHeaderLines.append( '\r\n' )
    #
    return '\r\n'.join( lHeaderLines )




def getRequestHeader(
        sHost,
        sPath           = '/',
        sQuery          = '',
        bViaProxy       = False,
        sCookie         = '',
        bZipOK          = True,
        sSpoofForwarded = '',
        sSpoofCacheCtrl = '',
        sSpoofHttpVia   = '',
        bMozilla        = False,
        sReferrer       = '',
        bCacheContentOK = True,
        dLines          = {},
        **dMoreLines ):
    #
    # called here and in TestProxies
    #
    from Web.Address    import getPathQueryCombo, getURLfromHostPathQuery
    #
    if not sPath: sPath = '/'
    #
    if bViaProxy:
        #
        sGetThis = getURLfromHostPathQuery( sHost, sPath, sQuery )
        #
    else:
        #
        sGetThis = getPathQueryCombo( sPath, sQuery )
        #
    #
    iSubVersion     = 1
    #
    # if bViaProxy:
    #     #
    #     iSubVersion = 0
    #     #
    #
    lHeaderLines    = [
        'GET %s HTTP/1.%s' % ( sGetThis, iSubVersion ),
        'Host: %s' % sHost ] # 'http://',
    #
    dLines[ 'User-Agent' ] = \
        'Mozilla/5.0 (compatible; PowerBrowser/2.0; Linux) KHTML/3.4.1 (like Gecko)'
    #
    if bMozilla:
        #
        dLines[ 'User-Agent' ] = \
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008072820 Firefox/3.0.1'
    #
    dLines[ 'Accept' ] = \
        'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5'
    #
    dLines[ 'Accept-Language' ] = 'en-us,en;q=0.5'
    #
    if sCookie:
        #
        dLines[ 'Cookie' ] = sCookie
        #
    if bZipOK:
        #
        sZip    = 'gzip'
        #
        if bMozilla: sZip = 'gzip,deflate'
        #
        dLines[ 'Accept-Encoding' ] = sZip
        #
    #
    dLines[ 'Accept-Charset' ] = 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'
    #
    if sReferrer:
        #
        dLines[ 'Referer' ] = sReferrer.strip()
        #
    #
    if sSpoofForwarded:
        #
        dLines[ 'X-Forwarded-For' ] = sSpoofForwarded
        #
    #
    if sSpoofCacheCtrl:
        #
        dLines[ 'Cache-Control' ] = sSpoofCacheCtrl
        #
    #
    if sSpoofHttpVia:
        #
        dLines[ 'Via' ] = sSpoofHttpVia
        #
    #
    if bViaProxy:
        #
        dLines[ 'Keep-Alive' ] = '300'
        dLines[ 'Proxy-Connection' ] = 'Keep-Alive'
        #
    else:
        #
        dLines[ 'Connection' ] = 'Keep-Alive'
        #
    #
    if not bCacheContentOK:
        #
        dLines[ 'Pragma' ] = 'no-cache'
        #
    #
    dLines.update( dMoreLines )
    #
    lHeaderLines.extend( [ '%s: %s' % t for t in getItemIter( dLines ) ] )
    #
    lHeaderLines.append( '\r\n' )
    #
    return '\r\n'.join( lHeaderLines )



def getHeaderOffBytes( sHTML ):
    #
    sHeader = ''
    #
    uSplitOn = '\r\n\r\n'
    uHeader1 = 'HTTP/1.'
    #
    if PYTHON3 and isinstance( sHTML, bytes ):
        #
        uSplitOn = uSplitOn.encode()
        uHeader1 = uHeader1.encode()
        #
    #
    lParts  = sHTML.split( uSplitOn )
    #
    if sHTML.startswith( uHeader1 ) and len( lParts ) >= 1:
        #
        sHeader = lParts[ 0 ]
        #
    #
    return sHeader



def getHeaderValueOffBytes( sHTML, sHeader ):
    #
    from String.Get import getTextAfterC
    #
    sHttpHeader = getHeaderOffBytes( sHTML )
    #
    sValue      = ''
    #
    sHeader     = sHeader.strip()
    #
    if not sHeader.endswith( ':' ): sHeader += ':'
    #
    sRest       = getTextAfterC( sHttpHeader, sHeader ).lstrip()
    #
    if sRest:
        #
        lRest   = sRest.split()
        #
        sValue  = lRest[0]
        #
    #
    return sValue





def getRawContent(
        sURL,
        sReferrer       = '',
        bMozilla        = False,
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
        dLines          = {},
        **dMoreLines ):
    #
    from Web.Links      import getLinkOffHref
    #
    # bShowError      = no try/except, rather python experiences the error
    # bPrintError     = use try/except, but output message when error occurs
    #
    if sReferrer is None: sReferrer = ''
    #
    if iRecursive > 4:
        #
        return ''   # keep to a reasonable maximum
        #
    global asyncore, socket
    #
    from six.moves.urllib.parse import urljoin
    #
    from Collect.Get    import getListFromNestedLists
    from Iter.AllVers   import lMap, iZip
    from String.Get     import getUnZipped, getTextAfter, getTextBefore
   #from Utils.Both2n3  import urljoin
    from Utils.ImIf     import ImIf
    from Web.Zip        import getCompressedOffChunks
    from Web.HTML       import getBodyOnly, \
                        oFindiFrameBeg, oFindFrameSpec, oFindFrameSpec
    #
    sContent    = ''
    #
    bGotContent = False
    bUnZipped   = False
    iTry        = 0
    #
    sURL        = sURL.strip()
    #
    dMoreLines.update( dLines )
    #
    if bShowError and not isURL( sURL ):
        #
        if bPrintError:
            print3( 'URL "%s" no good' % ( sURL ) )
        #
        return ''
        #
    #
    bZipOK          = True
    #
    while iTry < 5 and not bUnZipped:
        #
        bGotContent = False
        #
        iTry        += 1
        #
        if bShowError:
            #
            oPage = getPageSocket(
                        sURL,
                        sReferrer,
                        bMozilla,
                        tProxy,
                        sCookie,
                        sSpoofForwarded,
                        sSpoofCacheCtrl,
                        sSpoofHttpVia,
                        bPrintError = bPrintError,
                        bZipOK      = bZipOK,
                        dLines      = dMoreLines )
            #
            asyncore.loop()
            #
            bGotContent = True
            #
        else:
            #
            try:
                #
                oPage = getPageSocket(
                            sURL,
                            sReferrer,
                            bMozilla,
                            tProxy,
                            sCookie,
                            sSpoofForwarded,
                            sSpoofCacheCtrl,
                            sSpoofHttpVia,
                            bPrintError = bPrintError,
                            bZipOK      = bZipOK,
                            dLines      = dMoreLines )
                #
                asyncore.loop()
                #
                bGotContent = True
                #
            except socket.gaierror:
                #
                if bPrintError:
                    error, msg, traceback = exc_info()
                    print3( 'got socket gaierror for:', sURL, msg )
                return ''
                #
            except socket.error:
                #
                error, msg, traceback = exc_info()
                #
                if iTry < 3 and msg == (101, 'Network is unreachable'): # wake up, ADSL!!!
                    #
                    oPage = None
                    #
                    continue
                    #
                else:
                    if bPrintError:
                        print3( 'got socket error for:', sURL, e )
                    return ''
            except:
                #
                raise
                if bPrintError:
                    print3( 'problem URL:', sURL )
                return ''
                #
            #
        #
        #
        if bGotContent:
            #
            sContent = ''.join( oPage.lContent )
            #
            if getHeaderValueOffBytes( sContent, 'Content-Encoding' ) == 'gzip':
                #
                bUnZipped, sHTML = getUnZipped( sContent )
                #
                if not bUnZipped:
                    #
                    bZipOK  = False
                    #
                    continue
                    #
                #
            else:
                #
                bUnZipped   = True
                #
            #
        #
    if bGotContent and bUnZipped:
        #
        liFrames     = oFindiFrameBeg.findall( sContent )
        #
        if doFrames and liFrames:
            #
            try:
                #
                liFrameSpecs = [ oFindFrameSpec.split( sFrame )[ 1 ]
                                for sFrame in liFrames ]
                #
                liFrameSpecs = [ getLinkOffHref( sFrame )
                                for sFrame in liFrameSpecs ]
                #
                liFrameSpecs = [ urljoin( sURL, sFrame )
                                for sFrame in liFrameSpecs ]
                #
                lFrameText  = [ getPageContent(
                                    sFrame,
                                    sURL,
                                    bWantHeader = False,
                                    iRecursive = iRecursive + 1,
                                    bPrintError= bPrintError )
                                for sFrame in liFrameSpecs ]
                #
                lFrameText  = lMap( getBodyOnly, lFrameText )
                #
                lFrameText.append( '' )
                #
                lParts      = oFindiFrameEnd.split( sContent )
                #
                lParts      = [ oFindiFrameBeg.split( sPart )[ 0 ]
                                for sPart in lParts ]
                #
                lWhole      = getListFromNestedLists(
                                    iZip( lParts, lFrameText ) )
                #
                sContent    = ''.join( lWhole )
                #
            except:
                #
                pass
                #
        #
        sStatusCode     = getStatusCodeOffBytes( sContent )
        #
        if doReDirect and sStatusCode in ( '307', '303', '302', '301' ):
            #
            # Temporary Redirect, See Other, Found, Moved Permanently
            #
            sLocation = getHeaderValueOffBytes( sContent, 'Location' )
            #
            if isURL( sLocation ):
                #
                sContent    = getPageContent(
                                sLocation, iRecursive = iRecursive + 1, bPrintError = bPrintError )
                #
        #
        if not bWantHeader:
            #
            lParts = sContent.split( '\r\n\r\n' )
            #
            if len( lParts ) > 1 and len( lParts[0] ) < 1000:
                #
                lParts      = lParts[ 1 : ]
                #
                sContent    = '\r\n\r\n'.join( lParts )
                #
        #
        #
        #
    #
    #
    return sContent



def getHttpStripHeader( sHTML ):
    #
    sBody   = sHTML
    #
    lParts  = sHTML.split( '\r\n\r\n' )
    #
    if sHTML.startswith( 'HTTP/1.' ) and len( lParts ) >= 2:
        #
        sBody   = lParts[ 1 ]
        #
    #
    return sBody



def getStatusCodeOffBytes( sHTML, sReturn = '' ):
    #
    from Iter.AllVers   import tFilter
    from String.Get import getTextBefore
    #
    if sHTML is None or type( sHTML ) != str or sHTML == '':
        #
        pass
        #
    else:
        #
        s1stLine = getTextBefore( sHTML, '\r\n' )
        #
        lWords   = s1stLine.split()
        #
        def ThreeDigitsOnly( sWord ): return sWord.isdigit() and len( sWord ) == 3
        #
        tStatusCode = tFilter( ThreeDigitsOnly, lWords )
        #
        if tStatusCode:
            #
            sReturn = tStatusCode[ 0 ]
            #
    #
    return sReturn



if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    sURL        = 'http://www.python.org/'
    #
    sHTML = getRawContent( sURL, sReferrer = 'http://www.perl.org/', bMozilla = True )
    #
    # print3( len( sHTML ) )
    if len( sHTML ) < 5000:
        #
        lProblems.append( 'getRawContent()' )
        #
    #
    if len( getHeaderOffBytes( sHTML ) ) < 250:
        #
        lProblems.append( 'getHeaderOffBytes()' )
        #
    # print3( getHeaderOffBytes( sHTML ) )
    if      int( getHeaderValueOffBytes( sHTML, 'Content-Length'  ) ) + \
            len( getHeaderOffBytes( sHTML ) ) + 4 != len( sHTML ):
        #
        lProblems.append( 'getHeaderValueOffBytes()' )
        #
    if getStatusCodeOffBytes( sHTML ) != '200':
        #
        lProblems.append( 'getStatusCodeOffBytes()' )
        #
    if      str( len( getHttpStripHeader( sHTML ) ) ) != \
                getHeaderValueOffBytes( sHTML, 'Content-Length' ):
        #
        lProblems.append( 'getHttpStripHeader()' )
        #
    #
    sHeader = getRequestHeader(
        sHost           = 'www.python.org',
        sPath           = '/about/',
        sQuery          = '',
        bViaProxy       = False,
        sCookie         = '',
        bZipOK          = 1,
        sSpoofForwarded = '',
        sSpoofCacheCtrl = '',
        sSpoofHttpVia   = '',
        bMozilla        = 1,
        sReferrer       = 'www.perl.org' )
    #
    lHeader             = sHeader.split( '\r\n' )
    #
    if      lHeader[0] != 'GET /about/ HTTP/1.1' or \
            lHeader[1] != 'Host: www.python.org' :
        #
        lProblems.append( 'getRequestHeader() GET and Host' )
        #
    #
    lExpect = [
        'Accept-Language: en-us,en;q=0.5',
        'Accept-Encoding: gzip,deflate',
        'Accept: text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
        'User-Agent: Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008072820 Firefox/3.0.1',
        'Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Connection: Keep-Alive',
        'Referer: www.perl.org' ]
    #
    for sLine in lExpect:
        #
        if sLine not in lHeader:
            #
            lProblems.append( 'getRequestHeader() %s' % sLine )
            #
    #
    if not sHeader.endswith( '\r\n\r\n' ):
        #
        lProblems.append( 'getRequestHeader() double CR LF' )
        #
    #
    sayTestResult( lProblems )