#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions get geocodes
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
# Copyright 2012-2016 Rick Graves
#

'''
objects to fetch geocodes for addresses
 
 
 '''

from String.Transform   import getSwapper

from six                import print_ as print3
#
from Utils.Config       import getConfDict
from Web.Get2n3         import getPage, getPageForNoInternet

true    = True  # json uses lower case true/false
false   = False


dConf   = getConfDict( 'getGeocodes.conf' )

_sGotInternet = dConf['main'].get( 'gotinternet', 'Yes' )

if _sGotInternet == 'No':
    #
    oUsePageGetter = getPageForNoInternet
    #
else:
    #
    oUsePageGetter = getPage
    #

_dEvalError = {
    "status":'JSON eval error!',
    "ResultSet":{
        "ErrorMessage":"JSON eval error!",
        "Results": None } }

_dHttpError = {
    "status":'Web error!',
    "ResultSet":{
        "ErrorMessage":"Web error!",
        "Results": {} } }

class baseGeocodes( oUsePageGetter ):
    #
    def __init__( self,
            bUseCookie  = False,
            sUserAgent  = 'default',
            bAcceptGzip = False,
            sGeoService = 'specify here',
            sAddrKey    = 'address',
            sCityKey    = 'city',
            sCountyKey  = 'county',
            sStateKey   = 'state',
            sZipKey     = 'zip',
            sOverLimit  = '',
            **kwargs ):
        #
        iSecsPause      = 0
        #
        self.dConfService = {}
        self.sAddrKey     = sAddrKey
        self.sCityKey     = sCityKey
        self.sCountyKey   = sCountyKey
        self.sStateKey    = sStateKey
        self.sZipKey      = sZipKey
        self.sOverLimit   = sOverLimit
        self.sLastURL     = ''
        #
        self.dConfService = {}
        #
        if sGeoService in dConf:
            self.dConfService = dConf[sGeoService]
        #
        if 'iSecsPause' in kwargs:
            #
            iSecsPause = eval( kwargs['iSecsPause'] )
            #
        elif 'secondspause' in self.dConfService:
            #
            iSecsPause  = eval( self.dConfService['secondspause'] )
            #
        #
        super( baseGeocodes, self ).__init__(
                    bUseCookie  = bUseCookie,
                    sUserAgent  = sUserAgent,
                    bAcceptGzip = bAcceptGzip,
                    iSecsPause  = iSecsPause,
                    **kwargs )
        #
        self.iMaxPerDay = int( dConf[sGeoService].get( 'maxperday', 0 ) )
        #


    def _getParam( self, dParams, d, sLabelName, sKey ):
        #
        dConfService = self.dConfService
        #
        if sKey in d:
            dParams[ dConfService[ sLabelName ] ] = d[ sKey ]
        else:
            dParams[ dConfService[ sLabelName ] ] = ''
        
        
    def _getRequestURL( self, d ):
        #
        '''
        '''
        # "contact_id";"us_st_add";"us_st_add2";"us_city";"state";"zip_code"
        #
        dConfService = self.dConfService
        #
        sURL = dConfService['url']
        #
        dParams = {}
        #
        if 'ziplabel' in dConfService:
            #
            self._getParam( dParams, d, 'addresslabel',self.sAddrKey   )
            self._getParam( dParams, d, 'citylabel',   self.sCityKey   )
            self._getParam( dParams, d, 'countylabel', self.sCountyKey )
            self._getParam( dParams, d, 'statelabel',  self.sStateKey  )
            self._getParam( dParams, d, 'ziplabel',    self.sZipKey    )
            #
            #dParams[ dConfService['addresslabel'] ] = d[self.sAddrKey  ]
            #dParams[ dConfService['citylabel'   ] ] = d[self.sCityKey  ]
            #dParams[ dConfService['statelabel'  ] ] = d[self.sStateKey ]
            #dParams[ dConfService['ziplabel'    ] ] = d[self.sZipKey   ]
            #
        else:
            #
            # no county using this method
            #
            lAddressParts = [
                d[self.sAddrKey  ],
                d[self.sCityKey  ],
                d[self.sStateKey ],
                d[self.sZipKey   ] ]
            #
            sAddressParts = ', '.join( [ s for s in lAddressParts if s ] )
            #
            dParams[ dConfService['addresslabel'] ] = sAddressParts
            #
        #
        if 'useridlabel' in dConfService:
            #
            dParams[ dConfService['useridlabel'] ] = dConfService['userid']
        #
        if 'jsonlabel' in dConfService:
            #
            dParams[ dConfService['jsonlabel'] ] = dConfService['jsonparam']
        #
        if 'alsosendlabel' in dConfService:
            #
            dParams[ dConfService['alsosendlabel'] ] = dConfService['alsosend']
        #
        sParams = self.getParams( dParams )
        #
        self.sLastURL = '?'.join( ( sURL, sParams ) )
        #
        return self.sLastURL


    def getGeoCodes( self, d ):
        #
        from copy import deepcopy
        #
        sURL = self._getRequestURL( d )
        #
        sJSON, oReceiveHeaders, dResult = self.getHtmlAndResults( sURL )
        #
        sStatus, dResponse = 'unknown', {}
        #
        if dResult['sErrorCode'] or dResult['sReason']:
            #
            dResponse = deepcopy( _dHttpError )
            dReSet    = dResponse["ResultSet"]
            dReSet["Error"       ]       = dResult['sErrorCode']
            dReSet["ErrorMessage"]       = dResult['sReason'   ]
            dReSet["Results"]['Comment'] = dResult['sComment'  ]
            dReSet["Results"]['sURL'   ] = dResult['sRealURL'  ]
            #
        else:
            #
            try:
                #
                dResponse = eval( sJSON )
                #
                #print3( 'success' )
                #
            except Exception:
                #
                dResponse = deepcopy( _dEvalError )
                #
                dResponse["Results"] = sJSON
                #print3( 'Exception' )
                #
            #
        #
        if "ResultSet" in dResponse: # yahoo or error
            #
            dReSet = dResponse["ResultSet"]
            #
            if dReSet["ErrorMessage"] != 'No error':
                #
                sStatus = dReSet["ErrorMessage"]
                #
            else:
                #
                sStatus = 'OK'
                #
            #
        elif "status" in dResponse: # google
            #
            sStatus = dResponse["status"]
            #
        else: # invalid
            #
            pass
            #
        #
        if sStatus != 'OK':
            #
            sJSON = repr( dResponse )
            #
        #
        return sStatus, sJSON




