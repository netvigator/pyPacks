#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# putOutSQL.py output SQL statements file
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
# Copyright 2014-2016 Rick Graves
#

'''

'''

from os.path        import expanduser

from six            import print_ as print3

from File.Test      import isFileThere
from File.Write     import openAppendClose
from Utils.Config   import getConfDict


oExampleConf        = getConfDict( 'putOutSQL.conf' )

sDirOut             = expanduser(
                        oExampleConf['main']['dirout'       ] )

sDataFile       = oExampleConf['main']['datafile'   ]

sOutFile        = oExampleConf['main']['outfile'    ]






def deleteOutFile( sDirOut, sOutFile ):
    #
    from File.Del import DeleteIfExists
    #
    DeleteIfExists( sDirOut, sOutFile )



def writeLineToOutFile( sLine, sDirOut, sOutFile, bNewLineBefore = True ):
    #
    openAppendClose( sLine, sDirOut, sOutFile,
            bNewLineBefore  = bNewLineBefore,
            bNewLineAfter   = False )


_tFirstLines = (
    'start transaction ;',
    'use dareport_dacrm ;',
    'delete from civicrm_custom_value '
        'where entity_table = "civicrm_contact" and custom_field_id = 25 ;',
    'insert into civicrm_custom_value '
        '( entity_table, entity_id, custom_field_id, char_data ) '
        'values ' )



def _writeLineToOutFile( sLine, bNewLineBefore = True ):
    #
    # do this in the calling script to cut down out parameters
    #
    writeLineToOutFile(
        sLine, sDirOut, sOutFile, bNewLineBefore  = bNewLineBefore )



def doFirstLines(
        tFirstLines = _tFirstLines,
        writeLineToOutFile = _writeLineToOutFile ):
    #
    bNewLineBefore = False
    #
    for s in tFirstLines:
        #
        writeLineToOutFile( s, bNewLineBefore )
        #
        bNewLineBefore = True



def _getValuesLine( sCID, sDist ):
    #
    return '( "civicrm_contact", %6s, 25, "%s" )' % ( sCID, sDist )



_tAddTextFormat = ( ',\n%s', '%s' )



def writeValueLineToOutFile( sLine, bFirstLine = False ):
    #
    sAddTextFormat = _tAddTextFormat[ bFirstLine ] # choose which one
    #
    sAddText = sAddTextFormat % sLine
    #
    _writeLineToOutFile( sAddText, bNewLineBefore = bFirstLine )




def _writeValueLineToOutFile( sCID, sDist, bFirstLine = False ):
    #
    # this is an oExample
    #
    sAddText = _getValuesLine( sCID, sDist )
    #
    writeValueLineToOutFile( sAddText, bFirstLine )



_tLastLines = (
    ' ;',
    'commit ;' )


def writeLastLines(
        tLastLines = _tLastLines,
        writeLineToOutFile = _writeLineToOutFile ):
    #
    for s in tLastLines:
        #
        writeLineToOutFile( s )


def _writeTestFile():
    #
    from Iter.Get import getItemIterWithKeysConsistentCase
    #
    deleteOutFile( sDirOut, sOutFile )
    #
    doFirstLines( _tFirstLines )
    #
    tTestLines = (
        ( 'abc', '01' ),
        ( 'def', '02' ),
        ( 'ghi', '03' ),
        ( 'jkl', '04' ) )
    #
    bFirst = True
    #
    for t in tTestLines:
        #
        sCID, sDist = t
        #
        _writeValueLineToOutFile( sCID, sDist, bFirstLine = bFirst )
        #
        bFirst = False
    #
    writeLastLines()

    
    
    


if __name__ == "__main__":
    #
    from sys import argv
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    args = argv[ 1 : ]
    #
    if args and args[0] == 'write':
        #
        writeLists()
        #
    elif args and args[0] == 'debug':
        #
        bDebugPrint = True
        #
    elif args and args[0] == 'test':
        #
        _writeTestFile()
    #
    #
    #

    #
    sayTestResult( lProblems )
