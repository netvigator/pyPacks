#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions getGoogle get qoogle query results using custom search API
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
# Copyright 2012-2017 Rick Graves
#
# self test needs internet connection and will access www.googleapis.com
'''
classes implementing google searches

'''

'''
reload( Web.getGoogle )
import Web.getGoogle
from File.Write import putListInTemp, MakeTemp, QuickDump, QuickDumpLines
from File.Get import getContent
from String.Find  import getFinder
from Web.HTML import addLineBreaks
from String.Text4Tests import sGoogleQuerResult_Konq, sGoogleQuerResult_Chrome

sHTML = addLineBreaks( getContent('search_result_chrome.html') )
sHTML = sGoogleQuerResult_Chrome

sBigQuery = (
  'allintext: -error REMOTE_ADDR REQUEST_METHOD '
  'googlebot(at)googlebot.com HTTP_USER_AGENT '
  'HTTP_CONNECTION HTTP_HOST HTTP_REFERER HTTP_ACCEPT' )
o =  Web.getGoogle.getGoogleSearchWeb( q = sBigQuery, bUseCookie = False )
self = o
iterLinkTitleSnip = o._getGoogleResults( sHTML )
putListInTemp( list( iterLinkTitleSnip ) )


'''
from six                import print_ as print3
from six.moves.urllib.parse import quote_plus, unquote_plus

from String.Convert     import getString
from String.Dumpster    import getWhiteDumped
from Utils.Config       import getConfDict
from Web.Get2n3         import getPage
from Web.HTML           import addLineBreaks

from pprint import pprint

class Finished( Exception ):
    #
    def __init__( self, arg = None ):
        #
        self.arg = arg
        #
    def __str__( self ):
        #
        return str( self.arg )

class FinishedPage( Exception ): pass

dConf   = getConfDict( 'getGoogle.conf' )


class baseGoogle( getPage ):
    #
    def __init__( self,
            q = 'q is the query parameter and it is required',
            start       =  1,
            iPerPage    =  10,
            iPause      =  5,
            bUseCookie  = False,
            sUserAgent  = 'default',
            bAcceptGzip = True,
            sConfSection= '',
            **kwargs ):
        #
        super( baseGoogle, self ).__init__(
                    bUseCookie  = bUseCookie,
                    sUserAgent  = sUserAgent,
                    bAcceptGzip = bAcceptGzip,
                    **kwargs )
        #
        self.iPriorGotP = 0
        self.iStartIndex= start
        self.iPerPage   = iPerPage
        self.iPause     = iPause
        #
        self._setEscapeThese()
        #
        iSecondsPause   = 2
        iPauseVaries    = 0
        #
        dConfSection = {}
        #
        if sConfSection and sConfSection in dConf:
            #
            dConfSection = dConf[sConfSection]
            #
            if 'fields' in dConfSection:
                #
                kwargs['fields'] = dConfSection['fields']
            #
            if 'secondspause' in dConfSection:
                #
                iSecondsPause = float( dConfSection['secondspause'] )
            #
            if 'pausevaries'  in dConfSection:
                #
                iPauseVaries  = float( dConfSection['pausevaries'] )
            #
        #
        self.dConfSection = dConfSection
        #
        dParams = dict( q = q )
        #
        dParams.update( kwargs )
        #
        sParams = self.getParams( dParams )
        #
        self.sParams = sParams
        #
        self.iSecondsPause  = iSecondsPause
        self.iPauseVaries   = iPauseVaries
        self.tPriorRequest  = 0


    def _recordTime( self ):
        #
        from time import time
        #
        self.tPriorRequest = time()


    def _checkTime( self ):
        #
        from random import random
        from time import time, sleep
        #
        tNow = time()
        #
        if (    self.tPriorRequest > 0 and
                tNow - self.tPriorRequest < self.iSecondsPause ):
            #
            tWantPause = ( self.iSecondsPause +
                            ( self.iPauseVaries * random() ) -
                            ( self.iPauseVaries / 2.0 ) )
            #
            tWantRequest = self.tPriorRequest + tWantPause
            #
            if tWantRequest > tNow:
                #
                tSleep = tWantRequest - tNow
                if self.dConfSection.get( 'debug' ):
                    print3( 'pausing for %4.1f seconds ...' % tSleep )
                sleep( tSleep )


    def getParams( self, dParams ):
        #
        from Dict.Get       import getItemIter
        #
        sParams = '&'.join( [ '%s=%s' %
            ( kv[0], self._quoteThis( *kv ) )
                for kv in getItemIter( dParams )
                if kv[1] ] )
        #
        return sParams


    def _setEscapeThese( self ):
        #
        '''
        override this method if you want different values escaped
        '''
        #
        self.setEscapeThese = frozenset( ( 'q', ) )


    def _quoteThis( self, key, value ):
        #
        #from Utils.Both2n3  import quote_plus
        #
        if key in self.setEscapeThese:
            #
            value = quote_plus( value )
        #
        return value


    def getPageStartIndex( self ):
        #
        if self.iPriorGotP > 0:
            #
            self.iStartIndex += self.iPerPage
            #
        #
        self.iPriorGotP += 1



