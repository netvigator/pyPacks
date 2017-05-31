#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# looking for  getPageContent(

from sys                import stderr
from os                 import remove
from time               import time

from six                import print_ as print3

from twisted.internet   import reactor
from twisted.web        import client

from FileMethods        import getFileContent, getTempFile
from ListMethods        import isListOrTuple, getRandoms, getAllIndexes, FifoPopper
from ObjMethods         import getPropertyValue, ObserverClass, ValueContainer
from ComboMethods       import No, Any
from DateMethods        import sayLocalTime, getSayDurationAsDaysHrsMinsSecs
from StringMethods      import ReadableNo, Plural
from WebMethods         import isURL, getPlainIfZipped
from IterMethods        import isIterator



USER_AGENT  = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.8) ' \
              'Gecko/20061108 Fedora/1.5.0.8-1.fc5 Firefox/1.5.0.8'

dHEADERS    = {
        'accept' : 'text/xml,application/xml,application/xhtml+xml,text/html;' \
                 'q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
        'accept-charset'  : 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'accept-encoding' : 'gzip,deflate',
        'accept-language' : 'en-us,en;q=0.5' }




class getPagesClass( ObserverClass ):
    #
    """
    This class is closed to modification but open to extension !!!
    The "abstract methods" are doOnSuccess and doOnFailure --
    you can either delegate to or override those.  Take a look !!!

    You can pass a list of 1) URL's, 2) dictionaries, or 3) objects.
    If you pass a list of dictionaries, the URL must be in an item with key 'sURL'.
    If you pass a list of objects, each object must have a sURL property.

    Implements observer design pattern.
    Clients can subscribe/unsubscribe by calling
    registerObserver( self )/removeObserver( self )
    (self would be a reference to the client object).
    Either that, or pass observers to constructor
    on instantiation (param name is uObservers).
    Clients must implement update() method.
    This (subject) will pass dictionary of values to clients (observers).
    """
    #
    def __init__( self,
            uPages          = [],
            iMax            = 5,
            bSayEachResult  = False,
            dHeaders        = dHEADERS,
            sAgent          = USER_AGENT,
            bPartialOK      = True,
            bDeleteTmpFile  = True,
            bGetGoing       = True,
            uObservers      = None ):
        #
        if isinstance( uPages, str): uPages = [ uPages ]
        #
        self.lPages         = list( uPages )
        #
        self.lURLsFiFo      = FifoPopper( self.lPages )
        #
        self.lDownLoading   = []
        self.bNoMorePages   = False
        self.lFinished      = []
        #
        self.iMax           = iMax
        self.bSayEachResult = bSayEachResult
        self.dHeaders       = dHeaders
        self.sAgent         = sAgent
        self.bPartialOK     = bPartialOK
        self.bDeleteTmpFile = bDeleteTmpFile
        #
        self.holdActive     = None
        #
        self.lSubscribers   = [] # observer clients
        #
        self.iCompleted     = 0
        self.iInvalid       = 0
        #
        self.dLastState     = {}
        #
        self.bReactorOn     = False # reactor.running may not return correct value instantly
        self.bFinished      = False
        #
        self.dBegEndTimes   = {}
        #
        ObserverClass.__init__( self, uObservers )
        #
        if bGetGoing:
            #
            self.getGoing()
        #
    #
    def getGoing( self, iSlot2Avoid = None ):
        #
        iSlot               = 0
        #
        while iSlot is not None:
            #
            iSlot           = self.doNext( iSlot2Avoid = iSlot2Avoid, bUpdate = False )
            #
            if self.bFinished: break
            #
        #
        self.getStarted()
        #
    def getStarted( self ):
        #
        if not self.bFinished and not reactor.running and Any( self.lDownLoading ):
            #
            if self.bSayEachResult:
                print3( 'Starting reactor ...' )
            #
            self.bReactorOn = True
            #
            self.statusChanged()
            #
            reactor.run()
            #
        #
    #
    def statusChanged( self, bUpdate = True ):
        #
        if bUpdate:
            #
            iTotal  = len( self.lPages ) + len( self.lFinished )
            #
            iActive = self.getActives()
            #
            dStatus = dict(
                        bFinished   = self.bFinished,
                        bReactorOn  = self.bReactorOn,
                        iTotal      = iTotal,
                        iCompleted  = self.iCompleted,
                        iInvalid    = self.iInvalid,
                        iActive     = iActive )
            #
            if self.dLastState != dStatus:
                #
                self.notifyObservers( dStatus ) # in ObserverClass
                #
                self.dLastState = dStatus
    #
    def getActives( self ):
        #
        from Iter.AllVers import tFilter
        #
        return len( tFilter( bool, self.lDownLoading ) )
        #
    #
    def AppendOrExtend( self, uAdd, iSlot = None ):
        #
        lAdd                = uAdd
        #
        if isIterator( uAdd ):
            #
            uAdd            = list( uAdd )
            #
        elif not isListOrTuple( uAdd ):
            #
            lAdd            = [ uAdd ]
            #
        #
        iAddMore            = len( lAdd )
        #
        if self.bNoMorePages:
            #
            # self.lFinished.extend( self.lPages )
            #
            self.getFinished()
            #
            self.lPages     = lAdd
            #
        else:
            #
            self.lPages.extend( lAdd )
            #
        #
        self.lURLsFiFo.extend( lAdd )
        #
        self.bNoMorePages      = False
        #
        if iAddMore > 0:
            #
            self.statusChanged()
            #
        #
        if iAddMore > 0 and iSlot is not None:
            #
            self.holdActive = self.lDownLoading[ iSlot ]
            #
            self.doNext()       # use next slot
            #
            self.lDownLoading[ iSlot ] = None
            #
            if iAddMore == 1:
                #
                self.getStarted()
                #
        if iAddMore > 1:
            #
            self.getGoing( iSlot2Avoid = iSlot )
            #
        #
    #
    def getFinished( self ):
        #
        self.lFinished.extend( self.lPages )
        #
        self.lPages = []
        #
        return self.lFinished
        #
    #
    def doNext( self, iSlot = None, iSlot2Avoid = None, bUpdate = True ):
        #
        from six            import next as getNext
        #
       #from Utils.Both2n3  import getNext
        #
        sURL                = None
        uNext               = None
        dMoHeaders          = None
        dNewHeaders         = None
        #
        bChange             = False
        #
        if iSlot is None:
            #
            iSlot           = self.getDownLoadSlot( iSlot2Avoid = iSlot2Avoid )
            #
        #
        if iSlot is not None and not self.bNoMorePages:
            #
            while sURL is None:
                #
                uNext               = getNext( self.lURLsFiFo )
                #
                if uNext is None:
                    #
                    self.bNoMorePages  = True
                    #
                    sURL            = None
                    #
                    if self.bSayEachResult:
                        print3( 'URL list is finished' )
                    #
                    break
                    #
                else: # if uNext is not None:
                    #
                    sURL            = self.GetNextURL( uNext )
                    #
                    dMoHeaders, dNewHeaders = self.GetMoreHeaders( uNext )
                    #
                    if not isURL( sURL ):
                        #
                        if self.bSayEachResult:
                            print3( '"%s" is not a URL' % sURL )
                        #
                        sURL        = None
                        #
                        self.iInvalid   += 1
                        #
                    elif sURL:
                        #
                        bChange     = True
                        #
                        if self.bSayEachResult:
                            print3( 'next URL is %s' % sURL )
                    #
        if iSlot is not None:
            #
            if sURL:
                #
                sTempFile = getTempFile()
                #
                dHeaders = self.dHeaders
                #
                if dNewHeaders:
                    #
                    dHeaders = dNewHeaders
                    #
                elif dMoHeaders:
                    #
                    dHeaders = self.dHeaders.copy()
                    #
                    dHeaders.update( dMoHeaders )
                    #
                #
                oDownLoad = client.downloadPage(
                    sURL,
                    sTempFile,
                    headers         = dHeaders,
                    agent           = self.sAgent,
                    supportPartial  = self.bPartialOK )
                #
                # uNext comes in as uThis in doOnSuccess and doOnFailure
                #
                self.dBegEndTimes[ sURL ] = ValueContainer( nBeg = time(), nEnd = 0.0 )
                #
                oDownLoad.addCallback( self.doOnSuccess, sURL, uNext, sTempFile, iSlot )
                oDownLoad.addErrback(  self.doOnFailure, sURL, uNext, sTempFile, iSlot )
                #
                self.lDownLoading[ iSlot ] = oDownLoad
                #
                if self.bSayEachResult:
                    print3( 'started download using slot %s' % iSlot )
            #
            else:
                #
                if self.lDownLoading[ iSlot ]:
                    #
                    if self.bSayEachResult:
                        print3( 'wiping slot %s' % iSlot )
                    #
                    self.lDownLoading[ iSlot ]  = None
                    #
                #
                iSlot                       = None
                #
                bChange                     = True
                #
        #
        if iSlot is None and self.bReactorOn and No( self.lDownLoading ):
            #
            # self.stopReactor()
            #
            if self.bSayEachResult:
                print3( "Stopping reactor" )
            #
            self.bReactorOn = False
            self.bFinished  = True
            #
            reactor.stop()
            #
            self.statusChanged()
            #
        #
        self.statusChanged( bUpdate )
        #
        return iSlot
    #
    def getNextURL( self, uNext ):
        #
        sURL        = None
        #
        if isinstance( uNext, str ):
            #
            sURL    = uNext
            #
        else:
            #
            sURL    = getPropertyValue( uNext, 'sURL' )
            #
        #
        return sURL
    #
    def getMoreHeaders( self, uNext ):
        #
        dMoHeaders      = None
        dNewHeaders     = None
        #
        if not isinstance( uNext, str ):
            #
            dMoHeaders  = getPropertyValue( uNext, 'dMoHeaders' )
            dNewHeaders = getPropertyValue( uNext, 'dNewHeaders' )
            #
        #
        return dMoHeaders, dNewHeaders
    #

    def getPlainText( self, sFileName ):
        #
        return getPlainIfZipped( getFileContent( sFileName ) )



    def getDownLoadSlot( self, iSlot2Avoid = None ):
        #
        from Iter.AllVers import tFilter
        #
        iLen            = len( self.lDownLoading )
        #
        iSlot           = None
        #
        if iLen < self.iMax:
            #
            if iLen > 0 and self.lDownLoading[ iLen -1 ] is None:
                #
                # cosmetic: start using slots in order
                #
                iSlot       = iLen - 1
                #
            else:
                #
                iSlot       = iLen
                #
                self.lDownLoading.append( None )
            #
        elif len( tFilter( bool, self.lDownLoading ) ) < self.iMax:
            #
            if iSlot2Avoid is None:
                #
                try:
                    #
                    iSlot   = self.lDownLoading.index( None )
                    #
                except ValueError:
                    #
                    iSlot   = None
                    #
            else:
                #
                lNotActives = getAllIndexes( self.lDownLoading, None )
                #
                if iSlot2Avoid in lNotActives:
                    #
                    lNotActives.remove( iSlot2Avoid )
                    #
                if len( lNotActives ) > 0:
                    #
                    iSlot   = lNotActives[0]
                    #
        #
        return iSlot




    def sayError( self, oError ):
        #
        sError      = repr( oError )[ 1 : -1 ]
        #
        return sError.split()[ 1 ]




    def getHtmlDelTemp( self, sTempFile ):
        #
        sHTML       = self.GetPlainText( sTempFile )
        #
        if self.bDeleteTmpFile:
            #
            # without the try/except, errors elsewhere can confuse the program;
            # so if there is another error, the try/except here lets other error surface better
            #
            try:
                remove( sTempFile )
            except OSError:
                pass
            #
        #
        return sHTML



    def sayResultMaybe( self, sResult, iSlot ):
        #
        if self.bSayEachResult:
            #
            print3( '%s %s Slot %s' % ( sResult, sayLocalTime(), iSlot ) )


    def sayWhenNothingElse( self, sURL, iBytes, oFailure = None):
        #
        if self.bSayEachResult:
            #
            if oFailure is None:
                #
                sMore = ''
                #
            else:
                #
                sMore = ' on %s' % self.sayError( oFailure )
                #
            #
            sSayDuration = self.getSayDuration( sURL )
            #
            print3( 'got %s bytes after %s%s' % ( ReadableNo( iBytes ), sSayDuration, sMore ) )



    def setEndTime( self, sURL ):
        #
        if sURL in self.dBegEndTimes:
            #
            self.dBegEndTimes[ sURL ].nEnd = time()





    def getSayDuration( self, sURL ):
        #
        if sURL in self.dBegEndTimes:
            #
            oThis   = self.dBegEndTimes[ sURL ]
            #
            if oThis.nEnd:
                #
                sSay= getSayDurationAsDaysHrsMinsSecs( oThis.nBeg, oThis.nEnd )
                #
            else:
                #
                sSay= 'Not over yet!'
                #
            #
        else:
            #
            sSay    = 'Cannot find entry for %s!' % sURL
            #
        #
        return sSay


    def doOnSuccess( self, oSuccess, sURL, uThis, sTempFile, iSlot ):
        #
        """
        This is like an abstract class; you could override it.
        If the list item has a propery doWithSuccess,
        it will be called with the params above.
        (Delegation is considered better than subclassing anyway.)
        Normally, oSuccess is None; it is included so
        doOnSuccess and doOnFailure can be polymorphic and have the same parameters.
        """
        #
        self.setEndTime( sURL )
        #
        self.iCompleted += 1
        #
        self.sayResultMaybe( 'Success', iSlot )
        #
        doWithSuccess   = getPropertyValue( uThis, 'doWithSuccess' )
        #
        sHTML           = self.getHtmlDelTemp( sTempFile )
        #
        if doWithSuccess:
            #
            doWithSuccess( self, sHTML, sURL, uThis, sTempFile, iSlot, oSuccess )
            #
        else:
            #
            self.sayWhenNothingElse( sURL, len( sHTML ) )
            #
        #
        if self.bReactorOn: # reactor.running:
            #
            self.doNext( iSlot )
        #


    def doOnFailure( self, oFailure, sURL, uThis, sTempFile, iSlot ):
        #
        """
        This is like an abstract class; you could override it.
        If the list item has a propery doWithFailure,
        it will be called with the params above.
        (Delegation is considered better than subclassing anyway.)
        Normally, oFailure is an instance of a Twisted exception object.
        doOnSuccess and doOnFailure can be polymorphic and have the same parameters.
        """
        #
        self.setEndTime( sURL )
        #
        self.iCompleted += 1
        #
        self.sayResultMaybe( 'Failure', iSlot )
        #
        doWithFailure = getPropertyValue( uThis, 'doWithFailure' )
        #
        sHTML           = self.getHtmlDelTemp( sTempFile )
        #
        if doWithFailure:
            #
            doWithFailure( self, sHTML, sURL, uThis, sTempFile, iSlot, oFailure )
            #
        else:
            #
            self.sayWhenNothingElse( sURL, len( sHTML ), oFailure )
        #
        if reactor.running:
            #
            self.doNext( iSlot )
        #



