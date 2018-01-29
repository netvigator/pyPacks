#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# string functions Find
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
# Copyright 2004-2018 Rick Graves
#
from collections import OrderedDict

def getRegExSpecialsEscapedNoShortcut( sString ):
    #
    from Iter.AllVers import getEnumerator
    #
    lString = list( sString )
    #
    for cSpecial in '*?\[]{}$^+|()':
        #
        for i, c in getEnumerator( lString ):
            #
            if c == cSpecial:
                #
                lString[ i ] = '\\' + c
        #
    #
    return ''.join( lString )


def getRegExSpecialsEscapedWithShortcut( sString ):
    #
    from Iter.AllVers import getEnumerator
    #
    lGotChars = [ c for c in '*?\[]{}$^+|()' if c in sString ]
    #
    if lGotChars:
        #
        lString = list( sString )
        #
        for cSpecial in lGotChars:
            #
            for i, c in getEnumerator( lString ):
                #
                if c == cSpecial:
                    #
                    lString[ i ] = '\\' + c
            #
        return ''.join( lString )
        #
    else:
        #
        return sString
        #


getRegExSpecialsEscaped = getRegExSpecialsEscapedWithShortcut




def getFinder( sPattern,
        bCaseSensitive = False, bDotAll = False, bMultiLine = False ):
    #
    '''
    pass RegEx pattern, returns RegEx finder for the pattern
    a re finder can be fast when you are searching for several things,
     as the finder can make one pass and snag them all.
    If you are only looking for one thing, string methods are faster
    If you are only looking for one thing whether upper or lower case,
     string methods are faster if coded right
    '''
    from re import compile as REcompile, IGNORECASE, DOTALL, MULTILINE
    #
    iFlags = 0
    #
    if not bCaseSensitive and sPattern.upper() != sPattern.lower():
        #
        iFlags      = IGNORECASE
        #
    if bDotAll:
        #
        # Make the '.' special character match any character at all,
        # including a newline; without this flag,#
        # '.' will match anything except a newline.
        #
        iFlags      = iFlags | DOTALL
        #
    if bMultiLine:
        #
        iFlags      = iFlags | MULTILINE
        #
    #
    oFinder     = REcompile( sPattern, iFlags )
    #
    return oFinder



def getFinderFindAll( sPattern, bCaseSensitive = False, bDotAll = False ):
    #
    '''
    this function returns a ready to call finder
    just pass in the RegEx pattern
    the finder returns a list of finds
    note that said list can contian empty strings, sometimes lots!
    maybe helpful in Collect.Get:
    getListNoFalsies() returns only items that evaluate as True
    (this would omit all empty strings)
    so you can wrap the finder call with getListNoFalsies()
    '''
    oFinder = getFinder( sPattern,
                         bCaseSensitive = bCaseSensitive, bDotAll = bDotAll )
    #
    return oFinder.findall


def getSeqWordBounds( seq ):
    #
    return r'\b%s\b' % r'\b|\b'.join( seq )



dSub1st = OrderedDict( (
    ( '&',      ' (&|and) ' ),  # ampersand also matches and
    ( ' and ',  ' (&|and) ' ),  # and also matches ampersand
    ( '/',      '(/ )+'     ),  # slash matches ONE  or more spaces or slashes
    ( ' +- +',  '-'         ),  # remove spaces about hypens
    ( '"',      '"*'        ),  # double quotes optional
    ( "'" ,     "'*"        ))) # single quotes optional

# normalize white space between 1st & 2nd

dSub2nd = OrderedDict( (
    ( ' ',      ' *'        ),  # space    matches ZERO or more spaces
    ( '-',      '[- ]*'     ),  # hyphen   matches ZERO or more hypens or spaces
    ( ',',      '[, ]*'     ),  # comma    matches ZERO or more commas or spaces
    ( '.',      '[. ]*'     ))) # dot      matches ZERO or more dots or spaces


