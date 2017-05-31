#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions Address
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
'''

need working ftp server to test?

'''

from six.moves.urllib.parse import urlsplit, urlunsplit

def _getTopLevelDomainSets():
    #
    #
    # from http://www.iana.org/domains/root/db/#
    # updated last 08-06-23
    #
    # http://en.wikipedia.org/wiki/List_of_Internet_top-level_domains
    # updated last 2013-12-31
    #
    tTopLevelDomains = (
        'aero', 'arpa', 'asia',  'biz',  'cat', 'com',
        'coop', 'edu',  'gov',   'info', 'int', 'jobs',
        'mil',  'mobi', 'museum','name', 'net', 'org',
        'post', 'pro',  'tel',  'travel','xxx',
        'الجزائر',
        'বাংলা',
        '中国',
        '中國',
        'مصر',
        'გე',
        '香港',
        'الاردن',
        'қаз',
        'مليسيا',
        'мон',
        'المغرب',
        'عمان',
        'پاکستان',
        'فلسطين',
        'قطر',
        '',
        '',
        'рф',
        '',
        'срб',
        '新加坡',
        'சிங்கப்பூர்',
        '한국',
        'ලංකා',
        'இலங்கை',
        'سودان',
        'سوريا',
        '台湾',
        '台灣',
        'ไทย',
        'تونس',
        'укр',
        'امارات',
        'اليمن',
        )
    #
    # .co.th, .net.th, .or.th, .in.th, .ac.th, .go.th
    # http://www.thainic.net/
    #
    tMiniDomains = ( 'co', 'or', 'in', 'ac', 'go', 'ed' )
    #
    return frozenset( tTopLevelDomains ), frozenset( tMiniDomains )



setTopLevelDomains, setMiniDomains  = _getTopLevelDomainSets()



def getServerDomainOffURL( sHost ):
    #
    from Web.Test       import isDotQuad
    from Web.Country    import dCountryCodes
    #
    sScheme, sUser, sPassword, sHost, sPort, sPath, sQuery, sFragmentID = UrlSplitMore( sHost )
    #
    sServer = sDomain = ''
    #
    if sHost and not isDotQuad( sHost ):
        #
        lParts                  = sHost.lower().split( '.' )
        #
        if len( lParts ) > 1:
            #
            sLastPart           = lParts[ -1 ]
            sNext2Last          = lParts[ -2 ]
            #
            iDomainParts        = 2
            #
            if len( sLastPart ) == 2 and sLastPart in dCountryCodes:
                #
                if      sNext2Last in setTopLevelDomains or \
                        sNext2Last in setMiniDomains:
                    #
                    iDomainParts= 3
                    #
                #
            #
            lDomain             = lParts[ - iDomainParts : ]
            #
            lServer             = lParts[ : - iDomainParts ]
            #
            sDomain             = '.'.join( lDomain )
            #
            sServer             = '.'.join( lServer )
            #
    #
    return sServer, sDomain



def getDomainOffURL( sURL ):
    #
    sServer, sDomain = getServerDomainOffURL( sURL )
    #
    return sDomain



def _UrlUnSplitLocation( sUser, sPassword, sHost, sPort ):
    #
    """
    Return sLocation from tuple (user, password, host, port) .
    Inspired by location_parse.py in Text Processing in Python by David Mertz.
    """
    #
    sPort           = str( sPort )
    #
    lLocation       = []
    #
    if sUser        : lLocation = [ sUser ]
    #
    if sPassword    : lLocation.extend( [ ':', sPassword ] )
    #
    if lLocation    : lLocation.append( '@' )
    #
    lLocation.append( sHost )
    #
    if sPort        : lLocation.extend( [ ':', sPort ] )
    #
    return ''.join( lLocation )



