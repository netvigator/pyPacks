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
# Copyright 2004-2020 Rick Graves
#

try:
    from ..Iter.AllVers import tMap
    from ..Numb.Stats   import getMeanMembers
    from ..Object.Get   import ValueContainer
    from ..String.Eat   import eatPunctuationBegAndEnd
    from ..String.Test  import isPunctuation
except ( ValueError, ImportError ):
    from Iter.AllVers   import tMap
    from Numb.Stats     import getMeanMembers
    from Object.Get     import ValueContainer
    from String.Eat     import eatPunctuationBegAndEnd
    from String.Test    import isPunctuation

def AscStats( sString ):
    #
    #
    tOrds       = tMap( ord, sString )
    #
    iMin        = min( tOrds )
    iMax        = max( tOrds )
    #
    fAvg        = getMeanMembers( *tOrds )
    #
    iTotal      = sum( tOrds )
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




def getLocationsDict( s ):
    #
    lWords = s.split()
    #
    dWordLocations = {}
    #
    for i in range( len( lWords ) ):
        #
        sThisWord = eatPunctuationBegAndEnd( lWords[ i ] )
        #
        dWordLocations[ sThisWord ] = i
        #
    #
    return dWordLocations



def _isShorterSubstringOK( sLookForThis, dWordLocations, iShorterByOK ):
    #
    iLookAtThis = iInTitleLocation = None
    #
    for sWord in dWordLocations.keys():
        #
        if len( sWord ) < len( sLookForThis ) + 1: continue
        #
        if sWord.startswith( sLookForThis ):
            #
            iLookAtThis = len( sLookForThis )
            #
        elif sWord.endswith( sLookForThis ):
            #
            iLookAtThis = len( sWord ) - len( sLookForThis ) - 1
            #
        #
        if ( iLookAtThis is not None and
             ( isPunctuation( sWord[ iLookAtThis ] ) or
               ( iShorterByOK and
                 len( sWord ) == len( sLookForThis ) + iShorterByOK ) ) ):
            #
            iInTitleLocation = dWordLocations[ sWord ]
            #
            break
            #
        #
    #
    return iInTitleLocation





def getSubStringLocation(
            sSubStr, dWordLocations, iShorterByOK = 0, bRecordSteps = False):
    #
    iInTitleLocation = None
    #
    if bRecordSteps and sSubStr == '15" SILVER':
        #
        print()
        print( 'dWordLocations.keys():')
        pprint(dWordLocations.keys())
        #
    if sSubStr in dWordLocations:
        #
        iInTitleLocation = dWordLocations[ sSubStr ]
        #
    elif len( sSubStr ) > 2:
        #
        iInTitleLocation = _isShorterSubstringOK(
                sSubStr, dWordLocations, iShorterByOK )
        #
    #
    if iInTitleLocation is None:
        #
        tParts = tuple( map( eatPunctuationBegAndEnd, sSubStr.split() ) )
        #
        if bRecordSteps and sSubStr == '15" SILVER':
            print( 'tParts:', tParts )
        #
        if len( tParts ) > 1:
            #
            bGotParts = True
            #
            for i, s in enumerate( tParts ):
                #
                if s in dWordLocations:
                    #
                    iThisPart = dWordLocations[ s ]
                    #
                    if bRecordSteps and sSubStr == '15" SILVER':
                        print( 's, iThisPart:', s, iThisPart )
                    #
                    if  i + 1 < len( tParts ):
                        #
                        if i + 2 == len( tParts ):
                            #
                            iInTitleLocation = iThisPart
                            #
                        #
                    elif i + 2 >= len( tParts ) and i > 0:
                        #
                        iInTitleLocation = _isShorterSubstringOK(
                                tParts[i], dWordLocations, iShorterByOK )

                        #
                    else:
                        #
                        bGotParts = False
                        #
                        break
                        #
                    #
                    #
                else:
                    #
                    bGotParts = False
                    #
                    break
                    #
                #
                if iInTitleLocation is not None: break
                #
            #
        #
    #
    return iInTitleLocation


