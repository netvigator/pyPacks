#!/home/rick/.local/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Utility functions Config
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
#   http://www.gnu.org/licenses/
#
# Copyright 2004-2023 Rick Graves
#
"""
you need this in ConfExample.conf:

[main]
foo     = bar
spam    = eggs
[Other]
spam    = toast

config parsers have these methods (among others):
has_section( section )
has_option( section, option )

"""

from copy               import copy
from inspect            import stack
from os                 import access, R_OK
from os.path            import dirname, join
from socket             import gethostname
from sys                import path, argv

from six                import print_ as print3

try:
    from ..Collect.Filter import RemoveDupes
    from ..Collect.Test import isListOrTuple
    from ..Dict.Get     import getItemIter, getDictOffPairOfLists, getKeyIter
    from ..File.Test    import isFileThere
    from ..Iter.AllVers import iFilter, lMap
    from ..Object.Get   import ValueContainer
    from ..String.Get   import getTextAfter, getTextBefore
except ( ValueError, ImportError ):
    from Collect.Filter import RemoveDupes
    from Collect.Test   import isListOrTuple
    from Dict.Get       import getItemIter, getDictOffPairOfLists, getKeyIter
    from File.Test      import isFileThere
    from Iter.AllVers   import iFilter, lMap
    from Object.Get     import ValueContainer
    from String.Get     import getTextAfter, getTextBefore



class invalidInputError( ValueError ): pass

class MissingHostnameSectionHeaderError( Exception ): pass

try:
    #
    import configparser # python 3
    #
except ImportError:
    #
    try:
        #
        import ConfigParser as configparser
        #
    except ImportError:
        #
        import SafeConfigParser as configparser
#



oOptions            = None

class NoConfigFile( Exception ): pass



def _isNotUsrOrVar( s ):
    #
    return not ( s.startswith( '/usr/' ) or s.startswith( '/var/' ) )


def _getPathTryThis():
    #
    #
    yield argv[0]
    #
    for sTryPath in iFilter( _isNotUsrOrVar, path ):
        #
        yield sTryPath
        #
    #
    for t in stack()[ : -1 ]: # exclude last one, already checked
        #
        yield dirname( t[1] )



def _findConfFile( sConfigFile ):
    #
    #
    if not isFileThere( sConfigFile ):
        #
        for sThisPath in _getPathTryThis():
            #
            if isFileThere( sThisPath, sConfigFile ):
                #
                sConfigFile = join( sThisPath, sConfigFile )
                #
                break
        #
    #
    return sConfigFile



def getConfigOptions(
            sConfigFile = 'ConfExample.conf',
            dDefaults   = {},
            bNoConfigOK = False ):
    #
    '''
    all config option names are coverted to all lower case!!!
    '''
    #
    if type( sConfigFile ) == type( [] ):   # list!? what the heck!!!
        #
        if len( sConfigFile ) == 1:
            sConfigFile = sConfigFile[0]    # you get a list when .py file called from shell
        else:
            sConfigFile = ''
        #
    #
    oOptions        = configparser.ConfigParser()
    #
    if not bNoConfigOK:
        #
        sConfigFile = _findConfFile( sConfigFile )
        #
    #
    if access( sConfigFile, R_OK ) or bNoConfigOK:
        oOptions.read( sConfigFile )
    else:
        #
        raise NoConfigFile( 'Error accessing config file: %s' % sConfigFile )

    # defaults
    #
    for sSection in dDefaults:
        #
        if not oOptions.has_section( sSection ):
            #
            oOptions.add_section( sSection )
            #
        #
        lSectionItems = []
        #
        if isinstance( dDefaults[ sSection ], dict ):
            #
            lSectionItems = getItemIter( dDefaults[ sSection ] )
            #
        elif isListOrTuple( dDefaults[ sSection ] ):
            #
            lSectionItems = dDefaults[ sSection ]
            #
        for sName, uValue in lSectionItems:
            #
            if not oOptions.has_option( sSection, sName ):
                #
                oOptions.set( sSection, sName, uValue )
                #
            #
        #
    #
    return oOptions



def __hasContentNotComment( s ):
    #
    return '=' in s and not s.lstrip().startswith( '#' )


def __getOption( s ):
    #
    #
    s = getTextBefore( s, '=' )
    #
    return s.strip()


