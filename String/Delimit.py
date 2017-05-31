#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# string functions Delimit Delimiters
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
# Copyright 2004-2017 Rick Graves
#

from six import print_ as print3

def _LopOffEnd( sOrig, sSplitOn, sSplitB4 ):
    #
    # called in _blankBlockUseEnd
    #
    from String.Split import SplitC
    #
    lParts  = SplitC( sOrig, sSplitOn, iMaxSplits = 1, bSplitLeft = False )
    #
    if len( lParts ) == 1: return sOrig + sSplitB4
    #
    return lParts[ 0 ]



def _LopOffBeg( sOrig, sSplitOn, sSplitB4 ):
    #
    # called in _blankBlockUseEnd
    #
    from String.Split import SplitC
    #
    lParts  = SplitC( sOrig, sSplitOn, iMaxSplits = 1 )
    #
    if len( lParts ) == 1: return  sSplitB4 + sOrig
    #
    return lParts[ -1 ]



def _blankBlockUseEnd(
        sOrigText, sBegCode = '!#', sEndCode = '$%*', sOrigLower = '' ):
    #
    from Iter.AllVers import iZip, iMap
    from String.Split import getPartsListAndBothStarts
    #
    lParts, lStartText, lStartSplit = \
        getPartsListAndBothStarts( sOrigText, sEndCode, sOrigLower )
    #
    if len( lParts ) <= 1: # no blocks to blank
        #
        return sOrigText
        #
    #
    # [ t[0] - t[1] for t in iZip( lStartSplit, lStartText ) ] == m@p( len, lParts )
    #
    iEndLen         = len( sEndCode )
    #
    lPartsLens      = [ iEndLen + t[0] - t[1]
                        for t in iZip( lStartSplit, lStartText ) ]
    #
    lPartsLens[-1]  -= iEndLen # no split char after end
    #
    def LopOffEndAddBlanks( t ):
        #
        sOrig, iWantLen = t
        #
        return _LopOffEnd( sOrig, sBegCode, sEndCode ).ljust( iWantLen )
    #
    lParts          = iMap( LopOffEndAddBlanks, iZip( lParts, lPartsLens ) )
    #
    return ''.join( lParts )[ : - len( sEndCode ) ]




def _blankBlockUseBeg(
        sOrigText, sBegCode = '!#', sEndCode = '$%*', sOrigLower = '' ):
    #
    from Iter.AllVers   import iMap, lMap, iZip
    from String.Split   import getPartsListAndBothStarts
    #
    lParts, lStartText, lStartSplit = \
        getPartsListAndBothStarts( sOrigText, sBegCode, sOrigLower )
    #
    if len( lParts ) <= 1: # no blocks to blank
        #
        return sOrigText
        #
    #
    if lStartSplit[0] == 0 and len( lStartSplit ) > len( lStartText ):
        #
        lStartText[0:0] = [0]
        #
    #
    iBegLen         = len( sBegCode )
    #
    lPartsLens      = [ iBegLen + t[0] - t[1] for t in iZip( lStartSplit, lStartText ) ]
    #
    lPartsLens[0]   -= iBegLen # no split char on first fragment
    #
    sPart0          = lParts[0]
    #
    def LopOffBegAddBlanks( t ):
        #
        sOrig, iWantLen = t
        #
        return _LopOffBeg( sOrig, sEndCode, sBegCode ).rjust( iWantLen )
    #
    lParts          = lMap( LopOffBegAddBlanks, iZip( lParts, lPartsLens ) )
    #
    lParts[0] = sPart0
    #
    return ''.join( lParts )