def _sayPageInfo( oGetPages, sHTML, sURL, uThis, sTempFile, iSlot, oSuccess ):
    #
    """
    This is part of the demo.
    """
    #
    if oGetPages.bSayEachResult:
        #
        sSayDuration = oGetPages.getSayDuration( sURL )
        #
        print3( 'got %s bytes after %s' % ( ReadableNo( len( sHTML ) ), sSayDuration ) )



def _getLinksSamples( oGetPages, sHTML, sURL, uThis, sTempFile, iSlot, oSuccess ):
    #
    """
    This is part of the demo.
    """
    #
    from Web.HTML import getLinksOffHTML
    #
    lLinks      = getLinksOffHTML( sHTML, sURL, bKeepUrlDomains = False )
    #
    lEnvs       = getRandoms( lLinks, oGetPages.iMax * 2 )
    #
    dMoHeaders  = { 'Referer' : sURL }
    #
    sOrigURL    = sURL
    #
    lEnvs       = [ {   'sURL'          : sURL,
                        'doWithSuccess' : _sayPageInfo,
                        'dMoHeaders'    : dMoHeaders
                    } for sURL in lEnvs ]
    #
    if oGetPages.bSayEachResult:
        #
        sSayDuration = oGetPages.getSayDuration( sOrigURL )
        #
        print3( 'got %s links after %s, but will only investigate %s' %
                ( len( lLinks ), sSayDuration, len( lEnvs ) ) )
    #
    oGetPages.AppendOrExtend( lEnvs, iSlot )