class googleGeocodes( baseGeocodes ):
    #
    def __init__( self,
            sAddrKey    = 'address',
            sCityKey    = 'city',
            sStateKey   = 'state',
            sZipKey     = 'zip',
            sOverLimit  = 'OVER_QUERY_LIMIT',
            **kwargs ):
        #
        super( googleGeocodes, self ).__init__(
                sGeoService = 'google',
                sAddrKey    = sAddrKey,
                sCityKey    = sCityKey,
                sStateKey   = sStateKey,
                sZipKey     = sZipKey,
                sOverLimit  = sOverLimit,
                **kwargs )



class yahooGeocodes( baseGeocodes ):
    #
    def __init__( self,
            sAddrKey    = 'address',
            sCityKey    = 'city',
            sCountyKey  = 'county',
            sStateKey   = 'state',
            sZipKey     = 'zip',
            sOverLimit  = '?',
            **kwargs ):
        #
        super( yahooGeocodes, self ).__init__(
                sGeoService = 'yahoo',
                sAddrKey    = sAddrKey,
                sCityKey    = sCityKey,
                sCountyKey  = sCountyKey,
                sStateKey   = sStateKey,
                sZipKey     = sZipKey,
                sOverLimit  = sOverLimit,
                **kwargs )


# http://maps.googleapis.com/maps/api/geocode/json?address=1231+N+48th+St,+Seattle,+WA&sensor=false

_dGoogleExample = '''
{ "results" : [
      {
         "address_components" : [
            {
               "long_name" : "1231",
               "short_name" : "1231",
               "types" : [ "street_number" ]
            },
            {
               "long_name" : "N 48th St",
               "short_name" : "N 48th St",
               "types" : [ "route" ]
            },
            {
               "long_name" : "Wallingford",
               "short_name" : "Wallingford",
               "types" : [ "neighborhood", "political" ]
            },
            {
               "long_name" : "Seattle",
               "short_name" : "Seattle",
               "types" : [ "locality", "political" ]
            },
            {
               "long_name" : "King",
               "short_name" : "King",
               "types" : [ "administrative_area_level_2", "political" ]
            },
            {
               "long_name" : "Washington",
               "short_name" : "WA",
               "types" : [ "administrative_area_level_1", "political" ]
            },
            {
               "long_name" : "United States",
               "short_name" : "US",
               "types" : [ "country", "political" ]
            },
            {
               "long_name" : "98103",
               "short_name" : "98103",
               "types" : [ "postal_code" ]
            }
         ],
         "formatted_address" : "1231 N 48th St, Seattle, WA 98103, USA",
         "geometry" : {
            "location" : {
               "lat" : 47.6633570,
               "lng" : -122.3423260
            },
            "location_type" : "ROOFTOP",
            "viewport" : {
               "northeast" : {
                  "lat" : 47.66470598029149,
                  "lng" : -122.3409770197085
               },
               "southwest" : {
                  "lat" : 47.66200801970850,
                  "lng" : -122.3436749802915
               }
            }
         },
         "partial_match" : true,
         "types" : [ "street_address" ]
      }
   ],
   "status" : "OK"
}
'''

