#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions Quads
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

from six            import print_ as print3

from String.Output  import getZeroPadder

StrPadZero  = getZeroPadder( 3 )

def getQuadTuple( sQuad, bIsDotQuad = False, bIsHexQuad = False ):
    #
    from Iter.AllVers   import iMap
    from String.Get import getAlphaNumsOnly
    from Web.Test   import isHexQuad
    #
    if bIsDotQuad:
        #
        bHexQuad            = False
        #
    elif bIsHexQuad:
        #
        bHexQuad            = True
        #
    else:
        #
        bHexQuad            = isHexQuad( sQuad, bFormCheckOnly = True )
        #
    #
    if bHexQuad:
        #
        sQuad               = sQuad.lower()
        #
        lHexQuads           = sQuad.split( '0x' )
        #
        if len( lHexQuads ) == 5:
            #
            sQuad           = getAlphaNumsOnly( sQuad )
            #
            lHexQuads       = sQuad.split( '0x' )
            #
            lStrNos         = lHexQuads[ 1 : ]
            #
        elif '.' in sQuad:
            #
            sQuad           = sQuad.replace( '0x', '' )
            #
            lStrNos         = sQuad.split( '.' )
            #
        elif len( sQuad ) == 8:
            #
            lStrNos         = sQuad[0:2], sQuad[2:4], sQuad[4:6], sQuad[6:8]
            #
        else:
            #
            lStrNos         = [ '0' ] * 4   # could raise an error, should not be here!!!
            #
        #
        def _getInt( sNumb ): return int( sNumb, 16 )
        #
    else:
        #
        lStrNos             = sQuad.split( '.' )
        #
        _getInt = int
        #
    #
    def _getIntegers( sNumb ):
        #
        try:
            #
            iInteger    = _getInt( sNumb )
            #
        except:
            #
            iInteger    = -1
            #
        #
        return iInteger
    #
    lIntegers           = iMap( _getIntegers, lStrNos )
    #
    return tuple( lIntegers )



def getDotQuad( sMayBeDotQuad, bLocalDotQuadOK = True, bExtremesOK = True, bOverOK = False ):
    #
    from Web.Test import isDotQuadValid
    #
    if type( sMayBeDotQuad ) == type( () ): sMayBeDotQuad = sMayBeDotQuad[0:1]
    #
    if type( sMayBeDotQuad ) != str: return ''
    #
    sMayBeDotQuad = sMayBeDotQuad.split( ':' )[ 0 ] # port # on the end is OK
    #
    sMayBeDotQuad = sMayBeDotQuad.strip()
    #
    if not isDotQuadValid( sMayBeDotQuad, bLocalDotQuadOK, bExtremesOK, bOverOK ):
        #
        sMayBeDotQuad = ''
        #
    #
    return sMayBeDotQuad



def getDotQuadStripPort( sDotQuadColonPort ):
    #
    # not used anywhere yet
    #
    lParts = sDotQuadColonPort.split( ':' )
    #
    return lParts[ 0 ]


def gotDotQuadPortTupleFromString( sMayBeDotQuad ):
    #
    from Test import isDotQuadWithPort
    #
    tReturn = ( '', -1 )
    #
    if isDotQuadWithPort( sMayBeDotQuad ):
        #
        lReturn = sMayBeDotQuad.split( ':' )
        #
        tReturn = ( lReturn[0], int( lReturn[1] ) )
    #
    return tReturn



def getDotQuadPortStringFromTuple( tShouldBeIP ):
    #
    return '%s:%s' % tShouldBeIP


def gotDotQuadPortTuple( uDotQuadPort ):
    #
    if type( uDotQuadPort ) == tuple:
        #
        tDotQuadPort = uDotQuadPort
        #
    else:
        #
        tDotQuadPort = gotDotQuadPortTupleFromString( uDotQuadPort )
        #
    #
    return tDotQuadPort


def getDotQuadsWithPorts( sStuff ):
    #
    # not used anywhere yet
    #
    from Iter.AllVers import tFilter
    from Web.Test import isDotQuadPortAfterCleanup
    #
    lFrags = sStuff.split()
    #
    return tFilter( isDotQuadPortAfterCleanup, lFrags )



