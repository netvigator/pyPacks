#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# File functions Spec
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

from os.path    import join

from Dir.Get    import sTempDir, sDurableTempDir


def getPathNameExt( sSpec ):
    #
    from os.path import split, splitext
    #
    sPath, sFile = split( sSpec)
    #
    sFile, sExtn = splitext( sFile )
    #
    return sPath, sFile, sExtn



def getExtension( sFile ):
    #
    from os.path import splitext
    #
    sName, sExt = splitext( sFile )
    #
    return sExt



def getNameNoPathNoExt( sFullSpec ):
    #
    from os.path import splitext, basename
    #
    sName, sExt = splitext( basename( sFullSpec ) )
    #
    return sName



def _getPartsRight( tParts ):
    #
    '''must pass tuple with file spec parts
    '''
    #
    from os.path import isdir
    #
    while tParts and tParts[-1] is None:
        #
        tParts = tParts[ : -1 ]
        #
    #
    while tParts and tParts[0] is None:
        #
        tParts = tParts[ 1 : ]
        #
    #
    if len( tParts ) == 2 and isdir( tParts[1] ):
        #
        tParts = ( tParts[1], tParts[0] )
        #
    #
    return tParts


def _getFileSpecOffParts( tParts ):
    #
    '''must pass tuple with file spec parts
    '''
    #
    from os.path import join
    #
    tParts = _getPartsRight( tParts )
    #
    return join( *tParts )




def getFullSpec( *tParts ):
    #
    from String.Test import isStringLike
    #
    if isStringLike( tParts ):
        #
        sFileSpec = tParts
        #
    elif len( tParts ) == 1:
        #
        sFileSpec = tParts[0]
        #
    else: # not isStringLike( tParts )
        #
        sFileSpec = _getFileSpecOffParts( tParts )
        #
    #
    return sFileSpec



def getFullSpecDefaultOrPassed( *tParts, **kwargs ):
    #
    from String.Test import isStringLike
    #
    if not tParts:
        #
        sFileSpec = kwargs.get( 'sDefault', join( sTempDir, 'temp.txt' ) )
        #
    else:
        #
        sFileSpec = getFullSpec( *tParts )
        #
    #
    return sFileSpec




if __name__ == "__main__":
    #
    lProblems = []
    #
    from os.path import join, exists
    from os      import rename
    #
    from Dir.Get        import sTempDir
    from File.Del       import DeleteIfExists
    from Utils.Result   import sayTestResult
    #
    if getPathNameExt( '/home/Common/pyPacks/File/Spec.py' ) != \
            ('/home/Common/pyPacks/File', 'Spec', '.py'):
        #
        lProblems.append( 'getPathNameExt()' )
        #
    #

    if getExtension( '/home/Common/pyPacks/File/Spec.py' ) != '.py':
        #
        lProblems.append( 'getExtension()' )
        #
    #

    if getNameNoPathNoExt( '/home/Common/pyPacks/File/Spec.py' ) != 'Spec':
        #
        lProblems.append( 'getNameNoPathNoExt()' )
        #
    #
    sTempFile = join( sTempDir,        'temp.txt' )
    sDuraFile = join( sDurableTempDir, 'temp.txt' )
    #
    if    getFullSpec(                 'temp.txt' ) !=          'temp.txt':
        #
        lProblems.append( 'getFullSpec() temp.txt' )
        #
    #
    if    getFullSpec(         sTempDir, 'temp.txt' ) !=     sTempFile:
        #
        lProblems.append( 'getFullSpec() {temp dir} temp.txt two args' )
        #
    #
    if    getFullSpec(             '/tmp/temp.txt' ) !=     sTempFile:
        #
        lProblems.append( 'getFullSpec() {temp dir} temp.txt one arg' )
        #
    #
    if    getFullSpec( '/var', 'tmp', 'temp.txt' ) != join( sDurableTempDir, 'temp.txt' ):
        #
        lProblems.append( 'getFullSpec() /var{temp dir} temp.txt' )
        #
    #
    tIn1    = ( '/home/Common/pyPacks/File', 'Get.py' )
    tIn2    = ( 'Get.py', '/home/Common/pyPacks/File')
    #
    tWant   = ('/home/Common/pyPacks/File', 'Get.py')
    #
    sSpec   = '/home/Common/pyPacks/File/Get.py'
    #
    if      _getPartsRight( tIn1 ) != tWant or \
            _getPartsRight( tIn2 ) != tWant:
        #
        lProblems.append( '_getPartsRight()' )
        #
    #
    if _getFileSpecOffParts( tIn2 ) != sSpec:
        #
        lProblems.append( '_getFileSpecOffParts()' )
        #
    #
    if getFullSpec( *tIn2 ) != sSpec or getFullSpec( *tIn1 ) != sSpec:
        #
        lProblems.append( 'getFullSpec() passed two arguments' )
        #
    #
    if getFullSpec( sSpec ) != sSpec:
        #
        lProblems.append( 'getFullSpec() passed complete spec as string' )
        #
    #
    if getFullSpecDefaultOrPassed( *tIn2 ) != sSpec:
        #
        lProblems.append( 'getFullSpecDefaultOrPassed() passed two args' )
        #
    #
    if getFullSpecDefaultOrPassed()        != join( sTempDir, 'temp.txt' ):
        #
        lProblems.append( 'getFullSpecDefaultOrPassed() passed nothing' )
        #
    #
    if getFullSpecDefaultOrPassed( sSpec ) != sSpec:
        #
        lProblems.append( 'getFullSpecDefaultOrPassed() passed complete spec as string' )
        #
    #
    if      getFullSpec('/home/Common/pyPacks/File', 'Get.py') != \
                '/home/Common/pyPacks/File/Get.py' or \
            getFullSpec('/home/Common/pyPacks/File/Get.py') != \
                '/home/Common/pyPacks/File/Get.py':
        #
        lProblems.append( 'getFullSpec()' )
        #
    #
    sayTestResult( lProblems )