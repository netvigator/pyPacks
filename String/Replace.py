#!/home/rick/.local/bin/pythonTest
# -*- coding: utf-8 -*-
#
# string functions Replace
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

try:
    from .Split         import SplitC, iterSplit, SplitRegular as _SplitRegular
    from ..Dict.Get     import getDictOffPairOfLists
    from ..Iter.AllVers import iFilter, lFilter, iMap
except ( ValueError, ImportError ):
    from String.Split   import SplitC, iterSplit, SplitRegular as _SplitRegular
    from Dict.Get       import getDictOffPairOfLists
    from Iter.AllVers   import iFilter, lFilter, iMap



def getReplaced( sThis, oFinder, sWant = '' ):
    #
    iLastLen        = -1
    #
    while len( sThis ) != iLastLen:
        #
        iLastLen    = len( sThis )
        #
        sThis       = oFinder.sub( sWant, sThis )
        #
    #
    return sThis


# def getReplaced( oFinder, sThis, sWant = '' ):



def _obsoleteGlobalReplacements( sText, lListofTuples ):
    #
    """
    Multiple replacements in one pass via re.
    """
    #
    try: # moving this to the top breaks this package!
        from .Transform       import getSwapper
    except ( ValueError, ImportError ): # maybe circular import issue
        from String.Transform import getSwapper
    #
    dReplace            = dict( lListofTuples )
    #
    Swapper          = getSwapper( dReplace )
    #
    bSameLengths        = True
    #
    for sOld, sNew in lListofTuples:
        #
        if len( sOld ) != len( sNew ):
            #
            bSameLengths= False
            #
            break
            #
        #
    #
    if bSameLengths:
        #
        sCopy           = sText
        #
        while True:
            #
            sText       = Swapper( sText )
            #
            if sCopy == sText:
                #
                break
                #
            else:
                #
                sCopy   = sText
                #
            #
        #
    else:
        #
        iLastLen = -1
        #
        while len( sText ) != iLastLen:
            #
            iLastLen    = len( sText )
            #
            sText       = Swapper( sText )
            #
        #
    #
    #
    return sText


def getManyOldWithManyNewSwapper( dReplace,
                                    bEscape = True, bMultiLine = False ):
    #
    #
    try: # moving this to the top breaks this package!
        from .Transform       import getSwapper
    except ( ValueError, ImportError ): # maybe circular import issue
        from String.Transform import getSwapper
    #
    Swapper = getSwapper( dReplace,
                    bEscape = bEscape, bMultiLine = bMultiLine )
    #
    return Swapper



def ReplaceManyOldWithManyNew( sText, dReplace, bEscape = True ):
    #
    Swapper = getManyOldWithManyNewSwapper( dReplace, bEscape = bEscape )
    #
    return Swapper( sText )




def getReplaceManyOldWithBlanksSwapper( lReplace, bJustRemove = False ):
    #
    try: # moving this to the top breaks this package!
        from .Transform       import getSwapper
    except ( ValueError, ImportError ): # maybe circular import issue
        from String.Transform import getSwapper
    #
    #
    if bJustRemove:
        #
        lNew            = [ '' ] * len( lReplace )
        #
    else:
        #
        lNew            = [ ''.ljust( len( sOld ) ) for sOld in lReplace ]
    #
    dReplace            = getDictOffPairOfLists( lReplace, lNew )
    #
    Swapper             = getSwapper( dReplace )
    #
    return Swapper




def ReplaceManyOldWithBlanks( sText, lReplace, bJustRemove = False ):
    #
    Swapper          = getReplaceManyOldWithBlanksSwapper( lReplace, bJustRemove )
    #
    return Swapper( sText )



def get_obsoleteGlobalReplaceWithSwapper( sText, Swapper ):
    #
    sCopy = sText
    #
    while True:
        #
        sText   = Swapper( sText )
        #
        if sText == sCopy:
            #
            break
            #
        else:
            #
            sCopy = sText
            #
        #
    #
    return sText



def getBlanksForReMatchObj( oMatch ):
    #
    """
    used for re finder object .sub functions
    returns string of space characters same length as the matched string
    example:
    sNew = oFindUnNeeded.sub( getBlanksForReMatchObj, sOrig )
    """
    #
    return ''.ljust( len( oMatch.group() ) )



