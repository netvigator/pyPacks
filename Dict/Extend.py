#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# dict functions Extend
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
# Copyright 2004-2012 Rick Graves
#


class returnValueOrArg( dict ):
    #
    '''
    dictonary with getVorA() method -- see docstring for method
    name is short for "return value or argument"
    '''
    #
    def getVorA( self, k ):
        #
        '''
        pass one argument to the method
        getVorA() returns the value if the argument is a key
        otherwise, it returns the argument
        name is short for "get value or argument"
        '''
        #
        return self.get( k, k )



class DoubleDictClass( dict ):
    #
    """
    For fast lookups of keys and values.
    Implemented by having a second dict with keys as values and values as keys.
    This code assumes the values are unique.
    If the above does not apply, this class needs updating.
    """
    #
    def __init__( self, dThis = {} ):
        #
        self.update( dThis )
        #
        self.UpdateReverseFromDict()
        #
    #
    def Update( self, uKey, uValue ):
        #
        self[ uKey ]            = uValue
        #
        self.dReverse[ uValue ] = uKey
    #
    def UpdateReverseFromDict( self ):
        #
        from Dict.Get import getReverseDictGotUniqueItems
        #
        self.dReverse   = getReverseDictGotUniqueItems( self )
    #
    def hasValue( self, uValue ):
        #
        return uValue in self.dReverse
    #
    def hasSomething( self, uSomething ):
        #
        return uSomething in self or uSomething in self.dReverse
    #
    def hasKey( self, uSomething ):
        #
        return uSomething in self
    #
    def getKeyFromValue( self, uValue ):
        #
        return self.dReverse.get( uValue )
    #
    def getValueFromKey( self, uKey ):    # just a wrapper for get()
        #
        return self.get( uKey )




class getClosestClass( dict ): # not used anywhere
    #
    """Returns key and value for key or value that is close to
    the look up value -- look up value can be shorter than actual key.
    Example, look up value abc will find key abcde.
    Known to work with string keys, may work with other types also.
    Example application is class Countries in getMamboMirrors.
    Here is the rub: all values must be unique."""
    #
    def __init__( self, dLookIn ):
        #
        from Dict.Get import getItemIter, getValueList
        #
        self.update( dLookIn )
        #
        self.dReverse   = {}
        #
        for sKey, sValue in getItemIter( self ):
            #
            self.dReverse[ sValue ] = sKey  # if you have the value, look up the key
            #
        #
        self.lValues    = getValueList( self )
        #
        self.lValues.sort()
        #


    def getValue4Key( self, sLook4This ):
        #
        import bisect
        #
        uValue      = None
        sKey        = None
        #
        if sLook4This in self:
            #
            sKey    = sLook4This
            #
            uValue  = self[ sLook4This ]
            #
        elif sLook4This in self.dReverse:
            #
            uValue  = sLook4This
            #
            sKey    = self.dReverse[ sLook4This ]
            #
        else:
            #
            iNext   = bisect.bisect( self.lValues, sLook4This )
            #
            # bisect = bisect_right
            #
            if      iNext < len(  self.lValues ) and \
                    sLook4This in self.lValues[ iNext ]:
                #
                uValue  = self.lValues[ iNext ]
                #
                sKey    = self.dReverse[ uValue ]
                #


        return sKey, uValue





if __name__ == "__main__":
    #
    lProblems = []
    #
    from Collect.Test   import AllMeet
    from Dict.Get       import getKeyIter, getItemIter, getValueIter
    from Utils.Result   import sayTestResult
    #
    dTest = dict( a = 1, b = 2, c = 3, d = 4, e = 5, f = 6, g = 7, h = 8 )
    #
    dReverse = DoubleDictClass( dTest )
    #
    def isRightValue( value ): return dReverse[ dReverse.getKeyFromValue( value ) ] == value
    #
    if      not AllMeet( getValueIter( dTest ), dReverse.hasValue      ) or \
            not AllMeet( getValueIter( dTest ), dReverse.hasSomething  ) or \
            not AllMeet( getKeyIter(   dTest ), dReverse.hasKey        ) or \
            not AllMeet( getKeyIter(   dTest ), dReverse.hasSomething  ) or \
            not AllMeet( getValueIter( dTest ), isRightValue           ):
        #
        lProblems.append( 'DoubleDictClass()' )
        #
    #
    dClose = getClosestClass( dTest )
    #
    setItems = frozenset( getItemIter( dTest ) )
    #
    def GotItem( t ): return t in setItems
    #
    def hasItemForKey( key ): return GotItem( dClose.getValue4Key( key ) )
    #
    if not AllMeet( getKeyIter( dTest ), hasItemForKey ):
        #
        lProblems.append( 'GetClosestClass()' )
        #
    #
    dTest = returnValueOrArg()
    #
    dTest[ 'toast' ] = 'beans on toast'
    #
    if dTest.getVorA( 'toast' ) != 'beans on toast':
        #
        lProblems.append( 'returnValueOrArg() has key' )
        #
    #
    if dTest.getVorA( 'spam' ) != 'spam':
        #
        lProblems.append( 'returnValueOrArg() does not have key' )
        #
    #
    sayTestResult( lProblems )