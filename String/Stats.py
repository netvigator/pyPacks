#!/home/rick/.local/bin/pythonTest
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
# Copyright 2004-2023 Rick Graves
#

from collections            import OrderedDict
from itertools              import chain
from string                 import digits, ascii_letters as letters

try:
    from ..Collect.Test     import TupleEndsWithable
    from ..Iter.AllVers     import tMap, iRange, tZip
    from ..Numb.Stats       import getMeanMembers
    from ..Object.Get       import ValueContainer, RandomFeeder
    from ..String.Eat       import eatPunctuationBegAndEnd
    from ..String.Find      import getRegExObj, oFinderPunctuation
    from ..String.Replace   import ReplaceManyOldWithManyNew
    from ..String.Test      import isPunctuation, isNotPunctuation
    from ..Utils.TimeTrial  import TimeTrial
except ( ValueError, ImportError ):
    from Collect.Test       import TupleEndsWithable
    from Iter.AllVers       import tMap, iRange, tZip
    from Numb.Stats         import getMeanMembers
    from Object.Get         import ValueContainer, RandomFeeder
    from String.Eat         import eatPunctuationBegAndEnd
    from String.Find        import getRegExObj, oFinderPunctuation
    from String.Replace     import ReplaceManyOldWithManyNew
    from String.Test        import isPunctuation, isNotPunctuation
    from Utils.TimeTrial    import TimeTrial

if __name__ == "__main__":
    #
    try:
        from ..Object.Get   import ValueContainerCanPrint as ValueContainer
    except ( ValueError, ImportError ):
        from Object.Get     import ValueContainerCanPrint as ValueContainer



IGNORE_JOINERS = frozenset( ( '/', '|' ) )



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
                    iTotal      = iTotal,
                    sString     = sString )
    #
    return oReturn



_oFindParens = getRegExObj( '([()])' )



def getLocationsDict( s, bCarefulWithParens = False ):
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
        sCareful = _oFindParens.sub( ' \\1 ', s )
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



def getLocationsDictOrig( s ):
    #
    return getLocationsDict( s, bCarefulWithParens = True )






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
        for sWord, tLocations in dAllWordLocations.items():
            #
            if sSubStr in sWord:
                #
                iInTitleLocation = tLocations[ 0 ]
                #
                break
                #
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