tSubLast = (
    ( ' *Corporation',
                ' *(Corporation|Company|Corp|Co)' ),
    ( ' *Company',
                ' *(Corporation|Company|Corp|Co)' ),
    ( ' *Corp',
                ' *(Corporation|Company|Corp|Co)' ),
    ( ' *Co',
                ' *(Corporation|Company|Corp|Co)' ) )

def getRegEx4Chars( s,
        dSub1st = dSub1st, dSub2nd = dSub2nd, tSubLast = tSubLast ):
    #
    from Collect.Query  import get1stThatMeets
    from String.Replace import ReplaceManyOldWithManyNew
    #
    s = s.strip()
    #
    while s[-1] == '.':
        #
        s= s[:-1].strip()
        #
    #
    #print3( 'a', s )
    #
    l = s.split( '|' )
    #
    if len( l ) > 1: # handle OR via |
        #
        l = [ sPart.strip() for sPart in l ]
        #
        s = _getPartsParenedAndBarred( frozenset( l ) )
        #
    #
    s = ReplaceManyOldWithManyNew( s, dSub1st )
    #
    #print3( 'b', s )
    #
    l = s.split() # normalize white space
    #
    s = ' '.join( l )
    #
    s = ReplaceManyOldWithManyNew( s, dSub2nd )
    #
    #print3( 'c', s )
    #
    sUpper = s.upper()
    #
    def gotLastSomewhere( t ): return t[0].upper() in sUpper
    #
    if get1stThatMeets( tSubLast, gotLastSomewhere ):
        #
        l = s.split( '|' )
        #
        lNew = []
        #
        for s in l:
            #
            for t in tSubLast:
                #
                # print3( 's, t[0]:', s, t[0] )
                #
                if s.upper().endswith( t[0].upper() ):
                    #
                    s = s[ : - len( t[0] ) ] + t[1]
                    #
                elif s.upper().endswith( t[0].upper() + ')' ):
                    #
                    s = s[ : - ( 1 + len( t[0] ) ) ] + t[1] + ')'
                    #
                #
            #
            lNew.append( s )
            #
        #
        s = '|'.join( lNew )
    #
    return s



def _getPartsParenedAndBarred( u ):
    #
    l = list( u )
    #
    l.insert( 0, '' )
    l.append(    '' )
    #
    return ')|('.join( l )[ 2 : -2 ]


def _getEscapedThenSplit( s, cSplitOn ):
    #
    s = getRegExSpecialsEscaped( s )
    #
    l = s.split( cSplitOn )
    #
    return l


def gotRawRex( s ):
    #
    return (
        ( s.startswith( 'r"' ) and s.endswith( '"' ) ) or
        ( s.startswith( "r'" ) and s.endswith( "'" ) ) )


def getRegExpFinder(
        sOrig           = '',
        dSub1st         = dSub1st,
        dSub2nd         = dSub2nd,
        tSubLast        = tSubLast,
        fDoThisFirst    = None,
        cSeparator      = '\r',
        bPermutate      = False ):
    #
    from Iter.AllVers   import permutations
    from String.Get     import getRawGotStr # not sure we need this
    #
    if gotRawRex( sOrig ):
        #
        sInside = sOrig[ 2 : -1 ]
        #
        return getFinderFindAll( getRawGotStr( sOrig ) )
        #
    #
    sRegEx = ''
    #
    if fDoThisFirst is not None:
        #
        sOrig       = fDoThisFirst( sOrig )
        #
    #
    lOrig = _getEscapedThenSplit( sOrig, cSeparator )
    #
    if bPermutate:
        #
        lNewParts = []
        #
        for s in lOrig:
            #
            lSubParts = s.split()
            #
            for l in permutations( lSubParts ):
                #
                lNewParts.append( r'\b.*\b'.join( l ) )
                #
            #
        #
        lRegEx = frozenset( lNewParts )
        #
    else:
        #
        lRegEx = [  getRegEx4Chars( s,
                        dSub1st=dSub1st, dSub2nd=dSub2nd, tSubLast=tSubLast )
                    for s in lOrig ]
    #
    if len( lRegEx ) == 1:
        #
        if lRegEx[0][0] != '(':
            #
            sRegEx  = '(%s)' % lRegEx[0]
            #
        #
    else:
        #
        sRegEx = _getPartsParenedAndBarred( frozenset( lRegEx ) )
        #
    #
    # print3( sRegEx )
    #
    return getFinderFindAll( sRegEx )

        





