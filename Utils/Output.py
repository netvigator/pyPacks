#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Utility functions Output
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
#

from six import print_ as print3


def getTextOutputFromExternalCommand( sCommand ):
    #
    """
    pass an external command
    returns the stdout and stderr of the external command
    """
    #
    from shlex      import split
    from subprocess import PIPE, Popen # new in 2.4
    #
    args = split( sCommand )
    #
    sOutPut, sError = Popen(
                        args,
                        stdout = PIPE,
                        stderr = PIPE,
                        shell=True ).communicate()
    #
    return sOutPut, sError



def doSomethingSupressOutput( doSomething ):
    #
    from Object.Get import StreamNull
    from sys        import stdout, stderr
    #
    OrigStdOut  = stdout
    OrigStdErr  = stderr
    #
    stdout      = StreamNull()
    stderr      = StreamNull()
    #
    doSomething()
    #
    stdout      = OrigStdOut
    stderr      = OrigStdErr
    #





def PrintMaybe( uSomething, bPrintAnyway = False ):
    #
    from sys            import stdout
    #
    from Iter.AllVers   import iMap
    from Iter.Test      import isIterable
    from String.Test    import isString
    #
    if stdout.isatty() or bPrintAnyway:
        #
        if isString(     uSomething ):
            #
            sSomething = uSomething
            #
        elif isIterable( uSomething ):
            #
            sSomething = '\n'.join( iMap( str, uSomething ) )
            #
        else:
            #
            sSomething = uSomething
            #
        #
        print3( sSomething )



def OutLocals(): print3( locals() )




if __name__ == "__main__":
    #
    lProblems = []
    #
    from Utils.Get      import getMainNamePath
    from Utils.Result   import sayTestResult
    #
    sScript, sPath  = getMainNamePath()
    #
    sDirCmd         = 'ls %s/*.py' % sPath
    #
    sDirOut, sError = getTextOutputFromExternalCommand( sDirCmd )
    #
    if 'temp.txt' in sDirOut or not 'Output.py' in sDirOut:
        #
        lProblems.append( 'getTextOutputFromExternalCommand()' )
        #
    def getDir(): return getTextOutputFromExternalCommand( sDirCmd )
    #
    if doSomethingSupressOutput( getDir ):
        #
        lProblems.append( 'doSomethingSupressOutput()' )
        #
    if PrintMaybe( 'This is a test!' ):
        #
        lProblems.append( 'PrintMaybe()' )
        #
    #
    sayTestResult( lProblems )
