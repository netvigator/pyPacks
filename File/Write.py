#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# File functions Write
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
# Copyright 2004-2019 Rick Graves
#
# getFullSpec( *sFileSpec )
# getFullSpecDefaultOrPassed( *sFileSpec )

import              io

from os             import utime, rmdir, sep as cSep
from os.path        import join

from six            import print_ as print3

try:
    from .Get               import getFileObject, getFileContent
    from .Spec              import getFullSpec, getFullSpecDefaultOrPassed
    from ..Collect.Output   import getPrintableTextFromSeq
    from ..Dir.Get          import sTempDir
    from ..Dir.Test         import isDirThere
    from ..Iter.AllVers     import iMap, lMap, iRange
    from ..String.Convert   import getUnicodeOut
    from ..String.Get       import getTextAfterLast
    from ..String.Paragraph import getTextMakeParagraphs
    from ..Utils.Both2n3    import PYTHON2, getEncoded, getStrGotBytes
    from ..Utils.ImIf       import ImIf
except ( ValueError, ImportError ):
    from File.Get           import getFileObject, getFileContent
    from File.Spec          import getFullSpec, getFullSpecDefaultOrPassed
    from Collect.Output     import getPrintableTextFromSeq
    from Dir.Get            import sTempDir
    from Dir.Test           import isDirThere
    from Iter.AllVers       import iMap, lMap, iRange
    from String.Convert     import getUnicodeOut
    from String.Get         import getTextAfterLast
    from String.Paragraph   import getTextMakeParagraphs
    from Utils.Both2n3      import PYTHON2, getEncoded, getStrGotBytes
    from Utils.ImIf         import ImIf

def QuickDump( sText, *sFileSpec, **kwargs ):
    #
    ''' pass content, *filespec, **kwargs '''
    # chr(92) is backslash
    #
    #
    # print3( '*sFileSpec:', *sFileSpec )
    #
    sName = getFullSpec( *sFileSpec )
    #
    # print3( 'sName:', sName )
    #
    bSayBytes   = kwargs.get( 'bSayBytes', True )
    sMode       = kwargs.get( 'sMode',     'w'  )
    bWantDir    = kwargs.get( 'bWantDir',  True )
    sEncoding   = kwargs.get( 'sEncoding', 'UTF-8' ) 
    #
    if bWantDir and not ( cSep in sName or chr(92) in sName ):
        sName = join( sTempDir, sName )
    #
    # print3( 'sName (expanded):', sName )
    #
    bUseIO = False
    #
    if PYTHON2 and isinstance( sText, type( u'' ) ):
        #
        bUseIO = True
        #
    elif isinstance( sText, bytes ): # python2 always returns True
        #
        sText = getStrGotBytes( sText )
        #
    #
    if bUseIO:
        #
        hTemp = io.open( sName, sMode, encoding = sEncoding )
        #
    else:
        #
        hTemp = open( sName, sMode )
        #
    #
    #print3( type( sText ) )
    #print3( 'sEncoding:', sEncoding )
    #print3( str( sText.encode( sEncoding ) ) )
    #
    # underlying OS environmental variables
    # determine whether python can write!
    #
    # https://stackoverflow.com/questions/41408791/python-3-unicodeencodeerror-ascii-codec-cant-encode-characters
    #
    try:
        #
        hTemp.write( sText )
        #
    except UnicodeEncodeError:
        #
        print3( 'UnicodeEncodeError:' )
        print3( type( sText ) )
        print3( 'sEncoding:', sEncoding )
        print3( str( sText.encode( sEncoding ) ) )
        hTemp.write( getEncoded( sText, sEncoding ) )
        #
    except UnicodeDecodeError:
        #
        #print3( 'UnicodeDecodeError:' )
        #sLineBefore = ''
        #
        for sLine in sText:
            #
            try:
                #
                hTemp.write( getStrGotBytes( sLine, sEncoding ) )
                #
            except UnicodeDecodeError:
                #
                sInstead = getUnicodeOut( sLine )
                hTemp.write( sInstead )
                #sLineBefore = sLine
            #
        #
    #
    hTemp.close()
    #
    if bSayBytes: print3( len( sText ), 'bytes' )



def QuietDump( sText, *sFileSpec, **kwargs ):
    #
    kwargs[ 'bSayBytes' ] = False
    #
    QuickDump( sText, *sFileSpec, **kwargs )



def WriteText2File( sText, *sFileSpec ):
    #
    kwargs = dict( bSayBytes = False, bWantDir = False )
    #
    QuickDump( sText, *sFileSpec, **kwargs )



