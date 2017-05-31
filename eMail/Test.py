#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Mail functions Test
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
# Copyright 2004-2016 Rick Graves
#
from string             import ascii_letters, digits
#
from six                import print_ as print3

from Iter.AllVers       import iZip        as _iZip
from String.Transform   import getSwapper  as _getSwapper
from Dict.Get           import getItemIter as _getItemIter
#
class Failure( Exception ): pass
#
_EMAIL_OK_CHRS = tuple( "!#$%*/?|^{}`~&'+-=_." + ascii_letters + digits )
#
_oBlanks4EmailChars = _getSwapper(
        dict( _iZip( _EMAIL_OK_CHRS, [' '] * len( _EMAIL_OK_CHRS ) ) ) )
#
_setBogusDomains    = frozenset( ( 'noemail.com', ) )


class dCounting( dict ):
    #
    '''
    import & pass instance to dumpEmailBodies2Temp
    so that you only dump contents with unique subjects
    '''
    #
    def add( self, k ):
        #
        self[ k ] = self.setdefault( k, 0 ) + 1


def isEmailAddress( s, setExcludeDomains = None ):
    #
    '''
    OK susan.prewitt@algorithmics.com
    NOT OK 'susan prewitt <susan.prewitt@algorithmics.com>'
    OK bill@microsoft.com
    OK sergy@google.com
    NOT OK 'bill@microsoft.com, sergy@google.com'
    use isOKasEmail() to return true for the NOT OK's 
    '''
    #
    from Web.Test       import isDomainName
    #
    try:
        #
        if s is None:                       raise Failure
        #
        try:
            s = s.strip()
        except AttributeError:              raise Failure
        #
        s = s.lower()
        #
        lParts = s.split( '@' )
        #
        if len( lParts ) != 2:              raise Failure
        #
        sMailBox = lParts[0]
        #
        if not sMailBox:                    raise Failure
        #
        if not isDomainName( lParts[1] ):   raise Failure
        #
        if lParts[1] in _setBogusDomains:   raise Failure
        #
        if setExcludeDomains and \
            lParts[1] in setExcludeDomains: raise Failure
        #
        if ' ' in  sMailBox:                raise Failure
        #
        if '..' in sMailBox:                raise Failure
        #
        if sMailBox.startswith( '.' ) or sMailBox.endswith( '.' ):
                                            raise Failure
        #
        sBlanks4Chrs = _oBlanks4EmailChars( sMailBox )
        #
        if sBlanks4Chrs.replace( ' ', '' ): raise Failure
        #
        bEmailAddress  = True
        #
    except Failure:
        #
        bEmailAddress  = False
        #
    #
    return bEmailAddress



def isNoEmailAddress( s ):
    #
    '''
    returns negative of isEmailAddress(s)
    '''
    #
    return not isEmailAddress( s )




def isOKasEmail( sEmail ):
    #
    '''
    OK 'susan prewitt <susan.prewitt@algorithmics.com>'
    OK 'bill@microsoft.com, sergy@google.com'
    '''
    #
    from Collect.Query  import get1stThatMeets
    from eMail.Get      import getRealEmail, getEmailListFromString
    from Iter.AllVers   import iMap
    #
    lEmails = iMap( getRealEmail, getEmailListFromString( sEmail ) )
    #
    return get1stThatMeets( lEmails, isEmailAddress )



def isNotOKasEmail( sEmail ):
    #
    return not isOKasEmail( sEmail )


def isSentBefore( oSentBefore, lSendNow ):
    #
    from Collect.Test import ContainsAll
    #
    return oSentBefore and ContainsAll( oSentBefore, lSendNow )



def _getDivider( bHtml = True, bDouble = False ):
    #
    if bHtml:
        sDivide = '<HR>'
    else:
        sDivide = '\n##########################################################'
    #
    if bDouble:
        #
        sDivide = '%s%s\n' % ( sDivide, sDivide )
        #
    else:
        #
        sDivide =   '%s\n' % sDivide
        #
    #
    return sDivide