def UrlUnSplitMore( tTuple ):
    #
    """
    Return complete URL from tuple
    (sScheme, sUser, sPassword, sHost, sPort, sPath, sQuery, sFragmentID) .
    Inspired by location_parse.py in Text Processing in Python by David Mertz.
    """
    #
    #from Utils.Both2n3 import urlunsplit
    #
    sScheme, sUser, sPassword, sHost, sPort, sPath, sQuery, sFragmentID = tTuple
    #
    if      sPath == '' and sQuery == '' and sFragmentID == '' and sHost:
        #
        sPath = '/'
    #
    sLocation = _UrlUnSplitLocation( sUser, sPassword, sHost, sPort )
    #
    return urlunsplit( ( sScheme, sLocation, sPath, sQuery, sFragmentID ) )



def UrlMustHaveSchemeAndPath( sURL ):
    #
    #from Utils.Both2n3 import urlsplit, urlunsplit
    #
    sScheme, sLocation, sPath, sQuery, sFragmentID = urlsplit( sURL )
    #
    if sScheme not in ( 'http', 'https', 'ftp' ): # if you got no scheme, urlsplit gets confused
        #
        sScheme, sLocation, sPath, sQuery, sFragmentID = urlsplit( 'http://' + sURL )
        #
    #
    if not sPath: sPath = '/'
    #
    return urlunsplit( ( sScheme, sLocation, sPath, sQuery, sFragmentID ) )



def UrlSplitMore( sURL ):
    #
    """
    Return tuple (user, password, host, port) for sLocation.
    Inspired by location_parse.py in Text Processing in Python by David Mertz.
    """
    #
    #from Utils.Both2n3 import urlsplit
    #
    sScheme, sLocation, sPath, sQuery, sFragmentID = urlsplit( sURL )
    #
    if sScheme not in ( 'http', 'https', 'ftp' ): # if you got no scheme, urlsplit gets confused
        #
        sScheme, sLocation, sPath, sQuery, sFragmentID = urlsplit( 'http://' + sURL )
        #
        sScheme             = ''
    #
    if not '@' in sLocation:
        sLocation           = ':@' + sLocation
    #
    lLocations              = sLocation.split( '@' )
    #
    sLogin, sNet            = lLocations[ : 2 ]
    #
    if ':' not in sLogin:   sLogin += ':'
    #
    sUser, sPassword        = sLogin.split( ':' )
    #
    if ':' not in sNet:     sNet += ':'
    #
    lParts                  = sNet.split( ':' )
    #
    sHost, sPort            = '', ''
    #
    if len( lParts ) == 2:
        #
        sHost, sPort        = lParts
        #
    #
    return sScheme, sUser, sPassword, sHost, sPort, sPath, sQuery, sFragmentID



def getScheme( sURL ):
    #
    # not used anywhere
    #
    sScheme, sUser, sPassword, sHost, sPort, sPath, sQuery, sFragmentID = UrlSplitMore( sURL )
    #
    return sScheme


def getCleanURL( sURL ):
    #
    return UrlUnSplitMore( UrlSplitMore( sURL ) )



def _getPort( sScheme ):
    #
    iPort = 0
    #
    if sScheme == 'http':
        #
        iPort = 80
        #
    elif sScheme == 'https':
        #
        iPort = 443
        #
    elif sScheme == 'ftp':
        #
        iPort = 21
        #
    return iPort



def getHostPortPathQuery( sURL ):
    #
    sScheme, sUser, sPassword, sHost, sPort, sPath, sQuery, sFragmentID = UrlSplitMore( sURL )
    #
    if sPort == '':
        #
        iPort = _getPort( sScheme )
        #
    elif sPort.isdigit():
        #
        iPort = int( sPort )
        #
    else:
        #
        iPort = 0
        #
    #
    sQuery = UrlUnSplitMore( ( '', '', '', '', '', '', sQuery, sFragmentID ) )
    #
    return sHost, iPort, sPath, sQuery



def getHostPortPath( sURL ):
    #
    sHost, iPort, sPath, sQuery = getHostPortPathQuery( sURL )
    #
    # sHost, iPort, sPath = getHostPortPath( sURL )
    #
    return sHost, iPort, sPath + sQuery


