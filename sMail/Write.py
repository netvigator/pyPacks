#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# SnailMail sMail functions Write
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
from Time.Output import getNormalDate


def getLetterTop( sReturn, sRE = None, sSayDate = None ):
    #
    lOut    = [''] * 4
    #
    lOut[0] = sSayDate
    #
    if sSayDate is None:
        #
        lOut[0] = getNormalDate()
    #
    lOut.append( sReturn )
    #
    if sRE:
        #
        lOut.append( '' )
        lOut.append( 'Re: %s' % sRE )
        #
    #
    lOut.append( '' )
    lOut.append( '' )
    #
    return '\n'.join( lOut )



def getPageTwoHeader( sTo, iPage = 2, sSayDate = None ):
    #
    lOut        = [''] * 6
    #
    lOut[0]     = sTo
    #
    lOut[1]     = 'Page %s' % iPage
    #
    lOut[2]     = sSayDate
    #
    if sSayDate is None:
        #
        lOut[2] = getNormalDate()
    #
    return '\n'.join( lOut )



if __name__ == "__main__":
    #
    from six            import print_ as print3
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    tReturn = ( 'Rick Graves',
                '19/78 Sukhumvit Suite Bldg.',
                'Sukhumvit Soi 13',
                'Khlong Toei Nua, Watthana',
                'Bangkok 10110 Thailand' )
    #
    sRE     = 'Viagra available online'
    #
    sToday  = getNormalDate()
    #
    lTop = getLetterTop( '\n'.join( tReturn ), sRE, sToday ).split( '\n' )
    #
    lWant = [ sToday ]
    lWant.extend( ( '', '', '' ) )
    lWant.extend( tReturn )
    lWant.extend( ( '', 'Re: ' + sRE, '', '' ) )
    #
    if lTop != lWant:
        #
        print3( lWant )
        #
        lProblems.append( 'getEmailAdd()' )
        #
    #
    sPageTwoHeader = getPageTwoHeader( tReturn[0], 2, sToday )
    #
    lPageTwoHeader = [ tReturn[0] ]
    lPageTwoHeader.extend( ( 'Page 2', sToday, '', '', '' ) )
    #
    if sPageTwoHeader != '\n'.join( lPageTwoHeader ):
        #
        lProblems.append( 'getPageTwoHeader()' )
        #
    #
    sayTestResult( lProblems )