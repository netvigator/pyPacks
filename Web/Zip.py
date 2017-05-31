#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions Zip
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

from six            import print_ as print3

from Utils.Version  import PYTHON3

# NOT WORKING IN PYTHON3


def UnZipThis( sCompressed ):
    #
    from six            import BytesIO
    #
   #from Utils.Both2n3  import BytesIO
    from gzip           import GzipFile
    #
    sStream         = BytesIO( sCompressed )
    #
    oZipper         = GzipFile( fileobj = sStream )
    #
    bUnZipped       = True
    sContent        = ''
    #
    try:
        #
        sContent    = oZipper.read() # zip sometimes chokes
        #
    except:
        #
        bUnZipped   = False
        #
    #
    return bUnZipped, sContent



def getCompressedOffChunks( sChunks ):
    #
    """
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html
    3.6.1 Chunked Transfer Coding
       Chunked-Body   = *chunk
                        last-chunk
                        trailer
                        CRLF

       chunk          = chunk-size [ chunk-extension ] CRLF
                        chunk-data CRLF
       chunk-size     = 1*HEX
       last-chunk     = 1*("0") [ chunk-extension ] CRLF

       chunk-extension= *( ";" chunk-ext-name [ "=" chunk-ext-val ] )
       chunk-ext-name = token
       chunk-ext-val  = token | quoted-string
       chunk-data     = chunk-size(OCTET)
       trailer        = *(entity-header CRLF)
    Appendix 19.4.6
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec19.html#sec19.4.6
    A process for decoding the "chunked" transfer-coding (section 3.6)
    can be represented in pseudo-code as:
       length := 0
       read chunk-size, chunk-extension (if any) and CRLF
       while (chunk-size > 0) {
          read chunk-data and CRLF
          append chunk-data to entity-body
          length := length + chunk-size
          read chunk-size and CRLF
       }
       read entity-header
       while (entity-header not empty) {
          append entity-header to existing header fields
          read entity-header
       }
       Content-Length := length
       Remove "chunked" from Transfer-Encoding
    """
    #
    from six            import next as getNext
    #
    from sys            import exc_info
    from File.Write     import MakeTemp
   #from Utils.Both2n3  import getNext
    #
    uCRLF       = '\r\n'
    #
    if PYTHON3 and isinstance( sChunks, bytes ): uCRLF = uCRLF.encode()
    #
    lCompressed = []
    #
    lChunks     = sChunks.split( uCRLF )
    #
    oChunks     = iter( lChunks )
    #
    bGotChunks  = True
    #
    while True:
        #
        try:
            sChunkSize  = getNext( oChunks )
        except StopIteration:
            break
        #
        sHexBytes   = sChunkSize.split( ';' )[ 0 ]
        #
        if sHexBytes == '0': break # finished
        #
        try:
            #
            iLenChunk   = int( sHexBytes, 16 )
            #
        except ValueError:  # that was not a Hex number after all
            #
            error, msg, traceback = exc_info()
            #
            print3( "got Value error:", msg )
            print3( sHexBytes )
            bGotChunks  = False
            #
            MakeTemp( sChunks )
            #
            break
        #
        sThisChunk  = getNext( oChunks )
        #
        while len( sThisChunk ) < iLenChunk:
            #
            try:
                sThisChunk += '\r\n' + getNext( oChunks )
            except StopIteration:
                break
        #
        if len( sThisChunk ) != iLenChunk:
            #
            bGotChunks  = False
            print3( "got wrong length off chunks!" )
            #
            MakeTemp( sChunks )
            #
            break
        #
        lCompressed.append( sThisChunk )
        #
    #
    #
    if bGotChunks:
        return ''.join( lCompressed )
    else:
        return sChunks



def ZipThis( sContent ):
    #
    from six            import BytesIO
    #
    from gzip           import GzipFile
    from Utils.Both2n3  import getBytes, sDefaultEncoding
    #
    oWriteable  = BytesIO()
    #
    oCompress   = GzipFile( fileobj = oWriteable, mode = 'wb' )
    #
    print3( 'sContent:', sContent )
    #
    oCompress.write( getBytes( sContent, encoding = sDefaultEncoding ) )
    #
    # oCompress.write( sContent )
    #
    oCompress.close()
    #
    oWriteable.seek(0)
    #
    sZipped     = oWriteable.read()
    #
    oWriteable.close()
    #
    return sZipped




def getCompressedChunks( sText, iWantChunks = 3, iMaxLen = None ):
    #
    # not used anywhere yet
    #
    from math               import ceil
    #
    from Iter.AllVers       import lMap, iZip
    from Numb.Get           import getSumOnlyIntegers
    from Numb.Accumulate    import getCumulativeIntegerTotals
    from Iter.Get           import getSequencePairsThisWithNext as getThisWithNext
    from Utils.Version      import PYTHON3
    #
    #
    uZipsStart = '\x1f\x8b'
    #
    if PYTHON3 and isinstance( sText, bytes ): uZipsStart = uZipsStart.encode()
    #
    if not sText.startswith( uZipsStart ):
        #
        sText           = ZipThis( sText )
        #
    #
    iLen                = len( sText )
    #
    lLens               = [ ceil( iLen / float( iWantChunks  ) ) ] * iWantChunks
    #
    lLens               = lMap( int, lLens )
    #
    lLens[ -1 ]         += iLen - getSumOnlyIntegers( *lLens )
    #
    lTotals             = getCumulativeIntegerTotals( lLens )
    #
    lTotals[ 0 : 0 ]    = [ 0 ]
    #
    lChunks             = [ str( sText[ iBeg : iEnd ] )
                            for iBeg, iEnd in getThisWithNext( lTotals ) ]
    #
    lHexByteLens        = [ hex( i ) for i in lLens ]
    #
    lLensChunks         = [ ';\r\n'.join( t ) for t in iZip( lHexByteLens, lChunks ) ]
    #
    lLensChunks.extend( [ '0;', '', '' ] )
    #
    return '\r\n'.join( lLensChunks )



