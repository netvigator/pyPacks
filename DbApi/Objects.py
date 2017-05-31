#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# DbApi functions Objects
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
# Copyright 2017 Rick Graves
#

class Schema( object ):
    #
    name = None
    #
    dTables = {
        'example': {
            'column1': {
                'name':         'id',
                'col_type':     'serial',
                'constraint':   'primary key' },
            'table_constraints': None }
        }
    
    def getTableCreationOrder( self ):
        #
        from Dict.Get import getKeyIter
        #
        lTablesNotDepending = []
        lTablesDepending    = []
        #
        setTablesNotDepending   = set( [] )
        setTablesDepending      = set( [] )
        #
        for sTable in getKeyIter( self.dTables ):
            #
            if ( 'table_constraints' in self.dTables[ sTable ] and
                    self.dTables[ sTable ][ 'table_constraints' ] is not None ):
                #
                lTablesDepending.append( sTable )
                setTablesDepending.add( sTable )
                #
            else:
                #
                lTablesNotDepending.append( sTable )
                setTablesNotDepending.add( sTable )
                #
    



if __name__ == "__main__":
    #
    #from DbApi.Connect  import getConf, getConnected
    #from Utils.Config   import NoConfigFile
    from Utils.Result   import sayTestResult
    #
    lProblems       = []
    #
    oDBConnect      = oCursor = None
    #
    #oConf, oDbApi   = getConf( bNoConfigOK = 1 )
    #
    class AuctionSchema( Schema ):
        
        def __init__( self ): pass
        
        name = 'Auctions'
        #
        # define the order in which tables are to be defined
        #
        dTables = {
            'users': {
                'column1': {
                    'name':         'id',
                    'col_type':     'serial',
                    'constraint':   'primary key' },
                'column2': {
                    'name':         'cnamegiven',
                    'col_type':     'varchar(48)',
                    'constraint':   'not nul' },
                'column3': {
                    'name':         'cnamefamily',
                    'col_type':     'varchar(48)',
                    'constraint':   'not nul' },
                'column4': {
                    'name':         'cemail',
                    'col_type':     'citext',
                    'constraint':   'not nul unique' },
                'column5': {
                    'name':         'cpasswordDigest',
                    'col_type':     'text',
                    'constraint':   'not nul' },
                'column6': {
                    'name':         'tcreate',
                    'col_type':     'timestamp',
                    'constraint':   'not nul' },
                'column7': {
                    'name':         'tmodify',
                    'col_type':     'timestamp',
                    'constraint':    None },
                },
            'brands': {
                'column1': {
                    'name':         'id',
                    'col_type':     'serial',
                    'constraint':   'primary key' },
                'column2': {
                    'name':         'cbrandname',
                    'col_type':     'varchar(48)',
                    'constraint':   'not nul' },
                'column3': {
                    'name':         'bwanted',
                    'col_type':     'bool',
                    'constraint':   'default true' },
                'column4': {
                    'name':         'ballofinterest',
                    'col_type':     'bool',
                    'constraint':   'default true' },
                'column5': {
                    'name':         'istars',
                    'col_type':     'smallint',
                    'constraint':    None },
                'column6': {
                    'name':         'ccomments',
                    'col_type':     'text',
                    'constraint':    None },            
                'column7': {
                    'name':         'cnationality',
                    'col_type':     'char(2)',
                    'constraint':    'not null' },
                'column8': {
                    'name':         'user_id',
                    'col_type':     'integer',
                    'constraint':   'not null' },
                'column9': {
                    'name':         'tcreate',
                    'col_type':     'timestamp',
                    'constraint':   'not nul' },
                'columnA': {
                    'name':         'tmodify',
                    'col_type':     'timestamp',
                    'constraint':    None },
                'table_constraints': (
                    'FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE',
                    ) },
            'brandexclude': {
                'column1': {
                    'name':         'brand_id',
                    'col_type':     'integer',
                    'constraint':   'not null' },
                'column2': {
                    'name':         'cexcludeif',
                    'col_type':     'varchar(48)',
                    'constraint':   'not nul' },
                'column3': {
                    'name':         'user_id',
                    'col_type':     'integer',
                    'constraint':   'not null' },
                'column4': {
                    'name':         'tcreate',
                    'col_type':     'timestamp',
                    'constraint':   'not nul' },
                'column5': {
                    'name':         'tmodify',
                    'col_type':     'timestamp',
                    'constraint':    None },
                'table_constraints': (
                    'FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE',
                    'FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE CASCADE'
                    )
            } }
    
    if False:
        #
        lProblems.append( 'getCountDistinct() for %s' % sThisRun )
        #
    #
    #
    sayTestResult( lProblems )