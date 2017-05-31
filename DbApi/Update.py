#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# DbApi functions Update
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

from six import print_ as print3

def getUpdateStatement(
        sTable,
        tColsSet,       tValsSet,
        tColsWhere,     tValsWhere,
        tWhereOper      = None,
        oDbApi          = None,
        oValFormatter   = None, ):
    #
    from DbApi.Format import getTypeCaster, getSequence, CommaSeparated
    from DbApi.Query  import getTableKeyOffName, getMeetsConditions, setColsEqualsValues
    from Iter.AllVers import iZip
    #
    getTypeCastValue    = getTypeCaster( oValFormatter )
    #
    sTableKey           = getTableKeyOffName( sTable )
    #
    if oDbApi:
        #
        dColsTypes      = oDbApi.dTables[ sTableKey ].dColsTypes
        #
        tColsWhere      = getSequence( tColsWhere )
        #
        tValsWhere      = getSequence( tValsWhere )
        #
        lColsValues     = iZip( tColsWhere, tValsWhere )
        #
        lTypesValues    = [ ( dColsTypes[ sCol ], uValue ) for sCol, uValue in lColsValues ]
        #
        tValsWhere      = [ getTypeCastValue( sType, uValue ) for sType, uValue in lTypesValues ]
        #
        tColsSet        = getSequence( tColsSet )
        #
        tValsSet        = getSequence( tValsSet )
        #
        lColsValues     = iZip( tColsSet, tValsSet )
        #
        lTypesValues    = [ ( dColsTypes[ sCol ], uValue ) for sCol, uValue in lColsValues ]
        #
        tValsSet        = [ getTypeCastValue( sType, uValue ) for sType, uValue in lTypesValues ]
        #
    #
    sWheres             = getMeetsConditions( tColsWhere, tValsWhere, tWhereOper )
    #
    #
    sSets               = setColsEqualsValues( tColsSet, tValsSet )
    #
    #
    sUpdate             = "update %s set %s where %s" % ( sTable, sSets, sWheres )
    #
    return sUpdate



def doUpdate(
        oCursor,
        oDbApi,
        sTable,
        tColsSet,
        tValsSet,
        tColsWhere,
        tValsWhere,
        tWhereOper      = None,
        oValFormatter   = None,
        bRaiseError     = 1 ):
    #
    sUpdateStatement    = getUpdateStatement(
                            sTable,
                            tColsSet,       tValsSet,
                            tColsWhere,     tValsWhere,
                            tWhereOper      = tWhereOper,
                            oDbApi          = oDbApi,
                            oValFormatter   = oValFormatter, )
    #
    bGotError           = 0
    #
    try:
        #
        oCursor.execute( sUpdateStatement )
        #
    except:
        #
        bGotError       = 1
        #
        if bRaiseError:
            print3( sUpdateStatement )
            raise
    #
    if bRaiseError:
        return sUpdateStatement
    else:
        return bGotError



def doUpdateOrError(
        oCursor,
        oDbApi,
        sTable,
        tColsSet,
        tValsSet,
        tColsWhere,
        tValsWhere,
        tWhereOper      = None,
        oValFormatter   = None ):
    #
    bGotError = \
        doUpdate(
            oCursor,
            oDbApi,
            sTable,
            tColsSet,
            tValsSet,
            tColsWhere,
            tValsWhere,
            tWhereOper      = tWhereOper,
            oValFormatter   = oValFormatter,
            bRaiseError     = 0 )
    #
    return bGotError



def _GetColsGetDefs( sTable, oDbApi, sType ):
    #
    dColsTypes      = oDbApi.dTables[ sTable ].dColsTypes
    #
    def isItemOfType( tItem ):
        #
        sCol, sColType = tItem
        #
        return sColType == sType
    #
    return isItemOfType, dColsTypes


def _getColsGotType( sTable, oDbApi, sType ):
    #
    from Iter.AllVers   import iFilter
    from Collect.Get    import getKeyListOffItems
    from Dict.Get       import getItemIter
    #
    isItemOfType, dColsTypes = _GetColsGetDefs( sTable, oDbApi, sType )
    #
    lItemsOfType    = iFilter( isItemOfType, getItemIter( dColsTypes ) )
    #
    return getKeyListOffItems( lItemsOfType )


