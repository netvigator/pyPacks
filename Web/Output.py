#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions Output
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
# Copyright 2004-2013 Rick Graves
#
# self test needs internet connection and will access python.org

def PutPageInTemp( sURL, tProxy = ('', -1), **dMoreLines ):
    #
    from Web.Get    import getPageContent
    from File.Write import MakeTemp
    #
    sHTML = getPageContent( sURL, tProxy = tProxy, dLines = dMoreLines )
    #
    MakeTemp( sHTML, bSayBytes = False )



if __name__ == "__main__":
    #
    from os.path        import exists, join
    #
    from Dir.Get        import sTempDir
    from File.Info      import getSize, getModTime
    from Time.Clock     import getSecsSinceEpoch
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    nNow        = getSecsSinceEpoch()
    #
    PutPageInTemp( 'www.python.org' )
    #
    sTempFile   = join( sTempDir, 'temp.txt' )
    #
    if not exists( sTempFile ):
        #
        lProblems.append( 'PutPageInTemp() does not exist' )
        #
    elif getSize(  sTempFile ) < 5000:
        #
        lProblems.append( 'PutPageInTemp() size too small -- do u have internet?' )
        #
    #
    elif getModTime( sTempFile ) < nNow:
        #
        lProblems.append( 'PutPageInTemp() too old' )
        #
    #
    elif getModTime( sTempFile ) > nNow * 1.01:
        #
        lProblems.append( 'PutPageInTemp() future file date/time' )
        #
    #
    sayTestResult( lProblems )
    # self test needs internet connection and will access python.org