# http://code.google.com/apis/customsearch/v1/using_rest.html

sSEARCH = '''https://www.googleapis.com/customsearch/v1?
    key=%(api_key)s
    &cx=%(cse_id)s
    &start=%(iStartIndex)d
    &%(sParams)s
    '''

sSEARCH = getWhiteDumped( sSEARCH )


class getGoogleAPI( baseGoogle ):
    #
    '''
    class implements the google JSON/Atom Custom Search API
    http://code.google.com/apis/customsearch/v1/using_rest.html#query-params
    '''
    #
    def __init__( self,
            q = 'q is the query parameter and it is required',
            start       =  1,
            iPerPage    =  10,
            iPause      =  5,
            exactTerms  = '',
            excludeTerms= '',
            orTerms     = '',
            bUseCookie  = False,
            sUserAgent  = '',
            bAcceptGzip = True,
            **kwargs ):
        #
        from Utils.Version import getSayVersion
        #
        if bAcceptGzip and 'gzip' not in sUserAgent:
            #
            sUserAgent = 'getGoogle (%s) (gzip)' % getSayVersion()
        #
        super( getGoogleAPI, self ).__init__(
                q           = q,
                start       = start,
                iPerPage    = iPerPage,
                iPause      = iPause,
                bUseCookie  = bUseCookie,
                sUserAgent  = sUserAgent,
                bAcceptGzip = bAcceptGzip,
                sConfSection= 'api-search',
                **kwargs )
        #
        self.exactTerms  = exactTerms
        self.excludeTerms= excludeTerms
        self.orTerms     = orTerms

    def getNextPage( self ): # getGoogleAPI
        #
        from Iter.AllVers   import iFilter
        #
        self.getPageStartIndex()
        #
        dSearch = dict(
            sParams     = self.sParams,
            iStartIndex = self.iStartIndex )
        #
        dSearch.update( dConf['main'] )
        #
        sURI = sSEARCH % dSearch
        #
        self._checkTime()
        #
        sHTML, oHeaders, dResult = self.getHtmlAndResults( sURI )
        #
        dResult['URI'] = sURI
        #
        #sHead       = repr( getDictOffObject( oHeaders ) )
        #sResult     = repr( dResult )
        #
        self._recordTime()
        #
        return sHTML, oHeaders, dResult

    def _setEscapeThese( self ):
        #
        '''
        override this method if you want different values escaped
        '''
        #
        self.setEscapeThese = frozenset(
            ( 'q', 'exactTerms', 'excludeTerms', 'orTerms', ) )
        #



# http://code.google.com/apis/customsearch/docs/xml_results.html