def getRegExTips():
    #
    '''
from Mastering Regular Expressions by Jeffrey E.F. Friedl

use non-capturing parens (?:  )
do not add superfluous parens
do not use usperfluous character classes
use leading anchors
expose literal text
expose anchors
 expose ^ and \G at start
 expose $ at end
Lazy vs Greedy: be specific
split into multiple regexes when there is no common text
Mimic initial character discrimination
use atomic grouping (?>   ) (not supported by Python 2.7 or 3.2)
use possessive quantifiers (not supported by Python 2.7 or 3.2)
    '''
    #
    pass



def getTextInQuotes( sText ):
    #
    sQuoted             = ''
    #
    lSingleParts    = sText.split( "'" )
    lDoubleParts    = sText.split( '"' )
    #
    if len( lSingleParts ) >= 3 and len( lDoubleParts ) >= 3:
        #
        if      len( lSingleParts[0] ) < len( lDoubleParts[0] ):
            #
            sQuoted = lSingleParts[1]
            #
        else:
            #
            sQuoted = lDoubleParts[1]
            #
        #
    elif len( lSingleParts ) >= 3:
        #
        sQuoted     = lSingleParts[1]
        #
    elif len( lDoubleParts ) >= 3:
        #
        sQuoted     = lDoubleParts[1]
        #
    #
    return sQuoted


