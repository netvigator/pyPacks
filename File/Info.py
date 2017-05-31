#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# File functions Info
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
# Copyright 2004-2015 Rick Graves
#
# from os.path import join, isfile, getmtime, split, splitext, exists, basename, isdir
# from os      import stat, environ, getcwd, listdir, rename, remove


from File.Spec import getFullSpec as _getFullSpec

def getModTime( *tParts, **kwargs ):
    #
    from time           import timezone
    from os.path        import getmtime
    #
    from Utils.ImIf   import ImIf
    #
    sFullSpec   = _getFullSpec( *tParts )
    #
    bWantLocal  = False
    #
    bWantLocal  = kwargs.get( 'bWantLocal' )
    #
    iAdjust4TZ  = ImIf( bWantLocal, 0, timezone )
    #
    return int( getmtime( sFullSpec ) ) + iAdjust4TZ



def getTimeStamp( *tParts ):
    #
    from os.path import getmtime
    #
    sPathName = _getFullSpec( *tParts )
    #
    return getmtime( sPathName )




def getSize( *tParts ):
    #
    from os      import stat
    #
    sFullSpec   = _getFullSpec( *tParts )
    #
    return stat( sFullSpec )[6]



def getSaySize( iBytes ):
    #
    iKbytes, iRbytes = divmod( iBytes,  1024 )
    #
    iMbytes, iKbytes = divmod( iKbytes, 1024 )
    #
    iGbytes, iMbytes = divmod( iMbytes, 1024 )
    #
    if iGbytes > 0:
        #
        sSay    = '%-9.2f' % ( iGbytes + float( iMbytes ) / 1024 )
        #
        sSay    = '%s Gb' % ( sSay.strip() )
        #
    elif iMbytes > 0:
        #
        sSay    = '%-5.2f' % ( iMbytes + float( iKbytes ) / 1024 )
        #
        sSay    = '%s Mb' % ( sSay.strip() )
        #
    elif iKbytes > 0:
        #
        sSay    = '%-5.2f' % ( iKbytes + float( iRbytes ) / 1024 )
        #
        sSay    = '%s Kb' % ( sSay.strip() )
        #
    else:
        #
        sSay    = '%s bytes' % iBytes
    #
    return sSay



def getLineCount( *tParts ):
    #
    from File.Get       import FileNotThereError
    from File.Test      import isFileThere
    #
    sFileSpec = _getFullSpec( *tParts )
    #
    if not isFileThere( sFileSpec ): raise FileNotThereError( sFileSpec )
    #
    fFile = open( sFileSpec )
    #
    iLines = 0
    #
    for sLine in fFile:
        #
        iLines += 1
    #
    fFile.close()
    #
    return iLines


def _isURL( s ):
    #
    from Web.Test import isURL
    #
    return isURL( s,
            bAnySchemeOK = False, bSecureHttpOK = False, bNoSchemeOK = True )


def _getDomainsOffLine( s ):
    #
    from Iter.AllVers import iFilter
    #
    lParts = s.split()
    #
    return iFilter( _isURL, lParts )


def getDomainCount( *tParts ):
    #
    # see Web.Info.getDomainCountsOffFile()
    #
    from Collect.Info   import getCounts
    from Dict.Get       import getItemIter
    from File.Get       import FileNotThereError
    from File.Test      import isFileThere
    from Iter.AllVers   import iMap
    from Iter.Get       import getListSwapValueKey
    from File.Write     import putListInTemp
    from Web.Address    import getDomainOffUrl
    #
    #
    sFileSpec = _getFullSpec( *tParts )
    #
    if not isFileThere( sFileSpec ): raise FileNotThereError( sFileSpec )
    #
    fFile = open( sFileSpec )
    #
    lURLs = []
    #
    for sLine in fFile:
        #
        lURLs.extend( _getDomainsOffLine( sLine ) )
    #
    fFile.close()
    #
    lURLs = list( frozenset( lURLs ) )
    #
    lDomains = iMap( getDomainOffUrl, lURLs )
    #
    dCounts = getCounts( lDomains )
    #
    if '' in dCounts: del dCounts[ '' ]
    #
    lCounts = getListSwapValueKey( getItemIter( dCounts ) )
    #
    lCounts.sort()
    lCounts.reverse()
    #
    putListInTemp( [ '%s,%s' % t for t in lCounts ] )


if __name__ == "__main__":
    #
    from os.path        import join
    #
    from Dir.Get        import sTempDir
    from File.Get       import getTempFile, getListOffFileLines
    from File.Write     import QuickDumpLines
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if getModTime( 'Info.py' ) < 1170000000:
        #
        lProblems.append( 'getModTime()' )
        #
    #

    if getTimeStamp( 'Info.py' ) < 1170000000:
        #
        lProblems.append( 'getTimeStamp()' )
        #
    #
    iSize = getSize( 'Info.py' )
    #
    if iSize < 6000 or iSize > 7000:
        #
        lProblems.append( 'getSize() size of Info.py' )
        lProblems.append( "got size: %s bytes" % str( getSize( 'Info.py' ) ) )
        #
    #

    if not getSaySize( iSize ):
        #
        lProblems.append( 'getSaySize()' )
        #
    #
    iLines = getLineCount( 'Info.py' )
    #
    if iLines < 200 or iLines > 300:
        #
        lProblems.append( 'getLineCount()' )
        lProblems.append( "  " + str( getLineCount( 'Info.py' ) ) )
        #
    #
    sTempFile = getTempFile()
    #
    lURLs = [
        'http://www.python.org',
        'http://www.python.org/help/',
        'http://www.python.org/about/index.html?foo=bar',
        'http://www.iht.com/articles/2008/05/15/news/china.php',
        'http://hub.ebay.com/ http://www.ebay.com/',
        "http://www.house.gov/curly/",
        "http://www.house.gov/larry/",
        "http://www.house.gov/moe/",
        "http://www.house.gov/groucho/",
        "http://www.house.gov/harpo/",
        "http://www.house.gov/geppo/" ]
    #
    QuickDumpLines( lURLs, sTempFile )
    #
    getDomainCount( sTempFile )
    #
    lCounts = getListOffFileLines( join( sTempDir, 'temp.txt' ) )
    #
    if lCounts != ['6,house.gov', '3,python.org', '2,ebay.com', '1,iht.com']:
        #
        lProblems.append( 'getDomainCount()' )
        lProblems.append( "  " + str( lCounts ) )
        #
    #
    #
    sayTestResult( lProblems )