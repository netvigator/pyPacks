#!/usr/bin/pythonTest
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
#   http://www.gnu.org/licenses/gpl.html
#
# Copyright 2004-2016 Rick Graves
#

from os import sep as cSep


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



def getMakeDir( *sDir ):
    #
    from os      import makedirs
    from os.path import exists, isdir, join
    #
    sDir = join( *sDir )
    #
    if not isdir( sDir ) or not exists( sDir ):
        #
        makedirs( sDir )


def _getTempDir():
    #
    from Dir.Test import isDirThere
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



if __name__ == "__main__":
    #
    from os             import mkdir, rmdir
    from os.path        import exists, join
    #
    from six            import print_ as print3
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if getDirBelow( '/home/Common/', '/home/Common/Python/Dir' ) != 'Python/Dir':
        #
        lProblems.append( 'getDirBelow()' )
        #
    #
    if exists( join( sTempDir, 'test' ) ): rmdir( join( sTempDir, 'test' ) )
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