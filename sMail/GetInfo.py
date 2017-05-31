#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# SnailMail sMail functions get Info getMissingInfo
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


from String.Get     import getTextAfter, getTextWithin
from Web.Scraper    import PosterScraperClass, getterScraperClass, oSequencer


class Finished( Exception ): pass

sTempUnavailable = 'temporarily unavailable: web site for %s'



class getParamsClass( object ):
    #
    def __init__( self ):
        #
        self.sURL           = ''
        self.sReferer       = ''
        self.sBefore        = ''
        self.sAfter         = ''
        self.sNotFound      = ''
        self.sBlocked       = ''
        self.sMultiZip4s    = ''
        self.sOtherResult   = ''
        self.sOtherBegin    = ''
        self.sOtherEnd      = ''
        self.sUnvailable    = ''
        self.sFieldAdd      = ''
        self.sFieldCity     = ''
        self.sFieldState    = ''
        self.sFieldZip5     = ''
        self.sFieldSubmit   = ''
        self.sValueSubmit   = ''
        self.dMoreArgs      = {}
        #
    def getParams( self, sAdd1 = '', sCity = '', sStateCode = '', sZip5 = '' ):
        #
        dParams = {}
        #
        if self.sFieldAdd:   dParams[ self.sFieldAdd   ] = sAdd1
        if self.sFieldCity:  dParams[ self.sFieldCity  ] = sCity
        if self.sFieldState: dParams[ self.sFieldState ] = sStateCode
        if self.sFieldZip5:  dParams[ self.sFieldZip5  ] = sZip5
        #
        if self.sFieldSubmit and self.sValueSubmit:
            dParams[ self.sFieldSubmit ] = self.sValueSubmit
        #
        if self.dMoreArgs: dParams.update( self.dMoreArgs )
        #
        return dParams

    def _getAddressRight( self, sAdd1, sCity, sStateCode ):
        #
        # can override for different results
        #
        from Iter.AllVers import tMap
        from String.Get   import getUpper
        #
        return tMap( getUpper, ( sAdd1, sCity, sStateCode ) )
    #


class getHtmlThenZipPlus4( getParamsClass ):
    #
    def __init__( self ):
        #
        super( getHtmlThenZipPlus4, self ).__init__()
        #
    #
    def _HtmlThenZipPlus4( self, sAdd1, sCity, sStateCode, sZip5 = '', sHTML = '' ):
        #
        from String.Test    import getItemFoundInString
        from Collect.Test   import isListOrTuple
        #
        sAdd1, sCity, sStateCode = \
            self._getAddressRight( sAdd1, sCity, sStateCode )
        #
        if not sHTML:
            #
            dParams = self.getParams( sAdd1, sCity, sStateCode, sZip5 )
            #
            sHTML   = self._getHTML( **dParams )
            #
        #
        #from File.Write import MakeTemp
        #MakeTemp( sHTML )
        sZipPlus4 = sMsg = ''
        #
        bBeforeList = isListOrTuple( self.sBefore )
        #
        if bBeforeList:
            sBefore = getItemFoundInString( sHTML, self.sBefore )
            if not sBefore: sBefore = self.sBefore[0]
        else:
            sBefore = self.sBefore
            #
        #
        bNotFoundList  = isListOrTuple( self.sNotFound )
        bUnavailableL  = isListOrTuple( self.sUnvailable )
        #
        # print3( 'bNotFoundList:', bNotFoundList
        if bNotFoundList:
            sNotFound = getItemFoundInString( sHTML, self.sNotFound )
            if not sNotFound: sNotFound = self.sNotFound[0]
        else:
            sNotFound = self.sNotFound
        #
        if bUnavailableL:
            sUnvailable = getItemFoundInString( sHTML, self.sUnvailable )
            if not sUnvailable: sUnvailable = self.sUnvailable[0]
        else:
            sUnvailable = self.sUnvailable
        #
        if not sHTML:
            #
            sMsg = 'got nothing'
            #
        elif len( sHTML ) < 100:
            #
            sMsg = sHTML.strip()
            #
        elif sNotFound and sNotFound in sHTML:
            #
            sMsg = 'address not in %s database' % self.__class__.__name__
            #
        elif sUnvailable and sUnvailable in sHTML:
            #
            sMsg = sTempUnavailable % self.__class__.__name__
            #
        elif self.sOtherResult and self.sOtherResult in sHTML:
            #
            sLess = getTextAfter( sHTML, self.sOtherResult )
            #
            sMsg = 'Other result: %s' % \
                getTextWithin( sLess, self.sOtherBegin, self.sOtherEnd )
            #
        elif self.sBlocked and self.sBlocked in sHTML:
            #
            sMsg = '%s is blocked by the target server!' % self.__class__.__name__
            #
            self.iWantWait = 2 * self.iWantWait
            #
        elif sBefore in sHTML:
            #
            from sMail.Get import getZipPlus4, getZip5
            #
            sLess = getTextWithin( sHTML, sBefore, self.sAfter )
            #
            sZipPlus4 = getZipPlus4( sLess )
            #
            if not sZipPlus4:
                #
                sZip5 = getZip5( sLess )
                #
                sSay = sBefore
                #
                if sZip5:
                    # getDistricts looks for verbatim message
                    # getDistricts looks for verbatim message
                    sMsg = 'got Zip 5 %s but not Zip plus 4!' % sZip5
                    # getDistricts looks for verbatim message
                    # getDistricts looks for verbatim message
                else:
                    sMsg = 'did not get Zip plus 4 but found "%s"!' % \
                            sBefore
                    #
                    sOutFile = self._writeResults( sHTML )
                #
        elif self.sMultiZip4s and self.sMultiZip4s in sHTML:
            #
            sMsg = 'info provided returned more than one result'
            #
        else:
            #
            sOutFile = self._writeResults( sHTML )
            #
            sMsg = 'unknown, results in file "%s"' % sOutFile
            #
        #
        if not ( sZipPlus4 or sMsg): sMsg = 'the code set no msg!'
        #
        #print3( '_HtmlThenZipPlus4 sMsg:', sMsg
        return sZipPlus4, sMsg, sHTML

    def ZipPlus4( self, sAdd1, sCity, sStateCode, sZip5 = '', sHTML = '' ):
        #
        sZipPlus4, sMsg, sHTML = \
            self._HtmlThenZipPlus4( sAdd1, sCity, sStateCode, sZip5, sHTML )
        #
        #print3( 'ZipPlus4 sMsg:', sMsg
        #
        if self.bWantLog:
            #
            if sZipPlus4:
                #
                sLine = \
                    'success add: %s city: %s state: %s zip: %s' % \
                    ( sAdd1, sCity, sStateCode, sZip5 )
                #
            else:
                #
                sLine = \
                    'failure %s add: %s city: %s state: %s zip: %s' % \
                    ( sMsg, sAdd1, sCity, sStateCode, sZip5 )
                #
            self.doLog( sLine )
        #
        return sZipPlus4, sMsg