def getSubStrLocationsBegAndEnd( dWordLocations, tLocations ):
    #
    lLocations = list( dWordLocations.values() )
    #
    # if a word is repeated, the prior position number will be missing
    #
    iMax = max( lLocations )
    #
    dLocations = dict.fromkeys( range( iMax + 1 ) ) # values are None
    #
    lLocations.sort()    # make sure they are listed low to high
    #
    for i in tLocations:
        #
        dLocations[ i ] = True
        #
    #
    lTowardFront = []
    #
    for i in range( len( lLocations ) // 2 ):
        #
        if dLocations[ i ]:
            #
            lTowardFront.append( i )
            #
        #
    #
    lLocations.reverse() # make sure they are listed high to low
    #
    lOnEnd = []
    #
    for i in lLocations:
        #
        if dLocations[ i ]:
            #
            lOnEnd.append( i )
            #
        else:
            #
            break
            #
        #
    #
    return tuple( lTowardFront ), tuple( lOnEnd )





if __name__ == "__main__":
    #
    from string import digits
    from string import ascii_letters   as letters
    from string import ascii_uppercase as uppercase
    from string import ascii_lowercase as lowercase
    #
    from Utils.Result   import sayTestResult
    from Utils.Both2n3  import print3
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
    sSub = 'Le5'
    sBig = 'Jbl L65 Jubal Le5-12 Mids Pair Working Nice! See Pictures'
    #
    dWordLocations = getLocationsDict( sBig )
    #
    dExpect = { 'Jbl'       : 0,
                'L65'       : 1,
                'Jubal'     : 2,
                'Le5-12'    : 3,
                'Mids'      : 4,
                'Pair'      : 5,
                'Working'   : 6,
                'Nice'      : 7,
                'See'       : 8,
                'Pictures'  : 9 }
    #
    #
    if dWordLocations != dExpect:
        #
        lProblems.append( 'getLocationsDict( "JBL L65" )' )
        #
    #
    if getSubStringLocation( sSub, dWordLocations ) != 3:
        #
        lProblems.append( 'getSubStringLocation( "JBL L65" )' )
        #
    #
    sSub = '15" SILVER'
    sBig = 'VINTAGE TANNOY GRF CORNER CABINET w. 15" SILVER DUAL CONCENTRIC DRIVER LSU/HF/15'
    #
    dWordLocations = getLocationsDict( sBig )
    #
    dExpect = { 'VINTAGE'   :  0,
                'TANNOY'    :  1,
                'GRF'       :  2,
                'CORNER'    :  3,
                'CABINET'   :  4,
                'w'         :  5,
                '15'        :  6,
                'SILVER'    :  7,
                'DUAL'      :  8,
                'CONCENTRIC':  9,
                'DRIVER'    : 10,
                'LSU/HF/15' : 11 }
    #
    #
    if dWordLocations != dExpect:
        #
        lProblems.append( 'getLocationsDict( "VINTAGE TANNOY GRF" )' )
        #
    #
    #
    if getSubStringLocation( sSub, dWordLocations ) != 6:
        #
        lProblems.append( 'getSubStringLocation( "VINTAGE TANNOY" )' )
        #
    #
    sSub = "6SN7GT"
    sBig = "VINTAGE RCA 6SN7GTB ELECTRON TUBE NOS"
    #
    dWordLocations = getLocationsDict( sBig )
    #
    dExpect = { 'VINTAGE': 0,
                'RCA': 1,
                '6SN7GTB': 2,
                'ELECTRON': 3,
                'TUBE': 4,
                'NOS': 5}
    #
    #
    if dWordLocations != dExpect:
        #
        lProblems.append( 'getLocationsDict( "VINTAGE RCA 6SN7GTB" )' )
        #
    #
    #
    if getSubStringLocation( sSub, dWordLocations, iShorterByOK = 1 ) != 2:
        #
        print3( getSubStringLocation( sSub, dWordLocations ) )
        lProblems.append( 'getSubStringLocation( "VINTAGE RCA" )' )
        #
    #
    # "A7" not in "Altec Lansing Magnificent A7-500-II Speakers pair"
    #
    #print3( dWordLocations )
    #print3( getSubStringLocation( sSub, dWordLocations, iShorterByOK = 1 ) )
    #
    sBig = ( "Amperex 6922 gold pin tube military edition "
             "audio grade gold pins 6DJ8 E88CC" )
    #
    dWordLocations = getLocationsDict( sBig )
    #
    def getLocationForSub( s ):
        return getSubStringLocation( s, dWordLocations )
    #
    tLocations = tuple( map( getLocationForSub, ( "6922", "6DJ8", "E88CC" ) ) )
    #
    if getSubStrLocationsBegAndEnd(
            dWordLocations, tLocations ) != ((1,), (12, 11)):
        #
        lProblems.append(
                'getSubStrLocationsBegAndEnd( "Amperex 6922 gold" )' )
        #
    #
    tLocations = tuple( map( getLocationForSub, ( "6SN7GTB", "L65", "GRF" ) ) )
    #
    if getSubStrLocationsBegAndEnd(
            dWordLocations, tLocations ) != ((), ()):
        #
        lProblems.append(
                'getSubStrLocationsBegAndEnd( "6SN7GTB, L65, GRF" )' )
        #
    #
    
    sayTestResult( lProblems )