def openAppendClose( sText, *sFileSpec, **kwargs ):
    #
    bNewLineBefore  = kwargs.get( 'bNewLineBefore', False )
    bNewLineAfter   = kwargs.get( 'bNewLineAfter',  True  )
    bSayBytes       = kwargs.get( 'bSayBytes',      False )
    bWantDir        = kwargs.get( 'bWantDir',       True  )
    sMode           = kwargs.get( 'sMode',          'a+'  )
    sEncoding       = kwargs.get( 'sEncoding',      'utf-8' ) 
    #
    if bNewLineBefore and not ( sText.startswith( '\n' ) or sText.startswith( '\r' ) ):
        #
        sText   = '\n' + sText
        #
    if bNewLineAfter and not ( sText.endswith( '\n' ) or sText.endswith( '\r' ) ):
        #
        sText   += '\n'
        #
    #
    kwargs = dict(
        bSayBytes       = bSayBytes,
        bWantDir        = bWantDir,
        sMode           = sMode,
        sEncoding       = sEncoding )
    #
    QuickDump( sText, *sFileSpec, **kwargs )



def Append2LastLine( sText, *sFileSpec, **kwargs ):
    #
    #
    bNewLineBefore  = kwargs.get( 'bNewLineBefore', False )
    bNewLineAfter   = kwargs.get( 'bNewLineAfter',  True  )
    bSayBytes       = kwargs.get( 'bSayBytes',      False )
    bWantDir        = kwargs.get( 'bWantDir',       True  )
    sMode           = kwargs.get( 'sMode',          'a+'  )
    #
    oFile = getFileObject( *sFileSpec, **kwargs )
    #
    sLastLiner = ''
    sNext2Last = ''
    #
    for sLine in oFile:
        #
        sNext2Last, sLastLiner = sLastLiner, sLine
        #
    #
    if len( sLastLiner ) <= 2:
        #
        sText = ''.ljust( len( sNext2Last ) - 1 ) + sText
        #
    #
    if bNewLineBefore and not ( sText.startswith( '\n' ) or sText.startswith( '\r' ) ):
        #
        sText   = '\n' + sText
        #
    #
    if bNewLineAfter and not ( sText.endswith( '\n' ) or sText.endswith( '\r' ) ):
        #
        sText   += '\n'
        #
    #
    oFile.write( sText )
    oFile.close()


def _NoDoubleQotes( s ): return s.replace( '"', "'" )

def getExcelCsvLine( seq ):
    #
    #
    l = iMap( str, seq )
    #
    return '"%s"' % '","'.join( iMap( _NoDoubleQotes, l ) )


def MakeTemp( sText, bSayBytes = True ):
    #
    QuickDump( sText, 'temp.txt', bSayBytes = bSayBytes )



def QuickDumpLines( lText, *sFileSpec, **kwargs ):
    #
    #
    bSayBytes   = kwargs.get( 'bSayBytes',  False   )
    sNewLine    = kwargs.get( 'sNewLine',   '\n'    )
    sEncoding   = kwargs.get( 'sEncoding', 'utf-8'  ) 
    #
    bConvert2Text = kwargs.get( 'bConvert2Text', True  )
    #
    sText = getPrintableTextFromSeq(
                lText, sNewLine, bConvert2Text = bConvert2Text )
    #
    if sText.startswith( sNewLine ): sText = sText[ len( sNewLine ) : ]
    #
    kwargs = dict(
        bSayBytes       = bSayBytes,
        sMode           = 'w',
        sEncoding       = sEncoding )
    #
    QuickDump( sText, *sFileSpec, **kwargs )




def QuietDumpLines( lText, *sFileSpec, **kwargs ):
    #
    kwargs[ 'bSayBytes' ] = False
    #
    QuickDumpLines( lText, *sFileSpec, **kwargs )



def putListInTemp( lText, sNewLine = '\n', bSayBytes = False ):
    #
    QuickDumpLines( lText, 'temp.txt', bSayBytes = bSayBytes, sNewLine = sNewLine )



def PutLinesInTemp( lText, sNewLine = '\n', bSayBytes = True ):
    #
    return QuickDumpLines( lText, 'temp.txt', bSayBytes = bSayBytes, sNewLine = sNewLine )


def getTextRemoveReturnsReWrite( *sFileSpec, **kwargs ):
    #
    """
    removes hard returns within each paragraph
    (on the end of each wrapped line),
    leaves double return between each paragraph.
    reads the file, removes returns,
    then overwrites the file, so
    best to make a backup first.
    """
    #
    #
    sFile   = getFullSpecDefaultOrPassed( *sFileSpec )
    #
    sText   = getFileContent( sFile )
    #
    bSayBytes = kwargs.get( 'bSayBytes', True )
    #
    openAppendClose(
        getTextMakeParagraphs( sText ), sFile,
        bNewLineBefore = True, bNewLineAfter = True, bSayBytes = bSayBytes )