class getZipPlus4Getter( getterScraperClass, getHtmlThenZipPlus4 ):
    #
    def __init__( self, oSequencer, sLogFile = None ):
        #
        super( getZipPlus4Getter, self ).__init__( oSequencer, sLogFile = sLogFile )
        #
        getHtmlThenZipPlus4.__init__( self )
    #





class getZipPlus4Poster( PosterScraperClass, getHtmlThenZipPlus4 ):
    #
    def __init__( self, oSequencer, sLogFile = None ):
        #
        super( getZipPlus4Poster, self ).__init__( oSequencer, sLogFile = sLogFile )
        #
        getHtmlThenZipPlus4.__init__( self )
    #
    def _getAddressRight( self, sAdd1, sCity, sStateCode ):
        #
        # can override for different results
        #
        from string         import upper
        #
        from Iter.AllVers   import tMap
        from sMail.Abbrev   import getAbbreviate
        #
        sAdd1, sCity, sStateCode = tMap( upper, ( sAdd1, sCity, sStateCode ) )
        #
        sAdd1 = getAbbreviate( sAdd1 )
        #
        return sAdd1, sCity, sStateCode
    #



class SemaphoreCorpClass( getZipPlus4Poster ):
    #
    def __init__( self, oSequencer, sLogFile = None ):
        #
        super( SemaphoreCorpClass, self ).__init__( oSequencer, sLogFile = sLogFile )
        #
        self.sURL           = 'http://www.semaphorecorp.com/cgi/zp4.acgi$find'
        self.sReferer       = 'http://www.semaphorecorp.com/cgi/form.html'
        self.sBefore        = '<B>Your Input</B>'
        self.sAfter         = '</TABLE>'
        self.sNotFound      = 'Address not found'
        self.sBlocked       = 'bumped'
        self.sMultiZip4s    = ''
        self.sOtherResult   = 'Search warnings'
        self.sOtherBegin    = '">'
        self.sOtherEnd      = '</A><BR></TABLE>'
        self.sFieldAdd      = 'address'
        self.sFieldState    = 'state'
        self.sFieldCity     = 'city'
        self.sFieldState    = 'state'
        self.sFieldZip5     = 'ZIP'
        self.sFieldSubmit   = 'submit'
        self.sValueSubmit   = 'Find'
        self.dMoreArgs      = { "company" : '' }
        #
        self.iWantWait      = 60




class ZipCodesDotComClass( getZipPlus4Getter ):
    #
    def __init__( self, oSequencer, sLogFile = None ):
        #
        super( ZipCodesDotComClass, self ).__init__( oSequencer, sLogFile = sLogFile )
        #
        self.sURL        = 'http://www.zip-codes.com/search.asp?%s'
        self.sReferer    = 'http://www.zip-codes.com/'
        self.sBefore     = '<h3>Full Address in Standard Format:</h3>'
        self.sAfter      = '</table>'
        self.sNotFound   = \
            (   'Address Not Found.',
                'Invalid City',
                'Multiple addresses were found' )
        self.sBlocked    = 'bumped'
        self.sMultiZip4s    = ''
        self.sFieldAdd   = 'fld-address'
        self.sFieldCity  = 'fld-city2'
        self.sFieldState = 'fld-state2'
        self.sFieldp5    = ''
        self.dMoreArgs   = { 'srch.x' : '0', 'srch.y' : '0' }
        #
        self.iWantWait   = 10


class PostalServiceClass( getZipPlus4Poster ):
    #
    def __init__( self, oSequencer, sLogFile = None ):
        #
        super( PostalServiceClass, self ).__init__( oSequencer, sLogFile = sLogFile )
        #
        self.sURL           = 'http://zip4.usps.com/zip4/zcl_0_results.jsp'
        self.sReferer       = 'http://zip4.usps.com/zip4/welcome.jsp'
        self.sBefore        = ( 'Full Address in Standard Format',
                                'You Gave Us the Building Address',
                                'Matching Addresses' )
        self.sAfter         = "Mailing Industry Information"
        self.sNotFound      = ( 'The address was not found.',
                                'This address may be Non-Deliverable' )
        self.sBlocked       = 'blocked'
        self.sMultiZip4s    = 'We returned more than one result'
        self.sOtherResult   = 'We were unable to process your request.'
        self.sOtherBegin    = '<p class="mainRed">'
        self.sOtherEnd      = 'Please check the address below.'
        self.sUnvailable    = 'Temporarily Unavailable'
        self.sFieldAdd      = 'address1'
        self.sFieldCity     = 'city'
        self.sFieldState    = 'state'
        self.sFieldZip5     = 'zip5'
        self.sFieldSubmit   = 'submit'
        self.sValueSubmit   = "Find ZIP Code"
        self.dMoreArgs      = dict(
                                address2    = '',
                                visited     = '1',
                                pagenumber  = '0',
                                firmname    = '',
                                urbanization= '' )
        #
        self.iWantWait   = 10





