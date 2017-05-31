#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# DbApi functions Create
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

def _GetColTypesDict( lCols ):
    #
    return dict( [ ( d['name'], d['type'] ) for d in lCols ] )


def Append2TableDict( dTables, sTable, lCols, sConstr ):
    #
    """
    Used for created tables from table definitions.
    Append2TableDict updates dTables as a "byproduct",
    so there is no need to pass dTables back as a return value
    """
    #
    from Object.Get         import ValueContainer
    from DbApi.Query        import getTableKeyOffName
    #
    dColsTypes              = _GetColTypesDict( lCols )
    #
    sTableKey               = getTableKeyOffName( sTable )
    #
    dTables[ sTableKey ]    = \
        ValueContainer(
            lCols = lCols, sConstr = sConstr, dColsTypes = dColsTypes )
    #
    # updates dTables as a "byproduct",
    # so there is no need to pass dTables back as a return value



def _getCommandLine( sDataBase, sHost, sUser, sPassword ):
    #
    sCommand        = ''
    #
    if sHost:
        #
        sCommand    += '--host=%s ' % sHost
        #
    if sUser:
        #
        sCommand    += '--username=%s ' % sUser
        #
    if sPassword:
        #
        sCommand    += '--password=%s ' % sPassword
        #
    sCommand    += sDataBase
    #
    return sCommand



def DropDataBase( oDbApi, oConf ):
    #
    """
    """
    from commands       import getstatusoutput
    #
    from File.Del       import DeleteIfExists
    #
    sDataBase           = oConf.get( 'main', 'sDataBase'  )
    #
    if oDbApi.sSystemSQL == 'sqlite':
        #
        DeleteIfExists( sDataBase )
        #
    else:
        #
        sHost               = oConf.get( 'main', 'sHost'      )
        sUser               = oConf.get( 'main', 'sUser'      )
        sPassword           = oConf.get( 'main', 'sPassword'  )
        #
        sCommand            = \
            _getCommandLine(
                oConf.get( 'main', 'sDataBase' ), sHost, sUser, sPassword )
        #
        # print3( sCommand )
        #
        sDrop   = 'dropdb %s' % sCommand
        #
        iStatus, sOutput    = getstatusoutput( sDrop )
        #
        if iStatus: print3( sOutput )












def DropTable( sTable, oDbApi, oDBConnect, oCursor ):
    #
    from DbApi.Test import hasTable
    #
    if hasTable( sTable, oDbApi, oDBConnect, oCursor ):
        #
        oCursor.execute( 'drop table %s;' % sTable )
        #
        oDBConnect.commit()
        #
        if sTable in oDbApi.dTables:
            #
            del oDbApi.dTables[ sTable ]



def TableMustHaveAllCols( sTable, oDbApi, oDBConnect, oCursor ):
    #
    from DbApi.Format   import getTranslatedType, getCreateTableString
    from DbApi.Query    import getTableKeyOffName
    from DbApi.Test     import hasTable, hasColumn
    #
    sTableKey           = getTableKeyOffName( sTable )
    #
    dColsTypes          = oDbApi.dTables[ sTableKey ].dColsTypes
    #
    bAddedCol           = 0
    #
    if not hasTable( sTable, oDbApi, oDBConnect, oCursor ):
        #
        oTable          = oDbApi.dTables[ sTable ]
        #
        sCreateTable    = getCreateTableString( sTable, oTable, oDbApi.dColTypes )
        #
        oCursor.execute( sCreateTable )
        #
    #
    for sColumn in dColsTypes:
        #
        if not hasColumn( sTable, sColumn, oDbApi, oDBConnect, oCursor ):
            #
            sType       = getTranslatedType( dColsTypes[ sColumn ], oDbApi.dColTypes )
            #
            sAddCol     = 'alter table %s add column %s %s;' % ( sTable, sColumn, sType )
            #
            oCursor.execute( sAddCol )
            #
            bAddedCol   = 1
        #
    #
    if bAddedCol:
        #
        oDBConnect.commit()
        #
    #
    return bAddedCol



def TablesMustHaveAllCols( oDbApi, oDBConnect, oCursor, lNoNeed2CheckTables = () ):
    #
    for sTable in oDbApi.dTables:
        #
        if sTable not in lNoNeed2CheckTables:
            #
            TableMustHaveAllCols( sTable, oDbApi, oDBConnect, oCursor )


