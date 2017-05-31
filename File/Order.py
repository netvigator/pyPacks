#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# File functions Order
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

'''

def _isDigit( c ): return c.isdigit()


def _getEndDigits( s ):
    #
    from Iter.AllVers   import takewhile
    #
    lChars = list( s )
    #
    lChars.reverse()
    #
    iEndDigits  = 0
    #
    lEndDigits  = list( takewhile( _isDigit, lChars ) )
    #
    lEndDigits.reverse()
    #
    if not lEndDigits: lEndDigits = [ '0' ]
    #
    return ''.join( lEndDigits )



def _getMaxEndDigits( l ):
    #
    from Iter.AllVers import iMap
    #
    return max( iMap( len, l ) )



def OrderFileNames( sDir = '', iWantDigits = None, sSeparator = '_' ):
    #
    from os.path        import isfile, splitext, join, exists
    from os             import listdir, rename, getcwd
    #
    from six            import print_ as print3
    #
    from Collect.Get    import getSeparateKeysValues
    from Iter.AllVers   import tFilter, iMap, tMap, iZip
    #
    if type( iWantDigits ) == str and iWantDigits.isdigit():
        #
        iWantDigits = int( iWantDigits )
        #
    #
    if iWantDigits is not None and type( iWantDigits ) != int:
        #
        print3( 'must pass integer as iWantDigits' )
        print3( 'instead got', iWantDigits )
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
    
    #
    def isRealFile( sFile ): return isfile( join( sDir, sFile ) )
    #
    tFiles = tFilter( isRealFile, listdir( sDir ) )
    #
    lNames, lExts = getSeparateKeysValues( iMap( splitext, tFiles ) )
    #
    lEndDigits      = tMap( _getEndDigits, lNames )
    #
    if iWantDigits is None:
        #
        iWantDigits = _getMaxEndDigits( lEndDigits )
    #
    sFormat = '%s0%sd' % ( '%', iWantDigits )
    #
    for           sFile,  sName,  sExt,  sEndDigits in \
            iZip( tFiles, lNames, lExts, lEndDigits ):
        #
        sName       = sName[ : - len( sEndDigits ) ]
        #
        if sSeparator and sName and not sName.endswith( sSeparator ):
            #
            sName = sName + sSeparator
            #
        #
        sEndDigits  = sFormat % int( sEndDigits )
        #
        sNewName = '%s%s%s' % ( sName, sEndDigits, sExt )
        #
        sNewPath = join( sDir, sNewName )
        #
        if not exists( sNewPath ):
            #
            print3( '"%s" becomes "%s"' % ( sFile, sNewName ) )
            #
            rename(
                join( sDir, sFile ),
                sNewPath )
            #
        #
    #




if __name__ == "__main__":
    #
    from sys            import argv
    #
    from six            import print_ as print3
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    args = argv[ 1 : ]
    #
    if args:
        OrderFileNames( *args )
    else:
        #
        print3( 'self testing ...' )
        #
        #
        sayTestResult( lProblems )