#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# number functions Output
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
# Copyright 2004-2011 Rick Graves
#
# ### ### ### ### ### ### ### ### ### ### ###
# ### ### ### ### ### ### ### ### ### ### ###
# ### ### ### ### ### ### ### ### ### ### ###
# ###   ReadableNo is in String.Output    ###
# ### ### ### ### ### ### ### ### ### ### ###
# ### ### ### ### ### ### ### ### ### ### ###
# ### ### ### ### ### ### ### ### ### ### ###


def getSayLessThanOne( nNumb, iWantSignificants = 2 ):
    #
    iLen        = iWantSignificants
    #
    sLen        = int( iLen )
    #
    sFormat     = '%s.%sf' % ( '%', sLen )
    #
    return sFormat % nNumb


def getSayPercentOffRatio( fRatio, iDecimals = 1, bZeroPad = False ):
    #
    from Iter.AllVers   import iMap
    from Numb.Stats import getPercent
    #
    fPC = getPercent( fRatio, iDecimals )
    #
    sFormat = '%%%s.%sf' % tuple( iMap( str, ( iDecimals + 3, iDecimals ) ) )
    #
    if bZeroPad: sFormat = '%%0%s.%sf' % tuple( iMap( str, ( iDecimals + 3, iDecimals ) ) )
    #
    sOut = '%s%%' % ( sFormat % float( fPC ) )
    #
    return sOut.strip()


def getSayPerCent( *args, **kwargs ):
    #
    if len( args ) == 2:
        #
        iTotal, iHowMany = args
        #
    else: # values inside tuple
        #
        iTotal, iHowMany = args[0]
        #
    #
    iDecimals = kwargs.get( 'iDecimals', 1 )
    bZeroPad  = kwargs.get( 'bZeroPad',  0 )
    #
    if iTotal:
        #sFormat    = '%.' + str( iDecimals ) + 'f%%'
        #sHowManyPC = sFormat % ( fHowManyPC, )
        #fHowManyPC = 100.0 * iHowMany / iTotal
        fHowManyPC = 1.0 * iHowMany / iTotal
        sHowManyPC = getSayPercentOffRatio(
                fHowManyPC, iDecimals = iDecimals, bZeroPad = bZeroPad )
    else:
        sHowManyPC = ''.join( [ '--.' ] + ( ['-'] * iDecimals ) + [ '%' ] )
    #
    return sHowManyPC


dEndings = { '1' : 'st', '2' : 'nd', '3' : 'rd' }


def sayOrdinalAsNumb( i ):
    #
    from String.Output  import ReadableNo
    #
    sNumb = ReadableNo( i )
    #
    # simulated ternary operator, with short cutting/short circuiting
    #
    sEnd = ( (  len( sNumb ) > 1 and
                sNumb[-2] == '1' and
                'th' ) or
            dEndings.get( sNumb[-1], 'th' ) )
    #
    return '%s%s' % ( sNumb, sEnd )


if __name__ == "__main__":
    #
    from Iter.AllVers   import tMap, iRange
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    Pi = 3.141592654
    #
    nDec = Pi - 3
    #
    if      getSayLessThanOne( nDec    ) != '0.14'   or \
            getSayLessThanOne( nDec, 5 ) != '0.14159':
        #
        lProblems.append( 'getSayLessThanOne()' )
        #
    #
    if getSayPercentOffRatio( .5 ) != '50.0%':
        #
        lProblems.append( 'getSayPercentOffRatio()' )
        #
    #
    if getSayPercentOffRatio( .05 ) != '5.0%':
        #
        lProblems.append( '`()' )
        #
    #
    if getSayPercentOffRatio( .05, bZeroPad = True ) != '05.0%':
        #
        lProblems.append( 'getSayPercentOffRatio()' )
        #
    #
    if getSayPerCent( 100, 49 ) != '49.0%':
        #
        lProblems.append( 'getSayPerCent() valid numbers' )
        #
    #
    if getSayPerCent( ( 100, 49 ) ) != '49.0%':
        #
        lProblems.append( 'getSayPerCent() numbers in tuple' )
        #
    #
    if getSayPerCent( 0, 10 ) != '--.-%':
        #
        lProblems.append( 'getSayPerCent() zero total' )
        #
    #
    if getSayPerCent( 100, 5, bZeroPad = True ) != '05.0%':
        #
        lProblems.append( 'getSayPercent() bZeroPad' )
        #
    #
    tOrds = (   tMap( sayOrdinalAsNumb, iRange(  1,  5 ) ),
                tMap( sayOrdinalAsNumb, iRange( 11, 15 ) ),
                tMap( sayOrdinalAsNumb, iRange( 21, 25 ) ) )
    #
    if tOrds != \
        (   ( '1st',  '2nd',  '3rd',  '4th'),
            ('11th', '12th', '13th', '14th'),
            ('21st', '22nd', '23rd', '24th') ):
        #
        lProblems.append( 'sayOrdinalAsNumb()' )
        #
    #
    #
    sayTestResult( lProblems )