#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# DbApi functions Format
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

from six                import print_ as print3

from String.Transform   import getSwapper


setTimeStamp            = frozenset( ( 'date', 'timestamp' ) )


class ValueFormatterClass( object ):
    #
    def __init__( self, sSystemSQL = 'sqlite', oConf = None ):
        #
        if oConf is not None:
            #
            sSystemSQL = oConf.get( 'main', 'sSystemSQL' )
            #
        #
        self.dConvertTypes = dict.fromkeys(
            (   'bool',
                'char',
                'date',
                'inet',
                'text',
                'time',
                'timestamp',
                'varchar' ) )
        #
        if 1 or sSystemSQL != 'sqlite':
            #
            dUpdates    = getConvertTypesDictUpdates( sSystemSQL )
            #
            self._getUpdateConvertTypesDict( dUpdates )
        #
        self.sSystemSQL = sSystemSQL



    def _getUpdateConvertTypesDict( self, dUpdates ):
        #
        self.dConvertTypes.update( dUpdates )


    def _getFormattedValue( self, sType, uValue, bCastType = 0 ):
        #
        """
        Potentially a slight problem here  --
        one cannot put "null" or "None" as strings
        into a character or text field,
        as they are interpreted as null/None.
        """
        #
        from Collect.Test   import isListOrTuple
        from Iter.Test      import isIterable
        from String.Test    import isInQuotesSingle
        from String.Get     import getInSingleQuotes
        from Numb.Test      import isNumber
        from Time.Convert   import getIsoDateTimeStrFromSecs
        #
        if isIterable( uValue ):
            #
            uValue      = [ self._getFormattedValue( sType, uMember )
                            for uMember in uValue ]
            #
        elif uValue is None or uValue == 'None':
            #
            uValue          = 'null'
            #
        elif uValue == 'null' or uValue == 'not null':
            #
            pass
            #
        elif uValue == 'not None':
            #
            uValue          = 'not null'
            #
        elif sType in self.dConvertTypes:
            #
            if sType in setTimeStamp and isNumber( uValue ):
                #
                uValue = getIsoDateTimeStrFromSecs( uValue )
                #
                if sType == 'date': uValue = uValue[:10]
                #
            if not isInQuotesSingle( uValue ):
                #
                uValue  = getInSingleQuotes( uValue )
                #
            if bCastType and self.dConvertTypes[ sType ]:
                #
                if type( self.dConvertTypes[ sType ] ) != str:
                    #
                    fConvert = self.dConvertTypes[ sType ]
                    #
                    uValue  = fConvert( uValue )
                    #
                elif not uValue.startswith( self.dConvertTypes[ sType ] ):
                    #
                    uValue  = '%s %s' % ( self.dConvertTypes[ sType ], uValue )
                    #
            #
            #
            if isListOrTuple( uValue ):
                #
                uValue  = '( %s )' % ', '.join( uValue )
                #
        #
        return uValue


    def getTypeCastValue( self, sType, uValue ):
        #
        return self._getFormattedValue( sType, uValue, bCastType = 1 )




def CommaSeparated( *Items ):
    #
    from Utils.ImIf   import ImIf
    from Collect.Test   import isListOrTuple
    from Iter.AllVers   import iMap
    #
    if      len( Items    ) == 1 and \
            len( Items[0] ) >= 1 and \
            isListOrTuple( Items[0] ):
        #
        Items = Items[0]
        #
    #
    Items   = [ ImIf( sItem == '', 'null', sItem ) for sItem in iMap( str, Items ) ]
    #
    sItems  = ', '.join( Items )
    #
    return sItems



def getFormatter( oValFormatter ):
    #
    if oValFormatter is None:
        #
        def _getFormattedValue( sType, uValue ): return uValue
        #
    else:
        #                     oFormatter._getFormattedValue
        _getFormattedValue   = oValFormatter._getFormattedValue
        #
    #
    return _getFormattedValue



