#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions Error
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

def _getErrorPatterns():
    #
    from re import compile as REcompile
    #
    from Collect.Get import getNewKeysTuple4Items
    #
    lErrorPatterns = [
        ( r'(?is)<TITLE>.*?(404|403).*?ERROR.*?</TITLE>'    , 0.95 ),
        ( r'(?is)<TITLE>.*?403.*?Forbidden.*?</TITLE>'      , 0.95 ),
        ( r'(?is)<TITLE>.*?ERROR.*?(404|403).*?</TITLE>'    , 0.95 ),
        ( r'(?is)<TITLE>.*?503.*?Unavailable.*?</TITLE>'    , 0.85 ),
        ( r'(?is)<META .*?(404|403).*?ERROR.*?>'            , 0.80 ),
        ( r'(?is)<META .*?ERROR.*?(404|403).*?>'            , 0.80 ),
        ( r'(?is)<TITLE>.*?File Not Found.*?</TITLE>'       , 0.80 ),
        ( r'(?is)<title>.*?Police Ale(a?)rt.*?</title>'     , 0.80 ),
        ( r'(?is)<TITLE>.*?Not Found.*?</TITLE>'            , 0.40 ),
        ( r'(?is)<TITLE>.*?page cannot be found.*?</TITLE>' , 0.80 ),
        ( r'(?is)<TITLE>ERROR</TITLE>'                      , 0.30 ),
        ( r'(?is)<H1>.*?not found.*?</H1>'                  , 0.15 ),
        ( r'(?is)<H1>.*?(404|403).*?</H1>'                  , 0.15 ),
        ( r'(?is)<TITLE>.*?ERROR.*?</TITLE>'                , 0.10 ),
        ( r'(?is)<BODY.*(404|403)'                          , 0.10 ),
        ( r'(?is)<BODY.*not found'                          , 0.10 ),
        ( r'(?is)<BODY.*the requested URL'                  , 0.10 ),
        ( r'(?is)<BODY.*the page you requested'             , 0.10 ),
        ( r'(?is)<BODY.*page.{1,50}unavailable'             , 0.10 ),
        ( r'(?is)<BODY.*request.{1,50}unavailable'          , 0.10 ),
        ( r'(?is)<BODY.*web site.{1,50}has been closed'     , 0.10 ),
        ( r'(?i)does not exist'                             , 0.10 )  ]
    #
    lErrorPatterns.append(
        ( r'(?is)<BODY.*ict.cyberclean.org'                 , 0.95 ) )# Thailand specific
    #
    return getNewKeysTuple4Items( lErrorPatterns, REcompile )

tErrorPatterns = _getErrorPatterns()


def _getErrorOrWhat( sHTML ):
    #
    # inspired by code in Text Processing with Python by David Mertz
    #
    # import sys
    #
    # sHTML = sys.stdin.read()
    #
    if len( sHTML ) == 0: return 0.0
    #
    # Mapping from patterns to probability contribution of pattern
    #
    fErrScore = 0
    #
    for oPattern, fProbable in tErrorPatterns:
        #
        if oPattern.search( sHTML ):
            #
            fErrScore += fProbable
            #
        if fErrScore > 0.9: break

    return fErrScore


def getErrorPerCent( sHTML ):
    #
    from Numb.Stats import getPercent
    #
    fErrScore = _getErrorOrWhat( sHTML )
    #
    return getPercent( fErrScore )



tScores = ( .25, .5, .75, .9, .99 )

tOut    = ( 'Page is probably content; error chance ',
            'Fair indication page is an error report',
            'Better-than-even odds page is error report',
            'It is highly likely page is an error report',
            'Page is almost surely an error report',
            'Page is definitely an error report', )

