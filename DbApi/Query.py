#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# DbApi functions Query
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
# Copyright 2004-2011 Rick Graves
#

from String.Transform   import getSwapper

setMinMax               = frozenset( ( 'min', 'max' ) )

oWhereSyntaxSwapper     = getSwapper(
    {   " = 'null'"     : ' is null',
        " = null"       : ' is null',
        " = 'not null'" : ' is not null',
        " = not null"   : ' is not null',
        " != null"      : ' is not null',
        " = ("          : ' in (',
        " = ["          : ' in (',
        "]"             : ')'           } )

setAggregates = frozenset( ( 'count', 'min', 'max', 'sum', 'avg' ) )

class WrongParamsExcept(Exception): pass



def _getColEqualsValueList( tColumns, tValues, tCompOperators = None ):
    #
    from Iter.AllVers import iMap, iZip
    #
    lValues             = iMap( str, tValues )
    #
    if not tCompOperators:
        #
        tCompOperators  = [ '=' ] * len( tColumns )
        #
    #
    lColsValues         = [ '%s %s %s' % ( sColumn, sCompOperator, sValue )
                            for sColumn, sCompOperator, sValue
                            in iZip( tColumns, tCompOperators, lValues ) ]
    #
    return lColsValues



def setColsEqualsValues( tColumns, tValues, tCompOperators = None ):
    #
    lColsValues = _getColEqualsValueList( tColumns, tValues, tCompOperators )
    #
    return ', '.join( lColsValues )



def getMeetsConditions( tColumns, tValues, tCompOperators = None, bWhereAnd = 1 ):
    #
    from Iter.AllVers import iMap
    #
    lValues         = iMap( str, tValues )
    #
    lConditions     = _getColEqualsValueList( tColumns, lValues, tCompOperators )
    #
    if bWhereAnd:
        sJoin = ' and '
    else:
        sJoin = ' or '
        #
    #
    return oWhereSyntaxSwapper( sJoin.join( lConditions ) )



def _getCols4Statement( uWantCols, sGetWhich ):
    #
    from Iter.Test      import isIterable
    from DbApi.Format   import CommaSeparated
    #
    if      uWantCols and isIterable( uWantCols ):
        #
        if len( uWantCols ) > 1:
            #
            sWantCols   = CommaSeparated( uWantCols )
            #
        else:
            #
            sWantCols   = uWantCols[0]
            #
    else:
        #
        sWantCols       = uWantCols
        #
    #
    if sGetWhich in setMinMax:
        #
        sWantCols       = '%s( %s )' % ( sGetWhich, sWantCols )
        #
    #
    return sWantCols



def getTableKeyOffName( sTable ):
    #
    sTableKey   = sTable
    #
    if sTable.startswith( 'temp' ):
        #
        sTableKey   = sTable[ 4 : ]
        #
    #
    return sTableKey



def getLimitClause(
        sTable,
        tLimitCols,
        tLimitVals,
        tLimitOper          = None,
        bLimitAnd           = 1,
        oDbApi              = None,
        getTypeCastValue    = None,
        sLimit              = 'where' ):
    #
    from DbApi.Format   import getSequence, FixOneItemTuple
    from Iter.AllVers   import iZip
    #
    tLimitCols          = getSequence( tLimitCols )
    #
    tLimitVals          = getSequence( tLimitVals )
    #
    lLimitValues        = []
    #
    if oDbApi:
        #
        sTableKey       = getTableKeyOffName( sTable )
        #
        dColsTypes      = oDbApi.dTables[ sTableKey ].dColsTypes
        #
        lColsValues     = iZip( tLimitCols, tLimitVals )
        #
        try:
            lTypesValues    = [
                ( dColsTypes[ sCol ], FixOneItemTuple( uValue ) )
                        for sCol, uValue in lColsValues ]
        except:
            print3( sCol )
            raise
        #
        # print3( lTypesValues )
        lLimitValues    = [ getTypeCastValue( sType, uValue )
                            for sType, uValue in lTypesValues ]
        #
    #
    #
    sLimit  = ' %s %s' % (
                sLimit,
                getMeetsConditions(
                    tLimitCols, lLimitValues, tLimitOper, bLimitAnd ) )
    #
    return sLimit