def getDomainNameOrDotQuadWithPort( sMayBe ):
    #
    from Test import isDomainNameOrDotQuadWithPort
    #
    tReturn = ( '', -1 )
    #
    sMayBe = sMayBe.strip()
    #
    if isDomainNameOrDotQuadWithPort( sMayBe ):
        #
        lReturn = sMayBe.split( ':' )
        #
        tReturn = ( lReturn[0], int( lReturn[1] ) )
    #
    return tReturn




def getQuadValue( uDotQuad, bIsDotQuad = False, bIsHexQuad = False ):
    #
    if type( uDotQuad ) == str:
        #
        liBits  = getQuadTuple( uDotQuad, bIsDotQuad = bIsDotQuad, bIsHexQuad = bIsHexQuad )
        #
    else:
        #
        liBits  = uDotQuad
        #
    #
    iValue = iBitsLen = -1
    #
    try:
        iBitsLen = len( liBits )
    except:
        pass
    #
    if iBitsLen == 4:
        #
        iValue      =   ( liBits[0] * 256**3 ) + \
                        ( liBits[1] * 256**2 ) + \
                        ( liBits[2] * 256    ) + \
                          liBits[3]
    #
    return iValue



def getDotQuadFromDotQuadTuple( tDotQuad ):
    #
    from Iter.AllVers import iMap
    #
    lDotQuad    = iMap( str, tDotQuad )
    #
    return '.'.join( lDotQuad )


def getDotQuadFromValue( iValue ):
    #
    from Iter.AllVers import lRange
    #
    lBits       = lRange( 4 )
    #
    lBits.reverse()
    #
    lQuads      = lBits[:]
    #
    for iBit in lBits: # [3, 2, 1, 0]
        #
        iThis               = iValue // ( 256 ** iBit )
        #
        lQuads[ 3 - iBit ]  = iThis
        #
        iValue              -= iThis * 256 ** iBit
        #
    #
    return getDotQuadFromDotQuadTuple( lQuads )





def getDotQuadFromHexQuad( sHexQuad ):
    #
    iAddress    = getQuadValue( sHexQuad, bIsHexQuad = True )
    #
    return getDotQuadFromValue( iAddress )









def _getNextDotQuad( sDotQuad, iIncrement = 1 ):
    #
    iValue      = getQuadValue( sDotQuad, bIsDotQuad = True )
    #
    return getDotQuadFromValue( iValue + iIncrement )



def _getPriorDotQuad( sDotQuad, iIncrement = None ):
    #
    if iIncrement is None:
        #
        iIncrement = -1
        #
    elif iIncrement > 0:
        #
        iIncrement = - iIncrement
        #
    return _getNextDotQuad( sDotQuad, iIncrement )



def getClassCNetBegEnd( sDotQuad ):
    #
    lsBits      = list( getQuadTuple( sDotQuad ) )
    #
    lsBits[-1]  = 0
    #
    sBeg        = getDotQuadFromDotQuadTuple( lsBits )
    #
    lsBits[-1]  = 255
    #
    return sBeg, getDotQuadFromDotQuadTuple( lsBits )



def getOutsideClassCNet( sDotQuad ):
    #
    # not used anywhere yet
    #
    sBeg, sEnd = getClassCNetBegEnd( sDotQuad )
    #
    return _getPriorDotQuad( sBeg ), _getNextDotQuad( sEnd )



def getClassCNetRangeBegEnd( sBeg, sEnd ):
    #
    """
    this returns
    * the start dot quad for the class C net for sBeg, and
    * the end   dot quad for the class C net for sEnd.
    so the returned sBeg & sEnd will be from different class C nets if
    the sBeg & sEnd arguments coming in are from different class C nets.
    """
    #
    if getQuadValue( sBeg ) > getQuadValue( sEnd ):
        #
        sEnd, sBeg  = sBeg, sEnd
        #
    #
    sBeg, sTrowAway = getClassCNetBegEnd( sBeg )
    sTrowAway, sEnd = getClassCNetBegEnd( sEnd )
    #
    return sBeg, sEnd



def getClassCBeg( sDotQuad ):
    #
    sBeg, sEnd = getClassCNetBegEnd( sDotQuad )
    #
    return sBeg




def getDotQuadPadR( sDotQuad ):
    #
    return sDotQuad.ljust( 15 )



