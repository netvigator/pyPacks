#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# string functions Stats
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
# Copyright 2004-2011 Rick Graves
#


def AscStats( sString ):
    #
    from Iter.AllVers   import tMap
    from Numb.Stats import getMeanMembers
    from Object.Get import ValueContainer
    #
    tOrds       = tMap( ord, sString )
    #
    iMin        = min( tOrds )
    iMax        = max( tOrds )
    #
    fAvg        = getMeanMembers( *tOrds )
    #
    iTotal      = int( round( fAvg * len( tOrds ) ) )
    #
    iLast       = tOrds[0]
    #
    iLength     = len( sString )
    #
    iDifference = 0
    #
    for iOrd in tOrds:
        #
        iDifference += abs( iOrd - iLast )
        #
        iLast       = iOrd
        #
    #
    oReturn = ValueContainer(
                    fAvg        = fAvg,
                    iDifference = iDifference,
                    iLength     = iLength,
                    iMin        = iMin,
                    iMax        = iMax,
                    iTotal      = iTotal )
    #
    return oReturn




if __name__ == "__main__":
    #
    from string import digits
    from string import ascii_letters   as letters
    from string import ascii_uppercase as uppercase
    from string import ascii_lowercase as lowercase
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    sLines  = ' \n'.join( ( digits, lowercase, digits, uppercase, digits ) )
    #
    oTest   = AscStats( sLines )
    #
    if      oTest.fAvg          != 73.388888888888886   or \
            oTest.iDifference   != 581                  or \
            oTest.iLength       != 90                   or \
            oTest.iMin          != 10                   or \
            oTest.iMax          != 122                  or \
            oTest.iTotal        != 6605                 :
        #
        lProblems.append( 'AscStats()' )
        #
    #
    sayTestResult( lProblems )