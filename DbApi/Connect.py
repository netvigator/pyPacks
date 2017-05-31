#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# DbApi functions Connect
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
oDbApi              = None

setSUPPORT_APIs       = frozenset( ( 'postgresql', 'sqlite' ) )
setForUpdates         = frozenset( ( 'postgresql',          ) )

setCONSTRAINTS_TABLE  = frozenset( ( 'PRIMARY KEY', 'UNIQUE', 'CHECK' ) )
setCONSTRAINTS_COL    = frozenset(
    ( 'NOT NULL', 'PRIMARY KEY', 'UNIQUE', 'CHECK', 'DEFAULT', 'COLLATE' ) )

tCOL_DICT_KEYS          = ( 'name', 'type', 'length', 'constraint' )

qPG_GET_COLS = '''
SELECT
  a.attname AS field,
  t.typname AS type,
  a.attlen AS length,
  a.attnotnull AS not_null
FROM
  pg_class c,
  pg_attribute a,
  pg_type t
WHERE
  c.relname = '%s'   AND
  a.attnum > 0       AND
  a.attrelid = c.oid AND
  a.atttypid = t.oid
ORDER BY a.attnum'''


class DbApiClass( object ):
    #
    def __init__( self, oConf, getTableDict ):
        #
        from Dict.Get import getItemIter
        #
        sSystemSQL = oConf.sSystemSQL
        #
        self.sSystemSQL = sSystemSQL.lower()
        #
        self.sConnectTo = None
        #
        if self.sSystemSQL   == 'postgresql':
            #
            from pgdb import connect
            from pg   import DatabaseError, InternalError, OperationalError
            #
            self.sConnectTo = 'template1'
            #
        elif self.sSystemSQL   == 'sqlite':
            #
            from pysqlite2.dbapi2 import connect, DatabaseError, \
                                        InternalError, OperationalError
            #
        #
        self.connect    = connect
        #
        self.InternalError  = InternalError
        self.DatabaseError  = DatabaseError
        self.OperationalError = OperationalError
        #
        # problem integer type is None
        # try Test.py
        #
        self.dColTypes   = \
            dict.fromkeys( (
                'bool',
                'char',
                'integer',
                'serial',
                'timestamp',
                'varchar', ) )
        #
        if self.sSystemSQL == 'sqlite':
            #
            dSqLiteTypes = {
                'bool'      : ( 'integer',  None            ),
                'char'      : ( 'text',     None            ),
                'serial'    : ( 'integer',  'AUTOINCREMENT' ),
                'timestamp' : ( 'text',     None            ),
                'varchar'   : ( 'text',     None            ) }
            #
            self.dColTypes.update( dSqLiteTypes )
            #
        #
        if getTableDict is not None:
            self.dTables, self.lIndexes = getTableDict()
        else:
            self.dTables, self.lIndexes = None, None
        #
    #
    def getCreateTableStatements( self, oDbApi, oDBConnect, oCursor ):
        #
        from DbApi.Test     import hasTable
        from DbApi.Format   import getCreateTableString
        #
        self.lTables = [ getCreateTableString( sTable, oTable, self.dColTypes )
                         for sTable, oTable in getItemIter( self.dTables )
                         if not hasTable(sTable,oDbApi,oDBConnect,oCursor) ]
        #
        return self.lTables, self.lIndexes
    #
    def getTableInfoOffDatabase( self ):
        #
        # lCols = [ dict( name = 'iPkgLag',       type = 'serial',    length =   0,
        #           constraint = 'NOT NULL PRIMARY KEY' ),
        #         ]
        #
        # lIndexes = []
        #
        #
        if self.dTables is None:
            #
            pass



def getConnectedOffParams(
        connect,
        sDataBase,
        sSystemSQL  = 'postgresql',
        host        = None,
        user        = None,
        password    = None ):
    #
    from os.path    import exists
    #
    if sSystemSQL == 'sqlite':
        bGotDatabase = exists( sDataBase )
        oDBConnect  = connect( database = sDataBase )
    else:
        oDBConnect  = connect(
                        database    = sDataBase,
                        host        = host,
                        user        = user,
                        password    = password )
    #
    oCursor     = oDBConnect.cursor()
    #
    return oDBConnect, oCursor