# http://where.yahooapis.com/geocode?appid=PqueyE7k&addr=1231+N+48th+St&city=Seattle&state= WA&flags=J

_dYahooExample = '''
{"ResultSet":{"version":"1.0","Error":0,"ErrorMessage":"No error","Locale":"us_US","Quality":10,"Found":1,
  "Results":
  [
  {"quality":87,
   "latitude":"47.663570",
   "longitude":"-122.342842",
   "offsetlat":"47.663437",
   "offsetlon":"-122.342842",
   "radius":4800,
   "name":"",
   "line1":"1231 N 48th St",
   "line2":"Seattle, WA  98103",
   "line3":"",
   "line4":"United States",
   "house":"1231",
   "street":"N 48th St",
   "xstreet":"",
   "unittype":"",
   "unit":"",
   "postal":"98103",
   "neighborhood":"",
   "city":"Seattle",
   "county":"King County",
   "state":"Washington",
   "country":"United States",
   "countrycode":"US",
   "statecode":"WA",
   "countycode":"","uzip":"98103","hash":"44EE6E2C68C182F4","woeid":12798947,"woetype":11}]}}
'''






if __name__ == "__main__":
    #
    from Dir.Get        import sTempDir
    from File.Write     import QuickDump
    from Numb.Test      import isNumber
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    kwargs = dict( 
        sAddrKey    = 'addr',
        sCityKey    = 'town',
        sCountyKey  = 'coun',
        sStateKey   = 'prov',
        sZipKey     = 'code' )
    #
    if _sGotInternet == 'No':
        #
        kwargs['uFakeResp'] = _dGoogleExample
        #
        oGoogle = googleGeocodes( **kwargs )
        #
        kwargs['uFakeResp'] = _dYahooExample
        #
        oYahoo  = yahooGeocodes(  **kwargs )
        #
    #
    else:
        oGoogle = googleGeocodes( **kwargs )
        oYahoo  = yahooGeocodes(  **kwargs )
    #
    if not ( oGoogle.iSecsPause and oYahoo.iSecsPause ):
        #
        lProblems.append( 'iSecsPause not set' )
        #
    #
    if not ( isNumber(oGoogle.iSecsPause) and isNumber(oYahoo.iSecsPause) ):
        #
        lProblems.append( 'iSecsPause set but not a number' )
        #
    #
    if not ( oGoogle.iMaxPerDay and oYahoo.iMaxPerDay ):
        #
        lProblems.append( 'iMaxPerDay not set' )
        #
    #
    if not ( isNumber(oGoogle.iMaxPerDay) and isNumber(oYahoo.iMaxPerDay) ):
        #
        lProblems.append( 'iMaxPerDay set but not a number' )
        #
    #
    
    #print3( 'oGoogle.iMaxPerDay:', oGoogle.iMaxPerDay )
    #print3( 'oYahoo.iMaxPerDay: ', oYahoo.iMaxPerDay  )
    d = dict(
        addr = '1231 N 48th Street',
        town = 'Seattle',
        prov = 'WA',
        code = '98103' )
    #
    sStatus, sJSON = oGoogle.getGeoCodes( d )
    #
    if _sGotInternet != 'No':
        #
        QuickDump(  sJSON,
                sTempDir, 'Google_getGeoCodes_response.json',
                bSayBytes = False )
    #
    if sStatus != 'OK':
        #
        lProblems.append( 'oGoogle.getGeoCodes( d )' )
        lProblems.append( sStatus )
        #
        if sStatus == 'unknown': print3( sJSON )
    #
    d = dict(
        addr = '1600 Pennsylvania Ave NW',
        town = 'Washington',
        prov = 'DC',
        code = '20500' )
    #
    sStatus, sJSON = oYahoo.getGeoCodes( d )
    #
    if _sGotInternet != 'No':
        #
        QuickDump(  sJSON,
                sTempDir, 'Yahoo_getGeoCodes_response.json',
                bSayBytes = False )
        #
        QuickDump( oYahoo.sLastURL,
                sTempDir, 'Yahoo_getGeoCodes_URL.txt',
                bSayBytes = False )
    #
    if sStatus != 'OK':
        #
        lProblems.append( 'oYahoo.getGeoCodes( d )' )
        lProblems.append( sStatus )
        #
    #
    sTrueFalseOrig = 'Is the assertion true or false?'
    sTrueFalseWant = 'Is the assertion True or False?'
    #
    #
    if False:
        #
        lProblems.append( 'someproblem()' )
        #
    #
    sayTestResult( lProblems )