def _getBlankBlocks( sOrigText, oFinder ):
    #
    from String.Split import getIterPartsAndBothStarts
    #
    """
    getBlocksBlank( '012345!#spam$%*6789!#eggs$%*abcde!#toast$%*fghijk',
        getFinder( '(\!#)(.*?)(\$%\*)' ) )
    returns         '012345         6789         abcde          fghijk'
    """
    #
    '''
    say sOrig = 'abcdefg<table>hijklm<table>nopqrs<table>tuvwxyz'
    list( getIterPartsAndBothStarts( sOrig, getFinder( '<table>' ) ) )
    returns
    [ ('abcdefg',  0,  7),
      ('hijklm',  14, 20),
      ('nopqrs',  27, 33),
      ('tuvwxyz', 40, 47) ]
    WARNING:
    last number in last tuple is length of whole string!
    '''
    #
    iterPartBegEnd = getIterPartsAndBothStarts( sOrigText, oFinder )
    #
    lParts = []
    #
    iPriorEnd = 0
    #
    for sPart, iBeg, iEnd in iterPartBegEnd:
        #
        lParts.append( sPart.rjust( len( sPart ) + iBeg - iPriorEnd ) )
        #
        iPriorEnd = iEnd
        #
    #
    return ''.join( lParts )




def BlankBlock(
        sOrigText, sBegCode = '!#', sEndCode = '$%*', sOrigLower = '' ):
    #
    """
    BlankBlock( '012345!#spam$%*6789!#eggs$%*abcde!#toast$%*fghijk' )
    returns     '012345         6789         abcde          fghijk'
    """
    #
    # called in pGrab Text and Scripts
    #
    if len( sBegCode ) >= len( sEndCode ):
        #
        return _blankBlockUseBeg( sOrigText, sBegCode, sEndCode, sOrigLower )
        #
    else:
        #
        return _blankBlockUseEnd(  sOrigText, sBegCode, sEndCode, sOrigLower )



def getBlocksBlanked( sOrig, oFinder ):
    #
    '''
    pass original text and finder for begin/end delimiter expressions
    returns text with spaces in place of begin/end strings
    getBlocksFinder() can return finder
    example in self test code
    '''
    from re import sub
    #
    from String.Replace import getBlanksForReMatchObj
    #
    return sub( oFinder, getBlanksForReMatchObj, sOrig )


def getBlocksFinder( tDelims, bDotAll = True ):
    #
    '''
    pass tuple or list of regex begin/end delimiter expressions
    returns finder
    default is matches can cover multiple lines
    example in self test code
    '''
    #
    from String.Find import getFinder
    #
    sPattern = '|'.join( tDelims )
    #
    return getFinder( sPattern, bDotAll = bDotAll )



def _getRestAfter( sOrig, sSplitOn ):
    #
    # called in getListsTextBetween
    #
    from String.Split import SplitC
    #
    lParts  = SplitC( sOrig, sSplitOn, iMaxSplits = 1 )
    #
    if len( lParts ) == 1: return False, ''
    #
    if lParts: del lParts[ 0 ]
    #
    return True, lParts[ -1 ]



def _getBeforeOrAll( s, sBegCode ):
    #
    from String.Get import getTextBeforeC
    #
    return getTextBeforeC( s, sBegCode, bWantEmptyIfNoAfter = False )