def getSpaceForWhiteAlsoStrip( s ):
    #
    '''pass string
    each set of contiguous whitespace chars is replaced with one space
    except white on front and end is discarded
    return string
    aka getExtraWhiteOut()
    '''
    #
    lParts = s.split()
    #
    return ' '.join( lParts )



def getTextReversed( s ):
    #
    return s[::-1]



def ReverseOrder( uText ):  # works on strings and tuples as well as lists
    #
    bGotString  = isinstance( uText, str )
    #
    if bGotString:
        #
        uReturn = uText[::-1]
        #
    else:
        #
        lText       = list( uText ) # in case of tuple also
        #
        lText.reverse()
        #
        uReturn = lText
        #
    return uReturn




def replaceLast( s, sOld, sNew, iHowMany = 1 ):
    #
    '''
    The string built-in replace function can replace
    the first n (rather i) occurances of sOld,
    working left to right; this works right to left.
    If you want replace all,
    use string built-in replace function -- it's faster.
    Use this if you want to replace some on the right but not all.
    '''
    sReversed   = getTextReversed( s )
    #
    sReplaced   = sReversed.replace( getTextReversed( sOld ), getTextReversed( sNew ), iHowMany )
    #
    return getTextReversed( sReplaced )



def getGlobalReplaceReSplits( oFinder, sHaystack, sNewNeedle ):
    #
    try: # moving this to the top breaks this package!
        from .Get       import getStripped
    except ( ValueError, ImportError ): # maybe circular import issue
        from String.Get import getStripped    
    #
    lParts = oFinder.split( sHaystack )
    #
    lParts = lFilter( None, iMap( getStripped, iFilter( None, lParts ) ) )
    #
    if lParts[0][0] != sHaystack[0][0]:
        #
        lParts[0:0] = ['']
        #
    return sNewNeedle.join( lParts )



def _getReplacedSplit( sHaystack, oFinder, sNewNeedle='' ):
    #
    """
    Like replace, except not case sensitive.
    A little faster than ReReplaceC!
    currently not called anywhere, not even tested here
    """
    #
    #
    iterParts = iterSplit( sHaystack, oFinder )
    #
    return sNewNeedle.join( iterParts )



def _obsoleteGlobalReplace( sThis, sDump, sWant = '', fSplit = _SplitRegular ):
    #
    """
    Keeps on going until sDump is completely gone.
    Example: you want to compress newline-space-newline sandwiches.
    Consider using regular expressions instead of this.
    This is the case sensitive version.
    """
    #
    if len( sDump ) != len( sWant ):
        #
        iLastLen        = -1
        #
        while len( sThis ) != iLastLen:
            #
            iLastLen    = len( sThis )
            #
            lParts      = fSplit( sThis, sDump )
            #
            sThis       = sWant.join( lParts )
            #
    else:
        #
        while True:
            #
            lParts      = fSplit( sThis, sDump )
            #
            sNew        = sWant.join( lParts )
            #
            if sNew == sThis:
                break
            else:
                sThis = sNew
        #
    #
    return sThis


def _global_ReplaceC( sThis, sDump, sWant = '' ):
    #
    """
    This is the version that is not case sensitive.
    currently not used anywhere
    """
    #
    #
    return _obsoleteGlobalReplace( sThis, sDump, sWant, SplitC )




