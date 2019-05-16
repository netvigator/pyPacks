#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# File functions get
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

#from os.path import join, isfile, getmtime, split, splitext, exists, basename, isdir
#from os      import stat, environ, getcwd, listdir, rename, remove

# from os.path import exists, join, isfile, isdir

from os                     import utime, environ, close
from os.path                import join, isfile, isdir
from glob                   import glob
from tempfile               import mkstemp

try:
    from .Test              import isFileThere
    from .Spec              import getFullSpec, getFullSpecDefaultOrPassed
    from ..Utils.Version    import PYTHON2
    from ..Dir.Get          import sTempDir
    from ..Numb.Get         import getRandomDigits
    from ..Utils.Config     import getConfDict
except ( ValueError, ImportError ):
    from File.Test          import isFileThere
    from File.Spec          import getFullSpec, getFullSpecDefaultOrPassed
    from Utils.Version      import PYTHON2
    from Dir.Get            import sTempDir
    from Numb.Get           import getRandomDigits
    from Utils.Config       import getConfDict

class FileNotThereError( Exception ): pass

class LineParserObject( object ):
    #
    def __init__( self, sConfFile = 'LineParserTest.conf' ):
        #
        #
        dMain       = { 'infile'  : join( sTempDir, 'LineParserTestInput.txt' ),
                        'rowhead' : 'new row',
                        'colhead1': 'next row',
                        'outfile' : join( sTempDir, 'LineParserTestOutput.txt' ) }
        dDefaults   = { 'main' : dMain }
        bNoConfigOK = ( sConfFile == 'LineParserTest.conf' )
        #
        dFile2Parse = getConfDict(
                        sConfFile,
                        dDefaults = dDefaults,
                        bNoConfigOK = bNoConfigOK )
        #
        self.dFile2Parse = dFile2Parse
        #
        if self.dFile2Parse == dDefaults:
            #
            # print3( dFile2Parse )
            #
            self._makeTestFile()
        #
        self.oInFile = open( self.dFile2Parse['main']['infile'] )

    def _makeTestFile( self ):
        #
        try: # moving this to the top breaks this package!
            from .Write     import QuickDump
        except ( ValueError, ImportError ): # maybe circular import issue
            from File.Write import QuickDump
        #
        sTestContent = ( '\nnew row\nspam\n\nnext row\ntoast\n\n\n'
                         'new row\neggs\n\nnext row\nbeans\n\n' )
        #
        QuickDump( sTestContent, self.dFile2Parse['main']['infile'], bSayBytes = False )
        #

    def _isNewRow( self, s ):
        #
        '''can be subclassed
        '''
        return s == self.dFile2Parse['main']['rowhead']

    def ReadWrite( self ):
        #
        pass


def getFileObject( *sFileSpec, **kwargs ):
    #
    sMode = 'r'
    #
    sNcode = ''
    #
    if 'sMode'  in kwargs: sMode  = kwargs[ 'sMode'  ]
    if 'sNcode' in kwargs: sNcode = kwargs[ 'sNcode' ]
    #
    sFileSpec = getFullSpec( *sFileSpec )
    #
    f       = None
    #
    if not isFileThere( sFileSpec ): raise FileNotThereError( sFileSpec )
    #
    try:
        #
        if sNcode:
            #
            f   = open( sFileSpec, sMode, encoding = sNcode )
            #
            # print3( 'sNcode:', sNcode )
            #
        else:
            #
            f   = open( sFileSpec, sMode )
            #
        #
    except:
        #
        pass
        #
    #
    #
    return f



def getFileContent( *sFileSpec, **kwargs ):
    #
    sFileSpec = getFullSpecDefaultOrPassed( *sFileSpec, **kwargs )
    #
    sMode  = 'r'
    sNcode = ''
    #
    if 'sMode' in kwargs: sMode = kwargs[ 'sMode' ]
    if 'sNcode' in kwargs: sNcode = kwargs[ 'sNcode' ]
    #
    #if sNcode:
    #    #
    #    print3( 'sNcode:', sNcode )
    #    #
    #
    f = getFileObject( sFileSpec, sMode = sMode, sNcode = sNcode )
    #
    if f is None:
        #
        sContents = ''
        #
    else:
        #
        try:
            #
            sContents = f.read()
            #
            # print3( 'read without exception' )
            #
        except UnicodeDecodeError:
            #
            # print3( 'got UnicodeDecodeError' )
            sMode += 'b'
            #
            f = getFileObject( sFileSpec, sMode = sMode )
            #
            sContents = f.read()
            #
        #
        f.close()
        #
    #
    # print3( 'contents are of type', type( sContents ) )
    #
    return sContents