class yahooBusinessClass( getZipPlus4Poster ):
    #
    def __init__( self, oSequencer, sLogFile = None ):
        #
        super( yahooBusinessClass, self ).__init__( oSequencer, sLogFile = sLogFile )
        #
        self.sURL           = 'http://smallbusiness.yahoo.com/resources/zipCodeLookup.php?result=yes'
        self.sReferer       = 'http://smallbusiness.yahoo.com/r-zipCodeLookup'
        self.sBefore        = 'The zip code you requested is'
        self.sAfter         = 'For this address:'
        self.sNotFound      = ( 'The address was not found.',
                                'unable to find a zip code associated' )
        self.sBlocked       = 'blocked'
        self.sMultiZip4s    = ''
        self.sOtherResult   = 'We were unable to process your request.'
        self.sOtherBegin    = '<p class="mainRed">'
        self.sOtherEnd      = 'Please check the address below.'
        self.sFieldAdd      = 'addr'
        self.sFieldCity     = 'csz'
        self.sFieldState    = ''
        self.sFieldZip5     = ''
        self.sFieldSubmit   = 'submit'
        self.sValueSubmit   = "Search"
        self.dMoreArgs      = { 'country' : 'us' }
        self.iWantWait      = 10
        #
    def _getAddressRight( self, sAdd1, sCity, sStateCode ):
        #
        # can override for different results
        #
        sCity       = ', '.join( ( sCity, sStateCode ) )
        sStateCode  = ''
        #
        return sAdd1, sCity, sStateCode



class getCityStateClass( getParamsClass ):
    #
    def __init__( self ):
        #
        super( getCityStateClass, self ).__init__()
        #
    #
    def _getHtmlThenCityState( self, sZip5 ):
        #
        from String.Test    import getItemFoundInString
        from Collect.Test   import isListOrTuple
        #
        dParams = self.getParams( sZip5 = sZip5 )
        #
        sHTML   = self._getHTML( **dParams )
        #
        sCity = sState = sMsg = ''
        #
        bSuccess = self.getSuccess( sHTML )
        #
        # print3( 'bSuccess:', bSuccess
        #
        bNotFoundList = isListOrTuple( self.sNotFound )
        #
        if bNotFoundList:
            sNotFound = getItemFoundInString( sHTML, self.sNotFound )
            if not sNotFound: sNotFound = self.sNotFound[0]
        else: sNotFound = self.sNotFound
        #
        if not sHTML:
            #
            sMsg = 'got nothing'
            #
        elif len( sHTML ) < 100:
            #
            sMsg = sHTML
            #
        elif sNotFound and sNotFound in sHTML:
            #
            sMsg = 'not valid; %s' % sNotFound
            #
        elif self.sOtherResult and self.sOtherResult in sHTML:
            #
            sLess = getTextAfter( sHTML, self.sOtherResult )
            #
            sMsg = 'Other result: %s' % \
                getTextWithin( sLess, self.sOtherBegin, self.sOtherEnd )
            #
        elif self.sBlocked and self.sBlocked in sHTML:
            #
            sMsg = '%s is blocked by the target server!' % self.__class__.__name__
            #
            self.iWantWait = 2 * self.iWantWait
            #
        elif self.sUnvailable and self.sUnvailable in sHTML:
            #
            sMsg = 'temporarily unavailable:  %s' % self.__class__.__name__
            #
        elif bSuccess:
            #
            sCity, sState, sMsg = \
                self.fGetCityState(
                    sHTML,
                    self.sSuccess,     self.sBeyond,
                    self.sCityBefore,  self.sCityAfter,
                    self.sStateBefore, self.sStateAfter,
                    self.fFilterCities )
            #
            if sCity and sState:    pass
            elif sMsg:              pass
            else:
                #
                sMsg = 'did not get city state but found "%s"!' % self.sSuccess
                #
                sOutFile = self._writeResults( sHTML )
                #
        else:
            #
            sOutFile = self._writeResults( sHTML )
            #
            sMsg = 'unknown, results in file "%s"' % sOutFile
            #
        #
        if not ( sCity or sState or sMsg): sMsg = 'the code set no msg!'
        #
        return sCity, sState, sMsg, sHTML


    def getCityState( self, sZip5 ):
        #
        sCity, sState, sMsg, sHTML= \
            self._getHtmlThenCityState( sZip5 )
        #
        if self.bWantLog:
            #
            if sMsg:
                #
                sLine = 'failure %s zip: %s' % ( sMsg, sZip5 )
                #
            else:
                #
                sLine = \
                    'success zip: %s' % sZip5
                #
            self.doLog( sLine )
        #
        return sCity, sState, sMsg
        #

    def getSuccess( self, sHTML ):
        #
        return self.sSuccess in sHTML


class getCityStateOffZipGetter( getterScraperClass, getCityStateClass ):
    #
    def __init__( self, oSequencer, sLogFile = None ):
        #
        super( getCityStateOffZipGetter, self ).__init__( oSequencer, sLogFile = sLogFile )
        #
        getCityStateClass.__init__( self )
        #
        self.sURL           = ''
        self.sReferer       = ''
        self.sSuccess       = ''
        self.sCityBefore    = ''
        self.sCityAfter     = ''
        self.sStateBefore   = ''
        self.sStateAfter    = ''
        self.sBeyond        = ''
        self.fFilterCities  = None
        self.fGetCityState  = _getCityStateOffHtmlNoTable
        self.sNotFound      = ''
        self.sBlocked       = ''
        self.sOtherResult   = ''
        self.sOtherBegin    = ''
        self.sOtherEnd      = ''
        self.sFieldAdd      = ''
        self.sFieldCity     = ''
        self.sFieldState    = ''
        self.sFieldZip5     = ''
        self.dMoreArgs      = {}
        #


class getCityStateOffZipPoster( PosterScraperClass, getCityStateClass ):
    #
    def __init__( self, oSequencer, sLogFile = None ):
        #
        super( getCityStateOffZipPoster, self ).__init__( oSequencer, sLogFile = sLogFile )
        #
        getCityStateClass.__init__( self )
        #
        self.sURL           = ''
        self.sReferer       = ''
        self.sSuccess       = ''
        self.sCityBefore    = ''
        self.sCityAfter     = ''
        self.sStateBefore   = ''
        self.sStateAfter    = ''
        self.sBeyond        = ''
        self.fFilterCities  = None
        self.fGetCityState  = _getCityStateOffHtmlNoTable
        self.sNotFound      = ''
        self.sBlocked       = ''
        self.sOtherResult   = ''
        self.sOtherBegin    = ''
        self.sOtherEnd      = ''
        self.sFieldAdd      = ''
        self.sFieldCity     = ''
        self.sFieldState    = ''
        self.sFieldZip5     = ''
        self.sFieldSubmit   = 'submit'
        self.sValueSubmit   = ""
        self.dMoreArgs      = {}
        #