def _getMainOptions( sConfigFile ):
    #
    try: # moving this to the top breaks this package!
        from ..File.Get import getContent
    except ( ValueError, ImportError ): # maybe circular import issue
        from File.Get   import getContent
    #
    sConfigFile = _findConfFile( sConfigFile )
    #
    sContent    = getTextAfter( getContent( sConfigFile ), '[main]' )
    #
    if '[' in sContent: sContent = getTextBefore( sContent, '[' )
    #
    lLines      = [ s.rstrip() for s in sContent.split( '\n' ) ]
    #
    lLines      = iFilter( __hasContentNotComment, lLines )
    #
    return lMap( __getOption, lLines )



def _StartWithS( sOption ):
    #
    if not sOption.startswith( 's' ):
        #
        sOption = 's%s' % sOption
        #
    #
    return sOption



def getConfLite(
        sConfigFile = 'ConfExample.conf', dDefaults = {}, bNoConfigOK = False ):
    #
    '''
    For everything under main, you can get return an object with
    properties for all the values under main (including defaults).
    '''
    #
    if not 'main' in dDefaults:
        #
        dDefaults = { 'main' : dDefaults }
        #
    #
    oOptions    = getConfigOptions( sConfigFile, dDefaults, bNoConfigOK )
    #
    lWantOpts   = _getMainOptions( sConfigFile )
    #
    lWantOpts.extend( getKeyIter( dDefaults[ 'main' ] ) )
    #
    lWantOpts   = RemoveDupes( lWantOpts )
    #
    #
    lOptions    = [ sOption.lower() for sOption in lWantOpts ]
    #
    lVars       = [ _StartWithS( sOption ) for sOption in lWantOpts ]
    #
    lVals       = [ oOptions.get( 'main', sOption ) for sOption in lOptions ]
    #
    oOptions.__dict__.update( getDictOffPairOfLists( lVars, lVals ) )
    #
    return oOptions



def getDict( oConf ):
    #
    dConf = {}
    #
    for sSection in oConf.sections():
        #
        dSec = {}
        #
        dConf[ sSection ] = dSec
        #
        for sOption in oConf.options( sSection ):
            #
            dSec[ sOption ] = oConf.get( sSection, sOption )
            #
        #
    #
    return dConf



def getConfDict(
            sConfigFile = 'ConfExample.conf',
            dDefaults   = {},
            bNoConfigOK = False ):
    #
    oConf = getConfigOptions(
        sConfigFile = sConfigFile,
        dDefaults   = dDefaults,
        bNoConfigOK = bNoConfigOK )
    #
    return getDict( oConf )




_setTrue = frozenset( ( 'yes', 'y',            'true', 't',              ) )
_setValid= frozenset( ( 'yes', 'y', 'no', 'n', 'true', 't', 'false', 'f' ) )

def getBoolOffYesNoTrueFalse( sConfText ):
    #
    sConfText = sConfText.lower().strip()
    #
    if sConfText not in _setValid:
        #
        raise invalidInputError( sConfText )
    #
    return sConfText in _setTrue



def getListOffCommaString( sConfText ):
    #
    lParts = sConfText.split( ',' )
    #
    lParts = [ s.strip() for s in lParts ]
    #
    return lParts


def getTupleOffCommaString( sConfText ):
    #
    return tuple( getListOffCommaString( sConfText ) )



def getSetFrozenOffCommaString( sConfText ):
    #
    return frozenset( filter( bool, getListOffCommaString( sConfText ) ) )




def gotCharsGetBool( d ):
    #
    '''
    modifies the dictionary in place -- returns None
    '''
    #
    for k, v in getItemIter( d ):
        #
        d[ k ] = getBoolOffYesNoTrueFalse( v )



def getBoolValue( d, sLookFor ):
    #
    sLookFor = sLookFor.lower()
    #
    return sLookFor in d and d[ sLookFor ]




def getValueTier2( d, sTier1, sTier2, uDefault = None ):
    #
    sTier2 = sTier2.lower()
    #
    dTier2 = d.get( sTier1, {} )
    #
    uReturn = uDefault
    #
    if sTier2 in dTier2:
        #
        uReturn = dTier2[ sTier2 ]
        #
    #
    return uReturn




def gotCommaStringGetSetFrozen( d ):
    #
    '''
    modifies the dictionary in place -- returns None
    '''
    #
    for k, v in getItemIter( d ):
        #
        _setFrozen = frozenset( getTupleOffCommaString( v ) )
        #
        d[ k ] = _setFrozen


