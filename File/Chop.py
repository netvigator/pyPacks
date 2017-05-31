#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# File functions Chop
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

'''
command line utility to change file names en masse

'''
from six            import print_ as print3

def ChopFileNames( iChopChars, sDir = '', sSeparator = '_', bChopFront = True ):
    #
    from os.path    import isfile, splitext, join, exists
    from os         import listdir, rename
    #
    from Iter.AllVers   import iFilter
    #
    if type( iChopChars ) == str and iChopChars.isdigit():
        #
        iChopChars = int( iChopChars )
        #
    #
    if type( iChopChars ) != int:
        #
        print3( 'must pass integer as iChopChars' )
        print3( 'instead got', iChopChars )
        return
        #
    #
    if sDir == '':
        #
        sDir = getcwd()
        #
    elif not exists( sDir ):
        #
        print3( '"%s" does not exist' % sDir )
        #
        #
    #
    lFiles = listdir( sDir )
    #
    def isRealFile( sFile ): return isfile( join( sDir, sFile ) )
    #
    lFiles = iFilter( isRealFile, lFiles )
    #
    bChopFront      = int( bChopFront ) # can come in as character
    #
    if bChopFront:
        #
        iSeparatorBeg = iChopChars - 1
        iSeparatorEnd = iChopChars
        #
        iDropPart =  0
        #
        def ChopName( sName ): return sName[ iChopChars : ]
        #
    else:
        #
        iSeparatorBeg = - iChopChars
        iSeparatorEnd = - iChopChars + 1
        #
        iDropPart = -1
        #
        def ChopName( sName ): return sName[ : - iChopChars ]
        #
    #
    for sFile in lFiles:
        #
        sName, sExt = splitext( sFile )
        #
        sNameChop = ''
        #
        if len( sName ) > iChopChars and sSeparator in sName:
            #
            if iChopChars > 0:
                #
                if sSeparator == sName[ iSeparatorBeg : iSeparatorEnd ]:
                    #
                    # found sSeparator where it was expected
                    #
                    sNameChop = ChopName( sName )
                    #
                #
                #
            else:
                #
                lParts = sName.split( sSeparator )
                #
                del lParts[ iDropPart ]
                #
                sName = sSeparator.join( lParts )
                #
            #
        #
        if sNameChop and sNameChop != sName:
            #
            sNewName = '%s%s' % ( sNameChop, sExt )
            #
            sNewPath = join( sDir, sNewName )
            #
            if exists( sNewPath ):
                #
                print3( 'cannot rename "%s" as "%s" already exists!' % (
                        sFile, sNewName ) )
                #
            else:
                #
                print3( '"%s" becomes "%s"' % ( sFile, sNewName ) )
                #
                rename(
                    join( sDir, sFile ),
                    sNewPath )
                #
            #
        #
    #




if __name__ == "__main__":
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
        ChopFileNames( *args )
    else:
        #
        print3( 'Usage: Chop( iChopChars[ sDir sSeparator bChopFront ] )' )
        print3( 'sDir defaults to current, sSeparator defaults to _, bChopFront defaults to Yes' )
        print3( 'self testing ...' )
        #
        #
        sayTestResult( lProblems )