def getHostOnly( sURL ):
    #
    sScheme, sUser, sPassword, sHost, sPort, sPath, sQuery, sFragmentID  = \
            UrlSplitMore( sURL )
    #
    return sHost


def getUrlDropPathQuery( sURL ):
    #
    # not used anywhere
    #
    #from Utils.Both2n3 import urlsplit, urlunsplit
    #
    sScheme, sLocation, sPath, sQuery, sFragmentID = urlsplit( sURL )
    #
    return urlunsplit( ( sScheme, sLocation, '', '', '' ) )




def getHostPathTuple( sURL ):
    #
    sScheme, sUser, sPassword, sHost, sPort, sPath, sQuery, sFragmentID  = \
            UrlSplitMore( sURL )
    #
    sQuery = UrlUnSplitMore( ( '', '', '', '', '', '', sQuery, sFragmentID ) )
    #
    return sHost, sPath, sQuery





def getTuple4Socket( sURL ):
    #
    sHost, iPort, sPath, sQuery = getHostPortPathQuery( sURL )
    #
    sHost = getHostOnly( sHost )
    #
    if sPath == '': sPath = '/'
    #
    return sHost, iPort, sPath, sQuery




def getPathEtc( sURL ):
    #
    sScheme, sUser, sPassword, sHost, sPort, sPath, sQuery, sFragmentID = \
            UrlSplitMore( sURL )
    #
    sScheme, sUser, sPassword, sHost, sPort = '', '', '', '', ''
    #
    return UrlUnSplitMore(
            ( sScheme, sUser, sPassword, sHost, sPort, sPath, sQuery, sFragmentID ) )


def getPathQueryCombo( sPath, sQuery, sFragmentID = '' ):
    #
    sPathQuery = UrlUnSplitMore( ( '', '', '', '', '', sPath, sQuery, sFragmentID ) )
    #
    sPathQuery = sPathQuery.replace( '??', '?' ) ## getting double for queries!!!
    #
    return sPathQuery


def getPathQuerySeparates( sURL ):
    #
    sScheme, sUser, sPassword, sHost, sPort, sPath, sQuery, sFragmentID = \
            UrlSplitMore( sURL )
    #
    sQuery = UrlUnSplitMore( ( '', '', '', '', '', '', sQuery, sFragmentID ) )
    #
    return sPath, sQuery



def getWholeURL( sScheme, sUser, sPassword, sHost, sPort, sPath, sQuery, sFragmentID='' ):
    #
    sURL = \
        UrlUnSplitMore(
            ( sScheme, sUser, sPassword, sHost, sPort, sPath, sQuery, sFragmentID ) )
    #
    sURL = sURL.replace( '??', '?' ) ## getting double for queries!!!
    #
    return sURL



def getURLfromHostPathQuery( sHost, sPath, sQuery ):
    #
    return getWholeURL( 'http', '', '', sHost, '', sPath, sQuery )




def getToplessHost( sURL ):
    #
    """
    just 'google' from http://www.google.com/
    """
    #
    sToplessHost = getDomainOffURL( sURL )
    #
    return sToplessHost.split( '.' )[0]



def _getFileNameOffURL( sURL ):
    #
    sFile = sURL[ sURL.rfind('/') + 1 : ]
    #
    return sFile.split( '?' )[ 0 ]


def _getUrlDropFile( sURL ):
    #
    lParts = sURL.split( '/' )
    #
    lParts[ -1 ] = ''
    #
    return '/'.join( lParts )


def getFilePathNameOffURL( sURL ):
    #
    # not used anywhere
    #
    return _getUrlDropFile( sURL ), _getFileNameOffURL( sURL )



