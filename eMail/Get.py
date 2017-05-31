#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# eMail functions get
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
# Copyright 2004-2011 Rick Graves
#
'''

from File.Get import getListFromFileLines


dNew = dict.fromkeys( getListFromFileLines( 'NewEmails.txt' ) )

l =  getListFromFileLines( 'NewDump.txt' )

'''
from String.Dumpster    import DumpYouNameItClass as _dumpYouNameItClass
from String.Find        import getFinder          as _getFinder

_oPeriodCommaDumpster   = _dumpYouNameItClass( '.,' )
_oEmailBracketDumpster  = _dumpYouNameItClass( '<>' )
_oSpaceCommaSemiFinder  = _getFinder( '[ ,;]' )


def getHyphen( s ): return s.replace( '_', '-' )



def getEmailAddsIter( s ):
    #
    from eMail.Test     import isEmailAddress
    from Iter.AllVers   import iFilter
    #
    lParts = _oEmailBracketDumpster.Dump( s.lower() ).split()
    #
    return iFilter( isEmailAddress, lParts )



def getEmailAddsTuple( s ):
    #
    return tuple( getEmailAddsIter( s ) )



def getEmailAdd( s ):
    #
    from eMail.Test     import isEmailAddress
    from Collect.Query  import get1stThatMeets
    #
    lParts = _oEmailBracketDumpster.Dump( s ).split()
    #
    return get1stThatMeets( lParts, isEmailAddress )



def getRealPerCent( sText ):
    #
    return sText.replace( 'cPC(', '%(' )



def getCleanName( sName ):
    #
    '''mail servers dislike commas and periods
    in the text name in front of the email address
    this cleans them out
    '''
    #
    from Iter.AllVers   import iMap
    from String.Get     import getTitleizedIfNeeded
    from String.Replace import getSpaceForWhiteAlsoStrip
    #
    sName = getSpaceForWhiteAlsoStrip( _oPeriodCommaDumpster.Dump( sName ) )
    #
    lName = sName.split()
    #
    return ' '.join( iMap( getTitleizedIfNeeded, lName ) )



def getReturnPathVERP( sListName, sAddressee, sServer ):
    #
    # Return-Path:
    # <member-database-team-bounces+gravesricharde=yahoo.com@members.democratsabroad.org>
    #
    '''returns Mailman style VERP return path
    '''
    #
    sListName += '-bounces'
    #
    sEmbedAddress = sAddressee.replace( '@', '=' )
    #
    return '<%s+%s@%s>' % ( sListName, sEmbedAddress, sServer )



def _getSplitOnSpacesComasSemis( s ):
    #
    return _oSpaceCommaSemiFinder.split( s )
    

def getEmailListFromString( s ):
    #
    from Iter.AllVers   import lFilter
    #
    return lFilter( None, _getSplitOnSpacesComasSemis( s ) )


def getRealEmail( s ):
    #
    from String.Get import getTextWithin
    #
    if '<' in s and '>' in s:
        #
        s = getTextWithin( s, '<', '>' )
        #
    #
    return s


def getUserFriendlyAddress( sName, sEmail ):
    #
    from Iter.AllVers   import lFilter
    #
    lEmails = lFilter( bool, [ s.strip() for s in sEmail.split( ',' ) ] )
    #
    sEmail  = ''
    #
    if lEmails: sEmail = lEmails[0]
    #
    if sName and sEmail:
        sSayEmail = '"%s" <%s>' % ( sName, sEmail )
    else:
        sSayEmail = sEmail
    #
    if len( lEmails ) > 1:
        #
        sRest = ', '.join( lEmails[1:] )
        #
        sSayEmail = '%s, %s' % ( sSayEmail, sRest )
        #
    #
    return sSayEmail



def getAddresseeStrOffSeq( uTo ):
    #
    from Collect.Test import isListOrTuple
    #
    if isListOrTuple( uTo ):
        #
        sTo = ', '.join( uTo )
        #
    else:
        #
        sTo = uTo
        #
    #
    return sTo




if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    s = '~!@#$%^&*()@gmail.com 999 <aardvigator@gmail.com> how now brown cow'
    #
    #
    if getEmailAddsTuple( s ) != ( 'aardvigator@gmail.com', ):
        #
        lProblems.append( 'getEmailAddsTuple()' )
        #
    #
    if getEmailAdd( s ) != 'aardvigator@gmail.com':
        #
        lProblems.append( 'getEmailAdd()' )
        #
    #
    if getRealPerCent( '"cPC(sName)s" <cPC(sEmail)s>' ) != \
            '"%(sName)s" <%(sEmail)s>':
        #
        lProblems.append( 'getRealPerCent()' )
        #
    #
    if getCleanName( "Frederick Heath, Jr. " ) != "Frederick Heath Jr":
        #
        lProblems.append( 'getCleanName()' )
        #
    #
    if getReturnPathVERP(
                'member-database-team',
                'gravesricharde@yahoo.com',
                'members.democratsabroad.org' ) != \
            '<member-database-team-bounces+gravesricharde=yahoo.com@members.democratsabroad.org>':
        #
        lProblems.append( 'getReturnPathVERP()' )
        #
    #
    sTest = 'susan.prewitt@algorithmics.com <susan.prewitt@algorithmics.com>'
    sWant = 'susan.prewitt@algorithmics.com'
    #
    if getRealEmail( sTest ) != sWant or getRealEmail( sWant ) != sWant :
        #
        lProblems.append( 'getRealEmail()' )
        #
    #
    sEmails = ', linus@gmail.com;guido@gmail.com,  guido@hotmail.com ;'
    #
    if getEmailListFromString( sEmails ) != \
            ['linus@gmail.com', 'guido@gmail.com', 'guido@hotmail.com']:
        #
        lProblems.append( 'getEmailListFromString() 3 in list' )
        #
    #
    if getEmailListFromString( 'linus@gmail.com' ) != [ 'linus@gmail.com' ]:
        #
        lProblems.append( 'getEmailListFromString() one only' )
        #
    #
    if getEmailListFromString( 'a,b;c, ' ) != ['a', 'b', 'c']:
        #
        lProblems.append( 'getEmailListFromString() blank not removed' )
        #
    #
    sName  = "Mattia Melocchi, Macom srl"
    sEmail = "mattia@macomsrl.it"
    #
    if getUserFriendlyAddress( sName, sEmail ) != \
            '"Mattia Melocchi, Macom srl" <mattia@macomsrl.it>':
        #
        lProblems.append( 'getUserFriendlyAddress()' )
        #
    #
    #
    sayTestResult( lProblems )