def getDotQuad4Sort( sDotQuad ):
    #
    #!# coverting to an integer may be better for storting
    #
    from Iter.AllVers import iMap
    #
    sPort = ''
    #
    lDotQuadPort = sDotQuad.split(':')
    #
    if len( lDotQuadPort ) > 1:
        #
        sPort = lDotQuadPort[ 1 ]
        #
    #
    # accomodating an unusual case -- a range in the form sDotQuad01-sDotQuad02
    #
    lDotQuads    = sDotQuad.split('-')
    #
    sDotQuad     = lDotQuads[0]
    #
    sDotQuad     = getDotQuad( sDotQuad, bOverOK = True, bExtremesOK = True )
    #
    lsBits       = sDotQuad.split( '.' )
    #
    lsBits       = iMap( StrPadZero, lsBits )
    #
    lDotQuads[0] = '.'.join( lsBits )
    #
    sDotQuad     = '-'.join( lDotQuads )
    #
    if sPort:
        #
        sDotQuad += ':' + sPort.zfill( 5 )
        #
    #
    #
    return sDotQuad


def getDotQuadFromDotQuad4Sort( sDotQuad ):
    #
    tDotQuad    = getQuadTuple( sDotQuad, bIsDotQuad = True )
    #
    return getDotQuadFromDotQuadTuple( tDotQuad )


def getDotQuad4SortFromValue( iDotQuad ):
    #
    return getDotQuad4Sort( getDotQuadFromValue( iDotQuad ) )


def getHexQuadFromDotQuad( sQuad, sSeparator = '', bRemove0x = True ):
    #
    # not used anywhere yet
    #
    from Iter.AllVers import iMap
    from Utils.Both2n3 import getZeroFilled
    #
    tQuad   = getQuadTuple( sQuad, bIsDotQuad = True )
    #
    if bRemove0x and sSeparator == '':
        #
        def getHex( i ): return getZeroFilled( hex( i )[ 2 : ], 2 )
        #
    elif bRemove0x :
        #
        def getHex( i ): return hex( i )[ 2 : ]
        #
    else:
        #
        def getHex( i ): return hex( i )
        #
    #
    lHex    = iMap( getHex, tQuad )
    #
    return sSeparator.join( lHex )


def getDotQuadFromHexQuad( sQuad ):
    #
    from Iter.AllVers import iMap
    #
    tQuad   = getQuadTuple( sQuad, bIsHexQuad = True )
    #
    return '.'.join( iMap( str, tQuad ) )