def _getPageContent( oGetPages, sHTML, sURL, uThis, sTempFile, iSlot, oSuccess ):
    #
    oGetPages.sHTML = sHTML
    oGetPages.sFail = ''



def _getErrorMessage( oGetPages, sHTML, sURL, uThis, sTempFile, iSlot, oFailure ):
    #
    oGetPages.sHTML = sHTML
    oGetPages.sFail = 'Error: %s' % oFailure.getErrorMessage()



class _demoObserver( object ):
    #
    """
    This is part of the demo.
    """
    #
    def update( self, dStatus = None ):
        #
        if dStatus:
            #
            print3( dStatus )



def _doDemo( iMax = 5, bSayEachResult = True, bDeleteTmpFile = False ):
    #
    oGetPages       = None
    #
    dURL = {    'sURL'          : 'http://www.ipmaster.org/proxyjudge.html',
                'doWithSuccess' :  _getLinksSamples }
    try:
        #
        oGetPages   = \
            getPagesClass(
                uPages          = [ dURL ],
                iMax            = iMax,
                bSayEachResult  = bSayEachResult,
                bDeleteTmpFile  = bDeleteTmpFile,
                uObservers      = _demoObserver() )
        #
    except KeyboardInterrupt:
        #
        print3( "\n\nExiting on user cancel.", file = stderr )
        #
    #
    return oGetPages



