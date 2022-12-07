#!/home/rick/.local/bin/pythonTest
# -*- coding: utf-8 -*-
#
# dir functions get
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
#   http://www.gnu.org/licenses/
#
# Copyright 2004-2023 Rick Graves
#

from errno                  import EEXIST
from os                     import makedirs, sep as cSep
from os.path                import exists, isdir, join

try:
    from .Test              import isDirThere
    from ..File.Del         import DeleteIfExists
    from ..File.Test        import isFileThere
    from ..Utils.Both2n3    import PYTHON2
except ( ValueError, ImportError ):
    from Dir.Test           import isDirThere
    from File.Del           import DeleteIfExists
    from File.Test          import isFileThere
    from Utils.Both2n3      import PYTHON2


if PYTHON2:
    class FileExistsError(OSError):
        def __init__(self, msg):
            super(FileExistsError, self).__init__(EEXIST, msg)


def _stripLeadingSlash( sDir ):
    if sDir[:1] == cSep: sDir = sDir[1:]
    return sDir


def _getPastNextSlash( sDir ):              # returns stuff after next slast
    sDir = _stripLeadingSlash( sDir )
    iSlashAt    = sDir.find( cSep )
    if iSlashAt > 0:
        sDir = sDir[iSlashAt + 1 :]
    else:
        sDir = ''
    return sDir




def getDirBelow( sHeadDir, sHeadAndBelow ):
    #
    # was used in LagMirror
    #
    sEatDirHead     = sHeadDir
    sEatDirSub      = sHeadAndBelow
    #
    while sEatDirHead != '':
        #
        sEatDirHead = _getPastNextSlash( sEatDirHead )
        sEatDirSub  = _getPastNextSlash( sEatDirSub  )
        #
    #
    iEat            = len( sHeadAndBelow ) - len( sEatDirSub )
    #
    return sHeadAndBelow[ iEat : ]



def getMakeDir( *sDir, **kwargs ):
    #
    iMode     = kwargs.get( 'iMode',    0o777 )
    bExistsOK = kwargs.get( 'bExistsOK', True )
    #
    sDir = join( *sDir )
    #
    if isFileThere( sDir ): DeleteIfExists( sDir )
    #
    if not isdir( sDir ) or not exists( sDir ):
        #
        # hit a FileExistsError 2019-08-11
        #
        try:
            if PYTHON2:
                #
                makedirs( sDir, mode = iMode )
                #
            else:
                #
                makedirs( sDir, mode = iMode, exist_ok = bExistsOK )
                #
        except FileExistsError:
            #
            pass
            #



def _getTempDir():
    #
    #
    if cSep == '/':
        #
        sTempDir = '/tmp'
        #
    else:
        #
        sTempDir = 'C:\\temp'
        #
        if not isDirThere( sTempDir ):
            #
            getMakeDir( sTempDir )
            #
        #
    #
    return sTempDir

sTempDir = _getTempDir()

#from os.path   import join
#from Dir.Get   import sTempDir, sDurableTempDir


def _getDurableTempDir():
    #
    sTempDir = _getTempDir()
    #
    if sTempDir.startswith( cSep ):
        #
        sTempDir = '/var%s' % sTempDir
        #
    #
    return sTempDir

sDurableTempDir = _getDurableTempDir()


'''

def getThisFileSpec( sFullSpec ):
def getThisFileSpec( sFileName ):
this is in Utils.Both2n3
this note is to aid any text search for the function
'''



if __name__ == "__main__":
    #
    from os             import mkdir, rmdir
    from os.path        import exists, join
    #
    from File.Get       import Touch
    from Utils.Result   import sayTestResult
    from Utils.Both2n3  import print3
    #
    lProblems = []
    #
    if getDirBelow( '/home/Common/', '/home/Common/Python/Dir' ) != 'Python/Dir':
        #
        lProblems.append( 'getDirBelow()' )
        #
    #
    sWillMake = join( sTempDir, 'test' )
    #
    DeleteIfExists( sWillMake )
    #
    getMakeDir( sTempDir, 'test' )
    #
    if not exists( join( sTempDir, 'test' ) ):
        #
        lProblems.append( 'getMakeDir() /tmp test' )
        #
    else:
        #
        rmdir( join( sTempDir, 'test' ) )
        #
    #
    getMakeDir( join( sTempDir, 'test' ) )
    #
    if not exists( join( sTempDir, 'test' ) ):
        #
        lProblems.append( 'getMakeDir() /tmp/test' )
        #
    else:
        #
        rmdir( join( sTempDir, 'test' ) )
        #
    #
    DeleteIfExists( join( sTempDir, 'test' ) )
    #
    Touch( join( sTempDir, 'test' ) )
    #
    try:
        #
        getMakeDir( join( sTempDir, 'test' ) )
        #
    except FileExistsError:
        #
        lProblems.append(
            'getMakeDir() hits error if file with same name exists' )
        #
    #
    if sTempDir not in ( sTempDir, 'C:\\temp' ):
        #
        print3( 'sTempDir:', sTempDir )
        lProblems.append( '_getTempDir()' )
        #
    if sDurableTempDir not in ( '/var/tmp', 'C:\\temp' ):
        #
        lProblems.append( '_getDurableTempDir()' )
        #
        
    #
    sayTestResult( lProblems )