def _getSelectStatement(
        sTable,
        uWantCols       = ('*',),
        tWhereCols      = (),
        tWhereVals      = [],
        tWhereOper      = None,
        bWhereAnd       = 1,
        oDbApi          = None,
        oValFormatter   = None,
        tOrderByCols    = (), bOrderByDesc = 0,
        uDistinctCols   = None,
        sManualWhere    = None,
        tHavingCols     = (),
        tHavingVals     = None,
        tHavingOper     = None,
        bHavingAnd      = 1,
        sGetWhich       = '',
        bForUpdate      = 0,
        iLimit          = 0 ):
    #
    from DbApi.Format   import getTypeCaster
    from DbApi.Connect  import setForUpdates
    #
    sWantCols           = _getCols4Statement( uWantCols, sGetWhich )
    #
    sWhere              = ''
    #
    getTypeCastValue   = getTypeCaster( oValFormatter )
    #
    sTableKey           = getTableKeyOffName( sTable )
    #
    if sManualWhere:
        #
        sWhere          = ' %s' % sManualWhere.strip()
        #
    elif tWhereCols:
        #
        sWhere          = getLimitClause(
                            sTable,
                            tWhereCols,
                            tWhereVals,
                            tWhereOper,
                            bWhereAnd,
                            oDbApi,
                            getTypeCastValue )
    #
    bSelectDistinct         = 0
    #
    if uWantCols == uDistinctCols:
        #
        bSelectDistinct     = 1
        #
    elif uDistinctCols is None:
        #
        uDistinctCols       = ''
        #
    elif isIterable( uDistinctCols ):
        #
        uDistinctCols       = CommaSeparated( uDistinctCols )
        #
    else:
        #
        uDistinctCols       = uDistinctCols
        #
    #
    sSelectDistinct         = ''
    #
    bGetDistinctOn          = 0
    #
    if bSelectDistinct:
        #
        sSelectDistinct     = 'DISTINCT '
        #
    elif uDistinctCols:
        #
        if oDbApi.sSystemSQL == 'postgresql':
            #
            sSelectDistinct = 'DISTINCT ON ( %s ) ' % uDistinctCols
            #
        else:
            #
            bGetDistinctOn  = 1
            #
    #
    sHaving                 = ''
    #
    if tHavingCols and tHavingVals is not None:
        #
        sHaving = getLimitClause(
                    sTable,
                    tHavingCols,
                    tHavingVals,
                    tHavingOper,
                    bHavingAnd,
                    oDbApi,
                    getTypeCastValue,
                    sLimit              = 'having'  )
        #
    #
    sOrderBy                = ''
    #
    if tOrderByCols:
        #
        sOrderByCols        = _getCols4Statement( tOrderByCols, sGetWhich )
        #
        sOrderByDesc        = ''
        #
        if bOrderByDesc:
            #
            sOrderByDesc    = ' desc'
        #
        sOrderBy            = ' order by %s%s' % ( sOrderByCols, sOrderByDesc )
        #
    #
    sForUpdate              = ''
    #
    if bForUpdate and oDbApi.sSystemSQL in setForUpdates:
        #
        sForUpdate          = ' for update'
        #
    #
    sLimit                  = ''
    #
    if iLimit:
        #
        sLimit              = ' limit %s' % iLimit
        #
    #
    sSelect                 = 'select %s%s from %s%s%s%s%s%s' % (
                                sSelectDistinct, sWantCols, sTable, sWhere,
                                sHaving, sOrderBy, sForUpdate, sLimit )
    #
    return sSelect.strip(), bGetDistinctOn




