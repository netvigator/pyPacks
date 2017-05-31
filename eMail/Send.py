#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Mail functions Send
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
# self test actually tries to send email, so need working internet

from os.path        import join

from six            import print_ as print3

from Dict.Get       import getItemIter        as _getItemIter
from String.Encrypt import DecryptLite, Decrypt
from String.Test    import getHasSubstrTester as _getHasSubstrTester
from Utils.Config   import getConfDict, getBoolOffYesNoTrueFalse

tryAgain = _getHasSubstrTester( '(No route to host|TimeOverExcept)' )

class AttachmentFailure( Exception ): pass


dMailConf           = getConfDict('Mail.conf')

sServerOut          = dMailConf['main']['outgoingmailserver']

bOutAuthenticate    = getBoolOffYesNoTrueFalse(
                      dMailConf['main'].get( 'outgoingauthenticate', 'no' ) )

sUserName           = dMailConf['main'].get( 'username', None )
sPassword           = dMailConf['main'].get( 'password', None )

bEncryptConnect     = getBoolOffYesNoTrueFalse(
                      dMailConf['main'].get( 'outgoingsecure', 'no' ) )

sOutgoSecurityType  = dMailConf['main'].get( 'outgoingsecuritytype', None )

iPort               = dMailConf['main'].get( 'outgoingmailport', None )

bLiteEncryption     = getBoolOffYesNoTrueFalse(
                      dMailConf['main'].get( 'liteencryption', 'yes' ) )


if iPort is None and bEncryptConnect:
    #
    iPort = 465            
    #
elif iPort is None:
    #
    iPort = 25
    #
else:
    #
    iPort = int( iPort )
    #

if sOutgoSecurityType is None and bEncryptConnect:
    #
    sOutgoSecurityType = 'SSL'
    #
elif sOutgoSecurityType:
    #
    sOutgoSecurityType = sOutgoSecurityType.upper()
    #


iPause              = int(
                      dMailConf['main'].get( 'pause', '5' ) )

if bLiteEncryption:
    #
    fDecrypt = DecryptLite
    #
else:
    #
    fDecrypt = Decrypt
    #

# oConf




def _hasSSL():
    #
    import smtplib
    #
    return 'SMTP_SSL' in dir( smtplib )





def _getMIMEmessage(
        sFrom,
        uTo,
        sSubject,
        sBody,
        uCC         = None,
        bHtmlMsg    = False,
        sCharSet    = 'UTF-8',
        lAttachments= [],
        **kwargs ):
    #
    # other mail headers can go in kwargs
    # eg Return-Path
    #
    # from email.MIMEText import MIMEText
    #
    import base64, quopri
    #
    from cStringIO              import StringIO
    from email                  import encoders
    from email                  import Utils
    from email.Message          import Message
    from email.mime.base        import MIMEBase
    from email.mime.multipart   import MIMEMultipart
    from email.mime.text        import MIMEText
    from mimetypes              import guess_type
    from os.path                import basename
    #
    from eMail.Get              import getAddresseeStrOffSeq
    from File.Test              import isFileThere
    from Iter.AllVers           import tFilter

    #
    if lAttachments:
        #
        iLenBeg     = len( lAttachments )
        #
        tThere      = tFilter( isFileThere, lAttachments )
        #
        if len( tThere ) < iLenBeg:
            #
            lCannotFind = [ s for s in lAttachments if s not in tThere ]
            #
            print3( 'Cannot find attachment', ', '.join( lCannotFind ) )
            #
            raise AttachmentFailure
            #
        #
    #
    sType           = 'plain'
    #
    if bHtmlMsg:
        #
        sType       = 'html'
        #
    #
    if lAttachments:
        #
        oMsg        = MIMEMultipart()
        #
        oMsg.attach( MIMEText( sBody, sType, sCharSet ) )
        #
    else:
        #
        oMsg        = MIMEText( sBody, sType, sCharSet )
        #
    #
    if bHtmlMsg:
        #
        oMsg.set_default_type( 'message/rfc822' )
        #
    #
    oMsg[ 'To' ]            = getAddresseeStrOffSeq( uTo )
    oMsg[ 'From' ]          = sFrom
    #
    if uCC is not None:
        #
        oMsg[ 'CC' ]        = getAddresseeStrOffSeq( uCC )
        #
    #
    oMsg[ 'Subject' ]       = sSubject
    oMsg[ 'Date' ]          = Utils.formatdate( localtime = 1 )
    oMsg[ 'Message-ID' ]    = Utils.make_msgid()
    #
    for sFileSpec in lAttachments:
        #
        if not isFileThere( sFileSpec ): continue
        #
        sContentType,sEncoding = guess_type(sFileSpec)
        #
        if sContentType is None or sEncoding is not None:
            # If no guess, use generic opaque text
            sContentType = "application/octet-stream"
        #
        sMainType, sSubType = sContentType.split('/', 1)
        #
        if sMainType == 'text':
            oFile = open(sFileSpec)
            # Note: we should handle calculating the charset
            oAttach = MIMEText(oFile.read(), _subtype = sSubType)
        elif sMainType == 'image':
            oFile = open(sFileSpec, 'rb')
            oAttach = MIMEImage(oFile.read(), _subtype = sSubType)
        elif sMainType == 'audio':
            oFile = open(sFileSpec, 'rb')
            oAttach = MIMEAudio(oFile.read(), _subtype = sSubType)
        else:
            oFile = open(sFileSpec, 'rb')
            oAttach = MIMEBase(sMainType, sSubType)
            oAttach.set_payload(oFile.read())
            # Encode the payload using Base64
            encoders.encode_base64(oAttach)
        #
        oFile.close()
        #
        oAttach.add_header(
            'Content-Disposition',
            'attachment; filename="%s"' % basename( sFileSpec ) )
        oMsg.attach(oAttach)
    #
    for k, v in _getItemIter( kwargs ):
        #
        oMsg[ k ] = v
        #
    #
    if bHtmlMsg:
        #
        oMsg.set_default_type( 'message/rfc822' )
        #
    #
    return oMsg.as_string()