sToRowHTML = '''
    <tr>
      <td>%s:</td>
      <td>&nbsp;&nbsp;</td>
      <td>%s</td>
    </tr>'''


sToTableHTML = '''
<table>
  <tbody>%s
  </tbody>
</table>
'''

sToTableText = '''
%s'''

def _getRow( sWhat, sContent, bHtml = True ):
    #
    if sContent == 'None': return ''
    #
    if bHtml:
        #
        sTo = sToRowHTML % ( sWhat, sContent )
        #
    else:
        #
        sTo = '%s:     ' % sWhat
        #
        sTo = sTo[ : 5 ] +  sContent + '\n'
        #
    #
    return sTo


tToTable = ( sToTableText, sToTableHTML )


_dReplaceChevrons = { '<' : '&lt;', '>' : '&gt;' }
#
_oGetChevronCodes = _getSwapper( _dReplaceChevrons, bEscape = False )


def _getSayAdds( uTo ):
    #
    sSayAdd = repr( uTo )
    #
    if sSayAdd.startswith( "'" ) and sSayAdd.endswith( "'" ):
        #
        sSayAdd = sSayAdd[ 1 : -1 ]
    #
    return _oGetChevronCodes( sSayAdd )


def _getToTable( uTo, uCC, uBcc, bHtml, sFrom, sSubject, **kwargs ):
    #
    from Iter.AllVers import iMap, lZip
    #
    def getRow( t ):
        #
        sWhat, sContent = t
        #
        return _getRow( sWhat, sContent, bHtml )
    #
    lTos = iMap( _getSayAdds, ( uTo, uCC, uBcc ) )
    #
    lPairs = lZip( ( 'To', 'cc', 'bcc' ), lTos )
    #
    if not lPairs[2][1]:
        #
        del lPairs[2] # no bcc, d/n include the line
        #
    #
    sRows = ''.join( [ getRow( t ) for t in lPairs ] )
    #
    if sFrom:       sRows += getRow( ( 'From', _getSayAdds( sFrom ) ) )
    #
    if sSubject: sRows += getRow( ( 'Subject', sSubject ) )
    #
    for k, v in _getItemIter( kwargs ):
        #
        sRows += getRow( ( k, _getSayAdds( v ) ) )
        #
    #
    sToTable = tToTable[ bHtml ]
    #
    return sToTable % sRows



def _getShowEmail(
        d, getMsgInfo, bHtml = True, sFrom = '', sSubject = '', **kwargs ):
    #
    from eMail.Get  import getAddresseeStrOffSeq
    from eMail.Get  import getHyphen
    #
    sText, uTo, uCC, uBcc = getMsgInfo( d )
    #
    sTo     = getAddresseeStrOffSeq( uTo  )
    sCC     = getAddresseeStrOffSeq( uCC  )
    sBcc    = getAddresseeStrOffSeq( uBcc )
    #
    MsgKwargs   = {}
    #
    if kwargs:
        #
        for k, v in _getItemIter( kwargs ):
            MsgKwargs[ getHyphen( k ) ] = v( d )
        #
    #
    sFrom    = sFrom    % d
    sSubject = sSubject % d
    #
    sToTable = _getToTable( sTo, sCC, sBcc, bHtml, sFrom, sSubject, **MsgKwargs )
    #
    sDivide  = _getDivider( bHtml )
    #
    return sToTable + sDivide + sText



def _dumpThisOne( sSubject, oSubjDone, d, getMsgInfo ):
    #
    '''
    for oSubjDone,
    you can import dCounting or
    use a set (non-frozen)
    '''
    #
    bDumpThis = True
    #
    if oSubjDone is not None:
        #
        if '%(' in sSubject:
            #
            getMsgInfo( d )
            #
            sThisSubject = sSubject % d
            #
        #
        if sThisSubject in oSubjDone:
            #
            bDumpThis = False
            #
        #
        oSubjDone.add( sThisSubject )
        #
    #
    return bDumpThis