def UrlJoinBrowserStyle( *args ):
    #
    """
    Plain, old urljoin does not get this join right:
    http://www.iht.com/articles/2008/05/15/
    plus
    /articles/2008/05/15/news/china.php
    The correct link would be
    http://www.iht.com/articles/2008/05/15/news/china.php
    Note that parts overlap in the two frags
    that should not be repeated for link to be correct.
    Browsers get this join right, and this functions hopes to, too.
    """
    #
    from six.moves.urllib.parse import urljoin
    #
    from Iter.AllVers   import iRange
   #from Utils.Both2n3  import urljoin
    #
    #
    bStartsWithHTTP     = False
    #
    lArgs               = list( args )
    #
    if len( lArgs ) == 0:
        #
        return ''
        #
    elif len( lArgs ) == 1:
        #
        return lArgs[0]
        #
    elif lArgs[1].startswith( 'http://' ) and len( lArgs ) == 2:
        #
        return lArgs[1]
        #
    elif lArgs[1].startswith( 'http://' ) and len( lArgs ) > 2:
        #
        return UrlJoinBrowserStyle( lArgs[1:] )
        #
    #
    if lArgs[0].startswith( 'http://' ):
        #
        lArgs[0]        = lArgs[0][7:]
        bStartsWithHTTP = True
        #
    #
    if lArgs[0].endswith( '/' ):
        #
        lArgs[0]        = lArgs[0][:-1]
        #
    else:
        #
        lParts          = lArgs[0].split('/')
        #
        if lParts: del lParts[ -1 ]
        #
        lArgs[0]        = '/'.join( lParts )
        #
    #
    for iThis in iRange( len( lArgs ) - 1 ):
        #
        lParts0         = lArgs[ iThis     ].split('/')
        #
        if len( lParts0 ) > 1:
            #
            lParts1     = lArgs[ iThis + 1 ].split('/')
            #
            for iPart, sPart0 in enumerate( lParts0 ):
                #
                if sPart0 == lParts1[0]:
                    #
                    oRest   = enumerate( iRange( iPart + 1, len( lParts0 ) ) )
                    #
                    bRestMatches    = True
                    #
                    iDropParts      = 1
                    #
                    for iRest, iMorePart in oRest:
                        #
                        if      len( lParts1 ) > iRest + 1 and \
                                lParts0[ iMorePart ] == lParts1[ iRest + 1 ]:
                            #
                            iDropParts      += 1
                            #
                        else:
                            #
                            bRestMatches    = False
                            #
                            break
                    #
                    if bRestMatches:
                        #
                        lParts1 = lParts1[ iDropParts : ]
                        #
                        lArgs[ iThis + 1 ] = '/'.join( lParts1 )
                        #
                    #
                #
            #
        else:
            #
            break
            #
        #
    #
    if bStartsWithHTTP:
        #
        lArgs[0]         = 'http://%s/' % lArgs[0]
        #
    #
    return urljoin( *lArgs )



def _getLinksMakeOver( sHTML, sURL ):
    #
    from Iter.AllVers   import iMap, lMap, iZip
    from String.Find    import getTextInQuotes
    from Web.HTML       import oFindLinkStart # href=
    #
    lParts      = oFindLinkStart.split( sHTML ) # href=
    #
    sHead       = lParts[ 0 ]
    #
    if lParts: del lParts[ 0 ]
    #
    lLinksOrig  = iMap( getTextInQuotes, lParts )
    #
    def getNewLink( sLink ): return UrlJoinBrowserStyle( sURL, sLink )
    #
    def getLinkReplaced( t ):
        #
        sPart, sOrig = t
        #
        return sPart.replace( sOrig, getNewLink( sOrig ), 1 )
    #
    lPartsNew   = lMap( getLinkReplaced, iZip( lParts, lLinksOrig ) )
    #
    lPartsNew[ 0 : 0 ] = [ sHead ]
    #
    return ' href='.join( lPartsNew )



def SplitUrlPath( sPath ):
    #
    lPathParts          = sPath.split( '/' )
    #
    sTarget             = lPathParts[ -1 ]
    #
    lPathParts[ -1 ]    = ''
    #
    return '/'.join( lPathParts ), sTarget