def _getCityStateOffHtmlNoTable(
        sHTML,
        sSuccess,     sBeyond,
        sCityBefore,  sCityAfter,
        sStateBefore, sStateAfter,
        fFilterCities ):
    #
    # can be overridden
    #
    sCity, sState, sMsg = '', '', ''
    #
    sLess   = getTextWithin(  sHTML, sSuccess,     sBeyond     )
    #
    sCity   = getTextWithin(  sLess, sCityBefore,  sCityAfter  )
    #
    sLess   = getTextAfter(
                getTextAfter( sLess, sCityBefore), sCityAfter  )
    #
    sState  = getTextWithin(  sLess, sStateBefore, sStateAfter )
    #
    return sCity.title(), sState.upper(), sMsg


def _getCityStateOffHtmlTable(
        sHTML,
        sSuccess,     sBeyond,
        sCityBefore,  sCityAfter,
        sStateBefore, sStateAfter,
        fFilterCities ):
    #
    from Collect.Get    import getSequencePairsThisWithNext
    from Iter.AllVers   import lFilter
    from sMail.Abbrev   import setMPSA, dCodesStates
    from String.Get     import getStringsBetDelims
    #
    # abstract class may be overridden
    #
    sCity, sState, sMsg = '', '', ''
    #
    sLess   = getTextWithin( sHTML, sSuccess, sBeyond )
    #
    tCityStates = getSequencePairsThisWithNext(
                    getStringsBetDelims( sLess, sCityBefore, sCityAfter ) )
    #
    lCities     = [ t[0] for t in tCityStates if t[1] in dCodesStates ]
    lStates     = [ t[1] for t in tCityStates if t[1] in dCodesStates ]
    #
    if fFilterCities:
        #
        lCities = lFilter( fFilterCities, lCities )
        #
    #
    if lCities: sCity = ', '.join( lCities )
    #
    if lStates: sState = lStates[0]
    #
    lMilitary   = [ t[1] for t in tCityStates if t[1] in setMPSA ]
    #
    if lMilitary: sMsg = 'military zip'
    elif not ( sCity and sState ): sMsg = 'failed to extract city & state'
    #
    return sCity.title(), sState.upper(), sMsg



class ZipCodeWorldFetcher( getCityStateOffZipPoster ):
    #
    def __init__( self, oSequencer, sLogFile = None ):
        #
        super( ZipCodeWorldFetcher, self ).__init__( oSequencer, sLogFile = sLogFile )
        #
        self.sURL           = 'http://www.zipcodeworld.com/lookup.asp'
        self.sReferer       = 'http://www.zipcodeworld.com/lookup.asp?country=1'
        self.sSuccess       = 'ZIP_CODE'
        self.sCityBefore    = '<td class="fontblackregular" align="center" bgcolor="#CCCCCC">'
        self.sCityAfter     = '</td>'
        self.sStateBefore   = '<td class="fontblackregular" align="center" bgcolor="#FFFFFF">'
        self.sStateAfter    = '</td>'
        self.sBeyond        = 'AREA_CODE'
        self.sNotFound      = 'not found in database. Please try again.'
        self.sBlocked       = ''
        self.sOtherResult   = ''
        self.sOtherBegin    = ''
        self.sOtherEnd      = ''
        self.sFieldZip5     = 'code'
        self.sFieldSubmit   = 'submit'
        self.sValueSubmit   = "Search"
        self.dMoreArgs      = \
                { 'country' : '1', 'city' : '', 'area' : '', 'county' : '' }




class PeopleFinderFetcher( getCityStateOffZipGetter ):
    #
    def __init__( self, oSequencer, sLogFile = None ):
        #
        super( PeopleFinderFetcher, self ).__init__( oSequencer, sLogFile = sLogFile )
        #
        self.sURL           = 'http://www.peoplefinder.com/results.php?%s'
        self.sReferer       = 'http://www.peoplefinder.com/zipcodelookup.php'
        self.sSuccess       = '>TIME ZONE</span>'
        self.sCityBefore    = '<td class="F1">'
        self.sCityAfter     = '</td>'
        self.sStateBefore   = '<td class="F1">'
        self.sStateAfter    = '</td>'
        self.sBeyond        = '>Prev</span>&nbsp;<span'
        self.fGetCityState  = _getCityStateOffHtmlTable
        self.sNotFound      = 'Invalid Zip Code'
        self.sBlocked       = ''
        self.sOtherResult   = ''
        self.sOtherBegin    = ''
        self.sOtherEnd      = ''
        self.sFieldZip5     = 'qz'
        self.dMoreArgs      = { 'ReportType' : '42', 'qi' : '0', 'qk' : '100' }
        #


class ArulJohnFetcher( getCityStateOffZipPoster ):
    #
    def __init__( self, oSequencer, sLogFile = None ):
        #
        super( ArulJohnFetcher, self ).__init__( oSequencer, sLogFile = sLogFile )
        #
        self.sURL           = 'http://aruljohn.com/zip.php'
        self.sReferer       = 'http://aruljohn.com/zip.php'
        self.sSuccess       = '<p>Results for zip code <b>'
        self.sCityBefore    = '</b></p>'
        self.sCityAfter     = ','
        self.sStateBefore   = ' '
        self.sStateAfter    = '</h2>'
        self.sBeyond        = '<table class="content-table">'
        self.sNotFound      = 'Invalid Zip Code, please try again'
        self.sBlocked       = ''
        self.sOtherResult   = ''
        self.sOtherBegin    = ''
        self.sOtherEnd      = ''
        self.sFieldZip5     = ''
        self.sFieldSubmit   = 'submit'
        self.sValueSubmit   = "resolve"
        self.dMoreArgs      = {}
        #