sGoogleHomeURL  = '''http://www.google.com'''

sGoogleSearch_1 = '''http://www.google.com/search?
                    %(sParams)s&btnG=Google+Search'''

sGoogleSearch_N = '''http://www.google.com/search?
                    %(sParams)s&start=%(start)d&btnG=Search'''

sGoogleSearch_1 = getWhiteDumped( sGoogleSearch_1 )
sGoogleSearch_N = getWhiteDumped( sGoogleSearch_N )


'''
helpful hints
allintext   = 'has all of the words in the search query in the body of the document.',
intitle     = 'has a particular word in the document title',
allintitle  = 'has all of the query words in the document title',
inurl       = 'has a particular word in the document URL',
allinurl    = 'has all of the query words in the document URL'
'''
class getGoogleSearchWeb( baseGoogle ):
    #
    '''
    class implements browser style google search
    '''
    #
    def __init__( self,
            q = 'q is the query parameter and it is required',
            start       =  1,
            iPerPage    =  10,
            iPause      =  5,
            bUseCookie  = True,
            bAcceptGzip = True,
            **kwargs ):
        #
        super( getGoogleSearchWeb, self ).__init__(
                q           = q,
                start       = start,
                iPerPage    = iPerPage,
                iPause      = iPause,
                bUseCookie  = bUseCookie,
                bAcceptGzip = bAcceptGzip,
                sConfSection= 'web-search',
                **kwargs )
        #
        self.sInitReturn = self.getCookieOffHomePage( sGoogleHomeURL )
        #
        self._getTextFinders()
        #
        self.sNextPageQuery = None

    def getNextPage( self ): # getGoogleSearchWeb
        #
        if self.sNextPageQuery:
            #
            sGoogleSearch = self.sNextPageQuery
            #
        elif self.iStartIndex == 1:
            #
            sGoogleSearch = sGoogleSearch_1
            #
        else:
            #
            sGoogleSearch = sGoogleSearch_N
            #
        #
        if not self.sNextPageQuery and self.iPerPage != 10:
            #
            sGoogleSearch = sGoogleSearch.replace( '&start=%(iStartIndex)d', '&start=%(iStartIndex)d&num=%(iPerPage)d' )
        #
        self.getPageStartIndex()
        #
        dSearch = dict(
                sParams = self.sParams,
                start   = self.iStartIndex,
                iPerPage= self.iPerPage )
        #
        sURI = sGoogleSearch % dSearch
        #
        self._checkTime()
        #
        sHTML, oHeaders, dResult = self.getHtmlAndResults( sURI )
        #
        dResult['URI'] = sURI
        #
        self._recordTime()
        #
        return sHTML, oHeaders, dResult


    def _getTextFinders( self ):
        #
        from String.Find    import getFinder, getFinderFindAll
        from Web.HTML       import oTagFinder
        #
        dConfSection        = self.dConfSection
        #
        self.oAboveResults  = getFinder( dConfSection['resultsafter'] )
        #
        sCacheSimilar       = dConfSection['cachesimilar']
        #
        self.oCiteFinder    = getFinder( '<cite.+?</cite>',
                                                    bDotAll = True )
        #
        self.oCacheSimFind  = getFinder( sCacheSimilar )
        #
        self.oHasNext       = getFinderFindAll( dConfSection['next'] )
        #
        # self.oTagFinder   = getFinder( '<.*?>'  )
        # self.oTagFinder   = getFinder( '''<("[^"]*"|'[^']*'|[^'">])*>''' )
        self.oTagFinder     = oTagFinder
        #
        # self.oEndTagFind  = getFinder( '</.+?>' )
        #
        self.oAnchorBegFind = getFinder( '<a '  )
        self.oAnchorEndFind = getFinder( '</a>' )
        #
        self.oThruGoogleFind= getFinder( '\?q='  )
        #
        self.oSupressText   = getFinder( dConfSection['supresstext'] )
        #
        self.oResultBegFind = getFinder( dConfSection['resultbeg'] )
        #
        self.oResultEndFind = getFinder( dConfSection['resultend'] )



    def _getAllTagsWiped( self, s ):
        #
        return self.oTagFinder.sub( '', s )


    def _getSplitOnBegResult( self, s ):
        #
        return self.oResultBegFind.split( s )


    def _getHtmlResultsAndFooter( self, sHTML ):
        #
        from File.Write         import QuickDump
        from Iter.AllVers       import iMap
       #from Utils.Both2n3      import unquote_plus
        #
        from String.Get         import getTextAfter, getTextWithin
        from String.Dumpster    import getChoppedOff
        #
        sFoot, sResult  = '', ''
        #
        lBodyFoot       = sHTML.split( self.dConfSection['footbeg'], 1 )
        #
        sPlainParams    = getTextAfter( unquote_plus( self.sParams ), '=' )
        #
        lHeadBody       = lBodyFoot[0].split( sPlainParams, 1 )
        #
        if len( lHeadBody ) == 1:
            #
            print3(self.sParams)
            print3('no search parameters found in page')
            # raise Finished('no search parameters found in page')
            #
            QuickDump( sHTML, 'no_search_params.html' )
        #
        sFoot       = getTextWithin(
                        lBodyFoot[ -1 ], '>', self.dConfSection['footend'] )
        #
        sResult     = getChoppedOff( lHeadBody[ -1 ], '<' )
        #
        lJunkResults= self.oAboveResults.split( sResult )
        #
        lResults    = self.oCiteFinder.split( lJunkResults[ -1 ] )
        #
        iResults    = iMap( self._getSnippetZapRest, lResults )
        #
        sResult     = self._getTextSupressed( ''.join( iResults ) )
        #
        return sResult, sFoot


    def _getSnippetZapRest( self, s ):
        #
        from Iter.AllVers import iReverseRange
        #
        lParts  = self.oCacheSimFind.split( s )
        #
        iParts  = len( lParts )
        #
        if iParts > 1:
            #
            lAnchorEnds = self.oAnchorEndFind.split(
                            lParts[ -1 ], maxsplit = 1 )
            #
            if len( lAnchorEnds ) > 1:
                #
                s = lAnchorEnds[ -1 ]
            #
        #
        return s


    def _getTextSupressed( self, sSnipAndCodes ):
        #
        from Iter.AllVers  import iRange, iReverseRange
        #
        # lSupressSnips   = self.oSupressText.findall( sSnipAndCodes )
        #
        lSupressText    = self.oSupressText.split(   sSnipAndCodes )
        #
        iTextLen        = len( lSupressText )
        #
        for i in iReverseRange( len( lSupressText ) - 1 ):
            #
            # sSnip   = lSupressSnips[i]
            #
            iBegTag = lSupressText[i].rfind( '<' )
            #
            sBegTag = lSupressText[i][ iBegTag : ]
            #
            sTag    = sBegTag[ 1 : ].split()[0]
            #
            sEndTag = '</%s>' % sTag
            #
            lWipeThese = []
            #
            for iLook in iRange( i + 1, iTextLen ):
                #
                lWipeThese.append( iLook )
                #
                if sEndTag in lSupressText[ iLook ]:
                    #
                    del lWipeThese[ -1 ]
                    #
                    iRest = lSupressText[ iLook ].find( sEndTag )
                    #
                    lSupressText[ iLook ] = \
                        lSupressText[ iLook ][ iRest + len( sEndTag ) : ]
                    #
                    for iWipe in lWipeThese:
                        #
                        lSupressText[ iWipe ] = ''
                        #
                    #
                    break
                    #
                #
            #
            lSupressText[i] = lSupressText[i][ : iBegTag ]
            #
        #
        sSnipAndCodes = ''.join( lSupressText )
        #
        return sSnipAndCodes


    def _getLinkTitleSnip( self, sResult ):
        #
        #from Utils.Both2n3   import unquote_plus
        #
        from String.Split    import getWhiteCleaned
        from Web.HTML        import getChars4HtmlCodes
        #
        sRest, sSnip = '', ''
        #
        # sNoCite = self.oCiteFinder.sub( '', s )
        #
        lParts = self.oResultEndFind.split( unquote_plus( sResult ), 1 )
        #
        sLink = lParts[0]
        #
        lLinkParts = self.oThruGoogleFind.split( sLink )
        #
        if len( lLinkParts ) > 1: sLink = lLinkParts[1]
        #
        iQmarkAt = sLink.find( '?' )
        #
        if iQmarkAt > 0: sLink = sLink[ : iQmarkAt ]
        #
        if len( lParts ) > 1: sRest = lParts[1]
        #
        lJunkWant = sRest.split( self.dConfSection['titlebeg'], 1 )
        #
        sWant   = lJunkWant[ -1 ]
        #
        lTitleRest = sWant.split( self.dConfSection['titleend'], 1 )
        #
        sTitle  = getChars4HtmlCodes(
                    self._getAllTagsWiped( ( lTitleRest[ 0 ] ) ) )
        #
        if len( lTitleRest ) > 1:
            #
            sSnip = getWhiteCleaned(
                    getChars4HtmlCodes(
                    self._getAllTagsWiped( lTitleRest[1] ) ) ).strip()
            #
        #
        return sLink, sTitle, sSnip


    def _getNextPageQuery( self, s ):
        #
        from String.Find import getTextInQuotes
        from Web.HTML    import getChars4HtmlCodes
        #
        sNextPageQuery = None
        #
        lLinks = ( '', )
        #
        if self.oHasNext( s ):
            #
            lLinks = self.oAnchorBegFind.split( s )
            #
        sNextLink = lLinks[ -1 ]
        #
        if self.oHasNext( sNextLink ):
            #
            sNextPageQuery = getChars4HtmlCodes(
                                getTextInQuotes( sNextLink ) )
        #
        return sNextPageQuery


    def _getGoogleResults( self, sHTML ):
        #
        from sys            import exc_info
        #
        from File.Write     import QuickDump
        from Iter.AllVers   import iMap
        #
        try:
            #
            sResult, sFoot  = self._getHtmlResultsAndFooter( sHTML )
            #
            #if self.dConfSection.get( 'debug' ):
                #QuickDump(
                    #addLineBreaks( sResult ), 'googleResults.txt' )
                #QuickDump(
                    #addLineBreaks( sFoot   ), 'googleFoot.txt' )
            #
            self.sNextPageQuery = None
            #
            sNextPageQuery  = self._getNextPageQuery( sFoot )
            #
            if sNextPageQuery:
                self.sNextPageQuery = sGoogleHomeURL + sNextPageQuery
            #
            lResults        = self._getSplitOnBegResult( sResult )
            #
            if len( lResults ) == 1: raise Finished('no links')
            #
            del lResults[0]
            #
            if len( lResults ) != self.iPerPage or not sNextPageQuery:
                #
                QuickDump(
                    addLineBreaks( sHTML ),
                    'google_results_p%03d.html' % self.iPriorGotP,
                    bSayBytes = False )
                #
            #
            iterLinkTitleSnip = iMap( self._getLinkTitleSnip, lResults )
            #
        except Finished:
            #
            error, msg, traceback = exc_info()
            #
            iterLinkTitleSnip = iter( ( error, msg, traceback ) )
            #
            self.sNextPageQuery = ''
        #
        return iterLinkTitleSnip


    def getQueryResults( self ):
        #
        from six            import next as getNext
        #
       #from Utils.Both2n3  import getNext
        #
        while True:
            #
            sHTML, oHeaders, dResult = self.getNextPage()
            #
            if not sHTML:
                raise StopIteration('no content from page')
            #
            iterLinkTitleSnip = self._getGoogleResults( sHTML )
            print3( 'got page %d ...' % self.iPriorGotP )
            #
            try:
                #
                while True:
                    #
                    try:
                        #
                        yield getNext( iterLinkTitleSnip )
                        #
                    except StopIteration:
                        #
                        if self.sNextPageQuery:
                            raise FinishedPage
                        else:
                            raise StopIteration('no query for next page')
                #
            except FinishedPage:
                #
                continue
            #