def getListsTextBetween(
        sOrigText, sBegCode = '!#', sEndCode = '$%*', sOrigLower = '' ):
    #
    """
    returns a tuple of lists
    getListsTextBetween(
        '012345!#spam$%*6789!#eggs$%*abcde!#toast$%*fghijk',
        sBegCode = '!#',
        sEndCode = '$%*' )
    returns
    ( [  'spam', 'eggs', 'toast'],
      [      9,      9,       10],
      ['012345', '6789', 'abcde', 'fghijk'] )
    Note: to z!p lBetween and lOutsideDelims to reconstitute the original,
    one must lBetween.append( '' ) first -- or use ziplongest.
    see ReconstituteDelimiters()
    """
    #
    # called in pGrab Scripts
    #
    from Numb.Get       import getAdder
    from Iter.AllVers   import iMap, lMap, iZip
    from Collect.Get    import getSeparateKeysValues
    from Utils.Combos   import All
    
    from String.Split   import getPartsListAndBothStarts
    #
    lParts, lStartText, lStartSplit = \
        getPartsListAndBothStarts( sOrigText, sEndCode, sOrigLower )
    #
    #print 'lParts before:', lParts
    if len( lParts ) == 1: return [], [0], [sOrigText]
    #
    #if lParts: del lParts[ -1 ]
    #
    def getAfterBegCode( sOrig ): return _getRestAfter( sOrig, sBegCode )
    #
    iterFoundBegBetween= iMap( getAfterBegCode, lParts )
    #
    lFoundBeg, lBetween = getSeparateKeysValues( iterFoundBegBetween )
    #
    #print 'lFoundBeg:', lFoundBeg
    #print 'lBetween:', lBetween
    #
    if not All( lFoundBeg ): # there are sEndCodes without matching sBegCodes
        #
        lFixThese = [ i for i, b in enumerate( lFoundBeg ) if not b ]
        #
        lFixThese.reverse()
        #
        #print lFixThese
        #print lStartText
        for iFixThis in lFixThese:
            #
            if iFixThis < len( lParts ) - 1:
                #
                lParts[ iFixThis + 1 ] = \
                    lParts[ iFixThis ] + sEndCode + lParts[ iFixThis + 1 ]
                #
                del lParts[      iFixThis ]
                del lStartText[  iFixThis + 1 ]
                del lStartSplit[ iFixThis ]
            #
            del lBetween[    iFixThis ]
            #
        #
        #print 'lParts after:', lParts
        #print 'lBetween after:', lBetween
        #
    #
    iBegCodeLen     = len( sBegCode )
    iEndCodeLen     = len( sEndCode )
    #
    AddBothCodeLens = getAdder( iBegCodeLen + iEndCodeLen )
    #
    lBetLens        = lMap( AddBothCodeLens, iMap( len, lBetween ) )
    #
    lOutsideDelims  = [ _getBeforeOrAll( s, sBegCode ) for s in lParts ]
    #
    # Note: to z!p lBetween and lOutsideDelims to reconstitute the original,
    # one must lBetween.append( '' ) first.
    # see ReconstituteDelimiters()
    #
    return lBetween, lBetLens, lOutsideDelims



def getIterTextBetween( sOrigText, oFinder ):
    #
    """
    returns a tuple of lists
    maybe you are looking for getTextWithin in Get.py

    list( getIterTextBetween(
        '012345!#spam$%*6789!#eggs$%*abcde!#toast$%*fghijk',
        getFinder( '(\!#)(.*?)(\$%\*)' ) ) )
    returns
    [ ('012345', 'spam',  2,  9),
      ('6789',   'eggs',  2,  9),
      ('abcde',  'toast', 2, 10),
      ('fghijk', '',      0,  0)]
    unZip( getIterTextBetween(
        '012345!#spam$%*6789!#eggs$%*abcde!#toast$%*fghijk',
        getFinder( '(\!#)(.*?)(\$%\*)' ) )
    returns
    [ ['012345', '6789', 'abcde', 'fghijk'],
      [   'spam',  'eggs',  'toast', ''],
      [2, 2, 2, 0],
      [9, 9, 10, 0] ]
    Note: to z!p lBetween and lOutsideDelims to reconstitute the original,
    see ReconstituteDelimiters()
    """
    #
    iterMatch = oFinder.finditer( sOrigText )
    #
    iBefore = 0
    #
    for oMatch in iterMatch:
        #
        yield ( sOrigText[ iBefore : oMatch.start(0) ],
                oMatch.group(2),
                oMatch.start(2) - oMatch.start(0),
                len( oMatch.group(0) )
                )
        #
        iBefore = oMatch.start(3) + len( oMatch.group(3) )
    #
    sBefore, sBetween, iPrefixLen, iSandwichLen = (
        sOrigText[ iBefore : ], '', 0, 0 )
    #
    yield sBefore, sBetween, iPrefixLen, iSandwichLen


def _getBlanks( iLen ): return ''.ljust( iLen )


def ReconstituteDelimiters( lBetNew, lOutsideDelims ):
    #
    # Note if you want to keep the original length,
    # lBetNew members must be the the lengths in lBetLens
    # so manipulate lBetween before calling this function
    #
    from Iter.AllVers import iZipLongest
    #
    #lBetNew = list( lBetNew )
    #
    return ''.join(
        [ ''.join( t ) for t
          in iZipLongest( lOutsideDelims, lBetNew, fillvalue = '' ) ] )


_sBegDelim, _sEndDelim = '!#', '$%*'