class YellowPagesFetcher( getCityStateOffZipGetter ):
    #
    def __init__( self, oSequencer, sLogFile = None ):
        #
        super( YellowPagesFetcher, self ).__init__( oSequencer, sLogFile = sLogFile )
        #
        self.sURL           = 'http://www.yellowpages.com/findgeo/zip?%s'
        self.sReferer       = 'http://www.yellowpages.com/findaperson/zip'
        self.sSuccess       = '<div id="zip-info">'
        self.sCityBefore    = '<h3>'
        self.sCityAfter     = ','
        self.sStateBefore   = ' '
        self.sStateAfter    = '</h3>'
        self.sBeyond        = '<table>'
        self.sNotFound      = "We didn't find any results for"
        self.sBlocked       = ''
        self.sOtherResult   = ''
        self.sOtherBegin    = ''
        self.sOtherEnd      = ''
        self.sFieldZip5     = 'fap[zip]'
        self.dMoreArgs      = { 'fap[searchtype]' : 'zip' }
        #




class SimplyZipCodesFetcher( getCityStateOffZipPoster ):
    #
    def __init__( self, oSequencer, sLogFile = None ):
        #
        super( SimplyZipCodesFetcher, self ).__init__( oSequencer, sLogFile = sLogFile )
        #
        self.sURL           = 'http://www.simplyzipcodes.com/zclookup.php'
        self.sReferer       = 'http://www.simplyzipcodes.com/'
        self.sSuccess       = 'Enter Zip Code: &nbsp; <input type="text" name'
        self.sCityBefore    = '<TD>'
        self.sCityAfter     = '&nbsp;</TD>'
        self.sStateBefore   = '<TD>'
        self.sStateAfter    = '&nbsp;</TD>'
        self.sBeyond        = '</table>'
        self.fGetCityState  = _getCityStateOffHtmlTable
        self.fFilterCities  = self._CityFilter
        self.sNotFound      = 'Zip Code Does Not Exist'
        self.sBlocked       = ''
        self.sOtherResult   = ''
        self.sOtherBegin    = ''
        self.sOtherEnd      = ''
        self.sFieldZip5     = "zipLookup"
        self.sFieldSubmit   = 'Submit'
        self.sValueSubmit   = "Search"
        self.dMoreArgs      = { "SMT" : "TRUE" }
        #
    def _CityFilter( self, sCity ): return not '/' in sCity



class ESRISegmentsFetcher( getCityStateOffZipGetter ):
    #
    def __init__( self, oSequencer, sLogFile = None ):
        #
        super( ESRISegmentsFetcher, self ).__init__( oSequencer, sLogFile = sLogFile )
        #
        self.sURL           = 'http://www.arcwebservices.com/services/servlet/EBIS_Reports?%s'
        self.sReferer       = 'http://www.esri.com/data/esri_data/tapestry.html'
        self.sSuccess       = 'Post Office:'
        self.sCityBefore    = '<div class="repHeader">'
        self.sCityAfter     = ','
        self.sStateBefore   = ' '
        self.sStateAfter    = '</div></td>'
        self.sBeyond        = 'Top Tapestry Segments</th>'
        self.sNotFound      = 'available as ad hoc data, in report format from'
        self.sBlocked       = ''
        self.sOtherResult   = ''
        self.sOtherBegin    = ''
        self.sOtherEnd      = ''
        self.sFieldAdd      = ''
        self.sFieldCity     = ''
        self.sFieldState    = ''
        self.sFieldZip5     = 'zipcode'
        self.dMoreArgs      = {
            'serviceName' : "FreeZip",
            'errorURL'      : "http://www.esri.com/data/esri_data/tapestry.html" }
        #


class getZipsDotComFetcher( getCityStateOffZipGetter ):
    #
    def __init__( self, oSequencer, sLogFile = None ):
        #
        super( getZipsDotComFetcher, self ).__init__( oSequencer, sLogFile = sLogFile )
        #
        self.sURL           = 'http://www.getzips.com/CGI-BIN/ziplook.exe?%s'
        self.sReferer       = 'http://www.getzips.com/zip.htm'
        self.sSuccess       = 'CITY AND STATE'
        self.sCityBefore    = '<TD WIDTH="50%" VALIGN=TOP><P>'
        self.sCityAfter     = ','
        self.sStateBefore   = ' '
        self.sStateAfter    = '</TD>'
        self.sBeyond        = '</BODY>'
        self.fFilterCities  = self._CityFilter
        self.sNotFound      = 'No matching zip codes found.'
        self.sBlocked       = ''
        self.sUnvailable    = 'Zip Express and have this lookup capability available at all times!'
        self.sOtherResult   = ''
        self.sOtherBegin    = ''
        self.sOtherEnd      = ''
        self.sFieldAdd      = ''
        self.sFieldCity     = ''
        self.sFieldState    = ''
        self.sFieldZip5     = 'Zip'
        self.dMoreArgs      = { 'What' : "1", "Submit" : "Look It Up" }
        #

    def getSuccess( self, sHTML ):
        #
        sLess = getTextWithin( sHTML, self.sSuccess, self.sBeyond )
        #
        bCityRow = '<TR>' in sLess
        #
        return bCityRow

    def _CityFilter( self, sCity ): return sCity != 'CITY AND STATE'



class AresLlcDotComFetcher( getCityStateOffZipPoster ):
    #
    def __init__( self, oSequencer, sLogFile = None ):
        #
        super( AresLlcDotComFetcher, self ).__init__( oSequencer, sLogFile = sLogFile )
        #
        self.sURL           = 'http://www.aresllc.com/zip-codes-finder/search.php'
        self.sReferer       = 'http://www.aresllc.com/zip-codes-finder/'
        self.sSuccess       = "<div class='MapArea'>"
        self.sCityBefore    = '<h1>Map of '
        self.sCityAfter     = ','
        self.sStateBefore   = ' '
        self.sStateAfter    = '</h1><p><strong>'
        self.sBeyond        = '</div>'
        self.sNotFound      = 'There were no results.'
        self.sBlocked       = ''
        self.sOtherResult   = ''
        self.sOtherBegin    = ''
        self.sOtherEnd      = ''
        self.sFieldAdd      = ''
        self.sFieldCity     = ''
        self.sFieldState    = ''
        self.sFieldZip5     = 'SearchTerm'
        self.sFieldSubmit   = 'submit'
        self.sValueSubmit   = "Zip Code Search"
        self.dMoreArgs      = {}
        #



