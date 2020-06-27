#!/home/rick/bin/pythonTest
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
#   http://www.gnu.org/licenses/
#
# Copyright 2004-2020 Rick Graves
#
from collections            import OrderedDict
from re                     import compile as REcompile
from re                     import IGNORECASE, DOTALL, MULTILINE
from string                 import punctuation

from six                    import print_ as print3

try:
    from ..Collect.Get      import getRidOfDupesKeepOrder
    from ..Collect.Query    import get1stThatMeets
    from ..Iter.AllVers     import iRange, getEnumerator, permutations
    from ..Iter.Get         import iRevRange
    from .Dumpster          import getAlphaNumCleanNoSpaces, getAlphaNumDashNoSpaces
    from ..String           import setNonAlphaNums
    from ..Utils.TimeTrial  import TimeTrial
except ( ValueError, ImportError ):
    from Collect.Get        import getRidOfDupesKeepOrder
    from Collect.Query      import get1stThatMeets
    from Iter.AllVers       import iRange, getEnumerator, permutations
    from Iter.Get           import iRevRange
    from String.Dumpster    import getAlphaNumCleanNoSpaces, getAlphaNumDashNoSpaces
    from String             import setNonAlphaNums
    from Utils.TimeTrial    import TimeTrial



def _getSpecials( bEscBegEndOfStr ):
    #
    if bEscBegEndOfStr:
        #
        sSpecials = r'\*?[]{}$^+|()'
        #
    else:
        #
        sSpecials = r'\*?[]{}+|()'
        #
    #
    return sSpecials


def getRegExSpecialsEscapedNoShortcut( sString, bEscBegEndOfStr = True ):
    #
    lString = list( sString )
    #
    sSpecials = _getSpecials( bEscBegEndOfStr )
    #
    for cSpecial in sSpecials:
        #
        for i, c in getEnumerator( lString ):
            #
            if c == cSpecial:
                #
                lString[ i ] = '\\' + c
        #
    #
    return ''.join( lString )


def getRegExSpecialsEscapedWithShortcut( sString, bEscBegEndOfStr = True ):
    #
    #
    sSpecials = _getSpecials( bEscBegEndOfStr )
    #
    lGotChars = [ c for c in sSpecials if c in sString ]
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




