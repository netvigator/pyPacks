#!/home/rick/bin/pythonTest
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
#   http://www.gnu.org/licenses/
#
# Copyright 2004-2020 Rick Graves
#

try:
    from ..Collect.Get  import getListFromNestedLists
    from ..Iter.AllVers import tMap, iRange, tZip
    from ..Numb.Stats   import getMeanMembers
    from ..Object.Get   import ValueContainer
    from ..String.Eat   import eatPunctuationBegAndEnd
    from ..String.Find  import getRegExObj
    from ..String.Test  import isPunctuation, isNotPunctuation
except ( ValueError, ImportError ):
    from Collect.Get    import getListFromNestedLists
    from Iter.AllVers   import tMap, iRange, tZip
    from Numb.Stats     import getMeanMembers
    from Object.Get     import ValueContainer
    from String.Eat     import eatPunctuationBegAndEnd
    from String.Find    import getRegExObj
    from String.Test    import isPunctuation, isNotPunctuation

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


_oFindParens = getRegExObj( '[()]' )
    


def getLocationsDict( s, bCarefulWithParens = True ):
    #
    '''pass a string with spaces between "words"
    returns a dictionary
    keys are the words
    values are tuples, inside each are
    integers, the positions of the words
    leftmost word is position 0 (python style)
    '''
    #
    sCareful = s
    #
    if bCarefulWithParens:
        #
        lParens = _oFindParens.findall( s )
        #
        if lParens:
            #
            lParts = _oFindParens.split( s )
            #
            lNewParts = []
            #
            for i in iRange( len( lParens ) ):
                #
                lNewParts.append( lParts[ i] )
                lNewParts.append( lParens[i])
                #
            #
            lNewParts.append( lParts[ -1 ] )
            #
            sCareful = ' '.join( lNewParts )
            #
        #
    #
    lWords = sCareful.split()
    #
    #
    dAllWordLocations = {}
    #
    for i in iRange( len( lWords ) ):
        #
        # if a word begins or ends with punctuation, strip the punctuation
        # if the "word" is punctuation only, keep it
        #
        sThisWord = eatPunctuationBegAndEnd( lWords[ i ] ) or lWords[ i ]
        #
        dAllWordLocations.setdefault( sThisWord, [] ).append( i )
        #
    #
    for k, v in dAllWordLocations.items():
        #
        dAllWordLocations[ k ] = tuple( v )
        #
    #
    return dAllWordLocations



def _isShorterSubstringOK( sLookForThis, dAllWordLocations, iShorterByOK ):
    #
    iLookAtThis = iInTitleLocation = None
    #
    for sWord in dAllWordLocations.keys():
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
            iInTitleLocation = dAllWordLocations[ sWord ][ 0 ]
            #
            break
            #
        #
    #
    return iInTitleLocation





def getSubStringLocation( sSubStr, dAllWordLocations, iShorterByOK = 0 ):
    #
    iInTitleLocation = None
    #
    if sSubStr in dAllWordLocations:
        #
        iInTitleLocation = dAllWordLocations[ sSubStr ][ 0 ] # first location
        #
    elif len( sSubStr ) > 2:
        #
        iInTitleLocation = _isShorterSubstringOK(
                sSubStr, dAllWordLocations, iShorterByOK )
        #
    #
    if iInTitleLocation is None:
        #
        tParts = tuple( map( eatPunctuationBegAndEnd, sSubStr.split() ) )
        #
        if len( tParts ) > 1:
            #
            bGotParts = True
            #
            for i, s in enumerate( tParts ):
                #
                if s in dAllWordLocations:
                    #
                    iThisPart = dAllWordLocations[ s ][ 0 ]
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
                                tParts[i], dAllWordLocations, iShorterByOK )

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



def _isLocationInParens( iLocation, iParenOpen, iParenClose ):
    #
    return iParenOpen < iLocation < iParenClose