def getTypeCaster( oValFormatter ):
    #
    if oValFormatter is None:
        #
        def getTypeCastValue( sType, uValue ): return uValue
        #
    else:
        #
        getTypeCastValue    = oValFormatter.getTypeCastValue
        #
    #
    return getTypeCastValue



def getSequence( uGot ):
    #
    from Collect.Test   import isListOrTuple
    from Iter.Test      import isIterable
    #
    if isListOrTuple( uGot ):
        #
        tGot        = uGot
        #
    elif isIterable( uGot ):
        #
        tGot        = tuple( uGot )
        #
    else:
        #
        tGot    = ( uGot, )
        #
    #
    return tGot



def getTupleElementsExtracted( lList ):
    #
    """
    When selecting one column only, you get a list of one-element tuples.
    This give you a list of the strings or numbers inside.
    """
    #
    return [ t[0] for t in lList ]



def _getStrippedMaybe( bStrip, uCell ):
    #
    if bStrip:
        #
        uCell   = uCell.strip()
        #
    #
    return uCell



def getMembersStripped( tRow, lStripOrNot ):
    #
    from Iter.AllVers import iZip
    #
    try:
        lStripRow   = iZip( lStripOrNot, tRow )
    except:
        print3( lStripOrNot )
        print3( tRow )
        raise
    #
    lRow = [ _getStrippedMaybe( bStrip, uCell )
             for bStrip, uCell in lStripRow ]
    #
    return tuple( lRow )



def getStripIterator( oIterator, lStripOrNot ):
    #
    for tRow in oIterator:
        #
        yield getMembersStripped( tRow, lStripOrNot )


def getTranslatedType( sType, dColTypes ):
    #
    from Collect.Test   import isListOrTuple
    #
    if dColTypes.get( sType ) is not None:
        #
        sType   = dColTypes.get( sType )
    #
    if isListOrTuple( sType ):
        #
        sType   = sType[ 0 ]
        #
    #
    return sType



def _getTranslateConstraint( sConstraint, sType, dColTypes ):
    #
    if sConstraint:
        #
        sNewConstraint      = dColTypes.get( sType )
        #
        if sNewConstraint:
            #
            sNewConstraint  = sNewConstraint[ 1 ]
            #
            if sNewConstraint:
                #
                sConstraint = '%s %s' % ( sConstraint, sNewConstraint )
                #
            #
        #
    #
    return sConstraint.strip()



def _getColumnCreate( dColumn, dColTypes ):
    #
    sName           = dColumn['name']
    sType           = dColumn['type']
    iLen            = dColumn['length']
    #
    sOrigType       = sType
    #
    sType           = getTranslatedType( sType, dColTypes )
    #
    if iLen:
        #
        sType       = '%s(%d)' % ( sType, iLen )
        #
    #
    sConstraint     = ''
    #
    if 'constraint' in dColumn:
        #
        sConstraint = dColumn['constraint']
        #
    #
    sConstraint     = _getTranslateConstraint( sConstraint, sOrigType, dColTypes )
    #
    return ' '.join( ( sName, sType, sConstraint ) ).strip()


def _getColumnStrings( lCols, dColTypes ):
    #
    lColStrings = [ _getColumnCreate( dColumn, dColTypes ) for dColumn in lCols ]
    #
    return ',\n'.join( lColStrings )



def getCreateTableString( sTable, oTable, dColTypes, bTemp = 0 ):
    #
    lCols       = oTable.lCols
    sConstr     = oTable.sConstr
    #
    if sConstr: sConstr = ',\n' + sConstr
    #
    sColumns = _getColumnStrings( lCols, dColTypes )
    #
    sTemp       = ''
    #
    if bTemp:
        #
        sTemp   = ' TEMP'
        #
    #
    return 'CREATE%s TABLE %s(\n%s%s\n);' % ( sTemp, sTable, sColumns, sConstr )




