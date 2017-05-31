#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# File functions Import
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
# Copyright 2004-2017 Rick Graves
#
from six            import print_ as print3
from six            import next   as getNext

from Dir.Get        import sTempDir
from File.Test      import isFileThere
from Iter.AllVers   import iMap, tMap
from String.Find    import getFinder
#from Utils.Both2n3 import getNext

tLineEnd = ( '\n', '\r' )

_oNullFinder = getFinder(
    r'(?<=;)null(?=;)|'     # null between semicolons
     '(?<=,)null(?=,)|'     # null between comas
          '^null(?=,|;)|'   # null at beginning of line
   '(?<=,|;)null$' )        # null at end of line

def getLineOmitNewLine( s ):
    #
    while s and s[ -1 ] in tLineEnd:
        #
        s = s[ : -1 ] # drop new line and/or return
        #
    #
    return s


def unSlashQuotes( s ):
    #
    return s.replace( '\\"', '"' ).replace( "\\'", "'" ).strip()


def getFileObjFirstLine( *sFileSpec, **kwargs ):
    #
    from File.Get       import getFileObject
    from File.Spec      import getFullSpec
    #
    sMode = 'r'
    sNcode = ''
    #
    if 'sMode'  in kwargs: sMode  = kwargs[ 'sMode'  ]
    if 'sNcode' in kwargs: sNcode = kwargs[ 'sNcode' ]
    #
    sFileSpec       = getFullSpec( *sFileSpec )
    #
    oFile           = getFileObject( sFileSpec, sMode = sMode )
    #
    sLine0          = getLineOmitNewLine( getNext( oFile ) )
    #
    return oFile, sLine0




def _killNulls( s ):
    #
    from String.Replace import getBlanksForReMatchObj
    #
    return _oNullFinder.sub( getBlanksForReMatchObj, s )