def AddresssString2List( uTo ):
    #
    from Iter.AllVers import lMap
    from Collect.Test import isListOrTuple
    from String.Get   import getStripped
    from String.Split import getSplitButNotIfQuoted
    #
    if uTo is None:
        #
        lTo     = []
        #
    elif isListOrTuple( uTo ):
        #
        lTo = list( uTo )
        #
    else:
        #
        # lTo = [ s.strip() for s in uTo.split( ',' ) ]
        #
        lTo = lMap( getStripped, getSplitButNotIfQuoted( uTo, ',' ) )
        #
    #
    return lTo



def _getSayTo( uTo ):
    #
    from Collect.Test   import isListOrTuple
    #
    sSayTo = uTo
    #
    if isListOrTuple( uTo ): sSayTo = ', '.join( uTo )
    #
    return sSayTo


def _putErrorMsg( uTo, oExceptMsg, oTraceBack, sErrorFile, sMsg ):
    #
    from sys            import exc_info
    #
    from Dir.Get        import sTempDir
    from File.Write     import openAppendClose, QuickDump
    from Time.Output    import sayGMT
    #
    if sErrorFile is None:
        #
        print3( '*** message may not have been sent! ***' )
        print3( uTo )
        print3( oExceptMsg )
        try:
            oTraceBack.print_stack()
        except AttributeError:
            #
            error, msg, traceback = exc_info()
            #
            print3( error, msg )
            print3( dir( oTraceBack ) )
        #
    else:
        #
        sOut = '%s\n%s\n\n' % ( _getSayTo( uTo ), repr( oExceptMsg ) )
        #
        openAppendClose( sOut, sErrorFile, bSayBytes = False )
        #
    #
    QuickDump(  sMsg,
                sTempDir, 'email_mime_%s.txt' % sayGMT( sBetween = '_' ),
                bSayBytes = False )
    


def _putSentLog( uTo, sSendFile ):
    #
    from Collect.Test   import isListOrTuple
    from File.Write     import openAppendClose
    #
    if sSendFile is not None:
        #
        if not isListOrTuple( uTo ): uTo = [ uTo ]
        #
        sOut = '%s\n' % '\n'.join( uTo )
        #
        openAppendClose( sOut, sSendFile, bSayBytes = False )
        #