def sayGetErrorOrWhat( fErrScore ):
    #
    from bisect import bisect_left
    #
    from Numb.Stats import getPercent
    #
    #if   fErrScore > 0.90: sOut = 'Page is almost surely an error report'
    #elif fErrScore > 0.75: sOut = 'It is highly likely page is an error report'
    #elif fErrScore > 0.50: sOut = 'Better-than-even odds page is error report'
    #elif fErrScore > 0.25: sOut = 'Fair indication page is an error report'
    #else:                  sOut = 'Page is probably real content'
    #
    return '%s -- %s%s' % \
                ( tOut[ bisect_left( tScores, fErrScore ) ],
                str( getPercent( fErrScore ) ),
                '%' )


if __name__ == "__main__":
    #
    from Collect.Test   import AllMeet
    from Iter.AllVers   import iMap, tMap
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    s404simple = '''
        <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
        <HTML><HEAD>
        <TITLE>404 Not Found</TITLE>
        </HEAD><BODY>
        <H1>Not Found</H1>
        The requested URL /nopage/index.html was not found on this server.<P>
        <P>Additionally, a 404 Not Found
        error was encountered while trying to use an ErrorDocument to handle the request.
        <HR>
        <ADDRESS>Apache/1.3.33 Server at www.advanced-app.com.hk Port 80</ADDRESS>
        </BODY></HTML>
    '''
    #
    s404fancy = '''
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
        <html dir=ltr>
        <head>
        <style>
        a:link			{font:8pt/11pt verdana; color:FF0000}
        a:visited		{font:8pt/11pt verdana; color:#4e4e4e}
        </style>
        <META NAME="ROBOTS" CONTENT="NOINDEX">
        <title>The page cannot be found</title>
        <META HTTP-EQUIV="Content-Type" Content="text-html; charset=Windows-1252">
        </head>
        <script>
        function Homepage(){
        <!--
        // in real bits, urls get returned to our script like this:
        // res://shdocvw.dll/http_404.htm#http://www.DocURL.com/bar.htm
                //For testing use DocURL = "res://shdocvw.dll/http_404.htm#https://www.microsoft.com/bar.htm"
                DocURL = document.URL;
                //this is where the http or https will be, as found by searching for :// but skipping the res://
                protocolIndex=DocURL.indexOf("://",4);
                //this finds the ending slash for the domain server
                serverIndex=DocURL.indexOf("/",protocolIndex + 3);
                        //for the href, we need a valid URL to the domain. We search for the # symbol to find the begining
                //of the true URL, and add 1 to skip it - this is the BeginURL value. We use serverIndex as the end marker.
                //urlresult=DocURL.substring(protocolIndex - 4,serverIndex);
                BeginURL=DocURL.indexOf("#",1) + 1;
                urlresult=DocURL.substring(BeginURL,serverIndex);
                //for display, we need to skip after http://, and go to the next slash
                displayresult=DocURL.substring(protocolIndex + 3 ,serverIndex);
                InsertElementAnchor(urlresult, displayresult);
        }
        function HtmlEncode(text)
        {
            return text.replace(/&/g, '&amp').replace(/'/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        }
        function TagAttrib(name, value)
        {
            return ' '+name+'="'+HtmlEncode(value)+'"';
        }
        function PrintTag(tagName, needCloseTag, attrib, inner){
            document.write( '<' + tagName + attrib + '>' + HtmlEncode(inner) );
            if (needCloseTag) document.write( '</' + tagName +'>' );
        }
        function URI(href)
        {
            IEVer = window.navigator.appVersion;
            IEVer = IEVer.substr( IEVer.indexOf('MSIE') + 5, 3 );
            return (IEVer.charAt(1)=='.' && IEVer >= '5.5') ?
                encodeURI(href) :
                escape(href).replace(/%3A/g, ':').replace(/%3B/g, ';');
        }
        function InsertElementAnchor(href, text)
        {
            PrintTag('A', true, TagAttrib('HREF', URI(href)), text);
        }
        //-->
        </script>
        <body bgcolor="FFFFFF">
        <table width="410" cellpadding="3" cellspacing="5">
        <tr>
            <td align="left" valign="middle" width="360">
                <h1 style="COLOR:000000; FONT: 13pt/15pt verdana"><!--Problem-->The page cannot be found</h1>
            </td>
        </tr>
        <tr>
            <td width="400" colspan="2">
                <font style="COLOR:000000; FONT: 8pt/11pt verdana">The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.</font></td>
        </tr>
        <tr>
            <td width="400" colspan="2">
                <font style="COLOR:000000; FONT: 8pt/11pt verdana">
                <hr color="#C0C0C0" noshade>
            <p>Please try the following:</p>
                <ul>
            <li>If you typed the page address in the Address bar, make sure that it is spelled correctly.<br>
            </li>
            <li>Open the
                <script>
                <!--
                if (!((window.navigator.userAgent.indexOf("MSIE") > 0) && (window.navigator.appVersion.charAt(0) == "2")))
                {
                        Homepage();
                }
                //-->
                </script>
                home page, and then look for links to the information you want.</li>
            <li>Click the <a href="javascript:history.back(1)">Back</a> button to try another link.</li>
            </ul>
            <h2 style="font:8pt/11pt verdana; color:000000">HTTP 404 - File not found<br>
            Internet Information Services<BR></h2>
                <hr color="#C0C0C0" noshade>
                <p>Technical Information (for support personnel)</p>
        <ul>
        <li>More information:<br>
        <a href="http://www.microsoft.com/ContentRedirect.asp?prd=iis&sbp=&pver=5.0&pid=&ID=404&cat=web&os=&over=&hrd=&Opt1=&Opt2=&Opt3=" target="_blank">Microsoft Support</a>
        </li>
        </ul>
            </font></td>
        </tr>
        </table>
        </body>
        </html>
    '''
    #
    sCyberCleanBlocked = '''
        <BODY BGCOLOR="#CCFFCC" TEXT="black" LINK="lime" VLINK="#33CC00" ALINK="#009900">
        <P ALIGN="center"><SPAN STYLE="font-size:36pt;"><FONT FACE="Arial Unicode MS"><A HREF="http://ict.cyberclean.org/modules/cyberclean2" TARGET="_parent"><IMG SRC="http://w3.mict.go.th/ci/logo54.gif" BORDER="0"></A></FONT></SPAN><P ALIGN="center"><B><SPAN STYLE="font-family:'Angsana New'; font-size:36pt;"><FONT FACE="Arial Unicode MS" COLOR="#003300">&#3586;&#3629;&#3629;&#3616;&#3633;&#3618;</FONT></SPAN></B></p>
        <H4 ALIGN="center"><SPAN STYLE="font-family:'Angsana New'; font-size:20pt;"><font face="Microsoft Sans Serif" color="#003300">&#3648;&#3623;&#3655;&#3610;&#3652;&#3595;&#3605;&#3660;&#3609;&#3637;&#3657;&#3648;&#3611;&#3655;&#3609;&#3648;&#3623;&#3655;&#3610;&#3652;&#3595;&#3605;&#3660;&#3607;&#3637;&#3656;&#3652;&#3617;&#3656;&#3648;&#3627;&#3617;&#3634;&#3632;&#3626;&#3617;</font></SPAN><font face="Microsoft Sans Serif"></font>
            <H4
        ALIGN="center"><B><SPAN STYLE="font-family:'Angsana New'; font-size:20pt;"><font face="Microsoft Sans Serif" color="#0066CC">&#3585;&#3619;&#3632;&#3607;&#3619;&#3623;&#3591;&#3648;&#3607;&#3588;&#3650;&#3609;&#3650;&#3621;&#3618;&#3637;&#3626;&#3634;&#3619;&#3626;&#3609;&#3648;&#3607;&#3624;&#3649;&#3621;&#3632;&#3585;&#3634;&#3619;&#3626;&#3639;&#3656;&#3629;&#3626;&#3634;&#3619;</font></SPAN></B><font face="Microsoft Sans Serif"></font>
                <H4 ALIGN="center"><SPAN STYLE="font-family:'Angsana New'; font-size:20pt;"><font face="Microsoft Sans Serif" color="#003300">&#3650;&#3604;&#3618;&#3652;&#3604;&#3657;&#3619;&#3633;&#3610;&#3588;&#3623;&#3634;&#3617;&#3619;&#3656;&#3623;&#3617;&#3617;&#3639;&#3629;&#3592;&#3634;&#3585;&#3612;&#3641;&#3657;&#3651;&#3627;&#3657;&#3610;&#3619;&#3636;&#3585;&#3634;&#3619;&#3629;&#3636;&#3609;&#3648;&#3607;&#3629;&#3619;&#3660;&#3648;&#3609;&#3655;&#3605;</font></SPAN><font face="Microsoft Sans Serif"></font>
                    <H4 ALIGN="center"><SPAN STYLE="font-family:'Angsana New'; font-size:20pt;"><font face="Microsoft Sans Serif" color="#003300">&#3649;&#3621;&#3632;&#3610;&#3619;&#3636;&#3625;&#3633;&#3607; &#3585;&#3626;&#3607; &#3650;&#3607;&#3619;&#3588;&#3617;&#3609;&#3634;&#3588;&#3617; &#3592;&#3635;&#3585;&#3633;&#3604; (&#3617;&#3627;&#3634;&#3594;&#3609;)</font></SPAN><font face="Microsoft Sans Serif"></font>
                        <H4
        ALIGN="center"><SPAN STYLE="font-family:'Angsana New'; font-size:20pt;"><font face="Microsoft Sans Serif" color="#003300">&#3592;&#3635;&#3648;&#3611;&#3655;&#3609;&#3605;&#3657;&#3629;&#3591;&#3611;&#3636;&#3604;&#3585;&#3633;&#3657;&#3609;&#3648;&#3623;&#3655;&#3610;&#3652;&#3595;&#3605;&#3660;&#3609;&#3637;&#3657;</font></SPAN><font face="Microsoft Sans Serif"></font>
                            <H4 ALIGN="center"><B><SPAN STYLE="font-family:'Angsana New'; font-size:20pt;"><font face="Microsoft Sans Serif" color="#CC6600">&#3627;&#3634;&#3585;&#3617;&#3637;&#3586;&#3657;&#3629;&#3588;&#3636;&#3604;&#3648;&#3627;&#3655;&#3609;&#3629;&#3639;&#3656;&#3609;&#3651;&#3604; &#3627;&#3619;&#3639;&#3629;&#3614;&#3610;&#3648;&#3623;&#3655;&#3610;&#3652;&#3595;&#3605;&#3660;&#3629;&#3639;&#3656;&#3609;&#3607;&#3637;&#3656;&#3652;&#3617;&#3656;&#3648;&#3627;&#3617;&#3634;&#3632;&#3626;&#3617;</font></SPAN></B><font face="Microsoft Sans Serif"></font>
                                <H4 ALIGN="center"><B><SPAN STYLE="font-family:'Angsana New'; font-size:20pt;"><font face="Microsoft Sans Serif" color="#CC6600">&#3650;&#3611;&#3619;&#3604;&#3649;&#3592;&#3657;&#3591;&#3612;&#3656;&#3634;&#3609;&#3604;&#3623;&#3591;&#3605;&#3634;&#3586;&#3657;&#3634;&#3591;&#3610;&#3609;&#3627;&#3619;&#3639;&#3629;</font></SPAN></B><font face="Microsoft Sans Serif"></font></H4>
                                <H4 ALIGN="center"><B><A HREF="http://ict.cyberclean.org/modules/cyberclean2"><SPAN STYLE="font-family:'Angsana New'; font-size:20pt;"><font face="Microsoft Sans Serif" color="red">ict.cyberclean.org</font></SPAN></A></B></H4>
                                <p align="center">( Sorry! the web site you are accessing has been blocked by ministry of information and communication technology )</p>
                                <P>&nbsp;
    '''
    #
    sThaiPoliceBlocked = '''
        <!-- saved from url=(0022)http://internet.e-mail -->
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
        <html>
        <head>
        <!-- Blocked By ICT -->
        <!-- TemplateBeginEditable name="doctitle" -->
        <title>Police Aleart</title>
        <!-- TemplateEndEditable -->
        <meta http-equiv="Content-Type" content="text/html; charset=windows-874">
        <!-- TemplateBeginEditable name="head" -->
        <!-- TemplateEndEditable -->
        </head>
        <body>
        <div align="center">
        <p><br>
            <br>
        </p>
        <p>&nbsp; </p>
        <table width="75" border="1" align="center" cellpadding="0" cellspacing="0" bordercolor="#006699">
            <tr>
            <td><table width="676" border="0" cellpadding="8" cellspacing="0" bordercolor="#0066FF" bgcolor="#CFE7FF">
                <tr>
                    <td><div align="center">���ҧ�ѡҹ�Ǩ�觪ҵԢ�ЧѺ���u����䫵��
                        ��ҡ��� ����w������ � �a͹Ҩ� �ѹ
                        <br>
                        ����µ����ͧҵ�/div></td>
                </tr>
                <tr>
                    <td width="666"><p align="center">���������� "����Ţ�ʹ�&quot;
                        �� 19 � 2 �ѡҹ�Ǩ�觪ҵ�<br>
                        ��� �� �10330 � 0-2251-0164 �� webmaster@police.go.th
                    </p>
                    <p align="center"><a href="http://www.police.go.th/crimewebpost/report/sum.php">ʶԵԡ����Դ��ͧ�ѡҹ�Ǩ�觪ҵ�/a></p></td>
                </tr>
                <tr>
                    <td> <hr align="center"> </td>
                </tr>
                <tr>
                    <td height="65"><div align="center">Sorry, the web site you are accessing
                        has been closed by Royal Thai Police due to inappropriateness
                        such as pornography, gambling or contain any information which
                        is deemed to violate national security. </div></td>
                </tr>
                <tr>
                    <td><p align="center">For more information, please contact "Police
                        Information System Center&quot; Bld#19 2nd Flr, Royal Thai Police,
                        Rama I, Patumwan, Bangkok 10330 Tel. 0-2251-0164, <br>
                        email : webmaster@police.go.th </p>
                    <p align="center"><a href="http://www.police.go.th">http://www.police.go.th</a></p>
                    </td>
                </tr>
                </table></td>
            </tr>
        </table>
        <p>&nbsp;</p>
        </div>
        <p>&nbsp;</p>
        <p>&nbsp;</p>
        <p>&nbsp;</p>
        </body>
        </html>
    '''
    #
    sUnavailable = '''
        <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
        <HTML><HEAD>
        <TITLE>503 Service Temporarily Unavailable</TITLE>
        </HEAD><BODY>
        <H1>Service Temporarily Unavailable</H1>
        The server is temporarily unable to service your
        request due to maintenance downtime or capacity
        problems. Please try again later.
        </BODY></HTML>
    '''
    #
    lPageSource = [ s404simple, s404fancy, sCyberCleanBlocked,
                    sThaiPoliceBlocked, sUnavailable ]
    #
    lScores     = tMap( _getErrorOrWhat, lPageSource )
    #
    def FairOrBetter( f ): return f > .75
    #
    if not AllMeet( lScores, FairOrBetter ):
        #
        lProblems.append( '_getErrorOrWhat()' )
        #
    lPerCents   = iMap( getErrorPerCent, lPageSource )
    #
    def FairOrBetter( f ): return f > 75
    #
    if not AllMeet( lPerCents, FairOrBetter ):
        #
        lProblems.append( 'getErrorPerCent()' )
        #
    if not tMap( sayGetErrorOrWhat, lScores ):
        #
        lProblems.append( 'sayGetErrorOrWhat()' )
        #

    #
    sayTestResult( lProblems )