#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# DbApi functions Insert
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


def _getInsertStatement(
        sTable, tColumns, tValues,
        oDbApi          = None,
        oValFormatter   = None ):
    #
    #! fix tValues  to lValues?
    #
    from Iter.AllVers   import iZip
    from DbApi.Format   import getTypeCaster, getSequence, CommaSeparated
    from DbApi.Query    import getTableKeyOffName
    #
    getTypeCastValue    = getTypeCaster( oValFormatter )
    #
    tColumns            = getSequence( tColumns )
    tValues             = getSequence( tValues  )
    #
    sTableKey           = getTableKeyOffName( sTable )
    #
    if oDbApi:
        #
        dColsTypes      = oDbApi.dTables[ sTableKey ].dColsTypes
        #
        lColsValues     = iZip( tColumns, tValues )
        #
        lTypesValues    = [ ( dColsTypes[ sCol ], uValue )
                            for sCol, uValue in lColsValues ]
        #
        tValues         = [ getTypeCastValue( sType, uValue )
                            for sType, uValue in lTypesValues ]
        #
    #
    #
    sColList            = CommaSeparated( tColumns )
    sValueList          = CommaSeparated( tValues  )
    #
    sInsert = "insert into %s( %s ) values( %s )" % ( sTable, sColList, sValueList )
    #
    return sInsert




def doInsert(
        oCursor,
        oDbApi,
        sTable,
        tColsSet,
        tValsSet,
        tColsWhere      = None,
        tValsWhere      = None,
        tWhereOper      = None,
        oValFormatter   = None,
        bRaiseError     = 1 ):
    #
    # Note! the tColsWhere, tValsWhere, & tWhereOper params are not used!
    # they are for plug compatibility with the doUpdate function!
    #
    from six            import print_ as print3
    #
    sInsertStatement    = _getInsertStatement(
                            sTable, tColsSet, tValsSet, oDbApi, oValFormatter )
    #
    bGotError           = 0
    #
    # print3( sInsertStatement )
    try:
        #
        oCursor.execute( sInsertStatement )
        #
    except oDbApi.DatabaseError:
        #
        bGotError       = bRaiseError
        #
    except:
        #
        bGotError       = bRaiseError
        #
    #
    if bGotError:
        #
        print3( sInsertStatement )
        raise
        #
    #
    if bRaiseError:
        return sInsertStatement
    else:
        return bGotError



def doInsertOrError(
        oCursor,
        oDbApi,
        sTable,
        tColsSet,
        tValsSet,
        tColsWhere      = None,
        tValsWhere      = None,
        tWhereOper      = None,
        oValFormatter   = None ):
    #
    bGotError           = \
        doInsert(
            oCursor,
            oDbApi,
            sTable,
            tColsSet,
            tValsSet,
            tColsWhere      = tColsWhere,
            tValsWhere      = tValsWhere,
            tWhereOper      = tWhereOper,
            oValFormatter   = oValFormatter,
            bRaiseError     = 0 )
    #
    return bGotError



if __name__ == "__main__":
    #
    from DbApi.Connect  import getConf, getConnected
    from DbApi.Create   import CreateDatabase, DropDataBase
    from DbApi.Format   import ValueFormatterClass
    from DbApi.Test     import hasDataBase
    from Utils.Config   import NoConfigFile
    from Utils.Result   import sayTestResult
    #
    lProblems       = []
    #
    oDBConnect      = oCursor = None
    #
    oConf, oDbApi   = getConf( bNoConfigOK = 1 )
    #
    sThisRun            = 'sqlite'
    sConfigFile         = 'ConfNoExample.conf'
    #
    while True:
        #
        sDataBase   = oConf.get( 'main', 'sDataBase'  )
        sSystemSQL  = oConf.get( 'main', 'sSystemSQL' )
        #
        sHost       = oConf.get( 'main', 'sHost'      )
        sUser       = oConf.get( 'main', 'sUser'      )
        sPassword   = oConf.get( 'main', 'sPassword'  )
        #
        bNoConfigOK = ( sThisRun == 'sqlite' )
        #
        if hasDataBase( sDataBase, oDbApi, sHost, sUser, sPassword ):
            #
            oDBConnect = oCursor = None
            #
            DropDataBase( oDbApi, oConf )
            #
        #
        CreateDatabase( oConf, oDbApi, oDBConnect, oCursor )
        #
        oValFormatter   = ValueFormatterClass( oConf = oConf )
        #
        sTable          = 'Package'
        #
        tCols           = ( 'iPackage', 'sPackage' )
        #
        tValues         = (          0,   'python' )
        #
        if _getInsertStatement(
                    sTable, tCols, tValues, oDbApi, oValFormatter ) != \
                "insert into Package( iPackage, sPackage ) values( 0, 'python' )":
            #
            lProblems.append( '_getInsertStatement() for %s' % sThisRun )
            #
        #
        if oDBConnect is None or oCursor is None:
            #
            oDBConnect, oCursor = getConnected( oDbApi, oConf )
            #
        #
        if doInsert(
                    oCursor, oDbApi,
                    sTable, tCols, tValues, oValFormatter = oValFormatter ) != \
                "insert into Package( iPackage, sPackage ) values( 0, 'python' )":
            #
            lProblems.append( 'doInsert() returned incorrect statement for %s' % sThisRun )
            #
        #
        oDBConnect = oCursor = None
        #
        if hasDataBase( sDataBase, oDbApi, sHost, sUser, sPassword ):
            #
            DropDataBase( oDbApi, oConf )
            #
        #
        if sThisRun == 'sqlite':
            #
            oConf = oDbApi = None
            #
            try:
                #
                sConfigFile     = 'DbApiTest.conf'
                #
                oConf, oDbApi   = getConf( sConfigFile )
                #
                sThisRun        = oConf.get( 'main', 'sSystemSQL' )
                #
                if sThisRun == 'sqlite':
                    #
                    lProblems.append( "No real database to test!" )
                    #
                    break
                #
            except NoConfigFile:
                #
                lProblems.append( 'cannot access DbApiTest.conf' )
                #
                break
                #
            #
        else:   # quit after 2nd time through
            #
            break
            #
        #
    #
    sayTestResult( lProblems )