def UrlSplitEvenMore( sURL ):
    #
    sScheme, sUser, sPassword, sHost, sPort, sPath, sQuery, sFragmentID \
        = UrlSplitMore( sURL )
    #
    #
    sServer, sDomain    = getServerDomainOffURL( sHost )
    #
    sDotQuad            = ''
    #
    if sDomain == '':
        #
        sDotQuad        = sHost
        #
    #
    sPath, sTarget      = SplitUrlPath( sPath )
    #
    return sScheme, sUser, sPassword, sServer, sDomain, sDotQuad, sPort, sPath, sTarget, sQuery, sFragmentID




def getDomainOffUrl( sURL ):
    #
    sScheme, sUser, sPassword, sServer, sDomain, sDotQuad, sPort, sPath, sTarget, sQuery, sFragmentID \
            = UrlSplitEvenMore( sURL )
    #
    return sDomain



def _getDomainPathOffUrl( sURL ):
    #
    sScheme, sUser, sPassword, sServer, sDomain, sDotQuad, sPort, sPath, sTarget, sQuery, sFragmentID \
            = UrlSplitEvenMore( sURL )
    #
    return sDomain, sPath



def _getServerDomainPathOffUrl( sURL ):
    #
    sScheme, sUser, sPassword, sServer, sDomain, sDotQuad, sPort, sPath, sTarget, sQuery, sFragmentID \
            = UrlSplitEvenMore( sURL )
    #
    return sServer, sDomain, sPath



def _getSite( sServer, sDomain ):
    #
    sSite   = sDomain
    #
    if sServer: sSite = '%s.%s' % ( sServer, sDomain )
    #
    return sSite


def _getSiteOffUrl( sURL ):
    #
    """
    Site is server + domain.
    """
    #
    sScheme, sUser, sPassword, sServer, sDomain, sDotQuad, sPort, sPath, sTarget, sQuery, sFragmentID \
            = UrlSplitEvenMore( sURL )
    #
    return _getSite( sServer, sDomain )



def _getSitePathOffUrl( sURL ):
    #
    sScheme, sUser, sPassword, sServer, sDomain, sDotQuad, sPort, sPath, sTarget, sQuery, sFragmentID \
            = UrlSplitEvenMore( sURL )
    #
    return _getSite( sServer, sDomain ), sPath






def _getDecorationUrlDict( lURLs, fGetDecoration ):
    #
    from Collect.Get    import getDecoratedIter
    from Dict.Get       import getDictOfListsOffItems
    #
    dDomainsURLs        = getDictOfListsOffItems(
                            getDecoratedIter( lURLs, fGetDecoration ) )
    #
    return dDomainsURLs



def getDomainUrlDictOffUrls( lURLs ):
    #
    #
    return _getDecorationUrlDict( lURLs, getDomainOffUrl )


def getDomainPathTupleUrlDictOffUrls( lURLs ):
    #
    # not used anywhere
    #
    return _getDecorationUrlDict( lURLs, _getDomainPathOffUrl )


def getServerDomainPathTupleUrlDictOffUrls( lURLs ):
    #
    #
    return _getDecorationUrlDict( lURLs, _getServerDomainPathOffUrl )


def getSiteUrlDictOffUrls( lURLs ):
    #
    """
    Site is server + domain.
    """
    #
    return _getDecorationUrlDict( lURLs, _getSiteOffUrl )


def __getSitePathTupleUrlDictOffUrls( lURLs ):
    #
    # not used anywhere
    #
    return _getDecorationUrlDict( lURLs, _getSitePathOffUrl )


def getServerPath( sURL ):
    #
    sScheme, sUser, sPassword, sServer, \
        sDomain, sDotQuad, sPort, sPath, \
        sTarget, sQuery, sFragmentID = UrlSplitEvenMore( sURL )
    #
    return sServer, sPath


