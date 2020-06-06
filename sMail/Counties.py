#!/home/rick/bin/pythonTest
# -*- coding: utf-8 -*-
#
# SnailMail sMail functions Counties
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
# Copyright 2004-2020 Rick Graves
#

# http://www.ng3k.com/misc/usc_ind.html

from sMail          import tStatesCounties
from Dict.Get       import getKeyIter
from String.Find    import getFinderFindAll, getSeqWordBounds

_dCountiesStates = {}


def _addCounty( sCounty, sState ):
    #
    lStates = _dCountiesStates.setdefault( sCounty, [] )
    #
    lStates.append( sState )


def _getCountiesStatesDict( sState, tCounties ):
    #
    for sCounty in tCounties:
        #
        _addCounty( sCounty, sState )
        #
        if sCounty.startswith( 'St. ' ):
            #
            sCounty = sCounty.replace( 'St. ', 'Saint ' )
            #
            _addCounty( sCounty, sState )
            #
        elif sCounty.startswith( 'Ste. ' ):
            #
            sCounty = sCounty.replace( 'St. ', 'Sainte ' )
            #
            _addCounty( sCounty, sState )
            #
        #
    #

for t in tStatesCounties:
    #
    _getCountiesStatesDict( t[0], t[1] )
    

for sCounty in _dCountiesStates:
    #
    _dCountiesStates[ sCounty ] = frozenset( _dCountiesStates[ sCounty ] )

oCountyFinder = getFinderFindAll(
    getSeqWordBounds( getKeyIter( _dCountiesStates ) ) )


dLowerCountyCounty = dict(
    [ ( s.lower(), s ) for s in getKeyIter( _dCountiesStates ) ] )


def _sayCountyCapitalized( sCounty ):
    #
    return dLowerCountyCounty.get(
                sCounty.strip().lower(),
                "County '%s' not found!" % sCounty )


def isCountyInState( s, sState ):
    #
    '''
    pass string and state
    returns whether string is a county in that state
    actually returns the name of the county
    '''
    #
    from sMail.Abbrev import dCodesStates, getStateGotCode
    #
    if len( sState ) == 2:
        #
        sState = sState.upper()
        #
    else:
        #
        sState = sState.title()
        #
    #
    if sState in dCodesStates:
        #
        sState = getStateGotCode( sState )
        #
    #
    sCountyInState = ''
    #
    lCounty = oCountyFinder( s )
    #
    lCounty.reverse()
    #
    for sCounty in lCounty:
        #
        sCountyLower = sCounty.lower()
        #
        if sState in _dCountiesStates[ dLowerCountyCounty[ sCountyLower ] ]:
            #
            sCountyInState = dLowerCountyCounty[ sCountyLower ]
            #
            break
            #
        #
    #
    return sCountyInState



def sayCounty( sCounty, sState ):
    #
    if sState in ( 'LA', 'Louisiana' ):
        #
        sSayCounty = 'Parish'
        #
    else:
        #
        sSayCounty = 'County'
        #
    return '%s %s' % ( _sayCountyCapitalized( sCounty ), sSayCounty )
        

if __name__ == "__main__":
    #
    from six            import print_ as print3
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if not isCountyInState( 'City of Beaver Dam,  Dodge County', 'WI' ):
        #
        lProblems.append( 'isCountyInState() also city' )
        #
    #
    if not isCountyInState( 'king', 'washington' ):
        #
        lProblems.append( 'isCountyInState() full state name' )
        #
    #
    if not isCountyInState( 'shelby', 'tn' ):
        #
        lProblems.append( 'isCountyInState() state abbreviation' )
        #
    #
    if not isCountyInState( "O'Brien", 'Iowa' ):
        #
        lProblems.append( 'isCountyInState() apostraphe in county name' )
        #
    #
    if not isCountyInState( 'Kanawha County', 'WV' ):
        #
        lProblems.append( 'isCountyInState() Kaawha County WV' )
        #
    #
    if not isCountyInState( "Fond Du Lac", 'WI' ):
        #
        lProblems.append( 'isCountyInState() Fond Du Lac WI miscapitalized' )
        #
    #
    if sayCounty( 'king', 'washington' ) != 'King County':
        #
        lProblems.append( 'sayCounty() King County' )
        #
    #
    if sayCounty( "Acadia", 'LA' ) != 'Acadia Parish':
        #
        lProblems.append( 'sayCounty() Acadia Parish' )
        #
    #
    #
    sayTestResult( lProblems )
