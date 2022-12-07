#!/home/rick/.local/bin/pythonTest
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
#   http://www.gnu.org/licenses/
#
# Copyright 2004-2023 Rick Graves
#
#
from shlex              import split
from subprocess         import PIPE, Popen # new in 2.4
from sys                import stdout, stderr

from six                import print_ as print3

try:
    from ..Iter.AllVers import iMap
    from ..Iter.Test    import isIterable
    from ..Object.Get   import StreamNull
    from ..String.Test  import isString
except ( ValueError, ImportError ):
    from Iter.AllVers   import iMap
    from Iter.Test      import isIterable
    from Object.Get     import StreamNull
    from String.Test    import isString

def getTextOutputFromExternalCommand( sCommand ):
    #
    """
    pass an external command
    returns the stdout and stderr of the external command
    """
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



def getOutputFromExternalCommand( sCommand ):
    #
    """
    pass an external command as string
    returns the stdout and stderr of the external command
    works when getTextOutputFromExternalCommand() does not
    """
    #
    sOutPut, sError = Popen(
                        [ sCommand ],
                        stdout = PIPE,
                        stderr = PIPE,
                        shell=True ).communicate()
    #
    return sOutPut, sError




def doSomethingSupressOutput( doSomething, *args, **kwargs ):
    #
    from sys    import stdout, stderr # need this again !
    #
    OrigStdOut  = stdout
    OrigStdErr  = stderr
    #
    stdout      = StreamNull()
    stderr      = StreamNull()
    #
    doSomething( *args, **kwargs )
    #
    stdout      = OrigStdOut
    stderr      = OrigStdErr
    #





def PrintMaybe( uSomething, bPrintAnyway = False ):
    #
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


_tYesOrNo  = ( 'No', 'Yes' )
_tBlankYes = ( '',   'Y'   )
_tYorN     = ( 'N',  'Y'   )

def getSayYesOrNo( bValue, _tYesOrNo = _tYesOrNo ):
    #
    # formerly getSayColYesOrNo() when in Collect.Output
    # def sayColYesOrNo() support text search for similar name
    # def sayYesOrNo() support text search for similar name
    #
    return _tYesOrNo[ int( bValue) ]


def getSayYesOrNoLooser( u, _tYesOrNo = _tYesOrNo ):
    #
    # formerly getSayColYesOrNoLooser() when in Collect.Output
    #
    return _tYesOrNo[ int( bool( u ) ) ]


def getSayYesOrBlank( bValue ):
    #
    # formerly getSayColYesOrBlank() when in Collect.Output
    #
    return getSayYesOrNo( bValue, _tYesOrNo = _tBlankYes )


def getSayColYorN( bValue ):
    #
    # formerly getSayColYorN() when in Collect.Output
    #
    return getSayYesOrNo( bValue, _tYesOrNo = _tYorN )


def getSayYesOrBlankLooser( u ):
    #
    # formerly getSayColYesOrBlankLooser() when in Collect.Output
    #
    return getSayYesOrNoLooser( u, _tYesOrNo = _tBlankYes )



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
    if getSayYesOrNo( False ) != 'No' or getSayYesOrNo( True ) != 'Yes':
        #
        lProblems.append( 'getSayYesOrNo()' )
        #
    #
    if getSayYesOrNoLooser( '' ) != 'No' or getSayYesOrNoLooser( 'a' ) != 'Yes':
        #
        lProblems.append( 'getSayYesOrNoLooser()' )
        #
    #
    if getSayYesOrBlank( False ) != '' or getSayYesOrBlank( True ) != 'Y':
        #
        lProblems.append( 'getSayYesOrBlank()' )
        #
    #
    if getSayColYorN( False ) != 'N' or getSayColYorN( True ) != 'Y':
        #
        lProblems.append( 'getSayColYorN()' )
        #
    #
    if getSayYesOrBlankLooser( '' ) != '' or getSayYesOrBlankLooser( 'a' ) != 'Y':
        #
        lProblems.append( 'getSayYesOrBlankLooser()' )
        #
    #
    sayTestResult( lProblems )