def UnZipContent( sHTML ):
    #
    # this is for HTTP headers + content
    # without HTTP headers, this does not work!!!
    #
    from String.Get import getTextAfter
    from Web.GetRaw import getHeaderValueOffBytes, getHeaderOffBytes
    #
    sLength     = getHeaderValueOffBytes( sHTML, 'Content-Length' )
    #
    iLength     = 0
    #
    try:
        iLength = int( sLength )
    except:
        pass
    #
    if iLength: # they are supposed to give this but some do not
        #
        sCompressed = sHTML[ -iLength : ]
        #
    else:
        #
        sCompressed = getTextAfter( sHTML, '\r\n\r\n' )
        #
    #
    if getHeaderValueOffBytes( sHTML, 'Transfer-Encoding' ) == 'chunked':
        #
        sCompressed = getCompressedOffChunks( sCompressed )
        #
    #
    bUnZipped, sContent = UnZipThis( sCompressed )
    #
    #
    if not bUnZipped and iLength:
        #
        sCompressed = getTextAfter( sHTML, '\r\n\r\n' )
        #
        bUnZipped, sContent = UnZipThis( sCompressed )
        #
        # print3( 'could not unzip!!!' )
    #
    if not bUnZipped:
        #
        sContent    = sCompressed
        #
    #
    sNewContent = '%s\r\n\r\n%s' % ( getHeaderOffBytes( sHTML ), sContent )
    #
    return bUnZipped, sNewContent



def getPlainIfZipped( sMaybeZipped ):
    #
    # this is for content only -- without HTTP headers
    #
    sPlainText          = sMaybeZipped
    #
    if sMaybeZipped[ : 2 ] == '\x1f\x8b':
        #
        bUnZipped, sNewContent = UnZipThis( sMaybeZipped )
        #
        if bUnZipped:
            #
            sPlainText  = sNewContent
            #
        else: # try chunks
            #
            sCompressed = getCompressedOffChunks( sMaybeZipped )
            #
            bUnZipped, sNewContent = UnZipThis( sCompressed )
            #
            if bUnZipped:
                #
                sPlainText  = sNewContent
                #
            #
        #
    #
    return sPlainText




if __name__ == "__main__":
    #
    from gzip           import GzipFile
    #
    from String.Get     import getTextAfter
    from Utils.Both2n3  import getBytes, getStrGotBytes
    from Utils.Result   import sayTestResult
    #
    sText = '''
        How now brown cow.
        Mary had a little lamb.
        For breakfast today we are having spam, eggs and toast.
    '''
    #
    lProblems = []
    #
    sZipped         = ZipThis( sText )
    #
    bUnZipped, sReturned = UnZipThis( sZipped )
    #
    if not bUnZipped or sReturned != sText:
        #
        lProblems.append( 'UnZipThis()' )
        #
        lProblems.append( 'ZipThis()' )
        #
    if      getPlainIfZipped( sZipped ) != sText or \
            getPlainIfZipped( sText   ) != sText:
        #
        lProblems.append( 'getPlainIfZipped()' )
        #
    #
    sChunkTxt   = getCompressedChunks( sText   )
    #
    sZoffChunk  = getCompressedOffChunks( sChunkTxt )
    sToffChunk  = getPlainIfZipped( sZoffChunk )
    #
    if sToffChunk != sText:
        #
        lProblems.append( 'getCompressedOffChunks()' )
        #
        lProblems.append( 'getCompressedChunks()' )
        #
        lProblems.append( 'getPlainIfZipped()' )
        #
    #
    sChunkZip   = getCompressedChunks( sZipped )
    #
    sZoffChunk  = getCompressedOffChunks( sChunkZip )
    sToffChunk  = getPlainIfZipped( sZoffChunk )
    #
    if sToffChunk != sText:
        #
        lProblems.append( 'getCompressedOffChunks()' )
        #
        lProblems.append( 'getCompressedChunks()' )
        #
        lProblems.append( 'getPlainIfZipped()' )
        #
    #
    sHTML = 'HTTP/1.1\r\nContent-Length: %s\r\n\r\n' % len( sZipped )
    #
    if PYTHON3:
        sHTML   = getBytes( sHTML )
    #
    sHTML = sHTML + sZipped
    #
    if PYTHON3: sHTML = getStrGotBytes( sHTML )
    #
    bUnZipped, sNewContent = UnZipContent( sHTML )
    #
    if getTextAfter( sNewContent, '\r\n\r\n' ) != sText or not bUnZipped:
        #
        lProblems.append( 'UnZipContent()' )
        #

    #
    sayTestResult( lProblems )