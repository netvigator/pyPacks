#!/home/rick/bin/pythonTest
# -*- coding: utf-8 -*-
#
# time functions ReadWrite (name File d/n work)
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

from datetime           import datetime
from time               import time


try:
    from .Convert       import getSecsSinceEpochFromString, getIsoDateTimeStrFromSecs
    from ..File.Get     import getFileContent
    from ..File.Info    import getModTime
    from ..File.Spec    import getFullSpecDefaultOrPassed
    from ..File.Write   import QuickDump, openAppendClose
except ( ValueError, ImportError ):
    from Time.Convert   import getSecsSinceEpochFromString, getIsoDateTimeStrFromSecs
    from File.Get       import getFileContent
    from File.Info      import getModTime
    from File.Spec      import getFullSpecDefaultOrPassed
    from File.Write     import QuickDump, openAppendClose


def getTimeFromFile( *sFileSpec ):
    #
    """
    goes with putTimeInFile
    """
    #
    #
    sText   = getFileContent( *sFileSpec )
    #
    lText   = sText.split( '\n' )
    #
    sTime   = lText [ 0 ]
    #
    if lText: del lText[ 0 ]
    #
    sRest   = '\n'.join( lText )
    #
    fTime   = 0.0
    #
    try:
        #
        fTime       = float( sTime )
        #
    except ( ValueError, ImportError ):
        #
        try:
            #
            fTime   = getSecsSinceEpochFromString( sTime )
            #
        except:
            #
            pass
            #
        #
    except:
        #
        pass
    #
    return fTime, sRest




def putTimeInFile( *sFileSpec, **kwargs ):
    #
    # sFile = None, fSecsSinceEpoch = None, bOverWrite = True, sWriteMore = '' ):
    #
    """
    goes with getTimeFromFile
    """
    #
    #
    fSecsSinceEpoch = kwargs.get( 'fSecsSinceEpoch',  time() )
    bOverWrite      = kwargs.get( 'bOverWrite',       True      )
    sWriteMore      = kwargs.get( 'sWriteMore',       ''     )
    #
    #
    sFile = getFullSpecDefaultOrPassed( *sFileSpec, **kwargs )
    #
    sTime = '%s\n%s' % ( getIsoDateTimeStrFromSecs( fSecsSinceEpoch ), sWriteMore )
    #
    if bOverWrite:
        QuickDump( sTime, sFile, bSayBytes = False, bWantDir = False )
    else:
        openAppendClose( sTime, sFile, bSayBytes = False, bWantDir = False )



def getModTimeDateTimeObjFromFile( *sFileSpec, **kwargs ):
    # sPathMaybeMore = None, sFileName=None, bWantLocal = True ):
    #
    # not used anywhere
    #
    #
    bWantLocal      = kwargs.get( 'bWantLocal', True )
    #
    sFile = getFullSpecDefaultOrPassed( *sFileSpec, **kwargs )
    #
    iSecs           = getModTime( sFile, bWantLocal = bWantLocal )
    #
    oModTime        = datetime.fromtimestamp( iSecs )
    #
    return oModTime





if __name__ == "__main__":
    #
    lProblems = []
    #
    from time           import time
    #
    from Time.Convert   import getIsoDateTimeStrFromSecs, \
                               getSecsSinceEpochFromString
    from Utils.Result   import sayTestResult
    #
    iNow    = int( time() )
    sNow    = getIsoDateTimeStrFromSecs( iNow )
    #
    putTimeInFile( fSecsSinceEpoch = iNow )
    #
    iSinceEpoch, sRest = getTimeFromFile()
    #
    if iSinceEpoch != iNow:
        #
        lProblems.append( 'putTimeInFile()' )
        lProblems.append( 'getTimeFromFile()' )
        #
    #
    oFileTime = getModTimeDateTimeObjFromFile()
    #
    if abs( getSecsSinceEpochFromString( oFileTime.__str__() ) - iNow ) > 2:
        #
        lProblems.append( 'getSecsSinceEpochFromString()' )
        #
    #
    sayTestResult( lProblems )