def dumpEmailBodies2Temp( l, getMsgInfo,
        sFrom       = None,
        sSubject    = None,
        bHtml       = True,
        oSubjDone   = None,
        bGetLast    = False,
        **kwargs ):
    #
    '''
    for oSubjDone,
    you can import dCounting or
    use a set (non-frozen)
    '''
    #
    from Dict.Get       import getValueIter, getKeyList
    from Dir.Get        import sTempDir
    from eMail.Get      import getHyphen
    from File.Write     import putCsvOut, QuietDump
    from Iter.Get       import getListSwapValueKey
    #
    if sFrom    is None: sFrom    = ''
    if sSubject is None: sSubject = ''
    #
    if bGetLast: # get last email for each unique subject
        #
        dEmails = {}
        #
        if type( l ) == dict:
            #
            iDicts = getValueIter( l )
            #
        else:
            #
            iDicts = l
            #
        #
        for d in iDicts:
            #
            sShowEmail  = _getShowEmail( d, getMsgInfo, bHtml, sFrom, sSubject, **kwargs )
            #
            sThisSubject = sSubject % d
            #
            dEmails[ sThisSubject ] = sShowEmail
            #
            if oSubjDone is not None: oSubjDone.add( sThisSubject )
            #
        #
        lSubjects = getKeyList( dEmails )
        #
        lSubjects.sort()
        #
        lEmails = [ dEmails[ k ] for k in lSubjects ]
        #
    elif type( l ) == dict:
        #
        d = l
        #
        lEmails = [ _getShowEmail(
                        d[k], getMsgInfo, bHtml, sFrom, sSubject, **kwargs )
                    for k in d
                    if _dumpThisOne( sSubject, oSubjDone, d[k], getMsgInfo ) ]
        #
    else:
        #
        lEmails = [ _getShowEmail( d, getMsgInfo, bHtml, sFrom, sSubject, **kwargs )
                    for d in l
                    if _dumpThisOne( sSubject, oSubjDone, d, getMsgInfo ) ]
        #
    #
    sDivide = _getDivider( bHtml, bDouble = True )
    #
    QuietDump( sDivide.join( lEmails ), 'temp.html' )
    #
    if oSubjDone is not None:
        #
        lCounts = getListSwapValueKey( _getItemIter( oSubjDone ) )
        #
        lCounts.sort()
        lCounts.reverse()
        #
        lCounts[0:0] = [ ( 'count', 'subject' ) ]
        putCsvOut( lCounts, sTempDir, 'subject_counts.csv' )
        
        
        
    



if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if          isEmailAddress( '~!@#$%^&*()@gmail.com' ) or \
                isEmailAddress( '999'                   ) or \
                isEmailAddress( 'none3@thistime'        ) or \
                isEmailAddress( 'aar..igator@gmail.com' ) or \
            not isEmailAddress( 'aardvigator@gmail.com' ):
        #
        lProblems.append( 'isEmailAddress()' )
    #
    if          isEmailAddress( 'aardvigator@noemail.com' ):
        #
        lProblems.append( 'isEmailAddress() noemail.com' )
    #
    oSentBefore = [ 'bill@microsoft.com', 'sergy@google.com', 'larry@oracle.com' ]
    #
    lSendNow1   = [ 'bill@microsoft.com', 'sergy@google.com' ]
    lSendNow2   = [ 'melinda@microsoft.com', 'larry@google.com' ]
    #
    if      not isSentBefore( oSentBefore, lSendNow1 ) or \
                isSentBefore( [],          lSendNow1 ) or \
                isSentBefore( oSentBefore, lSendNow2 ):
        #
        lProblems.append( 'isSentBefore()' )
        #
    #
    sTest = 'susan.prewitt@algorithmics.com <susan.prewitt@algorithmics.com>'
    #
    if      not isOKasEmail( ', '.join( lSendNow1 ) ) or \
            not isOKasEmail( sTest ) or \
                isOKasEmail( 'xyz' ):
        #
        lProblems.append( 'isOKasEmail()' )
        #
    #
    #
    sayTestResult( lProblems )