def _doTimeTrial():
    #
    from Utils.TimeTrial import TimeTrial
    from six             import print_ as print3
    #
    tTestStrings = (
        "ACRO",
        "Addison",
        "Allied",
        "Altec-Lansing",
        "Amperex",
        "Ampex",
        "Astronic",
        "Audio",
        "Audio Concepts",
        "Audio Engineering",
        "Audio Research",
        "Audiocraft",
        "B&K",
        "Bell",
        "Audio Note",
        "Briggs, G.A.",
        "Brook",
        "Radio Craftsmen",
        "Crosby",
        "Crowhurst, Norman H",
        "Dynaco",
        "EICO",
        "Fada",
        "Fairchild",
        "Fisher",
        "GE",
        "Grommes",
        "Harman-Kardon",
        "Western Electric",
        "Hewlett-Packard",
        "Hickok",
        "High Fidelity",
        "JBL",
        "Jensen",
        "Karg",
        "Klipsch",
        "Knight",
        "Lafayette",
        "McIntosh",
        "Newark",
        "PACO",
        "Peerless",
        "Pilot",
        "Kepco",
        "RCA",
        "Sherwood",
        "Stancor",
        "Stephens",
        "Stromberg-Carlson",
        "Sylvania Electric",
        "Tandberg",
        "Tektronix",
        "Tung-Sol",
        "UTC",
        "University",
        "Thordarson",
        "Radio Engineering Laboratories",
        "Triad",
        "Hallicrafters",
        "Chigaco Standard Transformer Corp.",
        "Langevin",
        "Tech-Master",
        "Regency",
        "Sargent-Rayment",
        "Interelectronics",
        "KenRad",
        "National Union",
        "Arcturus",
        "Cunningham",
        "Luxman",
        "PYE",
        "Marantz",
        "Bartolucci",
        "GEC",
        "Leak",
        "Wharfedale",
        "Thorens",
        "Telefunken",
        "Tannoy",
        "Mullard",
        "Philips",
        "Quad",
        "Scott, H.H.",
        "CBS",
        "Raytheon",
        "Philco",
        "Westinghouse",
        "Bendix",
        "United Electronics",
        "Hytron",
        "Dumont",
        "Chatham",
        "Union Tube Co",
        "Silvertone",
        "Simpson",
        "IPC",
        "Spartan",
        "Lansing",
        "SpeakerLab",
        "Mastering Lab",
        "MFA",
        "Janszen",
        "KLH",
        "Emerson",
        "Fake",
        "Koss",
        "Sentinel",
        "Garod",
        "Fluke",
        "Acoustat",
        "Kadette",
        "Coronado",
        "Globe",
        "Packard-Bell",
        "Visseaux",
        "Motorola",
        "Hyvac",
        "GE 5 Star",
        "Zenith",
        "Brociner",
        "DeWald",
        "Arvin",
        "Meyer",
        "Cetron",
        "Empire",
        "Acoustic Research",
        "National",
        "DuKane",
        "EMI",
        "Chartwell",
        "CIFTE",
        "Decca",
        "Funke",
        "Kelley",
        "Spendor",
        "Radford",
        "Neuberger",
        "Nems Clarke",
        "Toshiba",
        "AER",
        "AVO",
        "Barzillay",
        "Crosley",
        "Goodmans",
        "Marconi",
        "Vitavox",
        "Wizard",
        "Valvo",
        "Tungsram",
        "Tango",
        "Tamura",
        "Siemens",
        "Rogers",
        "Mazda",
        "Mullard IEC/10M",
        "Motiograph",
        "MO Valve",
        "Matsushita",
        "Osram",
        "Partridge",
        "Sharp",
        "McGohan",
        "Westrex",
        "ERPI",
        "Unholtz-Dickie Corp.",
        "Lambda",
        "Bogen",
        "Audiomaster",
        "Klangfilm",
        "Brimar",
        "Lowther",
        "Williamson",
        "SME",
        "Electro-Voice",
        "Ballantyne",
        "Heathkit",
        "Sprague",
        "{blank}",
        "Heintz & Kaufman" )
    #
    def doNamesWithShortcut():
        #
        for sName in tTestStrings:
            #
            getRegExSpecialsEscapedWithShortcut( sName )

    def doNamesNoShortcut():
        #
        for sName in tTestStrings:
            #
            getRegExSpecialsEscapedNoShortcut( sName )

    #
    print3( '\ndoing doNamesWithShortcut() ...\n' )
    #
    TimeTrial( doNamesWithShortcut )
    #
    # microseconds per call (with 100 calls per repetition)
    # 350.29 361.01 361.93 365.09 365.64 368.20 368.34 369.03 371.67 546.59
    #
    print3( '\ndoing doNamesNoShortcut() ...\n' )
    #
    TimeTrial( doNamesNoShortcut )
    #
    # milliseconds per call (with 50 calls per repetition)
    # 1.97  1.98  2.00  2.00  2.03  2.04  2.06  2.06  2.09  2.21