def _getSubStrLocationsBegAndEnd(
            dAllWordLocations, tLocationsOfInterest, bTrouble = False ):
    #
    # this is called by both
    # getStrLocationsBegAndEnd and _getStrLocationsBegAndEnd
    #
    # if a word is repeated, the prior position number will be missing
    #
    lLocations = list( chain.from_iterable( dAllWordLocations.values() ) )
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
    tIgnoreLocations = tuple(
        chain.from_iterable(
            [ dAllWordLocations[ s ]
            for s in dAllWordLocations.keys()
            if s in IGNORE_JOINERS ] ) )
    #
    if bTrouble:
        print3( 'dLocations:' )
        pprint( dLocations )
        print3( 'lLocations:', lLocations )
    #
    lNearFront = []
    #
    iBailOutHere = len( lLocations ) // 3
    #
    for i in iRange( len( lLocations ) ):
        #
        if dLocations[ i ]:
            #
            lNearFront.append( i )
            #
        elif i in tIgnoreLocations:
            #
            pass
            #
        elif i > iBailOutHere:
            #
            break # keep going if contiguous
            #
        #
    #
    lLocations.reverse() # now high to low
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
    lOnEnd.reverse() # lOnEnd now low to high
    #
    lNearEnd = []
    #
    iMaxNearFront   = 0
    #
    if lNearFront:
        iMaxNearFront = max( 1 + max( lNearFront ), iMax // 2 )
    #
    iMinOnEnd       = iMax
    #
    if lOnEnd:      iMinOnEnd = min( lOnEnd )
    #
    iOnEndBeginsHere = iMaxNearFront + 1
    #
    lLocations.reverse() # now low to high
    #
    for i in iRange( iMaxNearFront, iMinOnEnd ):
        #
        if dLocations[ lLocations[ i ] ]:
            #
            lNearEnd.append( lLocations[ i ] )
            #
        #
    #
    if bTrouble:
        print3( 'iMaxNearFront, iMinOnEnd, range( iMaxNearFront + 1, iMinOnEnd ):' )
        print3( iMaxNearFront,
                iMinOnEnd,
                tuple( iRange( iMaxNearFront + 1, iMinOnEnd ) ) )
        print3( 'lNearEnd:', lNearEnd )
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
            # single pair of parens
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
            # more parens than just one pair of parens
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
                      if isWordInParens( k ) and
                         isNotPunctuation( k ) and
                         dAllWordLocations[k][0] in tLocationsOfInterest ]
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
    iOfInterest = len( tLocationsOfInterest )
    #
    if lNearEnd and iOfInterest > 2:
        #
        iNearFront  = len( lNearFront )
        iNearEnd    = len( lNearEnd )
        iSpacing    = iMax // iOfInterest
        iBetween    = lNearEnd[-1] - lNearEnd[0]
        #
        if (    iNearFront == iNearEnd and
                ( iNearFront + iNearEnd ) == iOfInterest and
                iSpacing <= iBetween < 2 * iSpacing ):
            #
            # evenly spaced models, some on front and some on end
            #
            lNearEnd = []
            #
        #
    #
    if  (   len( lNearFront ) > 1   and
            lNearEnd                and
            lNearFront[ 1 ] -  lNearFront[ 0 ]  > 1 and
            lNearFront[ 1 ] >  lNearEnd[ 0   ] // 2 ):
            #lNearFront[ 1 ] >= lOnEnd[    -1 ] // 2 and
            #lOnEnd                  and
        #
        # move the latter lNearFront nodes to the beginning of lNearEnd
        #
        lNotSoNearFront = lNearFront[ 1 : ]
        #
        lNearEnd[ : 0 ] = lNotSoNearFront
        #
        del lNearFront[ - len( lNotSoNearFront ) : ]
        #
    #
    return ValueContainer(
            tNearFront  = tuple( lNearFront ),
            tOnEnd      = tuple( lOnEnd ),
            tNearEnd    = TupleEndsWithable( lNearEnd ),
            tInParens   = tInParens )


_setAlphaNums = frozenset( list( letters ) + list( digits ) )


def getStrLocationsBegAndEnd(
        sWhole, tStringsOfInterest, bUseSwapper = False, bTrouble = False ):
    #
    # swapper is slower, takes more than twice as long as using replace
    # but this one works better on this string:
    # ( "Electro Voice EV Vintage FiberGlass 8HD Horn Pair "
    #   "Speaker T10 T25 T250 A" )
    #
    #
    setUseChars = _setAlphaNums.difference( frozenset( sWhole ) )
    #
    lLensStrings = [ ( len(s), s ) for s in tStringsOfInterest ]
    #
    if len( setUseChars ) <= max( [ t[0] for t in lLensStrings ] ):
        #
        setUseChars = _setAlphaNums
        #
    #
    oRandoms = RandomFeeder(
                    setUseChars,
                    bRecycle          = True,
                    bShuffleOnRecycle = True )
    #
    dSubstitutes = OrderedDict()
    #
    sSubstitute = None
    #
    dReverseSubs= {}
    #
    dReverseSubs[ None ] = None
    #
    lLensStrings.sort()
    lLensStrings.reverse() # longest on top
    #
    lStringsOfInterest = [ t[1] for t in lLensStrings ]
    #
    if len( _oFindParens.findall( sWhole ) ) > 1:
        #
        lStringsOfInterest.extend(
            list( frozenset( oFinderPunctuation.findall( sWhole ) ) ) )
        #
    #
    if bTrouble:
        print3( 'lStringsOfInterest:', lStringsOfInterest )
    #
    for sStr in lStringsOfInterest:
        #
        while sSubstitute in dReverseSubs:
            #
            iGetLen = len( sStr )
            #
            if iGetLen == 1: iGetLen = 2
            #
            lRandoms = oRandoms.getNextSome( iGetLen )
            #
            sSubstitute = ''.join( lRandoms )
            #
            lRandoms[0:0] = [ " " ]
            #
            lRandoms.append( " " )
            #
            sPadSubstitute = ''.join( lRandoms )
            #
        #
        dSubstitutes[ sStr ] = sPadSubstitute
        #
        dReverseSubs[ sSubstitute ] = sStr
        #
    #
    del dReverseSubs[ None ]
    #
    if bTrouble:
        print3( 'dSubstitutes:' )
        pprint( dSubstitutes )
        print3( 'dReverseSubs:' )
        pprint( dReverseSubs )
        print3( 'sWhole before:', sWhole )
    if bUseSwapper:
        #
        sWhole = ReplaceManyOldWithManyNew( sWhole, dSubstitutes )
        #
    else:
        #
        for s in lStringsOfInterest:
            #
            sWhole = sWhole.replace( s, dSubstitutes[s] )
            #
        #
    #
    dAllWordLocations = getLocationsDict( sWhole )
    #
    if bTrouble:
        print3( 'sWhole after:', sWhole )
        print3( 'tStringsOfInterest before:', tStringsOfInterest )
        print3( 'dAllWordLocations:' )
        pprint( dAllWordLocations )
    #
    tStringsOfInterest = tuple(
            [ s for s in tStringsOfInterest
              if dSubstitutes[s].strip() in dAllWordLocations ] )
    #
    if bTrouble:
        print3( 'tStringsOfInterest after:', tStringsOfInterest )
    #
    if tStringsOfInterest:
        #
        for k, v in dReverseSubs.items():
            #
            if k in dAllWordLocations:
                #
                dAllWordLocations[ v ] = dAllWordLocations[ k ]
                #
                del dAllWordLocations[ k ]
                #
            #
        #
        tLocationsOfInterest = tuple(
            chain.from_iterable(
                [ dAllWordLocations[ s ] for s in tStringsOfInterest ] ) )
        #
    else:
        #
        tLocationsOfInterest = ()
        #
    #
    if bTrouble:
        print3( 'tLocationsOfInterest after:', tLocationsOfInterest )
    #
    o = _getSubStrLocationsBegAndEnd(
            dAllWordLocations, tLocationsOfInterest, bTrouble = bTrouble )
    #
    o.dAllWordLocations = dAllWordLocations
    #
    return o


def _getStrLocationsBegAndEnd( sWhole, tStrsOfInterest,
                               bUseSwapper = False, bTrouble = False ):
    #
    lStingsGotSpace = [ s for s in tStrsOfInterest if ' ' in s ]
    #
    dChanges    = {}
    dChangeBack = {}
    #
    if lStingsGotSpace:
        #
        for sOrig in lStingsGotSpace:
            #
            sNew = sOrig.replace( ' ', '_' )
            #
            sWhole = sWhole.replace( sOrig, sNew )
            #
            dChanges[ sOrig ] = sNew
            #
            dChangeBack[ sNew ] = sOrig
            #
        #
        lStrsOfInterest = [ dChanges.get( s, s ) for s in tStrsOfInterest ]
        #
    else:
        #
        lStrsOfInterest = tStrsOfInterest
        #
    #
    if False: # TimeTrial shows this takes more time
        #
        lStrsOfInterestAndMore = list( lStrsOfInterest )
        #
        lStrsOfInterestAndMore.append( '[()]' )
        #
        oFindInterests = getRegExObj( '(%s)' % '|'.join( lStrsOfInterestAndMore ) )
        #
        sWhole = oFindInterests.sub( ' \\1 ', sWhole )
        #
    else:
        #
        lStrsOfInterestAndMore = list( lStrsOfInterest )
        #
        lStrsOfInterestAndMore.extend( [ '(', ')' ] )
        #
        for s in lStrsOfInterestAndMore:
            #
            sWhole = sWhole.replace( s, ' %s ' % s )
            #
        #
    if bTrouble:
        #
        print3( 'sWhole:', sWhole )
        print3( 'lStrsOfInterest:', lStrsOfInterest )
        #
    #
    dAllWordLocations = getLocationsDict( sWhole )
    #
    lStrsOfInterest = [ s for s in lStrsOfInterest if s in dAllWordLocations ]
    #
    if lStrsOfInterest:
        #
        tLocationsOfInterest = tuple(
            chain.from_iterable(
                [ dAllWordLocations[ s ] for s in lStrsOfInterest ] ) )
        #
    else:
        #
        tLocationsOfInterest = ()
        #
    #
    o = _getSubStrLocationsBegAndEnd( dAllWordLocations, tLocationsOfInterest )
    #
    for k, v in dChangeBack.items():
        #
        if k in dAllWordLocations:
            #
            dAllWordLocations[ v ] = dAllWordLocations[ k ]
            #
            del dAllWordLocations[ k ]
            #
        #
    #
    o.dAllWordLocations = dAllWordLocations
    #
    return o




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
    def getTupleOffObj( o ):
        #
        return ( o.tNearFront,
                 o.tOnEnd,
                 o.tNearEnd,
                 o.tInParens )
    #
    lTestItems = []
    #
    sSub = 'Le5'
    sBig = 'Jbl L65 Jubal Le5-12 Mids Pair Working Nice! See Pictures'
    #
    dAllWordLocations = getLocationsDictOrig( sBig )
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
        lProblems.append( 'getLocationsDictOrig( "JBL L65" )' )
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
    dAllWordLocations = getLocationsDictOrig( sBig )
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
        lProblems.append( 'getLocationsDictOrig( "VINTAGE TANNOY GRF" )' )
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
    dAllWordLocations = getLocationsDictOrig( sBig )
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
        lProblems.append( 'getLocationsDictOrig( "VINTAGE RCA 6SN7GTB" )' )
        #
    #
    tLook4Models = ( sSub, )
    #
    def getLocationForSub( s ):
        return getSubStringLocation( s, dAllWordLocations )
    #
    tLocationsOfInterest = tuple( map( getLocationForSub, tLook4Models ) )
    #
    o = _getSubStrLocationsBegAndEnd( dAllWordLocations, tLocationsOfInterest )
    #
    # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
    #
    tGot = getTupleOffObj( o )
    #
    tExpect = ((2,), (), (), ())
    #
    lTestItems.append(
            ( sBig, tLook4Models, tExpect,
                    "VINTAGE RCA 6SN7GTB" ) )
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
    dAllWordLocations = getLocationsDictOrig( sBig )
    #
    def getLocationForSub( s ):
        return getSubStringLocation( s, dAllWordLocations )
    #
    tLook4Models = ( "6922", "6DJ8", "E88CC" )
    #
    tLocationsOfInterest = tuple( map( getLocationForSub, tLook4Models ) )
    #
    o = _getSubStrLocationsBegAndEnd(
            dAllWordLocations, tLocationsOfInterest )
    #
    # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
    #
    tGot = getTupleOffObj( o )
    #
    tExpect = ((1,), (11, 12), (), ())
    #
    lTestItems.append(
            ( sBig, tLook4Models, tExpect, "Amperex 6922 gold" ) )
    #
    if tGot != tExpect:
        #
        print3( tGot )
        lProblems.append(
                '_getSubStrLocationsBegAndEnd( "Amperex 6922 gold" )' )
        #
    #
    tLook4Models = ( "6SN7GTB", "L65", "GRF" )
    #
    tLocationsOfInterest = tuple( map( getLocationForSub, tLook4Models ) )
    #
    o = _getSubStrLocationsBegAndEnd( dAllWordLocations, tLocationsOfInterest )
    #
    # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
    #
    tGot = getTupleOffObj( o )
    #
    tExpect = ((), (), (), ())
    #
    lTestItems.append(
            ( sBig, tLook4Models, tExpect,
                    "Amperex 6922 gold (wrong models)" ) )
    #
    if tGot != tExpect:
        #
        lProblems.append(
                '_getSubStrLocationsBegAndEnd( "6SN7GTB, L65, GRF" )' )
        #
    #
    sBig = ( "Valvo Heerlen E88CC NOS Grey Shield CCa 6DJ8 6922 "
             "CV2492 CV2493 CV5358 CV5472 6N23P 6N11 ECC88 PCC88 7DJ8" )
    #
    dAllWordLocations = getLocationsDictOrig( sBig )
    #
    def getLocationForSub( s ):
        return getSubStringLocation( s, dAllWordLocations )
    #
    tLook4Models = tuple( "E88CC CCa 6DJ8 6922 CV2492 CV2493 CV5358 "
                             "CV5472 6N23P 6N11 ECC88 PCC88 7DJ8".split() )
    #
    tLocationsOfInterest = tuple(
                            map( getLocationForSub, ( tLook4Models ) ) )
    #
    # print3( 'tLocationsOfInterest:', tLocationsOfInterest )
    #
    o = _getSubStrLocationsBegAndEnd( dAllWordLocations, tLocationsOfInterest )
    #
    # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
    #
    tGot = getTupleOffObj( o )
    #
    tExpect = ( (2,), (6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17), (), () )
    #
    lTestItems.append(
            ( sBig, tLook4Models, tExpect,
                    "E88CC CCa 6DJ8 6922 etc." ) )
    #
    # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
    #
    if tGot != tExpect:
        #
        print3( "E88CC CCa 6DJ8 6922 etc.:", tGot )
        lProblems.append(
                '_getSubStrLocationsBegAndEnd( "E88CC CCa 6DJ8 6922 etc." )' )
        #
    #
    sBig = ( "2x  ECC88 / 6DJ8   TELEFUNKEN  <> tubes  - NOS  "
             "-  ( ~  7DJ8 / PCC88 )  MILITARY" )
    #
    dAllWordLocations = getLocationsDictOrig( sBig )
    #
    def getLocationForSub( s ):
        return getSubStringLocation( s, dAllWordLocations )
    #
    tLocationsOfInterest = tuple(
                            map( getLocationForSub, ( tLook4Models ) ) )
    #
    o = _getSubStrLocationsBegAndEnd(
            dAllWordLocations, tLocationsOfInterest, bTrouble = False )
    #
    # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
    #
    tGot = getTupleOffObj( o )
    #
    tExpectOne = ( ((1, 3), (), (12, 14), (12, 14)),
                   ((1, 3), (), (13, 15), (13, 15)) )
    #
    lTestItems.append(
            ( sBig, tLook4Models, tExpectOne,
                    "ECC88 / 6DJ8 (7DJ8/PCC88)" ) )
    #
    if tGot not in tExpectOne:
        #
        print3( "ECC88 / 6DJ8 (7DJ8/PCC88):", tGot )
        lProblems.append(
                '_getSubStrLocationsBegAndEnd( "ECC88 / 6DJ8 (7DJ8/PCC88)" )' )
        #
    #
    sBig = "DYNACO ST-70 ORIGINAL CAGE (with meter) VG SHAPE ( 1 EA )"
    #
    dAllWordLocations = getLocationsDictOrig( sBig )
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
    tLook4Models = ( 'ST-70', '1', )
    #
    def getLocationForSub( s ):
        return getSubStringLocation( s, dAllWordLocations )
    #
    tLocationsOfInterest = tuple(
                            map( getLocationForSub, ( tLook4Models ) ) )
    #
    o = _getSubStrLocationsBegAndEnd( dAllWordLocations, tLocationsOfInterest )
    #
    # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
    #
    tGot = getTupleOffObj( o )
    #
    tExpect = ((1,), (), (11,), (11,))
    #
    lTestItems.append(
            ( sBig, tLook4Models, tExpect,
                    "DYNACO ST-70 ORIGINAL CAGE" ) )
    #
    if tGot != tExpect:
        #
        print3( tGot )
        lProblems.append(
                '_getSubStrLocationsBegAndEnd( "DYNACO ST-70 ORIGINAL CAGE" )' )
        #
    #
    sBig = ( "AZ1 Valvo Pair! Mesh Plate Tube Valve Röhre "
             "Big Ballon Klangfilm AD1 Tested Good" )
    #
    dAllWordLocations = getLocationsDictOrig( sBig )
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
    tLook4Models = tuple( "AD1 AZ1".split() )
    #
    tLocationsOfInterest = tuple( map( getLocationForSub, tLook4Models ) )
    #
    o = _getSubStrLocationsBegAndEnd( dAllWordLocations, tLocationsOfInterest )
    #
    # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
    #
    tGot = getTupleOffObj( o )
    #
    tExpect = ((0,), (), (11,), ())
    #
    lTestItems.append(
            ( sBig, tLook4Models, tExpect, "AZ1 Valvo Pair!" ) )
    #
    if tGot != tExpect:
        #
        print3( tGot )
        lProblems.append(
                '_getSubStrLocationsBegAndEnd( "AZ1 Valvo Pair!" )' )
        #
    #
    sBig = ( "Vintage Stark 8-77 Tube Tester Hickok 6000" )
    #
    dAllWordLocations = getLocationsDictOrig( sBig )
    #
    dExpect = { 
        'Vintage': (0,),
        'Stark': (1,),
        '8-77': (2,),
        'Tube': (3,),
        'Tester': (4,),
        'Hickok': (5,),
        '6000': (6,) }
    #
    if dAllWordLocations != dExpect:
        #
        lProblems.append(
                'dAllWordLocations( "Stark 8-77 Tube Tester" )' )
        #
    #
    def getLocationForSub( s ):
        return getSubStringLocation( s, dAllWordLocations )
    #
    #
    tLook4Models = tuple( "8-77 6000".split() )
    #
    tLocationsOfInterest = tuple( map( getLocationForSub, tLook4Models ) )
    #
    o = _getSubStrLocationsBegAndEnd( dAllWordLocations, tLocationsOfInterest )
    #
    # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
    #
    tGot = getTupleOffObj( o )
    #
    tExpect = ((2,), (6,), (), ())
    #
    lTestItems.append(
            ( sBig, tLook4Models, tExpect, "Stark 8-77 Tube Tester" ) )
    #
    if tGot != tExpect:
        #
        print3( tGot )
        lProblems.append(
                '_getSubStrLocationsBegAndEnd( "Stark 8-77 Tube Tester" )' )
        #
    #
    sBig = ( "Altec A5 Customized with sound nice "
             "so more than the original (515/288/2405)" )
    #
    dAllWordLocations = getLocationsDictOrig( sBig )
    #
    dExpect = { 
        'Altec':        ( 0,),
        'A5':           ( 1,),
        'Customized':   ( 2,),
        'with':         ( 3,),
        'sound':        ( 4,),
        'nice':         ( 5,),
        'so':           ( 6,),
        'more':         ( 7,),
        'than':         ( 8,),
        'the':          ( 9,),
        'original':     (10,),
        '(':            (11,),
        '515/288/2405': (12,),
        ')':            (13,) }
    #
    if dAllWordLocations != dExpect:
        #
        lProblems.append(
                'dAllWordLocations( "Altec A5 Customized" )' )
        #
    #
    def getLocationForSub( s ):
        return getSubStringLocation( s, dAllWordLocations )
    #
    #
    tLook4Models = tuple( "A5 515 288 2405".split() )
    #
    tLocationsOfInterest = tuple( map( getLocationForSub, tLook4Models ) )
    #
    o = _getSubStrLocationsBegAndEnd( dAllWordLocations, tLocationsOfInterest )
    #
    # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
    #
    tGot = getTupleOffObj( o )
    #
    tExpectOne = ( ((1,), (), (12,), (12,)),
                   ((1,), (), (12, 14, 16), (12, 14, 16)) )
    #
    lTestItems.append(
            ( sBig, tLook4Models, tExpectOne, "Altec A5 Customized" ) )
    #
    if tGot not in tExpectOne:
        #
        print3( tGot )
        lProblems.append(
                '_getSubStrLocationsBegAndEnd( "Altec A5 Customized" )' )
        #
    #
    sBig = ( "JBL L220 Oracle Speakers 076 Cat Eye Tweeters, "
             "LE14A Woofer, LE5-9 midrange" )
    #
    dAllWordLocations = getLocationsDictOrig( sBig )
    #
    dExpect = {
        'JBL':      ( 0,),
        'Oracle':   ( 2,),
        'L220':     ( 1,),
        'Speakers': ( 3,),
        '076':      ( 4,),
        'Cat':      ( 5,),
        'Eye':      ( 6,),
        'Tweeters': ( 7,),
        'LE14A':    ( 8,),
        'Woofer':   ( 9,),
        'LE5-9':    (10,),
        'midrange': (11,) }
    #
    if dAllWordLocations != dExpect:
        #
        lProblems.append(
                'dAllWordLocations( "JBL L220 Oracle Speakers" )' )
        #
    #
    def getLocationForSub( s ):
        return getSubStringLocation( s, dAllWordLocations )
    #
    #
    tLook4Models = tuple( "L220 076 LE14A LE5-9".split() )
    #
    tLocationsOfInterest = tuple( map( getLocationForSub, tLook4Models ) )
    #
    o = _getSubStrLocationsBegAndEnd( dAllWordLocations, tLocationsOfInterest )
    #
    # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
    #
    tGot = getTupleOffObj( o )
    #
    tExpect = ((1, 4), (), (), ())
    #
    lTestItems.append(
            ( sBig, tLook4Models, tExpect, "JBL L220 Oracle Speakers" ) )
    #
    if tGot != tExpect:
        #
        print3( tGot )
        lProblems.append(
                '_getSubStrLocationsBegAndEnd( "JBL L220 Oracle Speakers" )' )
        #
    #
    oTest = getStrLocationsBegAndEnd( sBig, tLook4Models )
    #
    # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
    #
    if oTest.dAllWordLocations != dExpect:
        #
        print3( 'oTest.dAllWordLocations:' )
        pprint( oTest.dAllWordLocations )
        lProblems.append(
                'getStrLocationsBegAndEnd dAllWordLocations'
                '( "JBL L220 Oracle Speakers" )' )
        #
    #
    tGot = getTupleOffObj( oTest )
    #
    if tGot != tExpect:
        #
        print3( tGot )
        lProblems.append(
                'getStrLocationsBegAndEnd( "JBL L220 Oracle Speakers" )' )
        #
    #
    sBig = ( "BROOK 10C Tube Amplifier   "
             "Western Electric Fairchild 620 300B 2A3   Tested 10C3" )
    # should find 10C not the rest
    #
    dAllWordLocations = getLocationsDictOrig( sBig )
    #
    def getLocationForSub( s ):
        return getSubStringLocation( s, dAllWordLocations )
    #
    tLook4Models = ( "10C", "10C3", "620", "2A3", "300B" )
    #
    tLocationsOfInterest = tuple( map( getLocationForSub, tLook4Models ) )
    #
    o = _getSubStrLocationsBegAndEnd(
            dAllWordLocations, tLocationsOfInterest, bTrouble = False )
    #
    # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
    #
    tGot = getTupleOffObj( o )
    #
    tExpect = ((1,), (11,), (7, 8, 9), ())
    #
    if tGot != tExpect:
        #
        print3( '"BROOK 10C Tube Amplifier"' )
        print3( 'tGot:', tGot )
        print3( 'tExpect:', tExpect )
        lProblems.append(
                '_getSubStrLocationsBegAndEnd( "BROOK 10C Tube Amplifier" )' )
        #
    #
    # print3( 'dAllWordLocations:', dAllWordLocations )
    #
    # print3( 'tGot:', tGot )
    #
    # "15 x EL84 Telefunken Valvo Siemens Lorenz 6BQ5 old version Made in West Germany"
    # should find EL84 not 6BQ5
    #
    # "4 pcs - RCA 6922 vintage vacuum tube quad - E88CC 6DJ8 CV2492 CCa - valves"
    # should find 6922 not the rest
    #
    sBig = ( "British Made Mullard 7DJ8 PCC88 Tube Valve "
             "6DJ8 ECC88 sub -Warm Old School hifi" )

    #
    tLook4Models = ( "7DJ8", "PCC88", "6DJ8", "ECC88" )
    #
    o = getStrLocationsBegAndEnd( sBig, tLook4Models )
    #
    # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
    #
    tGot = getTupleOffObj( o )
    #
    tExpect = ( (3, 4), (), (7, 8), () )
    #
    if tGot != tExpect:
        #
        print3( '"Mullard 7DJ8 PCC88 Tube"' )
        print3( 'tGot:', tGot )
        print3( 'tExpect:', tExpect )
        lProblems.append(
                'getStrLocationsBegAndEnd( "Mullard 7DJ8 PCC88 Tube" )' )
        #
    #
    sBig = ( "Electro Voice EV Vintage FiberGlass 8HD Horn Pair "
             "Speaker T10 T25 T250 A" )
    #
    tLook4Models = ( "8HD", "T250", "T25" )
    #
    # o = _getStrLocationsBegAndEnd( sBig, tLook4Models, bTrouble = True )
    #
    o = getStrLocationsBegAndEnd( sBig, tLook4Models )
    #
    dAllWordLocations = o.dAllWordLocations
    #
    dExpect = {
        'Electro':      ( 0,),
        'Voice':        ( 1,),
        'EV':           ( 2,),
        'Vintage':      ( 3,),
        'FiberGlass':   ( 4,),
        '8HD':          ( 5,),
        'Horn':         ( 6,),
        'Pair':         ( 7,),
        'Speaker':      ( 8,),
        'T10':          ( 9,),
        'T25':          (10,),
        'T250':         (11,),
        'A':            (12,) }
    #
    if dAllWordLocations != dExpect:
        lProblems.append(
                'getStrLocationsBegAndEnd( '
                '"Electro Voice EV Vintage FiberGlass 8HD Horn" )' )
        #
    #
    sBig = ( 'Telefunken E88CC/01 w/ Mullard label <> '
             'audiophono grade 6922 CCA 6DJ8 Gold Pins' )
    #
    tLook4Models = ('6DJ8', '6922', 'E88CC', 'CCA')
    #
    # o = _getSubStrLocationsBegAndEnd(
    #         dAllWordLocations, tLook4Models, bTrouble = True )
    #
    o = getStrLocationsBegAndEnd( sBig, tLook4Models, bTrouble = False )
    #
    # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
    #
    tGot = getTupleOffObj( o )
    #
    tExpect = ( (1,), (), (9, 10, 11), () )
    #
    if tGot != tExpect:
        #
        print3( '"Telefunken E88CC/01 w/ Mullard label"' )
        print3( 'tGot:', tGot )
        print3( 'tExpect:', tExpect )
        lProblems.append(
                'getStrLocationsBegAndEnd( "Telefunken E88CC/01 w/ Mullard label" )' )
        #
    #
    sBig = ( 'Pair Electro-Voice EV The Patrician Premium System 18Wk, '
             '(2)828HF, T25A/6HD T35' )
    #
    tLook4Models = ('6HD', 'T35', '828HF', 'Patrician', 'T25A', '18Wk')
    #
    o = getStrLocationsBegAndEnd( sBig, tLook4Models, bTrouble = False )
    #
    # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
    #
    tGot = getTupleOffObj( o )
    #
    tExpect = ( (6,), (18, 19), (9, 14, 16), () )
    #
    if tGot != tExpect:
        #
        print3( '"Electro-Voice EV The Patrician Premium System"' )
        print3( 'tGot:', tGot )
        print3( 'tExpect:', tExpect )
        lProblems.append(
                'getStrLocationsBegAndEnd( '
                '"Electro-Voice EV The Patrician Premium System" )' )
        #
    #
    sBig = "2 Metal RCA 6V6 VT-107 Vacuum Tubes Tested Guaranteed!"
    #
    tLook4Models = ( 'VT-107', '6V6' )
    #
    o = getStrLocationsBegAndEnd( sBig, tLook4Models, bTrouble = False )
    #
    # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
    #
    tGot = getTupleOffObj( o )
    #
    tExpect = ( (3, 4), (), (), () )
    #
    if tGot != tExpect:
        #
        print3( '"Metal RCA 6V6 VT-107 Vacuum Tubes"' )
        print3( 'tGot:', tGot )
        print3( 'tExpect:', tExpect )
        lProblems.append(
                'getStrLocationsBegAndEnd( '
                '"Metal RCA 6V6 VT-107 Vacuum Tubes" )' )
        #
    #
    sBig = ( "2 Vintage Philips Holland GE  6DJ8 6922 E88CC Vacuum Tubes "
             "Tested Guaranteed!" )
    #
    tLook4Models = ( 'E88CC', '6DJ8', '6922' )
    #
    o = getStrLocationsBegAndEnd( sBig, tLook4Models, bTrouble = False )
    #
    # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
    #
    tGot = getTupleOffObj( o )
    #
    tExpect = ( (5, 6, 7), (), (), () )
    #
    if tGot != tExpect:
        #
        print3( '"Philips Holland GE  6DJ8 6922 E88CC Vacuum Tubes"' )
        print3( 'tGot:', tGot )
        print3( 'tExpect:', tExpect )
        lProblems.append(
                'getStrLocationsBegAndEnd( '
                '"Philips Holland GE  6DJ8 6922 E88CC Vacuum Tubes" )' )
        #
    #
    sBig = "IEC Mullard 6922 / E88CC / 6DJ8 Gold Pin Tube"
    #
    tLook4Models = ( '6922', 'E88CC', '6DJ8' )
    #
    o = getStrLocationsBegAndEnd( sBig, tLook4Models, bTrouble = False )
    #
    # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
    #
    tGot = getTupleOffObj( o )
    #
    tExpect = ( (2, 4, 6), (), (), () )
    #
    if tGot != tExpect:
        #
        print3( '"Mullard 6922 / E88CC / 6DJ8 Gold"' )
        print3( 'tGot:', tGot )
        print3( 'tExpect:', tExpect )
        lProblems.append(
                'getStrLocationsBegAndEnd( '
                '"Mullard 6922 / E88CC / 6DJ8 Gold" )' )
        #
    #
    sBig = ( "JBL L220 Walnut Excellent "
             "with 076 Cats-eye, LE5-9, LE14A Aquaplas Cone all OEM" )
    #
    tLook4Models = ( 'L220', 'LE14A', '076', 'LE5-9' )
    #
    o = getStrLocationsBegAndEnd( sBig, tLook4Models, bTrouble = False )
    #
    # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
    #
    tGot = getTupleOffObj( o )
    #
    tExpect = ( (1,), (), (5, 7, 9), () )
    #
    if tGot != tExpect:
        #
        print3( '"JBL L220 Walnut Excellent"' )
        print3( 'tGot:', tGot )
        print3( 'tExpect:', tExpect )
        lProblems.append(
                'getStrLocationsBegAndEnd( '
                '"JBL L220 Walnut Excellent" )' )
        #
    #
    #
    for t in lTestItems:
        #
        bTrouble = False and ( t[3] == "Altec A5 Customized" )
        #
        if True or bTrouble:
            #
            # print3( t[3] )
            oTest = _getStrLocationsBegAndEnd(
                        t[0], t[1], bUseSwapper = True, bTrouble = bTrouble )
            #
            # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
            #
            tGot = getTupleOffObj( oTest )
            #
            if not ( tGot == t[2] or tGot in t[2] ):
                #
                print3()
                print3( 'tGot   :', tGot )
                print3( 'tExpect:', t[2] )
                #
                lProblems.append(
                        '_getStrLocationsBegAndEnd( "%s", '
                        'bUseSwapper = True )' % t[3] )
                #
            #
            oTest = _getStrLocationsBegAndEnd(
                        t[0], t[1], bUseSwapper = False, bTrouble = bTrouble )
            #
            # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
            #
            tGot = getTupleOffObj( oTest )
            #
            if not ( tGot == t[2] or tGot in t[2] ):
                #
                print3()
                print3( 'tGot   :', tGot )
                print3( 'tExpect:', t[2] )
                #
                lProblems.append(
                        '_getStrLocationsBegAndEnd( "%s", '
                        'bUseSwapper = False )' % t[3] )
                #
            #
            oTest = getStrLocationsBegAndEnd( t[0], t[1] )
            #
            # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
            #
            tGot = getTupleOffObj( oTest )
            #
            if not ( tGot == t[2] or tGot in t[2] ):
                #
                print3()
                print3( 'tGot   :', tGot )
                print3( 'tExpect:', t[2] )
                #
                lProblems.append(
                        'getStrLocationsBegAndEnd( "%s" )' % t[3] )
                #
            #
        #
        #break
    #
    # "4 pcs - RCA 6922 vintage vacuum tube quad - E88CC 6DJ8 CV2492 CCa - valves"
    #
    # should find 6922 and return others cuz bunched up near end
    #
    #
    # "HEATHKIT TUBE AMPLIFIER EA-3   \/ UA-2 \/ UA-1"
    #
    # find first only?
    #
    def testSwapper():
        #
        for t in lTestItems:
            #
            oTest = _getStrLocationsBegAndEnd( t[0], t[1], bUseSwapper = True )
            #
    #
    def testReplace():
        #
        for t in lTestItems:
            #
            oTest = _getStrLocationsBegAndEnd( t[0], t[1], bUseSwapper = False )
            #
    #
    def testOriginalMistake():
        #
        for t in lTestItems:
            #
            dAllWordLocations = getLocationsDict( t[0] )
            #
            def getLocationForSub( s ):
                return getSubStringLocation( s, dAllWordLocations )
            #
            tLocationsOfInterest = tuple( map( getLocationForSub, t[1] ) )
            #
            o = _getSubStrLocationsBegAndEnd( dAllWordLocations, tLocationsOfInterest )
        #
    #
    def testOriginal():
        #
        for t in lTestItems:
            #
            oTest = _getStrLocationsBegAndEnd( t[0], t[1] )
            #
    #
    def testNewImproved():
        #
        for t in lTestItems:
            #
            oTest = getStrLocationsBegAndEnd( t[0], t[1] )
            #
    #
    #print3( '\ndoing _getStrLocationsBegAndEnd() w swapper ...\n' )
    #
    #TimeTrial( testSwapper )
    #
    #
    #print3( '\ndoing _getStrLocationsBegAndEnd() w replace ...\n' )
    #
    #TimeTrial( testReplace )
    #
    '''
    #
    new, imporoved getStrLocationsBegAndEnd is
    somewhat faster than _getStrLocationsBegAndEnd
    #
    print3( '\ndoing _getSubStrLocationsBegAndEnd() ...\n' )
    #
    TimeTrial( testOriginal )
    #
    print3( '\ndoing getStrLocationsBegAndEnd() ...\n' )
    #
    TimeTrial( testNewImproved )
    '''
    #
    #
    sayTestResult( lProblems )
