#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Utility functions Lock
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

from sys            import exc_info

from File.Get       import getFileContent

class LockError( OSError ): pass

IMODEWROTE = 511 # 0o777
IMODEMAKE  = 493 # 0o755
IMODELOCK  = 420 # 0o644

def _WroteLockFile( sFileName, sContents='', iMode=IMODEWROTE ):
    #
    from os         import makedirs, O_EXCL, O_CREAT, O_WRONLY, close, write
    from os         import open as os_open
    from os.path    import dirname, exists
    from errno      import EEXIST
    #
    from Utils.Version import PYTHON3
    #
    sLockDir = dirname(sFileName)
    #
    try:
        if sLockDir != '' and not exists(sLockDir):
            makedirs(sLockDir, iMode=IMODEMAKE)
        fd = os_open( sFileName, O_EXCL|O_CREAT|O_WRONLY, iMode )
    except OSError:
        error, msg, traceback = exc_info()
        if msg.errno != EEXIST: raise msg
        return False
    else:
        if PYTHON3: sContents = bytes( sContents, 'utf-8' )
        write( fd, sContents )
        close(fd)
        return True




def doUnlock(sLockFile):
    #
    from    os      import remove
    #
    try:
        remove(sLockFile)
    except OSError:
        pass



def _GetPID( sLockFile ):
    #
    sPID     = getFileContent(sLockFile)
    #
    try:
        #
        iPID = int( sPID )
        #
    except ValueError:
        #
        iPID = None
    #
    return iPID



def doLock( sLockFile, bKill = False, oLogger = None ):
    #
    from os             import getpid, kill
    from errno          import ESRCH
    #
    mypid   = str( getpid() )
    #
    while not _WroteLockFile( sLockFile, mypid, IMODELOCK):
        #
        iOldPID = _GetPID( sLockFile )
        #
        if iOldPID is None: # invalid data, throw away.
            #
            doUnlock(sLockFile)
            #
        else:
            #
            try: kill(iOldPID, 0)
            #
            except OSError:
                error, msg, traceback = exc_info()
                if msg[0] == ESRCH:
                    # no such pid
                    doUnlock(sLockFile)
                else:
                    # What?
                    msg = 'Unable to check if PID %s is active' % iOldPID
                    raise LockError(1, msg)
            else:
                # Another copy seems to be running.
                #
                #
                if bKill:
                    #
                    doKill( sLockFile, oLogger )
                    #
                else:
                    #
                    msg = 'Existing lock %s: another copy is running. Aborting.' % sLockFile
                    raise LockError(0, msg)



def isAnotherProgramRunning( sLockFile ):
    #
    from os.path        import exists
    from os             import getpid, kill
    from errno          import ESRCH
    #
    bAnotherProgramRunning  = False
    #
    if exists( sLockFile ):
        #
        iPID = _GetPID( sLockFile )
        #
        if iPID is None: # invalid data, throw away.
            #
            doUnlock(sLockFile)
            #
        else:
            #
            try: kill(iPID, 0)
            #
            except OSError:
                error, msg, traceback = exc_info()
                if msg[0] == ESRCH:
                    # no such pid
                    doUnlock(sLockFile)
                else:
                    # What?
                    bAnotherProgramRunning  = True
                    #
            else:
                #
                bAnotherProgramRunning      = True
                #
            #
        #
    #
    return bAnotherProgramRunning




def doKill( sLockFile, oLogger = None ):
    #
    from os.path        import exists
    from signal         import SIGKILL
    from os             import kill
    #
    if exists( sLockFile ):
        #
        iPID = _GetPID( sLockFile )
        #
        if iPID is None: # invalid data, throw away.
            #
            doUnlock(sLockFile)
            #
        else:
            #
            kill( iPID, SIGKILL )
            #
            doUnlock(sLockFile)
            #
            if oLogger:
                #
                oLogger.log( 0,'killed pid %s' % iPID )
                #



if __name__ == "__main__":
    #
    from os.path     import exists
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    PID_FILE    = 'YouCanDeleteThis.pid'
    #
    doLock(PID_FILE)
    #
    # print3( 'The test script is locked.' )
    #
    if not exists( PID_FILE ):
        #
        lProblems.append( 'doLock() no PID_FILE' )
        #
    #
    # print3( "This script's PID is %s." % getFileContent( PID_FILE ) )
    #
    if not getFileContent( PID_FILE ).isdigit():
        #
        lProblems.append( 'doLock() no digits inside' )
        #
    #
    #
    doUnlock(PID_FILE)
    #
    # print3( 'The test script is unlocked.' )
    #
    if exists( PID_FILE ):
        #
        lProblems.append( 'doLock() PID_FILE still there' )
        #
    #
    sayTestResult( lProblems )