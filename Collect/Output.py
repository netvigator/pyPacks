#!/home/rick/.local/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Collection functions Output
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
    from ..Iter.AllVers import lMap, tMap, iZip
    from ..Dict.Numbs   import getValuesAdded
    from ..Numb.Get     import getBooleanInt
    from ..Utils.Output import getSayYesOrBlank
except ( ValueError, ImportError ):
    from Iter.AllVers   import lMap, tMap, iZip
    from Dict.Numbs     import getValuesAdded
    from Numb.Get       import getBooleanInt
    from Utils.Output   import getSayYesOrBlank

def getPrintableTextFromSeq( lSeq, sNewLine = '\n', **kwargs ):
    #
    bConvert2Text = kwargs.get( 'bConvert2Text', True  )
    #
    if bConvert2Text:
        lText   = [ str( uLine ) for uLine in lSeq ]
    else:
        lText   = lSeq
    #
    return sNewLine.join( lText )


def _wipeAnds( sOrig, sHideThis ):
    #
    return sOrig.replace( sHideThis, '!@#$' )


def getTextSequence( lSeq, sSep = ', ', sAnd = 'and' ):
    #
    '''Pass this sequence: [ 'Moe', 'Larry', 'Curly' ]
    and function returns 'Moe, Larry and Curly'

    '''
    #
    sUseAnd = ' %s ' % sAnd
    #
    lUseSeq = [ _wipeAnds( s.strip(), sUseAnd ) for s in lSeq ]
    #
    sSeq = sUseAnd.join( lUseSeq )
    #
    if len( lUseSeq ) > 1:
        #
        sSeq = sSeq.replace( sUseAnd, sSep, len( lUseSeq ) - 2 )
        #
    #
    return sSeq.replace( '!@#$', sUseAnd )



def getColsUpdateTotals( *args, **kwargs ):
    #
    '''order of params must match tColHeads order!!!
    '''
    #
    tVals       = tMap( getBooleanInt, args )
    #
    tColHeads   = kwargs.get( 'tColHeads' )
    dTotals     = kwargs.get( 'dTotals' )
    getSayCol   = kwargs.get( 'getSayCol', getSayYesOrBlank )
    #
    dVals       = dict( iZip( tColHeads, tVals ) )
    #
    getValuesAdded( dTotals, dVals )
    #
    return lMap( getSayCol, tVals )


if __name__ == "__main__":
    #
    from Iter.AllVers   import iMap, iRange
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if getPrintableTextFromSeq( iRange( 10 ) ) != \
            '0\n1\n2\n3\n4\n5\n6\n7\n8\n9':
        #
        lProblems.append( 'getPrintableTextFromSeq()' )
        #
    #
    if getTextSequence( iMap( str, iRange(10) ) ) != \
            '0, 1, 2, 3, 4, 5, 6, 7, 8 and 9':
        #
        print3( getTextSequence( iMap( str, iRange(10) ) ) )
        lProblems.append( 'getTextSequence()' )
        #
    #
    l = [   'first name and overseas address',
            'first name and USA voting address',
            'date of birth', 'overseas phone number digits match',
            'same email prefix (part before "@")',
            'last and first names (almost exactly the same),',
            'overseas address city']
    #
    sSay = getTextSequence( l )
    #, sSep = '; '
    sWant = (   'first name and overseas address, '
                'first name and USA voting address, date of birth, '
                'overseas phone number digits match, '
                'same email prefix (part before "@"), '
                'last and first names (almost exactly the same), and '
                'overseas address city' )
    #
    if sSay != sWant:
        #
        print3( sSay  )
        print3( ''    )
        print3( sWant )
        lProblems.append( 'getTextSequence()' )
        #
    #
    tColHeads = ( 'spam', 'toast', 'eggs' )
    #
    dTotals     = dict.fromkeys( tColHeads, 0 )
    #
    lSayCols = getColsUpdateTotals(
                    1, 0, 1, tColHeads = tColHeads, dTotals = dTotals )
    #
    if lSayCols != ['Y', '', 'Y']:
        #
        lProblems.append( 'getColsUpdateTotals() sayCols output' )
        #
    #
    if dTotals != {'spam': 1, 'toast': 0, 'eggs': 1}:
        #
        lProblems.append( 'getColsUpdateTotals() dTotals update' )
        #
    #
    sayTestResult( lProblems )
