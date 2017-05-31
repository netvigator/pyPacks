#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions FTP
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
# self test needs internet connection and ftp site to which one can upload
#

def _ftpSendTextFile( oFTP, sFileSpec, cServerDir = '', bCloseFTP = True ):
    #
    from os     import path
    #
    from File.Get  import FileNotThereError
    from File.Test import isFileThere
    # first
    # from ftplib import FTP
    # oFTP = FTP('ftp.domain.com')
    # oFTP.login('username', 'password')
    #
    if not isFileThere( sFileSpec ): raise FileNotThereError( sFileSpec )
    #
    sCWD        = ''
    #
    if cServerDir:
        #
        sCWD    = oFTP.cwd( cServerDir )
        #
    #
    bCWD        = sCWD == '' or sCWD.startswith( '250' ) # OK. Current directory is ...
    #
    fLocal      = open( sFileSpec )
    #
    sResult     = oFTP.storlines( 'STOR %s' % path.basename( sFileSpec ), fLocal )
    #
    fLocal.close()
    #
    bSuccess    = sResult.startswith('226') # File successfully transferred
    #
    if bCloseFTP:
        #
        oFTP.quit()
        #
    #
    return bCWD, bSuccess




def FtpUploadTextFile(
        sDomain, sFileSpec, sUserName = 'anonymous', sPassword = '', cServerDir = '' ):
    #
    from ftplib import FTP
    #
    bLoggedIn, bCWD, bSuccess = False, False, False
    #
    try:
        #
        oFTP            = FTP( sDomain )
        #
        sLogin          = oFTP.login( sUserName, sPassword )
        #
        bLoggedIn       = sLogin.startswith( '230' )
        #
    except:
        #
        pass
        #
    #
    if bLoggedIn:
        #
        bCWD, bSuccess  = _ftpSendTextFile( oFTP, sFileSpec, cServerDir )
        #
    #
    return bCWD, bSuccess




if __name__ == "__main__":
    #
    from getpass        import getpass
    from os.path        import join
    #
    from Dir.Get        import sTempDir
    from File.Write     import MakeTemp
    from Utils.Result   import sayTestResult
    #
    class Abort( Exception ): pass
    #
    lProblems = []
    #
    try:
        #
        sFtpSite    = raw_input( "Type domain for this FTP upload:" )
        #
        if not sFtpSite: raise Abort
        #
        sUserName   = raw_input( "Name for ftp account:" )
        #
        if not sUserName: raise Abort
        #
        sPassWord   = getpass()
        #
        if not sPassWord: raise Abort
        #
        sScriptDir  = raw_input( "Move upload to (optional):" )
        #
    except Abort:
        #
        pass
        #
    #
    if sFtpSite and sUserName and sPassWord:
        #
        MakeTemp( 'How now brown cow.', bSayBytes = False )
        #
        bDirOK, bUploaded = \
            FtpUploadTextFile(
                sFtpSite,
                join( sTempDir, 'temp.txt' ),
                sUserName, sPassWord, sScriptDir )
        #
    #
    if not ( bDirOK and bUploaded ):
        #
        lProblems.append( 'FtpUploadTextFile()' )
        #

    #
    sayTestResult( lProblems )
    # self test needs internet connection and ftp site to which one can upload