def _getOrigSandwich( sBetween, iPrefixLen, iSandwichLen, sNext ):
    #
    return ''.join( ( _sBegDelim, sBetween, _sEndDelim, sNext ) )


def _getManipulateBetweenDelims( iter, getNewSandwich ):
    #
    from six           import next as getNext
    #
   #from Utils.Both2n3 import getNext
    #
    sThisB4, sThisBetween, iThisPrefixLen, iThisSandwichLen = getNext( iter )
    #
    yield sThisB4
    #
    for tNext in iter:
        #
        sNextB4, sNextBetween, iNextPrefixLen, iNextSandwichLen = tNext
        #
        yield getNewSandwich(
                    sThisBetween, iThisPrefixLen, iThisSandwichLen, sNextB4 )
        #
        sThisBetween, iThisPrefixLen, iThisSandwichLen = (
            sNextBetween, iNextPrefixLen, iNextSandwichLen )
        #
    #


def ReconstituteIterDelimiters( iter, getNewSandwich ):
    #
    return ''.join(
        _getManipulateBetweenDelims( iter, getNewSandwich ) )


def _doOneByOne():
    #
    from String.Text4Tests import sHTML, ttDelims
    #
    sBlanked = sHTML
    #
    for t in ttDelims:
        #
        sBeg, sEnd = t
        #
        #iLenBefor = len( sBlanked )
        #
        #QuickDump( sBlanked, 'sBefore' )
        sBlanked = BlankBlock( sBlanked, sBeg, sEnd )
        #
        #if len( sBlanked ) != iLenBefor:
            ##
            #print3( 'lost length when blanking', sBeg, sEnd )
            #break
            ##
        #if '<html>' not in sBlanked:
            ##
            #print3( 'lost HTML when blanking', sBeg, sEnd )
            #break
            #
        #
    #
    return sBlanked


def _BlankBlocksTimeTrial():
    #
    from Utils.TimeTrial import TimeTrial
    #
    from String.Text4Tests import sHTML, tWantBlanks
    #
    oFinder = getBlocksFinder( tWantBlanks )
    #
    print3( '\nBlankBlock over and over ...' )
    #
    TimeTrial( _doOneByOne )
    #
    print3( '\ngetBlocksBlanked single pass ...' )
    #
    TimeTrial( getBlocksBlanked, sHTML, oFinder )
    #
    print3( '\n_getBlankBlocks single pass ...' )
    #
    TimeTrial( _getBlankBlocks, sHTML, oFinder )
    #
    # for multiple substitutions in one pass,
    # getBlocksBlanked is the fastest
    



def _TextBetweenTimeTrial():
    #
    from String.Find     import getFinder
    from Utils.TimeTrial import TimeTrial
    #
    from String.Text4Tests import sGoogleQuerResult_Chrome as sHTML
    #
    sHtmlLower = sHTML.lower()
    #
    oFinder = getFinder( '(<script.)(.*?)(</script>)', bDotAll = True )
    #
    print3( '\ngetListsTextBetween (split the hard way) ...' )
    #
    TimeTrial( getListsTextBetween, sHTML, '<script', '</script>' )
    #
    print3( '\ngetListsTextBetween (split the easy way) ...' )
    #
    TimeTrial( getListsTextBetween,sHTML, '<script', '</script>', sHtmlLower )
    #
    print3( '\ngetIterTextBetween...' )
    #
    def getListOff( *args ): return list( getIterTextBetween( *args ) )
    #
    TimeTrial( getListOff, sHTML, oFinder ) 
    #
    # getListsTextBetween is fastest,
    # it is a little better to pass sLower if available
    