def getDictIterOffCSV( *sFileSpec, **kwargs ):
    #
    # sFileSpecOrPath, sFile = '', fLineTreatment = None ):
    #
    """
    pass the spec for a CSV file,
    returns iterator of dictionaries
    (returns dictionaries one by one,
    one dictionary for each data line).
    keys are column headings,
    values are column contents.
    CSV file MUST have column headings as first line.
    """
    #
    from String.Test import isQuote
    #
    class Finished( Exception ): pass
    #
    from copy           import copy
    #
    from Iter.AllVers   import iRange, iZip
    from String.Get     import getTextAfter, getCharNotIn, getTextAfterLast
    #
    fLineTreatment  = kwargs.get( 'fLineTreatment', None  )
    bSayLineErrors  = kwargs.get( 'bSayLineErrors', True )
    #
    oFile, sLine0   = getFileObjFirstLine( *sFileSpec, **kwargs )
    #
    if sLine0.startswith( '\xef\xbb\xbf' ): sLine0 = sLine0[ 3 : ]
    #
    sQuote          = sLine0[ 0 ]
    #
    if isQuote( sQuote ):
        #
        def StripQuotes( s ):
            #
            iBeg = 0
            iEnd = len( s )
            #
            if s.startswith( sQuote ): iBeg =  1
            if s.endswith(   sQuote ): iEnd = -1
            #
            return s[ iBeg : iEnd ]
            #
        #
        sLine0          = sLine0[ 1 : ][ : -1 ]
        #
        sEscQuote       = '\\' + sQuote
        #
        sColDelimiter   = getTextAfter( sLine0.replace( sEscQuote, '' ), sQuote )[ 0 ]
        #
        sQuoteCommaQuote= '%s%s%s' % ( sQuote, sColDelimiter, sQuote )
        #
    else:
        #
        def StripQuotes( s ): return s
        #
        lDelims = [ ( sLine0.count( sDelim ), sDelim ) for sDelim in ( ',', ';' ) ]
        #
        lDelims.sort()
        #
        sColDelimiter   = lDelims[ -1 ][ 1 ]
        #
        sQuoteCommaQuote= sColDelimiter
        #
    #
    tColNames       = tuple( sLine0.split( sQuoteCommaQuote ) )
    #
    iColNamesLen    = len( tColNames )
    #
    sNullEnd        = '%sNULL'   %   sColDelimiter
    #
    sEscColDelim    = '\\' + sColDelimiter
    #
    lMoreLines      = [] # this helps handle returns in the column value
    #
    while True:
        #
        sLineOrig   = getNext( oFile )
        #
        if not sLineOrig: break
        #
        sLineOrig   = getLineOmitNewLine( sLineOrig )
        #
        lMoreLines.append( sLineOrig )
        #
        sLineOrig   = '\n'.join( lMoreLines )
        #
        if sLineOrig:
            #
            if fLineTreatment is not None:
                #
                sLineOrig   = fLineTreatment( sLineOrig )
                #
            #
            if      not sLineOrig.endswith( sQuote ) and \
                    not sLineOrig.endswith( sNullEnd ):
                #
                if 1 + sLineOrig.count( sColDelimiter ) < iColNamesLen:
                    #
                    continue
                    #
                #
                sLastCol = getTextAfterLast( sLineOrig, sColDelimiter )
                #
                if          sLastCol.startswith( sQuote ) and \
                        not sLastCol.endswith(   sQuote ):
                    #
                    continue
                    #
            #
            sLineOrig   = _killNulls( sLineOrig )
            #
            try:
                #
                sLine   = StripQuotes( sLineOrig )
                #
                tColVals= sLine.split( sQuoteCommaQuote )
                #
                if len( tColVals ) == iColNamesLen:
                    #
                    raise Finished
                    #
                #
                tColVals= sLineOrig.split( sColDelimiter )
                #
                if len( tColVals ) == iColNamesLen:
                    #
                    tColVals = tMap( StripQuotes, tColVals )
                    #
                    raise Finished
                    #
                #
                # reconstitute here
                #
                lColRecon = copy( tColVals )
                #
                for iThis in iRange( len( tColVals ) - 1, 0, -1 ):
                    #
                    sBefo = lColRecon[ iThis - 1 ]
                    sThis = lColRecon[ iThis     ]
                    #
                    if      sBefo and sThis                  and \
                          (     sThis == sQuote or
                            not sThis.startswith( sQuote ) ) and \
                                sThis.endswith(   sQuote )   and \
                            not sBefo.endswith(   sQuote ):
                        #
                        lColRecon[ iThis - 1 ] = \
                            sColDelimiter.join( ( sBefo, sThis ) )
                        del lColRecon[ iThis ]
                        #
                #
                if len( lColRecon ) == iColNamesLen:
                    #
                    tColVals = tMap( StripQuotes, lColRecon )
                    #
                    raise Finished
                    #
                #
                if    ( len( tColVals ) > iColNamesLen and
                        sEscColDelim in sLineOrig ):
                    #
                    lNewVals = [ tColVals[0] ]
                    #
                    for s in tColVals[ 1 : ]:
                        #
                        if lNewVals[ -1 ].endswith( '\\' ):
                            #
                            lNewVals[ -1 ] = lNewVals[ -1 ] + sColDelimiter + s
                            #
                        else:
                            #
                            lNewVals.append( s )
                            #
                        #
                    #
                    if len( lNewVals ) == iColNamesLen:
                        #
                        tColVals = [ s.replace( sEscColDelim, sColDelimiter )
                                     for s
                                     in tMap( StripQuotes, lNewVals ) ]
                        #
                    raise Finished
                    #
                #
                if bSayLineErrors:
                    print3( 'this line does not split into values '
                            'for each column heading:' )
                    print3( sLineOrig )
                    print3( 'the column headings are:' )
                    print3( tColNames )
                #
            except Finished:
                #
                pass
                #
            #
            lMoreLines      = []
            #
            yield dict( iZip( tColNames, iMap( unSlashQuotes, tColVals ) ) )
            #
        #
        else:
            #
            lMoreLines      = []
            #




