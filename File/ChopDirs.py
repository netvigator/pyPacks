#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# File functions ChopDirs
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
(not self testing)
'''

from os.path        import split, splitext

from six            import print_ as print3

from Iter.AllVers   import iZip
from String.Find    import getFinderFindAll

oPrefFinder = getFinderFindAll( '^\d{5}(?:_|\d{2},)' )
oSuffFinder = getFinderFindAll( '_12[2|3]_\d{1,5}lo' )
oShorFinder = getFinderFindAll(         '_\d{1,5}lo' )



def getArgs( args ):
    #
    from os.path import isdir
    #
    sChopDir = None
    #
    try:
        if len( args ) == 1:
            sChopDir = args[ 0 ]
        elif len( args ) > 1:
            print3( args )
    except:
        print3( 'Usage: ChopDirs {sChopDir}' )
    else:
        #
        if not isdir( sChopDir ):
            print3( 'Error: sChopDir is not a directory!' )
            sChopDir = None
    #
    return sChopDir


def _getNaExtOffFullSpec( s ): return split( s )[1]

def _getNameOffFullSpec( s ): return splitext( split( s )[1] )[0]

def _getExtnOffFullSpec( s ): return splitext( s )[1]



def ChopOneName( sName ):
    #
    from String.Get import getTextBefore
    #
    lPref           = oPrefFinder( sName )
    lSign           = oSuffFinder( sName )
    lShort          = oShorFinder( sName )
    #
    sNewName        = sName
    #
    if lPref:
        #
        sNewName    = sName[ len( lPref[0] ) : ]
        #
    if lSign or lShort:
        #
        iEndChop    = len(
                        ( lSign  and lSign[0]  ) or
                        ( lShort and lShort[0] ) )
        #
        sNewName    = sNewName[ : - iEndChop ]
        #
    #
    return sNewName


def RenameAll( sChopDir, lNaExt, lNewNs ):
    #
    from os      import rename
    from os.path import join
    #
    for sOrig, sNew in iZip( lNaExt, lNewNs ):
        #
        sOrig   = join( sChopDir, sOrig )
        sNew    = join( sChopDir, sNew  )
        #
        rename( sOrig, sNew )
        #


def RenameCarefully( sChopDir, lNames, lExtns, lNaExt, lNewNs ):
    #
    from os      import rename
    from os.path import join, exists
    #
    dNew    = dict.fromkeys( lNames, 0 )
    #
    for sName, sExt, sOrig, sNew in iZip( lNames, lExtns, lNaExt, lNewNs ):
        #
        sPathNew        = join( sChopDir, sNew  )
        #
        while exists( sPathNew ):
            #
            dNew[ sName ] += 1
            #
            sNew        = '%s-%s%s' % ( sName, dNew[ sName ], sExt )
            #
            sPathNew    = join( sChopDir, sNew  )
            #
        #
        sPathOrig        = join( sChopDir, sOrig )
        #
        rename( sPathOrig, sPathNew )
        #


def ChopNames( sChopDir ):
    #
    from os      import listdir
    from os.path import isfile, isdir, join, exists
    #
    from Collect.Query  import get1stThatMeets
    from Iter.AllVers   import iFilter, tFilter, iMap, tMap
    #
    def WholeFileSpec( s ): return join( sChopDir, s )
    #
    tFiles      = tFilter( isfile, tMap( WholeFileSpec, listdir( sChopDir ) ) )
    #
    if tFiles:
        #
        tNaExt  = tMap( _getNaExtOffFullSpec, tFiles )
        #
        tNames  = tMap( _getNameOffFullSpec, tFiles )
        #
        lExtns  = tMap( _getExtnOffFullSpec, tFiles )
        #
        tNewNs  = tMap( ChopOneName, tNames )
        #
        tNewNs  = [ '%s%s' % (sN, sE ) for sN, sE in iZip( tNewNs, lExtns ) ]
        #
        setNew  = frozenset( tNewNs )
        #
        if tNaExt == tuple( tNewNs ):
            #
            pass # print3( 'no name changes for', sChopDir
            #
        elif len( setNew ) == len( tNaExt ):
            #
            lPathNew = iMap( WholeFileSpec, tNewNs )
            #
            if get1stThatMeets( lPathNew, exists ):
                #
                RenameCarefully( sChopDir, tNames, lExtns, tNaExt, tNewNs )
                #
            else:
                #
                RenameAll( sChopDir, tNaExt, tNewNs )
                #
            #
        elif len( setNew ) >= 0.9 * len( tNaExt ):
            #
            RenameCarefully( sChopDir, tNames, lExtns, tNaExt, tNewNs )
            #
        else:
            #
            print3( 'fail, in %s got %s orig and %s new' % \
                ( sChopDir, len( tNaExt ), len( setNew ) ) )
            #
    #


def main( sChopDir ):
    #
    import time
    #
    sChopDir = getArgs( sChopDir )
    #
    if sChopDir is not None:
        #
        print3( 'Chopping file names...' )
        #
        iStart  = time.time()
        #
        ChopNames( sChopDir )



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
        print3( 'Usage: ChopDirs {sChopDir}', 'self testing ...', sep = '\n' )
        #
        #
        sayTestResult( lProblems )