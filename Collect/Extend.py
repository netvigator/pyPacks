#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Collection functions Extend
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

class FifoPopper( list ):
    #
    """
    list pop() takes items off the end, FILO
    this list takes items off the front, FIFO
    """
    #
    def __init__( self, lInit = None ):
        #
        if lInit:
            #
            self.extend( lInit )
            #
    #
    def __iter__( self ):
        #
        while self:
            yield self.pop(0)
    #
    def next( self ):
        #
        return self.pop( 0 )




if __name__ == "__main__":
    #
    from six            import print_ as print3
    #
    from Iter.AllVers   import iRange
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    oPopper = FifoPopper( iRange( 10 ) )
    #
    if list( oPopper ) != [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] and len( oPopper ) != 0:
        #
        lProblems.append( 'FifoPopper()' )
        #
    #

    #
    sayTestResult( lProblems )