def getConvertTypesDictUpdates( sSystemSQL = None ):
    #
    from DbApi.Boolean  import getBoolFactory
    #
    dUpdates            = {}
    #
    if sSystemSQL != 'sqlite':
        #
        # getBoolFactory( sSystemSQL )
        #
        dUpdates        = dict(
                            bool        = getBoolFactory( sSystemSQL ),
                            date        = 'date',
                            inet        = 'inet',
                            time        = 'time',
                            timestamp   = 'timestamp' )
    #
    else:
        #
        dUpdates        = dict(
                            bool        = getBoolFactory( sSystemSQL ) )
        #
    #
    return dUpdates



def FixOneItemTuple( uItem ):
    #
    from Collect.Test import isListOrTuple
    #
    if isListOrTuple( uItem ) and len( uItem ) == 1:
        #
        uItem       = uItem[0]
        #
    #
    return uItem



def _getIsoDateTimeDaysAgo( iDaysAgo ):
    #
    from Time.Delta import getIsoDateTimeNowPlus
    #
    return getIsoDateTimeNowPlus( - iDaysAgo )



def getTimeStampDaysAgo( iDaysAgo, fValueTypeCaster ):
    #
    return fValueTypeCaster( 'timestamp', _getIsoDateTimeDaysAgo( iDaysAgo ) )



def getDictListOffQuery( tWantCols, lResults ):
    #
    '''
    see getColFetcherFactory in Fetch!
    '''
    #
    from Dict.Get import getDictOffPairOfLists
    #
    return [ getDictOffPairOfLists( tWantCols, l ) for l in lResults ]



def getDictIterOffQuery( tWantCols, lResults ):
    #
    '''
    see getColFetcherFactory in Fetch!
    '''
    #
    from Dict.Get import getDictOffPairOfLists
    #
    for l in lResults:
        #
        yield getDictOffPairOfLists( tWantCols, l )