def _getNone4None( s ):
    #
    uReturn     = s
    #
    if s == 'None': uReturn = None
    #
    return uReturn


def getConnected( oDbApi, oConf ):
    #
    sHost       = _getNone4None( oConf.sHost     )
    sUser       = _getNone4None( oConf.sUser     )
    sPassword   = _getNone4None( oConf.sPassword )
    #
    return getConnectedOffParams(
            oDbApi.connect,
            oConf.sDataBase,
            oConf.sSystemSQL,
            sHost,
            sUser,
            sPassword  )



def getConf(
        sConfigFile = 'DbApiTest.conf',
        dDefaults   = None,
        bNoConfigOK = 0 ):
    #
    """
    getConfLite can find sConfigFile
    in the current directory or in the python path.
    """
    #
    from Utils.Config import getConfLite
    from DbApi.Create   import getExampleTableDict
    #
    if dDefaults is None:
        #
        dDefaults   = { 'main':
            dict(
                sSystemSQL  = 'sqlite',
                sDataBase   = 'TempSelfTest',
                sHost       = '',
                sUser       = '',
                sPassword   = '') }
        #
    #
    oConf   =   getConfLite(
                sConfigFile = sConfigFile,
                dDefaults   = dDefaults,
                bNoConfigOK = bNoConfigOK )
    #
    oDbApi = DbApiClass( oConf, getExampleTableDict )
    #
    return oConf, oDbApi



def getConfAndConnected(
        sConfigFile = 'ConfNoExample.conf',
        dDefaults   = None,
        bNoConfigOK = 0 ):
    #
    oConf, oDbApi       = getConf( sConfigFile, dDefaults, bNoConfigOK )
    #
    oDBConnect, oCursor = getConnected( oDbApi, oConf )
    #
    return oConf, oDbApi, oDBConnect, oCursor



def _getConnected4Create( oDbApi, oConf ):
    #
    # maybe not necessary
    #
    sConnectTo      = oConf.sDataBase
    #
    if oDbApi.sConnectTo is not None:
        #
        sConnectTo  = oDbApi.sConnectTo
        #
    #
    return getConnectedOffParams(
            oDbApi.connect,
            sConnectTo,
            oConf.sSystemSQL,
            oConf.sHost,
            oConf.sUser,
            oConf.sPassword )



def _getColComponents( uNameTypeConstr ):
    #
    from String.Get     import getTextBefore
    from String.Eat     import eatCharsOffEnd
    from String.Test    import isString
    from Dict.Get       import getDictOffPairOfLists
    from Iter.AllVers   import lMap
    #
    if isString( uNameTypeConstr ):
        lParts  = uNameTypeConstr.split( ' ' )
    else:
        lParts  = lMap( str, uNameTypeConstr )
    #
    sName, sType, sConstraint = \
        lParts[0], lParts[1], ' '.join( lParts[ 2 : ] )
    #
    lParts = sType.split( '(' )
    #
    sLen    = '0'
    #
    if len( lParts ) > 1:
        #
        sLen    = getTextBefore( lParts[1], ')' )
        #
        sType = lParts[0]
        #
    #
    sConstraint = eatCharsOffEnd( sConstraint, sEatThese = ' ,' )
    #
    if sType.endswith( ',' ): sType = sType[ : -1 ]
    #
    if sType == 'integer' and sConstraint.endswith( 'AUTOINCREMENT' ):
        #
        sType = 'serial'
        #
        sConstraint = getTextBefore( sConstraint, 'AUTOINCREMENT' )
        #
    #
    return getDictOffPairOfLists( tCOL_DICT_KEYS, ( sName, sType, int( sLen ), sConstraint.strip() ) )



def _getColDictList( lTableCols ):
    #
    from Iter.AllVers import lMap
    #
    return lMap( _getColComponents, lTableCols )



