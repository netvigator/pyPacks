#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# DbApi functions Fetch
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

setSingleValue      = frozenset( ( 'one', 'count', 'max', 'min' ) )

dGetFetch           = None # fill in below, AFTER functions are defined


def getBigFetchCount( sSelect, oCursor, iFetchLimit = 1000 ):
    #
    """
    Generator simplifying use of fetchmany,
    from fetchsome in Python Cookbook.
    """
    #
    oCursor.execute( sSelect )
    #
    iCount          = 0
    #
    while True:
        #
        lResults    = list( oCursor.fetchmany( iFetchLimit ) )
        #
        if lResults is None: break
        #
        iMore       = len( lResults )
        #
        if iMore == 0: break
        #
        iCount      += iMore
        #
    #
    return iCount



def getBigFetch( sSelect, oCursor, iFetchLimit = 1000 ):
    #
    """
    Generator simplifying use of fetchmany,
    adapted from fetchsome in Python Cookbook.
    """
    #
    oCursor.execute( sSelect )
    #
    while True:
        #
        lResults    = oCursor.fetchmany( iFetchLimit )
        #
        if not lResults:     break
        #
        for tResult in lResults:
            #
            yield tResult
            #
        #
    #


def getAllFetch( sSelect, oCursor ):
    #
    oCursor.execute( sSelect )
    #
    return oCursor.fetchall()


def getAllFetchList( sSelect, oCursor ):
    #
    return list( getAllFetch( sSelect, oCursor ) )


def getOneFetch( sSelect, oCursor ):
    #
    oCursor.execute( sSelect )
    #
    return oCursor.fetchone()



def getSingleColumnList( sSelect, oCursor ):
    #
    from DbApi.Format   import getTupleElementsExtracted
    #
    oCursor.execute( sSelect )
    #
    lContents           = getTupleElementsExtracted( oCursor.fetchall() )
    #
    return lContents



dGetFetch = {
    'all'             : getAllFetch,
    'all-big'         : getBigFetch,
    'onecolumnlist'   : getSingleColumnList,
    'one'             : getOneFetch,
    'count'           : getBigFetchCount,
    'max'             : getOneFetch,
    'min'             : getOneFetch }



def getColFetcherFactory( tWantCols ):
    #
    '''
    This is for queries that return a list of lists,
    a list of column contents for each row.
    For one row/record, this factory function allows
    one to access the column contents by column name.
    Pass the column names tuple to this function and it returns
    a fetcher function for use with the query results.
    Pass one column name and one result row to fetcher function
    and the fetcher function returns the content for that column.

    Column names are CASE SENSITIVE!
    '''
    #
    from Iter.AllVers import iRange, iZip
    #
    dColPositions = dict( iZip( tWantCols, iRange( len( tWantCols ) ) ) )
    #
    def FetchCol( sColName, lResultRow ):
        #
        return lResultRow[ dColPositions[ sColName ] ]
    #
    return FetchCol



if __name__ == "__main__":
    #
    from DbApi.Connect  import getConf, getConnected
    from DbApi.Create   import CreateDatabase, DropDataBase
    from DbApi.Format   import ValueFormatterClass
    from DbApi.Insert   import doInsert
    from DbApi.Test     import hasDataBase
    from Utils.Config import NoConfigFile
    from Utils.Result   import sayTestResult
    #
    lProblems = []
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
        tColsSet        = ( 'sPackage', )
        #
        for sPackage in tPkgs:
            #
            tValues = ( sPackage, )
            #
            doInsert(   oCursor, oDbApi,
                    sTable, tColsSet, tValues, oValFormatter = oValFormatter )
            #
        #
        sSelect = 'select * from Package'
        #
        # oCursor.execute( sSelect )
        #
        if not getBigFetchCount( sSelect, oCursor ):
            #
            lProblems.append( 'getBigFetchCount() for %s' % sThisRun )
            #
        #
        sSelect = 'select * from Package'
        #
        # oCursor.execute( sSelect )
        #
        if len( list( getBigFetch( sSelect, oCursor, 10 ) ) ) != 27:
            #
            lProblems.append( 'getBigFetch() with limit for %s' % sThisRun )
            #
        #
        # oCursor.execute( sSelect )
        #
        if len( list( getAllFetch( sSelect, oCursor ) ) ) != 27:
            #
            lProblems.append( 'getAllFetch() for %s' % sThisRun )
            #
        #
        if len( getAllFetchList( sSelect, oCursor ) ) != 27:
            #
            lProblems.append( 'getAllFetchList() for %s' % sThisRun )
            #
        #
        # oCursor.execute( sSelect )
        #
        if not getOneFetch( sSelect, oCursor ): # returns col value list
            #
            lProblems.append( 'getOneFetch() for %s' % sThisRun )
            #
        #
        sSelect = 'select sPackage from Package'
        #
        lPackage = getSingleColumnList( sSelect, oCursor )
        #
        sPackage = lPackage[0]
        #
        if not sPackage:
            #
            lProblems.append( 'getSingleColumnList() for %s' % sThisRun )
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
    tWantCols   = ( 'eeny', 'meany', 'miney', 'moe' )
    #
    lResults    = [
        [ 0,  1,  2,  3 ],
        [ 1,  5,  9, 13 ],
        [ 2,  4,  8, 16 ],
        [ 3,  9, 27, 81 ] ]
    #
    FetchToes = getColFetcherFactory( tWantCols )
    #
    if      FetchToes( 'eeny',  lResults[ 0 ] ) !=  0 or \
            FetchToes( 'meany', lResults[ 1 ] ) !=  5 or \
            FetchToes( 'miney', lResults[ 2 ] ) !=  8 or \
            FetchToes( 'moe',   lResults[ 3 ] ) != 81:
    #
        #
        lProblems.append( 'getColFetcherFactory()' )
        #
    #
    sayTestResult( lProblems )