if __name__ == "__main__":
    #
    from DbApi.Connect  import getConf, DbApiClass, getConnected
    from DbApi.Create   import CreateDatabase, DropDataBase
    from DbApi.Create   import getExampleTableDict as getTableDict
    from DbApi.Insert   import doInsert
    from DbApi.Query    import getTableKeyOffName, getSelection
    from DbApi.Test     import hasDataBase
    from DbApi.Boolean  import getBooleanInteger
    from Iter.AllVers   import iMap, lMap, iRange, tRange, iZip
    from Time.Delta     import getDeltaDaysFromISOs
    from Utils.Config   import NoConfigFile
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    # oValFormatter._getFormattedValue
    #
    oDBConnect = oCursor = None
    #
    oConf, oDbApi = getConf( bNoConfigOK = 1 )
    #
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
    uBooleanTrue        = 1
    uBooleanFalse       = 0
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
        oValFormatter   = ValueFormatterClass( sSystemSQL, oConf )
        #
        if CommaSeparated( tPkgs ) != \
                'apt, bluetooth, cups, dpkg, eject, firefox, gcc, gimp, ' \
                'iceweasel, kde3, locale, locate, mozilla, openoffice, ' \
                'openssh, perl, python, qt4, ruby, samba, sane, ssl, ' \
                'sudo, upstart, w3m, xine, xorg':
            #
            lProblems.append( 'CommaSeparated() for %s' % sThisRun )
            #
        #
        for sPkg in tPkgs:
            #
            doInsert( oCursor, oDbApi,
                    'Package', ('sPackage',), (sPkg,),
                    oValFormatter = oValFormatter )
        #
        sTable, cTimeStampCol = 'PkgLag', 'tPkgLag'
        #
        getFormattedValue = getFormatter( oValFormatter )
        #
        sTableKey       = getTableKeyOffName( sTable )
        #
        tColsSet        = ( 'iPackage',
                            'sPkgEpoch',
                            'sPkgVers',
                            'sRelease',
                            'sPkgArch',
                            'iDir',
                            'sExt',
                            'iLag',
                            'bNotActive',
                            'tPkgLag' )
        #
        tValues         = ( 1,
                            '8',
                            '4.88',
                            'abc',
                            'i386',
                            8,
                            'rpm',
                            '9',
                            '1',
                            1155037728 ) # '2006-08-08 18:48:48'
        #
        dColsTypes      = oDbApi.dTables[ sTableKey ].dColsTypes
        #
        lColsValues     = iZip( tColsSet, tValues )
        #
        lTypesValues    = [ ( dColsTypes[ sCol ], FixOneItemTuple( uValue ) )
                                for sCol, uValue in lColsValues ]
        #
        lWhereValues    = [ getFormattedValue( sType, uValue )
                            for sType, uValue in lTypesValues ]
        #
        lWantWhereVals  = [ 1,
                            "'8'",
                            "'4.88'",
                            "'abc'",
                            "'i386'",
                            8,
                            "'rpm'",
                            '9',
                            "'1'",
                            "'2006-08-08 18:48:48'" ]
        #
        if lWhereValues[ : 8 ] != lWantWhereVals[ : 8 ] or \
                lWhereValues[ 8 ][ :11 ] != lWantWhereVals[ 8 ][ :11 ] or \
                lWhereValues[ 8 ][ 14: ] != lWantWhereVals[ 8 ][ 14: ]:
            #
            # time zone dependent
            #
            print3( 'this is sSystemSQL dependent -- got' )
            print3( lWhereValues )
            print3( 'wanted:' )
            print3( lWantWhereVals )
            #
            for uWant, uGot in iZip( lWantWhereVals, lWhereValues ):
                #
                if uWant != uGot:
                    #
                    print3( '%s != %s' % ( uWant, uGot ) )
                    #
                else:
                    #
                    print3( '%s == %s' % ( uWant, uGot ) )
                    #
            #
            lProblems.append( 'getFormatter( oValFormatter ) or ValueFormatterClass() for %s' % sThisRun )
            #
        #
        oDbApi = DbApiClass( oConf, getTableDict )
        #
        tTest       = tRange( 5 )
        iterTest    = iMap( int, iRange( 5 ) )
        #
        if getSequence( tTest    ) != tTest:
            #
            lProblems.append( 'getSequence() list for %s' % sThisRun )
            #
        if getSequence( list( tTest ) ) != list( tTest ):
            #
            lProblems.append( 'getSequence() tuple for %s' % sThisRun )
            #
        if getSequence( iterTest ) != tTest:
            #
            lProblems.append( 'getSequence() iterator for %s' % sThisRun )
            #
        if getSequence(        8 ) != ( 8, ):
            #
            lProblems.append( 'getSequence() integer for %s' % sThisRun )
            #
        if getSequence( 'abcdef' ) != ( 'abcdef', ):
            #
            lProblems.append( 'getSequence() string for %s' % sThisRun )
            #
        #
        lEmbedResult = \
            getSelection(
                oCursor,
                oDbApi,
                'Package',
                uWantCols       = 'sPackage',
                oValFormatter   = oValFormatter )
        #
        lResult = getTupleElementsExtracted( lEmbedResult )
        #
        if lMap( str, lResult ) != list( tPkgs ):
            #
            # sqlite returns unicode string versions of the originals
            #
            lProblems.append( 'getTupleElementsExtracted() for %s' % sThisRun )
            #
        #
        sPadded = '  abc  '
        #
        if      _getStrippedMaybe( 1, sPadded ) != 'abc' or \
                _getStrippedMaybe( 0, sPadded ) != sPadded:
            #
            lProblems.append( '_getStrippedMaybe() for %s' % sThisRun )
            #
        #
        tStripOrNot = ( 1, 0, 1, 0, 1 )
        #
        lStripThese = [ sPadded ] * 5
        #
        if getMembersStripped( lStripThese, tStripOrNot ) != \
                ( 'abc', sPadded, 'abc', sPadded, 'abc' ):
            #
            lProblems.append( 'getMembersStripped() for %s' % sThisRun )
            #
        #
        lToStrip = [ [ ' abc ' ] * 5, [ ' def ' ] * 5, [ ' ghi ' ] * 5 ]
        #
        if list( getStripIterator( lToStrip, tStripOrNot ) ) != \
                [('abc', ' abc ', 'abc', ' abc ', 'abc'),
                 ('def', ' def ', 'def', ' def ', 'def'),
                 ('ghi', ' ghi ', 'ghi', ' ghi ', 'ghi')]:
            #
            lProblems.append( 'getStripIterator() for %s' % sThisRun )
            #
        #
        oFormatter  = ValueFormatterClass( sSystemSQL, oConf )
        #
        getTypeCastValue = getTypeCaster( oFormatter )
        #
        lTypes      = [ 'bool', 'char',       'date',     'inet', 'text',
                            'time',           'timestamp', 'varchar' ]
        lValues     = [     1,     'a', '2008-07-25', '10.0.0.1',  'abc',
                        '09:39:32', '2008-07-25 09:39:32',   'abcde' ]
        #
        # oFormatter._getFormattedValue
        lFormatted  = [ getTypeCastValue( *tTypeValue )
                        for tTypeValue in iZip( lTypes, lValues ) ]
        #
        #
        lWantVals   = \
            [   uBooleanTrue,
                "'a'",
                "date '2008-07-25'",
                "inet '10.0.0.1'",
                "'abc'",
                "time '09:39:32'",
                "timestamp '2008-07-25 09:39:32'",
                "'abcde'"]
        #
        if sThisRun == 'sqlite':
            #
            def _OmitType( s ):
                #
                from String.Get import getTextAfter
                #
                if isinstance( s, str ) and ' ' in s:
                    #
                    s = getTextAfter( s, ' ' )
                    #
                #
                return s
            #
            lWantVals = lMap( _OmitType, lWantVals )
        #
        if lFormatted != lWantVals:
            #
            print3( lFormatted )
            print3( lWantVals )
            #
            lProblems.append( 'getTypeCastValue() for %s' % sThisRun )
            #
        #
        dColTypes   = oValFormatter.dConvertTypes
        #
        lTranslated = [ getTranslatedType( sType, dColTypes )
                        for sType in lTypes ]
        #
        lShouldSay  = [ 'char',
                        'date',
                        'inet',
                        'text',
                        'time',
                        'timestamp',
                        'varchar']
        #
        if lTranslated[ 1 : ] != lShouldSay:
            #
            print3( 'this is translated' )
            print3( lTranslated )
            #
            lProblems.append( 'getTranslatedType() for %s' % sThisRun )
            #
        #
        # print3( 'is lCols for Package in oDbApi???' )
        # print3( 'yes, as a property of oDbApi.dTables[ 'Package' ] )
        # print3( [ dCol for dCol in oDbApi.dTables[ 'Package' ].lCols ] )
        #
        lCols       = oDbApi.dTables[ 'Package' ].lCols
        #
        lColsParts  = [ (   dCol[ 'name' ],
                            dCol[ 'type' ],
                            dCol.get( 'constraint', '' ) )
                    for dCol in lCols ]
        #
        #lCols.sort()
        #lColsParts.sort()
        #
        # print3( lColsParts )
        #
        lColsConstraints    = [ ( sName, _getTranslateConstraint(
                                            sConstraint, sType, dColTypes ) )
                                for sName, sType, sConstraint
                                in lColsParts ]
        #
        lWantConsts = [ ('iPackage', 'NOT NULL PRIMARY KEY'),
                        ('sPackage', 'NOT NULL'),
                        ('tPackage', '') ]
        #
        if lColsConstraints != lWantConsts:
            #
            # print3( lColsConstraints )
            lProblems.append( '_getTranslateConstraint() for %s' % sThisRun )
            #
        #
        lColStrings = [ _getColumnCreate( dColumn, dColTypes ) for dColumn in lCols ]
        #
        lWantStrings = [    'iPackage serial NOT NULL PRIMARY KEY',
                            'sPackage varchar(68) NOT NULL',
                            'tPackage timestamp' ]
        #
        if lColStrings != lWantStrings:
            #
            print3( lColStrings )
            lProblems.append( '_getColumnCreate() for %s' % sThisRun )
            #
        #
        sWantStrings =  "iPackage serial NOT NULL PRIMARY KEY,\n" \
                        "sPackage varchar(68) NOT NULL,\n" \
                        "tPackage timestamp"
        #
        if _getColumnStrings( lCols, dColTypes ) != sWantStrings:
            #
            print3( _getColumnStrings( lCols, dColTypes ) )
            lProblems.append( '_getColumnStrings() for %s' % sThisRun )
            #
        #
        sTable  = 'Package'
        oTable  = oDbApi.dTables[ sTable ]
        #
        sWantCreate =   "CREATE TABLE Package(\n" \
                        "iPackage serial NOT NULL PRIMARY KEY,\n" \
                        "sPackage varchar(68) NOT NULL,\n" \
                        "tPackage timestamp,\n" \
                        "UNIQUE ( sPackage )\n" \
                        ");"

        if      getCreateTableString(
                        sTable, oTable, dColTypes, bTemp = 0 ) != \
                    sWantCreate or \
                getCreateTableString(
                        sTable, oTable, dColTypes, bTemp = 1 ) != \
                    sWantCreate.replace( 'CREATE ', 'CREATE TEMP ' ):
            #
            # print3( getCreateTableString( sTable, oTable, dColTypes, bTemp = 0 ) )
            # print3( getCreateTableString( sTable, oTable, dColTypes, bTemp = 1 ) )
            lProblems.append( 'getCreateTableString() for %s' % sThisRun )
            #
            #
        #
        # getBoolFormatted = getBoolFactory( sSystemSQL )
        #
        iDaysAgo = 10
        #
        sTimeStampDaysAgo = getTimeStampDaysAgo(
                                iDaysAgo, fValueTypeCaster = getTypeCastValue )
        #
        if sThisRun == 'postgresql':
            #
            if not sTimeStampDaysAgo.startswith( 'timestamp ' ):
                #
                lProblems.append( 'getTimeStampDaysAgo() for %s' % sThisRun )
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
                if sThisRun == 'postgresql':
                    #
                    uBooleanTrue    = 'TRUE'
                    uBooleanFalse   = 'FALSE'
                    #
                if sThisRun == 'sqlite':
                    #
                    lProblems.append( "No real database to test!" )
                    #
                    break
                #
                oDBConnect = oCursor = None
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
        [ 2,  4,  8, 16 ] ]
    #
    if getDictListOffQuery( tWantCols, lResults ) != \
        [   { 'eeny': 0, 'meany': 1, 'miney': 2, 'moe':  3 },
            { 'eeny': 1, 'meany': 5, 'miney': 9, 'moe': 13 },
            { 'eeny': 2, 'meany': 4, 'miney': 8, 'moe': 16 } ]:
        #
        lProblems.append( 'getDictListOffQuery()' )
        #
    #
    if      list( getDictIterOffQuery( tWantCols, lResults ) ) != \
                  getDictListOffQuery( tWantCols, lResults ):
        #
        lProblems.append( 'getDictIterOffQuery()' )
        #
    #
    sNow        = _getIsoDateTimeDaysAgo(  0 )
    sDaysAgo    = _getIsoDateTimeDaysAgo( 31 )
    #
    nDaysSince  = getDeltaDaysFromISOs( sDaysAgo, sNow )
    #
    if nDaysSince != 31:
        #
        print3( 'from %s until %s should be 31 days, '
              'but instead is %4.1f days' % ( sDaysAgo, sNow, nDaysSince ) )
        lProblems.append( '_getIsoDateTimeDaysAgo()' )
        #
    #
    sayTestResult( lProblems )