def getContent( *sFileSpec, **kwargs ):
    #
    sFileSpec = getFullSpecDefaultOrPassed( *sFileSpec, **kwargs )
    #
    if 'sNcode' in kwargs and PYTHON2:
        #
        del kwargs['sNcode']
        #
    #
    return getFileContent( sFileSpec, **kwargs )





def getRandomFileName( sDir = None, bCreate = False ):
    #
    #
    if sDir is None:
        #
        sDir            = environ.get( 'HOME', sTempDir )
        #
    #
    if not isdir( sDir ): sDir = '' # put in current directory
    #
    while True:
        #
        sFile           = '%s.tmp' % getRandomDigits( 8 )
        #
        sPathFile       = join( sDir, sFile )
        #
        if not isfile( sPathFile ): break
        #
    #
    if bCreate:
        #
        oFile = open( sPathFile, 'w' )
        #
        oFile.close()
        #
    #
    return sPathFile



def getListFromFileLines( *sFileSpec, **kwargs ):
    #
    bStipLines = kwargs.get( 'bStipLines', True )
    #
    sFileSpec = getFullSpecDefaultOrPassed( *sFileSpec )
    #
    sText       = getFileContent( sFileSpec )
    #
    if sText.count( '\n' ) == sText.count( '\r\n' ):
        #
        lLines  = sText.split( '\r\n' )
        #
    else:
        #
        lLines  = sText.split( '\n' )
        #
    #
    if bStipLines:
        #
        return  [ sLine.strip() for sLine in lLines ]
        #
    else:
        #
        return  lLines


getListOffFileLines = getListFromFileLines



def getTempFile( suffix = None, dir = None ):
    #
    """
    Creates a unique temp file and returns the full path spec.
    """
    #
    #
    kwargs = {}
    #
    if suffix is not None:
        #
        kwargs[ 'suffix' ] = suffix
        #
    if dir is not None:
        #
        kwargs[ 'dir'    ] = dir
        #
    #
    fhTemp, sTempFile = mkstemp( **kwargs )
    #
    close( fhTemp )
    #
    # return getBackslashEscaped( sTempFile )
    #
    return sTempFile






def getObjFromFileContent( *sFileSpec ):
    #
    '''
    Goes with PutReprInTemp in File.Write
    '''
    #
    sFileSpec = getFullSpecDefaultOrPassed( *sFileSpec )
    #
    sContent    = getFileContent( sFileSpec )
    #
    return eval( sContent )




def getObjFromFileIter( *sFileSpec ):
    #
    '''
    Goes with PutReprInTemp in File.Write
    '''
    #
    sFileSpec = getFullSpecDefaultOrPassed( *sFileSpec )
    #
    oFile = getFileObject( sFileSpec )
    #
    return eval( oFile.read() )




def getFileNameNoSpaces( s ):
    #
    while '  ' in s:
        #
        s = s.replace( '  ', ' ' )
        #
    #
    return s.replace( ' ', '_' )


def getFilesMatchingPattern( sDir, sPattern ):
    #
    sFullSpec = getFullSpec( sDir, sPattern )
    #
    lFiles = [ sFile for sFile
               in glob( sFullSpec )
               if isfile( sFile ) ]
    #
    return lFiles

    

def getFileSpecHereOrThere( sFileName, tMaybeThere = ( '/tmp', ) ):
    #
    sFullSpec = None
    #
    if isFileThere( sFileName ):
        #
        sFullSpec = sFileName
        #
    else:
        #
        for sPath in tMaybeThere:
            #
            if isFileThere( sPath, sFileName ):
                #
                sFullSpec = join( sPath, sFileName )
                #
                break
                #
            #
        #
    #
    return sFullSpec



def Touch( sFileSpec, times=None):
    with open( sFileSpec, 'a' ):
        utime( sFileSpec, times )



