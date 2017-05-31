#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# string functions Outputs
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

from String.Transform import getSwapper


def ReadableNo( nNumb, iRtJustLen = 0, iWantDecimals=0 ):
    #
    if type( nNumb ) == str:
        #
        sNumb       = nNumb.strip()
        #
    else:
        #
        sNumb       = '%f' % nNumb
        #
    #
    sDecimals       = ''
    #
    if iWantDecimals > 0:
        #
        if '.' not in sNumb:
            #
            sNumb   += '.'
            #
        sNumb       += '0' * iWantDecimals
        #
        sNumb       =  sNumb[ : sNumb.find( '.' ) + iWantDecimals + 1 ]
        #
        sDecimals   =  sNumb[ sNumb.find( '.' ) : ]
        #
        sNumb       =  sNumb[ : sNumb.find( '.' ) ]
        #
    else:
        #
        if '.' in sNumb: sNumb = sNumb[ : sNumb.find('.') ]
        #
    #
    lNumbs          = list( sNumb )
    #
    lNumbs.reverse()
    #
    iCount          = 0
    #
    lDigits         = []
    #
    for sThisDigit in lNumbs:
        #
        lDigits.append( sThisDigit )
        #
        iCount      += 1
        #
        if iCount % 3 == 0:
            #
            lDigits.append( ',' )
            #
        #
    #
    sReadableNo     = ''
    #
    lDigits.reverse()
    #
    sReadableNo = ''.join( lDigits )
    #
    if len( sReadableNo ) > 1 and sReadableNo[ 0 ] == ',':
        #
        sReadableNo = sReadableNo[ 1 : ]
    #
    sReadableNo = sReadableNo + sDecimals
    #
    if iRtJustLen: sReadableNo = sReadableNo.rjust( iRtJustLen )
    #
    return sReadableNo



def Plural( iQty, sPlural = 's', sSingular = '' ):
    #
    from Utils.ImIf   import ImIf
    #
    return ImIf( iQty == 1, sSingular, sPlural )



def StrPadZero( uBase, iWantLen ): return str(uBase).zfill( iWantLen )


def getZeroPadder( iWantLen ):
    #
    def ZeroPadder( uBase ): return StrPadZero( uBase, iWantLen )
    #
    return ZeroPadder



dTitleReplace = {
    " And "         :   " and ",
    " And\b"        :   " and\n",
    " Of The "      :   " of the ",
    " And The "     :   " and the ",
    "'S "           :   "'s ",
    " Of\b"         :   " of\n",
    " Of "          :   " of ",
    " D'"           :   " d'",
    " The "         :   " the ",
    " The\b"        :   " the" }


def oldBetterTitle( sTitleize ):
    #
    from Replace import ReplaceManyOldWithManyNew
    #
    sTitleize   = sTitleize.title()
    #
    sTitleize   = ReplaceManyOldWithManyNew( sTitleize, dTitleReplace )
    #
    return sTitleize


getBetter = getSwapper( dTitleReplace, bIgnoreCase = True, bEscape = False )

def BetterTitle( sTitleize ):
    #
    return getBetter( sTitleize.title() )





def SayNone( u ):
    #
    if u is None: u = 'None'
    #
    return u


# def getTextMakeParagraphs( sText ): see Paragraph.py



def getPercentStr( iSome, iTotal, iDecimals = 1 ):
    #
    if iSome == iTotal:
        #
        sPerCent    = '100'
        #
    else:
        #
        fPerCent    = 100 * iSome / float( iTotal )
        #
        iWhole      = iDecimals + 3
        #
        sFormat     = "%-" + str( iWhole ) + '.' + str( iDecimals ) + "f"
        #
        sPerCent    = sFormat % fPerCent
        #
        sPerCent    = sPerCent.rstrip()
        #
    #
    sPerCent += '%'
    #
    return sPerCent



def show_re( sPattern, sString ):
    #
    """
    Try show_re( sPattern, sString ) to show what re matches.
    """
    #
    from six    import print_ as print3
    #
    from re     import compile as REcompile, MULTILINE
    #
    print3( '\n', REcompile( sPattern, MULTILINE ).sub("{\g<0>}", sString.rstrip() ) )


