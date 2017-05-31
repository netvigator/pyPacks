#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions HTML
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

from String.Find    import getFinder
from String.Output  import getZeroPadder

#
oFindiFrameBeg      = getFinder( '<iframe.*?>'  )
oFindiFrameEnd      = getFinder( '</iframe>'    )
oFindFrameBeg       = getFinder( '<frame '      )
oFindFrameSpec      = getFinder( 'src='         )
oFindLinkStart      = getFinder( ' href='       )
oFindBodyBeg        = getFinder( '<body.*?>'    )
oFindBodyEnd        = getFinder( '</body>'      )
oSeparatorFinder    = getFinder( '''>|'|"'''    )
#
oTagFinder          = getFinder( '''<(?:"[^"]*"|'[^']*'|[^'">])*>''' )
#

_padWith0s          = getZeroPadder( 3 )

tOtherChars = (
    'iexcl',
    'cent',
    'pound',
    'curren',
    'yen',
    'brvbar',
    'sect',
    'uml',
    'copy',
    'ordf',
    'laquo',
    'not',
    'shy',
    'reg',
    'macr',
    'deg',
    'plusmn',
    'sup2',
    'sup3',
    'acute',
    'micro',
    'para',
    'middot',
    'cedil',
    'sup1',
    'ordm',
    'raquo',
    'frac14',
    'frac12',
    'frac34',
    'iquest',
    'Agrave',
    'Aacute',
    'Acirc',
    'Atilde',
    'Auml',
    'Aring',
    'AElig',
    'Ccedil',
    'Egrave',
    'Eacute',
    'Ecirc',
    'Euml',
    'Igrave',
    'Iacute',
    'Icirc',
    'Iuml',
    'ETH',
    'Ntilde',
    'Ograve',
    'Oacute',
    'Ocirc',
    'Otilde',
    'Ouml',
    'times',
    'Oslash',
    'Ugrave',
    'Uacute',
    'Ucirc',
    'Uuml',
    'Yacute',
    'THORN',
    'szlig',
    'agrave',
    'aacute',
    'acirc',
    'atilde',
    'auml',
    'aring',
    'aelig',
    'ccedil',
    'egrave',
    'eacute',
    'ecirc',
    'euml',
    'igrave',
    'iacute',
    'icirc',
    'iuml',
    'eth',
    'ntilde',
    'ograve',
    'oacute',
    'ocirc',
    'otilde',
    'ouml',
    'divide',
    'oslash',
    'ugrave',
    'uacute',
    'ucirc',
    'uuml',
    'yacute',
    'thorn',
    'yuml',
    'OElig',
    'oelig',
    'Scaron',
    'scaron',
    'Yuml',
    'fnof',
    'circ',
    'tilde',
    'Alpha',
    'Beta',
    'Gamma',
    'Delta',
    'Epsilon',
    'Zeta',
    'Eta',
    'Theta',
    'Iota',
    'Kappa',
    'Lambda',
    'Mu',
    'Nu',
    'Xi',
    'Omicron',
    'Pi',
    'Rho',
    'Sigma',
    'Tau',
    'Upsilon',
    'Phi',
    'Chi',
    'Psi',
    'Omega',
    'alpha',
    'beta',
    'gamma',
    'delta',
    'epsilon',
    'zeta',
    'eta',
    'theta',
    'iota',
    'kappa',
    'lambda',
    'mu',
    'nu',
    'xi',
    'omicron',
    'pi',
    'rho',
    'sigmaf',
    'sigma',
    'tau',
    'upsilon',
    'phi',
    'chi',
    'psi',
    'omega',
    'thetasym',
    'upsih',
    'piv',
    'ensp',
    'emsp',
    'thinsp',
    'zwnj',
    'zwj',
    'lrm',
    'rlm',
    'ndash',
    'mdash',
    'lsquo',
    'rsquo',
    'sbquo',
    'ldquo',
    'rdquo',
    'bdquo',
    'dagger',
    'Dagger',
    'bull',
    'hellip',
    'permil',
    'prime',
    'Prime',
    'lsaquo',
    'rsaquo',
    'oline',
    'frasl',
    'euro',
    'image',
    'weierp',
    'real',
    'trade',
    'alefsym',
    'larr',
    'uarr',
    'rarr',
    'darr',
    'harr',
    'crarr',
    'lArr',
    'uArr',
    'rArr',
    'dArr',
    'hArr',
    'forall',
    'part',
    'exist',
    'empty',
    'nabla',
    'isin',
    'notin',
    'ni',
    'prod',
    'sum',
    'minus',
    'lowast',
    'radic',
    'prop',
    'infin',
    'ang',
    'and',
    'or',
    'cap',
    'cup',
    'int',
    'there4',
    'sim',
    'cong',
    'asymp',
    'ne',
    'equiv',
    'le',
    'ge',
    'sub',
    'sup',
    'nsub',
    'sube',
    'supe',
    'oplus',
    'otimes',
    'perp',
    'sdot',
    'lceil',
    'rceil',
    'lfloor',
    'rfloor',
    'lang',
    'rang',
    'loz',
    'spades',
    'clubs',
    'hearts',
    'diams' )



