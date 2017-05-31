#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Numb functions Convert
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

from six import print_ as print3


def _getKeepDotsDigits():
    #
    from String.Dumpster import KeepDotsDigitsClass
    #
    oKeepDotsDigits = KeepDotsDigitsClass()
    #
    return oKeepDotsDigits

oKeepDotsDigits = _getKeepDotsDigits()



def getNumberFromUncleanString( s ):
    #
    from String.Test import hasAnyDigits
    #
    sNumber = oKeepDotsDigits.Dump( s ).split()[ 0 ]
    #
    if not sNumber or not hasAnyDigits( sNumber ):
        return None
    elif '.' in sNumber:
        return float( sNumber )
    else:
        return int( sNumber )


def _getDicts():
    #
    dNumberWords = dict(
        one         = 1,
        two         = 2,
        three       = 3,
        four        = 4,
        five        = 5,
        six         = 6,
        seven       = 7,
        eight       = 8,
        nine        = 9,
        ten         = 10,
        eleven      = 11,
        twelve      = 12,
        thirteen    = 13,
        forteen     = 14,
        fourteen    = 14,
        fifteen     = 15,
        sixteen     = 16,
        seventeen   = 17,
        eighteen    = 18,
        nineteen    = 19,
        twenty      = 20,
        thirty      = 30,
        forty       = 40,
        fifty       = 50,
        sixty       = 60,
        seventy     = 70,
        eighty      = 80,
        ninety      = 90 )

    dMultipliers = dict(
        hundred     = 100,
        thousand    = 1000,
        million     = 1000000,
        trillion    = 1000000000,
        billion     = 1000000000000 )
    #
    return dNumberWords, dMultipliers

dNumberWords, dMultipliers = _getDicts()


def _getNumberWordFinder():
    #
    from String.Find    import getFinderFindAll
    from Dict.Get       import getKeyList, getKeyIter
    #
    lPattern = getKeyList( dNumberWords )
    #
    lPattern.extend( getKeyIter( dMultipliers ) )
    #
    lPattern.append( r'\d+' )
    #
    lPattern = [ r'\b%s\b' % sNumber for sNumber in lPattern ]
    #
    sPattern = '|'.join( lPattern )
    #
    return getFinderFindAll( sPattern )

getNumberWords = _getNumberWordFinder()


def _getMultiplierFinder():
    #
    from String.Find    import getFinder
    from Dict.Get       import getKeyIter
    #
    sPattern = '|'.join(
            [   r'\b%s\b' % sNumber
                for sNumber
                in getKeyIter( dMultipliers ) ] )
    #
    return getFinder( sPattern )

_oMultiplierFinder = _getMultiplierFinder()


def getNumberOffWord( sWord ):
    #
    iNumb = None
    #
    if sWord.isdigit():
        iNumb = int( sWord )
    else:
        iNumb = dNumberWords.get( sWord.lower() ) # returns None if not found
    #
    return iNumb


def getMultiplierOffWord( sWord ):
    #
    return dMultipliers.get( sWord.lower() ) # returns None if not found



def getNumberOffWords( sWords ):
    #
    from Iter.AllVers import iMap, lMap, tMap, iZip
    from Numb.Get import getSum, pairMultiply
    #
    lMultipliers = _oMultiplierFinder.findall( sWords )
    #
    if lMultipliers:
        #
        lParts = _oMultiplierFinder.split( sWords )
        #
    else:
        #
        lParts = [ sWords ]
        #
    #
    iNumberLists = iMap( getSum,
                         [ tMap( getNumberOffWord, s )
                           for s
                           in iMap( getNumberWords, lParts ) ] )
    #
    lMultiplierLists = [ getMultiplierOffWord( s ) for s in lMultipliers ]
    #
    lMultiplierLists.append( 1 )
    #
    lNumbMultis = iZip( iNumberLists, lMultiplierLists )
    #
    lSegments = [ pairMultiply( *t ) for t in lNumbMultis ]
    #
    return getSum( lSegments )



def _getSayWordDicts():
    #
    from Dict.Get import getReverseDict
    from Iter.AllVers import lMap
    #
    return lMap( getReverseDict, ( dNumberWords, dMultipliers ) )

dNumberSayWord, dMultiSayWord = _getSayWordDicts()




def _getRomanDictOrdered():
    #
    from collections import OrderedDict
    #
    dIntRoman = OrderedDict()
    #
    dIntRoman[1000] = "M"
    dIntRoman[900] = "CM"
    dIntRoman[500] = "D"
    dIntRoman[400] = "CD"
    dIntRoman[100] = "C"
    dIntRoman[90] = "XC"
    dIntRoman[50] = "L"
    dIntRoman[40] = "XL"
    dIntRoman[10] = "X"
    dIntRoman[9] = "IX"
    dIntRoman[5] = "V"
    dIntRoman[4] = "IV"
    dIntRoman[1] = "I"
    #
    return dIntRoman

_dIntRomanOrder = _getRomanDictOrdered()