def WordWrapText( s, iMaxLen = 72 ):
    #
    from Iter.AllVers import lMap, iRange, lRange
    #
    lLinesCRLF          = s.split( '\r\n' ) # Microsoft
    lLinesNewL          = s.split(   '\n' ) # Unix/Linux
    #
    if len( lLinesNewL ) > len( lLinesCRLF ):
        #
        lLines          = lLinesNewL
        sBreak          = '\n'
        #
    else:
        #
        lLines          = lLinesCRLF
        sBreak          = '\r\n'
        #
    #
    lDoLines            = lRange( len( lLines ) )
    #
    lDoLines.reverse()
    #
    def getLenPlusOne( s ): return len( s ) + 1
    #
    for iLine in lDoLines:
        #
        if len( lLines[iLine] ) > iMaxLen:
            #
            lParts      = lLines[iLine].split( ' ' )
            #
            lLens       = lMap( getLenPlusOne, lParts )
            #
            lInserts    = []
            #
            while lParts:
                #
                iLineLen    = 0
                iWantParts  = 0
                #
                iWantParts  = len( lParts ) + 1
                #
                for iPart in iRange( len( lParts ) ):
                    #
                    iLineLen += lLens[ iPart ]
                    #
                    if iLineLen > iMaxLen:
                        #
                        iWantParts  = iPart
                        #
                        break
                    #
                #
                iWantParts  = max( iWantParts, 1 )
                #
                lInserts.append( ' '.join( lParts[ : iWantParts ] ) )
                #
                del lParts[ : iWantParts ]
                del lLens[  : iWantParts ]
                #
                #lParts      = lParts[ iWantParts : ]
                #lLens       = lLens[  iWantParts : ]
                #
            #
            lLines[ iLine : iLine + 1 ] = lInserts
            #
        #
    #
    return sBreak.join( lLines )




def getCommaDelimited( *args, **kwargs ):
    #
    from Iter.AllVers import iMap
    #
    if 'sTerminatorField' in kwargs:
        sTerminatorField = kwargs['sTerminatorField']
    else:
        sTerminatorField = ','
    #
    if 'sTerminatorLine' in kwargs:
        sTerminatorLine = kwargs['sTerminatorLine']
    else:
        sTerminatorLine = '\n'
    #
    l = iMap( str, args )
    #
    return '%s%s' % ( sTerminatorField.join( l ), sTerminatorLine )


if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    from string import digits
    from string import ascii_letters   as letters
    from string import ascii_lowercase as lowercase
    from string import ascii_uppercase as uppercase
    #
    lProblems = []
    #
    i = 9876543210
    #
    if ReadableNo( i ) != '9,876,543,210':
        #
        lProblems.append( 'ReadableNo()' )
        #
    #
    if ReadableNo( i, 15 ) != '  9,876,543,210':
        #
        lProblems.append( 'ReadableNo() rjust' )
        #
    #
    if Plural( i, 'are lots', 'is one' ) != 'are lots':
        #
        lProblems.append( 'Plural()' )
        #
    if StrPadZero( 1, 8 ) != '00000001':
        #
        lProblems.append( 'StrPadZero()' )
        #
    #
    oZeroPadder = getZeroPadder( 8 )
    #
    if oZeroPadder( 1 ) != '00000001':
        #
        lProblems.append( 'getZeroPadder()' )
        #
    if BetterTitle( 'a tale of two cities' ) != 'A Tale of Two Cities':
        #
        lProblems.append( 'BetterTitle()' )
        #
    if SayNone( None ) != 'None':
        #
        lProblems.append( 'SayNone()' )
        #
    #
    if getPercentStr( 48, 100, 2 ) != '48.00%':
        #
        lProblems.append( 'getPercentStr()' )
        #
    #
    if getCommaDelimited( 'x', 8, 'z' ) != 'x,8,z\n':
        #
        lProblems.append( 'getCommaDelimited()' )
        #
    #
    sayTestResult( lProblems )