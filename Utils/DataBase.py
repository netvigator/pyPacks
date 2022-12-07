#!/home/rick/.local/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Utility functions DataBase
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
# Copyright 2023 Rick Graves
#
#

from six                import print_ as print3

try:
    from ..Collect.Get  import getStringsStripTuple, getStringsStripped
    from ..Object.Get   import QuickObject
    from ..String.Find  import getRegExObj
except ( ValueError, ImportError ):
    from Collect.Get    import getStringsStripTuple, getStringsStripped
    from Object.Get     import QuickObject
    from String.Find    import getRegExObj

# must have space before or after bar "|"
oFindColumnSplits = getRegExObj( r'(?: \|)|(?:\| )' )


def getNamePositionDict( tHeader ):
    #
    '''utility for getTableFromScreenCaptureGenerator()'''
    #
    dNamePosition = {}
    #
    i = 0
    #
    for sName in tHeader:
        #
        dNamePosition[ sName ] = i
        #
        i += 1
        #
    #
    return dNamePosition




def getTableFromScreenCaptureGenerator( uScreenCapture, bListOut = False ):
    #
    fGetStrings = getStringsStripped if bListOut else getStringsStripTuple
    #
    if isinstance( uScreenCapture, str ):
        #
        oLines = uScreenCapture.split( '\n' )
        #
    else:
        #
        oLines = uScreenCapture
        #
    #
    for sLine in oLines:
        #
        uParts = fGetStrings( oFindColumnSplits.split( sLine ) )
        #
        if len( uParts ) == 1: continue
        #
        yield uParts


def _getValue( lParts, sColName, dColPositions, dConverts, setNone4Empty ):
    #
    sValue = lParts[ dColPositions[ sColName ] ]
    #
    uValue = sValue
    #
    if not sValue and sColName in setNone4Empty:
        #
        uValue = None
        #
    elif sColName in dConverts:
        #
        uValue = dConverts[ sColName ]( sValue )
        #
    #
    return uValue



def _getTableDict( oTableIter, dColPositions, sKeyName,
                    dConverts = {}, setNone4Empty = () ):
    #
    dTable = {}
    #
    for lParts in oTableIter:
        #
        uKey = None
        #
        oThis = QuickObject()
        #
        for sCol in dColPositions:
            #
            uValue = _getValue(
                    lParts, sCol, dColPositions, dConverts, setNone4Empty )
            #
            setattr( oThis, sCol, uValue )
            #
            if sCol == sKeyName: uKey = uValue
            #
        #
        dTable[ uKey ] = oThis
        #
    #
    return dTable


def getTableDict( uScreenCapture, sKeyName,
                    dConverts = {}, setNone4Empty = () ):
    #
    oTableIter      = getTableFromScreenCaptureGenerator( uScreenCapture )
    #
    tHeader         = next( oTableIter )
    #
    dColPositions   = getNamePositionDict( tHeader )
    #
    dTable          = _getTableDict( oTableIter, dColPositions, sKeyName,
                                        dConverts, setNone4Empty )
    #
    return dTable

if __name__ == "__main__":
    #
    lProblems = []
    #
    from Utils.Result   import sayTestResult
    #
    from Utils          import sMarketsTable
    from Utils.Config   import getBoolOffYesNoTrueFalse as getBool
    #
    oTableIter      = getTableFromScreenCaptureGenerator( sMarketsTable )
    #
    tHeader         = next( oTableIter )
    #
    dColPositions   = getNamePositionDict( tHeader )
    #
    tExpect = ( 'cMarket',
                'cCountry',
                'cLanguage',
                'iEbaySiteID',
                'bHasCategories',
                'iCategoryVer',
                'cCurrencyDef',
                'iUtcPlusOrMinus',
                'cUseCategoryID' )
    #
    if tHeader != tExpect:
        #
        lProblems.append( 'tHeader from getTableFromScreenCaptureGenerator()' )
        #
    #
    oTableIter      = getTableFromScreenCaptureGenerator( sMarketsTable, True )
    #
    lHeader         = next( oTableIter )
    #
    if lHeader != list( tExpect ):
        #
        lProblems.append( 'lHeader from getTableFromScreenCaptureGenerator()' )
        #
    #
    dExpect = dict(
        cMarket         = 0,
        cCountry        = 1,
        cLanguage       = 2,
        iEbaySiteID     = 3,
        bHasCategories  = 4,
        iCategoryVer    = 5,
        cCurrencyDef    = 6,
        iUtcPlusOrMinus = 7,
        cUseCategoryID  = 8 )
    #
    # print3( 'dColPositions:', dColPositions )
    if dColPositions != dExpect:
        #
        lProblems.append( 'getNamePositionDict()' )
        #
        print3( dColPositions )
    #
    dConverts = dict(
        bHasCategories  = getBool,
        iEbaySiteID     = int,
        iCategoryVer    = int,
        iUtcPlusOrMinus = int )
    #
    setNone4Empty = ( 'cUseCategoryID', )
    #
    dTable = getTableDict(
                sMarketsTable, 'iEbaySiteID', dConverts, setNone4Empty )
    #
    if len( dTable ) != 23:
        #
        lProblems.append( 'len( dTable ) problem' )
        #
        print3( dTable )
    #
    #
    oUSA = dTable[ 0 ]
    #
    if ( oUSA.cMarket       != 'EBAY-US' or
         oUSA.iCategoryVer  != 124 or
         oUSA.bHasCategories is not True or
         oUSA.cUseCategoryID is not None ):
        #
        lProblems.append( 'dTable USA value problem' )
        #
    #
    

    #
    sayTestResult( lProblems )