def _getOneColGotType( sTable, oDbApi, sType ):
    #
    from Collect.Query  import get1stThatMeets
    from Dict.Get       import getItemIter
    #
    isItemOfType, dColsTypes = _GetColsGetDefs( sTable, oDbApi, sType )
    #
    tColType = get1stThatMeets( getItemIter( dColsTypes ), isItemOfType )
    #
    if tColType is None:
        #
        sWantCol = None
        #
    else:
        #
        sWantCol, sType = tColType
        #
    #
    return sWantCol


def _getSerialKeyCol( sTable, oDbApi ):
    #
    sSerialCol      = _getOneColGotType( sTable, oDbApi, 'serial' )
    #
    return sSerialCol



def _getRecycleOldRow(
        sTable,
        cTimeStampCol,
        iDaysOld,
        tWhereCols      = (),
        tWhereVals      = [],
        tWhereOper      = None,
        oCursor         = None,
        oDbApi          = None,
        oValFormatter   = None ):
    #
    from Time.Test      import isISOdatetime
    from Time.Delta     import getDeltaDaysFromStrings
    from DbApi.Format   import FixOneItemTuple
    from DbApi.Query    import getSelection
    #
    tOldRecord = \
        FixOneItemTuple(
            getSelection(
                oCursor,
                oDbApi,
                sTable,
                'min',
                uWantCols       = cTimeStampCol,
                tWhereCols      = tWhereCols,
                tWhereVals      = tWhereVals,
                tWhereOper      = tWhereOper,
                oValFormatter   = oValFormatter ) )
    #
    sSerialCol      = _getSerialKeyCol( sTable, oDbApi )
    #
    iOldRecord      = None
    #
    if      tOldRecord                  and \
            isISOdatetime( tOldRecord ) and \
            getDeltaDaysFromStrings( tOldRecord ) >= iDaysOld:
        #
        iOldRecord = \
            FixOneItemTuple(
                getSelection(
                    oCursor,
                    oDbApi,
                    sTable,
                    sGetWhich       = 'one',
                    uWantCols       = sSerialCol,
                    tWhereCols      = cTimeStampCol,
                    tWhereVals      = tOldRecord,
                    oValFormatter   = oValFormatter ) )
            #
        #
    #
    return iOldRecord, sSerialCol



def doInsertOrUpdate(
        sTable,
        cTimeStampCol,
        iDaysOld,
        tWhereCols      = (),
        tWhereVals      = [],
        tWhereOper      = None,
        tColsSet        = (),
        tValsSet        = (),
        oCursor         = None,
        oDbApi          = None,
        oValFormatter   = None,
        oDBConnect      = None ):
    #
    """
    This will update if possible, otherwise it will insert.
    Sending oDBConnect is optional: send it, and the script will commit().
    """
    #
    iOldRecord, sSerialCol = \
        _getRecycleOldRow(
            sTable,
            cTimeStampCol,
            iDaysOld        = iDaysOld,
            tWhereCols      = tWhereCols,
            tWhereVals      = tWhereVals,
            tWhereOper      = tWhereOper,
            oCursor         = oCursor,
            oDbApi          = oDbApi,
            oValFormatter   = oValFormatter )
    #
    if iOldRecord is None:
        #
        sSQL = \
            doInsert(
                oCursor,
                oDbApi,
                sTable,
                tColsSet        = tColsSet,
                tValsSet        = tValsSet,
                oValFormatter   = oValFormatter )
        #
        #
    else:
        #
        sSQL = \
            doUpdate(
                oCursor,
                oDbApi,
                sTable,
                tColsSet        = tColsSet,
                tValsSet        = tValsSet,
                tColsWhere      = sSerialCol,
                tValsWhere      = iOldRecord,
                oValFormatter   = oValFormatter ) # were tuples
        #
    #
    if oDBConnect:
        #
        oDBConnect.commit()
        #
    #
    return sSQL