def getDictIterOffCsvReader( oCsvReader ):
    #
    '''
    pass a csv.reader object
    CSV file MUST have column headings as first line.    
    '''
    #
    from Iter.AllVers   import iZip
    #
    lHeader = getNext( oCsvReader )
    #
    for l in oCsvReader:
        #
        yield dict( iZip( lHeader, l ) )





def getDictIterUseCsvReader(  *sFileSpec , **kwargs ):
    #
    from csv            import reader
    #
    from File.Get       import getFileObject
    #
    delimiter = kwargs.get( 'delimiter', ',' )
    quotechar = kwargs.get( 'quotechar', '"' )
    #
    oCsvReader = reader(
            getFileObject( *sFileSpec, sMode = 'r' ),
            delimiter = delimiter,
            quotechar = quotechar )
    #
    return getDictIterOffCsvReader( oCsvReader )





def getDictListOffCSV( *sFileSpec, **kwargs ):
    #
    """
    pass the spec for a CSV file,
    returns list of dictionaries.
    keys are column headings,
    values are column contents.
    CSV file MUST have column headings as first line.
    """
    #
    return list( getDictIterOffCSV( *sFileSpec, **kwargs ) )




def getDictTupleOffCSV( *sFileSpec, **kwargs ):
    #
    """
    pass the spec for a CSV file,
    returns tuple of dictionaries.
    keys are column headings,
    values are column contents.
    CSV file MUST have column headings as first line.
    """
    #
    return tuple( getDictIterOffCSV( *sFileSpec, **kwargs ) )



def getSetFromFileLines():
    #
    # use setFromFileLines( *sFileSpec )
    #
    pass


def setFromFileLines( *sFileSpec ):
    #
    """
    pass the spec for a list file,
    returns set, each line is one member.
    NOTE that if there are quotes,
    the line is considered to be what is within the quotes
    """
    #
    from File.Get       import getFileObject
    from Iter.AllVers   import iFilter
    from String.Get     import getContentOutOfQuotes
    #
    return frozenset(
            iFilter( bool,
             iMap( getContentOutOfQuotes,
               getFileObject( *sFileSpec ) ) ) )




if __name__ == "__main__":
    #
    lProblems = []
    #
    from csv            import reader
    from os.path        import join
    #
    from Dir.Get        import sTempDir
    from File.Get       import getFileObject
    from File.Write     import MakeTemp, putListInTemp
    from String.Get     import getInDoubleQuotes
    from Utils.Result   import sayTestResult
    #
    sTestExcel = \
