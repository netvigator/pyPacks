#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Object functions Set
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



def getAttributesFromDict(d, obj=None, objName="self"):
    #
    """No need for self.foo = foo, self.bar = bar, etc."""
    #
    from Dict.Get import getItemIter
    #
    if obj is None:
        obj = d.pop(objName)
    for n, v in getItemIter( d ):
        setattr(obj, n, v)



class _getsAttributesFromKWArgs( object ):
    #
    """No need for self.foo = foo, self.bar = bar, etc.
    ValueContainer is faster, does the job in about 20% of the time"""
    #
    def __init__( self, **kwargs ):
        #
        kwargs[ 'self' ] = self
        #
        getAttributesFromDict( kwargs )
        #
        # faster: self.__dict__.update( kwargs )



def _AttributesFromKWArgsSpeedTest():
    #
    from six                import print_ as print3
    #
    from Object.Get         import ValueContainer
    from Utils.TimeTrial    import TimeTrial
    #
    print3( '\n_getsAttributesFromKWArgs' )
    TimeTrial( _getsAttributesFromKWArgs,
                        a = 1, b = 2, c = 3 )
    #
    print3( '\nValueContainer' )
    TimeTrial( ValueContainer,
                        a = 1, b = 2, c = 3 )
    #
    # ValueContainer is faster, does the job in about 20% of the time



if __name__ == "__main__":
    #
    from six            import print_ as print3
    #
    from Object.Get     import ValueContainer
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    oTest = _getsAttributesFromKWArgs( foo = 3, bar = 88 )
    #
    if oTest.bar != 88:
        #
        lProblems.append( 'getAttributesFromDict()' )
        #
    #
    oTest       = _getsAttributesFromKWArgs(
                        a = 1, b = 2, c = 3 )
    #
    oValueCont  = ValueContainer(
                        a = 1, b = 2, c = 3 )
    #
    if oTest.__dict__ != oValueCont.__dict__:
        #
        lProblems.append( 'getAttributesFromDict & ValueContainer not same' )
        #
    #
    #

    #
    sayTestResult( lProblems )