#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# DbApi functions Recycle
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


def _getRecycleCount(
        sTable, sTimeStampCol, iDaysOld, oCursor, oDbApi, oValFormatter ):
    #
    from DbApi.Query    import getCount
    from Time.Delta     import getSecsNowPlusDHMS
    #
    iWayBack    = getSecsNowPlusDHMS( - iDaysOld )
    #
    return getCount(
        oCursor,
        oDbApi,
        sTable,
        tWhereCols      = sTimeStampCol,
        tWhereVals      = iWayBack,
        tWhereOper      = '<',
        oValFormatter   = oValFormatter )



def doTransaction( sToDo, oDBConnect, oDbApi ):
    #
    from DbApi.Query        import NoListBackQuery
    #
    NoListBackQuery( sToDo, oDBConnect )



def getRecycle(
        oDbApi, oConf,
        sTable, sColList, sTimeStampCol, iNeedRecs,
        iKeep4Days  = 31,
        iVerbosity  = 0 ):
    #
    from six             import print_ as print3
    #
    from DbApi.Query     import NoListBackQuery, getSelection
    from Object.Get      import RandomFeederClass
    from String.Output   import ReadableNo
    from Time.Delta      import getSecsNowPlusDHMS
    from Time.Output     import sayLocalTimeOnly
    #
    iRecycleable            = _getRecycleCount(
                                sTable, sTimeStampCol, iKeep4Days,
                                oCursor, oDbApi, oValFormatter )
    #
    oRecycleFeeder          = None
    #
    bRecycle                = iRecycleable >= iNeedRecs
    #
    if bRecycle:
        #
        doTransaction( 'begin', oDBConnect, oDbApi )
        #
        if iVerbosity > 4:
            print3( sayLocalTimeOnly(), "begin work successful"
        #
        iWayBack    = getSecsNowPlusDHMS( - iKeep4Days )
        #
        lRecycleables       = \
            getSelection(
                oCursor,
                oDbApi,
                sTable,
                uWantCols       = sColList,
                tWhereCols      = sTimeStampCol,
                tWhereVals      = iWayBack,
                tWhereOper      = '<',
                oValFormatter   = oValFormatter,
                tOrderByCols    = sTimeStampCol,
                bForUpdate      = 1,
                iLimit          = iNeedRecs )
        #
        if len( lRecycleables ) < iNeedRecs:  # did not get
            #
            print3( sayLocalTimeOnly(), "rolling back, cannot recycle", sTable, "records"
            #
            doTransaction( 'rollback', oDBConnect, oDbApi ) # cancel update
            #
            bRecycle    = 0
            #
            if iVerbosity > 4:
                print3( sayLocalTimeOnly(), \
                    "only got", ReadableNo( len( lRecycleables ) ), \
                    "recycleables, not enough, needed", ReadableNo( iNeedRecs )
            #
        else:
            #
            oRecycleFeeder      = RandomFeederClass( lRecycleables )
            #
            if iVerbosity > 4:
                print3( sayLocalTimeOnly(), "got", len( oRecycleFeeder ), sTable, "records to recycle"
        #
    #
    return bRecycle, oRecycleFeeder



if __name__ == "__main__":
    #
    lProblems       = []
    #
    from DbApi.Connect  import getConf, getConnected
    from DbApi.Create   import CreateDatabase, DropDataBase
    from DbApi.Insert   import doInsert
    from DbApi.Format   import ValueFormatterClass
    from DbApi.Test     import hasDataBase
    from Iter.AllVers   import tMap
    from Time.Output    import getNowIsoDateTimeStr
    from Time.Delta     import getDeltaDaysFromISOs
    from Utils.Config   import NoConfigFile
    from Utils.Result   import sayTestResult
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
        tColsSet        = ( 'iPackage', 'sPackage', 'tPackage' )
        #
        tValueSet       = ( (       0,  'python',  '2004-01-01 10:00:00' ),
                            (       1,  'perl',    '2005-01-01 11:00:00' ),
                            (       2,  'whois',   '2006-01-01 12:00:00' ),
                            (       3,  'ssh',     '2008-01-01 13:00:00' ) )
        #
        for tValues in tValueSet:
            #
            doInsert(   oCursor, oDbApi,
                        sTable, tColsSet, tValues,
                        oValFormatter = oValFormatter )
            #
        #
        sTimeStampCol   = 'tPackage'
        iDaysOld        = getDeltaDaysFromISOs( '2008-01-01 12:00:00' ) + 10
        #
        iRecycle        = _getRecycleCount(
                            sTable, sTimeStampCol, iDaysOld,
                            oCursor, oDbApi, oValFormatter )
        #
        if iRecycle != 3:
            #
            lProblems.append(
                '_getRecycleCount() returned %s for %s' %
                    ( iRecycle, sThisRun ) )
            #
        #
        sColList    = 'iPackage'
        iNeedRecs   = 3
        #
        bRecycle, oRecycleFeeder = getRecycle(
                oDbApi, oConf,
                sTable, sColList, sTimeStampCol, iNeedRecs,
                iKeep4Days  = iDaysOld )
        #
        tWant = ( (0,), (1,), (2,) )
        #
        if oRecycleFeeder is None:
            #
            lProblems.append( 'getRecycle() oRecycleFeeder is None' )
            #
        elif tMap( tuple, oRecycleFeeder.lList ) != lWant:
            #
            lProblems.append( 'getRecycle() wrong key list' )
            #
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