def getPageContent(
        sURL,
        sReferrer       = '',
        bJavascript     = False,
        dMoHeaders      = {} ):
    #
    from time import sleep
    #
    sContent            = ''
    #
    dMoHeaders          = {}
    #
    if sReferrer != '':
        #
        dMoHeaders.update( { 'Referer' : sURL } )
        #
    #
    if bJavascript:
        #
        dMoHeaders.update( { 'accept' : 'text/javascript,' + dHEADERS[ 'accept' ] } )
        #
    #
    dURL = {    'sURL'          : sURL,
                'doWithSuccess' : _getPageContent,
                'doWithFailure' : _getErrorMessage,
                'dMoHeaders'    : dMoHeaders }
    #
    try:
        oGetPages   = \
            getPagesClass(
                uPages          = [ dURL ],
                bGetGoing       = True )
        #       uObservers      = _demoObserver(),
        #
    except KeyboardInterrupt:
        #
        print3( "\n\nExiting on user cancel.", file = stderr )
        #
    #
    while not oGetPages.bFinished:
        #
        sleep( 1 )
        #
    #
    if len( oGetPages.sHTML ) > len( oGetPages.sFail ):
        sContent = oGetPages.sHTML
    else:
        sContent = oGetPages.sFail
    #
    return sContent