def _getRomanDict():
    #
    from Dict.Get import getReverseDictGotUniqueItems
    #
    return getReverseDictGotUniqueItems(
        dict(
            M   = 1000,
            CM  =  900,
            D   =  500,
            CD  =  400,
            C   =  100,
            XC  =   90,
            L   =   50,
            XL  =   40,
            X   =   10,
            IX  =    9,
            V   =    5,
            IV  =    4,
            I   =    1 ) )


_tRoman = ( 1000,900,500,400,100,90,50,40,10,9,5,4,1 )


from bisect import bisect


def _getRomanOffIntTest( iNum, iStart = 0 ):
    #
    from Iter.AllVers import iRange
    #
    for i in iRange( iStart, len( _tRoman ) ):
        #
        iKey = _tRoman[ i ]
        #
        if iKey > iNum: continue
        #
        iQuotient = iNum // iKey
        #
        yield _dIntRomanOrder[ iKey ] * iQuotient
        #
        iNum -= ( iKey * iQuotient )
        #
        # print3( 'remainder ', iNum )
        #
        if iNum > 0:
            #
            _getRomanOffIntTest( iNum, i + 1 )
            #
        else:
            #
            break
    #
    
    

def _getRomanOffIntOrig( iNum ):
    #
    # print3( 'passed ', iNum )
    #
    for iKey in _dIntRomanOrder:
        #
        # if iKey > iNum: continue
        #
        iQuotient = iNum // iKey
        #
        yield _dIntRomanOrder[ iKey ] * iQuotient
        #
        iNum -= ( iKey * iQuotient )
        #
        # print3( 'remainder ', iNum )
        #
        if iNum > 0:
            #
            _getRomanOffIntOrig( iNum )
            #
        else:
            #
            break



def getRomanNumeralOffIntSlower( iPassed ):
    #
    return ''.join( _getRomanOffIntOrig( iPassed ) )


def getRomanNumeralOffInt( iNum ):
    #
    lRomanNumerals = []
    #
    for iKey in _dIntRomanOrder:
        #
        if iKey > iNum: continue
        #
        iQuotient = iNum // iKey
        #
        lRomanNumerals.append( _dIntRomanOrder[ iKey ] * iQuotient )
        #
        iNum -= ( iKey * iQuotient )
        #
        if not iNum: break
        #
    #
    return ''.join( lRomanNumerals )




def _RomanNumeralConversionTimeTrial():
    #
    from Iter.AllVers     import tMap
    from Utils.TimeTrial  import TimeTrial
    #
    tTestVals = ( 69, 88, 153, 286, 386, 486, 500, 555, 1888, 1959, 2016 )
    #
    def testImproved(): return tMap( getRomanNumeralOffInt, tTestVals )
    #
    print3( testImproved() )
    #
    print3( '\nusing getRomanNumeralOffInt ...' )
    #
    TimeTrial( testImproved )
    #
    def testSlower(): return tMap( getRomanNumeralOffIntSlower, tTestVals )
    #
    print3( '\nusing getRomanNumeralOffIntSlower ...' )
    #
    TimeTrial( testSlower )



if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if      getNumberFromUncleanString( ' abcde 8.8 jasls' ) != 8.8 or \
            getNumberFromUncleanString( ' abcde   . jasls' ):
        #
        lProblems.append( 'getNumberFromUncleanString()' )
        #
    #
    sWords = 'In fourteen hundred and ninety-three, Columbus sailed the deep blue sea.'
    #
    if getNumberWords( sWords ) != ['fourteen', 'hundred', 'ninety', 'three']:
        #
        lProblems.append( 'getNumberWords() words only' )
        #
    #
    sWords = 'In 14 hundred and ninety-3, Columbus sailed the deep blue sea.'
    #
    if getNumberWords( sWords ) != ['14', 'hundred', 'ninety', '3']:
        #
        lProblems.append( 'getNumberWords() words and digits' )
        #
    #
    sWords = 'In fourteen hundred and ninety-three, Columbus sailed the deep blue sea.'
    #
    if getNumberOffWords( sWords ) != 1493:
        #
        lProblems.append( 'getNumberOffWords() words only' )
        #
    #
    sWords = 'In 14 hundred and ninety-3, Columbus sailed the deep blue sea.'
    #
    if getNumberOffWords( sWords ) != 1493:
        #
        lProblems.append( 'getNumberOffWords() words and digits' )
        #
    #
    iArabic = 69
    #
    if getRomanNumeralOffInt( iArabic ) != 'LXIX':
        #
        lProblems.append( 'getRomanNumeralOffInt( %s ) returns %s' %
                            ( iArabic, getRomanNumeralOffIntSlower( iArabic ) ) )
        #
    #
    iArabic = 200
    #
    if getRomanNumeralOffInt( iArabic ) != 'CC':
        #
        lProblems.append( 'getRomanNumeralOffInt( %s ) returns %s' %
                            ( iArabic, getRomanNumeralOffIntSlower( iArabic ) ) )
        #
    #
    iArabic = 2016
    #
    if getRomanNumeralOffInt( iArabic ) != 'MMXVI':
        #
        lProblems.append( 'getRomanNumeralOffInt( %s ) returns %s' %
                            ( iArabic, getRomanNumeralOffIntSlower( iArabic ) ) )
        #
    #
    #
    sayTestResult( lProblems )