def _getCompleteTags():
    #
    return (
        '<abbr>',
        '<acronym>',
        '<address>',
        '<applet>',
        '<b>',
        '<big>',
        '<blink>',
        '<blockquote>',
        '<body>',
        '<body>',
        '<br>',
        '<button>',
        '<caption>',
        '<center>',
        '<cite>',
        '<code>',
        '<col>',
        '<colgroup>',
        '<dd>',
        '<del>',
        '<dfn>',
        '<dir>',
        '<div>',
        '<dl>',
        '<em>',
        '<fieldset>',
        '<frame>',
        '<frameset>',
        '<h1>',
        '<h2>',
        '<h3>',
        '<h4>',
        '<h5>',
        '<h6>',
        '<head>',
        '<hr>',
        '<html>',
        '<i>',
        '<iframe>',
        '<ilayer>',
        '<ins>',
        '<isindex>',
        '<kbd>',
        '<label>',
        '<layer>',
        '<legend>',
        '<marquee>',
        '<menu>',
        '<meta>',
        '<nobr>',
        '<noframes>',
        '<nolayer>',
        '<noscript>',
        '<object>',
        '<ol>',
        '<option>',
        '<p>',
        '<param>',
        '<pre>',
        '<q>',
        '<s>',
        '<samp>',
        '<script>',
        '<select>',
        '<server>',
        '<small>',
        '<spacer>',
        '<span>',
        '<strike>',
        '<strong>',
        '<style>',
        '<sub>',
        '<sup>',
        '<table>',
        '<tbody>',
        '<td>',
        '<tfoot>',
        '<th>',
        '<thead>',
        '<title>',
        '<tr>',
        '<tt>',
        '<u>',
        '<ul>',
        '<var>',
        '<wbr>' )



def getCompleteTagsWiper():
    #
    from String.Replace import getReplaceManyOldWithBlanksSwapper
    #
    return getReplaceManyOldWithBlanksSwapper( _getCompleteTags() )


def _getIncompleteTags():
    #
    # test better below if function proves useful somewhere
    #
    tIncompletes = (
        '<!doctype',
        '<a',
        '<applet',
        '<area',
        '<base',
        '<basefont',
        '<bdo',
        '<bgsound',
        '<body',
        '<br',
        '<button',
        '<caption',
        '<col',
        '<colgroup',
        '<del',
        '<dir',
        '<div',
        '<dl',
        '<embed',
        '<font',
        '<form',
        '<frame',
        '<frameset',
        '<h1',
        '<h2',
        '<h3',
        '<h4',
        '<h5',
        '<h6',
        '<hr',
        '<iframe',
        '<img',
        '<input',
        '<ins',
        '<isindex',
        '<label',
        '<layer',
        '<legend',
        '<li',
        '<link',
        '<map',
        '<menu',
        '<meta',
        '<multicol',
        '<ol',
        '<optgroup',
        '<option',
        '<p',
        '<pre',
        '<q',
        '<script',
        '<select',
        '<spacer',
        '<table',
        '<td',
        '<textarea',
        '<th',
        '<tr',
        '<ul'
        )
    #
    return tIncompletes





def _getEnvVariableTuple():
    #
    tManyCodes = (
        'ALL',
        'APPL',
        'AUTH',
        'CERT',
        'CONTENT',
        'DATE',
        'DOCUMENT',
        'GATEWAY',
        'HTTPS',
        'HTTP',
        'INSTANCE',
        'LAST',
        'LOCAL',
        'LOGON',
        'PATH',
        'QUERY',
        'REDIRECT',
        'REMOTE',
        'REQUEST',
        'SCRIPT',
        'SERVER',
        'SSH',
        'UNIQUE',
        'USER'
        )
    #
    lManyCodes = [ '(?<=\s)%s_[A-Z_]+(?=\s)' % sCode for sCode in tManyCodes ] + \
                 [ '(?<=\s)%s(?=\s)' % sCode for sCode in
                    ( 'HTTPS', 'PATH', 'PATHEXT', 'REFERER', 'SERVER' ) ]
    #
    return lManyCodes