def doDelete(
        oCursor,
        oDbApi,
        sTable,
        tWhereCols      = None,
        tWhereVals      = None,
        tWhereOper      = None,
        oValFormatter   = None ):
    #
    from DbApi.Format import getTypeCaster
    from DbApi.Query  import getLimitClause
    #
    sWhere              = ''
    #
    getTypeCastValue    = getTypeCaster( oValFormatter )
    #
    if tWhereCols:
        #
        sWhere          = getLimitClause(
                            sTable,
                            tWhereCols,
                            tWhereVals,
                            tWhereOper,
                            oDbApi              = oDbApi,
                            getTypeCastValue    = getTypeCastValue )
    #
    sDeleteStatement    = 'delete from %s%s;' % ( sTable, sWhere )
    #
    try:
        oCursor.execute( sDeleteStatement )
    except:
        print3( sDeleteStatement )
        raise
    #
    return sDeleteStatement





if __name__ == "__main__":
    #
    from DbApi.Connect  import getConf, getConnected
    from DbApi.Create   import CreateDatabase, DropDataBase
    from DbApi.Insert   import doInsert
    from DbApi.Format   import ValueFormatterClass
    from DbApi.Test     import hasDataBase
    from Time.Output    import getNowIsoDateTimeStr
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
        oDBConnect, oCursor = getConnected( oDbApi, oConf )
        #
        oValFormatter   = ValueFormatterClass( oConf = oConf )
        #
        sTable          = 'Package'
        #
        tColsSet        = ( 'iPackage', 'sPackage' )
        #
        tValues         = (          0,   'python' )
        #
        doInsert(   oCursor, oDbApi,
                    sTable, tColsSet, tValues, oValFormatter = oValFormatter )
        #
        tValsSet        = (          1,   'perl' )
        tColsWhere      = ( 'iPackage', )
        tValsWhere      = (          0, )
        #
        sUpdate = getUpdateStatement(
                sTable,
                tColsSet,       tValsSet,
                tColsWhere,     tValsWhere,
                tWhereOper      = None,
                oDbApi          = oDbApi,
                oValFormatter   = oValFormatter )
        #
        if sUpdate != \
            "update Package set iPackage = 1, sPackage = 'perl' where iPackage = 0":
            #
            lProblems.append( 'doUpdate() returned incorrect statement for %s' % sThisRun )
            #
        #
        #
        if doUpdate(
                oCursor,
                oDbApi,
                sTable,
                tColsSet,
                tValsSet,
                tColsWhere,
                tValsWhere,
                tWhereOper      = None,
                oValFormatter   = oValFormatter ) != sUpdate:
            #
            lProblems.append( 'doUpdate() failed for %s' % sThisRun )
            #
        #
        isItemOfType, dColsTypes = _GetColsGetDefs( sTable, oDbApi, 'serial' )
        #
        dWantTypes  = { 'iPackage': 'serial',
                        'sPackage': 'varchar',
                        'tPackage': 'timestamp' }
        #
        if dColsTypes != dWantTypes or \
                not isItemOfType( ( 'iPackage', 'serial' ) ):
            #
            lProblems.append( '_GetColsGetDefs() not working for %s' % sThisRun )
            #
        #
        tTypes = (  'char',
                    'integer',
                    'serial',
                    'timestamp',
                    'varchar', )
        #
        lCols4Type  = [ _getColsGotType( sTable, oDbApi, sType )
                        for sType in tTypes ]
        #
        if lCols4Type != [[], [], ['iPackage'], ['tPackage'], ['sPackage']]:
            #
            lProblems.append( '_getColsGotType() not working for %s' % sThisRun )
            #
        #
        lCol4Type   = [ _getOneColGotType( sTable, oDbApi, sType )
                        for sType in tTypes ]
        #
        if lCol4Type != [None, None, 'iPackage', 'tPackage', 'sPackage']:
            #
            lProblems.append( '_getOneColGotType() not working for %s' % sThisRun )
            #
        #
        if _getSerialKeyCol( sTable, oDbApi ) != 'iPackage':
            #
            lProblems.append( '_getSerialKeyCol() not working for %s' % sThisRun )
            #
        #
        sTable, cTimeStampCol = 'PkgLag', 'tPkgLag'
        #
        tColsSet    = (
            'iPackage',
            'sPkgEpoch',
            'sPkgVers',
            'sRelease',
            'sPkgArch',
            'iDir',
            'sExt',
            'iLag',
            'tPkgLag' )
        #
        tValues     = (
            1,
            '8',
            '4.88',
            'abc',
            'i386',
            8,
            'rpm',
            '9',
            '2006-08-08 18:48:48' )
        #
        doInsert(   oCursor, oDbApi,
                    sTable, tColsSet, tValues, oValFormatter = oValFormatter )
        #
        if oDBConnect: oDBConnect.commit()
        #
        iDaysOld        = 10
        #
        iOldRecord, sSerialCol = \
            _getRecycleOldRow(
                    sTable,
                    cTimeStampCol,
                    iDaysOld,
                    tWhereCols      = (),
                    tWhereVals      = [],
                    tWhereOper      = None,
                    oCursor         = oCursor,
                    oDbApi          = oDbApi,
                    oValFormatter   = oValFormatter )
        #
        if ( iOldRecord, sSerialCol ) != ( 1, 'iPkgLag' ):
            #
            lProblems.append( '_getRecycleOldRow() not working for %s' % sThisRun )
            #
        #
        sNow            = getNowIsoDateTimeStr()
        #
        tValues = (
            1,
            '8',
            '4.88',
            'abc',
            'i386',
            8,
            'rpm',
            '9',
            sNow )
        #
        #
        sSQL =  "update PkgLag set iPackage = 1, " \
                "sPkgEpoch = '8', sPkgVers = '4.88', sRelease = 'abc', " \
                "sPkgArch = 'i386', iDir = 8, sExt = 'rpm', iLag = 9, " \
                "tPkgLag = '%s' where iPkgLag = 1"
        #
        sSQL =  sSQL % sNow
        #
        #
        if sSQL != \
            doInsertOrUpdate(
                sTable,
                cTimeStampCol,
                iDaysOld,
                tWhereCols      = (),
                tWhereVals      = [],
                tWhereOper      = None,
                tColsSet        = tColsSet,
                tValsSet        = tValues,
                oCursor         = oCursor,
                oDbApi          = oDbApi,
                oValFormatter   = oValFormatter ):
            #
            lProblems.append( 'doInsertOrUpdate() update for %s' % sThisRun )
            #
        #
        tValues = (
            2,
            '18',
            '8.88',
            'xyz',
            'i386',
            18,
            'rpm',
            '9',
            '2006-08-28 18:48:48' )
        #
        sSQL =  "insert into PkgLag( " \
                    "iPackage, sPkgEpoch, sPkgVers, sRelease, " \
                    "sPkgArch, iDir, sExt, iLag, tPkgLag ) " \
                "values( " \
                    "2, '18', '8.88', 'xyz', 'i386', 18, 'rpm', 9, " \
                        "'2006-08-28 18:48:48' )"
        #
        if sSQL != \
            doInsertOrUpdate(
                sTable,
                cTimeStampCol,
                iDaysOld,
                tWhereCols      = (),
                tWhereVals      = [],
                tWhereOper      = None,
                tColsSet        = tColsSet,
                tValsSet        = tValues,
                oCursor         = oCursor,
                oDbApi          = oDbApi,
                oValFormatter   = oValFormatter ):
            #
            lProblems.append( 'doInsertOrUpdate() update for %s' % sThisRun )
            #
        #
        sDelete = \
            doDelete(oCursor,
                    oDbApi,
                    sTable,
                    tWhereCols      = ( 'tPkgLag', ),
                    tWhereVals      = ( '2006-08-28 18:48:48', ),
                    tWhereOper      = None,
                    oValFormatter   = oValFormatter )
        #
        #
        if sDelete != \
                "delete from PkgLag where tPkgLag = '2006-08-28 18:48:48';":
            #
            lProblems.append( 'doDelete() failed for %s' % sThisRun )
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