if __name__ == "__main__":
    #
    from sys                import argv
    #
    from six                import next as getNext
    #
    from File.Write         import QuickDump, QuickDumpLines
    from Iter.AllVers       import iMap
    from Object.Get         import getDictOffObject
    from String.Text4Tests  import sGoogleQuerResult_Konq, sGoogleQuerResult_Chrome
   #from Utils.Both2n3      import getNext
    from Utils.Result       import sayTestResult
    #
    lProblems = []
    #
    doWebSearch   = len(argv) > 1
    #
    oGetGoogleAPI = getGoogleAPI( q = 'intitle:"AZ Environment variables"' )
    #
    if oGetGoogleAPI.bUseCookie:
        #
        lProblems.append( 'oGetGoogleAPI.bUseCookie is True' )
        #
    #
    if not oGetGoogleAPI.sUserAgent:
        #
        lProblems.append(
            'oGetGoogleAPI.sUserAgent is blank' )
        #
    #
    if doWebSearch:
        #
        sHTML, oHeaders, dResult = oGetGoogleAPI.getNextPage()
        #
        if oHeaders is None:
            sHead = 'None'
        else:
            sHead   = repr( getDictOffObject( oHeaders ) )
        #
        sResult     = repr( dResult )
        #
        if len( sHTML ) > 100:
            QuickDump( sHTML,   'googleAPI.txt', bSayBytes = False )
            if dConf['api-search'].get( 'debug' ):
                QuickDump( sHead,   'goHeadAPI.txt' )
                QuickDump( sResult, 'resultAPI.txt' )
        else:
            print3( 'recommend that you check the API URI result in a browser' )
            print3( dResult['URI'] )
            lProblems.append( '"AZ Environment variables" query did not work' )
        #
        if dConf['api-search'].get( 'debug' ):
            if sNextPageQuery:
                print3( sNextPageQuery )
                #
            else:
                print3( 'recommend that you check the Web URI result in a browser' )
                print3( dResult['URI'] )
                lProblems.append( '"AZ Environment variables" query did not work' )
    #
    sBigQuery = (
    'allintext: -error REMOTE_ADDR REQUEST_METHOD '
    'googlebot(at)googlebot.com HTTP_USER_AGENT '
    'HTTP_CONNECTION HTTP_HOST HTTP_REFERER HTTP_ACCEPT' )
    #
    #
    if doWebSearch:
        #
        oGetGoogleWeb = getGoogleSearchWeb( q = sBigQuery )
        #
        o = oGetGoogleWeb
        #
        if o.dConfSection.get( 'debug' ):
            #
            sHTML, oHeaders, dResult = o.getNextPage()
            #
            if sHTML:
                #
                iterLinkTitleSnip = o._getGoogleResults( sHTML )
                #
                #   list( iMap( getString, iterLinkTitleSnip ) ),
                QuickDumpLines(
                    iterLinkTitleSnip, 'LinkTitleSnip.txt' )
                #
                QuickDump( addLineBreaks( sHTML ),
                    'googleWeb.html', bSayBytes = False )
                QuickDump( sHead,
                    'goHeadWeb.txt',  bSayBytes = False )
                QuickDump( sResult,
                    'resultWeb.txt',  bSayBytes = False )
            #
        #
        #print3( oGetGoogleWeb.sParams )
        #
        else:
            #
            if oGetGoogleWeb.sInitReturn != 'OK':
                #
                lProblems.append( oGetGoogleWeb.sInitReturn  )
            else:
                #
                QuickDumpLines(
                    list( oGetGoogleWeb.getQueryResults() ), 'LinkTitleSnip.txt' )
        #
    #
    o = getGoogleSearchWeb( q = sBigQuery, bUseCookie = False )
    #
    iterLinkTitleSnip   = o._getGoogleResults( sGoogleQuerResult_Konq )
    #
    tLinkTitleSnip      = tuple( iterLinkTitleSnip )
    #
    tLinkTitleSnipCorrect = (
        'http://www.cem.brighton.ac.uk/cgi-bin/mas/mas_rec.exe',
        'AUTH_TYPE CONTENT_LENGTH 0 CONTENT_TYPE ...',
        '... HTTP_ACCEPT */* HTTP_CONNECTION Keep-alive HTTP_HOST ... '
            'HTTP_USER_AGENT Mozilla/5.0 (compatible; Googlebot/2.1; ... '
            'page=mas&file= w://cgi-bin//mas//00mas_logs REMOTE_ADDR ... '
            '66.249.72.164 REMOTE_IDENT [] REMOTE_USER REQUEST_METHOD ... '
            'HTTP_FROM= googlebot(at)googlebot.com ...' )
    #
    def isLinkTitleSnipCloseEnough( tResult, tWant ):
        #
        from String.Dumpster    import getWhiteWiped
        #
        return (
            tResult[0] == tWant[0] and
            tResult[1] == tWant[1] and
            getWhiteWiped( tResult[2] ) == getWhiteWiped( tWant[2] ) )
    #
    if not isLinkTitleSnipCloseEnough(
            tLinkTitleSnip[0], tLinkTitleSnipCorrect ):
        #
        print3( tLinkTitleSnip[0][0] )
        print3( tLinkTitleSnipCorrect[0] )
        print3( '\n' )
        print3( tLinkTitleSnip[0][1] )
        print3( tLinkTitleSnipCorrect[1] )
        print3( '\n' )
        print3( tLinkTitleSnip[0][2] )
        print3( tLinkTitleSnipCorrect[2] )
        #
        lProblems.append( 'did not get 1st link/title/snip off Konq' )
        #
    #
    if len( tLinkTitleSnip ) != 10:
        #
        lProblems.append( 'did not get 10 link/title/snips off Konq' )
        #
    #
    iterLinkTitleSnip   = o._getGoogleResults( sGoogleQuerResult_Chrome )
    #
    tLinkTitleSnip      = tuple( iterLinkTitleSnip )
    #
    tLinkTitleSnipCorrect = (
        'http://www.sg-as.ru/myip',
        'подробнее - Стерлинг Групп А.С.',
        '15 items ... (HostName): crawl-66-249-72-83.googlebot.com. '
        'Проверить ... Переменные сервера (Server Variables) Значения '
        '(Values) ALL_RAW Connection: Keep-alive Content ...' )
    #
    if not isLinkTitleSnipCloseEnough(
            tLinkTitleSnip[0], tLinkTitleSnipCorrect ):
        #
        print3( tLinkTitleSnip[0][0] )
        print3( tLinkTitleSnipCorrect[0] )
        print3( '\n' )
        print3( tLinkTitleSnip[0][1] )
        print3( tLinkTitleSnipCorrect[1] )
        print3( '\n' )
        print3( tLinkTitleSnip[0][2] )
        print3( tLinkTitleSnipCorrect[2] )
        #
        lProblems.append( 'did not get 1st link/title/snip off Chrome' )
        #
    #
    if len( tLinkTitleSnip ) != 10:
        #
        lProblems.append(
            'did got %d link/title/snips off Chrome' %
            len( tLinkTitleSnip ) )
        #
    #
    sayTestResult( lProblems )