def _getHTMLntts():
    #
    from six.moves.html_entities    import entitydefs
    #
    from Dict.Get                   import getDictOffPairOfLists, getItemIter
    from Iter.AllVers               import iMap, lMap, tMap, tRange
   #from Utils.Both2n3              import entitydefs
    #
    #
    dCareful = \
         dict(
            apos    = "'",
            quot    = '"',
            lt      = "<",
            gt      = ">",
            amp     = "&",
            nbsp    = chr(160) )
    #
    #   '   single quotation
    #   "   double quote
    #   <   less than
    #   >   greater than
    #   &   ampersand, better to do last
    #       non-breaking space
    #
    # zero-width joiners &#8205; &#x200d;
    #
    dCareful[ '#8205'  ] = ''
    dCareful[ '#x200d' ] = ''
    #
    def getCompleteCode( tCode ):
        #
        cKey, cValue = tCode
        #
        return ( '&%s;' % cKey, cValue )
    #
    def getCodeSansSemiC( sCode ):
        #
        return sCode[:-1]
    #
    def getCodeTupleSansColon( tCode ):
        #
        return ( tCode[0][:-1], tCode[1] )
    #
    lCareful        = lMap( getCompleteCode, getItemIter( dCareful   ) )
    #
    # do not need the ones excluded below
    #
    lnttHTML        = [ ( k, v ) for k, v
                        in iMap( getCompleteCode, getItemIter( entitydefs ) )
                        if not v.startswith( '&#' ) ]
    #
    # do not need the ones excluded above
    #
    dCareful        = dict( lCareful )
    #
    dHTMLntt        = dict( lnttHTML + lCareful )
    #
    lCareful        = lMap( getCodeTupleSansColon, lCareful )
    #
    lnttHTML        = lMap( getCodeTupleSansColon, lnttHTML )
    #
    dCarefulNoColon = dict( lCareful )
    #
    dHTMLnttNoColon = dict( lnttHTML + lCareful )
    #
    #
    #
    tWantChars      = tRange(32,127)
    #
    tChars          = tMap( chr, tWantChars )
    #
    lCodesNormal    = [ '&#%s;' % _padWith0s( iWantChar )   for iWantChar in tWantChars ]
    #
    lCodesCut       = [ '&#%s;' % str( iWantChar )          for iWantChar in tWantChars ]
    #
    lCodesHex       = [ '&#%s;' % hex( iWantChar )          for iWantChar in tWantChars ]
    #
    # lCodesHexCut  = [ '&#%s;' % hex( iWantChar )[ 1 : ]   for iWantChar in tWantChars ]
    #
    dNumbCodes      = getDictOffPairOfLists(
                        lCodesNormal + lCodesCut + lCodesHex,
                        tChars * 3 ) #  + lCodesHexCut
    #
    lOtherChars     = [ '&%s;' % s for s in tOtherChars ]
    #
    dOtherCodes     = dict.fromkeys( lOtherChars, ' ' )
    #
    lCodesNormal    = iMap( getCodeSansSemiC, lCodesNormal )
    #
    lCodesCut       = iMap( getCodeSansSemiC, lCodesCut    )
    #
    lCodesHex       = iMap( getCodeSansSemiC, lCodesHex    )
    #
    # lCodesHexCut  = m@p( getCodeSansSemiC, lCodesHexCut )
    #
    dNumbsNoColon   = getDictOffPairOfLists(
                        list( lCodesNormal ) +
                        list( lCodesCut ) +
                        list( lCodesHex ),
                        tChars * 3 ) #  + lCodesHexCut
    #
    lOthersNoColon  = iMap( getCodeSansSemiC, lOtherChars )
    #
    dOthersNoSemiC  = dict.fromkeys( lOthersNoColon, ' ' )
    #
    return dCareful, dHTMLntt, dNumbCodes, dOtherCodes, \
            dCarefulNoColon, dHTMLnttNoColon, dNumbsNoColon, dOthersNoSemiC