def getSelection(
        oCursor,
        oDbApi,
        sTable,
        sGetWhich       = 'all',
        uWantCols       = '*',
        tWhereCols      = (),
        tWhereVals      = [],
        tWhereOper      = None,
        bWhereAnd       = 1,
        oValFormatter   = None,
        tOrderByCols    = (), bOrderByDesc = 0,
        uDistinctCols   = None,
        bPrintSQL       = 0,
        sManualWhere    = None,
        tHavingCols     = (),
        tHavingVals     = [],
        tHavingOper     = None,
        bHavingAnd      = 1,
        bForUpdate      = 0,
        iLimit          = 0,
        bPrintQuery     = 1 ):
    #
    from Collect.Test   import isListOrTuple
    from DbApi.Fetch    import dGetFetch, setSingleValue
    from DbApi.Format   import getSequence, getMembersStripped
    #
    sSelect, bGetDistinctOn = \
        _getSelectStatement(
                sTable,
                uWantCols       = uWantCols,
                tWhereCols      = tWhereCols,
                tWhereVals      = tWhereVals,
                tWhereOper      = tWhereOper,
                bWhereAnd       = bWhereAnd,
                oDbApi          = oDbApi,
                oValFormatter   = oValFormatter,
                tOrderByCols    = tOrderByCols,
                bOrderByDesc    = bOrderByDesc,
                uDistinctCols   = uDistinctCols,
                sManualWhere    = sManualWhere,
                tHavingCols     = tHavingCols,
                tHavingVals     = tHavingVals,
                tHavingOper     = tHavingOper,
                bHavingAnd      = bHavingAnd,
                sGetWhich       = sGetWhich,
                bForUpdate      = bForUpdate,
                iLimit          = iLimit )
    #
    try:
        oCursor.execute( sSelect )
    except:
        if bPrintQuery:
            print3( sSelect )
        raise
    #
    if bPrintSQL:
        #
        print3( sSelect )
    #
    getFetch        = dGetFetch[ sGetWhich ]
    #
    uReturn         = getFetch( sSelect, oCursor )
    #
    sTableKey       = getTableKeyOffName( sTable )
    #
    if sGetWhich != 'count':
        #
        if uWantCols == '*':
            #
            lCols   = oDbApi.dTables[ sTableKey ].lCols
            #
            lTypes  = [ d['type'] for d in lCols ]
            #
        else:
            #
            dColsTypes  = oDbApi.dTables[ sTableKey ].dColsTypes
            #
            uWantCols   = getSequence( uWantCols )
            #
            try:
                lTypes      = [ dColsTypes[ sCol ] for sCol in uWantCols ]
            except:
                print3( sCol )
                print3( uWantCols )
                print3( dColsTypes )
                raise
        #
        lStrips         = [ sType == 'char' for sType in lTypes ]
        #
        if True in lStrips and uReturn:
            #
            if sGetWhich == 'one':
                #
                pass # uReturn = uReturn
                #
            elif sGetWhich == 'all-big':
                #
                uReturn = getStripIterator( uReturn, lStrips )
                #
            else:
                #
                uReturn = [ getMembersStripped( tRow, lStrips ) for tRow in uReturn ]
                #
            #
        #
    #
    if bGetDistinctOn:
        #
        pass
        #
    #
    if uReturn and sGetWhich in setSingleValue and type( uReturn ) == tuple:
        #
        uReturn     = uReturn[0]
    #
    return uReturn


def _getAggregateQuery(
        sTable,
        sAggregate      = 'count',
        tWhereCols      = (),
        tWhereVals      = (),
        tWhereOper      = None,
        bWhereAnd       = 1,
        oDbApi          = None,
        oValFormatter   = None,
        uDistinctCols   = None, ):
    #
    if sAggregate not in setAggregates:
        #
        # 'count', 'min', 'max', 'sum', 'avg'
        #
        print3( 'need one of these: %s' % ', '.join( list( setAggregates ) ) )
        raise WrongParamsExcept
    #
    if uDistinctCols is None:
        #
        uWantCols       = '%s(*)' % sAggregate
        #
    else:
        #
        #
        uWantCols       = '%s( distinct %s )' % ( sAggregate, uDistinctCols )
        #
    #
    sSelect, bGetDistinctOn = \
        _getSelectStatement(
            sTable,
            uWantCols       = uWantCols,
            tWhereCols      = tWhereCols,
            tWhereVals      = tWhereVals,
            tWhereOper      = tWhereOper,
            bWhereAnd       = bWhereAnd,
            oDbApi          = oDbApi,
            oValFormatter   = oValFormatter )
    #
    return sSelect