def WriteRepr2File( u, *sFileSpec ):
    #
    '''
    content can be reconstituted with getObjFromFileContent in File.Get
    '''
    #
    #
    sFileSpec = getFullSpec( *sFileSpec )
    #
    WriteText2File( repr( u ), sFileSpec )


def PutReprInTemp( u, bSayBytes = False ):
    #
    '''content can be reconstituted with getObjFromFileContent in File.Get
    '''
    #
    MakeTemp( repr( u ), bSayBytes = bSayBytes )


def _getListLenRight( l, iWantLen ):
    #
    if len( l ) < iWantLen:
        #
        l.extend( [ '' ] * ( iWantLen - len( l ) ) )
        #
    elif len( l ) > iWantLen:
        #
        del l[ iWantLen : ]
        #
    #
    return l


def putCsvOut( lOutput, *sFileSpec, **kwargs ):
    #
    #
    if not sFileSpec :
        sFileSpec = ( join( sTempDir, 'temp.csv' ), )
    #
    sColDelim       = kwargs.get( 'sColDelim',      ','  )
    sQuote          = kwargs.get( 'sQuote',         '"'  )
    #
    bConvert2Text   = kwargs.get( 'bConvert2Text', True  )
    sEncoding       = kwargs.get( 'sEncoding',   'utf-8' ) 
    #
    if lOutput:
        #
        if bConvert2Text:
            lOutput = [ lMap( str, l ) for l in lOutput ]
        #
        #
        sFirst  = lOutput[0][0]
        #
        try:
            #
            lOutput[0][0] = 'x'
            lOutput[0][0] = sFirst
            #
        except TypeError:
            #
            lOutput = [ list( l ) for l in lOutput ]
            #
        #
        sCell   = '%s%%s%s' % ( sQuote, sQuote )
        #
        iCols   = len( lOutput[0] )
        #
        sEscQ   = '\\' + sQuote
        #
        bAllRowsRightLen = True
        #
        for iRow in iRange( len( lOutput ) ):
            #
            bAllRowsRightLen = ( bAllRowsRightLen and
                                 len( lOutput[ iRow ] ) == iCols )
            #
            for iCol in iRange( iCols ):
                #
                try:
                    if sQuote in lOutput[ iRow ][ iCol ]:
                        #
                        try:
                            lOutput[ iRow ][ iCol ] = \
                            lOutput[ iRow ][ iCol ].replace( sQuote, sEscQ )
                        except TypeError:
                            lOutput[ iRow ] = list( lOutput[ iRow ] )
                            lOutput[ iRow ][ iCol ] = \
                            lOutput[ iRow ][ iCol ].replace( sQuote, sEscQ )
                #
                except IndexError:
                    pass
                #
            #
        #
        sFormat = sColDelim.join( [ sCell ] * iCols )
        #
        if bAllRowsRightLen:
            #
            iOutput = lOutput
            #
        else:
            #
            def getListLenRight( l ):
                #
                return _getListLenRight( l, iCols )
            #
            iOutput = iMap( getListLenRight, lOutput )
            #
        #
        lStrings = [ sFormat % tuple( l ) for l in iOutput ]
        #
        #
        QuickDumpLines( lStrings, *sFileSpec, **kwargs )
        #
        '''
        try:
            QuickDumpLines( lStrings, *sFileSpec, **kwargs )
        except TypeError:
            print3( 'iCols:', iCols )
            print3( 'sFormat:', sFormat )
            print3( 'got error, lOutput is in temp.txt' )
            putListInTemp( lOutput )
        '''
        #
    else:
        #
        sName = getFullSpec( *sFileSpec )
        #
        print3( 'got no ouput for', sName )



def Touch(fname):
    if isDirThere( fname ):
        rmdir( fname )
    try:
        utime(fname, None)
    except OSError:
        open(fname, 'a').close()