#client hung on
#Failure Sat, 13 Jan 2008, 18:02:11 ICT Slot 7
#Error: http://75i.net/
#Failure Sat, 13 Jan 2008, 18:02:11 ICT Slot 2
#Error: http://www.theproxy.be/




if __name__ == "__main__":
    #import hotshot
    #p = hotshot.Profile(os.path.expanduser("~/yum.prof"))
    #p.run('main(sys.argv[1:])')
    #p.close()
    #
    from os.path    import join
    from sys        import argv
    from File.Write import QuickDump
    #
    from Dir.Get    import sTempDir
    try:
        if len( argv ) >= 2:
            #
            lArgs   = argv[ 1 : ]
            #
            sContent = getPageContent( *lArgs )
            #
            if sContent.startswith( 'Error:' ) or sContent.startswith( '\n\nExiting' ):
                #
                print3( sContent )
                #
            else:
                #
                print3( 'got page, length is %s bytes' % len( sContent ) )
                #
                QuickDump( sContent, join( sTempDir, 'temp.txt' ), bSayBytes = False )
                #
            #
        else:
            #
            _doDemo()
            #
    except KeyboardInterrupt:
        print3( "\n\nExiting on user cancel." )
        # >> stderr,
        # doUnlock( PID_FILE )
        exit(1)
    #