def getAggregateResult(
        sAggregate,
        oDbApi,
        sTable,
        tWhereCols      = (),
        tWhereVals      = (),
        tWhereOper      = None,
        oValFormatter   = None,
        uDistinctCols   = None,
        bPrintQuery     = 1 ):
    #
    '''
    'count', 'min', 'max', 'sum', 'avg'
    '''
    #
    # not tested yet!!!
    #
    sAggregate = sAggregate.lower()
    #
    if sAggregate not in setAggregates:
        #
        print3( 'need one of these: %s' % ', '.join( list( setAggregates ) ) )
        raise WrongParamsExcept
        #
    #
    sQuery = _getAggregateQuery(
        sTable,
        sAggregate      = sAggregate,
        tWhereCols      = tWhereCols,
        tWhereVals      = tWhereVals,
        tWhereOper      = tWhereOper,
        oDbApi          = oDbApi,
        oValFormatter   = oValFormatter,
        uDistinctCols   = uDistinctCols )
    #
    try:
        oCursor.execute( sQuery )
    except:
        if bPrintQuery:
            print3( sQuery )
        #
        raise
    #
    return oCursor.fetchone()[0]



def _getCountQuery(
        sTable,
        tWhereCols      = (),
        tWhereVals      = (),
        tWhereOper      = None,
        oDbApi          = None,
        oValFormatter   = None,
        uDistinctCols   = None, ):
    #
    return _getAggregateQuery(
        sTable,
        sAggregate      = 'count',
        tWhereCols      = tWhereCols,
        tWhereVals      = tWhereVals,
        tWhereOper      = tWhereOper,
        oDbApi          = oDbApi,
        oValFormatter   = oValFormatter,
        uDistinctCols   = uDistinctCols )



def getCount(
        oCursor,
        oDbApi,
        sTable,
        tWhereCols      = (),
        tWhereVals      = (),
        tWhereOper      = None,
        oValFormatter   = None,
        uDistinctCols   = None,
        bPrintQuery     = 1 ):
    #
    sCountQuery = _getCountQuery(
        sTable, tWhereCols, tWhereVals, tWhereOper, oDbApi, oValFormatter, uDistinctCols )
    #
    try:
        oCursor.execute( sCountQuery )
    except:
        if bPrintQuery:
            print3( sCountQuery )
        #
        raise
    #
    iCount              = oCursor.fetchone()[0]
    #
    return iCount




def getCountDistinct(
            oConf,
            oCursor,
            sTable,
            uDistinctCols   = None,
            tWhereCols      = (),
            tWhereVals      = (),
            tWhereOper      = None,
            oDbApi          = None,
            oValFormatter   = None ):
    #
    from Collect.Test   import isListOrTuple
    from Iter.Test      import isIterator
    #
    sSystemSQL  = oConf.get( 'main', 'sSystemSQL' )
    #
    if      sSystemSQL == 'sqlite' or \
            ( ( isListOrTuple( uDistinctCols ) or isIterator( uDistinctCols ) ) and
              len( uDistinctCols ) > 1 ):
        #
        iCount  = \
            getSelection(
                oCursor         = oCursor,
                oDbApi          = oDbApi,
                sTable          = sTable,
                sGetWhich       = 'count',
                uWantCols       = uDistinctCols,
                tWhereCols      = tWhereCols,
                tWhereVals      = tWhereVals,
                tWhereOper      = tWhereOper,
                oValFormatter   = oValFormatter,
                uDistinctCols   = uDistinctCols )
        #
    else:
        #
        iCount              = getCount(
                                oCursor         = oCursor,
                                sTable          = sTable,
                                tWhereCols      = tWhereCols,
                                tWhereVals      = tWhereVals,
                                oDbApi          = oDbApi,
                                oValFormatter   = oValFormatter,
                                uDistinctCols   = uDistinctCols )
        #
    #
    return iCount




def getTempTable( sTable, oDbApi, oDBConnect, oCursor ):
    #
    # getCreateTableString( sTable, oTable, self.dColTypes )
    # for sTable, oTable in self.dTables items
    #
    from DbApi.Format   import getCreateTableString
    from DbApi.Test     import hasTable
    #
    sTempTable          = 'temp%s' % sTable
    #
    if hasTable( sTempTable, oDbApi, oDBConnect, oCursor ):
        #
        oCursor.execute( 'drop table %s;' % sTempTable )
        #
    #
    sCreateTemp     = \
        getCreateTableString(
                sTempTable,
                oDbApi.dTables[ sTable ],
                oDbApi.dColTypes, 1 )
    #
    oCursor.execute( sCreateTemp )
    #
    oDBConnect.commit()