class ZipSkinnyFetcher( getCityStateOffZipGetter ):
    #
    def __init__( self, oSequencer, sLogFile = None ):
        #
        super( ZipSkinnyFetcher, self ).__init__( oSequencer, sLogFile = sLogFile )
        #
        self.sURL           = 'http://zipskinny.com/index.php?%s'
        self.sReferer       = 'http://zipskinny.com/'
        self.sSuccess       = 'CONTENT="Demographic profile for ZIP Code'
        self.sCityBefore    = ' in '
        self.sCityAfter     = ','
        self.sStateBefore   = ' '
        self.sStateAfter    = '.">'
        self.sBeyond        = '<META NAME="Keywords" CONTENT="'
        self.sNotFound      = 'We do not have any information for this ZIP'
        self.sBlocked       = ''
        self.sOtherResult   = ''
        self.sOtherBegin    = ''
        self.sOtherEnd      = ''
        self.sFieldZip5     = 'zip'
        self.dMoreArgs      = { "submit" : "get the skinny" }
        #


class Zip2TaxFetcher( getCityStateOffZipGetter ):
    #
    # 10 per day limit!
    #
    def __init__( self, oSequencer, sLogFile = None ):
        #
        super( Zip2TaxFetcher, self ).__init__( oSequencer, sLogFile = sLogFile )
        #
        self.sURL           = 'http://www.zip2tax.com/z2t_lookup.asp?%s'
        self.sReferer       = 'http://zip2tax.com/'
        self.sSuccess       = 'altOn(this, "Sales Tax Breakout'
        self.sCityBefore    = ' For '
        self.sCityAfter     = ','
        self.sStateBefore   = ' '
        self.sStateAfter    = '",'
        self.sBeyond        = '>State of'
        self.sNotFound      = ( 'Zip Code you have entered does not exist.',
                                'No Sales Tax for APO/FPO/DPO Addresses' )
        self.sBlocked       = ''
        self.sOtherResult   = ''
        self.sOtherBegin    = ''
        self.sOtherEnd      = ''
        self.sFieldZip5     = 'inputZip'
        self.dMoreArgs      = {}
        #


def _hasCommaSpace( s ):
    #
    return len( s.split( ', ' ) ) > 1

def _getTextBeforeComma( s ):
    #
    from String.Get import getTextBefore
    #
    return getTextBefore( s, ',' )