def getRegExObj( sPattern,
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
    oRegExObj       = REcompile( sPattern, iFlags )
    #
    return oRegExObj



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
    oFinder = getRegExObj( sPattern,
                         bCaseSensitive = bCaseSensitive, bDotAll = bDotAll )
    #
    return oFinder.findall


def getSeqWordBounds( seq ):
    #
    return r'\b%s\b' % r'\b|\b'.join( seq )



dSub1st = OrderedDict( (
    ( '&',      ' (&|and) ' ),  # ampersand also matches and
    ( ' and ',  ' (&|and) ' ),  # and also matches ampersand
    ( ' AND ',  ' (&|and) ' ),  # and also matches ampersand
    ( '/',      '(/ )+'     ),  # slash matches ONE  or more spaces or slashes
    ( ' +- +',  '-'         ),  # remove spaces about hypens
    ( '"',      '"*'        ),  # double quotes optional
    ( "'" ,     "'*"        ))) # single quotes optional

# normalize white space between 1st & 2nd

dSub2nd = OrderedDict( (
    ( ' ',      ' *'        ),  # space    matches ZERO or more spaces
    ( '-',      '[-/ ]*'    ),  # hyphen   matches ZERO or more hypens, slashes or spaces
    ( ',',      '[, ]*'     ),  # comma    matches ZERO or more commas or spaces
    ( '.',      '[. ]*'     ))) # dot      matches ZERO or more dots or spaces

oFindSubs = getRegExObj( '(?: |\[-/ \]|\[, \]|\[. \])\*' )


tSubLast = (
    ( ' *corporation',
                ' *(Corporation|Company|Corp|Co)' ),
    ( ' *company',
                ' *(Corporation|Company|Corp|Co)' ),
    ( ' *corp',
                ' *(Corporation|Company|Corp|Co)' ),
    ( ' *co',
                ' *(Corporation|Company|Corp|Co)' ) )


def _getPartsParenedAndBarred( u ):
    #
    l = list( u )
    #
    l.insert( 0, '' )
    l.append(    '' )
    #
    return ')|('.join( l )[ 2 : -2 ]



def _getPartsBarred( u ):
    #
    l = list( u )
    #
    return '|'.join( l )


def _getBoundCodesIfShort( s, iMinLen ):
    #
    '''get the string within word boundary codes'''
    #
    if (    len( getAlphaNumCleanNoSpaces( s ) ) <= iMinLen and 
            not ( s.startswith( r'\b' ) or s.endswith( r'\b' ) ) ):
        return r'\b%s\b' % s
    else:
        return s


def getRegEx4Chars( s,
            dSub1st         = dSub1st,
            dSub2nd         = dSub2nd,
            tSubLast        = tSubLast,
            iWordBoundChrs  = 0 ):
    #
    try: # moving this to the top breaks this package!
        from .Replace       import ReplaceManyOldWithManyNew
    except ( ValueError, ImportError ): # maybe circular import issue
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
        s = _getPartsBarred(
                getRidOfDupesKeepOrder(
                    [ sPart.strip() for sPart in l ] ) )
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
    if iWordBoundChrs: # > 0
        #
        l = s.split( '|' )
        #
        l = [ _getBoundCodesIfShort( s, iWordBoundChrs ) for s in l ]
        #
        s = '|'.join( l )
        #
    #
    return s


def _getSplit( s, oSplitOn ):
    #
    if oSplitOn is None:
        #
        l = [ oSplitOn ]
        #        
    elif isinstance( oSplitOn, type('str') ):
        #
        l = s.split( oSplitOn )
        #
    else:
        #
        l = oSplitOn.split( s )
        #
    #
    return [ s for s in l if s ] # remove any empties


oFinderCRorLF = getRegExObj( '\r|\n' ) # finds carriage return or line feed


# getting \\r from postgresql when there is a \r in the character column
#
oFinderCRorLFnMore = getRegExObj(
                        '|'.join(
                            ( r'\\\\r',
                              r'\\\\n',
                              r'\\' '\r',
                              r'\\' '\n',
                              r'\\r',
                              r'\\n',
                              r'\r',
                              r'\n',
                              '\r', 
                              '\n' ) ) )


oFinderPunctuation = getRegExObj( '[%s]' % punctuation )


def _getEscapedThenSplit( s, oSplitOn, bEscBegEndOfStr = True ):
    #
    sNew = getRegExSpecialsEscaped( s, bEscBegEndOfStr = bEscBegEndOfStr )
    #
    return _getSplit( sNew, oSplitOn )



def gotRawRex( s ):
    #
    return (
        ( s.startswith( 'r"' ) and s.endswith( '"' ) ) or
        ( s.startswith( "r'" ) and s.endswith( "'" ) ) )




def _gotAlphaNumPutSeparator( sChars ):
    #
    #
    lNew   = []
    #
    wasAlpha = wasDigit = False
    #
    for i in iRevRange( len( sChars ) ):
        #
        sThisChar = sChars[ i ]
        #
        isAlpha = sThisChar.isalpha()
        isDigit = sThisChar.isdigit()
        #
        if ( isAlpha and wasDigit ) or ( isDigit and wasAlpha ):
            #
            lNew.append( ' ' )
            #
        #
        lNew.append( sThisChar )
        #
        wasAlpha = isAlpha
        wasDigit = isDigit
        #
    #
    lNew.reverse()
    #
    sNew = ''.join( lNew )
    #
    return sNew.split()


def _endsWithWordBoundary( s ): return s.endswith( r'\b' )


def getRegExpress(
        sLook4          = '',
        dSub1st         = dSub1st,
        dSub2nd         = dSub2nd,
        tSubLast        = tSubLast,
        fDoThisFirst    = None,
        oSeparator      = oFinderCRorLFnMore,
        bPermutate      = False,
        bAddDash        = False,
        bSubModelsOK    = False,
        iWordBoundChrs  = 0,
        bCaseSensitive  = False,   # will the search RegEx be case sensitive?
        bEscBegEndOfStr = True,    # escape RegEx beg/end of string chars
        bPluralize      = False ): # will also find plural version of word
    #
    '''
    ### DO NOT COVERT \r's to |'s before passing sLook4 to this !!! ###
    '''
    try: # moving this to the top breaks this package!
        from .Get        import getRawGotStr
        from .Test       import hasAnyAlpha, hasAnyDigits, hasPunctOrSpace
    except ( ValueError, ImportError ): # maybe circular import issue
        from String.Get  import getRawGotStr
        from String.Test import hasAnyAlpha, hasAnyDigits, hasPunctOrSpace
    #
    sLook4Orig = sLook4
    #
    if gotRawRex( sLook4 ):
        #
        sInside = sLook4[ 2 : -1 ]
        #
        return getRawGotStr( sLook4 ) # not sure we need getRawGotStr()
        #
    #
    lOrig = _getSplit( sLook4, oSeparator )
    #
    lLengths = [ len( getAlphaNumCleanNoSpaces( s ) )
                 for s
                 in lOrig ]
    #
    #if sLook4Orig == r'Model Two\rModel 2':
        #print3( '' )
        #print3( 'sLook4 0:', sLook4 )
        #print3( 'lOrig:', lOrig )
        #print3( 'lLengths:', lLengths )
        #print3( 'bAddDash:', bAddDash )
    #
    bHasAlphaNum = hasAnyAlpha(  sLook4 ) and hasAnyDigits( sLook4 )
    #
    if bAddDash and ( bHasAlphaNum or ' ' in sLook4 ):
        #
        lParts = _getSplit( sLook4, oSeparator )
        #
        if bHasAlphaNum:
            lParts = [ _gotAlphaNumPutSeparator( s ) for s in lParts ]
        else:
            lParts = [ s.split() for s in lParts ]
        #
        lParts = [ '-'.join( lChars ) for lChars in lParts ]
        #
        sLook4 = '\r'.join( lParts )
        #
    #
    #if sLook4Orig == r'Model Two\rModel 2':
        #print3( 'sLook4 1:', sLook4 )
    #
    sRegEx = ''
    #
    if fDoThisFirst:
        #
        sLook4 = fDoThisFirst( sLook4 )
        #
    #
    #
    #if sLook4Orig == r'Model Two\rModel 2':
        #print3( 'sLook4 2:', sLook4 )
    #
    lDashed = _getEscapedThenSplit(
                    sLook4, oSeparator, bEscBegEndOfStr = bEscBegEndOfStr )
    #
    #if sLook4Orig == r'Model Two\rModel 2':
        #print3( 'lDashed:', lDashed )
    #
    if bPermutate:
        #
        lNewParts = []
        #
        for s in lDashed:
            #
            lSubParts = s.split()
            #
            for l in permutations( lSubParts ):
                #
                lNewParts.append( r'\b.*\b'.join( l ) )
                #
            #
        #
        lRegEx = getRidOfDupesKeepOrder( lNewParts )
        #
    else:
        #
        lRegEx = [  getRegEx4Chars( s,
                        dSub1st        = dSub1st,
                        dSub2nd        = dSub2nd,
                        tSubLast       = tSubLast )
                    for s in lDashed ]
    #
    #if sLook4Orig == r'Model Two\rModel 2':
        #print3( 'lRegEx 1:', lRegEx )
    #
    if bSubModelsOK:
        #
        sLastChar = lRegEx[0][-1]
        #
        if sLastChar.isdigit() and lRegEx[0][-7:-1] != '[-/ ]*':
            #
            pass
            #
        elif sLastChar.isalpha() or sLastChar.isdigit():
            #
            if sLastChar.isalpha() and bCaseSensitive: # will the search object be case sensitive?
                #
                sSubModelsVary = '[a-zA-Z]'
                #
            elif sLastChar.isalpha():
                #
                sSubModelsVary = '[A-Z]'
                #
            else:
                #
                sSubModelsVary = '[0-9]'
                #
            #        
            if lRegEx[0][-7:-1] == '[-/ ]*':
                #
                lRegEx[0] = ''.join( (
                        lRegEx[0][:-7],
                        '(?:[-/ ]*',
                        sSubModelsVary,
                        r'){0,1}\b' ) )
                #
            else:
                #
                lRegEx[0] = ''.join(
                        ( lRegEx[0][:-1], sSubModelsVary, r'{0,1}\b' ) )
                #
            #
        #
    elif bPluralize:
        #
        for i, s in getEnumerator( lRegEx ):
            #
            s = s.lower()
            #
            if s.endswith( 'e' ):
                #
                lRegEx[ i ] = s + 's{0,1}'
                #
            elif s.endswith( 'y' ):
                #
                lRegEx[ i ] = s[ : -1 ] + '(?:y|ys|ies)'
                #
            elif not s.endswith( 's' ):
                #
                lRegEx[ i ] = s + '(?:s|es){0,1}'
                #
            #
        #
    #
    #if sLook4Orig == r'Model Two\rModel 2':
        #print3( 'lRegEx 2:', lRegEx )
        #print3( 'iWordBoundChrs:', iWordBoundChrs )
    #
    if iWordBoundChrs > 0:
        #
        lLengths = [ len( getAlphaNumCleanNoSpaces( s ) )
                     for s in lOrig ]
        #
        #if sLook4Orig == r'Model Two\rModel 2':
            #print3( 'lLengths:', lLengths )
        #
        for i in iRange( len( lOrig ) ):
            #
            lParts = oFindSubs.split( lRegEx[ i ] )
            #
            if lOrig[ i ][ -1 ].isdigit() and lOrig[ i ].startswith( '^' ):
                # this one ends with a digit
                #
                lRegEx[ i ] = r'%s\b' % lRegEx[ i ]
                #
            elif ( lLengths[ i ] <= iWordBoundChrs or
                   len( lParts ) > 1 and len( lParts[-1] ) <= iWordBoundChrs ):
                #
                # world boundary chars not wanted if the string
                # begins or ends with non alpha numeric!
                #
                if  (   lOrig[ i ][  0 ] in setNonAlphaNums and
                        lOrig[ i ][ -1 ] in setNonAlphaNums ):
                    #
                    continue
                    #
                elif lOrig[ i ][ 0 ] in setNonAlphaNums:
                    #
                    lRegEx[ i ] = r'%s\b' % lRegEx[ i ]
                    #
                elif lOrig[ i ][ -1 ] in setNonAlphaNums:
                    #
                    lRegEx[ i ] = r'\b%s' % lRegEx[ i ]
                    #
                elif lLengths[ i ] <= iWordBoundChrs:
                    #
                    lRegEx[ i ] = r'\b%s\b' % lRegEx[ i ]
                    #
                elif not bSubModelsOK:
                    #(  len( lParts ) > 1 and
                    #    len( lParts[-1] ) <= iWordBoundChrs and
                    #    not bSubModelsOK ):
                    #
                    lRegEx[ i ] = r'%s\b' % lRegEx[ i ]
                    #
                #
            #
            #if sLook4Orig == r'Model Two\rModel 2':
                #print3( 'lRegEx[ %s ]:' % i, lRegEx[ i ] )
            #
            while lRegEx[ i ].endswith( r'\b\b' ):
                #
                lRegEx[ i ] = lRegEx[ i ][ : -2 ]
                #
            while lRegEx[ i ].startswith( r'\b\b' ):
                #
                lRegEx[ i ] = lRegEx[ i ][ 2 : ]
                #
        #
    #
    #if sLook4Orig == r'Model Two\rModel 2':
        #print3( 'lRegEx 3:', lRegEx )
    #
    for i in iRange( len( lOrig ) ):
        #
        while lRegEx[ i ].endswith( r'\b\b' ):
            #
            lRegEx[ i ] = lRegEx[ i ][ : -2 ]
            #
        #
    #
    #if sLook4Orig == r'Model Two\rModel 2':
        #print3( 'lRegEx 4:', lRegEx )
    #
    sRegEx = _getPartsBarred( getRidOfDupesKeepOrder( lRegEx ) )
    #
    #if sLook4Orig == r'Model Two\rModel 2':
        #print3( 'sRegEx 5:', sRegEx )
    #
    return sRegEx



def getRegExpObjGotStr(
        sLook4          = '',
        dSub1st         = dSub1st,
        dSub2nd         = dSub2nd,
        tSubLast        = tSubLast,
        fDoThisFirst    = None,
        oSeparator      = oFinderCRorLFnMore,
        bPermutate      = False,
        bAddDash        = False,
        bSubModelsOK    = False ):
    #
    sRegEx = getRegExpress(
        sLook4          = sLook4,
        dSub1st         = dSub1st,
        dSub2nd         = dSub2nd,
        tSubLast        = tSubLast,
        fDoThisFirst    = fDoThisFirst,
        oSeparator      = oSeparator,
        bPermutate      = bPermutate,
        bAddDash        = bAddDash,
        bSubModelsOK    = bSubModelsOK )
    #
    return getRegExObj( sRegEx )




def getRegExTips():
    #
    '''
from Mastering Regular Expressions by Jeffrey E.F. Friedl

use non-capturing parens (?:  )
do not add superfluous parens
do not use superfluous character classes
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
    from Iter.AllVers   import iMap, iRange
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    sTest = ( letters + digits ) * 5
    #
    oFindABC_ignore = getRegExObj( 'abc', bCaseSensitive = False )
    oFindABC_CaseSe = getRegExObj( 'abc', bCaseSensitive = True, bDotAll = True )
    #
    #print3( 'oFindABC_ignore:', oFindABC_ignore )
    #
    l = oFinderCRorLF.split( 'abc\rdef\nghi' )
    #
    if l != ['abc', 'def', 'ghi']:
        #
        lProblems.append( 'oFinderCRorLF not working! alternating split chars' )
        #
    #
    if      oFindABC_ignore.findall( sTest ) != \
                ['abc', 'ABC', 'abc', 'ABC', 'abc', 'ABC', 'abc', 'ABC', 'abc', 'ABC'] or \
            oFindABC_CaseSe.findall( sTest ) != \
                ['abc', 'abc', 'abc', 'abc', 'abc']:
        #
        lProblems.append( 'getRegExObj()' )
        #
    if getTextInQuotes( ' " how now brown cow\' " abc ' ) != " how now brown cow' ":
        #
        lProblems.append( 'getTextInQuotes()' )
        #
    #
    sFindThis = '<script.+?</script>|<style.+?</style>'
    oFindThis = getRegExObj( sFindThis, bCaseSensitive = False )
    #
    sTest = 'abc<script id=10>def</script>hij<style id = 99>klm</style>nop'
    #
    if oFindThis.findall( sTest ) != \
        ['<script id=10>def</script>', '<style id = 99>klm</style>']:
        #
        lProblems.append( 'getRegExObj() compound regex expression' )
        #
    #
    s = r'\bXP[-/ ]*55[-/ ]*B\b'
    #
    oRegExObj = getRegExObj( s )
    #
    sThis = "Vintage The Fisher XP-55B Speaker System-Pair"
    #
    if not oRegExObj.search( sThis ):
        #
        lProblems.append( 'getRegExObj() title has target' )
        #
    #
    if oFinderPunctuation.findall( sThis ) != ['-', '-']:
        #
        lProblems.append( 'oFinderPunctuation( "%s" )' % sThis )
        #
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
    sLook4 = "{blank}"
    sWant = "\\{blank\\}"
    #
    sGot = getRegExSpecialsEscapedNoShortcut( sLook4 )
    #
    if sGot != sWant:
        #
        print3( sGot )
        #
        lProblems.append( 'getRegExSpecialsEscapedNoShortcut("{blank}")' )
        #
    #
    sGot = getRegExSpecialsEscapedWithShortcut( sLook4 )
    #
    if sGot != sWant:
        #
        print3( sGot )
        #
        lProblems.append( 'getRegExSpecialsEscapedNoShortcut("{blank}")' )
        #
    #
    sLook4 = sWant = "Peerless"
    #
    sGot = getRegExSpecialsEscapedNoShortcut( sLook4 )
    #
    if sGot != sWant:
        #
        print3( sGot )
        #
        lProblems.append( 'getRegExSpecialsEscapedNoShortcut("Peerless")' )
        #
    #
    sGot = getRegExSpecialsEscapedWithShortcut( sLook4 )
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
    if sGot != 'Harman[-/ ]*Kardon':
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
        #   'Chigaco *Standard *Transformer *(Corporation|Company|Corp|Co)|Chigaco *Standard'
        #
        print3( sGot )
        #
        lProblems.append(
            'getRegEx4Chars(Chigaco Standard Transformer Corp.)' )
        #
    #
    sGot = getRegEx4Chars(
            'Chigaco Standard|Chigaco Standard Transformer Corp.' )
    #
    if sGot not in (
            'Chigaco *Standard|'
            'Chigaco *Standard *Transformer *(Corporation|Company|Corp|Co)',
            'Chigaco *Standard *Transformer *(Corporation|Company|Corp|Co)|'
            'Chigaco *Standard'):
        #
        print3( sGot )
        #
        lProblems.append( 'getRegEx4Chars(Chigaco Standard|Chigaco Standard Transformer Corp)' )
        #
    #
    sGot = getRegEx4Chars( 'Unholtz-Dickie Corp.' )
    #
    if sGot != 'Unholtz[-/ ]*Dickie *(Corporation|Company|Corp|Co)':
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
    if oFinderPunctuation.findall( sGot ) != ['*', '(', '&', '|', ')', '*']:
        #
        print3( oFinderPunctuation.findall( sGot ) )
        lProblems.append( 'oFinderPunctuation( "%s" )' % sGot )
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
    sLook4  = '50-W-2'
    #
    sGot    = getRegEx4Chars( sLook4 )
    #
    if sGot != '50[-/ ]*W[-/ ]*2':
        #
        print3( sGot )
        #
        lProblems.append( 'getRegEx4Chars(%s)' % sLook4 )
        #
    #
    sLook4  = '15" gold'
    #
    sGot    = getRegEx4Chars( sLook4 )
    #
    if sGot != '15"* *gold':
        #
        print3( sGot )
        #
        lProblems.append( 'getRegEx4Chars(%s)' % sLook4 )
        #
    #
    if oFinderPunctuation.findall( sGot ) != ['"', '*', '*']:
        #
        print3( oFinderPunctuation.findall( sGot ) )
        lProblems.append( 'oFinderPunctuation( "%s" )' % sGot )
        #
    #
    sLook4  = "TR-10 'Tri-ette'"
    #
    sGot    = getRegEx4Chars( sLook4 )
    #
    if sGot != "TR[-/ ]*10 *'*Tri[-/ ]*ette'*":
        #
        print3( sGot )
        #
        lProblems.append( 'getRegEx4Chars(%s)' % sLook4 )
        #
    #
    tExpect = ['[', '-', '/', ']', '*', '*', "'", '*', '[',
            '-', '/', ']', '*', "'", '*']
    #
    if oFinderPunctuation.findall( sGot ) != tExpect:
        #
        print3( oFinderPunctuation.findall( sGot ) )
        lProblems.append( 'oFinderPunctuation( "%s" )' % sGot )
        #
    #
    sLook4  = 'TV-2/U'
    #
    sGot    = getRegEx4Chars( sLook4 )
    #
    if sGot != 'TV[-/ ]*2(/ *)+U':
        #
        print3( sGot )
        #
        lProblems.append( 'getRegEx4Chars(%s)' % sLook4 )
        #
    #
    sLook4  = '50-X-C3'
    #
    sGot    = getRegEx4Chars( sLook4 )
    #
    if sGot != '50[-/ ]*X[-/ ]*C3':
        #
        print3( sGot )
        #
        lProblems.append( 'getRegEx4Chars(%s)' % sLook4 )
        #
    #
    sLook4  = '1'
    #
    sGot    = getRegEx4Chars( sLook4, iWordBoundChrs = 1 )
    #
    if sGot != r'\b1\b':
        #
        print3( sGot )
        #
        lProblems.append( 'getRegEx4Chars(%s)' % sLook4 )
        #
    #

    #
    sLook4  = '1217-1290'
    #
    oFinder = getRegExpObjGotStr( sLook4 ).search
    #
    sTest   = 'VINTAGE JBL 175 driver with 1217/1290 HORNS!!'
    #
    oGot    = oFinder( sTest )
    #
    if not oGot:
        #
        print3( oGot )
        #
        lProblems.append(
            'getRegExpObjGotStr(%s) testing "%s"' % ( sLook4, sTest ) )
        #
    #
    #
    sLook4  = 'Heintz&Kaufman'
    #
    oFinder = getRegExpObjGotStr( sLook4 ).search
    #
    sTest   = '6DJ8 vacuum tube HEINTZ AND KAUFMAN "Made in England"'
    #
    oGot    = oFinder( sTest )
    #
    if not oGot:
        #
        print3( oGot )
        #
        lProblems.append(
            'getRegExpObjGotStr(%s) testing "%s"' % ( sLook4, sTest ) )
        #
    #
    sLook4  = 'AX-235'
    #
    oFinder = getRegExpObjGotStr( sLook4 ).search
    #
    sTest   = "Emerson \"Little Miracle\" Marbled Green White and Yellow Catalin Tube Radio AX235"
    #
    oGot    = oFinder( sTest )
    #
    if not oGot:
        #
        print3( oGot )
        #
        lProblems.append(
            'getRegExpObjGotStr(%s) testing "%s"' % ( sLook4, sTest ) )
        #
    #
    sLook4  = 'Fada'
    #
    oFinder = getRegExpObjGotStr( sLook4 ).search
    #
    sTest   = 'VINTAGE BEAUTIFUL 40s FADA BULLET ART DECO CATALIN BAKELITE ANTIQUE TUBE RADIO'
    #
    oGot    = oFinder( sTest )
    #
    if not oGot:
        #
        print3( oGot )
        #
        lProblems.append(
            'getRegExpObjGotStr(%s) testing "%s"' % ( sLook4, sTest ) )
        #
    #    
    sLook4  = 'L-56'
    #
    oFinder = getRegExpObjGotStr( sLook4 ).search
    #
    sTest   = 'Maroon Fada L-56 Catalin Radio'
    #
    oGot    = oFinder( sTest )
    #
    if not oGot:
        #
        print3( oGot )
        #
        lProblems.append(
            'getRegExpObjGotStr(%s) testing "%s"' % ( sLook4, sTest ) )
        #
    #    
    sLook4  = 'Black & Decker'
    #
    oFinder = getRegExpObjGotStr( sLook4 )
    #
    sTest   = 'abc BLACK AND DECKER efg'
    #
    oGot    = oFinder.search( sTest )
    #
    if not oGot:
        #
        print3( oGot )
        print3( 'oFinder:', oFinder )
        #
        lProblems.append(
            'getRegExpObjGotStr(%s) testing "%s"' % ( sLook4, sTest ) )
        #
    #
    sLook4  = 'BLACK AND DECKER'
    ##
    oFinder = getRegExpObjGotStr( sLook4 ).search
    #
    sTest   = 'abc Black&Decker efg'
    #
    oGot    = oFinder( sTest )
    #
    if not oGot:
        #
        print3( oGot )
        #
        lProblems.append(
            'getRegExpObjGotStr(%s) testing "%s"' % ( sLook4, sTest ) )
        #
    #
    sLook4 = 'How now brown cow'
    #
    oFinder = getRegExpObjGotStr( sLook4, bPermutate = True ).search
    #
    sTest   = 'Cow brown how now'
    #
    oGot    = oFinder( sTest )
    #
    if not oGot:
        #
        print3( oGot )
        #
        lProblems.append(
            'getRegExpObjGotStr(%s) testing "%s"' % ( sLook4, sTest ) )
        #
    #
    sLook4  = 'BM258'
    #
    lGot    = _gotAlphaNumPutSeparator( sLook4 )
    #
    if lGot != ['BM', '258']:
        #
        print3( lGot )
        #
        lProblems.append(
            '_gotAlphaNumPutSeparator(%s)' % sLook4 )
        #
    #
    sLook4 = 'N-15-00A00-18'
    #
    lGot    = _gotAlphaNumPutSeparator( sLook4 )
    #
    if lGot != ['N-15-00', 'A', '00-18']:
        #
        print3( lGot )
        #
        lProblems.append(
            '_gotAlphaNumPutSeparator(%s)' % sLook4 )
        #
    #
    sLook4  = 'N-1500A'
    #
    lGot    = _gotAlphaNumPutSeparator( sLook4 )
    #
    if lGot != ['N-1500', 'A' ]:
        #
        print3( lGot )
        #
        lProblems.append(
            '_gotAlphaNumPutSeparator(%s)' % sLook4 )
        #
    #    
    sRegExpress = getRegExpress( sLook4,
                            bSubModelsOK   = True,
                            bAddDash       = True )
    #
    sWant = r'N[-/ ]*1500(?:[-/ ]*[A-Z]){0,1}\b'
    #
    if sRegExpress != sWant:
        #
        print3( 'got: ', sRegExpress )
        print3( 'want:', sWant )
        #
        lProblems.append(
            'getRegExpress(%s) testing "%s"' % ( sLook4, 'bSubModelsOK = True, bAddDash = True' ) )
        #
    #
    sLook4 = 'Table Radio\rPre-amplifier\rPre-amp\rFuse Holder\rCapacitor'
    #
    sRegExpress = getRegExpress( sLook4, iWordBoundChrs = 2, bEscBegEndOfStr = False )
    #
    sWant = 'Table *Radio|Pre[-/ ]*amplifier|Pre[-/ ]*amp|Fuse *Holder|Capacitor'
    #
    if sRegExpress != sWant:
        #
        print3( 'got: ', sRegExpress )
        print3( 'want:', sWant )
        #
        lProblems.append(
            'getRegExpress(%s) testing "%s"' % ( sLook4, 'iWordBoundChrs = 5, bEscBegEndOfStr = False' ) )
        #
    #
    sLook4 = 'Lot of 10\rLot of (10)\r^10'
    #
    sRegExpress = getRegExpress( sLook4, iWordBoundChrs = 5, bEscBegEndOfStr = False )
    #
    sWant = r'Lot *of *10\b|Lot *of *\(10\)|^10\b'
    #
    if sRegExpress != sWant:
        #
        print3( 'got: ', sRegExpress )
        print3( 'want:', sWant )
        #
        lProblems.append(
            'getRegExpress(%s) testing "%s"' % ( sLook4, 'iWordBoundChrs = 5, bEscBegEndOfStr = False' ) )
        #
    #
    #
    sLook4 = r'Model Two\rModel 2'
    #
    sRegExpress = getRegExpress( sLook4, iWordBoundChrs = 2, bAddDash = True )
    #
    sWant = r'Model[-/ ]*Two|Model[-/ ]*2\b'
    #
    if sRegExpress != sWant:
        #
        print3( 'got: ', sRegExpress )
        print3( 'want:', sWant )
        #
        lProblems.append(
            'getRegExpress(%s) testing "%s"' % ( sLook4, 'iWordBoundChrs = 5, bAddDash = True' ) )
        #
    #
    #oRegExObj = getRegExObj( sRegExpress )
    #
    #print3( 'oRegExObj.pattern:', oRegExObj.pattern )
    #
    #
    sLook4 = 'Model 2'
    #
    sRegExpress = getRegExpress( sLook4, iWordBoundChrs = 4 )
    #
    if sRegExpress != r'Model *2\b':
        #
        print3( '%s:' % sLook4, sRegExpress )
        #
        lProblems.append(
            'getRegExpress(%s) testing "%s"' % ( sLook4, 'iWordBoundChrs = 4' ) )
        #
    #
    #
    #
    sLook4 = '288-8F'
    #
    sRegExpress = getRegExpress( sLook4,
                            bSubModelsOK   = True,
                            bAddDash       = True )
    #
    sWant = r'288[-/ ]*8(?:[-/ ]*[A-Z]){0,1}\b'
    #
    if sRegExpress != sWant:
        #
        print3( 'got: ', sRegExpress )
        print3( 'want:', sWant )
        #
        lProblems.append(
            'getRegExpress(%s) testing "%s"' % ( sLook4, 'bSubModelsOK = True, bAddDash = True' ) )
        #
    #
    sLook4  = 'LSU/HF/15'
    #
    sRegExpress = getRegExpress( sLook4, bAddDash = True )
    #
    oRegExObj = getRegExObj( sRegExpress )
    #
    sThis  = 'TANNOY GRF CORNER CABINET w. 15" SILVER DUAL CONCENTRIC DRIVER LSU/HF/15 SUPERB'
    #
    if not oRegExObj.search( sThis ):
        #
        lProblems.append( '%s : getRegExObj() title has target' % oRegExObj )
        #
    #
    #
    sLook4 = '15" Silver'
    #
    sRegExpress = getRegExpress( sLook4, bAddDash = True )
    #
    if sRegExpress != '15"*[-/ ]*Silver':
        #
        print3( sRegExpress )
        #
        lProblems.append(
            'getRegExpress(%s) testing "%s"' % ( sLook4, 'bAddDash = True' ) )
        #
    #
    oRegExObj = getRegExObj( sRegExpress )
    #
    sThis  = 'TANNOY GRF CORNER CABINET w. 15" SILVER DUAL CONCENTRIC DRIVER'
    #
    if not oRegExObj.search( sThis ):
        #
        lProblems.append( '%s : getRegExObj() title has target' % oRegExObj )
        #
    #
    sLook4 = 'watch\rphone\rcaddy'
    #
    sRegExpress = getRegExpress( sLook4, bPluralize = True )
    #
    tAll = (    'phones{0,1}',
                'watch(?:s|es){0,1}',
                'cadd(?:y|ys|ies)' )
    #
    bAllIn = True
    #
    for s in tAll:
        if s not in sRegExpress:
            bAllIn = False
    #
    if not bAllIn:
        #
        print3( sRegExpress )
        print3( tAll )
        #
        lProblems.append(
            'getRegExpress(%s) testing "%s"' % ( sLook4, 'bPluralize = True' ) )
        #
    #
    sLook4 = 'Lot of 10\r^10'
    #
    sRegExpress = getRegExpress( sLook4, bEscBegEndOfStr = False )
    #
    lParts = sRegExpress.split( '|' )
    #
    if '^10' not in lParts or 'Lot *of *10' not in lParts:
        #
        print3( sRegExpress )
        print3( lParts )
        #
        lProblems.append(
            'getRegExpress(%s) testing "%s"' %
                ( sLook4, 'bEscBegEndOfStr = False' ) )
        #
    #
    sLook4 = 'BM258'
    #
    sRegExpress = getRegExpress( sLook4, bAddDash = True )
    #
    if sRegExpress != 'BM[-/ ]*258':
        #
        print3( sRegExpress )
        #
        lProblems.append(
            'getRegExpress(%s) testing "%s"' %
                ( sLook4, 'bAddDash = True' ) )
        #
    #
    sLook4 = 'CA-3'
    #
    sRegExpress = getRegExpress(
                    sLook4, bSubModelsOK = True, iWordBoundChrs = 4 )
    #
    sWant = r'\bCA(?:[-/ ]*[0-9]){0,1}\b'
    #
    if sRegExpress != sWant:
        #
        print3( 'got: ', sRegExpress )
        print3( 'want:', sWant )
        #
        lProblems.append(
            'getRegExpress(%s) testing "%s"' % ( sLook4, 'bSubModelsOK = True' ) )
        #
    #
    
    sLook4 = 'LHT-1'
    #
    sRegExpress = getRegExpress( sLook4, bSubModelsOK = True )
    #
    sWant = r'LHT(?:[-/ ]*[0-9]){0,1}\b'
    #
    if sRegExpress != sWant:
        #
        print3( 'got: ', sRegExpress )
        print3( 'want:', sWant )
        #
        lProblems.append(
            'getRegExpress(%s) testing "%s"' % ( sLook4, 'bSubModelsOK = True' ) )
        #
    #
    sLook4 = '26A'
    #
    sRegExpress = getRegExpress( sLook4, bSubModelsOK = True )
    #
    sWant = r'26[A-Z]{0,1}\b'
    #
    if sRegExpress != sWant:
        #
        print3( 'got: ', sRegExpress )
        print3( 'want:', sWant )
        #
        lProblems.append(
            'getRegExpress(%s) testing "%s"' % ( sLook4, 'bSubModelsOK = True' ) )
        #
    #
    sLook4 = '604C'
    #
    sRegExpress = getRegExpress( sLook4,
                                 bSubModelsOK = True, iWordBoundChrs = 5 )
    #
    sWant = r'\b604[A-Z]{0,1}\b'
    #
    if sRegExpress != sWant:
        #
        print3( 'got: ', sRegExpress )
        print3( 'want:', sWant )
        #
        lProblems.append(
            'getRegExpress(%s) testing "%s"' % ( sLook4, 'bSubModelsOK = True' ) )
        #
    #
    oRegExpObj = getRegExpObjGotStr( sLook4, bSubModelsOK = True )
    #
    if not oRegExpObj.search( '604D' ):
        #
        print3( "oRegExpObj = getRegExpObjGotStr( '604C', bSubModelsOK = True )" )
        print3( "oRegExpObj.search( '604D' )", 'returned False' )
        #
        lProblems.append(
            'getRegExpObjGotStr(%s) testing "%s"' % ( sLook4, 'bSubModelsOK = True' ) )
        #
    #
    if oRegExpObj.search( '605C' ):
        #
        print3( "oRegExpObj = getRegExpObjGotStr( '604C', bSubModelsOK = True )" )
        print3( "oRegExpObj.search( '605C' )", 'returned True' )
        #
        lProblems.append(
            'getRegExpObjGotStr(%s) testing "%s"' % ( sLook4, 'bSubModelsOK = True' ) )
        #
    #
    sRegExpress = getRegExpress( sLook4, bAddDash = True, bSubModelsOK = True )
    #
    sWant = r'604(?:[-/ ]*[A-Z]){0,1}\b'
    #
    if sRegExpress != sWant:
        #
        print3( 'got: ', sRegExpress )
        print3( 'want:', sWant )
        #
        lProblems.append(
            'getRegExpress(%s) testing "%s"' % ( sLook4, 'bAddDash & bSubModelsOK = True' ) )
        #
    #
    oRegExpObj = getRegExpObjGotStr( sLook4, bAddDash = True, bSubModelsOK = True )
    #
    if not oRegExpObj.search( '604D' ):
        #
        print3( "oRegExpObj = getRegExpress( '604C', bAddDash = True, bSubModelsOK = True )" )
        print3( "oRegExpObj.search( '604D' )", 'returned False' )
        #
        lProblems.append(
            'getRegExpObjGotStr(%s) testing "%s"' % ( sLook4, 'bAddDash & bSubModelsOK = True' ) )
        #
    #
    if oRegExpObj.search( '605C' ):
        #
        print3( "oRegExpObj = getRegExpress( '604C', bAddDash = True, bSubModelsOK = True )" )
        print3( "oRegExpObj.search( '605C' )", 'returned True' )
        #
        lProblems.append(
            'getRegExpObjGotStr(%s) testing "%s"' % ( sLook4, 'bAddDash & bSubModelsOK = True' ) )
        #
    #
    sLook4 = 'ab\rcd\nef\n\rgh'
    #
    l = oFinderCRorLF.split( sLook4 )
    #
    if l != ['ab', 'cd', 'ef', '', 'gh']:
        #
        lProblems.append( 'oFinderCRorLF not working! repeated split chars' )
        #
    #
    sLook4More = ''.join( ( 'ab\rcd\nef', r'\\r', 'gh', r'\\n', 'ijk\\' '\nlmn\\' '\ropq' ) )
    #
    l = oFinderCRorLFnMore.split( sLook4More )
    #
    if l != ['ab', 'cd', 'ef', 'gh', 'ijk', 'lmn', 'opq']:
        #
        print3('')
        print3( sLook4More )
        print3( l )
        lProblems.append( 'oFinderCRorLFnMore not working! different split chars' )
        #
    #
    sLook4This = 'book shelf\rdigital'
    #
    l = oFinderCRorLFnMore.split( sLook4This )
    #
    if l != ['book shelf', 'digital']:
        #
        lProblems.append( 'oFinderCRorLFnMore not working! book shelf / digital' )
        #
    #
    #
    sLook4This = r'book shelf\rdigital'
    #
    l = oFinderCRorLFnMore.split( sLook4This )
    #
    if l != ['book shelf', 'digital']:
        #
        lProblems.append( 'oFinderCRorLFnMore not working! book shelf / psuedo r / digital' )
        #
    #
    #
    sLook4This = r'book shelf\\rdigital'
    #
    l = oFinderCRorLFnMore.split( sLook4This )
    #
    if l != ['book shelf', 'digital']:
        #
        lProblems.append( 'oFinderCRorLFnMore not working! book shelf / double slash psuedo r / digital' )
        #
    #
    sLook4 = 'ab\rcd\nef\n\rgh'
    #
    sRegExpress = getRegExpress( sLook4 ) # order is now predictable -- same
    #
    sWant = 'ab|cd|ef|gh'
    #
    if sRegExpress != sWant:
        #
        print3( 'got: ', sRegExpress )
        print3( 'want:', sWant )
        #
        lProblems.append(
            'getRegExpress(%s) testing "%s"' % ( sLook4, 'repeated split chars' ) )
        #
    #
    sLook4 = 'ab\rcdefghi\n\rjk'
    #
    sRegExpress = getRegExpress( sLook4, iWordBoundChrs  = 3 )
    #
    sWant = r'\bab\b|cdefghi|\bjk\b'
    #
    if sRegExpress != sWant:
        #
        print3( 'got: ', sRegExpress )
        print3( 'want:', sWant )
        #
        lProblems.append(
            'getRegExpress(%s) testing "%s"' % ( sLook4, 'iWordBoundChrs  = 3' ) )
        #
    #
    #
    sLook4 = 'Model 2\rModel Two'
    #
    sRegExpress = getRegExpress( sLook4, iWordBoundChrs  = 2 )
    #
    sWant = r'Model *2\b|Model *Two'
    #
    if sRegExpress != sWant:
        #
        print3( 'got: ', sRegExpress )
        print3( 'want:', sWant )
        #
        lProblems.append(
            'getRegExpress(%s) testing "%s"' % ( sLook4, 'iWordBoundChrs  = 3' ) )
        #
    #
    #
    sLook4 = '(2)'
    #
    sRegExpress = getRegExpress( sLook4, iWordBoundChrs  = 3 )
    #
    sWant = '\(2\)'
    #
    if sRegExpress != sWant:
        #
        print3( 'got: ', sRegExpress )
        print3( 'want:', sWant )
        #
        lProblems.append( 'getRegExpress(%s)' % sLook4 )
        #
    #
    sLook4 = 'H.S. Martin'
    #
    sRegExpress = getRegExpress( sLook4, iWordBoundChrs  = 3 )
    #
    sWant = 'H[. ]*S[. ]* *Martin'
    #
    if sRegExpress != sWant:
        #
        print3( 'got: ', sRegExpress )
        print3( 'want:', sWant )
        #
        lProblems.append( 'getRegExpress(%s)' % sLook4 )
        #
    #
    sLook4 = 'Groove Tubes'
    #
    sRegExpress = getRegExpress( sLook4, bAddDash = True )
    #
    sWant = 'Groove[-/ ]*Tubes'
    #
    if sRegExpress != sWant:
        #
        print3( 'got: ', sRegExpress )
        print3( 'want:', sWant )
        #
        lProblems.append( 'getRegExpress(%s)' % sLook4 )
        #
    #
    #
    sLook4 = 'Groove-Tubes'
    #
    sRegExpress = getRegExpress( sLook4, bAddDash = True )
    #
    if sRegExpress != sWant:
        #
        print3( 'got: ', sRegExpress )
        print3( 'want:', sWant )
        #
        lProblems.append( 'getRegExpress(%s)' % sLook4 )
        #
    #
    sLook4 = '6550-VI'
    #
    sRegExpress = getRegExpress( sLook4, iWordBoundChrs = 3 )
    #
    sWant = r'6550[-/ ]*VI\b'
    #
    if sRegExpress != sWant:
        #
        print3( 'got: ', sRegExpress )
        print3( 'want:', sWant )
        #
        lProblems.append( 'getRegExpress(%s)' % sLook4 )
        #
    #
    #
    sThis = '#83 Lot Of 3rca Cunningham Radiotron 45 Ux 245 Cx 345 Vacuum tubes'
    #
    sExclude = '83 total - #83'
    #
    sLook4 = '#83'
    #
    sRegExpress = getRegExpress( sLook4, iWordBoundChrs = 2 )
    #
    sWant = r'#83\b'
    #
    if sRegExpress != sWant:
        #
        print3( 'got: ', sRegExpress )
        print3( 'want:', sWant )
        #
        lProblems.append( 'getRegExpress(%s)' % sLook4 )
        #
    #
    #
    sLook4 = '83#'
    #
    sRegExpress = getRegExpress( sLook4, iWordBoundChrs = 2 )
    #
    sWant = r'\b83#'
    #
    if sRegExpress != sWant:
        #
        print3( 'got: ', sRegExpress )
        print3( 'want:', sWant )
        #
        lProblems.append( 'getRegExpress(%s)' % sLook4 )
        #
    #
    #
    sayTestResult( lProblems )
