#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# log utils
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
# Copyright 2004-2015 Rick Graves
#
'''
simplified facade for the python logging module
'''

import logging


def getSimpleDateTimeDataLogger( sFile ):
    #
    '''
    totally not multiple logger capable
    only use this as a single logger
    '''
    logging.basicConfig(
        filename= sFile,
        format='%(asctime)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO )
    #
    return logging.info


def getDateTimeDataLoggerMultipleOK( sFile, sName ):
    #
    oLogger = logging.getLogger( sName )
    #
    oFileHandler = logging.FileHandler( sFile )
    #
    oFormater = logging.Formatter(
                    fmt='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
    #
    oFileHandler.setFormatter( oFormater )
    #
    oLogger.addHandler( oFileHandler )
    #
    return oLogger.info



if __name__ == "__main__":
    #
    from time import sleep
    #
    from Dir.Get        import sTempDir
    from File.Del       import DeleteIfExists
    from File.Get       import getRandomFileName, getListFromFileLines
    from Time.Output    import sayIsoDateTimeLocal
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    sTempFile0 = getRandomFileName( sTempDir )
    #
    oTestLogger0 = getSimpleDateTimeDataLogger( sTempFile0 )
    #
    oTestLogger0( '99999' )
    sleep(1.1)
    sTime1 = sayIsoDateTimeLocal()
    sleep(1.1)
    oTestLogger0( '66666' )
    sleep(1.1)
    sTime2 = sayIsoDateTimeLocal()
    sleep(1.1)
    oTestLogger0( '33333' )
    #
    lLogged = getListFromFileLines( sTempFile0 )
    #
    if not (    sTime1 > lLogged[0] and
                sTime1 < lLogged[1] and
                sTime2 > lLogged[1] and
                sTime2 < lLogged[2] ):
        #
        lProblems.append( 'getSimpleDateTimeDataLogger() test sequences' )
        #
    #
    DeleteIfExists( sTempFile0 )
    #
    sTempFile1 = getRandomFileName( sTempDir )
    sTempFile2 = getRandomFileName( sTempDir )
    #    
    oTestLogger1 = getDateTimeDataLoggerMultipleOK( sTempFile1, '1' )
    oTestLogger2 = getDateTimeDataLoggerMultipleOK( sTempFile2, '2' )
    #
    oTestLogger1( '88888' )
    oTestLogger2( '77777' )
    sleep(1.1)
    sTime1 = sayIsoDateTimeLocal()
    sleep(1.1)
    oTestLogger1( '55555' )
    oTestLogger2( '44444' )
    sleep(1.1)
    sTime2 = sayIsoDateTimeLocal()
    sleep(1.1)
    oTestLogger1( '22222' )
    oTestLogger2( '11111' )
    #
    lLogged1 = getListFromFileLines( sTempFile1 )
    lLogged2 = getListFromFileLines( sTempFile2 )
    #
    if not (    sTime1 > lLogged1[0] and
                sTime1 < lLogged1[1] and
                sTime2 > lLogged1[1] and
                sTime2 < lLogged1[2] ):
        #
        lProblems.append( 'getSimpleDateTimeDataLogger() test sequences 1' )
        #
    #
    if not (    sTime1 > lLogged2[0] and
                sTime1 < lLogged2[1] and
                sTime2 > lLogged2[1] and
                sTime2 < lLogged2[2] ):
        #
        lProblems.append( 'getSimpleDateTimeDataLogger() test sequences 2' )
        #
    #
    DeleteIfExists( sTempFile1 )
    DeleteIfExists( sTempFile2 )
    #
    if False:
        #
        lProblems.append( 'big_problem()' )
        #
    #
    sayTestResult( lProblems )