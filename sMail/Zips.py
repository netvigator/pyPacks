#!/home/rick/.local/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Mail functions Abbreviations
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
# Copyright 2010-2023 Rick Graves
#

'''
'''
from sMail          import dZipRange4State, dApoZipCountry
from sMail.Abbrev   import getCodeGotState
from Dict.Get       import getItemIter



dZipRange4Code = dict(
      [ ( getCodeGotState( t[0] ), t[1] )
        for t
        in getItemIter( dZipRange4State ) ] )

del dZipRange4Code[ '' ]




def _getMinMax( d ):
    #
    return d['min'], d['max']

lZipRangeMinMaxCode = []

#
def _getZipRefLists():
    #
    from Collect.Get    import unZip
    from Iter.AllVers   import tMap
    #
    for t in getItemIter( dZipRange4Code ):
        #
        sStateCode, d = t
        #
        sMin, sMax = _getMinMax( d )
        #
        lZipRangeMinMaxCode.append( ( sMin, sMax, sStateCode ) )
        #
        if 'more' in d:
            #
            for d in d['more']:
                #
                sMin, sMax = _getMinMax( d )
                #
                lZipRangeMinMaxCode.append( ( sMin, sMax, sStateCode ) )
                #
            #
        #
    #
    lZipRangeMinMaxCode.sort()
    #
    lMinMins,  lMinMaxes, lMinStates = unZip( lZipRangeMinMaxCode )
    #
    return tMap( tuple,
          ( lZipRangeMinMaxCode,
            lMinMins,
            lMinMaxes ) )

( _tZipRangeMinMaxCode,
  _tMinMins,
  _tMinMaxes ) = _getZipRefLists()


def getStateGotZip( sZip ):
    #
    from bisect import bisect_left
    #
    from sMail.Test import isZipPlus4
    #
    if isZipPlus4( sZip ): sZip = sZip[ : 5 ]
    #
    iStartAt = bisect_left( _tMinMins, sZip )
    #
    if iStartAt > len( _tMinMins ) - 1: iStartAt = len( _tMinMins ) - 1
    #
    while iStartAt > 0:
        #
        if _tMinMins[ iStartAt ] > sZip:
            #
            iStartAt = iStartAt - 1
            #
        else:
            #
            break
            #
        #
    #
    iThis = max( iStartAt - 1, 0 )
    #
    lHits = []
    #
    while sZip >= _tMinMins[ iThis ]:
        #
        if sZip <= _tMinMaxes[ iThis ]:
            #
            lHits.append( lZipRangeMinMaxCode[ iThis ] )
            #
        #
        iThis += 1
        #
        if iThis == len( _tMinMins ): break
    #
    sStateCode = ''
    #
    if len( lHits ) == 1:
        #
        sStateCode = lHits[0][2]
        #
    elif len( lHits ) > 1:
        #
        lByRange = [ ( int(t[1]) - int(t[0]), t )  for t in lHits ]
        #
        lByRange.sort()
        #
        sStateCode = lByRange[0][1][2]
        #
    #
    return sStateCode
            
        



def putZerosBackInFront( sZip ):
    #
    '''
    putZerosBackInFront puts the dropped zero back
    pass 9824, returns 09824
    '''
    #
    if sZip and len( sZip ) < 5 and sZip.isdigit():
        #
        sZip = '%05d' % int( sZip )
    #
    return sZip


def getApoCountryOffZip( sZip ):
    #
    from sMail.Get  import getZip5GotZipPlus4
    from sMail.Test import isZipPlus4
    #
    if isZipPlus4( sZip ): sZip = getZip5GotZipPlus4( sZip )
    #
    sZip = putZerosBackInFront( sZip )
    #
    return dApoZipCountry.get( sZip, '' )



def getZipLike( s ):
    #
    from sMail.Test import isZipLike
    #
    if isZipLike( s ):
        sReturn = s
    else:
        sReturn = ''
    #
    return sReturn