def getServerPathQuery( sURL ):
    #
    sScheme, sUser, sPassword, sServer, \
        sDomain, sDotQuad, sPort, sPath, \
        sTarget, sQuery, sFragmentID = UrlSplitEvenMore( sURL )
    #
    return sServer, sPath, sQuery



def getServerPathMinimal( sURL ):
    #
    sServer, sPath = getServerPath( sURL )
    #
    if sServer == 'www': sServer = ''
    #
    if sPath.startswith( '/' ): sPath = sPath[ 1 :    ]
    if sPath.endswith(   '/' ): sPath = sPath[   : -1 ]
    #
    return sServer, sPath



if __name__ == "__main__":
    #
    from os.path        import join
    #
    from Dir.Get        import sTempDir
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if getServerDomainOffURL( 'http://www.python.org' ) != \
            ('www', 'python.org'):
        #
        lProblems.append( 'getServerDomainOffURL()' )
        #
    if getDomainOffURL( 'http://www.python.org' ) != 'python.org':
        #
        lProblems.append( 'getDomainOffURL()' )
        #
    if _UrlUnSplitLocation( 'david', 'processing', 'www.python.org', 80 ) != \
            'david:processing@www.python.org:80':
        #
        lProblems.append( '_UrlUnSplitLocation()' )
        #
    #
    sURL        = 'http://guest:gnosis@192.168.1.102:81//tmp/MAIL.MSG?foo=bar'
    #
    tSplitMore  = ('http', 'guest', 'gnosis', '192.168.1.102', '81',
                    '//tmp/MAIL.MSG', 'foo=bar', '')
    tSplit      = ('http', 'guest:gnosis@192.168.1.102:81',
                    '//tmp/MAIL.MSG', '', 'foo=bar', '')
    #
    if UrlUnSplitMore( tSplitMore ) != \
            'http://guest:gnosis@192.168.1.102:81//tmp/MAIL.MSG?foo=bar':
        #
        lProblems.append( 'UrlUnSplitMore()' )
        #
    #
    if      UrlMustHaveSchemeAndPath( 'www.python.org' ) != \
                'http://www.python.org/'                        or \
            UrlMustHaveSchemeAndPath( 'ftp://www.python.org' ) != \
                'ftp://www.python.org/':
        #
        lProblems.append( 'UrlMustHaveSchemeAndPath()' )
        #
    #
    if UrlSplitMore( sURL ) != \
            ('http', 'guest', 'gnosis', '192.168.1.102', '81',
             '//tmp/MAIL.MSG', 'foo=bar', ''):
        #
        lProblems.append( 'UrlSplitMore()' )
        #
    if getScheme( sURL ) != 'http':
        #
        lProblems.append( 'getScheme()' )
        #
    if getCleanURL( 'http://www.python.org:/' ) != 'http://www.python.org/':
        #
        lProblems.append( 'getCleanURL()' )
        #
    if      _getPort( 'http'  ) !=  80 or \
            _getPort( 'https' ) != 443 or \
            _getPort( 'ftp'   ) !=  21:
        #
        lProblems.append( '_getPort()' )
        #
    if getHostPortPathQuery( sURL ) != \
            ('192.168.1.102', 81, '//tmp/MAIL.MSG', '?foo=bar'):
        #
        lProblems.append( 'getHostPortPathQuery()' )
        #
    if getHostPortPath( sURL ) != \
            ('192.168.1.102', 81, '//tmp/MAIL.MSG?foo=bar'):
        #
        lProblems.append( 'getHostPortPath()' )
        #
    if getHostOnly( sURL ) != '192.168.1.102':
        #
        lProblems.append( 'getHostOnly()' )
        #
    if getUrlDropPathQuery( sURL ) != 'http://guest:gnosis@192.168.1.102:81':
        #
        lProblems.append( 'getUrlDropPathQuery()' )
        #
    if getTuple4Socket( sURL ) != \
            ('192.168.1.102', 81, '//tmp/MAIL.MSG', '?foo=bar'):
        #
        lProblems.append( 'getTuple4Socket()' )
        #
    if getPathEtc( sURL ) != '//tmp/MAIL.MSG?foo=bar':
        #
        lProblems.append( 'getPathEtc()' )
        #
    if getPathQueryCombo( '//tmp/MAIL.MSG', 'foo=bar' ) != \
            '//tmp/MAIL.MSG?foo=bar':
        #
        lProblems.append( 'getPathQueryCombo()' )
        #
    if getPathQuerySeparates( sURL ) != ('//tmp/MAIL.MSG', '?foo=bar'):
        #
        lProblems.append( 'getPathQuerySeparates()' )
        #
    if getWholeURL( *tSplitMore ) != sURL:
        #
        lProblems.append( 'getWholeURL()' )
        #
    if getURLfromHostPathQuery(
            '192.168.1.102', '//tmp/MAIL.MSG', 'foo=bar' ) != \
                'http://192.168.1.102//tmp/MAIL.MSG?foo=bar':
        #
        lProblems.append( 'getURLfromHostPathQuery()' )
        #
    #
    lParts = [ ( '192.168.1.102', '//tmp/MAIL.MSG',    'foo=bar' ),
               ( 'www.python.org', '/about/index.html','foo=bar' ) ]
    #
    lURLs  = ['http://192.168.1.102//tmp/MAIL.MSG?foo=bar',
              'http://www.python.org/about/index.html?foo=bar']
    #
    if getToplessHost(
            'http://www.python.org/about/index.html?foo=bar' ) != 'python':
        #
        lProblems.append( 'getToplessHost()' )
        #
    #
    sURL = 'http://www.python.org/about/index.html?foo=bar'
    #
    if _getFileNameOffURL( sURL ) != 'index.html':
        #
        lProblems.append( '_getFileNameOffURL()' )
        #
    if _getUrlDropFile( sURL ) != 'http://www.python.org/about/':
        #
        lProblems.append( '_getUrlDropFile()' )
        #
    if getFilePathNameOffURL( sURL ) != \
            ('http://www.python.org/about/', 'index.html'):
        #
        lProblems.append( 'getFilePathNameOffURL()' )
        #
    if UrlJoinBrowserStyle(
            'http://www.iht.com/articles/2008/05/15/',
            '/articles/2008/05/15/news/china.php' ) != \
            'http://www.iht.com/articles/2008/05/15/news/china.php':
        #
        lProblems.append( 'UrlJoinBrowserStyle()' )
        #
    #
    sHTML = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html lang="en" xml:lang="en" xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta content="text/html; charset=utf-8" http-equiv="content-type" />
    <title>About</title>
    </head>
    <body>
    <ul class="level-two">
    <li class=""><a href="gettingstarted" class="" title="">Getting Started</a>
    </li><li class=""><a href="apps" class="" title="">Applications</a>
    </li><li class=""><a href="success" class="" title="">Success Stories</a>
    </li><li class=""><a href="quotes" class="" title="">Quotes</a>
    </li><li class=""><a href="website" class="" title="">Website</a>
    </li><li class=""><a href="help" class="" title="">Help</a>
    </li>
    </ul>
    </body>
    </html>
    """
    #
    #
    if not "http://www.python.org/about/help" in _getLinksMakeOver( sHTML, sURL ):
        #
        lProblems.append( '_getLinksMakeOver()' )
        #
    if SplitUrlPath('about/index.html' ) != ('about/', 'index.html'):
        #
        lProblems.append( 'SplitUrlPath()' )
        #
    if UrlSplitEvenMore( sURL ) != \
            ('http', '', '', 'www', 'python.org', '', '',
             '/about/', 'index.html', 'foo=bar', ''):
        #
        lProblems.append( 'UrlSplitEvenMore()' )
        #
    if getDomainOffUrl( sURL ) != 'python.org':
        #
        lProblems.append( 'getDomainOffUrl()' )
        #
    if _getDomainPathOffUrl( sURL ) != ('python.org', '/about/'):
        #
        lProblems.append( '_getDomainPathOffUrl()' )
        #
    if _getServerDomainPathOffUrl( sURL ) != ('www', 'python.org', '/about/'):
        #
        lProblems.append( '_getServerDomainPathOffUrl()' )
        #
    if _getSite( 'www', 'python.org' ) != 'www.python.org':
        #
        lProblems.append( '_getSite()' )
        #
    if _getSiteOffUrl( sURL ) != 'www.python.org':
        #
        lProblems.append( '_getSiteOffUrl()' )
        #
    if _getSitePathOffUrl( sURL ) != ('www.python.org', '/about/'):
        #
        lProblems.append( '_getSitePathOffUrl()' )
        #
    lURLs  = ['http://hub.ebay.com/buy?ssPageName=h:h:cat:US',
              'http://www.python.org/about/index.html?foo=bar']
    #
    if _getDecorationUrlDict( lURLs, getToplessHost ) != \
            {'python': ['http://www.python.org/about/index.html?foo=bar'],
             'ebay'  : ['http://hub.ebay.com/buy?ssPageName=h:h:cat:US']}:
        #
        lProblems.append( '_getDecorationUrlDict()' )
        #
    if getDomainUrlDictOffUrls( lURLs ) != \
            {'ebay.com'  : ['http://hub.ebay.com/buy?ssPageName=h:h:cat:US'],
             'python.org': ['http://www.python.org/about/index.html?foo=bar']}:
        #
        lProblems.append( 'getDomainUrlDictOffUrls()' )
        #
    if getDomainPathTupleUrlDictOffUrls( lURLs ) != \
            {('ebay.com', '/')        :
                    ['http://hub.ebay.com/buy?ssPageName=h:h:cat:US'],
             ('python.org', '/about/'):
                    ['http://www.python.org/about/index.html?foo=bar']}:
        #
        lProblems.append( 'getDomainPathTupleUrlDictOffUrls()' )
        #
    if getServerDomainPathTupleUrlDictOffUrls( lURLs ) != \
            {('hub', 'ebay.com', '/')       :
                    ['http://hub.ebay.com/buy?ssPageName=h:h:cat:US'],
             ('www', 'python.org', '/about/'):
                    ['http://www.python.org/about/index.html?foo=bar']}:
        #
        lProblems.append( 'getServerDomainPathTupleUrlDictOffUrls()' )
        #
    if getSiteUrlDictOffUrls( lURLs ) != \
            {'hub.ebay.com' :
                    ['http://hub.ebay.com/buy?ssPageName=h:h:cat:US'],
            'www.python.org':
                    ['http://www.python.org/about/index.html?foo=bar']}:
        #
        lProblems.append( 'getSiteUrlDictOffUrls()' )
        #
    if __getSitePathTupleUrlDictOffUrls( lURLs ) != \
            {('www.python.org', '/about/'):
                    ['http://www.python.org/about/index.html?foo=bar'],
             ('hub.ebay.com',   '/')      :
                    ['http://hub.ebay.com/buy?ssPageName=h:h:cat:US']}:
        #
        lProblems.append( '__getSitePathTupleUrlDictOffUrls()' )
        #
    if getServerPath( "http://cantor.house.gov/" ) != ( 'cantor', '/' ):
        #
        lProblems.append( 'getServerPath()' )
        #
    #
    if  getServerPathMinimal(
            "http://www.house.gov/larsen/" ) != ( '', 'larsen' ):
        #
        lProblems.append( 'getServerPathMinimal() got path' )
        #
    #
    if  getServerPathMinimal(
            "http://randy.house.gov/" ) != ( 'randy', '' ):
        #
        lProblems.append( 'getServerPathMinimal() got server' )
        #
    #
    sayTestResult( lProblems )