class HTMLnttSwappersClass( object ):
    #
    def __init__(   self, **dUpdates ):
        #
        from String.Transform   import getSwapper
        #
        dCareful, dHTMLntt, dNumbCodes, dOtherCodes, \
            dCarefulNoSemiC, dHTMLnttNoSemiC, dNumbCodesNoSemiC, dOthersNoSemiC = _getHTMLntts()
        #
        dCareful.update(            dUpdates.get( 'dCareful',         {} ) )
        dHTMLntt.update(            dUpdates.get( 'dHTMLntt',         {} ) )
        dNumbCodes.update(          dUpdates.get( 'dNumbCodes',       {} ) )
        dOtherCodes.update(         dUpdates.get( 'dOtherCodes',      {} ) )
        dCarefulNoSemiC.update(     dUpdates.get( 'dCarefulNoSemiC',  {} ) )
        dHTMLnttNoSemiC.update(     dUpdates.get( 'dHTMLnttNoSemiC',  {} ) )
        dNumbCodesNoSemiC.update(   dUpdates.get( 'dNumbCodesNoSemiC',{} ) )
        dOthersNoSemiC.update(      dUpdates.get( 'dOthersNoSemiC',   {} ) )
        #
        dHTMLntt.update(            dNumbCodes        )
        dHTMLntt.update(            dOtherCodes       )
        #
        dHTMLnttNoSemiC.update( dNumbCodesNoSemiC )
        dHTMLnttNoSemiC.update( dOthersNoSemiC    )
        #
        self.SwapChars4Codes                 = getSwapper( dHTMLntt,
                                                         bIgnoreCase = True )
        self.SwapChars4CodesCareful          = getSwapper( dCareful,
                                                         bIgnoreCase = True )
        self.SwapChars4CodesNoSemiC          = getSwapper( dHTMLnttNoSemiC,
                                                         bIgnoreCase = True )
        self.SwapChars4CodesNoSemiCareful    = getSwapper( dCarefulNoSemiC,
                                                         bIgnoreCase = True )
        #
    def getChars4HtmlCodes( self, sHTML ):
        #
        return self.SwapChars4CodesNoSemiC( self.SwapChars4Codes( sHTML ) )


oHTMLnttSwapper = HTMLnttSwappersClass()

getChars4HtmlCodes = oHTMLnttSwapper.getChars4HtmlCodes


def getEnvVariableFinder():
    #
    from re import IGNORECASE, compile as REcompile
    #
    return REcompile( '|'.join( _getEnvVariableTuple() ), IGNORECASE )




def getHtmlRow(lCells ):
    #
    return '<td>%s</td>' % '</td><td>'.join( lCells )


def _getTableFormats( dFormats ):
    #
    lFormats    = []
    #
    iBorder     = dFormats.get( 'border',       0 )
    iPadding    = dFormats.get( 'cellpadding',  0 )
    iSpacing    = dFormats.get( 'cellspacing',  0 )
    uWidth      = dFormats.get( 'width',     None )
    #
    if iBorder:
        #
        lFormats.append( 'border= %s' % iBorder )
        #
    if iPadding:
        #
        lFormats.append( 'cellpadding = %s' % iPadding ) # space inside cells
        #
    if iSpacing:
        #
        lFormats.append( 'cellspacing = %s' % iSpacing ) # space around cells
        #
    if uWidth:
        #
        sQuote  = ''
        #
        if type( uWidth ) == type( '' ) and uWidth.endswith( '%' ):
            #
            sQuote = '"'
            #
        lFormats.append( 'width = %s%s%s' % ( sQuote, uWidth, sQuote ) )
        #
    #
    sFormats = ' %s' % ' '.join( lFormats )
    #
    if sFormats == ' ': sFormats = ''
    #
    return sFormats


def _getPaddedCells( lRows, iSpaces = 1 ):
    #
    if iSpaces:
        #
        sPadding    = '&nbsp;' * iSpaces
        #
        lRows       = [ [ ''.join( ( sPadding, sCell, sPadding ) )
                        for sCell in lRow ]
                        for lRow in lRows ]
    #
    return lRows


def getHtmlTable( lRows, sCaption = '', sCaptionAlign = '', iSpaces = 0, **dFormats ):
    #
    from Iter.AllVers import iMap
    #
    if iSpaces:
        #
        lRows   = _getPaddedCells( lRows, iSpaces = iSpaces )
    #
    sFormats    = _getTableFormats( dFormats )
    #
    lRows       = iMap( getHtmlRow, lRows )
    #
    if sCaption:
        #
        if sCaptionAlign:
            #
            sCaptionAlign = ' align=%s' % sCaptionAlign # top|bottom default top
            #
        #
        sCaption    = '<caption%s>%s</caption>\n' % ( sCaptionAlign, sCaption )
        #
    #
    return '<table%s>\n%s<tr>%s</tr>\n</table>' % (
                sFormats,
                sCaption,
                '</tr>\n<tr>'.join( lRows ) )



def _getSpecialCharCode( uChar ):
    #
    """The Special Character Code for dot "." or 46 is "&#046;" -- got it?"""
    #
    iChar = uChar
    #
    if type( uChar ) == str:  iChar = ord( uChar )
    #
    return '&#' + _padWith0s( iChar ) + ';'



def _getSpecialCharCodes( sText ):
    #
    """
    Change all characters in sText to their
    Special Character Codes -- see _getSpecialCharCode().
    """
    #
    from Iter.AllVers import iMap
    #
    lChars  = iMap( _getSpecialCharCode, sText )
    #
    return ''.join( lChars )



