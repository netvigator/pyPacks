#!/home/rick/.local/bin/pythonTest
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
#   http://www.gnu.org/licenses/
#
# Copyright 2004-2023 Rick Graves
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



def getRandomTrueOrFalse():
    #
    '''returns True or False at random'''
    #
    from random import randrange
    #
    return bool( randrange( 0, 1000 ) % 2 ) # randomly alternate


if __name__ == "__main__":
    #
    from Iter.AllVers   import iRange
    from Utils.Both2n3  import print3
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
    iTrue = iFalse = 0
    #
    for i in iRange(10000):
        #
        if getRandomTrueOrFalse():
            iTrue  += 1
        else:
            iFalse += 1
        #
    #
    if abs( iTrue - iFalse ) > 288: # got 258 2019-05-16
        #
        print3( 'iTrue :', iTrue )
        print3( 'iFalse:', iFalse)
        print3( 'difference:', abs( iTrue - iFalse ) )
        #
        lProblems.append( 'getRandomTrueOrFalse()' )
        #
    #        
    sayTestResult( lProblems )