if __name__ == "__main__":
    #
    lProblems = []
    #
    from re     import compile as REcompile
    from string import digits
    from string import ascii_letters   as letters
    from string import ascii_lowercase as lowercase
    from string import ascii_uppercase as uppercase
    #
    from String.Find    import getRegExObj
    from Utils.Result   import sayTestResult
    #
    sTest   = digits + lowercase + digits + uppercase + digits
    #
    if _obsoleteGlobalReplace( sTest, digits, '~' ) != '~' + lowercase + '~' + uppercase + '~':
        #
        lProblems.append( '_obsoleteGlobalReplace()' )
        #
    if _global_ReplaceC( sTest, lowercase, '~' ) != '~'.join( [digits] * 3 ):
        #
        lProblems.append( '_global_ReplaceC()' )
        #
    #
    oAlphaLowerFinder  = getRegExObj( '[a-z]', bCaseSensitive = True  )
    oAlphaLetterFinder = getRegExObj( '[a-z]', bCaseSensitive = False )
    #
    sTilde26 = '~' * 26
    #
    if      getReplaced( sTest, oAlphaLowerFinder, '~' ) != \
                    digits + sTilde26 + digits + uppercase + digits  or \
            getReplaced( sTest, oAlphaLetterFinder, '~' ) != \
                    sTilde26.join( [ digits ] * 3 ):
        #
        lProblems.append( 'getReplaced()' )
        #
    if _obsoleteGlobalReplacements( sTest, \
            ( ( digits, '~' ), ( uppercase, '!' ), ( lowercase, '@' ) ) ) != '~@~!~':
        #
        lProblems.append( '_obsoleteGlobalReplacements()' )
        #
    #
    if ReplaceManyOldWithManyNew( sTest, ( ( digits, '~' ), ( uppercase, '!' ), ( lowercase, '@' ) ) ) != '~@~!~':
        #
        lProblems.append( 'ReplaceManyOldWithManyNew() %s' % sTest )
        #
    #
    dReplace = { '&quot;' : '"', '&eacute;' : 'e' }
    #
    if ReplaceManyOldWithManyNew( ' &quot;Andr&eacute;&quot; ', dReplace ) != ' "Andre" ':
        #
        lProblems.append( 'ReplaceManyOldWithManyNew() Andre' )
        #
    #
    oSwap4Blanks = getReplaceManyOldWithBlanksSwapper( ( digits, uppercase, lowercase ) )
    #
    if oSwap4Blanks( sTest ) != ' ' * 82:
        #
        lProblems.append( 'getReplaceManyOldWithBlanksSwapper()' )
        #
    if ReplaceManyOldWithBlanks( sTest, ( digits, uppercase, lowercase ) ) != ' ' * 82:
        #
        lProblems.append( 'ReplaceManyOldWithBlanks()' )
        #
    if get_obsoleteGlobalReplaceWithSwapper( sTest, oSwap4Blanks ) != ' ' * 82:
        #
        lProblems.append( 'get_obsoleteGlobalReplaceWithSwapper()' )
        #
    #
    oMatch = REcompile( 'l.+e' )
    #
    if oMatch.sub( getBlanksForReMatchObj,
            'Mary had a little lamb.' ) != \
            'Mary had a        lamb.':
        #
        lProblems.append( 'getBlanksForReMatchObj()' )
        #
    #
    sWhiteChars = '\n\t\rabc\r\t\n'
    #
    if      getSpaceForWhiteAlsoStrip( sWhiteChars  ) != 'abc' or \
            getSpaceForWhiteAlsoStrip( sWhiteChars+sWhiteChars ) != 'abc abc':
        #
        lProblems.append( 'getSpaceForWhiteAlsoStrip()' )
        #
    #
    if replaceLast( 'abcde0fghij0klmno0pqrst0uvwxy0z', '0', '8' ) != \
                    'abcde0fghij0klmno0pqrst0uvwxy8z':
        #
        lProblems.append( 'replaceLast()' )
        #
    #
    if getTextReversed( lowercase ) != 'zyxwvutsrqponmlkjihgfedcba':
        #
        lProblems.append( 'getTextReversed()' )
        #
    #
    if ReverseOrder( lowercase ) != 'zyxwvutsrqponmlkjihgfedcba':
        #
        lProblems.append( 'ReverseOrder' )
        #
    #
    oFinder = getRegExObj( '<(?!(u>|/|em>|b(>| )))', bCaseSensitive = False )
    #
    sOneLongLine = '''<div id=gbar><nobr><em>ABC</em><b class=gb1>Search</b><u>More</u> &raquo;</a></nobr></div><div id=guser width=100%>'''
    #
    sShorterLines = '''
<div id=gbar>
<nobr><em>ABC</em><b class=gb1>Search</b><u>More</u> &raquo;</a></nobr></div>
<div id=guser width=100%>'''
    #
    sReplaced = getGlobalReplaceReSplits( oFinder, sOneLongLine, '\n<' )
    #
    if sReplaced != sShorterLines:
        #
        lProblems.append( 'getGlobalReplaceReSplits()' )
        #
    #
    sayTestResult( lProblems )