if __name__ == "__main__":
    #
    from time           import time
    #
    from six            import print_ as print3
    #
    from Utils.Result   import sayTestResult
    #
    sLog = 'GetInfoClasses'
    print3( 'start/end log in %s.log' % sLog )
    #
    print3( 'this takes a while because the must be a pause between requests ...' )
    #
    lProblems = []
    #
    sZipValid   = '98103'
    sZipInvalid = '99999'
    sZipMil     = '09007'
    #
    sLog = 'GetInfoClasses'
    #
    oGetUspsDotCom      = PostalServiceClass(    oSequencer, sLogFile = sLog )
    oGetZipCodesDotCom  = ZipCodesDotComClass(   oSequencer, sLogFile = sLog )
    oGetSemaphoreCorp   = SemaphoreCorpClass(    oSequencer, sLogFile = sLog )
    oGetYahooBusiness   = yahooBusinessClass(    oSequencer, sLogFile = sLog )
    #
    # fetchers get city & state from zip
    oGetZipCodeWorld    = ZipCodeWorldFetcher(   oSequencer, sLogFile = sLog )
    oPeopleFinder       = PeopleFinderFetcher(   oSequencer, sLogFile = sLog )
    # oYellowPages        = YellowPagesFetcher(    oSequencer, sLogFile = sLog )
    # oSimplyZipCodes     = SimplyZipCodesFetcher( oSequencer, sLogFile = sLog )
    oESRISegments       = ESRISegmentsFetcher(   oSequencer, sLogFile = sLog )
    oGetZipsDotCom      = getZipsDotComFetcher(  oSequencer, sLogFile = sLog )
    oAresLlcDotCom      = AresLlcDotComFetcher(  oSequencer, sLogFile = sLog )
    oZipSkinnyDotCom    = ZipSkinnyFetcher(      oSequencer, sLogFile = sLog )
    oZip2TaxDotCom      = Zip2TaxFetcher(        oSequencer, sLogFile = sLog )
    #
    #oArulJohn           = ArulJohnFetcher()
    #
    sZipPlus4, sMsg = \
        oGetSemaphoreCorp.ZipPlus4( '2130 Solar Lane', 'SAN MARCOS', 'CA' )
    #
    if ( sZipPlus4, sMsg ) != \
            ('', 'address not in SemaphoreCorpClass database' ):
        #
        lProblems.append( 'SemaphoreCorpClass() invalid address' )
        lProblems.append( '  %s' % sMsg )
        #
        #from File.Write import MakeTemp
        #MakeTemp( sHTML )
    #
    #
    sZipPlus4, sMsg = \
        oGetUspsDotCom.ZipPlus4( '870 5TH AVE', 'New York', 'NY' )
    #
    if sZipPlus4 != '10065-4953':
        #
        lProblems.append( 'oGetUspsDotCom() multi zip4 870 5TH AVE New York NY' )
        lProblems.append( '  %s' % sMsg )
        lProblems.append( '  %s' % sZipPlus4 )
        #
    #
    sCity, sState, sMsg = oZip2TaxDotCom.getCityState( sZipValid )
    #
    if ( sCity, sState, sMsg ) != ( 'Seattle', 'WA', '' ):
        #
        lProblems.append( 'oZip2TaxDotCom.getCityState() valid zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
        #
    #
    sCity, sState, sMsg = oZipSkinnyDotCom.getCityState( sZipValid )
    #
    if ( sCity, sState, sMsg ) != ( 'Seattle', 'WA', '' ):
        #
        lProblems.append( 'oZipSkinnyDotCom.getCityState() valid zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
        #
    #
    sZipPlus4, sMsg = \
        oGetZipCodesDotCom.ZipPlus4( '1231 N 48th St', 'Seattle', 'WA' )
    #
    if ( sZipPlus4, sMsg ) != ('98103-6625', ''):
        #
        lProblems.append( 'ZipCodesDotComClass() valid address' )
        #
    #
    sZipPlus4, sMsg = \
        oGetYahooBusiness.ZipPlus4( '1231 N 48th St', 'Seattle', 'WA' )
    #
    if ( sZipPlus4, sMsg ) != ('98103-6625', ''):
        #
        lProblems.append( 'oGetYahooBusiness() valid address' )
        #
    #
    sCity, sState, sMsg = oAresLlcDotCom.getCityState( sZipValid )
    #
    if ( sCity, sState, sMsg ) != ( 'Seattle', 'WA', '' ):
        #
        lProblems.append( 'oAresLlcDotCom.getCityState() valid zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
        #
    #
    sZipPlus4, sMsg = \
        oGetUspsDotCom.ZipPlus4( '320 E JOHNSON ST', 'Madison', 'WI' )
    #
    if sZipPlus4 != '53703-2219':
        #
        lProblems.append( 'oGetUspsDotCom() multi zip4 320 E JOHNSON ST Madison WI' )
        lProblems.append( '  %s' % sMsg )
        lProblems.append( '  %s' % sZipPlus4 )
        #
    #
    sCity, sState, sMsg = oGetZipsDotCom.getCityState( sZipValid )
    #
    if ( sCity, sState, sMsg ) != ( 'Seattle', 'WA', '' ):
        #
        lProblems.append( 'oGetZipsDotCom.getCityState() valid zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
        #
    #
    sCity, sState, sMsg = oESRISegments.getCityState( sZipValid )
    #
    if ( sCity, sState, sMsg ) != ( 'Seattle', 'WA', '' ):
        #
        lProblems.append( 'oESRISegments.getCityState() valid zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
        #
    #
    sCity, sState, sMsg = oPeopleFinder.getCityState( sZipValid )
    #
    if ( sCity, sState, sMsg ) != \
            ( 'Seattle', 'WA', '' ):
        #
        lProblems.append( 'oPeopleFinder.getCityState() valid zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
        #
    #
    '''
    sCity, sState, sMsg = oSimplyZipCodes.getCityState( sZipValid )
    #
    if ( sCity, sState, sMsg ) != \
            ( 'Seattle', 'WA', '' ):
        #
        lProblems.append( 'oSimplyZipCodes.getCityState() valid zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
        #
    '''
    #
    sZipPlus4, sMsg = oGetUspsDotCom.ZipPlus4(
        '1231 N 48th St',
        'Seattle', 'WA', '98103' )
    #
    if sZipPlus4 != '98103-6625':
        #
        lProblems.append( 'oGetUspsDotCom.ZipPlus4() correct address' )
        #
    #
    '''
    sCity, sState, sMsg = oYellowPages.getCityState( sZipValid )
    #
    if ( sCity, sState, sMsg ) != \
            ( 'Seattle', 'WA', '' ):
        #
        lProblems.append( 'oYellowPages.getCityState() valid zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
        #
    '''
    #
    sCity, sState, sMsg = oGetZipCodeWorld.getCityState( sZipValid )
    #
    if ( sCity, sState, sMsg ) != \
            ( 'Seattle', 'WA', '' ):
        #
        lProblems.append( 'oGetZipCodeWorld.getCityState() valid zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
        #
    #
    sCity, sState, sMsg = oPeopleFinder.getCityState( sZipMil )
    #
    if ( sCity, sState, sMsg ) != \
            ( '', '', 'military zip' ):
        #
        lProblems.append( 'oPeopleFinder.getCityState() military zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
        #
    #
    sCity, sState, sMsg = oZipSkinnyDotCom.getCityState( sZipMil )
    #
    if ( sCity, sState, sMsg ) != \
        ( '', '', 'not valid; We do not have any information for this ZIP' ):
        #
        lProblems.append( 'oZipSkinnyDotCom.getCityState() military zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
        #
    #
    sCity, sState, sMsg = oGetZipCodeWorld.getCityState( sZipMil )
    #
    if ( sCity, sState, sMsg ) != \
            ( "Apo", "AE", '' ):
        #
        lProblems.append( 'oGetZipCodeWorld.getCityState() military zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
        #
    #
    sCity, sState, sMsg = oZip2TaxDotCom.getCityState( sZipMil )
    #
    if ( sCity, sState, sMsg ) != ( '', '', "not valid; No Sales Tax for APO/FPO Addresses" ):
        #
        lProblems.append( 'oZipSkinnyDotCom.getCityState() military zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
        #
    #
    sZipPlus4, sMsg = \
        oGetZipCodesDotCom.ZipPlus4( '2130 Solar Lane', 'SAN MARCOS', 'CA' )
    #
    if ( sZipPlus4, sMsg ) != \
            ('', 'address not in ZipCodesDotComClass database' ):
        #
        lProblems.append( 'ZipCodesDotComClass() invalid address' )
        #
    #
    sZipPlus4, sMsg = \
        oGetUspsDotCom.ZipPlus4(
            '40A RICHARDSON ST',
            'BROOKLYN',  'NY', "" )
    #
    if sMsg != 'address not in PostalServiceClass database':
        #
        lProblems.append( 'address not in PostalServiceClass database' )
        lProblems.append( '  %s' % sMsg )
        #
    #
    '''
    sCity, sState, sMsg = oSimplyZipCodes.getCityState( sZipInvalid )
    #
    if ( sCity, sState, sMsg ) != \
            ( '', '', 'something not found' ):
        #
        lProblems.append( 'oSimplyZipCodes.getCityState() invalid zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
        #
    '''
    #
    sCity, sState, sMsg = oESRISegments.getCityState( sZipInvalid )
    #
    if ( sCity, sState, sMsg ) != \
        ( '', '', 'not valid; available as ad hoc data, in report format from' ):
        #
        lProblems.append( 'oESRISegments.getCityState() invalid zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
        #
    #
    sCity, sState, sMsg = oAresLlcDotCom.getCityState( sZipInvalid )
    #
    if ( sCity, sState, sMsg ) != \
            ( '', '', 'not valid; There were no results.' ):
        #
        lProblems.append( 'oAresLlcDotCom.getCityState() invalid zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
        #
    #
    sCity, sState, sMsg = oGetZipsDotCom.getCityState( sZipInvalid )
    #
    if ( sCity, sState, sMsg ) != \
            ( '', '', 'not valid; No matching zip codes found.' ):
        #
        lProblems.append( 'oGetZipsDotCom.getCityState() invalid zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
        #
    #
    '''
    sCity, sState, sMsg = oYellowPages.getCityState( sZipInvalid )
    #
    if ( sCity, sState, sMsg ) != \
            ( '', '', 'something not found' ):
        #
        lProblems.append( 'oYellowPages.getCityState() invalid zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
        #
    '''
    #
    sZipPlus4, sMsg = \
        oGetUspsDotCom.ZipPlus4(
            '2130 Solar Lane',
            'San Marcos',  'CA', "92069" )
    #
    if sMsg != 'address not in PostalServiceClass database':
        #
        lProblems.append( 'oGetUspsDotCom.ZipPlus4() San Marcos invalid address' )
        lProblems.append( '  %s' % sMsg )
        #
    #
    #
    #
    sCity, sState, sMsg = oZipSkinnyDotCom.getCityState( sZipInvalid)
    #
    if ( sCity, sState, sMsg ) != \
        ( '', '', 'not valid; We do not have any information for this ZIP' ):
        #
        lProblems.append( 'oZipSkinnyDotCom.getCityState() invalid zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
    #
    sCity, sState, sMsg = oZip2TaxDotCom.getCityState( sZipInvalid )
    #
    if ( sCity, sState, sMsg ) != \
        ( '', '', 'not valid; Zip Code you have entered does not exist.' ):
        #
        lProblems.append( 'oZip2TaxDotCom.getCityState() invalid zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
        #
    #
    sCity, sState, sMsg = oGetZipCodeWorld.getCityState( sZipInvalid )
    #
    if ( sCity, sState, sMsg ) != \
            ( "", "", 'not valid; not found in database. Please try again.' ):
        #
        lProblems.append( 'oGetZipCodeWorld.getCityState() invalid zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
        #
    #
    sZipPlus4, sMsg = \
        oGetYahooBusiness.ZipPlus4( '55 Ralston Avenue', 'Kenmore', 'NY' )
    #
    if ( sZipPlus4, sMsg ) != ('', 'address not in yahooBusinessClass database' ):
        #
        lProblems.append( 'oGetYahooBusiness() invalid address' )
        lProblems.append( '  %s' % sMsg )
        #
    #
    sCity, sState, sMsg = oPeopleFinder.getCityState( sZipInvalid )
    #
    if ( sCity, sState, sMsg ) != \
            ( '', '', 'not valid; Invalid Zip Code' ):
        #
        lProblems.append( 'oPeopleFinder.getCityState() invalid zip' )
        lProblems.append( '  "%s", "%s", "%s"' % ( sCity, sState, sMsg ) )
        #
    #
    sZipPlus4, sMsg = \
        oGetSemaphoreCorp.ZipPlus4( '1231 N 48th St', 'Seattle', 'WA' )
    #
    if ( sZipPlus4, sMsg ) != ('98103-6625', ''):
        #
        lProblems.append( 'SemaphoreCorpClass() valid address' )
        lProblems.append( '  %s' % sMsg )
        #
    #
    # down oGetSemaphoreCorp,
    #
    print3( 'Avg durations' )
    #
    l = []
    #
    for o in (  oGetUspsDotCom,
                oGetZipCodesDotCom,
                oGetYahooBusiness,
                oGetSemaphoreCorp,
                oGetZipCodeWorld,
                oPeopleFinder,
                oESRISegments,
                oGetZipsDotCom,
                oZipSkinnyDotCom,
                oAresLlcDotCom ):
        #       oSimplyZipCodes,
        #       oYellowPages,
        #
        sWait = str( o.getWaitDurationAndSeq() )
        fAvgDur = o.getAvgDuration()
        sName = o.__class__.__name__.ljust(21)
        #
        l.append( ( sWait, '%s %5.2f %s' % ( sName, fAvgDur, sWait ) ) )
    #
    l.sort()
    #
    for t in l: print3( t[1] )
    #
    sAdd1       = "720 Orange Grove Blvd."
    sCity       = "Pasadena"
    sStateCode  = "CA"
    sZip5       = '' # "91105-3522"
    #
    sHTML = '''<table width="635" border="0" cellspacing="0" cellpadding="0"
        summary="This table contains an error when the application is temporarily unavailable.">
        <tr>
            <td width="100"><img src="images/spacer.gif" height="40" width="100" alt="" border="0" /></td>
            <td width="435">
                <h1>Temporarily Unavailable</h1>
            </td>
            <td width="100"><img src="images/spacer.gif" height="40" width="100" alt="" border="0" /></td>
        </tr>
        <tr>
            <td width="100"><img src="images/spacer.gif" height="23" width="100" alt="" border="0" /></td>
            <td width="435">
                <span class="mainBold">SORRY!! The current application is temporarily unavailable.
            Sorry for any inconvenience, please try your transaction again or click on the
            following link and return to the ZIP Code Lookup landing page.</span>
            </td>'''
    #
    sZipPlus4, sMsg, sHTML = \
        oGetUspsDotCom._HtmlThenZipPlus4(
            sAdd1, sCity, sStateCode, sZip5, sHTML )
    #
    if sZipPlus4 or sMsg != 'temporarily unavailable: web site for PostalServiceClass':
        #
        lProblems.append( 'oGetUspsDotCom() temporarily unavailable' )
        #
    #
    sayTestResult( lProblems )