def getTempTableFromTable(
        sTable,
        uWantCols       = ('*',),
        tWhereCols      = (),
        tWhereVals      = [],
        tWhereOper      = None,
        bWhereAnd       = 1,
        bOrderByDesc    = 0,
        uDistinctCols   = None,
        oDbApi          = None,
        oDBConnect      = None,
        oCursor         = None,
        oValFormatter   = None ):
    #
    # getCreateTableString( sTable, oTable, self.dColTypes )
    # for sTable, oTable in self.dTables items
    #
    from DbApi.Test     import hasTable
    #
    sTempTable          = 'temp%s' % sTable
    #
    if hasTable( sTempTable, oDbApi, oDBConnect, oCursor ):
        #
        oCursor.execute( 'drop table %s;' % sTempTable )
        #
    #
    sSelect, bGetDistinctOn = \
        _getSelectStatement(
            sTable,
            uWantCols       = uWantCols,
            tWhereCols      = tWhereCols,
            tWhereVals      = tWhereVals,
            tWhereOper      = tWhereOper,
            bWhereAnd       = bWhereAnd,
            oDbApi          = oDbApi,
            oValFormatter   = oValFormatter,
            bOrderByDesc    = bOrderByDesc,
            uDistinctCols   = uDistinctCols )
    #
    sCreateTemp     = 'create temp table %s as %s' % ( sTempTable, sSelect )
    #
    try:
        oCursor.execute( sCreateTemp )
    except:
        print3( sCreateTemp )
        raise
    #
    oDBConnect.commit()



def getAggQueryResultOrError( sQuery, oDBConnect ):
    #
    iAgg        = -1
    bError      =  0
    #
    try:
        #
        lAgg    = oDBConnect.query( sQuery ).dictresult()
        #
        dAgg    = lAgg[0]
        #
        for sAgg in ( 'count', 'min', 'max', 'sum', 'avg' ):
            #
            if sAgg in dAgg:
                #
                iAgg = dAgg[ sAgg ]
                #
                break
                #
            #
            #
    except:
        # print3( "Query error!" )
        # print3( sQuery )
        bError = 1
    #
    return iAgg, bError


def _getDicListResult( sSelect, oCursor ):
    #
    oCursor.execute( sSelect )
    #
    return oCursor.fetchall()



def _getDicListResultOrError( sSelect, oCursor ):
    #
    try:
        #
        oCursor.execute( sSelect )
        #
        return oCursor.fetchall(), 0
        #
    except:
        return [], 1



def NoListBackQuery( sQuery, oDBConnect ):
    #
    try:
        oDBConnect.query( sQuery )
    except:
        print3( "Query error!" )
        print3( sQuery )


# getAggregateResult not tested yet

