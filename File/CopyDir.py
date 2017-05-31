#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
#
from os      import stat, listdir, mkdir, utime
from os.path import splitext, exists, getsize, isfile, isdir, join
from sys     import argv, exc_info

try:
    from os.path import samefile # only available on *ix plaforms
except:
    def samefile( sDirFrom, sDirTo ): return False

from six            import print_ as print3

iVerbose        = 0
iDirCount = iFileCount = 0
iMaxFileSize    = 100000
iBlock          = 1024*8
lWantExtensions = None

def CopyOneFile( sFileFrom, sFileTo, dWantExtensions = {}, iMaxFileSize = iMaxFileSize ):
    #
    sStub, sExtn    = splitext( sFileFrom )
    #
    sExtn           = sExtn.lower()
    #
    st_size         = 0
    #
    bGotStats       = 0
    #
    try:
        # print3( sFileFrom )
        st_mode, st_ino, st_dev, st_nlink, st_uid, st_gid, st_size, st_atime, st_mtime, st_ctime = \
            stat( sFileFrom )
        bGotStats   = True
    except:
        print3( 'Error getting file size for', sFileFrom, '-- skipped' )
    #
    iFromSize       = st_size   # getsize( sFileFrom )
    iCopiedFile     = 0
    #
    if  iFromSize > 0 and \
        ( dWantExtensions == {} or sExtn in dWantExtensions ) and \
        ( not exists(  sFileTo ) or \
            ( getsize( sFileTo ) != iFromSize ) ):
        #
        if iFromSize <= iMaxFileSize:
            #
            try:
                #
                f = open( sFileFrom )
                #
                sContents = f.read()
                #
                f.close()
                #
            except:
                #
                sContents = ''
                #
            #
            if sContents == '':
                #
                sType, sValue, oTraceBack = exc_info()
                print3( 'Error reading', sFileFrom, '-- skipped' )
                print3( sType, sValue )
                #
            else:
                #
                oFile = open( sFileTo, 'wb' )
                oFile.write( sContents )
                oFile.close()
                #
                iCopiedFile = 1
                #
            #
        else:   # big
            #
            try:
                #
                fFrom   = open( sFileFrom,  'rb' )
                fTo     = open( sFileTo,    'wb' )
                #
                while True:
                    #
                    sGotSome    = fFrom.read( iBlock )
                    #
                    if not sGotSome: break
                    #
                    fTo.write( sGotSome )
                    #
                #
                iCopiedFile = 1
                #
                fFrom.close()
                fTo.close()
                #
            except:
                #
                sType, sValue, oTraceBack = exc_info()
                print3( 'Error reading', sFileFrom, '-- skipped' )
                print3( sType, sValue )
                #
    #
    if bGotStats and isfile( sFileTo ):
        #
        utime( sFileTo, ( st_atime, st_mtime ) )
        #
    #
    return iCopiedFile


def CopyAllFiles( sDirFrom, sDirTo, uWantExtensions = [] ):
    #
    from File.Test      import isFileThere
    from Iter.AllVers   import iZip
    #
    if type( uWantExtensions ) == dict:
        #
        dWantExtensions = uWantExtensions
        #
    else:
        #
        dWantExtensions = dict( iZip( lWantExtensions, [None] * len( lWantExtensions ) ) )
        #
    #
    if iVerbose > 3: print3( 'in CopyAllFiles, copying from', sDirFrom, 'to', sDirTo )
    #
    global iDirCount, iFileCount
    #
    lFiles  = listdir( sDirFrom )
    #
    for sFile in lFiles:
        #
        sFileFrom   = join( sDirFrom, sFile )
        sFileTo     = join( sDirTo,   sFile )
        #
        if isdir( sFileFrom ):
            #
            if iVerbose > 3: print3( 'copying directory', sFileFrom, 'to', sFileTo, '...' )
            #
            try:
                #
                if not exists( sFileTo ):
                    #
                    mkdir( sFileTo )
                    #
                #
                CopyAllFiles( sFileFrom, sFileTo, dWantExtensions )
                #
                iDirCount += 1
                #
            except:
                #
                sType, sValue, oTraceBack = exc_info()
                print3( 'Error creating dir', sFileTo, '-- skipped' )
                print3( sType, sValue )
                #
        elif isfile( sFileFrom ):
            #
            if not isFileThere( sFileTo ): # skip if alread there
                #
                try:
                    #
                    if iVerbose > 7:
                        print3( 'copying', sFileFrom, 'to', sFileTo )
                    #
                    iCopiedFile = CopyOneFile(
                                    sFileFrom, sFileTo,
                                    dWantExtensions = dWantExtensions )
                    #
                    iFileCount += iCopiedFile
                    #
                except:
                    #
                    sType, sValue, oTraceBack = exc_info()
                    print3( 'Error copying', 
                           sFileFrom, 'to', sFileTo, '-- skipped' )
                    print3( sType, sValue )
                #


def ImIf( bCondition, uTrue, uFalse ):  # Immediate If
    #
    return ( uTrue, uFalse )[ not bCondition ]



def getArgs( *args ):
    #
    global lWantExtensions
    #
    sWantExtensions = ''
    lWantExtensions = []
    #
    sDirFrom, sDirTo = None, None
    #
    # print3( len( args ) )
    try:
        if len( args ) == 2:
            sDirFrom, sDirTo = args[ : 2 ]
        elif len( argv ) > 2:
            sDirFrom, sDirTo, sWantExtensions = args[ : 3 ]
            print3( sDirFrom, sDirTo, sWantExtensions )
    except:
        print3( 'Usage: CopyDir DirFrom DirTo [WantOnlyExtensionsInList]' )
    else:
        #
        lWantExtensions = sWantExtensions.split( ',')
        #
        lWantExtensions = [ sWant.strip() for sWant in lWantExtensions if sWant.strip() != '' ]
        #
        lWantExtensions = [ ImIf( sWant.startswith( '.' ), sWant, '.' + sWant )
                            for sWant in lWantExtensions ]
        #
        lWantExtensions = [ sWant.lower() for sWant in lWantExtensions ]
        #
        print3( sDirFrom )
        print3( sDirTo )
        #
        if not isdir( sDirFrom ):
            print3( 'Error: DirFrom is not a directory!' )
        elif not exists( sDirTo ):
            #
            mkdir( sDirTo )
            print3( 'Note: DirTo was created' )
            #
        else:
            #
            print3( 'Warning: DirTo already exists' )
            #
            if sDirFrom == sDirTo or samefile( sDirFrom, sDirTo ):
                #
                print3( 'Error, DirFrom is the same as DirTo!' )
                #
    #
    return sDirFrom, sDirTo, lWantExtensions


def main( sDirFrom = None, sDirTo = None, lWantExtensions = '' ):
    #
    import time
    #
    sDirFrom, sDirTo, lWantExtensions = getArgs( sDirFrom, sDirTo, lWantExtensions )
    #
    if sDirFrom is not None and sDirTo is not None:
        #
        print3( 'Copying ...' )
        #
        iStart  = time.time()
        #
        #
        CopyAllFiles( sDirFrom, sDirTo, lWantExtensions )
        #
        print3( 'Copied', iFileCount, 'files,', iDirCount, 'directories' )
        print3( 'in', round( time.time() - iStart, 1 ), 'seconds' )



if __name__ == '__main__':
    #
    from sys import argv
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    args = argv[ 1 : ]
    #
    if args:
        main( *args )
    else:
        #
        print3( 'Usage: CopyDir DirFrom DirTo [WantOnlyExtensionsInList]' )
        print3( 'self testing ...' )
        #
        #
        sayTestResult( lProblems )