def CreateDatabase(
        oConf, oDbApi, oDBConnect, oCursor, oLogger = None, fLogFile = None):
    #
    from commands           import getstatusoutput
    #
    from DbApi.Connect      import getConnectedOffParams
    from String.Get         import getTextWithin, getContentOutOfQuotes
    #
    from sys                import exit
    #
    # PrintMaybe( 'creating new DataBase ...', oOptions.bVerbose ) )
    # print3( 'creating new DataBase ...' )
    #
    sCommand                = ''
    #
    sDataBase               = oConf.get( 'main', 'sDataBase' )
    #
    if oConf.get( 'main', 'sSystemSQL' ) == 'postgresql':
        #
        sHost               = oConf.get( 'main', 'sHost'      )
        sUser               = oConf.get( 'main', 'sUser'      )
        sPassword           = oConf.get( 'main', 'sPassword'  )
        #
        sCommand            = \
            _getCommandLine( sDataBase, sHost, sUser, sPassword )
        #
        sCreate             = 'createdb %s' % sCommand
        #
        iStatus, sOutput    = getstatusoutput( sCreate )
        #
        bOK                 = iStatus == 0
        #
        if not bOK:
            #
            print3( sOutput )
            #
            if    ( 'could not connect to database' in sOutput and
                    'FATAL'                         in sOutput and
                    'role '                         in sOutput and
                    'does not exist'                in sOutput ):
                #
                sUser   = getContentOutOfQuotes(
                            getTextWithin( sOutput, 'role ', 'does not exist' ) )
                #
                print3( 'go into postgres account and "createuser %s"!' % sUser )
            #
            exit(1)
            #
        #
    #
    if oDBConnect is None or oCursor is None or \
            oConf.get( 'main', 'sSystemSQL' ) == 'sqlite':
        #
        oDBConnect, oCursor = \
            getConnectedOffParams(
                oDbApi.connect,
                sDataBase,
                oConf.get( 'main', 'sSystemSQL' ),
                oConf.get( 'main', 'sHost'      ),
                oConf.get( 'main', 'sUser'      ),
                oConf.get( 'main', 'sPassword'  ) )
        #
    lTables, lIndexes   = oDbApi.getCreateTableStatements( oDbApi, oDBConnect, oCursor )
    #
    for sCreateTable in lTables:
        #
        oCursor.execute( sCreateTable )
        #
    #
    for sCreateIndex in lIndexes:
        #
        oCursor.execute( sCreateIndex )
        #
    #
    oDBConnect.commit()



def getExampleTableDict(): # data definitions are here
    #
    dTables     = {}
    # key: table name;
    # value: oTable table object contains lCols, sConstr, & dColsTypes
    #
    # dColsTypes = dTables[ sTable ][ 'dColsTypes' ]
    #
    sTable = 'Package' # see note just below!
    #
    # change this and you will need to change Format.py & Update.py
    #
    lCols = [
        dict( name = 'iPackage',      type = 'serial',    length =   0,
                constraint = 'NOT NULL PRIMARY KEY' ),
        dict( name = 'sPackage',      type = 'varchar',   length =  68,
                constraint = 'NOT NULL' ),
        dict( name = 'tPackage',      type = 'timestamp', length =   0 ),
        ]
    #
    sConstr = 'UNIQUE ( %s )' % ( 'sPackage', )
    #
    # Append2TableDict updates dTables as a "byproduct",
    # so there is no need to pass dTables back as a return value
    #
    Append2TableDict( dTables, sTable, lCols, sConstr )
    #
    # Append2TableDict updates dTables as a "byproduct",
    # so there is no need to pass dTables back as a return value
    #
    #
    sTable = 'PkgLag'
    #
    lCols = [
        dict( name = 'iPkgLag',       type = 'serial',    length =   0,
                constraint = 'NOT NULL PRIMARY KEY' ),
        dict( name = 'iPackage',      type = 'integer',   length =   0,
                constraint = 'NOT NULL' ),
        dict( name = 'sPkgEpoch',     type = 'char',      length =   4,
                constraint = 'NOT NULL' ),
        dict( name = 'sPkgVers',      type = 'varchar',   length =  28,
                constraint = 'NOT NULL' ),
        dict( name = 'sRelease',      type = 'varchar',   length =  38,
                constraint = 'NOT NULL' ),
        dict( name = 'sPkgArch',      type = 'varchar',   length =   8,
                constraint = 'NOT NULL' ),
        dict( name = 'iDir',          type = 'integer',   length =   0,
                constraint = 'NOT NULL' ),
        dict( name = 'sExt',          type = 'char',      length =   3,
                constraint = 'NOT NULL' ),
        dict( name = 'iLag',          type = 'integer',   length =   0 ),
        dict( name = 'bNotActive',    type = 'bool',      length =   0 ),
        dict( name = 'tPkgLag',       type = 'timestamp', length =   0,
                constraint = 'NOT NULL' ),
        ]
    #
    sConstr = ''
    #
    # Append2TableDict updates dTables as a "byproduct",
    # so there is no need to pass dTables back as a return value
    #
    Append2TableDict( dTables, sTable, lCols, sConstr )
    #
    # Append2TableDict updates dTables as a "byproduct",
    # so there is no need to pass dTables back as a return value
    #
    lIndexes   = [ 'create index package_name on Package ( sPackage )',
                   'create index package_key  on PkgLag  ( iPackage )',
                   'create index package_arch on PkgLag  ( sPkgArch )' ]
    #
    return dTables, lIndexes



