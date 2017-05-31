#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Utility functions get
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
# Copyright 2004-2017 Rick Graves
#
#

def getMainNamePath():
    #
    from os.path    import split
    from sys        import argv
    #
    sPath, sScript = split(argv[0])
    #
    return sScript, sPath


def getTrue( *args, **kwargs ): return True


def getExample( u ):
    #
    from six            import next as getNext
    #
   #from Utils.Both2n3  import getNext
    #
    def getGenerator():
        #
        for item in u:
            #
            if item:
                #
                yield item
    #
    return getNext( getGenerator() )



if __name__ == "__main__":
    #
    from Iter.AllVers   import iRange
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if not getMainNamePath():
        #
        lProblems.append( 'getMainNamePath()' )
        #
    #
    fRange = iRange(8)
    #
    if getExample( fRange ) != 1:
        #
        lProblems.append( 'getExample()' )
        #
    #
    sayTestResult( lProblems )