def SendOneMessage( sServerOut, sFrom, uTo, sSubject, sBody,
        uCC                 = None,
        uBcc                = None,
        sUserName           = None,
        sPassword           = None,
        sErrorFile          = None,
        sSendFile           = None,
        oSentB4             = [],
        fDecryptPassword    = fDecrypt,
        bEncryptConnect     = False,
        bHtmlMsg            = False,
        sCharSet            = 'UTF-8',
        bAppendCodes        = False,
        oRecipient          = None,
        iPort               = iPort,
        lAttachments        = [],
        **kwargs ):
    #
    # kwargs values must be strings!!!
    #
    from smtplib            import SMTPException
    #from File.Write         import MakeTemp
    #
    class SMTPSSLException( SMTPException ): pass
    #
    if sOutgoSecurityType == 'TLS':
        #
        from smtplib        import SMTP
        #
    elif bEncryptConnect and _hasSSL():
        #
        from smtplib       import SMTP_SSL as SMTP
        #
    elif bEncryptConnect:
        #
        from ssmtplib       import SMTP_SSL as SMTP
        from ssmtplib       import SMTPSSLException
        #
    else:
        #
        from smtplib        import SMTP
        #
    #
    from socket             import gaierror, error, herror
    from sys                import exc_info
    #
    from String.Encrypt     import XOREncrypt
    from String.Output      import WordWrapText
    from eMail.Test         import isSentBefore
    from Utils.TimeLimit    import TimeLimitWrap, TimeOverExcept
    from Web.Address        import getToplessHost
    #
    if '%(' in sSubject and oRecipient is not None:
        #
        sSubject    = sSubject % oRecipient
        #
    #
    if '%(' in sFrom and oRecipient is not None:
        #
        sFrom       = sFrom % oRecipient
        #
    #else:
        ##
        #print3( 'sFrom:', sFrom )
        #print3( 'oRecipient:', oRecipient )
        #
    #
    sCodes      = ''
    #
    if bAppendCodes:
        #
        sCodes  = '\n%s' % XOREncrypt( getToplessHost( sServerOut ) )
        #
    #
    sMsg = _getMIMEmessage(
            sFrom,
            uTo,
            sSubject,
            WordWrapText( sBody + sCodes, 72 ),
            uCC,
            bHtmlMsg,
            sCharSet,
            lAttachments,
            **kwargs )
    #
    lRecipients = AddresssString2List( uTo ) + \
                  AddresssString2List( uCC ) + \
                  AddresssString2List( uBcc )
    #
    iSent = iTries = 0
    #
    # MakeTemp( '\n\n\n'.join( ( sFrom, '\n'.join( lRecipients ), sMsg ) ), bSayBytes = False )
    #
    if sPassword and fDecryptPassword:
        #
        sPassword = fDecryptPassword( sPassword )
    #
    while not isSentBefore( oSentB4, lRecipients ):
        #
        # while loop allows resend if the send times out
        #
        try:
            #
            # print3( 'try to connect', sServerOut, iPort )
            #
            # oSMTP   = TimeLimitWrap( 60, SMTP, sServerOut, iPort )
            #
            oSMTP   = SMTP( sServerOut, iPort )
            #
            # print3( 'connected' )
            #
            if sOutgoSecurityType == 'TLS':
                #
                oSMTP.starttls()
                #
                oSMTP.ehlo()
                #
            #
            # print3( 'started TLS' )
            #
            if sUserName and sPassword:
                #
                # print3( 'try to login' )
                #
                try:
                    #
                    # TimeLimitWrap( 60, oSMTP.login, sUserName, sPassword )
                    #
                    oSMTP.login( sUserName, sPassword )
                    #
                except ( SMTPException, SMTPSSLException ):
                    #
                    error, msg, traceback = exc_info()
                    #
                    _putErrorMsg( uTo, msg, traceback, sErrorFile, sMsg )
                    #
                    return 0
                #
            #
            try:
                #
                # TimeLimitWrap( 60, oSMTP.sendmail, sFrom, lRecipients, sMsg )
                #
                oSMTP.sendmail( sFrom, lRecipients, sMsg )
                #
            finally:
                #
                oSMTP.close()
                #
            #
            iSent   = 1
            #
            if sSendFile is not None:
                #
                _putSentLog( lRecipients, sSendFile )
                #
            #
        except ( error, TimeOverExcept ):
            #
            error, msg, traceback = exc_info()
            #
            if tryAgain( repr( msg ) ) and iTries < 2:
                #
                iTries += 1
                #
                continue
                #
            else:
                #
                _putErrorMsg( uTo, msg, traceback, sErrorFile, sMsg )
                #
        except ( gaierror, herror, SMTPException, SMTPSSLException ):
            #
            error, msg, traceback = exc_info()
            #
            _putErrorMsg( uTo, msg, traceback, sErrorFile, sMsg )
            #
        #
        break
        #
    #
    return iSent