def getSubStrLocationsBegAndEnd( dAllWordLocations, tLocationsOfInterest ):
    #
    # if a word is repeated, the prior position number will be missing
    #
    iMax = max( lLocations )
    #
    dLocations = dict.fromkeys( iRange( iMax + 1 ) ) # values are None
    #
    lLocations.sort()    # make sure they are listed low to high
    #
    for i in tLocationsOfInterest:
        #
        dLocations[ i ] = True
        #
    #
    lNearFront = []
    #
    for i in iRange( len( lLocations ) // 3 ):
        #
        if dLocations[ i ]:
            #
            lNearFront.append( i )
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
    setIgnoreThese = set( lOnEnd )
    #
    lOnEnd.reverse() # now low to high
    #
    lNearEnd = []
    #
    for i in iRange( len( lLocations ) // 3 ):
        #
        if dLocations[ lLocations[ i ] ]:
            #
            lNearEnd.append( lLocations[ i ] )
            #
        #
    #
    lNearEnd.reverse() # now low to high
    #
    tInParens = ()
    #
    if '(' in dAllWordLocations and ')' in dAllWordLocations:
        #
        tParenOpen  = dAllWordLocations[ '(' ]
        tParenClose = dAllWordLocations[ ')' ]
        #
        if len( tParenOpen ) == 1 or len( tParenClose ) == 1:
            #
            iParenOpen  = tParenOpen [  0 ]
            iParenClose = tParenClose[ -1 ]
            #
            def isWordInParens( s ):
                #
                iLocation = dAllWordLocations[ s ][ 0 ]
                #
                return _isLocationInParens( iLocation, iParenOpen, iParenClose )
                #
            #
        else:
            #
            tParenPairs = tZip( dAllWordLocations[ '(' ],
                                dAllWordLocations[ ')' ] )
            #
            def isWordInParens( s ):
                #
                iLocation = dAllWordLocations[ s ][ 0 ]
                #
                for tBegEnd in tParenPairs:
                    #
                    if _isLocationInParens(
                            iLocation, tBegEnd[0], tBegEnd[1] ):
                        #
                        return True
                        #
                    #
                # returns None if no location is within parens,
                # and None evaluates as False
                #
            #
        #
        lInParens = [ dAllWordLocations[k][0]
                      for k in dAllWordLocations
                      if isWordInParens( k ) and isNotPunctuation( k ) ]
        #
        lInParens.sort() # order not same python 2 vs 3, so need this
        #
        tInParens = tuple( lInParens )
        #
        setIgnoreThese.update( tInParens )
        #
    #
    lNearFront = [ s for s in lNearFront if s not in setIgnoreThese ]
    #
    return tuple( lNearFront ), tuple( lOnEnd ), tuple( lNearEnd ), tInParens





if __name__ == "__main__":
    #
    from pprint import pprint
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
    dAllWordLocations = getLocationsDict( sBig )
    #
    dExpect = { 'Jbl'       : ( 0, ),
                'L65'       : ( 1, ),
                'Jubal'     : ( 2, ),
                'Le5-12'    : ( 3, ),
                'Mids'      : ( 4, ),
                'Pair'      : ( 5, ),
                'Working'   : ( 6, ),
                'Nice'      : ( 7, ),
                'See'       : ( 8, ),
                'Pictures'  : ( 9, ) }
    #
    #
    if dAllWordLocations != dExpect:
        #
        pprint( dAllWordLocations )
        lProblems.append( 'getLocationsDict( "JBL L65" )' )
        #
    #
    if getSubStringLocation( sSub, dAllWordLocations ) != 3:
        #
        lProblems.append( 'getSubStringLocation( "JBL L65" )' )
        #
    #
    sSub = '15" SILVER'
    sBig = 'VINTAGE TANNOY GRF CORNER CABINET w. 15" SILVER DUAL CONCENTRIC DRIVER LSU/HF/15'
    #
    dAllWordLocations = getLocationsDict( sBig )
    #
    dExpect = { 'VINTAGE'   : (  0, ),
                'TANNOY'    : (  1, ),
                'GRF'       : (  2, ),
                'CORNER'    : (  3, ),
                'CABINET'   : (  4, ),
                'w'         : (  5, ),
                '15'        : (  6, ),
                'SILVER'    : (  7, ),
                'DUAL'      : (  8, ),
                'CONCENTRIC': (  9, ),
                'DRIVER'    : ( 10, ),
                'LSU/HF/15' : ( 11, ) }
    #
    #
    if dAllWordLocations != dExpect:
        #
        lProblems.append( 'getLocationsDict( "VINTAGE TANNOY GRF" )' )
        #
    #
    #
    if getSubStringLocation( sSub, dAllWordLocations ) != 6:
        #
        lProblems.append( 'getSubStringLocation( "VINTAGE TANNOY" )' )
        #
    #
    sSub = "6SN7GT"
    sBig = "VINTAGE RCA 6SN7GTB ELECTRON TUBE NOS"
    #
    dAllWordLocations = getLocationsDict( sBig )
    #
    dExpect = { 'VINTAGE'   : ( 0, ),
                'RCA'       : ( 1, ),
                '6SN7GTB'   : ( 2, ),
                'ELECTRON'  : ( 3, ),
                'TUBE'      : ( 4, ),
                'NOS'       : ( 5, ) }
    #
    #
    if dAllWordLocations != dExpect:
        #
        lProblems.append( 'getLocationsDict( "VINTAGE RCA 6SN7GTB" )' )
        #
    #
    #
    if getSubStringLocation( sSub, dAllWordLocations, iShorterByOK = 1 ) != 2:
        #
        print3( getSubStringLocation( sSub, dAllWordLocations ) )
        lProblems.append( 'getSubStringLocation( "VINTAGE RCA" )' )
        #
    #
    # "A7" not in "Altec Lansing Magnificent A7-500-II Speakers pair"
    #
    #print3( dAllWordLocations )
    #print3( getSubStringLocation( sSub, dAllWordLocations, iShorterByOK = 1 ) )
    #
    sBig = ( "Amperex 6922 gold pin tube military edition "
             "audio grade gold pins 6DJ8 E88CC" )
    #
    dAllWordLocations = getLocationsDict( sBig )
    #
    def getLocationForSub( s ):
        return getSubStringLocation( s, dAllWordLocations )
    #
    tLocationsOfInterest = tuple(
            map( getLocationForSub, ( "6922", "6DJ8", "E88CC" ) ) )
    #
    tGot = getSubStrLocationsBegAndEnd(
                    dAllWordLocations, tLocationsOfInterest )
    #
    if tGot != ((1,), (11, 12), (11, 12), ()):
        #
        print3( tGot )
        lProblems.append(
                'getSubStrLocationsBegAndEnd( "Amperex 6922 gold" )' )
        #
    #
    tLocationsOfInterest = tuple(
            map( getLocationForSub, ( "6SN7GTB", "L65", "GRF" ) ) )
    #
    if getSubStrLocationsBegAndEnd(
            dAllWordLocations, tLocationsOfInterest ) != ((), (), (), ()):
        #
        lProblems.append(
                'getSubStrLocationsBegAndEnd( "6SN7GTB, L65, GRF" )' )
        #
    #
    sBig = ( "Valvo Heerlen E88CC NOS Grey Shield CCa 6DJ8 6922 "
             "CV2492 CV2493 CV5358 CV5472 6N23P 6N11 ECC88 PCC88 7DJ8" )
    #
    dAllWordLocations = getLocationsDict( sBig )
    #
    def getLocationForSub( s ):
        return getSubStringLocation( s, dAllWordLocations )
    #
    tTubeTypes = tuple( "E88CC CCa 6DJ8 6922 CV2492 CV2493 CV5358 CV5472 "
                        "6N23P 6N11 ECC88 PCC88 7DJ8".split() )
    #
    tLocationsOfInterest = tuple( map( getLocationForSub, ( tTubeTypes ) ) )
    #
    # print3( 'tLocationsOfInterest:', tLocationsOfInterest )
    #
    tGot = getSubStrLocationsBegAndEnd(
            dAllWordLocations, tLocationsOfInterest )
    #
    if ( tGot !=
         (  (2,),
            (6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17),
            (12, 13, 14, 15, 16, 17),
            () ) ):
        #
        print3( "E88CC CCa 6DJ8 6922 etc.:", tGot )
        lProblems.append(
                'getSubStrLocationsBegAndEnd( "E88CC CCa 6DJ8 6922 etc." )' )
        #
    #
    sBig = ( "2x  ECC88 / 6DJ8   TELEFUNKEN  <> tubes  - NOS  "
             "-  ( ~  7DJ8 / PCC88 )  MILITARY" )
    #
    dAllWordLocations = getLocationsDict( sBig )
    #
    def getLocationForSub( s ):
        return getSubStringLocation( s, dAllWordLocations )
    #
    tLocationsOfInterest = tuple( map( getLocationForSub, ( tTubeTypes ) ) )
    #
    tGot = getSubStrLocationsBegAndEnd(
                    dAllWordLocations, tLocationsOfInterest )
    #
    if tGot != ((1, 3), (), (12, 14), (12, 14)):
        #
        print3( "ECC88 / 6DJ8 (7DJ8/PCC88):", tGot )
        lProblems.append(
                'getSubStrLocationsBegAndEnd( "ECC88 / 6DJ8 (7DJ8/PCC88)" )' )
        #
    #
    sBig = "DYNACO ST-70 ORIGINAL CAGE (with meter) VG SHAPE ( 1 EA )"
    #
    dAllWordLocations = getLocationsDict( sBig )
    #
    dExpect = { '('         : ( 4, 10),
                ')'         : ( 7, 13),
                'DYNACO'    : ( 0,),
                'ST-70'     : ( 1,),
                'ORIGINAL'  : ( 2,),
                'CAGE'      : ( 3,),
                'with'      : ( 5,),
                'meter'     : ( 6,),
                'VG'        : ( 8,),
                'SHAPE'     : ( 9,),
                '1'         : (11,),
                'EA'        : (12,) }
    #
    if dAllWordLocations != dExpect:
        #
        lProblems.append(
                'dAllWordLocations( "DYNACO ST-70 ORIGINAL CAGE" )' )
        #
    #
    #
    def getLocationForSub( s ):
        return getSubStringLocation( s, dAllWordLocations )
    #
    tLocationsOfInterest = tuple( map( getLocationForSub, ( tTubeTypes ) ) )
    #
    tGot = getSubStrLocationsBegAndEnd(
                    dAllWordLocations, tLocationsOfInterest )
    #
    if tGot != ((), (), (), (5, 6, 11, 12)):
        #
        print3( tGot )
        lProblems.append(
                'getSubStrLocationsBegAndEnd( "DYNACO ST-70 ORIGINAL CAGE" )' )
        #
    #
    sBig = ( "AZ1 Valvo Pair! Mesh Plate Tube Valve Röhre "
             "Big Ballon Klangfilm AD1 Tested Good" )
    #
    dAllWordLocations = getLocationsDict( sBig )
    #
    dExpect = { 'AZ1':          ( 0,),
                'Valvo':        ( 1,),
                'Pair':         ( 2,),
                'Mesh':         ( 3,),
                'Plate':        ( 4,),
                'Tube':         ( 5,),
                'Valve':        ( 6,),
                'Röhre':        ( 7,),
                'Big':          ( 8,),
                'Ballon':       ( 9,),
                'Klangfilm':    (10,),
                'AD1':          (11,),
                'Tested':       (12,),
                'Good':         (13,),
                }
    
    if dAllWordLocations != dExpect:
        #
        lKeys = [ (v, k) for k, v in dAllWordLocations.items() ]
        lKeys.sort()
        #
        for v,k in lKeys:
            print3( k.ljust( 12), v )
        lProblems.append(
                'dAllWordLocations( "AZ1 Valvo Pair!" )' )
        #
    #
    def getLocationForSub( s ):
        return getSubStringLocation( s, dAllWordLocations )
    #
    #
    tTubeTypes = tuple( "AD1 AZ1".split() )
    #
    tLocationsOfInterest = tuple( map( getLocationForSub, tTubeTypes ) )
    #
    tGot = getSubStrLocationsBegAndEnd(
                    dAllWordLocations, tLocationsOfInterest )
    #
    if tGot != ((0,), (), (11,), ()):
        #
        print3( tGot )
        lProblems.append(
                'getSubStrLocationsBegAndEnd( "AZ1 Valvo Pair!" )' )
        #
    #
    '''
    #
    '''
    #
    sayTestResult( lProblems )