def _getCharFromCode( s, bKeepLen ):
    #
    iLen        = len( s )
    #
    lParts      = s.split( ';' )
    #
    sCode       = lParts[0].lower()
    #
    if lParts: del lParts[0]
    #
    sRest       = ';'.join( lParts )
    #
    iCode       = -1
    #
    if 'x' in sCode and hasHexQuadDigitsOnly( sCode[1:] ):
        #
        sCode   = getTextAfter( sCode, 'x' )
        #
        iCode   = int( sNumb, 16 )
        #
    elif sCode.isdigit():
        #
        iCode   = int( sCode )
        #
    #
    if iCode < 256 and iCode > -1:
        #
        s       = '%s%s' % ( chr( iCode ), sRest )
        #
    else:
        #
        s       = '&#' + s
        #
    #
    if bKeepLen:
        #
        s       = s.ljust( iLen )
        #
    #
    return s


def getChars4SpecialCodes( sText, bKeepLen = False ):
    #
    """
    Change all Special Character Codes to
    their regular characters -- see _getSpecialCharCode().
    """
    #
    from Iter.AllVers   import iMap
    from String.Get import getTextBefore, getTextAfter
    #
    lBlocks         = sText.split( '&#' )
    #
    sFirst          = ''
    #
    if lBlocks:
        sFirst      = lBlocks[0]
        del lBlocks[0]
    #
    def getCharFromCode( s ): return _getCharFromCode( s, bKeepLen )
    #
    lBlocks         = iMap( getCharFromCode, lBlocks )
    #
    return sFirst + ''.join( lBlocks )




def ReplaceCharsWithSpecialCodes( sText, lCharNumbs, sTransStr = None ):
    #
    """
    For the characters listed by number in lCharNumbs,
    change such characters in sText to their
    Special Character Codes -- see _getSpecialCharCode().
    Note -- sText cannot include high bit chars!!!
    """
    #
    from Utils.Both2n3    import translate
    from String.Transform   import getTranslatorStr
    #
    sText           = sText.replace( chr(160), ' ' )    # used as white space on web pages
    #
    if sTransStr is None:
        #
        lRealChars  = [ chr( iChar       ) for iChar in lCharNumbs ]
        lHoldChars  = [ chr( iChar + 128 ) for iChar in lCharNumbs ]
        #
        sTransStr   = getTranslatorStr( ''.join(lRealChars), ''.join(lHoldChars) )
        #
    #
    sText           = translate( sText, sTransStr )
    #
    for iChar in lCharNumbs:
        #
        sText       = sText.replace( chr( iChar + 128 ), _getSpecialCharCode( iChar ) )
        #
    #
    return sText



def getBodyOnly( sHTML ):
    #
    lParts          = oFindBodyBeg.split( sHTML )
    #
    if len( lParts ) == 2:
        #
        sHTML       = lParts[ 1 ]
        #
        lParts      = oFindBodyEnd.split( sHTML )
        #
        if len( lParts ) == 2:
            #
            sHTML   = lParts[ 0 ]
            #
        #
    #
    return sHTML


_oBreakHereFinder = getFinder( '<(?!(?:u>|/|em>|wbr>|b(?:>| )))' )


def addLineBreaks( sHTML ):
    #
    '''
    some web sites skip line breaks in HTML for the web
    browsers are OK without line breaks, but if you
    want to bring the HTML into a text editor for a look,
    you might appreciate this function.
    '''
    #
    from String.Replace import getGlobalReplaceReSplits
    #
    return getGlobalReplaceReSplits( _oBreakHereFinder, sHTML, '\n<' )



def getTextgotYahooHTML( s ):
    #
    # also need to convert
    # &amp;quot;&amp;#39;***&amp;amp;!%%***&amp;amp;((&amp;#39;&amp;quot;
    # to
    # &quot;&#39;***&amp;!%%***&amp;((&#39;&quot;
    #
    # &#39;_@Mpz5HxJ&quot;7&#39;
    # to
    # '_@Mpz5HxJ"7'
    #
    from String.Test import isStringQuoted
    #
    while '&amp;' in s:
        #
        s = s.replace( '&amp;', '&' )
        #
    #
    s = getChars4HtmlCodes( getChars4SpecialCodes( s ) )
    #
    while isStringQuoted( s ):
        #
        s = s[ 1 : ][ : -1 ]
        #
    #
    return s