def SendEmailsOffList( l,
        sFrom,
        fGetMsgInfo,
        sSubject,
        bHtmlMsg        = False,
        sCharSet        = 'UTF-8',
        oSentB4         = [],
        fDecryptPassword= fDecrypt,
        lAttachments    = [],
        bOuputListOnly  = 0,
        **kwargs ):
    #
    # kwargs values must be a function returning strings!!!
    # one arg, the recipient object (dict)
    #
    '''
    Function fGetMsgInfo must return sBody, uTo, uCC, uBcc from list item.
    '''
    #
    from sys                import stdout
    from time               import sleep
    #
    from Dir.Get            import sDurableTempDir
    from eMail.Get          import getHyphen
    from eMail.Test         import isSentBefore
    from String.Output      import Plural, ReadableNo
    from Time.Output        import sayGMT
    from Utils.Progress     import TextMeter, DummyMeter
    #
    sGMT = sayGMT( sBetween = '_' )
    #
    sErrorFile  = join( sDurableTempDir, 'email_errors_%s.txt'  % sGMT )
    sSendFile   = join( sDurableTempDir, 'email_sendlog_%s.txt' % sGMT )
    sAsIfFile   = join( sDurableTempDir, 'email_AsIfLog_%s.txt' % sGMT )
    #
    oSentB4         = frozenset( oSentB4 )
    #
    # sServerOut  = oConf.get( 'main', 'OutgoingMailServer' )
    #
    sCC             = None
    #
    bUseHours       = len( l ) * iPause > 0.5 * 3600
    #
    oProgressMeter  = DummyMeter()
    #
    if stdout.isatty():
        #
        oProgressMeter = TextMeter( use_hours = bUseHours )
        #
    #
    iSent   = 0
    iSeq    = 0
    #
    sShowText = "%s recipients" % ReadableNo( len( l ) )
    #
    oProgressMeter.start( len( l ), sShowText, 'Sending emails to ...' )
    #
    for oRecipient in l:
        #
        if isinstance( l, dict ):
            #
            oRecipient = l.get( oRecipient )
            #
        #
        iSeq  += 1
        #
        oProgressMeter.update( iSeq )
        #
        sBody, uTo, uCC, uBcc = fGetMsgInfo( oRecipient )
        #
        lRecipients = AddresssString2List( uTo ) + \
                      AddresssString2List( uCC ) + \
                      AddresssString2List( uBcc )
        #
        MsgKwargs = {}
        #
        if kwargs:
            #
            for k, v in _getItemIter( kwargs ):
                MsgKwargs[ getHyphen( k ) ] = v( oRecipient )
            #
        #
        if isSentBefore( oSentB4, lRecipients ):
            #
            iSent += 1
            #
        elif bOuputListOnly:
            #
            iSent += 1
            #
            _putSentLog( lRecipients, sAsIfFile )
            #
        else:
            #
            iSent += SendOneMessage(
                        sServerOut, sFrom, uTo, sSubject, sBody,
                        uCC                 = uCC,
                        uBcc                = uBcc,
                        sUserName           = sUserName,
                        sPassword           = sPassword,
                        sErrorFile          = sErrorFile,
                        sSendFile           = sSendFile,
                        oSentB4             = oSentB4,
                        bEncryptConnect     = bEncryptConnect,
                        bHtmlMsg            = bHtmlMsg,
                        sCharSet            = sCharSet,
                        fDecryptPassword    = fDecryptPassword,
                        oRecipient          = oRecipient,
                        iPort               = iPort,
                        lAttachments        = lAttachments,
                        **MsgKwargs )
            #
            if iSeq < len( l ): sleep( iPause )
            #
        #
    #
    oProgressMeter.end( len( l ) )
    #
    if iSent < len( l ):
        #
        print3( '\nsent only %s email%s ....' % ( iSent, Plural( iSent ) ) )
        print3( 'error list in %s' % sErrorFile )
    #





sBodyPlain = \
'''This is the body.
More body.

Still more.

Regards,'''