if __name__ == "__main__":
    #
    from string         import digits
    from string         import ascii_letters as letters
    #
    from six            import print_ as print3
    #
    from Iter.AllVers   import iMap, iRange
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    sTest = ( letters + digits ) * 5
    #
    oFindABC_ignore = getFinder( 'abc', bCaseSensitive = False )
    oFindABC_CaseSe = getFinder( 'abc', bCaseSensitive = True, bDotAll = True )
    #
    if      oFindABC_ignore.findall( sTest ) != \
                ['abc', 'ABC', 'abc', 'ABC', 'abc', 'ABC', 'abc', 'ABC', 'abc', 'ABC'] or \
            oFindABC_CaseSe.findall( sTest ) != \
                ['abc', 'abc', 'abc', 'abc', 'abc']:
        #
        lProblems.append( 'getFinder()' )
        #
    if getTextInQuotes( ' " how now brown cow\' " abc ' ) != " how now brown cow' ":
        #
        lProblems.append( 'getTextInQuotes()' )
        #
    #
    sFindThis = '<script.+?</script>|<style.+?</style>'
    oFindThis = getFinder( sFindThis, bCaseSensitive = False )
    #
    sTest = 'abc<script id=10>def</script>hij<style id = 99>klm</style>nop'
    #
    if oFindThis.findall( sTest ) != \
        ['<script id=10>def</script>', '<style id = 99>klm</style>']:
        #
        lProblems.append( 'getFinder() compound regex expression' )
        #
    #
    oFind = getFinderFindAll( 'mnop' )
    #
    if oFind( letters ) != [ 'mnop', 'MNOP' ]:
        #
        lProblems.append( 'getFinderFindAll() not case sensitive' )
        #
    #
    oFind = getFinderFindAll( 'mnop', bCaseSensitive = True )
    #
    if oFind( letters ) != [ 'mnop' ]:
        #
        lProblems.append( 'getFinderFindAll() case sensitive' )
        #
    #
    tSeq = tuple( '123' )
    #
    sSeq = getSeqWordBounds( tSeq )
    #
    if sSeq != r'\b1\b|\b2\b|\b3\b':
        #
        lProblems.append( 'getSeqWordBounds()' )
        #
    #
    #
    sOrig = "{blank}"
    sWant = "\\{blank\\}"
    #
    sGot = getRegExSpecialsEscapedNoShortcut( sOrig )
    #
    if sGot != sWant:
        #
        print3( sGot )
        #
        lProblems.append( 'getRegExSpecialsEscapedNoShortcut("{blank}")' )
        #
    #
    sGot = getRegExSpecialsEscapedWithShortcut( sOrig )
    #
    if sGot != sWant:
        #
        print3( sGot )
        #
        lProblems.append( 'getRegExSpecialsEscapedNoShortcut("{blank}")' )
        #
    #
    sOrig = sWant = "Peerless"
    #
    sGot = getRegExSpecialsEscapedNoShortcut( sOrig )
    #
    if sGot != sWant:
        #
        print3( sGot )
        #
        lProblems.append( 'getRegExSpecialsEscapedNoShortcut("Peerless")' )
        #
    #
    sGot = getRegExSpecialsEscapedWithShortcut( sOrig )
    #
    if sGot != sWant:
        #
        print3( sGot )
        #
        lProblems.append( 'getRegExSpecialsEscapedNoShortcut("Peerless")' )
        #
    #
    sGot = getRegEx4Chars( 'Harman-Kardon' )
    #
    if sGot != 'Harman[- ]*Kardon':
        #
        print3( sGot )
        #
        lProblems.append(  'getRegEx4Chars(Harman-Kardon)' )
        #
    #
    sGot = getRegEx4Chars( 'Western Electric' )
    #
    if sGot != 'Western *Electric':
        #
        print3( sGot )
        #
        lProblems.append(  'getRegEx4Chars(Western Electric)' )
        #
    #
    sGot = getRegEx4Chars( 'Chigaco Standard Transformer Corp.' )
    #
    if sGot != (
            'Chigaco *Standard *Transformer *(Corporation|Company|Corp|Co)' ):
        #
        print3( sGot )
        #
        lProblems.append(
            'getRegEx4Chars(Chigaco Standard Transformer Corp)' )
        #
    #
    sGot = getRegEx4Chars(
            'Chigaco Standard|Chigaco Standard Transformer Corp.' )
    #
    if sGot not in (
            '(Chigaco *Standard)|'
            '(Chigaco *Standard *Transformer *(Corporation|Company|Corp|Co))',
            '(Chigaco *Standard *Transformer *(Corporation|Company|Corp|Co))|'
            '(Chigaco *Standard)'):
        #
        print3( sGot )
        #
        lProblems.append(  'getRegEx4Chars(Chigaco Standard Transformer Corp)' )
        #
    #
    sGot = getRegEx4Chars( 'Unholtz-Dickie Corp.' )
    #
    if sGot != 'Unholtz[- ]*Dickie *(Corporation|Company|Corp|Co)':
        #
        print3( sGot )
        #
        lProblems.append(  'getRegEx4Chars(Unholtz-Dickie Corp.)' )
        #
    #
    sGot = getRegEx4Chars( 'B&K' )
    #
    if sGot != 'B *(&|and) *K':
        #
        print3( sGot )
        #
        lProblems.append(  'getRegEx4Chars(B&K)' )
        #
    #
    sGot = getRegEx4Chars( 'Heintz&Kaufman' )
    #
    if sGot != 'Heintz *(&|and) *Kaufman':
        #
        print3( sGot )
        #
        lProblems.append(  'getRegEx4Chars(Heintz&Kaufman)' )
        #
    #
    sGot = getRegEx4Chars( 'Heintz and Kaufman' )
    #
    if sGot != 'Heintz *(&|and) *Kaufman':
        #
        print3( sGot )
        #
        lProblems.append(  'getRegEx4Chars(Heintz and Kaufman)' )
        #
    #
    sGot = getRegEx4Chars( 'Briggs, G.A.' )
    #
    if sGot != 'Briggs[, ]* *G[. ]*A':
        #
        print3( sGot )
        #
        lProblems.append(  'getRegEx4Chars(Briggs, G.A.)' )
        #
    #
    sOrig   = '50-W-2'
    #
    sGot    = getRegEx4Chars( sOrig )
    #
    if sGot != '50[- ]*W[- ]*2':
        #
        print3( sGot )
        #
        lProblems.append( 'getRegEx4Chars(%s)' % sOrig )
        #
    #
    sOrig   = '15" gold'
    #
    sGot    = getRegEx4Chars( sOrig )
    #
    if sGot != '15"* *gold':
        #
        print3( sGot )
        #
        lProblems.append( 'getRegEx4Chars(%s)' % sOrig )
        #
    #
    sOrig   = "TR-10 'Tri-ette'"
    #
    sGot    = getRegEx4Chars( sOrig )
    #
    if sGot != "TR[- ]*10 *'*Tri[- ]*ette'*":
        #
        print3( sGot )
        #
        lProblems.append( 'getRegEx4Chars(%s)' % sOrig )
        #
    #
    sOrig   = 'TV-2/U'
    #
    sGot    = getRegEx4Chars( sOrig )
    #
    if sGot != 'TV[- ]*2(/ *)+U':
        #
        print3( sGot )
        #
        lProblems.append( 'getRegEx4Chars(%s)' % sOrig )
        #
    #
    sOrig   = '50-X-C3'
    #
    sGot    = getRegEx4Chars( sOrig )
    #
    if sGot != '50[- ]*X[- ]*C3':
        #
        print3( sGot )
        #
        lProblems.append( 'getRegEx4Chars(%s)' % sOrig )
        #
    #
    #
    sOrig   = 'Heintz&Kaufman'
    #
    oFinder = getRegExpFinder( sOrig )
    #
    sTest   = '6DJ8 vacuum tube HEINTZ AND KAUFMAN "Made in England"'
    #
    lGot    = oFinder( sTest )
    #
    if not lGot:
        #
        print3( lGot )
        #
        lProblems.append(
            'getRegExpFinder(%s) testing "%s"' % ( sOrig, sTest ) )
        #
    #
    sTest   = 'abc Black and Decker efg'
    #
    lGot    = oFinder( sTest )
    #
    if lGot:
        #
        print3( lGot )
        #
        lProblems.append(
            'getRegExpFinder(%s) testing "%s"' % ( sOrig, sTest ) )
        #
    #
    sTest   = 'abc Black&Decker efg'
    #
    lGot    = oFinder( sTest )
    #
    if lGot:
        #
        print3( lGot )
        #
        lProblems.append(
            'getRegExpFinder(%s) testing "%s"' % ( sOrig, sTest ) )
        #
    #
    sTest   = 'Black&Decker'
    #
    sOrig = 'How now brown cow'
    #
    oFinder = getRegExpFinder( sOrig, bPermutate = True )
    #
    sTest   = 'Cow brown how now'
    #
    lGot    = oFinder( sTest )
    #
    if not lGot:
        #
        print3( lGot )
        #
        lProblems.append(
            'getRegExpFinder(%s) testing "%s"' % ( sOrig, sTest ) )
        #
    #
    #
    sayTestResult( lProblems )