def gotStringDigitsGetIntegers( d ):
    #
    '''
    modifies the dictionary in place -- returns None
    '''
    #
    for k, v in getItemIter( d ):
        #
        d[ k ] = int( v )



def fixConfValues( dConf, sVarName, fFixIt ):
    #
    for sTopLevel in dConf:
        #
        if sVarName in dConf[ sTopLevel ]:
            #
            v = dConf[ sTopLevel ][ sVarName ]
            #
            dConf[ sTopLevel ][ sVarName ] = fFixIt( v )





def fixSpecificLevel2s( dConf, dVarsFixers ):
    #
    for sTopLevel in dConf:
        #
        for sVarName in dConf[ sTopLevel ]:
            #
            if sVarName in dVarsFixers:
                #
                fFixIt = dVarsFixers[ sVarName ]
                #
                v = dConf[ sTopLevel ][ sVarName ]
                #
                dConf[ sTopLevel ][ sVarName ] = fFixIt( v )



def fixAllLevel2sUnderLevel1( dConf, dVarsFixers ):
    #
    for sTopLevel in dConf:
        #
        if sTopLevel in dVarsFixers:
            #
            fFixIt = dVarsFixers[ sTopLevel ]
            #
            for sVarName in dConf[ sTopLevel ]:
                #
                v = dConf[ sTopLevel ][ sVarName ]
                #
                dConf[ sTopLevel ][ sVarName ] = fFixIt( v )
                
    

def getConfName4Host( cBaseName, bVerbose = True ):
    #
    '''
    pass the base name, like MyApp
    say the hostname is Gertrude
    This will look for MyApp-Gertrude.conf
    '''
    #
    #
    sHostName = gethostname()
    #
    sLookForConf = "%s-%s.conf" % ( cBaseName, sHostName )
    #
    sLookForConf = _findConfFile( sLookForConf )
    #
    if not isFileThere( sLookForConf ):
        #
        if bVerbose: print3( ('Did not find config file: %s') % sLookForConf )
        #
        raise NoConfigFile
    #
    return sLookForConf
    


def getConfMainIsDefaultHostnameVaries(
        sConfigFile     = 'ConfExample.conf',
        tWantSections   = None,
        sFakeHostName4Testing = None ):
    #
    '''
    One config file shared by multiple development computers
    config info for all development computers in one config file
    default config settings are in main
    variations for host development computer are in a section
    heading for section is the hostname
    see bash shell prompt, hostname is right there
    you must get the hostname exactly right!
    '''
    #
    dConfig = getConfDict( sConfigFile )
    #
    dReturn = copy( dConfig['main'] )
    #
    if sFakeHostName4Testing is None:
        #
        sHostNameLower = gethostname()
        #
    else:
        #
        sHostNameLower = sFakeHostName4Testing
        #
    #
    if sHostNameLower in dConfig:
        #
        dThisHost = dConfig[ sHostNameLower ]
        #
        iterKeys = getKeyIter( dThisHost )
        #
        for sKey in iterKeys:
            #
            dReturn[ sKey ] = dThisHost[ sKey ]
            #
    else:
        #
        sMsg = 'no section heading for hostname "%s"!' % sHostNameLower
        #
        raise MissingHostnameSectionHeaderError( sMsg )
        #
    #
    if tWantSections:
        #
        for sSection in tWantSections:
            #
            if sSection in dConfig:
                #
                dReturn[ sSection ] = dConfig[ sSection ]
                #
            #
        #
    #
    return dReturn