def _isCreateIndex( u ):
    #
    if u is not None:
        #
        sStr    = str( u )
        #
        return sStr.upper().startswith( 'CREATE INDEX' )



def getInfoOffDatabase( oDbApi, oConf ):
    #
    from Iter.AllVers   import iFilter, lMap, iRange, iZip
    #
    from DbApi.Create   import Append2TableDict
    from DbApi.Fetch    import getAllFetchList, getSingleColumnList
    #
    sSystemSQL = oConf.sSystemSQL
    #
    if sSystemSQL == 'sqlite':
        #
        oDBConnect, oCursor = _getConnected4Create( oDbApi, oConf )
        #
        sTableQ     = "SELECT  *  FROM sqlite_master WHERE type='table'"
        sIndexQ     = "SELECT sql FROM sqlite_master WHERE type='index'"
        #
        # oCursor.execute( sTableQ )
        #
        lTableInfo  = getAllFetchList( sTableQ, oCursor )
        #
        # oCursor.execute( sIndexQ )
        #
        lIndexInfo  = getAllFetchList( sIndexQ, oCursor )
        #
        lTables     = [ ( str( t[1] ), str( t[4] ) ) for t in lTableInfo
                        if  str( t[0] ) == 'table' and
                            str( t[1] ) != 'sqlite_sequence' ]
        #
        lCreateCols = [ str( t[1] ) for t in lTables ]
        #
        lTables     = [ str( t[0] ) for t in lTables ]
        #
        lCreateCols = [ s.split( '\n' ) for s in lCreateCols ]
        #
        for l in lCreateCols:
            #
            del l[0]
            del l[-1]
            #
        #
        lIndexes    = lMap( str,
                        iFilter( _isCreateIndex,
                            [ t[0] for t in lIndexInfo ] ) )
        #
        lConstraintsTable   = [ '' ] * len( lTables )
        #
        for iThisTable in iRange( len( lTables ) ):
            #
            sLastCreate = lCreateCols[ iThisTable ][ -1 ]
            #
            for sConstraint in setCONSTRAINTS_TABLE:
                #
                if sLastCreate.startswith( sConstraint ):
                    #
                    lConstraintsTable[ iThisTable ] = sLastCreate
                    #
                    del lCreateCols[ iThisTable ][ -1 ]
                    #
                    break
                    #
                #
            #
            lColSpecs       = lCreateCols[ iThisTable ]
            #
        #
        lCreateCols = [ _getColDictList( lTableCols )
                        for lTableCols in lCreateCols ]
        #
    elif sSystemSQL == 'postgresql':
        #
        oDBConnect, oCursor = getConnected( oDbApi, oConf )
        #
        sTableQ = "SELECT tablename FROM pg_tables " \
                  "WHERE tableowner = current_user"
        #
        # gets a list of the cols
        # sColQ4T = "SELECT attname from pg_class, pg_attribute " \
        #           "WHERE relname='%s' AND pg_class.oid=attrelid AND attnum > 0"
        #
        sPKQ4T  = "SELECT conkey FROM pg_constraint JOIN pg_class " \
                  "ON pg_class.oid=conrelid " \
                  "WHERE contype='p' AND relname = '%s'"
        #
        sIndexQ1= "SELECT tablename, indexname, indexdef FROM pg_indexes " \
                  "WHERE schemaname = 'public'"
        #
        # get indexes (incl PK)
        sIndexQ2= 'SELECT * from pg_indexes WHERE tablename = %s'
        #
        # oCursor.execute( sTableQ )
        #
        lTables = getSingleColumnList( sTableQ, oCursor )
        #
        def getTableCreateCols( sTable ):
            #
            sColQ   = qPG_GET_COLS % sTable # sColQ4T gets list only
            #
            # oCursor.execute( sColQ )
            #
            lCols   = getAllFetchList( sColQ, oCursor )
            #
            # need lots of manipulation
            #
            return lCols
        #
        lCreateCols = lMap( getTableCreateCols, lTables )
        #
        lCreateCols = [ _getColDictList( lTableCols )
                        for lTableCols in lCreateCols ]
        #
        lIndexes    = getAllFetchList( sIndexQ1, oCursor )
        #
        lConstraintsTable = [ '' ] * len( lCreateCols )
        #
    #
    #
    lCreates = iZip( lTables, lCreateCols, lConstraintsTable )
    #
    dTables     = {}
    #
    for sTable, lCols, sConstr in lCreates:
        #
        Append2TableDict( dTables, sTable, lCols, sConstr )
        #
    #
    return dTables, lIndexes




