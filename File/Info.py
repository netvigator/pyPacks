#!/home/rick/.local/bin/pythonTest
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
#   http://www.gnu.org/licenses/
#
# Copyright 2004-2023 Rick Graves
#
# from os.path import join, isfile, getmtime, split, splitext, exists, basename, isdir
# from os      import stat, environ, getcwd, listdir, rename, remove

from os                 import stat
from os.path            import getmtime
from time               import timezone

try:
    from .Get           import FileNotThereError
    from .Spec          import getFullSpec as _getFullSpec
    from .Test          import isFileThere
    from .Write         import putListInTemp
    from ..Collect.Info import getCounts
    from ..Dict.Get     import getItemIter
    from ..Iter.AllVers import iMap
    from ..Iter.Get     import getListSwapValueKey
    from ..Web.Address  import getDomainOffUrl
    from ..Web.Test     import isURL
except ( ValueError, ImportError ):
    from File.Get       import FileNotThereError
    from File.Spec      import getFullSpec as _getFullSpec
    from File.Test      import isFileThere
    from File.Write     import putListInTemp
    from Collect.Info   import getCounts
    from Dict.Get       import getItemIter
    from Iter.Get       import getListSwapValueKey
    from Iter.AllVers   import iMap
    from Web.Address    import getDomainOffUrl
    from Web.Test       import isURL

def getModTime( *tParts, **kwargs ):
    #
    sFullSpec   = _getFullSpec( *tParts )
    #
    bWantLocal  = False
    #
    bWantLocal  = kwargs.get( 'bWantLocal' )
    #
    iAdjust4TZ  = 0 if bWantLocal else timezone
    #
    return int( getmtime( sFullSpec ) ) + iAdjust4TZ



def getTimeStamp( *tParts ):
    #
    #
    sPathName = _getFullSpec( *tParts )
    #
    return getmtime( sPathName )




def getSize( *tParts ):
    #
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
    #
    sFileSpec = _getFullSpec( *tParts )
    #
    if not isFileThere( sFileSpec ): raise FileNotThereError( sFileSpec )
    #
    with open( sFileSpec ) as oFile:
        #
        for i, s in enumerate( oFile ):
            #
            pass
            #
        #
    #
    return i + 1


def _isURL( s ):
    #
    #
    return isURL( s,
            bAnySchemeOK = False, bSecureHttpOK = False, bNoSchemeOK = True )


def _getDomainsOffLine( s ):
    #
    try: # moving this to the top breaks this package!
        from ..Iter.AllVers import iFilter
    except ( ValueError, ImportError ): # maybe circular import issue
        from Iter.AllVers   import iFilter
    #
    lParts = s.split()
    #
    return iFilter( _isURL, lParts )


def getDomainCount( *tParts ):
    #
    # see Web.Info.getDomainCountsOffFile()
    #
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
    from Utils.Both2n3  import getThisFileSpec
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    sThisFile = getThisFileSpec(__file__)
    #
    if getModTime( sThisFile ) < 1170000000:
        #
        lProblems.append( 'getModTime()' )
        #
    #

    if getTimeStamp( sThisFile ) < 1170000000:
        #
        lProblems.append( 'getTimeStamp()' )
        #
    #
    iSize = getSize( sThisFile )
    #
    if iSize < 7000 or iSize > 8000:
        #
        lProblems.append( 'getSize() size of Info.py' )
        lProblems.append( "got size: %s bytes" % str( getSize( sThisFile ) ) )
        #
    #

    if not getSaySize( iSize ):
        #
        lProblems.append( 'getSaySize()' )
        #
    #
    iLines = getLineCount( sThisFile )
    #
    if iLines < 200 or iLines > 300:
        #
        lProblems.append( 'getLineCount()' )
        lProblems.append( "  " + str( getLineCount( sThisFile ) ) )
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