if __name__ == "__main__":
    #
    from six            import print_ as print3
    
    from Collect.Test   import AllMeet
    from Dict.Test      import isDict
    from Iter.AllVers   import lMap
    from String.Split   import getWhiteCleaned
    from Utils.Result   import sayTestResult
    #
    lProblems           = []
    #
    sLotsOTags          = ' '.join( _getCompleteTags() )
    #
    oWipeCompleteTags   = getCompleteTagsWiper()
    #
    sWiped              = oWipeCompleteTags( sLotsOTags )
    #
    if      len( sWiped ) != len( sLotsOTags ) or sWiped.strip():
        #
        lProblems.append( 'getCompleteTagsWiper()' )
        #
    if not _getIncompleteTags():
        #
        lProblems.append( '_getIncompleteTags()' )
        #
    if not _getEnvVariableTuple():
        #
        lProblems.append( '_getEnvVariableTuple()' )
        #
    #
    sEnv = """
        HTTP_ACCEPT = text/html, image/jpeg, image/png, text/*, image/*, */*
        HTTP_ACCEPT_CHARSET = utf-8, utf-8;q=0.5, *;q=0.5
        HTTP_ACCEPT_ENCODING = x-gzip, x-deflate, gzip, deflate
        HTTP_ACCEPT_LANGUAGE = en
        HTTP_CONNECTION = keep-alive
        HTTP_HOST = www.proxy.us.pl
        HTTP_REFERER = http://www.ipmaster.org/proxyjudge.html
        HTTP_USER_AGENT = Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)
        HTTP_X_FORWARDED_FOR = 58.136.93.228
        HTTP_VIA = 1.1 wc-bkksp112 (NetCache NetApp/6.0.1)
        REMOTE_ADDR = 58.136.93.228
        REMOTE_PORT = 35645
        REQUEST_URI = /azenv.php
        REQUEST_METHOD = GET
        REQUEST_TIME = 1178230337
    """
    #
    setVars = frozenset(
        ['HTTP_ACCEPT', 'HTTP_ACCEPT_CHARSET', 'HTTP_ACCEPT_ENCODING',
         'HTTP_ACCEPT_LANGUAGE', 'HTTP_CONNECTION', 'HTTP_HOST',
         'HTTP_REFERER', 'HTTP_USER_AGENT', 'HTTP_X_FORWARDED_FOR',
         'HTTP_VIA', 'REMOTE_ADDR', 'REMOTE_PORT', 'REQUEST_URI',
         'REQUEST_METHOD', 'REQUEST_TIME'] )
    #
    oEnvVarFinder = getEnvVariableFinder()
    #
    def isInVars( sVar ): return sVar in setVars
    #
    if not AllMeet( oEnvVarFinder.findall( sEnv ), isInVars ):
        #
        lProblems.append( 'getEnvVariableFinder()' )
        #
    #
    tHTMLntts = _getHTMLntts()
    #
    if len( tHTMLntts ) != 8 or not AllMeet( tHTMLntts, isDict ):
        #
        lProblems.append( '_getHTMLntts()' )
        #
    #
    sRow0 = ( 'eany', 'meany', 'miny', 'moe' )
    #
    if getHtmlRow( sRow0 ) != '<td>eany</td><td>meany</td><td>miny</td><td>moe</td>':
        #
        lProblems.append( 'getHtmlRow()' )
        #
    #
    dFormats =  dict(
            border = 2, cellpadding = 3, cellspacing = 5, width = '50%' )
    #
    if      _getTableFormats( dFormats ) != \
            ' border= 2 cellpadding = 3 cellspacing = 5 width = "50%"':
        #
        lProblems.append( '_getTableFormats()' )
        #
    sRow1 = ( 'spam', 'eggs', 'toast', 'beans' )
    #
    lRows = [ sRow0, sRow1 ]
    #
    if _getPaddedCells( lRows, iSpaces = 1 ) != \
            [['&nbsp;eany&nbsp;',  '&nbsp;meany&nbsp;',
              '&nbsp;miny&nbsp;',  '&nbsp;moe&nbsp;'   ],
             ['&nbsp;spam&nbsp;',  '&nbsp;eggs&nbsp;',
              '&nbsp;toast&nbsp;', '&nbsp;beans&nbsp;' ]]:
        #
        lProblems.append( '_getPaddedCells()' )
        #
    #
    sTableShouldBe = \
        '<table border= 2 cellpadding = 3 cellspacing = 5 width = "50%">\n' \
        '<caption align=bottom>Python</caption>\n' \
        '<tr><td>&nbsp;eany&nbsp;</td><td>&nbsp;meany&nbsp;</td>' \
            '<td>&nbsp;miny&nbsp;</td><td>&nbsp;moe&nbsp;</td></tr>\n' \
        '<tr><td>&nbsp;spam&nbsp;</td><td>&nbsp;eggs&nbsp;</td>' \
            '<td>&nbsp;toast&nbsp;</td><td>&nbsp;beans&nbsp;</td></tr>\n' \
        '</table>'
    #
    sTable = getHtmlTable( lRows, sCaption = 'Python',
                        sCaptionAlign = 'bottom', iSpaces = 1, **dFormats )
    #
    if sTable != sTableShouldBe:
        #
        lProblems.append( 'getHtmlTable()' )
        #
    #
    lCodes = ['&#065;', '&#101;', '&#073;', '&#111;', '&#085;']
    #
    if lMap( _getSpecialCharCode, 'AeIoU' ) != lCodes:
        #
        lProblems.append( '_getSpecialCharCode()' )
        #
    if _getSpecialCharCodes( 'AeIoU' ) != ''.join( lCodes ):
        #
        lProblems.append( '_getSpecialCharCodes()' )
        #
    #
    sCodes = ''.join( lCodes )
    #
    if      getChars4SpecialCodes( sCodes, bKeepLen = False ) != 'AeIoU' or \
            getChars4SpecialCodes( sCodes, bKeepLen = True ) != \
                'A   e   I   o   U   ':
        #
        lProblems.append( 'getChars4SpecialCodes()' )
        #
    sText = 'How now brown cow.'
    #
    if ReplaceCharsWithSpecialCodes( sText, [ 99, 111 ] ) != \
            'H&#111;w n&#111;w br&#111;wn &#099;&#111;w.':
        #
        lProblems.append( 'ReplaceCharsWithSpecialCodes()' )
        #
    #
    sHTML = '''
        <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML <2.0>//EN">
        <HTML><HEAD>
        <TITLE>404 Not Found</TITLE>
        </HEAD>
        <BODY><H1>Not Found</H1>
        The requested URL /nopage/index.html was not found on this server.<P>
        <P>Additionally, a 404 Not Found
        error was encountered while trying to use an ErrorDocument to handle the request.
        <HR>
        <ADDRESS>Apache/1.3.33 Server at www.advanced-app.com.hk Port 80</ADDRESS>
        </BODY></HTML>
    '''
    #
    sShouldBe = '''<H1>Not Found</H1>
        The requested URL /nopage/index.html was not found on this server.<P>
        <P>Additionally, a 404 Not Found
        error was encountered while trying to use an ErrorDocument to handle the request.
        <HR>
        <ADDRESS>Apache/1.3.33 Server at www.advanced-app.com.hk Port 80</ADDRESS>
        '''
    #
    if getBodyOnly( sHTML ) != sShouldBe:
        #
        lProblems.append( 'getBodyOnly()' )
        #
    #
    lHtmlTags = [   '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML <2.0>//EN">',
                    '<HTML>',
                    '<HEAD>',
                    '<TITLE>',
                    '</TITLE>',
                    '</HEAD>',
                    '<BODY>',
                    '<H1>',
                    '</H1>',
                    '<P>',
                    '<P>',
                    '<HR>',
                    '<ADDRESS>',
                    '</ADDRESS>',
                    '</BODY>',
                    '</HTML>' ]
    #
    if oTagFinder.findall( sHTML ) != lHtmlTags:
        #
        lProblems.append( 'oTagFinder()' )
        #
    #
    #
    sHTMLCoded = \
        "<table><tr><td><b>Variable</b></td><td>&nbsp;</td>" \
        "<td><b>Value</b></td></tr><tr><td>" \
        "&#72;&#84;&#84;&#80;&#95;&#67;&#79;&#78;&#78;&#69;&#67;&#84;&#73;&#79;&#78;" \
        "</td><td>&nbsp;</td><td>&#107;&#101;&#101;&#112;-&#97;&#108;&#105;&#118;" \
        "&#101;</td></tr><tr><td><FONT color='orange'>" \
        "&#72;&#84;&#84;&#80;&#95;&#86;&#73;&#65;</FONT></td><td>&nbsp;</td>" \
        "<td>&#49;&#46;&#49; &#119;&#99;-&#98;&#107;&#107;&#115;&#112;&#49;&#49;&#50; " \
        "(&#78;&#101;&#116;&#67;&#97;&#99;&#104;&#101; " \
        "&#78;&#101;&#116;&#65;&#112;&#112;&#47;&#54;&#46;&#48;&#46;&#49;)</td></tr>" \
        "<tr><td>" \
        "<FONT color='orange'>&#72;&#84;&#84;&#80;&#95;&#88;&#95;&#70;&#79;" \
        "&#82;&#87;&#65;&#82;&#68;&#69;&#68;&#95;&#70;&#79;&#82;</FONT></td>" \
        "<td>&nbsp;</td><td><FONT color='red'>&#53;&#56;&#46;&#49;&#51;&#54;" \
        "&#46;&#57;&#51;&#46;&#53;&#52;</FONT></td></tr>" \
        "<tr><td>&#82;&#69;&#77;&#79;&#84;&#69;&#95;&#65;&#68;&#68;&#82;</td>" \
        "<td>&nbsp;</td><td><FONT color='red'>&#53;&#56;&#46;&#49;&#51;&#54;&#46;" \
        "&#57;&#51;&#46;&#53;&#52;</FONT></td></tr>" \
        "<tr><td>&#82;&#69;&#77;&#79;&#84;&#69;&#95;&#72;&#79;&#83;&#84;</td>" \
        "<td>&nbsp;</td><td><FONT color='red'>&#112;&#55;&#52;&#50;&#48;-&#97;&#100;" \
        "&#115;&#108;&#98;&#107;&#107;&#115;&#112;&#55;&#46;&#67;&#46;&#99;&#115;" \
        "&#108;&#111;&#120;&#105;&#110;&#102;&#111;&#46;&#110;&#101;&#116;</FONT>" \
        "</td></tr></table>"
    #
    sHTMLPlain = \
        "<table><tr><td><b>Variable</b></td><td>\xa0</td><td><b>Value</b></td></tr>" \
        "<tr><td>HTTP_CONNECTION</td><td>\xa0</td><td>keep-alive</td></tr>" \
        "<tr><td><FONT color='orange'>HTTP_VIA</FONT></td><td>\xa0</td>" \
        "<td>1.1 wc-bkksp112 (NetCache NetApp/6.0.1)</td></tr>" \
        "<tr><td><FONT color='orange'>HTTP_X_FORWARDED_FOR</FONT></td>" \
        "<td>\xa0</td><td><FONT color='red'>58.136.93.54</FONT></td></tr>" \
        "<tr><td>REMOTE_ADDR</td><td>\xa0</td>" \
        "<td><FONT color='red'>58.136.93.54</FONT></td></tr>" \
        "<tr><td>REMOTE_HOST</td><td>\xa0</td>" \
        "<td><FONT color='red'>p7420-adslbkksp7.C.csloxinfo.net</FONT></td></tr>" \
        "</table>"
    #
    oHTMLnttSwapper = HTMLnttSwappersClass()
    #
    if oHTMLnttSwapper.getChars4HtmlCodes( sHTMLCoded ) != sHTMLPlain:
        #
        lProblems.append( 'oHTMLnttSwapper.getChars4HtmlCodes()' )
        #
    #
    if getChars4HtmlCodes( sHTMLCoded ) != sHTMLPlain:
        #
        lProblems.append( 'getChars4HtmlCodes()' )
        #
    #
    # print3( getChars4HtmlCodes( 'Town &Amp; Country Condo' ) )
    #
    sCleanHTML = getWhiteCleaned( sHTML ).replace( '> <', '><' )
    #
    sBreaksInHTML = '''
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML
<2.0>//EN">
<HTML>
<HEAD>
<TITLE>404 Not Found</TITLE></HEAD>
<BODY>
<H1>Not Found</H1> The requested URL /nopage/index.html was not found on this server.
<P>
<P>Additionally, a 404 Not Found error was encountered while trying to use an ErrorDocument to handle the request.
<HR>
<ADDRESS>Apache/1.3.33 Server at www.advanced-app.com.hk Port 80</ADDRESS></BODY></HTML>'''
    #
    if addLineBreaks( sCleanHTML ) != sBreaksInHTML:
        #
        lProblems.append( 'addLineBreaks()' )
        #
    #
    # need function to convert 
    # '&#39;6RCOz&#92;&#39;a&quot;GlO&#39;'
    # to
    # '6RCOz\'a"GlO'
    #
    sOrig = '&#39;6RCOz&#92;&#39;a&quot;GlO&#39;'
    sWant = r'''6RCOz\'a"GlO'''
    #
    sGot    = getTextgotYahooHTML( sOrig )
    #
    if sGot != sWant:
        #
        print3( 'want: ', sWant )
        print3( 'got:  ', sGot  ) 
        lProblems.append( 'getTextgotYahooHTML()' )
        #
    #
    sOrig = '&#39;_@Mpz5HxJ&quot;7&#39;'
    sWant = '_@Mpz5HxJ"7'
    #
    sGot    = getTextgotYahooHTML( sOrig )
    #
    if sGot != sWant:
        #
        print3( 'want: ', sWant )
        print3( 'got:  ', sGot  ) 
        lProblems.append( 'getTextgotYahooHTML()' )
        #
    #
    sayTestResult( lProblems )