if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #

    if      getQuadTuple('192.168.0.1')     != (192, 168, 0, 1) or \
            getQuadTuple('0xc00xa80x00x1')  != (192, 168, 0, 1) or \
            getQuadTuple('c0a80001')        != (192, 168, 0, 1):
        #
        lProblems.append( 'getQuadTuple()' )
        #
    if      getDotQuad('192.168.0.1:80')    != '192.168.0.1' or \
            getDotQuad('192.168.0.1:80',0  )!= ''            or \
            getDotQuad('192.168.0.0:80',1,0)!= ''            or \
            getDotQuad('192.168.0.0:80',1,1)!= '192.168.0.0':
        #
        # getDotQuad(
        #  sMayBeDotQuad, bLocalDotQuadOK = True, bExtremesOK = True, bOverOK = False ):
        #
        lProblems.append( 'getDotQuad()' )
        #
    if      getDotQuadStripPort( '192.168.0.1'    ) != '192.168.0.1' or \
            getDotQuadStripPort( '192.168.0.1:80' ) != '192.168.0.1':
        #
        lProblems.append( 'getDotQuadStripPort()' )
        #
    if gotDotQuadPortTupleFromString('192.168.0.1:80') != ('192.168.0.1',80):
        #
        lProblems.append( 'gotDotQuadPortTupleFromString()' )
        #
    if getDotQuadPortStringFromTuple( ('192.168.0.1',80) ) != '192.168.0.1:80':
        #
        lProblems.append( 'getDotQuadPortStringFromTuple()' )
        #
    if      gotDotQuadPortTuple(  '192.168.0.1:80'  ) != ('192.168.0.1',80) or \
            gotDotQuadPortTuple( ('192.168.0.1',80) ) != ('192.168.0.1',80):
        #
        lProblems.append( 'gotDotQuadPortTuple()' )
        #
    #
    sStuff = '''How now brown cow.
        192.168.0.1:80
        We are having spam, eggs and toast for breakfast.
        www.python.org:443
        Mary had a little lamb.
    '''
    #
    if getDotQuadsWithPorts( sStuff ) != ('192.168.0.1:80',):
        #
        lProblems.append( 'getDotQuadsWithPorts()' )
        #
    if      getDomainNameOrDotQuadWithPort(
                '192.168.0.1:80'     ) != ('192.168.0.1', 80)     or \
            getDomainNameOrDotQuadWithPort(
                'www.python.org:443' ) != ('www.python.org', 443) or \
            getDomainNameOrDotQuadWithPort(
                'How now brown cow.' ) != ('', -1):
        #
        lProblems.append( 'getDomainNameOrDotQuadWithPort()' )
        #
    if      getQuadValue( '255.255.255.255' ) !=  4294967295 or \
            getQuadValue( '000.255.255.255' ) !=    16777215 or \
            getQuadValue( '000.000.255.255' ) !=       65535 or \
            getQuadValue( '000.000.000.255' ) !=         255 or \
            getQuadValue( '000.000.000.001' ) !=           1 or \
            getQuadValue( '192.168.000.001' ) !=  3232235521 or \
            getQuadValue( '0xc00xa80x00x01' ) !=  3232235521:
        #
        lProblems.append( 'getQuadValue()' )
        #
    if getDotQuadFromDotQuadTuple( (192, 168, 0, 1) ) != '192.168.0.1':
        #
        lProblems.append( 'getDotQuadFromDotQuadTuple()' )
        #
    if getDotQuadFromValue( 3232235521 ) != '192.168.0.1':
        #
        print3( 'getDotQuadFromValue( 3232235521 ):', getDotQuadFromValue( 3232235521 ) )
        lProblems.append( 'getDotQuadFromValue()' )
        #
    #
    if getDotQuadFromHexQuad( '0xc00xa80x00x01' ) != '192.168.0.1':
        #
        lProblems.append( 'getDotQuadFromHexQuad()' )
        #
    if      _getNextDotQuad( '192.168.000.001'     ) != '192.168.0.2' or \
            _getNextDotQuad( '192.168.000.001', -2 ) != '192.167.255.255':
        #
        lProblems.append( '_getNextDotQuad()' )
        #
    if _getPriorDotQuad( '192.168.000.00' ) != '192.167.255.255':
        #
        lProblems.append( '_getPriorDotQuad()' )
        #
    if getClassCNetBegEnd( '192.168.0.188' ) != \
            ('192.168.0.0', '192.168.0.255'):
        #
        lProblems.append( 'ClassCNet()' )
        #
    if getOutsideClassCNet( '192.168.0.188' ) != \
            ('192.167.255.255', '192.168.1.0'):
        #
        lProblems.append( 'getOutsideClassCNet()' )
        #
    if getClassCNetRangeBegEnd( '192.168.0.188', '192.168.18.188' ) != \
            ('192.168.0.0', '192.168.18.255'):
        #
        lProblems.append( 'getClassCNetRangeBegEnd()' )
        #
    if getClassCBeg( '192.168.0.188' ) != '192.168.0.0':
        #
        lProblems.append( 'getClassCBeg()' )
        #
    if getDotQuadPadR( '192.168.0.188' ) != '192.168.0.188  ':
        #
        lProblems.append( 'getDotQuadPadR()' )
        #
    if getDotQuad4Sort( '192.168.0.18' ) != '192.168.000.018':
        #
        lProblems.append( 'getDotQuad4Sort()' )
        #
    if getDotQuadFromDotQuad4Sort( '192.168.000.018' ) != '192.168.0.18':
        #
        lProblems.append( 'getDotQuadFromDotQuad4Sort()' )
        #
    if getDotQuad4SortFromValue( 3232235521 ) != '192.168.000.001':
        #
        lProblems.append( 'getDotQuad4SortFromValue()' )
        #
    if      getHexQuadFromDotQuad(
                '192.168.0.188', sSeparator = '.', bRemove0x = True ) != \
                    'c0.a8.0.bc' or \
            getHexQuadFromDotQuad(
                '192.168.0.188', sSeparator = '',  bRemove0x = False ) != \
                    '0xc00xa80x00xbc':
        #
        lProblems.append( 'getHexQuadFromDotQuad()' )
        #
    if      getDotQuadFromHexQuad( 'c0.a8.0.bc'     ) != '192.168.0.188' or \
            getDotQuadFromHexQuad( '0xc00xa80x00xbc') != '192.168.0.188':
        #
        lProblems.append( 'getDotQuadFromHexQuad()' )
        #

    
    #
    sayTestResult( lProblems )