'''"uid","name","email"
"21597","Guido von Rossum","guido@gmail.com"
,"Richard Matthew Stallman","rms@gnu.org"
"26271","Ian Murdock","imurdock@debian.org"
"26272","Linus Tovalds",
'''
    #
    MakeTemp( sTestExcel, bSayBytes = False )
    #
    lWant = [ { 'email' : 'guido@gmail.com',
                'uid'   : '21597',
                'name'  : 'Guido von Rossum'        },
              { 'email' : 'rms@gnu.org',
                'uid'   : '',
                'name'  : 'Richard Matthew Stallman'},
              { 'email' : 'imurdock@debian.org',
                'uid'   : '26271',
                'name'  : 'Ian Murdock'             },
              { 'email' : '',
                'uid'   : '26272',
                'name'  : 'Linus Tovalds'           } ]
    #
    if getDictListOffCSV( sTempDir, 'temp.txt' ) != lWant:
        #
        lProblems.append( 'getDictListOffCSV() CSV for Excel' )
        #
        print3( getDictListOffCSV( join( sTempDir, 'temp.txt' ) ) )
    #
    oIter = getDictIterOffCSV( sTempDir, 'temp.txt' )
    #
    if list( oIter ) != lWant:
        #
        lProblems.append( 'getDictIterOffCSV() CSV for Excel' )
        #
    #
    oCsvReader = reader(
            getFileObject( sTempDir, 'temp.txt', sMode = 'r' ),
            delimiter=',',
            quotechar='"' )
    #
    iterCSV = getDictIterOffCsvReader( oCsvReader )
    #
    lFromReader = list( iterCSV )
    #
    if lFromReader != lWant:
        #
        #
        lProblems.append( 'getDictIterOffCsvReader( oCsvReader )' )
        #
    #
    iterCSV = getDictIterUseCsvReader( sTempDir, 'temp.txt' )
    #
    lFromReader = list( iterCSV )
    #
    if lFromReader != lWant:
        #
        #
        lProblems.append( 'getDictIterUseCsvReader( *sFileSpec )' )
        #
    #
    #
    #
    #
    sTestExcel = (
'''uid,name,email
21597,Guido von Rossum,guido@gmail.com
,Richard Matthew Stallman,rms@gnu.org
26271,Ian Murdock,imurdock@debian.org
26272,Linus Tovalds,
''' )
    #
    MakeTemp( sTestExcel, bSayBytes = False )
    #
    if getDictListOffCSV( sTempDir, 'temp.txt' ) != lWant:
        #
        lProblems.append( 'getDictListOffCSV() CSV for Excel no quotes' )
        #
    #
    #
    sTestPlain = \
    '''"type";"name";"module";"description";"help";"has_title";"title_label";"has_body";"body_label";"min_word_count";"custom";"modified";"locked";"orig_type"
"page";"Page";"node";"If you want to add a static page.";;"1";"Title";"1";"Body";"0";"1";"1";"0";"page"
"article";"Article";"node";"Articles have a title, a teaser and a body.";;"1";"Title";"1";"Body";"0";"1";"1";"0";"story"
'''
    MakeTemp( sTestPlain, bSayBytes = False )
    #
    if getDictListOffCSV( join( sTempDir, 'temp.txt' ) ) != \
            [ { 'body_label': 'Body',
                'orig_type': 'page',
                'locked': '0',
                'help': '',
                'has_title': '1',
                'description': 'If you want to add a static page.',
                'modified': '1',
                'module': 'node',
                'has_body': '1',
                'title_label': 'Title',
                'custom': '1',
                'type': 'page',
                'min_word_count': '0',
                'name': 'Page' },
              { 'body_label': 'Body',
                'orig_type': 'story',
                'locked': '0',
                'help': '',
                'has_title': '1',
                'description': 'Articles have a title, a teaser and a body.',
                'modified': '1',
                'module': 'node',
                'has_body': '1',
                'title_label': 'Title',
                'custom': '1',
                'type': 'article',
                'min_word_count': '0',
                'name': 'Article' } ]:
        #
        lProblems.append( 'getDictListOffCSV() CSV plain' )
        #
        print3( getDictListOffCSV( join( sTempDir, 'temp.txt' ) ) )
    #
    #
    lTest = [ 'a', 'b', 'c', 'd' ]
    #
    putListInTemp( iMap( getInDoubleQuotes, lTest + [ '' ] ) )
    #
    if setFromFileLines( sTempDir, 'temp.txt' ) != frozenset( lTest ):
        #
        lProblems.append( 'setFromFileLines()' )
        #
    #
    if _killNulls( "10,null,'xyz'" ) != "10,    ,'xyz'":
        #
        lProblems.append( '_killNulls() should remove null within comas' )
        #
    #
    if _killNulls( "10;null;'xyz'" ) != "10;    ;'xyz'":
        #
        lProblems.append( '_killNulls() should remove null within semicolons' )
        #
    #
    if _killNulls( "t.r.null@gmail.com" ) != "t.r.null@gmail.com":
        #
        lProblems.append( '_killNulls() should keep null in email address' )
        #
    #
    if _killNulls( "null;'xyz'" ) != "    ;'xyz'":
        #
        lProblems.append( '_killNulls() should wipe null at beginning of line' )
        #
    #
    if _killNulls( "10;null" ) != "10;    ":
        #
        lProblems.append( '_killNulls() should wipe null at end of line' )
        #
    #

    sayTestResult( lProblems )