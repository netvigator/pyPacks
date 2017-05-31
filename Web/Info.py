#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions Info
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
# Copyright 2010-2011 Rick Graves
#


def getDomainCountsOffFile( *sFileSpec, **kwargs ):
    #
    # see File.Info.getDomainCount()
    #
    from Collect.Info   import getCounts
    from Iter.Get       import getListSwapValueKey
    from Dict.Get       import getItemIter
    from File.Get       import getContent
    from File.Spec      import getFullSpec
    from File.Write     import putCsvOut
    from Iter.AllVers   import iFilter, iMap
    from Web.Address    import getDomainOffURL
    from Web.Test       import isLazyURL
    #
    sName       = getFullSpec( *sFileSpec )
    #
    lText       = getContent( sName ).split()
    #
    lDomains    = iMap( getDomainOffURL, iFilter( isLazyURL, lText ) )
    #
    dCounts     = getCounts( lDomains )
    #
    lCountDomain= getListSwapValueKey( getItemIter( dCounts ) )
    #
    lCountDomain.sort()
    lCountDomain.reverse()
    #
    lCountDomain[ 0 : 0 ] = [ ( 'count', 'domain' ) ]
    #
    putCsvOut( lCountDomain )


if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    #lCountDomain.lCountDomain.
    lProblems = []
    #
    #
    if 0 and getCookieFromDict( dReceived ) != 'abcde01234':
        #
        lProblems.append( 'getCookieFromDict()' )
        #


    #
    sayTestResult( lProblems )