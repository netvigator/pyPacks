#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Number functions Stats
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



def getMeanMembers( *Numbers ):
    #
    '''aka def ListAverage
    '''
    from Numb.Get import getSumOffList
    #
    if Numbers:
        lNumbs  = Numbers
    else:
        lNumbs  = [ 0 ]
    #
    return getSumOffList( *lNumbs ) / float( len( lNumbs ) )



def getPercent( fRatio, iDecimals = 1 ):
    #
    return round( fRatio * 100, iDecimals )




def MinExcludeZero( *Numbers ):
    #
    from Iter.AllVers import iFilter
    from Test     import isNumber
    #
    MinNumber   = None
    #
    def isNonZeroNumb( u ): return u and isNumber( u )
    #
    lNumbers    = iFilter( isNonZeroNumb, *Numbers )
    #
    MinNumber = min( lNumbers )
    #
    return MinNumber



if __name__ == "__main__":
    #
    from six            import print_ as print3
    #
    from Iter.AllVers   import iRange
    from Numb.Test      import areClose
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if getMeanMembers( 1, 2, 3 ) != 2.0:
        #
        lProblems.append( 'getMeanMembers() integers' )
        #
    if not areClose( 303.4, getMeanMembers( ( 1.1, 2.2, 300.1 ) ), 0.01 ):
        #
        print3( 'getMeanMembers( ( 1.1, 2.2, 300.1 ) ):',
                 getMeanMembers( ( 1.1, 2.2, 300.1 ) ) )
        lProblems.append( 'getMeanMembers() floats' )
        #
    if getPercent( .488 ) != 48.8:
        #
        lProblems.append( 'getPercent()' )
        #
    if getMeanMembers( 1, 2, 3 ) != 2.0:
        #
        lProblems.append( 'ListAverage()' )
        #
    if MinExcludeZero( iRange(5) ) != 1:
        #
        lProblems.append( 'MinExcludeZero()' )
        #

    #
    sayTestResult( lProblems )