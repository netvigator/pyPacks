#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# File functions SelfTestScript
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
# Copyright 2012-2016 Rick Graves
#
'''
determine whether selftest.sh is complete,
list any python files omitted from global self test

'''

def _getSelfTestScriptFiles( sTestFile = 'selftest.sh' ):
    #
    from Dir.Get        import getParentDir
    from File.Get       import getFileObject
    from File.Spec      import getFullSpec
    from File.Test      import isFileThere
    from String.Get     import getTextAfter
    #
    sParentDir      = getParentDir()
    #
    iParentLen      = 1 + len( sParentDir )
    #
    if not isFileThere( sParentDir, sTestFile ):
        #
        print3( 'not there: %s' % getFullSpec( sParentDir, sTestFile ) )
        #
    #
    dFiles2Test     = {}
    dSkipFiles      = {}
    #
    setSkipDirs     = set()
    #
    oTestFile = getFileObject( sParentDir, sTestFile )
    #
    sDir            = ''
    #
    for sLine in oTestFile:
        #
        if sLine.startswith( 'cd ' ):
            #
            sDir    = sLine[ 3 : ].strip()
            #
            if not sDir.startswith( sParentDir ):
                #
                dFiles2Test[ sDir ] = set()
                #
            #
            continue
            #
        #
        if sLine.startswith( './' ):
            #
            sFile = sLine[ 2 : ].strip()
            #
            dFiles2Test[ sDir ].add( sFile )
            #
            continue
            #
        #
        if sLine.startswith( '#' ):
            #
            if 'cd ' in sLine:
                #
                sDir = getTextAfter( sLine, 'cd ' ).strip()
                #
                setSkipDirs.add( sDir )
                #
                continue
            #
            if './' in sLine:
                #
                if sDir not in dSkipFiles:
                    #
                    dSkipFiles[ sDir ] = set()
                    #
                #
                sFile = getTextAfter( sLine, './' ).strip()
                #
                dSkipFiles[ sDir ].add( sFile )
                #
        #
    #
    return sParentDir, dFiles2Test, setSkipDirs, dSkipFiles




def testSelfTestScript( sTestFile = 'selftest.sh' ):
    #
    from os             import walk, sep
    #
    from six            import print_ as print3
    #
    from Dict.Get       import getKeyIter
    from Iter.AllVers   import tFilter
    from String.Get     import getTextAfterLast
    #
    def isPySource( s ): return s.endswith( '.py' )
    #
    t = _getSelfTestScriptFiles( sTestFile )
    #
    sParentDir, dFiles2Test, setSkipDirs, dSkipFiles = t
    #
    oFileWalk   = walk( sParentDir )
    #
    tParent     = getNext( oFileWalk )
    #
    dOmitted    = {}
    #
    for tDir in oFileWalk:
        #
        if not tDir: continue
        #
        sDir    = getTextAfterLast( tDir[0], sep )
        #
        if sDir in setSkipDirs: continue
        #
        tFiles  = tFilter( isPySource, tDir[2] )
        #
        if not tFiles: continue
        #
        if sDir not in dFiles2Test: dFiles2Test[ sDir ] = set()
        #
        def isNotSelfTested( s ):
            return s not in dFiles2Test[ sDir ] and s != '__init__.py'
        #
        tOmitted = tFilter( isNotSelfTested, tFiles )
        #
        if tOmitted:
            #
            dOmitted[ sDir ] = set( tOmitted )
            #
        #
    #
    lDirs = [ ( k.upper(), k ) for k in getKeyIter( dOmitted ) if dOmitted[ k ] ]
    #
    lDirs.sort()
    #
    tResults = ( '', '#' )
    #
    def isFileCommented( sDir, sFile ):
        #
        return tResults[ bool( sDir in dSkipFiles and sFile in dSkipFiles[ sDir ] ) ]
        #
    #
    if lDirs: print3( '\nThe following are not self tested by the shell script:' )
    #
    for t in lDirs:
        #
        sDir = t[1]
        #
        print3( sDir )
        #
        lFiles = [ ( s.upper(), s ) for s in dOmitted[ sDir ] ]
        #
        lFiles.sort()
        #
        for tFile in lFiles:
            #
            sFile = tFile[1]
            #
            print3( '  %s%s' % ( isFileCommented( sDir, sFile ), sFile ) )
        





if __name__ == "__main__":
    #
    lProblems = []
    #
    from sys            import argv
    #
    from Utils.Result   import sayTestResult
    #
    args = argv[ 1 : ]
    #
    if args:
        #
        testSelfTestScript()
    #
    sayTestResult( lProblems )