if __name__ == "__main__":
    #
    from DbApi.Connect  import DbApiClass, getConf, getConnected, \
                            getConfAndConnected
    from DbApi.Test     import hasDataBase, hasTable, hasColumn
    from Utils.Config   import NoConfigFile
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    oDBConnect = oCursor = None
    #
    oConf, oDbApi = getConf( bNoConfigOK = 1 )
    #
    sThisRun        = 'sqlite'
    sConfigFile     = 'ConfNoExample.conf'
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
        sDataBase   = oConf.get( 'main', 'sDataBase'  )
        #
        oDbApi      = DbApiClass( oConf, getExampleTableDict )
        #
        if not ( 'Package' in oDbApi.dTables and
                 'PkgLag'  in oDbApi.dTables ):
            #
            lProblems.append( 'getExampleTableDict() for %s' % sThisRun )
            #
        #
        if hasDataBase( sDataBase, oDbApi, sHost, sUser, sPassword ):
            #
            oDBConnect = oCursor = None
            #
            DropDataBase( oDbApi, oConf )
            #
        #
        if hasDataBase( sDataBase, oDbApi, sHost, sUser, sPassword ):
            #
            lProblems.append( 'DropDataBase(), hasDataBase() for %s' % sThisRun )
            #
        #
        CreateDatabase( oConf, oDbApi, oDBConnect, oCursor )
        #
        # if oCursor is not None: oCursor.close()
        #
        if not hasDataBase( sDataBase, oDbApi, sHost, sUser, sPassword ):
            #
            lProblems.append( 'CreateDatabase() or hasDataBase() for %s' % sThisRun )
            #
        #
        dTables     = oDbApi.dTables
        #
        sTable = 'Directory'
        #
        lCols = [
            dict( name = 'iDir',          type = 'serial',    length =   0,
                    constraint = 'NOT NULL PRIMARY KEY' ),
            dict( name = 'sDir',          type = 'varchar',   length =  98,
                    constraint = 'NOT NULL UNIQUE'      ),
            dict( name = 'sDistro',       type = 'varchar',   length =   8, ),
            dict( name = 'sDistroVers',   type = 'char',      length =   3, ),
            dict( name = 'sDirArch',      type = 'varchar',   length =   8, ),
            dict( name = 'sRepository',   type = 'varchar',   length =  18, ),
            dict( name = 'sBranch',       type = 'varchar',   length =  18, ),
            ]
        #
        sConstr = ''    # sDistro, sDistroVers, sDirArch, sRepository
        #
        # Append2TableDict updates dTables as a "byproduct",
        # so there is no need to pass dTables back as a return value
        #
        Append2TableDict( dTables, sTable, lCols, sConstr )
        #
        if not sTable in dTables:
            #
            lProblems.append( 'Append2TableDict() for %s' % sThisRun )
            #
        #
        oDBConnect, oCursor = getConnected( oDbApi, oConf )
        #
        if not hasTable( 'PkgLag', oDbApi, oDBConnect, oCursor ):
            #
            lProblems.append( 'table PkgLag should be there for %s' % sThisRun )
            #
        #
        DropTable( 'PkgLag', oDbApi, oDBConnect, oCursor )
        #
        if hasTable( 'PkgLag', oDbApi, oDBConnect, oCursor ):
            #
            lProblems.append( 'hasTable() table should be dropped for %s' % sThisRun )
            #
        #
        bAddedCol   = TableMustHaveAllCols( 'Package', oDbApi, oDBConnect, oCursor )
        #
        if bAddedCol:
            #
            lProblems.append( 'TableMustHaveAllCols() none should have been added for %s' % sThisRun )
            #
        #
        sTable              = 'Package'
        #
        dNew = dict(
                name        = 'sPkgNewCol',
                type        = 'varchar',
                length      =  68,
                constraint  = 'NOT NULL' )
        #
        oDbApi.dTables[ sTable ].lCols.append( dNew )
        #
        oDbApi.dTables[ sTable ].dColsTypes = \
            _GetColTypesDict( oDbApi.dTables[ sTable ].lCols )
        #
        bAddedCol   = TableMustHaveAllCols( sTable, oDbApi, oDBConnect, oCursor )
        #
        if not bAddedCol:
            #
            lProblems.append( 'TableMustHaveAllCols() col should have been added for %s' % sThisRun )
            #
        #
        sTable              = 'Directory'
        #
        dNew['name']        = 'sDirNewCol'
        #
        oDbApi.dTables[ sTable ].lCols.append( dNew )
        #
        oDbApi.dTables[ sTable ].dColsTypes = \
            _GetColTypesDict( oDbApi.dTables[ sTable ].lCols )
        #
        TablesMustHaveAllCols( oDbApi, oDBConnect, oCursor )
        #
        if not hasColumn( sTable, 'sDirNewCol', oDbApi, oDBConnect, oCursor ):
            #
            lProblems.append( 'TablesMustHaveAllCols() table should have been added for %s' % sThisRun )
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