if __name__ == "__main__":
    #
    lProblems = []
    #
    from os.path        import getmtime
    from time           import sleep
    #
    from six            import print_ as print3
    #
    from Collect.Query  import get1stThatMeets
    from File.Del       import DeleteIfExists
    from File.Spec      import getPathNameExt
    from File.Test      import isFileThere
    from File.Write     import PutReprInTemp, QuietDump
    from Time.ReadWrite import putTimeInFile
    from Time.Test      import isISOdatetime
    from Utils.Result   import sayTestResult
    #
    #
    fThisFile = getFileObject( 'Get.py' )
    #
    def isStartsWithThis( s ): return s.startswith( 'def getFileObject' )
    #
    if get1stThatMeets( fThisFile, isStartsWithThis ) is None:
        #
        lProblems.append( 'getFileObject()' )
        #
    #
    fThisFile.close()
    #
    sContent = getContent( 'Get.py' )
    #
    lLines  = sContent.split( '\n' )
    #
    if get1stThatMeets( lLines, isStartsWithThis ) is None:
        #
        lProblems.append( 'getContent() / getFileContent() file spec passed' )
        #
    #
    putTimeInFile( getFullSpecDefaultOrPassed() )
    #
    # sContent = getContentOutOfQuotes( getContent() )
    #
    sContent = getContent( sNcode = 'utf-8' )
    #
    if not isISOdatetime( sContent ):
        #
        lProblems.append( 'getContent() / getFileContent() no file spec argument' )
        #
        print3( repr( sContent ) )
    #
    if len( getRandomFileName() ) < 10:
        #
        lProblems.append( 'getRandomFileName()' )
        #
    #
    lLines = getListFromFileLines( 'Get.py' )
    #
    if get1stThatMeets( lLines, isStartsWithThis ) is None:
        #
        lProblems.append( 'getListFromFileLines()' )
        #
    #
    if len( getTempFile() ) < 10:
        #
        lProblems.append( 'getTempFile()' )
        #
    #
    d = {'Fischbach': ['Corcoran', 'Ching Wu']}
    #
    PutReprInTemp( d )
    #
    if d != getObjFromFileContent():
        #
        lProblems.append( 'getObjFromFileContent()' )
        #
    #
    if d != getObjFromFileIter():
        #
        lProblems.append( 'getObjFromFileIter()' )
        #
    #
    if getFileNameNoSpaces( 'Jay  Inslee (D)' ) != 'Jay_Inslee_(D)':
        #
        lProblems.append( 'getFileNameNoSpaces()' )
        #
    #
    LineParserObject()
    #
    sText = 'How now brown cow.'
    #
    sTemp = getTempFile()
    #
    sHoldTemp = sTemp
    #
    QuietDump( sText, sTemp )
    #
    sPath, sFile, sExtn = getPathNameExt( sTemp )
    #
    sNameNoPath = sFile + sExtn
    #
    if getFileSpecHereOrThere( sNameNoPath ) == join( sPath, sNameNoPath ):
        pass
    else:
        #
        lProblems.append(
            'getFileSpecHereOrThere() should return full spec (no ext)' )
        #
    #
    # DeleteIfExists( sTemp )
    #
    sTemp = getTempFile()
    #
    sPath, sFile, sExtn = getPathNameExt( sTemp )
    #
    sNameNoPath = sFile + sExtn
    #
    DeleteIfExists( sTemp )
    #
    if getFileSpecHereOrThere( sNameNoPath ) is not None:
        #
        print3( sNameNoPath )
        lProblems.append( 'getFileSpecHereOrThere() file not there' )
        #
    #
    sTemp = '%s.tmp' % sTemp
    #
    QuietDump( sText, sTemp )
    #
    sPath, sFile, sExtn = getPathNameExt( sTemp )
    #
    sNameNoPath = sFile + sExtn
    #
    if getFileSpecHereOrThere( sNameNoPath ) == join( sPath, sNameNoPath ):
        pass
    else:
        #
        lProblems.append(
            'getFileSpecHereOrThere() should return full spec (with ext)' )
        #
    #
    
    DeleteIfExists( sTemp )
    #
    sTemp = 'test_file_%s_.txt'
    #
    for i in range(9):
        #
        sTempFile = sTemp % str( i )
        #
        QuietDump( sText, sTempFile )
        #
    #
    lFiles = getFilesMatchingPattern( '/tmp', 'test_file_%s_.txt' % '*' )
    #
    lFiles.sort()
    #
    lExpect = [ '/tmp/test_file_0_.txt',
                '/tmp/test_file_1_.txt',
                '/tmp/test_file_2_.txt',
                '/tmp/test_file_3_.txt',
                '/tmp/test_file_4_.txt',
                '/tmp/test_file_5_.txt',
                '/tmp/test_file_6_.txt',
                '/tmp/test_file_7_.txt',
                '/tmp/test_file_8_.txt']
    #
    if lFiles != lExpect:
        #
        lProblems.append( 'getFilesMatchingPattern()' )
        #
    #
    for i in range(9):
        #
        DeleteIfExists( '/tmp', sTemp % str( i ) )
        #
    #
    tLastMod = getmtime(sHoldTemp)
    #
    sleep( 0.1 )
    #
    Touch( sHoldTemp )
    #
    tRecently = getmtime(sHoldTemp)
    #
    if tLastMod >= tRecently:
        #
        print3( tLastMod  )
        print3( tRecently )
        lProblems.append( 'Touch() file already exists' )
        #
    #
    DeleteIfExists( sHoldTemp )
    #
    Touch( sHoldTemp )
    #
    if not isFileThere( sHoldTemp ):
        #
        lProblems.append( 'Touch() non existing file' )
        #
    #
    DeleteIfExists( sHoldTemp )
    #
    sayTestResult( lProblems )
