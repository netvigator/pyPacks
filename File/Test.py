#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# File functions Test
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
# Copyright 2004-2015 Rick Graves
#

#from os.path import join, isfile, getmtime, split, splitext, exists, basename, isdir
#from os      import stat, environ, getcwd, listdir, rename, remove


def isFileThere( *sFileSpec ):
    #
    from os.path    import isfile
    #
    from File.Spec  import getFullSpec
    #
    sFullSpec   = getFullSpec( *sFileSpec )
    #
    return isfile( sFullSpec ) # bFileThere




def hasWritePrivilege( sDir = None ):
    #
    from os         import remove
    from os.path    import isdir
    #
    from File.Get   import getTempFile
    #
    if not sDir: sDir = '.'
    #
    if isdir( sDir ):
        #
        try:
            #
            sTempFile = getTempFile( dir = sDir )
            #
            remove( sTempFile )
            #
            bHasWritePrivilege = True
            #
        except OSError:
            #
            bHasWritePrivilege = False
            #
        #
    else:
        #
        bHasWritePrivilege = False
        #
    #
    return bHasWritePrivilege




if __name__ == "__main__":
    #
    lProblems = []
    #
    from os             import remove
    from os.path        import split
    #
    from Dir.Get        import sTempDir
    from File.Get       import getTempFile
    from Utils.Result   import sayTestResult
    #
    sTemp = getTempFile()
    #
    if not isFileThere( sTemp ):
        #
        lProblems.append( 'isFileThere() full spec' )
        #
    #
    sDir, sFile = split( sTemp )
    #
    if not isFileThere( sDir, sFile ):
        #
        lProblems.append( 'isFileThere() sDir, sFile' )
        #
    #
    remove( sTemp )
    #
    if    ( not hasWritePrivilege( sTempDir      ) or
                hasWritePrivilege( '/etc'        ) or
                hasWritePrivilege( 'c:\\Windows' ) ):
        #
        lProblems.append( 'hasWritePrivilege()' )
        #
    #
    sayTestResult( lProblems )