if __name__ == "__main__":
    #
    from six            import print_ as print3
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if putZerosBackInFront( '9824' ) != '09824':
        #
        lProblems.append( 'putZerosBackInFront() put zero back in front' )
        #
    #
    if putZerosBackInFront( '09824' ) != '09824':
        #
        lProblems.append( 'putZerosBackInFront() orig zip correct' )
        #
    #
    dWA = { 'min' : '98000', 'max' : '99499' }
    #
    if dZipRange4State[ 'Washington' ] != dWA:
        #
        lProblems.append( 'dZipRange4State()' )
        #
    #
    if dZipRange4Code[ 'WA' ] != dWA:
        #
        lProblems.append( 'dZipRange4Code()' )
        #
    #
    if getApoCountryOffZip( '09888' ) != 'Kuwait':
        #
        lProblems.append( 'getApoCountryOffZip() valid zip' )
        #
    #
    if getApoCountryOffZip( '09888' ) != 'Kuwait':
        #
        lProblems.append( 'getApoCountryOffZip() valid zip' )
        #
    #
    if getApoCountryOffZip( '9618' ) != 'Italy':
        #
        lProblems.append( 'getApoCountryOffZip() valid zip' )
        #
    #
    if getApoCountryOffZip( '01000' ):
        #
        lProblems.append( 'getApoCountryOffZip() invalid zip' )
        #
    #
    if getApoCountryOffZip( '09888-1234' ) != 'Kuwait':
        #
        lProblems.append( 'getApoCountryOffZip() valid ZipPlus4' )
        #
    #
    if getZipLike( '09888-1234' ) != '09888-1234' or getZipLike( 'abc' ) != '':
        #
        print3( getZipLike( '09888-1234' ) )
        print3( getZipLike( 'abc' ) )
        lProblems.append( 'getZipLike()' )
        #
    #
    tStatesZips = (
        ('AK', '99749'),
        ('AL', '35999'),
        ('AR', '72299'),
        ('AS', '96799'),
        ('AZ', '85999'),
        ('CA', '93349'),
        ('CO', '80999'),
        ('CT', '06499'),
        ('DC', '20299'),
        ('DE', '19849'),
        ('FL', '33499'),
        ('GA', '30999'),
        ('GU', '96921'),
        ('HI', '96849'),
        ('IA', '51499'),
        ('ID', '83599'),
        ('IL', '61499'),
        ('IN', '46999'),
        ('KS', '66999'),
        ('KY', '41499'),
        ('LA', '70799'),
        ('MA', '01899'),
        ('MD', '21299'),
        ('ME', '04449'),
        ('MI', '48999'),
        ('MN', '55999'),
        ('MO', '64499'),
        ('MP', '96951'),
        ('MS', '39299'),
        ('MT', '59499'),
        ('NC', '27999'),
        ('ND', '58499'),
        ('NE', '68999'),
        ('NH', '03449'),
        ('NJ', '07999'),
        ('NM', '87949'),
        ('NV', '89449'),
        ('NY', '12499'),
        ('OH', '44499'),
        ('OK', '73999'),
        ('OR', '97499'),
        ('PA', '17349'),
        ('PR', '00664'),
        ('RI', '02899'),
        ('SC', '29499'),
        ('SD', '57499'),
        ('TN', '37799'),
        ('TX', '77499'),
        ('UT', '84499'),
        ('VA', '23349'),
        ('VI', '00814'),
        ('VT', '05499'),
        ('WA', '98749'),
        ('WI', '53999'),
        ('WV', '25849'),
        ('WY', '82599') )
    #
    lMisses = [ t for t in tStatesZips if getStateGotZip( t[1] ) != t[0] ]
    #
    if lMisses:
        #
        lProblems.append( 'getStateGotZip()' )
        #
    #
    #
    #
    sayTestResult( lProblems )