def getTestConnection( oConf, oDbApi, oDBConnect, oCursor, dTables ):
    #
    from DbApi.Query import getCount
    from Dict.Get    import getKeyTuple
    #
    sTable  = getKeyTuple( dTables )[0]
    #
    try:
        getCount( oCursor, oDbApi, sTable )
    except:
        oDBConnect, oCursor = getConnected( oDbApi, oConf )
    #
    #
    return oDBConnect, oCursor





if __name__ == "__main__":
    #
    lProblems = []
    #
    from six            import print_ as print3
    #
    from DbApi.Create   import getExampleTableDict
    from DbApi.Create   import DropDataBase, CreateDatabase
    from DbApi.Test     import hasDataBase
    from Dict.Get       import getKeyIter, getKeyTuple
    from Iter.AllVers   import iZip
    from String.Get     import getFrozenStringSetNotCaseSensitive as set
    from Utils.Config   import getConfLite, NoConfigFile
    from Utils.Result   import sayTestResult
    #
    dDefaults   = { 'main':
        dict(
            sSystemSQL  = 'sqlite',
            sDataBase   = 'TempSelfTest',
            sHost       = '',
            sUser       = '',
            sPassword   = '') }
    #
    oConf   =   getConfLite(
                sConfigFile = 'ConfNoExample.conf',
                dDefaults   = dDefaults,
                bNoConfigOK = 1 )
    #
    sThisRun            = 'sqlite'
    sConfigFile         = 'ConfNoExample.conf'
    #
    oDBConnect = oCursor = None
    #
    dGeneratedTypes = \
        dict(
            bool        = ('integer',),
            char        = ('text',),
            date        = ('text',),
            timestamp   = ('text',),
            varchar     = ('text',) )
    #
    def areTypesEquivalent( lOrig, lGenerated ):
        #
        bEquivalent     = 1
        #
        for ( sOrig, sGenerated ) in iZip( lOrig, lGenerated ):
            #
            if sOrig == sGenerated or sGenerated in dGeneratedTypes.get( sOrig, [] ):
                #
                pass
                #
            else:
                #
                bEquivalent = 0
                #
                print3( '%s != %s and dGeneratedTypes.get( %s ) returns %s' % \
                        ( sOrig, sGenerated, sOrig, dGeneratedTypes.get( sOrig ) ) )
                print3( '%s is of type %s and %s is of type %s' % \
                        ( sOrig, type( sOrig ), sGenerated, type( sGenerated ) ) )
                #
                break
        #
        return bEquivalent
    #
    while True:
        #
        sDataBase   = oConf.sDataBase
        sSystemSQL  = oConf.sSystemSQL
        #
        sHost       = oConf.sHost
        sUser       = oConf.sUser
        sPassword   = oConf.sPassword
        #
        bNoConfigOK = ( sThisRun == 'sqlite' )
        #
        if not oConf.sSystemSQL in setSUPPORT_APIs:
            #
            lProblems.append( 'getConfigOptions() %s' % sThisRun )
            #
        #
        #
        sSystemSQL  = oConf.sSystemSQL
        #
        oDbApi      = DbApiClass( oConf, getExampleTableDict )
        #
        sDataBase   = oConf.sDataBase
        #
        if not hasDataBase( sDataBase, oDbApi, sHost, sUser, sPassword ):
            #
            CreateDatabase( oConf, oDbApi, oDBConnect, oCursor )
            #
        #
        oDBConnect, oCursor = \
            getConnectedOffParams(
                oDbApi.connect,
                sDataBase,
                sSystemSQL,
                oConf.sHost,
                oConf.sUser,
                oConf.sPassword )
        #
        oConf, oDbApi, oDBConnect, oCursor = \
            getConfAndConnected( sConfigFile, None, bNoConfigOK )
        #
        dTables, lIndexes = getInfoOffDatabase( oDbApi, oConf )
        #
        dTablesOrig, lIndexesOrig = getExampleTableDict()
        #
        if      set( getKeyIter(     dTables ) ) != \
                set( getKeyIter( dTablesOrig ) ):
            #
            lTableProb = [
                'tables not right for %s' % sThisRun,
                'original:',
                repr( getKeyTuple( dTablesOrig ) ),
                'generated:',
                repr( getKeyTuple( dTables ) ) ]
            #
            lProblems.append( '\n     '.join( lTableProb ) )
            #
        else:
            #
            for sTableOrig in dTablesOrig:
                #
                oTableOrig  = dTablesOrig[ sTableOrig ]
                #
                oTableFake  = dTables.get( sTableOrig )
                #
                if not oTableFake: oTableFake = dTables.get( sTableOrig.lower() )
                #
                lColsOrig   = oTableOrig.lCols
                #
                lColsFake   = oTableFake.lCols
                #
                lColNamesOrig   = [ d[ 'name'   ] for d in lColsOrig ]
                lColTypesOrig   = [ d[ 'type'   ] for d in lColsOrig ]
                lColLensOrig    = [ d[ 'length' ] for d in lColsOrig ]
                #
                lColNamesFake   = [ d[ 'name'   ] for d in lColsFake ]
                lColTypesFake   = [ d[ 'type'   ] for d in lColsFake ]
                lColLensFake    = [ d[ 'length' ] for d in lColsFake ]
                #
                if      set( lColNamesOrig ) != \
                        set( lColNamesFake ):
                    #
                    lTableProb = [
                        'columns not right for table %s running under %s' % ( sTableOrig, sThisRun ),
                        'original:',
                        repr( lColNamesOrig ),
                        'generated:',
                        repr( lColNamesFake ) ]
                    #
                    lProblems.append( '\n     '.join( lTableProb ) )
                    #
                elif not areTypesEquivalent( lColTypesOrig, lColTypesFake ):
                    #
                    lTableProb = [
                        'column types not right for table %s running under %s' % ( sTableOrig, sThisRun ),
                        'original:',
                        repr( lColTypesOrig ),
                        'generated:',
                        repr( lColTypesFake ) ]
                    #
                    lProblems.append( '\n     '.join( lTableProb ) )
                    #
                #
                #
                # lCols = [
                #     dict( name = 'iPackage',      type = 'serial',    length =   0,
                #             constraint = 'NOT NULL PRIMARY KEY' ),
                #     dict( name = 'sPackage',      type = 'varchar',   length =  68,
                #             constraint = 'NOT NULL' ),
                #     ]
                # dTables[ sTableKey ]    = \
                #     ValueContainer(
                #         lCols = lCols, sConstr = sConstr, dColsTypes = dColsTypes )

            #
        #
        try:
            oDBConnect, oCursor = getTestConnection( oConf, oDbApi, oDBConnect, oCursor, dTables )
        except:
            #
            lProblems.append( 'getTestConnection() returned error for %s' % sThisRun )
            #
        #
        oDBConnect  = None
        oCursor     = None
        #
        if hasDataBase( sDataBase, oDbApi, sHost, sUser, sPassword ):
            #
            DropDataBase( oDbApi, oConf )
            #
            # does not always work the first time
            #
            if hasDataBase( sDataBase, oDbApi, sHost, sUser, sPassword ):
                #
                DropDataBase( oDbApi, oConf )
                #
            #
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
                sThisRun        = oConf.sSystemSQL
                #
                if sThisRun == 'sqlite':
                    #
                    lProblems.append( "No real database to test!" )
                    #
                    break
                    #
                elif sThisRun == 'postgresql':
                    #
                    dGeneratedTypes = \
                        dict(
                            char        = ('bpchar',),
                            date        = ('text',),
                            integer     = ('int4','int8'),
                            serial      = ('int4',) )
                    #
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