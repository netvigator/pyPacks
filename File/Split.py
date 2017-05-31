#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# had huge file, too big for editors
# this breaks the file into bite-sized chunks
#
from os.path        import join

from six            import print_ as print3

from Dir.Get        import sTempDir
from File.Get       import getFileObject
from File.Spec      import getFullSpecDefaultOrPassed


class ReallyFinished( Exception ): pass

class PartlyFinished( Exception ): pass


def doMain( *sFileSpec ):
    #
    iThisFile       = -1
    #
    kwargs = { 'sDefault' : join( sTempDir, 'Test.txt' ) }
    #
    sBigFile = getFullSpecDefaultOrPassed( *sFileSpec, **kwargs )
    #
    fBigFile        = getFileObject( sBigFile )
    #
    sLine           = ''
    #
    try:
        #
        while True:
            #
            try:
                #
                iThisFile   += 1
                #
                sThisFile   = '%03d.txt' % iThisFile
                #
                if sLine == '':
                    #
                    print3( '%s ...' % sThisFile )
                    #
                else:
                    #
                    print3( sLine )
                #
                fFilePart   = getFileObject( sThisFile, sMode = 'w' )
                #
                if sLine    != '':
                    #
                    fFilePart.write( sLine )
                    #
                #
                for sLine in fBigFile:
                    #
                    sStrip   = sLine.rstrip()
                    #
                    if sStrip.endswith( 'FROM stdin;' ):
                        #
                        raise PartlyFinished
                    #
                    fFilePart.write( sLine )
                    #
                #
                fFilePart.close()
                #
                raise ReallyFinished
                #
                #
            except PartlyFinished:
                #
                fFilePart.close()
                #
                continue
                #
    except ReallyFinished:
        #
        pass
    #
    fBigFile.close()



if __name__ == "__main__":
    #
    from sys import exit, argv
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    args = argv[ 1 : ]
    #
    if args:
        try:
            #
            doMain( *args )
        except KeyboardInterrupt:
            print3( "\n\nExiting on user cancel." )
            # >> stderr, 
            # doUnlock( PID_FILE )
            exit(1)
    else:
        #
        print3( 'Usage: Split {filename}' )
        print3( 'self testing ...' )
        #
        #
        sayTestResult( lProblems )