if __name__ == "__main__":
    #
    from Dict.Get       import getKeyIter
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    oOptions    = getConfigOptions(
                    dDefaults = { 'Other': [ ( 'bacon', 'eggs' ) ] } )
    #
    if oOptions.get( 'main',  'foo'  ) != 'bar':
        #
        lProblems.append( 'getConfigOptions() get from file -- file there?' )
        #
    if oOptions.get( 'Other', 'bacon') != 'eggs':
        #
        lProblems.append( 'getConfigOptions() access defaults with file' )
        #
    #
    oOptions    = getConfigOptions(
                    sConfigFile = 'ConfNoExample.conf',
                    dDefaults   = { 'Other': { 'bacon': 'eggs' } },
                    bNoConfigOK = True )
    #
    if oOptions.get( 'Other', 'bacon') != 'eggs':
        #
        lProblems.append( 'getConfigOptions() access defaults no file' )
        #
    #
    oOptions    = getConfigOptions(
                    sConfigFile = 'ConfExample.conf',
                    dDefaults   = { 'Other': { 'bacon': 'eggs' } },
                    bNoConfigOK = False )
    #
    if oOptions.get( 'Other', 'spam') != 'toast':
        #
        lProblems.append( 'getConfigOptions() access file' )
        #
    #
    d = {   'main' : { 'foo':   'bar',
                       'spam':  'eggs'},
            'Other': { 'bacon': 'eggs',
                       'spam':  'toast'} }
    #
    dGot = getDict( oOptions )
    #
    if dGot != d:
        #
        lProblems.append( 'getDict()' )
        #
    #
    oLiteOpts   = getConfLite(
                    sConfigFile = 'ConfExample.conf',
                    dDefaults = { 'Foo' : 'candy bar' } )
    #
    if      oLiteOpts.get( 'main', 'foo' ) != 'bar' or \
            oLiteOpts.get( 'Other', 'spam') != 'toast':
        #
        lProblems.append( 'getConfLite() regular values' )
        #
    #
    d = {   'main' : { 'foo':   'bar',
                       'spam':  'eggs'},
            'Other': { 'spam':  'toast'} }
    #
    if getConfDict() != d:
        #
        lProblems.append( 'getConfDict()' )
        #
    #
    if not getBoolOffYesNoTrueFalse( 'Yes' ):
        #
        lProblems.append( 'getBoolOffYesNoTrueFalse() Yes' )
        #
    #
    if not getBoolOffYesNoTrueFalse( 'Y' ):
        #
        lProblems.append( 'getBoolOffYesNoTrueFalse() Y' )
        #
    #
    if not getBoolOffYesNoTrueFalse( 'True' ):
        #
        lProblems.append( 'getBoolOffYesNoTrueFalse() True' )
        #
    #
    if getBoolOffYesNoTrueFalse( 'No' ):
        #
        lProblems.append( 'getBoolOffYesNoTrueFalse() No' )
        #
    #
    if getBoolOffYesNoTrueFalse( 'False' ):
        #
        lProblems.append( 'getBoolOffYesNoTrueFalse() False' )
        #
    #
    if getBoolOffYesNoTrueFalse( 'F' ):
        #
        lProblems.append( 'getBoolOffYesNoTrueFalse() F' )
        #
    #
    try:
        getBoolOffYesNoTrueFalse( 'xyz' )
    except invalidInputError:
        pass
    else:
        #
        lProblems.append( 'getBoolOffYesNoTrueFalse() xyz' )
        #
    #
    sCountries = 'Germany, Italy, Thailand'
    #
    tCountries = getTupleOffCommaString( sCountries )
    #
    if tCountries != ( 'Germany', 'Italy', 'Thailand' ):
        #
        lProblems.append( 'getTupleOffCommaString()' )
        #
    #
    d = dict( a = 'yes', b = 'no', c = 'true', d = 'false' )
    #
    gotCharsGetBool( d )
    #
    if d != dict( a = True, b = False, c = True, d = False ):
        #
        lProblems.append( 'gotCharsGetBool()' )
        #
    #
    if getBoolValue( d, 'b' ) or getBoolValue( d, 'z' ):
        #
        lProblems.append( 'getBoolValue() should return False' )
        #
    #
    if not ( getBoolValue( d, 'a' ) and getBoolValue( d, 'c' ) ):
        #
        lProblems.append( 'getBoolValue() should return True' )
        #
    #
    d = dict( a = '1,2, 3, 4', b = '5, 6, 7 , 8 ' )
    #
    gotCommaStringGetSetFrozen( d )
    #
    if d != dict( a = frozenset( ( '1', '2', '3', '4' ) ),
                  b = frozenset( ( '5', '6', '7', '8' ) ) ):
        #
        lProblems.append( 'gotCommaStringGetSetFrozen()' )
        #
    #
    d = dict( a = '1', b = '2', c = '3', d = '4' )
    #
    gotStringDigitsGetIntegers( d )
    #
    if d != dict( a = 1, b = 2, c = 3, d = 4 ):
        #
        lProblems.append( 'gotStringDigitsGetIntegers()' )
        #
    #
    # fixConfValues( d, sVarName, fFixIt )
    #
    dOrig = dict(   a = dict( spam = 1, eggs = 2, toast = 3 ),
                    b = {},
                    c = [],
                    d = () )
    #
    dWant = dict(   a = dict( spam = 1, eggs = '2', toast = 3 ),
                    b = {},
                    c = [],
                    d = () )
    #
    fFixIt = str
    #    
    fixConfValues( dOrig, 'eggs', fFixIt )
    #
    if dOrig != dWant:
        #
        lProblems.append( 'fixConfValues()' )
        #
    #
    if getValueTier2( dOrig, 'a', 'toast' ) != 3:
        #
        lProblems.append( 'getValueTier2() return actual value' )
        #
    #
    if getValueTier2( dOrig, 'b', 'toast', 'default' ) != 'default':
        #
        lProblems.append( 'getValueTier2() return default' )
        #
    #
    dOrig = dict(   a = dict( spam  =  1 ),
                    b = dict( eggs  = '2' ),
                    c = dict( toast = '1, 2, 3, 4',
                              jam   = 3.14156 ),
                    d = dict( bacon = 'yes' ), )
    #
    dFixers = dict( spam    = str,
                    eggs    = int,
                    toast   = getTupleOffCommaString,
                    bacon   = getBoolOffYesNoTrueFalse )
    #
    fixSpecificLevel2s( dOrig, dFixers )
    #
    dWant = dict(   a = dict( spam  = '1' ),
                    b = dict( eggs  =  2 ),
                    c = dict( toast = ('1', '2', '3', '4' ),
                              jam   = 3.14156 ),
                    d = dict( bacon = True ), )
    #
    if dOrig != dWant:
        #
        lProblems.append( 'fixSpecificLevel2s()' )
        #
    #
    dOrig = dWant 
    #
    dFixers = dict( c = str )
    #
    dWant = dict(   a = dict( spam  = '1' ),
                    b = dict( eggs  =  2 ),
                    c = dict( toast = "('1', '2', '3', '4')",
                              jam   = '3.14156' ),
                    d = dict( bacon = True ), )
    #
    fixAllLevel2sUnderLevel1( dOrig, dFixers )
    #
    if dOrig != dWant:
        #
        print3( dOrig )
        lProblems.append( 'fixAllLevel2sUnderLevel1()' )
        #
    #
    from socket     import gethostname
    #
    from File.Del   import DeleteIfExists
    #
    sHostName = gethostname()
    #
    sFile = 'MyImaginaryApp-%s.conf' % sHostName
    #
    oFile = open( sFile, 'w' )
    #
    oFile.close()
    #
    try:
        #
        getConfName4Host( 'MyImaginaryApp' )
        #
    except NoConfigFile:
        #
        lProblems.append( "getConfName4Host( 'MyImaginaryApp' )" )
        #
    finally:
        #
        DeleteIfExists( sFile )
        #
    #
    try:
        #
        getConfName4Host( 'Oops!', bVerbose = False )
        #
    except NoConfigFile:
        #
        pass
        #
    else:
        #
        lProblems.append( "getConfName4Host( 'Oops!' )" )
        #
    #
    dRetuned = getConfMainIsDefaultHostnameVaries(
                sFakeHostName4Testing = 'Other' )
    # None 
    #
    dWant = dict( foo = 'bar', spam = 'toast' )
    #
    if dRetuned != dWant:
        #
        # print3( dRetuned )
        #
        lProblems.append( "getConfMainIsDefaultHostnameVaries()" )
        #
    #
    try:
        #
        dRetuned = getConfMainIsDefaultHostnameVaries(
                sFakeHostName4Testing = 'NotInThere' ) 
        # 
        #
    except MissingHostnameSectionHeaderError:
        #
        pass
        #
    else:
        #
        lProblems.append( "getConfMainIsDefaultHostnameVaries() "
            "hostname not in there" )
        #
    #
    dRetuned = getConfMainIsDefaultHostnameVaries(
                tWantSections = ( 'Other', ),
                sFakeHostName4Testing = 'Other' )
    #
    dWant = {'foo': 'bar', 'Other': {'spam': 'toast'}, 'spam': 'toast'}
    #
    if dRetuned != dWant:
        #
        print3( dRetuned )
        #
        lProblems.append( "getConfMainIsDefaultHostnameVaries( "
                          "tWantSections = ( 'Other', ) )" )
        #
    #
    # getBoolOffYesNoTrueFalse( 'xyz' )
    #
    sayTestResult( lProblems )