sBodyHtml = \
'''<img src="https://www.democratsabroad.org/sites/default/files/DAandMonuments.jpg"><br>
<br>
<br>
Hello %(sFirst)s,<br><br>

This is <STRONG>the body</STRONG>.<br>
More body.<br><br>

<EM>Still more</EM>.<br><br>

Regards,<br><br>

The Boss<br>'''


def getMessageBody( sBody, dMember ):
    #
    return sBody % dMember



if __name__ == "__main__":
    #
    lProblems = []
    #
    from time           import sleep
    #
    from Dir.Get        import sTempDir
    from eMail.Get      import getRealPerCent
    from File.Write     import MakeTemp
    from Utils.Result   import sayTestResult
    #
    # sServerOut   = oConf.get( 'main',        'OutgoingMailServer' )
    #
    sCC             = None
    #
    #sFrom       = oConf.get( 'main', 'From' )
    sFrom       = getRealPerCent( '"cPC(sFromName)s" <cPC(sFromEmail)s>' )
    #
    sSubject    = 'single troubleshooting'
    #
    sTo         = '"Joe Blow" <gravesr@hutchcity.com>'
    # sTo       = '"Rick Graves" <gravesricharde@yahoo.com>'
    sCC         = '"Oscar Zilch" <aardvigator@gmail.com>'
    #
    oRecipient  = dict(
                sFromEmail = 'gravesricharde@yahoo.com',
                sFromName  = "Rick Graves" )
    #
    bHtmlMsg    = True
    #
    dAddressee = dict( sFirst = 'Joe' )
    #
    kwargs      = { 'Return-Path' : '<gravesricharde-bounces@yahoo.com>' }
    #
    sMessage    = 'This is a test!'
    #
    # print3( type( sMessage ) )
    #
    MakeTemp( sMessage, bSayBytes = False )
    #
    #
    print3( 'Sending single email message ...' )
    #
    SendOneMessage(
            sServerOut, sFrom, sTo, sSubject,
            getMessageBody( sBodyHtml, dAddressee ),
            uCC             = sCC,
            sUserName       = sUserName,
            sPassword       = sPassword,
            bEncryptConnect = bEncryptConnect,
            bHtmlMsg        = bHtmlMsg,
            fDecryptPassword= fDecrypt,
            oRecipient      = oRecipient,
            iPort           = iPort,
            lAttachments    = [],
            **kwargs )
    #
    print3( 'Single send attempt finished ...' )
    #
    sleep( 5 )
    #
    def getReturnPath( u ): return '<gravesricharde@yahoo.com>'
    #
    kwargs      = { 'Return-Path' : getReturnPath }
    #
    sSubject    = 'list troubleshooting'
    #
    lAddressees = [
            dict(
                sFirst     = 'Barney',
                sTo        = '"Barney Rubble" <gravesr@hutchcity.com>',
                sFromEmail = 'gravesricharde@yahoo.com',
                sFromName  = "Rick Graves" ),
            dict(
                sFirst     = 'Fred',
                sTo        = '"Fred Flintstone" <aardvigator@gmail.com>',
                sFromEmail = 'gravesricharde@yahoo.com',
                sFromName  = "Rick Graves" ) ]
    #
    lAddressees = [
            dict(
                sFirst     = 'Gail',
                sTo        = 'Gail Ann Fagen <gafagen@alice.it>',
                sFromEmail = 'gravesricharde@yahoo.com',
                sFromName  = "Rick Graves" ),
            dict(
                sFirst     = 'Shari',
                sTo        = '"Shari Temple" <shari_temple@democratsabroad.org>',
                sFromEmail = 'gravesricharde@yahoo.com',
                sFromName  = "Rick Graves" ) ]
    #
    def getMsgInfo( d ):
        #
        sBody   = getMessageBody( sBodyHtml, d )
        uTo     = d.get( 'sTo' )
        uCC     = d.get( 'uCC' )
        uBcc    = d.get( 'uBcc' )
        #
        return sBody, uTo, uCC, uBcc
    #
    #   lAttachments    = [],
    #
    SendEmailsOffList( lAddressees,
        sFrom,
        getMsgInfo,
        sSubject,
        bHtmlMsg        = True,
        oSentB4         = [],
        fDecryptPassword= fDecrypt,
        lAttachments    = [ join( sTempDir, 'temp.txt' ) ],
        **kwargs )
    #
    sayTestResult( lProblems )
    # self test actually tries to send email, so need working internet