if __name__ == "__main__":
    #
    from Collect.Get    import unZip
    from File.Write     import QuickDump
    from String.Find    import getFinder
    from Utils.Result   import sayTestResult
    #
    from String.Text4Tests import sHTML, sBlanked, tWantBlanks
    #
    oFinder = getFinder( '(?:\!#)(?:.*?)(?:\$%\*)' )
    #
    lProblems = []
    #
    sOrig0      = '012345!#spam$%*6789!#eggs$%*abcde!#toast$%*fghijk'
    sOrig1      = '012345!#spam$%*6789!#eggs$%*abcde  toast$%*fghijk'
    sOrig2      = '012345!#spam$%*6789!#eggs   abcde!#toast$%*fghijk'
    sOrig3      = '012345 spam$%*6789   eggs$%*abcde  toast$%*fghijk'
    #
    tDelims = ( '!#', '$%*' )
    #
    if _blankBlockUseBeg(
            '012345!#spam$%*6789!#eggs$%*abcde!#toast$%*fghijk' ) != \
            '012345         6789         abcde          fghijk':
        #
        lProblems.append( 'BlankBlock() short trials sOrig0' )
        #
    #
    if _getBlankBlocks(
            '012345!#spam$%*6789!#eggs$%*abcde!#toast$%*fghijk', oFinder) != \
            '012345         6789         abcde          fghijk':
        #
        lProblems.append( '_getBlankBlocks() short trials sOrig0' )
        #
    #
    if _blankBlockUseBeg(
            '012345!#spam$%*6789  eggs$%*abcde!#toast$%*fghijk' ) != \
            '012345         6789  eggs$%*abcde          fghijk':
        #
        lProblems.append( 'BlankBlock() short trials' )
        #
    #
    if _blankBlockUseBeg(
            '012345!#spam$%*6789!#eggs   abcde!#toast$%*fghijk' ) != \
            '012345         6789!#eggs   abcde          fghijk':
        #
        lProblems.append( 'BlankBlock() short trials sOrig1' )
        #
    #
    if _blankBlockUseEnd(
            '012345!#spam$%*6789!#eggs$%*abcde!#toast$%*fghijk' ) != \
            '012345         6789         abcde          fghijk':
        #
        lProblems.append( 'BlankBlock() short trials sOrig0' )
        #
    #
    if _blankBlockUseEnd(
            '012345!#spam$%*6789  eggs$%*abcde!#toast$%*fghijk' ) != \
            '012345         6789  eggs$%*abcde          fghijk':
        #
        lProblems.append( 'BlankBlock() short trials' )
        #
    #
    if _blankBlockUseEnd(
            '012345!#spam$%*6789!#eggs   abcde!#toast$%*fghijk' ) != \
            '012345         6789!#eggs   abcde          fghijk':
        #
        #print '012345!#spam$%*6789!#eggs   abcde!#toast$%*fghijk'
        #print '012345         6789!#eggs   abcde          fghijk'
        #print _blankBlockUseEnd(
            #'012345!#spam$%*6789!#eggs   abcde!#toast$%*fghijk' )
        lProblems.append( 'BlankBlock() short trials sOrig2' )
        #
    #
    #sBlanked = BlankBlock( sHTML, '<span ', '>' )
    #QuickDump( sBlanked, 'sBlanked' )
    #
    oFinder = getBlocksFinder( tWantBlanks )
    #
    sBlanked = getBlocksBlanked( sHTML, oFinder )
    #
    if sBlanked != sBlanked:
        #
        print3( 'sBlanked', end=' ' )
        QuickDump( sBlanked, 'sBlanked' )
        #
        lProblems.append( 'getBlocksBlanked()' )
        #
    #
    sBlanked = _doOneByOne()
    #
    if sBlanked != sBlanked:
        #
        #print3( 'wantBlanked', end=' ' )
        #QuickDump( sBlanked, 'wantBlanked' )
        print3( 'sBlanked', end=' ' )
        QuickDump( sBlanked, 'sBlanked' )
        #
        lProblems.append( 'BlankBlock() longer html' )
        #
    #
    lBetween, lBetLens, lOutsideDelims0 = getListsTextBetween( sOrig0, *tDelims )
    #
    lBetOrig0    = [ '%s%s%s' % ( '!#',  s, '$%*' ) for s in lBetween ]
    #
    #print sOrig1
    
    lBetween, lBetLens, lOutsideDelims1 = getListsTextBetween( sOrig1, *tDelims )
    #
    if ( lBetween, lBetLens, lOutsideDelims1 ) != (
            ['spam', 'eggs'],
            [9, 9],
            ['012345', '6789', 'abcde  toast$%*fghijk'] ):
        #
        lProblems.append( 'getListsTextBetween() broken beg/end codes' )
        #
        
    #
    #print 'lBetween:', lBetween
    #print 'lBetLens:', lBetLens
    #print 'lOutsideDelims1:', lOutsideDelims1
    #
    lBetOrig1    = [ '%s%s%s' % ( '!#',  s, '$%*' ) for s in lBetween ]
    #
    lBetween, lBetLens, lOutsideDelims2 = getListsTextBetween( sOrig2, *tDelims )
    #
    lBetOrig2    = [ '%s%s%s' % ( '!#',  s, '$%*' ) for s in lBetween ]
    #
    lBetOrig3, lBetLens, lOutsideDelims3 = getListsTextBetween( sOrig3 )
    #
    if getListsTextBetween( sOrig0, *tDelims ) != \
            ( [    'spam', 'eggs', 'toast'],
                [        9,      9,     10],
                ['012345', '6789', 'abcde', 'fghijk'] ):
        #
        #print sOrig0
        #print getListsTextBetween( sOrig0, *tDelims )
        lProblems.append( 'getListsTextBetween() A' )
        #
    #
    if getListsTextBetween(
            '012345!#spam$%*6789!#eggs abcde!#toast$%*fghijk', *tDelims ) != \
            ( [    'spam',   'eggs abcde!#toast'],
                [        9,                  22],
                ['012345', '6789', 'fghijk']):
        #
        lProblems.append( 'getListsTextBetween() B' )
        #
    #
    t = getListsTextBetween(
            '012345!#spam$%*6789 eggs$%*abcde!#toast$%*fghijk', *tDelims )
    if t !=   ( [   'spam',                   'toast'], [ 9, 10 ],
           ['012345',      '6789 eggs$%*abcde',       'fghijk']):
        #
        lProblems.append( 'getListsTextBetween() C' )
        #
    #
    oFinder = getFinder( '(\!#)(.*?)(\$%\*)' )
    #
    l = unZip( getIterTextBetween(
            '012345!#spam$%*6789 eggs$%*abcde!#toast$%*fghijk', oFinder ) )
    if l != [
           ['012345',      '6789 eggs$%*abcde',       'fghijk'],
           [        'spam',                   'toast', ''],
           [ 2, 2, 0 ],
           [ 9, 10, 0 ] ]:
        #
        #print l[0] == [   'spam',                   'toast', '']
        #print l[1] == [ 9, 10, 0 ]
        #print l[2] == ['012345',      '6789 eggs$%*abcde',       'fghijk']        
        #print l[3] == [ 2, 2, 0 ]
        lProblems.append( 'getIterTextBetween() C' )
        #
    #
    #
    if ReconstituteDelimiters( lBetOrig0, lOutsideDelims0 ) != sOrig0:
        #
        lProblems.append( 'ReconstituteDelimiters() 0' )
        #
    #print lBetOrig1
    #print lOutsideDelims1
    #
    iter = getIterTextBetween( sOrig0, oFinder )
    #
    s = ReconstituteIterDelimiters( iter, _getOrigSandwich )
    #
    if s != sOrig0:
        #
        #print sOrig0
        #print s
        lProblems.append( 'ReconstituteIterDelimiters() 0' )
        #
    #
    if ReconstituteDelimiters( lBetOrig1, lOutsideDelims1 ) != sOrig1:
        #
        #print sOrig1
        #print ReconstituteDelimiters( lBetOrig1, lOutsideDelims1 )
        lProblems.append( 'getListsTextBetween() 1' )
        #
    #
    iter = getIterTextBetween( sOrig1, oFinder )
    #
    s = ReconstituteIterDelimiters( iter, _getOrigSandwich )
    #
    if s != sOrig1:
        #
        #print sOrig1
        #print s
        lProblems.append( 'ReconstituteIterDelimiters() 1' )
        #
    #
    if ReconstituteDelimiters( lBetOrig2, lOutsideDelims2 ) != sOrig2:
        #
        lProblems.append( 'getListsTextBetween() 2' )
        #
    if ReconstituteDelimiters( lBetOrig3,  lOutsideDelims3 ) != sOrig3:
        #
        lProblems.append( 'getListsTextBetween() 3' )
        #

    #
    #
    sayTestResult( lProblems )