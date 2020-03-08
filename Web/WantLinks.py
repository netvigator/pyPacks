#!/home/rick/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions want links
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
# Copyright 2015-2020 Rick Graves
#

import requests

from time import sleep

try:
    from ..Collect.Query    import get1stThatMeets
    from ..File.Get         import getListFromFileLines
    from ..File.Write       import ( QuickDumpLines, putListInTemp,
                                     PutPrettyPrintInTemp )
    from ..String.Get       import getContentOutOfQuotes, getTextBeforeLast
    from ..String.Test      import isDigit
    from ..Iter.AllVers     import iRange
    from ..Utils.Both2n3    import print3
    from .Address           import getHostPathTuple, getDomainOffURL
    from .HTML              import oFindLinkStart # href=
    from .Test              import isURL
except ( ValueError, ImportError ):
    from Collect.Query      import get1stThatMeets
    from File.Get           import getListFromFileLines
    from File.Write         import ( QuickDumpLines, putListInTemp,
                                     PutPrettyPrintInTemp )
    from Iter.AllVers       import iRange
    from String.Get         import getContentOutOfQuotes, getTextBeforeLast
    from String.Test        import isDigit
    from Utils.Both2n3      import print3
    from Web.Address        import getHostPathTuple, getDomainOffURL
    from Web.HTML           import oFindLinkStart # href=
    from Web.Test           import isURL


def getUniqueLinks( sReadFile, sOutFile ):
    #
    lLines  = getListFromFileLines( sReadFile )
    #
    setLinks= frozenset( filter( isURL, lLines ) )
    #
    #
    lDecorate = [ ( getHostPathTuple( sURL ), sURL ) for sURL in setLinks ]
    #
    lDecorate = [ ( ( getDomainOffURL( t[0][0] ), t[0][1] ), t[1] ) for t in lDecorate ]
    #
    lDecorate.sort()
    #
    lLinks  = [ t[1] for t in lDecorate ]
    #
    QuickDumpLines( lLinks, sOutFile )


def _getPageHTML( sLink ):
    #
    oPage = requests.get( sLink )
    #
    return oPage.text


def _getLinksOffHTML( sHTML, tWantDomains = None, sEndsWith = None ):
    #
    #
    lMaybe      = oFindLinkStart.split( sHTML )
    #
    del lMaybe[0]
    #
    lLinks = [ getContentOutOfQuotes( s ) for s in lMaybe ]
    #
    if sEndsWith is not None:
        #
        lLinks = [  getTextBeforeLast( s, sEndsWith )
                    for s in lLinks
                    if s.endswith( sEndsWith ) ]
        #
    #
    if tWantDomains is not None:
        #
        lLinks = [ ( getDomainOffURL( s ).lower(), s ) for s in lLinks ]
        #
        lLinks = [ t[1] for t in lLinks if t[0] in tWantDomains ]
        #
    #
    return lLinks


def _getLinksOffURL( sLink, tWantDomains = None, sEndsWith = None ):
    #
    sHTML = _getPageHTML( sLink )
    #
    lLinks = _getLinksOffHTML( sHTML, tWantDomains, sEndsWith )
    #
    return lLinks




def getLinksDict(
        sLinkStart, iUntilPage,
        tWantDomains    = None,
        sEndsWith       = None,
        iPagePause      = 2 ):
    #
    lLinkParts = sLinkStart.split( '/' )
    #
    lLinkParts.reverse()
    #
    iStartPage = int( get1stThatMeets( lLinkParts, isDigit ) )
    #
    sLinkPattern = sLinkStart.replace( '/%s' % str( iStartPage ), '/%s' )
    #
    dLinks = {}
    #
    for iGetPage in iRange( iStartPage, iUntilPage + 1 ):
        #
        sNumberURL  = sLinkPattern % iGetPage
        #
        print3( 'getting %s ...' % sNumberURL )
        #
        if iGetPage > iStartPage: sleep( iPagePause )
        #
        lLinksOuter = _getLinksOffURL( sNumberURL, sEndsWith = sEndsWith )
        #
        for sLinkOuter in lLinksOuter:
            #
            print3( '    getting %s ...' % sLinkOuter )
            #
            sleep( iPagePause )
            #
            lLinksInner = _getLinksOffURL(
                                sLinkOuter, tWantDomains = tWantDomains )
            #
            if lLinksInner:
                #
                dLinks[ sLinkOuter ] = lLinksInner
                #
            #
        #
    #
    PutPrettyPrintInTemp( dLinks )



if __name__ == "__main__":
    #
    from os.path        import join
    from sys            import argv
    #
    from six            import print_ as print3
    #
    from Dir.Get        import sTempDir
    from File.Test      import isFileThere
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    args = argv[ 1 : ]
    #
    sReadFile   = join( sTempDir, 'LotsOfLinks.txt' )
    sOutFile    = join( sTempDir, 'UniqueLinks.txt' )
    #
    if args:
        #
        sReadFile       = args[0]
        #
        if len( args ) > 1:
            #
            sOutFile    = args[2]
            #
        #
    else:
        #
        if isFileThere( sReadFile ):
            #
            getUniqueLinks( sReadFile, sOutFile )
            #
        else:
            #
            print3( 'Usage: WantLinks [inputFile [, outputFile] ]' )
            print3( 'default inputFile  {temp dir}lotsolinks.txt' )
            print3( 'default outputFile {temp dir}UniqueLinks.txt' )
            #
        #
    #
    if False:
        #
        lProblems.append( 'getDotQuad4IspTester()' )
        #
    #
    #
    sayTestResult( lProblems )
