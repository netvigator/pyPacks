#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions Links
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
# Copyright 2004-2012 Rick Graves
#


def getLinkOffHref( sHref ):
    #
    """
    Quotes around the link text are optional.
    if there are quote characters, returns the content.
    returns text up to '>' if no quotes in there.
    """
    #
    from Web.HTML   import oSeparatorFinder
    #
    sLink           = ''
    #
    lSeparators     = oSeparatorFinder.findall( sHref )
    #
    if lSeparators:
        #
        lParts      = oSeparatorFinder.split(   sHref )
        #
        if lSeparators[0] == '>':
            #
            sLink   = lParts[0]
            #
        elif lSeparators.count( lSeparators[0] ) > 1:
            #
            sLink   = lParts[1]
            #
        #
    #
    return sLink

    
    



def getLinkFromHTML(sHTML):
    #
    from HTML       import oFindLinkStart # href=
    #
    sLink       = ''
    #
    lParts      = oFindLinkStart.split( sHTML ) # href=
    #
    if len( lParts ) > 1:
        #
        sLink   = getLinkOffHref( lParts[1] )
        #
    #
    return sLink


def _getLinksAndStarts( sHTML ):
    #
    from HTML   import oFindLinkStart # href=
    #
    lMaybe      = oFindLinkStart.split( sHTML )
    #
    iLen2Here   = len( lMaybe[ 0 ] )
    #
    if lMaybe: del lMaybe[ 0 ] # dump the first line - it did not start with ' href='
    #
    lLinks      = [ None ] * len( lMaybe )
    lLinkStart  = [ None ] * len( lMaybe )
    #
    iThis =   -1
    #
    for sLine in lMaybe:
        #
        iThis               += 1
        #
        iLen2Here           += 7
        #
        sLink               = getLinkOffHref( sLine )
        #
        sLink               = sHTML[ iLen2Here : iLen2Here + len( sLink ) ]
        #
        lLinks[     iThis ] = sLink
        #
        lLinkStart[ iThis ] = iLen2Here
        #
        iLen2Here           += ( len( sLine ) - 1 )
        #
    return lLinks, lLinkStart



def getStartsAndLinksIter( sHTML ):
    #
    from Iter.AllVers import iZip
    #
    lLinks, lLinkStart  = _getLinksAndStarts( sHTML )
    #
    return iZip( lLinkStart, lLinks )



def getLinksOffHTML( sHTML, sURL = None, bKeepUrlDomains = 1 ):
    #
    from Iter.AllVers import lFilter
    from Web.Address import getDomainOffURL
    #
    lLinks, lLinkStart = _getLinksAndStarts( sHTML )
    #
    if sURL and not bKeepUrlDomains:
        #
        sUrlDomain = getDomainOffURL( sURL )
        #
        def NotUrlDomain( sLink ):
            #
            return getDomainOffURL( sLink ) != sUrlDomain
        #
        lLinks = lFilter( NotUrlDomain, lLinks )
        #
    #
    return lLinks



def getEmailAddress( sLine ):
    #
    from Iter.AllVers   import tFilter
    from Web.Test       import hasAt
    from Web.Address    import getDomainOffURL
    #
    sEmailAdd   = ''
    #
    lParts      = sLine.split()
    #
    tGood       = tFilter( hasAt, lParts )
    #
    if tGood:
        #
        lFrags  = tGood[0].split( '@' )
        #
        sDomain = getDomainOffURL( lFrags[1] )
        #
        if len( sDomain ) > 1:
            #
            sEmailAdd   = tGood[0]
    #
    return sEmailAdd




if __name__ == "__main__":
    #
    from Iter.AllVers   import tZip
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if      getLinkOffHref( ' abc "inside" def ' ) != 'inside' or \
            getLinkOffHref( ' abc >inside  def ' ) != ' abc '  or \
            getLinkOffHref( ' abc >inside "def"' ) != ' abc ':
        #
        lProblems.append( 'getLinkOffHref()' )
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
    <li class=""><a href="http://www.python.org/about/gettingstarted" class="" title="">Getting Started</a>
    </li><li class=""><a href="http://www.python.org/about/apps" class="" title="">Applications</a>
    </li><li class=""><a href="http://www.python.org/about/success" class="" title="">Success Stories</a>
    </li><li class=""><a href="http://www.python.org/about/quotes" class="" title="">Quotes</a>
    </li><li class=""><a href="http://www.python.org/about/website" class="" title="">Website</a>
    </li><li class=""><a href="http://www.python.org/about/help" class="" title="">Help</a>
    </li>
    </ul>
    </body>
    </html>
    """
    #
    lLinksStarts = \
        ([  'http://www.python.org/about/gettingstarted',
            'http://www.python.org/about/apps',
            'http://www.python.org/about/success',
            'http://www.python.org/about/quotes',
            'http://www.python.org/about/website',
            'http://www.python.org/about/help'],
         [389, 502, 602, 708, 804, 902])
    #
    if getLinkFromHTML( sHTML ) != \
            'http://www.python.org/about/gettingstarted':
        #
        lProblems.append( 'getLinkFromHTML()' )
        #
    if _getLinksAndStarts( sHTML ) != lLinksStarts:
        #
        lProblems.append( '_getLinksAndStarts()' )
        #
    if (   tuple( getStartsAndLinksIter( sHTML ) ) !=
            tZip( lLinksStarts[1], lLinksStarts[0] ) ):
        #
        lProblems.append( 'getStartsAndLinksIter()' )
        #
    if getLinksOffHTML( sHTML ) != lLinksStarts[0]:
        #
        lProblems.append( 'getLinksOffHTML()' )
        #
    #
    sLine = ' How now brown cow help@python.org so there '
    #
    if getEmailAddress( sLine ) != 'help@python.org':
        #
        lProblems.append( 'getEmailAddress()' )
        #
    #
    sayTestResult( lProblems )