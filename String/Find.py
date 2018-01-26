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
    oFinder = getFinder( sPattern, bCaseSensitive, bDotAll )
    #
    return oFinder.findall


def getSeqWordBounds( seq ):
    #
    return r'\b%s\b' % r'\b|\b'.join( seq )





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
    #    
    sayTestResult( lProblems )