if __name__ == "__main__":
    #
    lProblems = []
    #
    from File.Del       import DeleteIfExists
    from File.Get       import getTempFile, getListFromFileLines, getContent, \
                            getRandomFileName
    from File.Test      import isFileThere
    from Iter.AllVers   import tRange
    from Utils.Result   import sayTestResult
    #
    sText = 'How now brown cow.'
    #
    sTemp = getTempFile()
    #
    QuietDump( sText, sTemp )
    #
    sContent = getContent( sTemp )
    #
    if not sContent.startswith( 'How now brown cow.' ):
        #
        lProblems.append( 'QuickDump() QuietDump()' )
        #
    #
    WriteText2File( sText, sTemp )
    #
    sContent = getContent( sTemp )
    #
    if not sContent.startswith( 'How now brown cow.' ):
        #
        lProblems.append( 'WriteText2File()' )
        #
    #
    openAppendClose( sText, sTemp, bSayBytes = False )
    #
    sContent = getContent( sTemp )
    #
    iLenGot     = len( sContent )
    iLenWant    = 2 * len( sText )
    #
    if iLenGot < iLenWant or iLenGot > 1.5 * iLenWant:
        #
        lProblems.append( 'openAppendClose()' )
        #
    #
    MakeTemp( sContent, bSayBytes = False )
    #
    sContent = getContent()
    #
    iLenGot     = len( sContent )
    iLenWant    = 2 * len( sText )
    #
    if iLenGot < iLenWant or iLenGot > 1.5 * iLenWant:
        #
        lProblems.append( 'MakeTemp()' )
        #
    #
    lText = getListFromFileLines()
    #
    QuietDumpLines( lText, sTemp )
    #
    sContent = getContent()
    #
    iLenGot     = len( sContent )
    iLenWant    = 2 * len( sText )
    #
    if iLenGot < iLenWant or iLenGot > 1.5 * iLenWant:
        #
        lProblems.append( 'QuietDumpLines() QuickDumpLines()' )
        #
    #
    #
    if PYTHON2:
        uText = u'ꀀ' + u'abcd' + u'\u07b4'
    else:
        uText = chr(40960) + 'abcd' + chr(1972)
    #
    sTemp = getTempFile()
    #
    QuietDump( uText, sTemp )
    #
    sContent = getContent( sTemp )
    #
    #
    lText = [ s.strip() + '\n\n' for s in lText ]
    #
    PutLinesInTemp( lText, bSayBytes = False )
    #
    sContent = getContent()
    #
    iLenGot     = len( sContent )
    iLenWant    = 2 * len( sText )
    #
    if iLenGot < iLenWant or iLenGot > 1.5 * iLenWant:
        #
        lProblems.append( 'PutLinesInTemp()' )
        #
    #
    putListInTemp( lText, bSayBytes = False )
    #
    sContent = getContent()
    #
    iLenGot     = len( sContent )
    iLenWant    = 2 * len( sText )
    #
    if iLenGot < iLenWant or iLenGot > 1.5 * iLenWant:
        #
        lProblems.append( 'putListInTemp()' )
        #
    #
    getTextRemoveReturnsReWrite( bSayBytes = False )
    #
    sContent = getContent()
    #
    if '\n\n' not in sContent:
        #
        lProblems.append( 'getTextRemoveReturnsReWrite()' )
        #
    #
    d = {'Fischbach': ['Corcoran', 'Ching Wu']}
    #
    PutReprInTemp( d )
    #
    sContent = getContent()
    #
    if sContent != repr( d ):
        #
        lProblems.append( 'PutReprInTemp()' )
        #
    #
    sFileSpec = getRandomFileName( sTempDir )
    #
    WriteRepr2File( d, sTempDir, sFileSpec[ 5 : ] )
    #
    sContent = getContent( sFileSpec )
    #
    DeleteIfExists( sTempDir, sFileSpec )
    #
    if sContent != repr( d ):
        #
        lProblems.append( 'WriteRepr2File()' )
        #
    #
    lLines = (  ('Column 1',     'Column 2'),
                ('line 1 col 1', 'line 1 col 2' ),
                ('line 2 col 1', 'line 2 col 2' ) )
    #
    putCsvOut( lLines, join( sTempDir, 'temp.txt' ) )
    #
    sContent = getContent()
    #
    if sContent != \
        '''"Column 1","Column 2"\n"line 1 col 1","line 1 col 2"\n"line 2 col 1","line 2 col 2"''':
        #
        lProblems.append( 'putCsvOut() w output file spec' )
        #
    #
    putCsvOut( lLines )
    #
    sContent = getContent()
    #
    if sContent != \
        '''"Column 1","Column 2"\n"line 1 col 1","line 1 col 2"\n"line 2 col 1","line 2 col 2"''':
        #
        lProblems.append( 'putCsvOut() no output file spec' )
        #
    #
    lLines = (  ('Column 1',     'Column 2'),
                ('line 1 col 1', 'line 1 col 2' ),
                ('line 2 col 1', ) )
    #
    putCsvOut( lLines, join( sTempDir, 'temp.txt' ) )
    #
    sContent = getContent()
    #
    if sContent != \
        '''"Column 1","Column 2"\n"line 1 col 1","line 1 col 2"\n"line 2 col 1",""''':
        #
        lProblems.append( 'putCsvOut() bAllRowsRightLen' )
        #
    #
    if getExcelCsvLine( tRange(9) ) != '"0","1","2","3","4","5","6","7","8"':
        #
        lProblems.append( 'getExcelCsvLine()' )
        #
    #
    Touch( '/tmp/test' )
    #
    if not isFileThere( '/tmp/test' ):
        #
        lProblems.append( "Touch( '/tmp/test' )" )
        #
    #
    sayTestResult( lProblems )