if __name__ == "__main__":
    #
    from DbApi.Connect  import getConf, DbApiClass, getConnected
    from DbApi.Create   import CreateDatabase, DropDataBase, DropTable
    from DbApi.Format   import ValueFormatterClass, getTypeCaster, getSequence, \
                            FixOneItemTuple
    from DbApi.Insert   import doInsert
    from DbApi.Test     import hasTable, hasDataBase
    from Iter.AllVers   import tMap, iRange, iZip, tZip
    from Utils.Config   import NoConfigFile
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    # oValFormatter.getTypeCastValue
    #
    oDBConnect = oCursor = None
    #
    oConf, oDbApi = getConf( bNoConfigOK = 1 )
    #
    tPkgs = (
        'apt',
        'bluetooth',
        'cups',
        'dpkg',
        'eject',
        'firefox',
        'gcc',
        'gimp',
        'iceweasel',
        'kde3',
        'locale',
        'locate',
        'mozilla',
        'openoffice',
        'openssh',
        'perl',
        'python',
        'qt4',
        'ruby',
        'samba',
        'sane',
        'ssl',
        'sudo',
        'upstart',
        'w3m',
        'xine',
        'xorg', )
    #
    sThisRun            = 'sqlite'
    sConfigFile         = 'ConfNoExample.conf'
    tTypesCast      = ( '', '1' )
    #
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
        getTypeCastValue = getTypeCaster( oValFormatter )
        #
        # print3( "getTypeCastValue( 'bool', '1' ) =", getTypeCastValue( 'bool', '1' ), 'for', sThisRun )
        #
        sTable          =   'Package'
        tColsSet        = ( 'sPackage', )
        #
        dColsTypes      = oDbApi.dTables[ sTable ].dColsTypes
        #
        sType           = dColsTypes[ tColsSet[0] ]
        #
        for sPkg in tPkgs:
            #
            doInsert(
                oCursor, oDbApi, sTable, tColsSet,
                    ( getTypeCastValue( sType, sPkg ), ) )
            #
        #
        tColumns        = \
            ( 'iPkgLag', 'sPkgEpoch', 'tPkgLag',            'bNotActive' )
        tValues         = \
            (  2,        'Jurasic',   '2006-04-28 08:38:18', 1           )
        tCompOperators  = \
            ( '=',       '!=',        '<=',                 '='          )
        #
        sTable          = 'PkgLag'
        #
        sTableKey       = getTableKeyOffName( sTable )
        #
        tColsSet        = getSequence( tColumns )
        #
        tValsSet        = getSequence( tValues  )
        #
        lColsValues     = iZip( tColsSet, tValsSet )
        #
        dColsTypes      = oDbApi.dTables[ sTableKey ].dColsTypes
        #
        lTypesValues    = [ ( dColsTypes[ sCol ], FixOneItemTuple( uValue ) )
                            for sCol, uValue in lColsValues ]
        #
        lTypeCastVals    = [ getTypeCastValue( sType, uValue )
                            for sType, uValue in lTypesValues ]
        #
        if _getColEqualsValueList( tColsSet, lTypeCastVals, tCompOperators ) != \
                [   'iPkgLag = 2',
                    "sPkgEpoch != 'Jurasic'",
                    "tPkgLag <=%s '2006-04-28 08:38:18'" % tTypesCast[0],
                    "bNotActive = %s" % tTypesCast[1] ]:
            #
            print3( _getColEqualsValueList( tColsSet, lTypeCastVals, tCompOperators ) )
            lProblems.append( '_getColEqualsValueList() for %s' % sThisRun )
            #
        #
        if setColsEqualsValues( tColsSet, lTypeCastVals, tCompOperators ) != \
                "iPkgLag = 2, sPkgEpoch != 'Jurasic', " \
                "tPkgLag <=%s '2006-04-28 08:38:18', " \
                "bNotActive = %s" % tTypesCast:
            #
            # print3( setColsEqualsValues( tColumns, lTypeCastVals, tCompOperators ) )
            lProblems.append( 'setColsEqualsValues() for %s' % sThisRun )
            #
        #
        if getMeetsConditions(
                    tColsSet, lTypeCastVals, tCompOperators ) != \
                "iPkgLag = 2 and sPkgEpoch != 'Jurasic' and " \
                "tPkgLag <=%s '2006-04-28 08:38:18' and " \
                "bNotActive = %s" %  tTypesCast:
            #
            # print3( getMeetsConditions( tColumns, lTypeCastVals, tCompOperators ) )
            lProblems.append( 'getMeetsConditions() for %s, no bWhereAnd' % sThisRun )
            #
        #
        if getMeetsConditions(
                    tColsSet, lTypeCastVals, tCompOperators, bWhereAnd = 0 ) != \
                "iPkgLag = 2 or sPkgEpoch != 'Jurasic' or " \
                "tPkgLag <=%s '2006-04-28 08:38:18' or " \
                "bNotActive = %s" %  tTypesCast:
            #
            # print3( getMeetsConditions( tColumns, lTypeCastVals, tCompOperators, bWhereAnd = 0 ) )
            lProblems.append( 'getMeetsConditions() for %s with bWhereAnd' % sThisRun )
            #
        #
        if _getCols4Statement( tColsSet, 'all' ) != \
                'iPkgLag, sPkgEpoch, tPkgLag, bNotActive':
            #
            # print3( _getCols4Statement( tColumns, 'all' ) )
            lProblems.append( '_getCols4Statement() for %s' % sThisRun )
            #
        #
        if      getTableKeyOffName(          sTable ) != sTable or \
                getTableKeyOffName( 'temp' + sTable ) != sTable:
            #
            lProblems.append( 'getTableKeyOffName() for %s' % sThisRun )
            #
        #
        sWhere = getLimitClause(
                    sTable,
                    tColsSet,
                    tValsSet,
                    tLimitOper          = tCompOperators,
                    oDbApi              = oDbApi,
                    getTypeCastValue   = getTypeCastValue )
        #
        if sWhere != \
                " where iPkgLag = 2 and sPkgEpoch != 'Jurasic' and " \
                "tPkgLag <=%s '2006-04-28 08:38:18' and " \
                "bNotActive = %s" %  tTypesCast:
            #
            # print3( sWhere )
            lProblems.append( 'getLimitClause() with "and" for %s' % sThisRun )
            #
        #
        if getLimitClause(
                    sTable,
                    tColsSet,
                    tValsSet,
                    tLimitOper          = tCompOperators,
                    bLimitAnd           = 0,
                    oDbApi              = oDbApi,
                    getTypeCastValue   = getTypeCastValue ) != \
                " where iPkgLag = 2 or sPkgEpoch != 'Jurasic' or " \
                "tPkgLag <=%s '2006-04-28 08:38:18' or " \
                "bNotActive = %s" %  tTypesCast:
            #
            # print3( sWhere )
            lProblems.append( 'getLimitClause() with "or" for %s' % sThisRun )
            #
        #
        sSelect, bGetDistinctOn = \
            _getSelectStatement(
                sTable,
                uWantCols       = ('*',),
                tWhereCols      = (),
                tWhereVals      = [],
                tWhereOper      = None,
                bWhereAnd       = 1,
                oDbApi          = oDbApi,
                oValFormatter   = oValFormatter,
                tOrderByCols    = (),
                bOrderByDesc    = 0,
                uDistinctCols   = None,
                sManualWhere    = None,
                sGetWhich       = '' )
        #
        if      bGetDistinctOn or \
                sSelect != 'select * from PkgLag':
            #
            lProblems.append( '_getSelectStatement() simple for %s' % sThisRun )
            #
        #
        sSelect, bGetDistinctOn = \
            _getSelectStatement(
                sTable,
                uWantCols       = ('*',),
                tWhereCols      = tColsSet,
                tWhereVals      = tValsSet,
                tWhereOper      = tCompOperators,
                bWhereAnd       = 1,
                oDbApi          = oDbApi,
                oValFormatter   = oValFormatter,
                tOrderByCols    = (),
                bOrderByDesc    = 0,
                uDistinctCols   = None,
                sManualWhere    = None,
                sGetWhich       = '' )
        #
        if      bGetDistinctOn or \
                sSelect != "select * from PkgLag where iPkgLag = 2 and " \
                           "sPkgEpoch != 'Jurasic' and " \
                           "tPkgLag <=%s '2006-04-28 08:38:18' and " \
                           "bNotActive = %s" %  tTypesCast:
            #
            print3( sSelect )
            lProblems.append( '_getSelectStatement() with "and" where for %s' % sThisRun )
            #
        #
        sSelect, bGetDistinctOn = \
            _getSelectStatement(
                sTable,
                uWantCols       = ('*',),
                tWhereCols      = tColsSet,
                tWhereVals      = tValsSet,
                tWhereOper      = tCompOperators,
                bWhereAnd       = 0,
                oDbApi          = oDbApi,
                oValFormatter   = oValFormatter,
                tOrderByCols    = (),
                bOrderByDesc    = 0,
                uDistinctCols   = None,
                sManualWhere    = None,
                sGetWhich       = '' )
        #
        if      bGetDistinctOn or \
                sSelect != "select * from PkgLag where iPkgLag = 2 or " \
                           "sPkgEpoch != 'Jurasic' or " \
                           "tPkgLag <=%s '2006-04-28 08:38:18' or " \
                           "bNotActive = %s" %  tTypesCast:
            #
            lProblems.append( '_getSelectStatement() with "or" where for %s' % sThisRun )
            #
        #
        # iLag
        #
        sSelect, bGetDistinctOn = \
            _getSelectStatement(
                sTable,
                uWantCols       = ('*',),
                tWhereCols      = tColsSet,
                tWhereVals      = tValsSet,
                tWhereOper      = tCompOperators,
                bWhereAnd       = 0,
                oDbApi          = oDbApi,
                oValFormatter   = oValFormatter,
                tOrderByCols    = (),
                uDistinctCols   = None,
                sManualWhere    = None,
                tHavingCols     = 'iLag',
                tHavingVals     = 0,
                tHavingOper     = '>',
                bOrderByDesc    = 0,
                sGetWhich       = '' )
        #
        if      bGetDistinctOn or \
                sSelect != "select * from PkgLag where iPkgLag = 2 or " \
                           "sPkgEpoch != 'Jurasic' or " \
                           "tPkgLag <=%s '2006-04-28 08:38:18' or " \
                           "bNotActive = %s having iLag > 0" %  tTypesCast:
            #
            print3( sSelect )
            lProblems.append( '_getSelectStatement() with "having" for %s' % sThisRun )
            #
        #
        #
        sTable          = 'Package'
        #
        lSelected = \
            getSelection(
                oCursor,
                oDbApi,
                sTable,
                uWantCols       = '*',
                tWhereCols      = (),
                tWhereVals      = [],
                tWhereOper      = None,
                oValFormatter   = oValFormatter,
                tOrderByCols    = (),
                bOrderByDesc    = 0,
                uDistinctCols   = None,
                bPrintSQL       = 0,
                sManualWhere    = None,
                bPrintQuery     = 1 )
        #
        # print3( lSelected )
        def getStrOffUniCode( t ): return ( t[0], str( t[1] ) )
        #
        tSelected   = tMap( getStrOffUniCode, lSelected )
        #
        if tSelected != tZip( iRange( 1, len( tPkgs ) + 1 ), tPkgs ):
            #
            lProblems.append( 'getSelection() all for %s' % sThisRun )
            #
        #
        sCountQuery = \
            _getCountQuery(
                sTable,
                tWhereCols      = (),
                tWhereVals      = (),
                tWhereOper      = None,
                oDbApi          = oDbApi,
                oValFormatter   = oValFormatter,
                uDistinctCols   = None, )
        #
        if sCountQuery != 'select count(*) from Package':
            #
            lProblems.append( '_getCountQuery() no where for %s' % sThisRun )
            #
        #
        sCountQuery = \
            _getCountQuery(
                sTable,
                tWhereCols      = ( 'sPackage', ),
                tWhereVals      = ( 's%',       ),
                tWhereOper      = None,
                oDbApi          = oDbApi,
                oValFormatter   = oValFormatter,
                uDistinctCols   = None, )
        #
        if sCountQuery != "select count(*) from Package where sPackage = 's%'":
            #
            lProblems.append( '_getCountQuery() with where for %s' % sThisRun )
            #
        #
        iCount = \
            getCount(
                oCursor,
                oDbApi,
                sTable,
                tWhereCols      = (),
                tWhereVals      = (),
                tWhereOper      = None,
                oValFormatter   = oValFormatter,
                uDistinctCols   = None,
                bPrintQuery     = 1 )
        #
        if iCount != len( tPkgs ):
            #
            lProblems.append( 'getCount() simple for %s' % sThisRun )
            #
        #
        iCount = \
            getCountDistinct(
                    oConf,
                    oCursor,
                    sTable,
                    uDistinctCols   = 'sPackage',
                    tWhereCols      = (),
                    tWhereVals      = (),
                    tWhereOper      = None,
                    oDbApi          = oDbApi,
                    oValFormatter   = oValFormatter )
        #
        if iCount != len( tPkgs ):
            #
            lProblems.append( 'getCountDistinct() for %s' % sThisRun )
            #
        #
        getTempTable( sTable, oDbApi, oDBConnect, oCursor )
        #
        if not hasTable( 'temp' + sTable, oDbApi, oDBConnect, oCursor ):
            #
            lProblems.append( 'getTempTable() for %s' % sThisRun )
            #
        #
        DropTable( 'temp' + sTable, oDbApi, oDBConnect, oCursor )
        #
        getTempTableFromTable(
                sTable,
                uWantCols       = ('*',),
                tWhereCols      = (),
                tWhereVals      = [],
                tWhereOper      = None,
                bOrderByDesc    = 0,
                uDistinctCols   = None,
                oDbApi          = oDbApi,
                oDBConnect      = oDBConnect,
                oCursor         = oCursor,
                oValFormatter   = oValFormatter )
            #
        if not hasTable( 'temp' + sTable, oDbApi, oDBConnect, oCursor ):
            #
            lProblems.append( 'getTempTableFromTable() for %s' % sThisRun )
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
            tTypesCast  = ( ' timestamp', 'TRUE' )
            #
        else:   # quit after 2nd time through
            #
            break
            #
        #
    #
    sayTestResult( lProblems )