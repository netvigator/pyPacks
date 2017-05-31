#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions want links
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
# Copyright 2015-2016 Rick Graves
#


def getUniqueLinks( sReadFile, sOutFile ):
    #
    from File.Get       import getListFromFileLines
    from File.Write     import QuickDumpLines
    #
    from Web.Address    import getHostPathTuple, getDomainOffURL
    from Web.Test       import isURL
    #
    lLines  = getListFromFileLines( sReadFile )
    #
    setLinks= frozenset( filter( isURL, lLines ) )
    #
    #
    lDecorate = [ ( getHostPathTuple( sURL ), sURL ) for sURL in setLinks ]
    #
    lDecorate = [ ( ( getDomainOffURL( t[0][0] ), t[0][1] ), t[1] ) for t in lDecorate ]
    #
    lDecorate.sort()
    #
    lLinks  = [ t[1] for t in lDecorate ]
    #
    QuickDumpLines( lLinks, sOutFile )




if __name__ == "__main__":
    #
    from os.path        import join
    from sys            import argv
    #
    from six            import print_ as print3
    #
    from Dir.Get        import sTempDir
    from File.Test      import isFileThere
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    args = argv[ 1 : ]
    #
    sReadFile   = join( sTempDir, 'LotsOfLinks.txt' )
    sOutFile    = join( sTempDir, 'UniqueLinks.txt' )
    #
    if args:
        #
        sReadFile       = args[0]
        #
        if len( args ) > 1:
            #
            sOutFile    = args[2]
            #
        #
    else:
        #
        if isFileThere( sReadFile ):
            #
            getUniqueLinks( sReadFile, sOutFile )
            #
        else:
            #
            print3( 'Usage: WantLinks [inputFile [, outputFile] ]' )
            print3( 'default inputFile  {temp dir}lotsolinks.txt' )
            print3( 'default outputFile {temp dir}UniqueLinks.txt' )
            #
        #
    #
    if False:
        #
        lProblems.append( 'getDotQuad4IspTester()' )
        #
    #
    #
    sayTestResult( lProblems )