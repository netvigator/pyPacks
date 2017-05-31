#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# DbApi functions Test
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


def hasDataBase(
        sDataBase,
        oDbApi,
        host         = None,
        user         = None,
        password     = None ):
    #
    from os.path    import isfile
    #
    from Connect    import getConnectedOffParams
    #
    bHasDataBase    = 0
    #
    if oDbApi.sSystemSQL == 'sqlite':
        #
        bHasDataBase    = isfile( sDataBase )
        #
    else:
        #
        try:
            #
            oDBConnect, oCursor = \
                getConnectedOffParams(
                    oDbApi.connect,
                    sDataBase,
                    oDbApi.sSystemSQL,
                    host        = host,
                    user        = user,
                    password    = password )
            #
            bHasDataBase    = 1
            #
            oCursor.close()
            #
        except oDbApi.InternalError:
            #
            pass
            #
        #
    #
    #
    return bHasDataBase



def hasTable( sTable, oDbApi, oDBConnect, oCursor ):
    #
    from DbApi.Query    import getCount
    #
    bHasTable           = 0
    #
    try:
        #
        bHasTable   = getCount( oCursor, oDbApi, sTable, bPrintQuery = 0 ) >= 0
        #
    except ( oDbApi.DatabaseError, oDbApi.OperationalError ):
        #
        pass
        #
    #
    if not bHasTable:
                #
        try:
            #
            oDBConnect.rollback()
            #
        except:
            #
            pass
            #
    #
    #
    return bHasTable



def hasColumn( sTable, sColumn, oDbApi, oDBConnect, oCursor ):
    #
    bHasColumn      = 0
    #
    try:
        #
        sSelect = 'select %s from %s limit 1;' % ( sColumn, sTable )
        #
        oCursor.execute( sSelect )
        #
        bHasColumn  = 1
        #
    except oDbApi.DatabaseError:
        #
        pass
        #
    #
    if not bHasColumn:
        #
        try:
            #
            oDBConnect.rollback()
            #
        except:
            #
            pass
            #
    #
    #
    return bHasColumn







if __name__ == "__main__":
    #
    from DbApi.Connect  import DbApiClass, getConfAndConnected, getConf, getConnected
    from DbApi.Create   import DropTable, DropDataBase, CreateDatabase
    from DbApi.Create   import getExampleTableDict as getTableDict
    from Utils.Config   import NoConfigFile
    from Utils.Result   import sayTestResult
    #
    lProblems       = []
    #
    oDBConnect = oCursor = None
    #
    oConf, oDbApi   = getConf( bNoConfigOK = 1 )
    #
    sThisRun        = 'sqlite'
    sConfigFile     = 'ConfNoExample.conf'
    #
    while True:
        #
        bNoConfigOK = ( sThisRun == 'sqlite' )
        #
        sDataBase   = oConf.get( 'main', 'sDataBase'  )
        sSystemSQL  = oConf.get( 'main', 'sSystemSQL' )
        #
        sHost       = oConf.get( 'main', 'sHost'      )
        sUser       = oConf.get( 'main', 'sUser'      )
        sPassword   = oConf.get( 'main', 'sPassword'  )
        #
        if hasDataBase( sDataBase, oDbApi, sHost, sUser, sPassword ):
            #
            oDBConnect = oCursor = None
            #
            DropDataBase( oDbApi, oConf )
            #
        #
        oDbApi = DbApiClass( oConf, getTableDict )
        #
        if hasDataBase( sDataBase, oDbApi, sHost, sUser, sPassword ):
            #
            lProblems.append(
                'DropDataBase() or hasDataBase() for %s' % sThisRun )
            #
        #
        CreateDatabase( oConf, oDbApi, oDBConnect, oCursor )
        #
        oDBConnect, oCursor = getConnected( oDbApi, oConf )
        #
        if not hasDataBase( sDataBase, oDbApi, sHost, sUser, sPassword ):
            #
            lProblems.append(
                'CreateDatabase() or hasDataBase() for %s' % sThisRun )
            #
        #
        sTable = 'Package'
        #
        if not hasTable( sTable, oDbApi, oDBConnect, oCursor ):
            #
            lProblems.append(
                'hasTable() table should be there for %s' % sThisRun )
            #
        #
        sColumn = 'iPkgLag'
        #
        if hasColumn( sTable, sColumn, oDbApi, oDBConnect, oCursor ):
            #
            lProblems.append(
                'hasColumn() but should not be there for %s' % sThisRun )
            #
        #
        if not hasColumn( 'PkgLag', sColumn, oDbApi, oDBConnect, oCursor ):
            #
            lProblems.append(
                'hasColumn() but should be there for %s' % sThisRun )
            #
        #
        DropTable( sTable, oDbApi, oDBConnect, oCursor )
        #
        if hasTable( sTable, oDbApi, oDBConnect, oCursor ):
            #
            lProblems.append(
                'hasTable() or DropTable() for %s' % sThisRun )
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
            # why was oConf.get( 'main', 'sSystemSQL' ) not working?
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