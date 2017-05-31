#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# string functions Text4Tests.py
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
# Copyright 2011-2016 Rick Graves
#

sHTML =  (
    '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n'
    '<html>\n'
    '<head>\n'
    '<title>The New York Times - Breaking News, World News & Multimedia</title>\n'
    '<meta  http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>\n'
    '<style type="text/css">\n'
    '@import url(http://graphics8.nytimes.com/css/home/screen/general.css); \n'
    '</style>\n'
    '<!--[if IE 7]>\n'
    '<style type="text/css"> @import url(http://graphics8.nytimes.com/css/home/screen/ie7.css); </style>\n'
    '<![endif]-->\n'
    '<script type="text/javascript" language="JavaScript"'
    'src="http://graphics8.nytimes.com/js/common/screen/DropDown.js"></script>\n'
    '</head>\n'
    '<body><a name="top"></a>\n'
    '<!-- ADXINFO classification="blank" campaign="dynlog30"-->'
    '<script src="http://content.dl-rms.com/rms/8001/nodetag.js"></script>\n'
    '<!-- ADXINFO classification="text_ad" campaign="tacoda-trackingtag"-->'
    '<SCRIPT LANGUAGE="JavaScript">var tcdacmd="dt";</SCRIPT>\n'
    '<h2>\n'
    '<a href="http://www.nytimes.com/aponline/world/AP-WorldBank-Wolfowitz.html?hp">Wolfowitz to Leave the World Bank</a>\n'
    '</h2>\n'
    '<div class="aColumn">\n'
    '<div class="byline">By THE ASSOCIATED PRESS&nbsp;<span class="timestamp">27 minutes ago</span></div>\n'
    '<p class="summary">'
    'Embattled World Bank President Paul D. Wolfowitz will resign at the end of June, the World Bank board announced. \n'
    "Mr. Wolfowitz's departure ends a two-year run at the development bank that was marked by controversy.</p>\n"
    '<SCRIPT SRC="http://an.tacoda.net/an/12985/slf.js" LANGUAGE="JavaScript"></SCRIPT>\n'
    '<!-- ADXINFO classification="blank-but-count-imps" campaign="inv-homepage-HHI100"-->'
    '<img src="http://graphics8.nytimes.com/ads/blank.gif">  \n'
    '</body>\n'
    '</html>\n' )


sBlanked = \
'''                                                                                                      
<html>
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
<body>              </a>
                                                                                                                               
                                                                                                                              
<h2>
                                                                               Wolfowitz to Leave the World Bank</a>
</h2>
                     
                    By THE ASSOCIATED PRESS&nbsp;                        27 minutes ago</span></div>
                   Embattled World Bank President Paul D. Wolfowitz will resign at the end of June, the World Bank board announced. 
Mr. Wolfowitz's departure ends a two-year run at the development bank that was marked by controversy.</p>
                                                                                  
                                                                                                                                            
</body>
</html>
'''


tWantBlanks = (
    '<!DOCTYPE HTML .*?>',
    '<script.*?</script>',
    '<title>.*?</title>',
    '<style .*?</style>',
    '<head>.*?</head>',
    '<a href=.*?>',
    '<meta .*?/>',
    '<!--.*?-->',
    '<span .*?>',
    '<div .*?>',
    '<img .*?>',
    '<a .*?>',
    '<p.*?>' )


ttDelims = [ sDelims.split( '.*?' ) for sDelims in tWantBlanks ]


sHtmlTable = \
'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="content-language" content="en" />
<meta name="robots" content="index,follow" />
<meta name="rating" content="general" />
<meta name="author" content="centosweb@centos.org" />
<meta name="generator" content="XOOPS" />
<title>www.centos.org - centos.org content</title>
<link href="/favicon.ico" rel="SHORTCUT ICON" />
<link rel="stylesheet" type="text/css" media="all" href="http://www.centos.org/xoops.css" />
<link rel="stylesheet" type="text/css" media="all" href="http://www.centos.org/themes/centos/styleNN.css" />


        <!-- these two are not necessary, they are for the layout of this page itself; not transmenus. -->
        <link rel="stylesheet" type="text/css" href="http://www.centos.org/menu/static/styles.css" />

        <!-- these two are required for transmenus to function -->
        <link rel="stylesheet" type="text/css" href="http://www.centos.org/menu/static/transmenu.css" />
        <script type="text/javascript" src="http://www.centos.org/menu/static/transmenu.js"></script>

                                   <script type="text/javascript" src="http://www.centos.org/menu/mh_e.js"></script>
                </head>

<body onload="init()">

<table border="0" cellpadding="0" cellspacing="0" id="okvir">
  <tr>
    <td>
      <table cellspacing="0">
      <tr>
      <td>
      <table cellspacing="0">
        <tr >
          <td colspan="1" rowspan="1" style="vertical-align: middle; text-align: left; width: 63px">
             <a href="http://www.centos.org/"><img src="http://www.centos.org/themes/centos/images/centos_icon_60.png" alt="CentOS Icon" border="0" /></a>
          </td>
          <td colspan="1" rowspan="1" style="vertical-align: middle; text-align: left; ">
             <a href="http://www.centos.org/"><img src="http://www.centos.org/themes/centos/images/centos_logo_45.png" alt="CentOS Logo" border="0" /></a>
          </td>
        </tr>
        <tr>
          <td colspan="2" rowspan="1" style="vertical-align: top; text-align: left; font-weight: bold; font-size: 13px; font-family: Verdana, Arial, Helvetica, sans-serif; ">
<a href="http://www.centos.org/"><img src="http://www.centos.org/themes/centos/images/centos_text2.png" alt="CentOS Text" border="0" /></a>
          </td>
        </tr>
      </table>
      </td>
      <td>
      &nbsp; &nbsp;
      </td>
      <td width="100%" align="right">
      </td>
      </tr>
      </table>

      <table width="100%" cellspacing="0">
        <tr>
          <td colspan="1" rowspan="1" style="vertical-align: middle; text-align: left;">
            <div id="wrap">
              <div id="menu">
<a id="m1" href="http://www.centos.org">Home</a>
<a id="m2" href="http://www.centos.org/modules/tinycontent/index.php?id=23">Donate</a>
<a id="m3" href="">Information <img src="/menu/img/down_pointer.png" alt=""/></a>
<a id="m4" href="">Support <img src="/menu/img/down_pointer.png" alt=""/></a>
<a id="m5" href="http://wiki.centos.org/">Wiki <img src="/menu/img/down_pointer.png" alt=""/></a>
<a id="m6" href="/modules/tinycontent/index.php?id=15">Downloads <img src="/menu/img/down_pointer.png" alt=""/></a>
<a id="m7" href="">Contact Us <img src="/menu/img/down_pointer.png" alt=""/></a>
<a id="m8" href="/search.php">Search</a>
<a id="m10" href="https://www.centos.org/register.php">Register</a>
<a id="m11" href="https://www.centos.org/user.php">Login</a>
<noscript> <table><tr><td><center><a href="need_javascript.html">This site uses JavaScript, Click for Info</a></center></td></tr></table></noscript>
                   <script type="text/javascript" src="http://www.centos.org/menu/mb_e.js"></script>
                              </div>
            </div>
          </td>
        </tr>
      </table>
<!-- body start -->
      <table border="0" cellpadding="0" cellspacing="0" id="cter">
        <tr>
          <td id="centercolumn">
             <!-- End display center blocks -->
            <div id="content"> <span style="font-size: x-large;">CentOS Public Mirrors</span>
<table border=0 width=100%><td colspan=5><p><b>Tier 1 (OC3 or faster)</b></p></td>
<tr><td align=center><b>&nbsp;<br>Country (Region)</b></td><td align=center ><b>&nbsp;<br>State (Area)</b></td><td ><b>&nbsp;<br>Organization Name</b></td><td ><b>&nbsp;<br>Versions</b></td><td ><b>&nbsp;<br>Architectures</b></td><td><b>Direct DVD<br>Downloads</b></td></tr>
<tr><td align=center valign=middle>Canada</td><td align=center valign=middle>AB</td><td><a href='http://www.arcticnetwork.ca/'>Arctic Network Mirrors</a></td><td align=center>All</td><td>All</td><td align=center>no</td><td align=center><a href='http://centos.arcticnetwork.ca/'>&nbsp;HTTP&nbsp;</a> </td><td align=center>
<a href='ftp://ftp.arcticnetwork.ca/pub/centos/'>&nbsp;FTP&nbsp;</a> </td><td align=center>
<a href='rsync://rsync.arcticnetwork.ca/centos/'>&nbsp;RSYNC&nbsp;</a> </td></tr>
<tr><td align=center valign=middle>Canada</td><td align=center valign=middle>AB</td><td><a href='http://www.telus.net/'>TELUS Communications Inc</a></td><td align=center>All</td><td>All</td><td align=center>no</td><td align=center><a href='http://ftp.telus.net/pub/centos/'>&nbsp;HTTP&nbsp;</a> </td><td align=center>
<a href='ftp://ftp.telus.net/pub/centos/'>&nbsp;FTP&nbsp;</a> </td><td align=center>
</td></tr>
<tr><td><small><small><small>&nbsp;</small></small></small></td></tr>
<tr><td align=center valign=middle>US</td><td align=center valign=middle>AK</td><td><a href='http://www.gina.alaska.edu/'>University of Alaska - GINA</a></td><td align=center>All</td><td>All</td><td align=center>no</td><td align=center><a href='http://dds.gina.alaska.edu/public/mirrors/centos/'>&nbsp;HTTP&nbsp;</a> </td><td align=center>
<a href='ftp://dds.gina.alaska.edu/mirrors/centos/'>&nbsp;FTP&nbsp;</a> </td><td align=center>
</td></tr>
<tr><td align=center valign=middle>US</td><td align=center valign=middle>AZ</td><td><a href='http://www.easynews.com/'>Easynews</a></td><td align=center>All</td><td>All</td><td align=center>no</td><td align=center><a href='http://mirrors.easynews.com//linux/centos/'>&nbsp;HTTP&nbsp;</a> </td><td align=center>
<a href='ftp://mirrors.easynews.com//linux/centos'>&nbsp;FTP&nbsp;</a> </td><td align=center>
</td></tr>
<tr><td align=center valign=middle>US</td><td align=center valign=middle>CA</td><td><a href='http://csumb.edu/'>CSU Monterey Bay</a></td><td align=center>All</td><td>All</td><td align=center><b>Yes</b></td><td align=center><a href='http://mirrors.csumb.edu/centos/'>&nbsp;HTTP&nbsp;</a> </td><td align=center>
</td><td align=center>
</td></tr>
<tr><td align=center valign=middle>US</td><td align=center valign=middle>CA</td><td><a href='http://www.hmc.edu'>Harvey Mudd College</a></td><td align=center>All</td><td>All</td><td align=center>no</td><td align=center><a href='http://yum.math.hmc.edu/os/centos/'>&nbsp;HTTP&nbsp;</a> </td><td align=center>
</td><td align=center>
</td></tr>
<tr><td><small><small><small>&nbsp;</small></small></small></td></tr>
<tr><td align=center valign=middle>US</td><td align=center valign=middle>CA</td><td><a href='http://www.kernel.org/'>Linux Kernel Archives</a></td><td align=center>All</td><td>All</td><td align=center><b>Yes</b></td><td align=center><a href='http://mirrors.kernel.org/centos/'>&nbsp;HTTP&nbsp;</a> </td><td align=center>
<a href='ftp://mirrors.kernel.org/centos/'>&nbsp;FTP&nbsp;</a> </td><td align=center>
<a href='rsync://mirrors.kernel.org/centos/'>&nbsp;RSYNC&nbsp;</a> </td></tr>
<tr><td align=center valign=middle>Asia</td><td align=center valign=middle>Korea</td><td><a href='http://Linux.Tini4u.Net/'>LTN Community</a></td><td align=center>All</td><td>All</td><td align=center><b>Yes</b></td><td align=center><a href='http://mirror.tini4u.net/centos/'>&nbsp;HTTP&nbsp;</a> </td><td align=center>
<a href='ftp://mirror.tini4u.net/centos/'>&nbsp;FTP&nbsp;</a> </td><td align=center>
<a href='rsync://mirror.tini4u.net/centos/'>&nbsp;RSYNC&nbsp;</a> </td></tr>
<tr><td align=center valign=middle>Asia</td><td align=center valign=middle>Korea</td><td><a href='http://Mirr4u.Com/'>Mirr4u.Com</a></td><td align=center>All</td><td>All</td><td align=center><b>Yes</b></td><td align=center><a href='http://mirror.mirr4u.com/centos/'>&nbsp;HTTP&nbsp;</a> </td><td align=center>
</td><td align=center>
<a href='rsync://mirror.mirr4u.com/centos-mirror/'>&nbsp;RSYNC&nbsp;</a> </td></tr>
<tr><td align=center valign=middle>Asia</td><td align=center valign=middle>Korea</td><td><a href='http://www.secuidc.com/'>secuidc.com</a></td><td align=center>All</td><td>All</td><td align=center>no</td><td align=center><a href='http://mirror.secuidc.com/centos/'>&nbsp;HTTP&nbsp;</a> </td><td align=center>
<a href='ftp://mirror.secuidc.com/centos/'>&nbsp;FTP&nbsp;</a> </td><td align=center>
</td></tr>
<tr><td><small><small><small>&nbsp;</small></small></small></td></tr>
<tr><td align=center valign=middle>Asia</td><td align=center valign=middle>Taiwan</td><td><a href='http://www.ncnu.edu.tw/'>National Chi Nan University</a></td><td align=center>All</td><td>All</td><td align=center><b>Yes</b></td><td align=center><a href='http://ftp.ncnu.edu.tw/Linux/CentOS/'>&nbsp;HTTP&nbsp;</a> </td><td align=center>
<a href='ftp://ftp.ncnu.edu.tw/Linux/CentOS/'>&nbsp;FTP&nbsp;</a> </td><td align=center>
<a href='rsync://ftp.ncnu.edu.tw/centos-incdvd/'>&nbsp;RSYNC&nbsp;</a> </td></tr>
<tr><td align=center valign=middle>Asia</td><td align=center valign=middle>Taiwan</td><td><a href='http://www.tcc.edu.tw/'>TaiChung County Education Network Center</a></td><td align=center>All</td><td>All</td><td align=center><b>Yes</b></td><td align=center><a href='http://ftp.tcc.edu.tw/Linux/CentOS/'>&nbsp;HTTP&nbsp;</a> </td><td align=center>
<a href='ftp://ftp.tcc.edu.tw/Linux/Centos/'>&nbsp;FTP&nbsp;</a> </td><td align=center>
</td></tr>
<tr><td><small><small><small>&nbsp;</small></small></small></td></tr>
<tr><td align=center valign=middle>Asia</td><td align=center valign=middle>Taiwan</td><td><a href='http://www.tnc.edu.tw/'>TNC education network center</a></td><td align=center>All</td><td>All</td><td align=center>no</td><td align=center><a href='http://ftp2.tnc.edu.tw/pub1/centos/'>&nbsp;HTTP&nbsp;</a> </td><td align=center>
<a href='ftp://ftp2.tnc.edu.tw/pub1/centos/'>&nbsp;FTP&nbsp;</a> </td><td align=center>
</td></tr>
<tr><td align=center valign=middle>Asia</td><td align=center valign=middle>Taiwan</td><td><a href='http://www.cse.yzu.edu.tw/'>Yuan Ze University in Taiwan</a></td><td align=center>All</td><td>All</td><td align=center><b>Yes</b></td><td align=center><a href='http://ftp.cse.yzu.edu.tw/pub/CentOS/'>&nbsp;HTTP&nbsp;</a> </td><td align=center>
<a href='ftp://ftp.cse.yzu.edu.tw/pub/CentOS/'>&nbsp;FTP&nbsp;</a> </td><td align=center>
</td></tr>
<tr><td align=center valign=middle>EU</td><td align=center valign=middle>France</td><td><a href='http://www.pasteur.fr/'>Institut Pasteur</a></td><td align=center>All</td><td>All</td><td align=center>no</td><td align=center></td><td align=center>
<a href='ftp://ftp.pasteur.fr/pub/computing/linux/centos/'>&nbsp;FTP&nbsp;</a> </td><td align=center>
</td></tr>
<tr><td align=center valign=middle>EU</td><td align=center valign=middle>Germany</td><td><a href='http://www.financial.com/'>Financial.com</a></td><td align=center>All</td><td>All</td><td align=center>no</td><td align=center><a href='http://centos-mirror.financial.com/'>&nbsp;HTTP&nbsp;</a> </td><td align=center>
<a href='ftp://centos-mirror.financial.com/'>&nbsp;FTP&nbsp;</a> </td><td align=center>
</td></tr>
<tr><td><small><small><small>&nbsp;</small></small></small></td></tr>
<tr><td><small><small><small>&nbsp;</small></small></small></td></tr>
<tr><td align=center valign=middle>Asia</td><td align=center valign=middle>India</td><td><a href='http://www.iitm.ac.in'>Indian Institute of Technology, Madras</a></td><td align=center>All</td><td>i386 x86_64</td><td align=center>no</td><td align=center><a href='http://ftp.iitm.ac.in/centos/'>&nbsp;HTTP&nbsp;</a> </td><td align=center>
<a href='ftp://ftp.iitm.ac.in/centos/'>&nbsp;FTP&nbsp;</a> </td><td align=center>
<a href='rsync://ftp.iitm.ac.in/centos/'>&nbsp;RSYNC&nbsp;</a> </td></tr>
<tr><td><small><small><small>&nbsp;</small></small></small></td></tr>
<tr><td align=center valign=middle>Oceania</td><td align=center valign=middle>New Zealand</td><td><a href='http://wicks.co.nz/'>wicks.co.nz</a></td><td align=center>All</td><td>i386 x86_64 alpha</td><td align=center>no</td><td align=center></td><td align=center>
<a href='ftp://ftp.wicks.co.nz/pub/linux/dist/centos/'>&nbsp;FTP&nbsp;</a> </td><td align=center>
</td></tr>
<tr><td><small><small><small>&nbsp;</small></small></small></td></tr>
<tr><td align=center valign=middle>South America</td><td align=center valign=middle>Chile</td><td><a href='http://www.netglobalis.net/'>NetGlobalis</a></td><td align=center>3&nbsp;4&nbsp;</td><td>i386 x86_64 alpha</td><td align=center>no</td><td align=center><a href='http://mirror.netglobalis.net/pub/centos/'>&nbsp;HTTP&nbsp;</a> </td><td align=center>
<a href='ftp://mirror.netglobalis.net/pub/centos/'>&nbsp;FTP&nbsp;</a> </td><td align=center>
</td></tr>
<tr><td align=center valign=middle>South America</td><td align=center valign=middle>Puerto Rico</td><td><a href='http://www.hpcf.upr.edu/'>University of Puerto Rico - HPCF</a></td><td align=center>All</td><td>All</td><td align=center>no</td><td align=center><a href='http://mirrors.hpcf.upr.edu/ftp/pub/Mirrors/CentOS/'>&nbsp;HTTP&nbsp;</a> </td><td align=center>
<a href='ftp://mirrors.hpcf.upr.edu/pub/Mirrors/CentOS/'>&nbsp;FTP&nbsp;</a> </td><td align=center>
</td></tr>
<tr><td align=center valign=middle>South America</td><td align=center valign=middle>Venezuela</td><td><a href='http://www.uc.edu.ve/'>Universidad de Carabobo</a></td><td align=center>4&nbsp;5</td><td>i386</td><td align=center>no</td><td align=center></td><td align=center>
<a href='ftp://ftp.uc.edu.ve/linux/Centos/'>&nbsp;FTP&nbsp;</a> </td><td align=center>
</td></tr>
</table><br>
<table border=0 width=100%><tr><td align=left>130 of 169 mirrors are current (updated within the last 24 hours).  Out of date mirrors are NOT LISTED above.  Please visit <a href='http://mirror-status.centos.org'>mirror-status.centos.org</a> for details.</td></tr>
</table><br>
<table><tr><td>last update: Sat May 26 13:53:01 UTC 2008</td></tr></table>
<div style="padding: 5px; text-align: right; margin-right:3px;">
  <a href="print.php?id=13"><img src="images/print.gif" border="0" alt="Printer Friendly Page" /></a>
  <a href="mailto:?subject=Interesting Article at www.centos.org&amp;body=Here is an interesting article I have found at www.centos.org:  http://www.centos.org/modules/tinycontent/index.php?id=13" target="_top"><img src="images/friend.gif" border="0" alt="Send this Story to a Friend" /></a>
</div>
 </div> <br /> <br /> <br />
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>


    <center>
      <table width="90%" cellspacing="0">
        <tr>
          <td colspan="1" rowspan="1" style="vertical-align: middle; text-align: left;">
            <div id="wrap">
              <div id="menu">
                 <!-- donavan's standard test account = donavan1 -->
                  <a href="/sm_e.php">Site Map</a>
                  <a href="/modules/contact/">Contact Webmaster</a>
                              </div>
            </div>
          </td>
        </tr>
      </table>

<table width="90%"  border="0" cellpadding="2" cellspacing="2" class="dole">
  <tr>
    <td>
      <div class="privatnost">
        <br />
          "Linux" is a registered trademark of Linus Torvalds. | All other trademarks are property of their respective owners. | All other content is Copyright @ 2004-2005 by donavan nelson, lance davis, 4wx networks, definite software ltd, or "each individual contributor (forums, comments, wiki, etc.) unless otherwise assigned". | This Site hosted on dedicated server donated by <b><a href="http://www.ndchost.com/" target="_blank">NDC Host</a></b>.| Theme based on a theme by <a href="http://www.7dana.com" target="_blank">7dana.com</a>
        <br />
      </div>
    </td>
  </tr>
</table>
</center>
</body>
</html>
'''



sHtmlFillIn = \
'''
<html>
<head>
<title>PROXY--http://www.DHeart.Net--(PROXY,PROXY LIST)</title>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=gb2312">
<META NAME="Generator" CONTENT="PROXY,PROXY LIST,lphy,DHeart.Net">
<META NAME="Author" CONTENT="lphy,DHeart.Net">
<META NAME="Keywords" CONTENT="PROXY,PROXY LIST,lphy,DHeart.Net">
<META NAME="Description" CONTENT="PROXY,PROXY LIST,lphy,DHeart.Net">
<link rel="stylesheet" href="/tools/lphyallcss.php" type="text/css">
<STYLE type="text/css">
<!--
table,select,input {
    font-family: Verdana, Arial, Helvetica, sans-serif;
    font-size: 12px;
    color: #333333;
}
td {
    padding:3px 5px;
}
.title {
    font-size: 18px;
    font-weight: bolder;
    color: #3366FF;
    background-color: #FFFFFF;
    text-align: left;
}
.header {
    font-weight: bolder;
    background-color: ECF8FF;
    text-align: center;
    color: #000000;
    font-size: 12px;
}
.cells {
    text-align: center;
    background-color: #FFFFFF;
}
.cells2 {
    text-align: center;
    background-color: #f3f3f3;
}
a:link,a:visited,a:active {
    text-decoration: none;
    color: #666666;
}
a:hover {
    color: #00ccff;
}
.sp_link{ color: #006CFF; }
h1,h2 {font-size: 18px; color: #000000; font-family:; font-weight: blod}
-->
</STYLE>
<script language="JavaScript">
<!--
function lphywhois(ipaddr)
{
    if(ipaddr!=""){
    document.lphydowhois.ip.value=ipaddr;
    document.lphydowhois.submit();
    }
}
//-->
</script>
</head>

<BODY leftMargin=0 topMargin=10>
<center>
<h1></h1></center>
<center><div id="lphyheadtxt" name="lphyheadtxt"></div></center>
<br />
<br />
<center><div id="lphymaingg1" name="lphymaingg1"></div></center>
<br />
<table width="728" border="0" align="center" cellpadding="0" cellspacing="0">

<tr class="cells">
    <td colspan="6" align="right"><span class='sp_link'>[1]</span> <a href='index.php?lphydo=list&port=&type=&country=&page=2'>[2] </a><a href='index.php?lphydo=list&port=&type=&country=&page=3'>[3] </a>... <a href='index.php?lphydo=list&port=&type=&country=&page=8'>[34]>></a>&nbsp;&nbsp;</td>
  </tr>
</table>
<table width="728" align="center" border=0 cellspacing=1 cellpadding=5 bgcolor="B4D0DC">
  <tr class="header">
  <form method=post action="index.php">
    <td colspan="2">
    <input type="submit" value="" onclick="javascript:location='index.php';return false">
   </td>
    <td>
    <input type="hidden" name="lphydo" value="search">
    <select name="port">
    <option value="" selected>--</option>
        <option value="80" >80</option>
        <option value="3128" >3128</option>
        <option value="6588" >6588</option>
        <option value="7212" >7212</option>
        <option value="8000" >8000</option>
        <option value="8080" >8080</option>
        <option value="8888" >8888</option>
    </select></td>
    <td><select name="type">
    <option value="" selected>--option>
            <option value="anonymous" >anonymous</option>
        <option value="high anonymity" >high anonymity</option>
        <option value="transparent" >transparent</option>
    </select></td>
    <td><select name="country">
    <option value="" selected>--</option>
                <option value="Albania" >Albania</option>
        <option value="Zimbabwe" >Zimbabwe</option>
    </select></td>
    <td colspan="2"><input type="submit" value=""></td>
    </form>
  </tr>
  <tr class="header">
    <td>&nbsp;</td>
    <td>IP<br>    </td>
    <td><br>    </td>
    <td><br>    </td>
    <td>/<br>    </td>
    <td></td>
    <td>WHOIS</td>
  </tr>
                  <tr class="cells" id="tr1" onmouseover="this.className='cells2'" onmouseout="this.className='cells'">
    <td >1</td>
    <td>196.202.252.244</td>
    <td>80</td>
    <td>transparent</td>
    <td>Angola</td>
    <td>2008.09.22</td>
    <td><a href="javascript:void(lphywhois('196.202.252.244'));"><span class="sp_link">WHOIS</span></a></td>
  </tr>
                  <tr class="cells" id="tr2" onmouseover="this.className='cells2'" onmouseout="this.className='cells'">
    <td >2</td>
    <td>221.209.18.18</td>
    <td>8000</td>
    <td>transparent</td>
    <td>China</td>
    <td>2008.09.22</td>
    <td><a href="javascript:void(lphywhois('221.209.18.18'));"><span class="sp_link">WHOIS</span></a></td>
  </tr>
                  <tr class="cells" id="tr3" onmouseover="this.className='cells2'" onmouseout="this.className='cells'">
    <td >3</td>
    <td>77.71.0.230</td>
    <td>3128</td>
    <td>transparent</td>
    <td></td>
    <td>2008.09.22</td>
    <td><a href="javascript:void(lphywhois('77.71.0.230'));"><span class="sp_link">WHOIS</span></a></td>
  </tr>
                  <tr class="cells" id="tr60" onmouseover="this.className='cells2'" onmouseout="this.className='cells'">
    <td >60</td>
    <td>217.11.27.61</td>
    <td>8080</td>
    <td>transparent</td>
    <td>Iran</td>
    <td>2008.09.22</td>
    <td><a href="javascript:void(lphywhois('217.11.27.61'));"><span class="sp_link">WHOIS</span></a></td>
  </tr>
  </table>
  <table width="728" border="0" align="center" cellpadding="0" cellspacing="0">
  <tr class="cells">
    <td align="left"><span class='sp_link'>[1]</span> <a href='index.php?lphydo=list&port=&type=&country=&page=2'>[2] </a><a href='index.php?lphydo=list&port=&type=&country=&page=3'>[3] </a>... <a href='index.php?lphydo=list&port=&type=&country=&page=34'>[8]>></a>&nbsp;&nbsp;</td>
  </tr>

</table>
<form method=post name="lphydowhois" target="_blank" action="index.php">
<input type="hidden" name="lphydo" value="whois">
<input type="hidden" name="ip" value="">
</form>
<iframe border=0 vspace=0 hspace=0 name=searchvip marginwidth=0 marginheight=0 framespacing=0 frameborder=0 scrolling=no height=0 width=0 src="lphypro.php"></iframe>
<br><br>
<P align=center>
<center><div id="google_adsense"><iframe name="Google" width="468" height="60" src="/tools/google.php?width=468&height=60&channel=0288824392" scrolling="no" frameborder="0"></iframe></div>
</center>
<br>
<center><div id="lphymaingg2" name="lphymaingg2"></div></center><br/>
<p align=center><small>Copyright 1999-2004 <a href="http://www.dheart.net" title="" target="_blank">DHeartNet</a> Allrights Reserved<br>(c)&nbsp;&nbsp;1999-2004&nbsp;&nbsp;E-mail:DHeart@163.com</small></p>
<script language="JavaScript" type="text/javascript" src="/tools/maingg.js"></script>
<script language="JavaScript" type="text/javascript" src="/tools/othergg.js"></script>
<script language="JavaScript" type="text/javascript" src="/tools/headtxt.js"></script>
<div class="lphyhidc"><script src="http://www3.itsun.com/counter.php?uuid=1511422&style=text"></script><script src=http://vip4.1tong.com.cn/link/count.php?id=238></script><script language="JavaScript" type="text/javascript" src="http://w.50bang.com/click.js?user_id=131479"></script></div>
</body>
</html>
'''

sGoogleQuerResult_Konq = \
'''<!doctype html><html itemscope itemtype="http://schema.org/WebPage"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><meta itemprop="image" content="/images/google_favicon_128.png"><title>allintext: -error REMOTE_ADDR REQUEST_METHOD googlebot(at)googlebot.com HTTP_USER_AGENT HTTP_CONNECTION HTTP_HOST HTTP_REFERER HTTP_ACCEPT - Google Search</title><style>#gbar,#guser{font-size:13px;padding-top:1px !important;}#gbar{height:22px}#guser{padding-bottom:7px !important;text-align:right}.gbh,.gbd{border-top:1px solid #c9d7f1;font-size:1px}.gbh{height:0;position:absolute;top:24px;width:100%}@media all{.gb1{height:22px;margin-right:.5em;vertical-align:top}#gbar{float:left}}a.gb1,a.gb4{text-decoration:underline !important}a.gb1,a.gb4{color:#00c !important}</style><style>
    body,td,div,.p,a{
      font-family:arial,sans-serif
    }
    body {
      margin:0
    }
    #gbar{
      float:left;
      height:22px;padding-left:2px;
      font-size:13px
    }
    
    .gssb_c table{
      font-size:1em
    }
    .gsfi,.gsfs{
      font-size:17px
    }
    
      .j{
        width:34em
      }
    
    a:link,.w,.q:active,.q:visited,.tbotu{
      color:#11c
    }
    a.fl,.flc a{
      color:#4272db;text-decoration:none
    }
    
    a.gl{
      text-decoration:none
    }
    cite, cite a:link{
      color:#0E774A;
      font-style:normal
    }
    #foot {
      padding:0 8px;
    }
    #foot a{
      white-space:nowrap
    }
    h3{
      font-size:16px;
      font-weight:normal;
      margin:0;
      padding:0
    }
    #res h3{
      display:inline
    }
    .hd{
      height:1px;
      position:absolute;
      top:-1000em
    }
    li.g,body,html,table,.std{
      font-size:13px
    }
    li.g{
      margin-bottom:14px;
      margin-top:0;
      zoom:1;
    }
    ol li,ul li{
      list-style:none
    }
    h1,ol,ul,li{
      margin:0;padding:0
    }
    #mbEnd li{
      margin:1em 0
    }
    #mbEnd h2{
      color:#676767;
      font-family:arial,sans-serif;
      font-size:11px;
      font-weight:normal
    }
    #center_col{
      border-left:1px solid #d3e1f9;
      padding:0 8px
    }
    
      #fll a,#bfl a{
        margin:0 10px
      }
    
    .f{
      color:#767676
    }
    .grn{
      color:#393
    }
    .ds{
      border-right:1px solid #e7e7e7;
      position:relative;
      height:32px;
      
      z-index:100
    }
    .e{
      margin:2px 0px 0.75em
    }
    #leftnav a,.slk a{
      text-decoration:none
    }
    #leftnav h2{
      color: #767676;
      font-weight: normal;
      margin:0
    }
    #logo{
      display:block;
      height:49px;
      margin-top:12px;
      margin-left:12px;
      overflow:hidden;
      position:relative;
      width:137px
    }
    #logo img{
      
      left:0;
      position:absolute;
      top:-41px
    }
    .lnsec{
      font-size:13px;
      border-top:1px solid #c9d7f1;
      margin-top:5px;
      padding-top:8px
    }
    .lsb,.micon,.csb,.star,.star div{
      background:url(/images/nav_logo_hp2.png) no-repeat;
      overflow:hidden
    }
    .lst{
      background:#fff;
      border:1px solid #ccc;
      border-bottom:none;
      color:#000;
      font:18px arial,sans-serif;
      
      float:left;
      height:26px;
      margin:0;
      padding:4px 0 0;
      padding-left:6px;
      padding-right:10px;
      vertical-align:top;
      width:100%;
      
      word-break:break-all
    }
    .lst:focus{
      outline:none
    }
    .lst-td{
      border-bottom:1px solid #999;
      padding:0
    }
    .lst-b{
      border:1px solid #CCC;
      border-bottom:none;
      padding-right:0;
      height:29px;
      padding-top:1px
    }
    .tia input{
      border-right:none;
      padding-right:0
    }
    .tia{
      padding-right:0
    }
    .lsbb{
      background:#eee;
      border:1px solid #999;
      border-top-color:#ccc;
      border-left-color:#ccc;
      height:30px
    }
    .lsb{
      background-position:bottom;
      border:none;
      color:#000;
      cursor:pointer;
      font:15px arial,sans-serif;
      height:30px;
      margin:0;
      vertical-align:top
    }
    .lsb:active{
      background:#ccc
    }
    .micon {
      float:left;
      height:19px;
      margin-top:2px;
      margin-right: 6px;
      width:19px;
    }
    #nav{
      
      border-collapse:collapse;
      margin-top:17px;
      text-align:left
    }
    #nav td{
      text-align:center;
    }
    .nobr{
      white-space:nowrap
    }
    #showmodes .micon{
      background-position:-150px -114px;
      height:17px;
      margin-left:9px;
      width:17px;
    }
    #subform_ctrl{
      font-size:11px;
      height:26px;
      margin:5px 3px 0;
      margin-left:17px
    }
    .ts{
      border-collapse:collapse
    }
    #mn{
      table-layout:fixed;width:996px
    }
    .mitem{
      font-size:15px;
      line-height:24px;
      margin-bottom:2px;
      padding-left:0
    }
    .msel{
      font-weight:bold;
      margin:-1px 0 0 0;
      border:solid #fff;
      border-width:1px 0
    }
    .r{
      margin:0
    }
    #res{
      padding:4px 8px 0
    }
    .s br{
      display:none
    }
    .spon{
      font-size:11px;
      font-weight:normal;
      color:#767676
    }
    .mitem,.lnsec{
      padding-left:8px
    }
    #showmodes{
      font-size:15px;
      line-height:24px;
    }
    #swr{
      margin-top:4px
    }
    #swr li{
      line-height:1.2;
      margin-bottom:4px
    }
    .csb{
      display:block;
      height:40px;
    }
    .images_table td{line-height:17px;padding-bottom:16px}
    .images_table img{border:1px solid #ccc;padding:1px}
    .taf{
      padding:1px 0 0
    }
    .tam{
      padding:14px 0 0
    }
    .tal{
      padding:14px 0 1px
    }
    #tbd,#abd{
      display:block;
      min-height:1px;
      padding-top:3px
    }
    #tbd li{
      
      display:inline
    }
    .tbfo,.tbt,.tbpd{
      margin-bottom:8px
    }
    #tbd .tbt li{
      display:block;
      font-size:13px;
      line-height:1.2;
      padding-bottom:3px;
      padding-left:8px;
      text-indent:-8px
    }
    .tbos,.b{
      font-weight:bold;
    }
    a:hover{
      text-decoration:underline
    }
    #leftnav a:hover {
      text-decoration:underline;
    }
    em{
      font-weight:bold;
      font-style:normal
    }
    
    .gac_wd{
      right:-2px !important;
      
      overflow:hidden
    }
    
    .fmg{
      display:inline-block;
      margin-top:7px;
      padding-right:8px;
      text-align-left;
      vertical-align:top;
      width:90px;
      zoom:1
    }
    .star{
      
          background-position:0 -120px;
        
      height:9px;
      overflow-hidden;
      width:50px
    }
    .star div{
      
          background-position:0 -110px
        
    }
    
    .pslires{
      padding-top:6px;
      overflow:hidden;
      width:99.5%
    }
    .psliimg{
      float:left;
      height:90px;
      text-align:top;
      width:90px
    }
    .pslimain{
      margin-left:100px;
      margin-right:9em
    }
    .psliprice{
      float:right;
      width:7em
    }
    .psliprice b{
      font-size:medium;
      font-weight:bold;
      white-space:nowrap
    }
    .psliimg img{
      border:none
    }
    </style><script type="text/javascript">
      window.google = { y: {} };
      </script><script type="text/javascript"></script></head>
    <body bgcolor="#ffffff" topmargin="3" marginheight="3" marginwidth="0"
  ><div id=gbar><nobr><b class=gb1>Search</b> <a class=gb1 href="http://www.google.com/search?hl=en&q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&gbv=1&um=1&ie=UTF-8&tbm=isch&source=og&sa=N&tab=wi">Images</a> <a class=gb1 href="http://www.google.com/search?hl=en&q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&gbv=1&um=1&ie=UTF-8&tbo=u&tbm=vid&source=og&sa=N&tab=wv">Videos</a> <a class=gb1 href="http://maps.google.com/maps?hl=en&q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&gbv=1&um=1&ie=UTF-8&sa=N&tab=wl">Maps</a> <a class=gb1 href="http://news.google.com/nwshp?hl=en&tab=wn">News</a> <a class=gb1 href="http://www.google.com/search?hl=en&q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&gbv=1&um=1&ie=UTF-8&tbo=u&tbm=shop&source=og&sa=N&tab=wf">Shopping</a> <a class=gb1 href="https://mail.google.com/mail/?tab=wm">Gmail</a> <a class=gb1 style="text-decoration:none" href="http://www.google.com/intl/en/options/"><u>More</u> &raquo;</a></nobr></div><div id=guser width=100%><nobr><span id=gbn class=gbi></span><span id=gbf class=gbf></span><span id=gbe><a  href="/history/optout?hl=en" class=gb4>Web History</a> | </span><a  href="/preferences?hl=en" class=gb4>Settings</a> | <a id=gb_70 href="https://accounts.google.com/ServiceLogin?hl=en&continue=http://www.google.com/search%3Fhl%3Den%26source%3Dhp%26q%3Dallintext:%2B-error%2BREMOTE_ADDR%2BREQUEST_METHOD%2Bgooglebot(at)googlebot.com%2BHTTP_USER_AGENT%2BHTTP_CONNECTION%2BHTTP_HOST%2BHTTP_REFERER%2BHTTP_ACCEPT%26gbv%3D1%26oq%3Dallintext:%2B-error%2BREMOTE_ADDR%2BREQUEST_METHOD%2Bgooglebot(at)googlebot.com%2BHTTP_USER_AGENT%2BHTTP_CONNECTION%2BHTTP_HOST%2BHTTP_REFERER%2BHTTP_ACCEPT%26aq%3Df%26aqi%3D%26gs_l%3Dhp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld." class=gb4>Sign in</a></nobr></div><div class=gbh style=left:0></div><div class=gbh style=right:0></div><br clear="all"><table border="0" cellpadding="0" cellspacing="0" id="mn" style="position:relative"><tr><td rowspan="2" valign="top" width="157"><h1><a href="/webhp?hl=en" id="logo" title="Go to Google Home"><img src="/images/nav_logo_hp2.png" alt="" height="222" style="border:0" width="167"></a></h1></td><td valign="top" style="padding-left:9px" width="559"><form name="gs" id="tsf" method="GET" action="/search" style="display:block;margin:0;background:none"><table border="0" cellpadding="0" cellspacing="0" id="sbhost" style="border-bottom:1px solid #e7e7e7;margin-top:18px;position:relative"><tr><td class="lst-td" width="100%" valign="bottom" style=""><div style="position:relative;zoom:1"><input autocomplete="off" class="lst" type="text" name="q" maxlength="2048" title="Search" value="allintext: -error REMOTE_ADDR REQUEST_METHOD googlebot(at)googlebot.com HTTP_USER_AGENT HTTP_CONNECTION HTTP_HOST HTTP_REFERER HTTP_ACCEPT"></div></td><td><div class="ds"><div class="lsbb"><input type="submit" name="btnG" class="lsb" value="Search"></div></div></td></tr></table><input type="hidden" name="hl" value="en"><input type="hidden" name="gbv" value="1"><input type="hidden" name="gs_l" value="hp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld."></form></td><td style="padding-left:5px" width="259"></td></tr><tr><td width="100%"><div id="subform_ctrl"><div style="float:right"><a class="fl" href="/advanced_search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=1&amp;prmd=ivns">Advanced search</a></div><div>About 2,380,000 results</div></div></td><td></td></tr><tr><td valign="top" id="leftnav" style="padding:4px"><div id="modeselector" style="padding-bottom:4px"><ul><li class="mitem msel"><span class="micon" style="
          background-position:-20px -132px
        "></span>Everything</li><li class="mitem"><a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=1&amp;prmd=ivns&amp;source=lnms&amp;tbm=isch&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;sa=X&amp;oi=mode_link&amp;ct=mode&amp;cd=2&amp;ved=0CAcQ_AUoAQ" class="q"><span class="micon" style="
          background-position:-40px -132px
        "></span>Images</a></li><li class="mitem"><a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=1&amp;prmd=ivns&amp;source=lnms&amp;tbm=vid&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;sa=X&amp;oi=mode_link&amp;ct=mode&amp;cd=3&amp;ved=0CAgQ_AUoAg" class="q"><span class="micon" style="
          background-position:-80px -132px
        "></span>Videos</a></li><li class="mitem"><a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=1&amp;prmd=ivns&amp;source=lnms&amp;tbm=nws&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;sa=X&amp;oi=mode_link&amp;ct=mode&amp;cd=4&amp;ved=0CAkQ_AUoAw" class="q"><span class="micon" style="
          background-position:-120px -132px
        "></span>News</a></li><li class="mitem"><a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=1&amp;prmd=ivns&amp;source=lnms&amp;tbm=shop&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;sa=X&amp;oi=mode_link&amp;ct=mode&amp;cd=5&amp;ved=0CAoQ_AUoBA" class="q"><span class="micon" style="
          background-position:-120px -152px
        "></span>Shopping</a></li></ul><a id="showmodes" class="q" href="/search?hl=en&amp;q=allintext%3A+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;gbv=1&amp;gs_l=hp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld.&amp;prmdo=1&amp;sa=X"><span class="micon"></span><span class="msm">More</span></a></div><div class="lnsec"><h2 class="hd">Search Options</h2><ul id="tbd" class="med"><li><ul class="tbt"></ul></li><li><ul class="tbt"></ul></li></ul><a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=1&amp;prmd=ivns&amp;tbo=1" class="q" style="display:block;margin-bottom:16px">Show search tools</a></div></td><td valign="top"><div id="center_col"><div id="res"><div id="ires"><ol><li class="g"><h3 class="r"><a href="/url?q=http://www.cem.brighton.ac.uk/cgi-bin/mas/mas_rec.exe%3Fpage%3Dmas%26file%3Dw://cgi-bin//mas//00mas_logs&amp;sa=U&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;ved=0CBEQFjAA&amp;usg=AFQjCNHG52G42OOnJ__djJN1nXMGVzp2bg">AUTH_TYPE CONTENT_LENGTH 0 CONTENT_TYPE <b>...</b></a></h3><div class="s"><b>...</b> <b>HTTP_ACCEPT</b> */* <b>HTTP_CONNECTION</b> Keep-alive <b>HTTP_HOST</b> <b>...</b> <br>  <b>HTTP_USER_AGENT</b> Mozilla/5.0 (compatible; <b>Googlebot</b>/2.1; <b>...</b> page=mas&amp;file=<br>  w://cgi-bin//mas//00mas_logs <b>REMOTE_ADDR</b> <b>...</b> 66.249.72.164 <br>  REMOTE_IDENT [] REMOTE_USER <b>REQUEST_METHOD</b> <b>...</b> HTTP_FROM=<br>  <b>googlebot</b>(<b>at</b>)<b>googlebot.com</b> <b>...</b><br><div><cite>www.cem.brighton.ac.uk/cgi-bin/mas/mas_rec.exe?page...</cite><span class="flc"> - <a href="//webcache.googleusercontent.com/search?hl=en&amp;gbv=1&amp;gs_l=hp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld.&amp;q=cache:0pKwA4jSH-0J:http://www.cem.brighton.ac.uk/cgi-bin/mas/mas_rec.exe?page=mas&amp;file=w://cgi-bin//mas//00mas_logs+allintext%3A+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;ct=clnk">Cached</a> - <a href="/search?hl=en&amp;gbv=1&amp;gs_l=hp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld.&amp;tbo=1&amp;q=related:http://www.cem.brighton.ac.uk/cgi-bin/mas/mas_rec.exe?page=mas&amp;file=w://cgi-bin//mas//00mas_logs+allintext%3A+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;sa=X">Similar</a></span></div></div></li><li class="g"><h3 class="r"><a href="/url?q=http://www.informatik.uni-ulm.de/sgi/cgi-bin/bsp/test.py&amp;sa=U&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;ved=0CBMQFjAB&amp;usg=AFQjCNFNan20Z01Cw5XtEsJ6VxDHRSaOCg">Second try with a small maxlen...</a></h3><div class="s"><b>HTTP_ACCEPT</b>; <b>HTTP_CONNECTION</b>; <b>HTTP_HOST</b>; HTTP_PRAGMA; <br>  <b>HTTP_REFERER</b>; <b>HTTP_USER_AGENT</b> <b>...</b> <b>googlebot</b>(<b>at</b>)<b>googlebot.com</b>; <br>  <b>HTTP_HOST</b>: www.informatik.uni-ulm.de; HTTP_IF_MODIFIED_SINCE <b>...</b> /usr/<br>  local/bin:/usr/bin:/bin; QUERY_STRING: <b>REMOTE_ADDR</b>: 66.249.66.57; <br>  REMOTE_PORT: 63944 <b>...</b><br><div><cite>www.informatik.uni-ulm.de/sgi/cgi-bin/bsp/test.py</cite><span class="flc"> - <a href="//webcache.googleusercontent.com/search?hl=en&amp;gbv=1&amp;gs_l=hp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld.&amp;q=cache:YRBomXMAucQJ:http://www.informatik.uni-ulm.de/sgi/cgi-bin/bsp/test.py+allintext%3A+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;ct=clnk">Cached</a> - <a href="/search?hl=en&amp;gbv=1&amp;gs_l=hp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld.&amp;tbo=1&amp;q=related:http://www.informatik.uni-ulm.de/sgi/cgi-bin/bsp/test.py+allintext%3A+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;sa=X">Similar</a></span></div></div></li><li class="g"><h3 class="r"><a href="/url?q=http://www.acc.umu.se/~guru/debug.cgi&amp;sa=U&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;ved=0CBUQFjAC&amp;usg=AFQjCNG8sX9VN1ixR6CLhCm5Ia4pPMoSqw">Second try with a small maxlen...</a></h3><div class="s">DOCUMENT_ROOT: /import/www/public_html; GATEWAY_INTERFACE: CGI/1.1; <br>  <b>HTTP_ACCEPT</b>: */ <b>...</b> HTTP_FROM: <b>googlebot</b>(<b>at</b>)<b>googlebot.com</b>; <b>HTTP_HOST</b>: <br>  www.acc.umu.se <b>...</b> <b>HTTP_USER_AGENT</b>: Mozilla/5.0 (compatible; <b>Googlebot</b>/<br>  2.1; <b>...</b> QUERY_STRING: <b>REMOTE_ADDR</b>: 66.249.72.136; REMOTE_HOST <b>...</b><br><div><cite>www.acc.umu.se/~guru/debug.cgi</cite><span class="flc"> - <a href="/search?hl=en&amp;gbv=1&amp;gs_l=hp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld.&amp;tbo=1&amp;q=related:http://www.acc.umu.se/~guru/debug.cgi+allintext%3A+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;sa=X">Similar</a></span></div></div></li><li class="g"><h3 class="r"><a href="/url?q=http://www.adres54.ru/adres54new/localProject/var/log/errorHandler.log&amp;sa=U&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;ved=0CBcQFjAD&amp;usg=AFQjCNEAuIOc9YAcfWyGIrZ5djuYoo1_-g">STARTED <b>AT</b>: 2011-04-21 13:08:13 (+0700) EXECUTION TIME <b>...</b></a></h3><div class="s">11 Oct 2011 <b>...</b> STARTED <b>AT</b>: 2011-04-21 13:08:13 (+0700) EXECUTION TIME: <br>  0.72622299194336 PHP_SELF: <b>...</b> &quot;<b>HTTP_CONNECTION</b>&quot;=&gt;&quot;Keep-alive&quot;, &quot;<br>  <b>HTTP_ACCEPT</b>&quot;=&gt;&quot;*/*&quot;, &quot;HTTP_FROM&quot;=&gt;&quot;<b>googlebot</b>(<b>at</b>)<b>googlebot.com</b>&quot;, &quot;<br>  <b>HTTP_USER_AGENT</b>&quot;=&gt;&quot;Mozilla/5.0 (compatible; <b>Googlebot</b>/2.1; <b>...</b><br><div><cite>www.adres54.ru/adres54new/localProject/var/log/errorHandler.log</cite><span class="flc"> - <a href="//webcache.googleusercontent.com/search?hl=en&amp;gbv=1&amp;gs_l=hp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld.&amp;q=cache:iI_NgVfJjPkJ:http://www.adres54.ru/adres54new/localProject/var/log/errorHandler.log+allintext%3A+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;ct=clnk">Cached</a> - <a href="/search?hl=en&amp;gbv=1&amp;gs_l=hp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld.&amp;tbo=1&amp;q=related:http://www.adres54.ru/adres54new/localProject/var/log/errorHandler.log+allintext%3A+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;sa=X">Similar</a></span></div></div></li><li class="g"><h3 class="r"><a href="/url?q=http://www.dikomm.ru/cgi-bin/python.py&amp;sa=U&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;ved=0CBkQFjAE&amp;usg=AFQjCNEwEMhQwPHl6S86U2xhOMzMrwWrlw">Second try with a small maxlen... - Dikomm.ru</a></h3><div class="s"><b>HTTP_ACCEPT</b>; <b>HTTP_CONNECTION</b>; <b>HTTP_HOST</b>; HTTP_PRAGMA; <br>  <b>HTTP_REFERER</b>; <b>HTTP_USER_AGENT</b> <b>...</b> <b>HTTP_CONNECTION</b>: close; <br>  HTTP_FROM: <b>googlebot</b>(<b>at</b>)<b>googlebot.com</b>; <b>HTTP_HOST</b>: www.dikomm. <b>...</b> /usr/<br>  local/bin:/usr/bin:/bin; QUERY_STRING: <b>REMOTE_ADDR</b>: 66.249.72.20; <br>  REMOTE_PORT: 33067 <b>...</b><br><div><cite>www.dikomm.ru/cgi-bin/python.py</cite><span class="flc"> - <a href="//webcache.googleusercontent.com/search?hl=en&amp;gbv=1&amp;gs_l=hp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld.&amp;q=cache:BtPZAGP52QMJ:http://www.dikomm.ru/cgi-bin/python.py+allintext%3A+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;ct=clnk">Cached</a> - <a href="/search?hl=en&amp;gbv=1&amp;gs_l=hp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld.&amp;tbo=1&amp;q=related:http://www.dikomm.ru/cgi-bin/python.py+allintext%3A+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;sa=X">Similar</a></span></div></div></li><li class="g"><h3 class="r"><a href="/url?q=http://jigl.com/hattrick.txt&amp;sa=U&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;ved=0CBsQFjAF&amp;usg=AFQjCNHM-C4DyQOejvih1TUgDn8UtocT1Q">Array ( [DOCUMENT_ROOT] =&gt; /home/jigl/public_html <b>...</b></a></h3><div class="s"><b>...</b> CGI/1.1 [<b>HTTP_ACCEPT</b>] =&gt; text/html,application/xhtml+xml,application/xml;q=<br>  0.9,*/* <b>...</b> max-age=259200 [<b>HTTP_CONNECTION</b>] =&gt; keep-alive [<b>HTTP_HOST</b>] =<br>  &gt; www.jigl.com [<b>HTTP_REFERER</b>] =&gt; http://www.jigl.com/ [<b>HTTP_USER_AGENT</b>] <br>  <b>....</b> Keep-alive [HTTP_FROM] =&gt; <b>googlebot</b>(<b>at</b>)<b>googlebot.com</b> [<b>HTTP_HOST</b>] <b>...</b><br><div><cite>jigl.com/hattrick.txt</cite><span class="flc"> - <a href="//webcache.googleusercontent.com/search?hl=en&amp;gbv=1&amp;gs_l=hp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld.&amp;q=cache:dyQLcI5__HEJ:http://jigl.com/hattrick.txt+allintext%3A+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;ct=clnk">Cached</a> - <a href="/search?hl=en&amp;gbv=1&amp;gs_l=hp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld.&amp;tbo=1&amp;q=related:http://jigl.com/hattrick.txt+allintext%3A+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;sa=X">Similar</a></span></div></div></li><li class="g"><h3 class="r"><a href="/url?q=http://www.ug.it.usyd.edu.au/~hwil7821/test.cgi&amp;sa=U&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;ved=0CB0QFjAG&amp;usg=AFQjCNFwH-dP0KM7WqQQjggOa7wBo1vIqw">Second try with a small maxlen... - Current UG</a></h3><div class="s"><b>...</b> <b>googlebot</b>(<b>at</b>)<b>googlebot.com</b>; <b>HTTP_HOST</b>: www.ug.it.usyd.edu.au <b>...</b> <br>  <b>HTTP_USER_AGENT</b>: Mozilla/5.0 (compatible; <b>Googlebot</b>/2.1; <b>...</b> <br>  QUERY_STRING: <b>REMOTE_ADDR</b>: 66.249.68.201; REMOTE_PORT <b>...</b> <br>  <b>HTTP_ACCEPT</b>; <b>HTTP_CONNECTION</b>; <b>HTTP_HOST</b>; HTTP_PRAGMA; <br>  <b>HTTP_REFERER</b>; <b>HTTP_USER_AGENT</b> <b>...</b><br><div><cite>www.ug.it.usyd.edu.au/~hwil7821/test.cgi</cite><span class="flc"> - <a href="//webcache.googleusercontent.com/search?hl=en&amp;gbv=1&amp;gs_l=hp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld.&amp;q=cache:OCnpvnmPlecJ:http://www.ug.it.usyd.edu.au/~hwil7821/test.cgi+allintext%3A+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;ct=clnk">Cached</a> - <a href="/search?hl=en&amp;gbv=1&amp;gs_l=hp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld.&amp;tbo=1&amp;q=related:http://www.ug.it.usyd.edu.au/~hwil7821/test.cgi+allintext%3A+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;sa=X">Similar</a></span></div></div></li><li class="g"><h3 class="r"><a href="/url?q=http://www.mischiefbox.com/demo/test.py&amp;sa=U&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;ved=0CB8QFjAH&amp;usg=AFQjCNHzxhQNUF0M_b_AZ1s9SW5-6AIJyg">Test output</a></h3><div class="s"><b>...</b> &#39;<b>REQUEST_METHOD</b>&#39;: &#39;GET&#39;, &#39;HTTP_FROM&#39;: &#39;<b>googlebot</b>(<b>at</b>)<b>googlebot.com</b>&#39;, &#39;<br>  SERVER_PROTOCOL&#39;: <b>...</b> &#39;<b>HTTP_USER_AGENT</b>&#39;: &#39;Mozilla/5.0 (compatible; <br>  <b>Googlebot</b>/2.1; <b>...</b> &#39;Keep-alive&#39;, &#39;SERVER_NAME&#39;: &#39;www.mischiefbox.com&#39;, &#39;<br>  <b>REMOTE_ADDR</b>&#39;: <b>...</b> <b>HTTP_ACCEPT</b>; <b>HTTP_CONNECTION</b>; <b>HTTP_HOST</b>; <br>  HTTP_PRAGMA <b>...</b><br><div><cite>www.mischiefbox.com/demo/test.py</cite><span class="flc"> - <a href="//webcache.googleusercontent.com/search?hl=en&amp;gbv=1&amp;gs_l=hp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld.&amp;q=cache:WHAMuH2N0WcJ:http://www.mischiefbox.com/demo/test.py+allintext%3A+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;ct=clnk">Cached</a> - <a href="/search?hl=en&amp;gbv=1&amp;gs_l=hp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld.&amp;tbo=1&amp;q=related:http://www.mischiefbox.com/demo/test.py+allintext%3A+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;sa=X">Similar</a></span></div></div></li><li class="g"><h3 class="r"><a href="/url?q=http://www.nacs.uci.edu/indiv/franklin/cgi-bin/values.cgi&amp;sa=U&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;ved=0CCEQFjAI&amp;usg=AFQjCNHo3HRI0vLSLUrx1XwSFEWs3DwttQ">CGI Values</a></h3><div class="s"><b>...</b> <b>HTTP_ACCEPT</b> = */* <b>HTTP_CONNECTION</b> = Keep-alive <b>HTTP_HOST</b> = <br>  dcssrv1.oit.uci.edu HTTP_PRAGMA = <b>HTTP_REFERER</b> = <b>HTTP_USER_AGENT</b> <br>  = Mozilla/5.0 (compatible; <b>Googlebot</b>/2.1; <b>...</b> REMOTE_USER = <br>  <b>REQUEST_METHOD</b> = GET SCRIPT_FILENAME <b>...</b> HTTP_FROM=&#39;<b>googlebot</b>(<b>at</b>)<br>  <b>googlebot.com</b>&#39; <b>...</b><br><div><cite>www.nacs.uci.edu/indiv/franklin/cgi-bin/values.cgi</cite><span class="flc"> - <a href="//webcache.googleusercontent.com/search?hl=en&amp;gbv=1&amp;gs_l=hp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld.&amp;q=cache:A4QOTqQX4dkJ:http://www.nacs.uci.edu/indiv/franklin/cgi-bin/values.cgi+allintext%3A+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;ct=clnk">Cached</a> - <a href="/search?hl=en&amp;gbv=1&amp;gs_l=hp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld.&amp;tbo=1&amp;q=related:http://www.nacs.uci.edu/indiv/franklin/cgi-bin/values.cgi+allintext%3A+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;sa=X">Similar</a></span></div></div></li><li class="g"><h3 class="r"><a href="/url?q=http://www.iro.umontreal.ca/~lapalme/ift3225/Dynamique/test_py.cgi&amp;sa=U&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;ved=0CCMQFjAJ&amp;usg=AFQjCNEMLBVEud612dEcZBOAHpNcWObqKg">echo Python</a></h3><div class="s">DOCUMENT_ROOT: /part/02/www/htdocs; GATEWAY_INTERFACE: CGI/1.1; <br>  <b>HTTP_ACCEPT</b>: */ <b>...</b> <b>googlebot</b>(<b>at</b>)<b>googlebot.com</b>; <b>HTTP_HOST</b>: wwwx.iro.<br>  umontreal.ca <b>...</b> QUERY_STRING: <b>REMOTE_ADDR</b>: 132.204.24.179; <br>  REMOTE_PORT: 43359 <b>...</b> <b>HTTP_HOST</b>; HTTP_PRAGMA; <b>HTTP_REFERER</b>; <br>  <b>HTTP_USER_AGENT</b> <b>...</b><br><div><cite>www.iro.umontreal.ca/~lapalme/ift3225/Dynamique/test_py.cgi</cite><span class="flc"> - <a href="//webcache.googleusercontent.com/search?hl=en&amp;gbv=1&amp;gs_l=hp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld.&amp;q=cache:J3tvgTWxVoAJ:http://www.iro.umontreal.ca/~lapalme/ift3225/Dynamique/test_py.cgi+allintext%3A+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;ct=clnk">Cached</a> - <a href="/search?hl=en&amp;gbv=1&amp;gs_l=hp.12...2956l2956l0l5545l1l1l0l0l0l0l0l0ll0l0.frgbld.&amp;tbo=1&amp;q=related:http://www.iro.umontreal.ca/~lapalme/ift3225/Dynamique/test_py.cgi+allintext%3A+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;sa=X">Similar</a></span></div></div></li></ol></div></div></div><div id="foot"><table align="center" border="0" cellpadding="0" cellspacing="0" id="nav"><tr valign="top"><td class="b" align="left"><span class="csb ch" style="background-position:-24px 0;width:28px"></span><b></b></td><td><span class="csb ch" style="background-position:-53px 0;width:20px"></span><b>1</b></td><td><a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=1&amp;prmd=ivns&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;start=10&amp;sa=N" class="fl"><span class="csb ch" style="background-position:-74px 0;width:20px"></span>2</a></td><td><a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=1&amp;prmd=ivns&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;start=20&amp;sa=N" class="fl"><span class="csb ch" style="background-position:-74px 0;width:20px"></span>3</a></td><td><a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=1&amp;prmd=ivns&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;start=30&amp;sa=N" class="fl"><span class="csb ch" style="background-position:-74px 0;width:20px"></span>4</a></td><td><a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=1&amp;prmd=ivns&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;start=40&amp;sa=N" class="fl"><span class="csb ch" style="background-position:-74px 0;width:20px"></span>5</a></td><td><a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=1&amp;prmd=ivns&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;start=50&amp;sa=N" class="fl"><span class="csb ch" style="background-position:-74px 0;width:20px"></span>6</a></td><td><a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=1&amp;prmd=ivns&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;start=60&amp;sa=N" class="fl"><span class="csb ch" style="background-position:-74px 0;width:20px"></span>7</a></td><td><a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=1&amp;prmd=ivns&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;start=70&amp;sa=N" class="fl"><span class="csb ch" style="background-position:-74px 0;width:20px"></span>8</a></td><td><a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=1&amp;prmd=ivns&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;start=80&amp;sa=N" class="fl"><span class="csb ch" style="background-position:-74px 0;width:20px"></span>9</a></td><td><a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=1&amp;prmd=ivns&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;start=90&amp;sa=N" class="fl"><span class="csb ch" style="background-position:-74px 0;width:20px"></span>10</a></td><td class="b" style="text-align:left"><a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=1&amp;prmd=ivns&amp;ei=goNxT-WHAaeViAfasoHkDw&amp;start=10&amp;sa=N" style="text-align:left"><span class="csb ch" style="background-position:-96px 0;width:71px"></span><span style="display:block;margin-left:53px">Next</span></a></td></tr></table><p id="bfl" class="flc" style="margin:19px 0 0;text-align:center"><a href="/support/websearch/bin/answer.py?answer=134479&amp;hl=en">Search Help</a> <a href="/quality_form?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=1&amp;prmd=ivns">Give us feedback</a></p><div id="fll" class="flc" style="margin:19px auto 19px auto;text-align:center"><a href="/">Google&#160;Home</a> <a href="
         /intl/en/ads/">Advertising&#160;Programs</a> <a href="/services">Business Solutions</a> <a href="/intl/en/policies/">Privacy</a> <a href="/intl/en/about.html">About Google</a></div></div></td><td valign="top"></td></tr></table><script src="/extern_js/f/CgJlbiswWjgALCswDjgALCswCjgAmgICaGUsKzAYOAAsgAJQkAJu/vwzbKdoxw18.js"></script><script type="text/javascript">google.ac.c({"client":"serp","dh":true,"ds":"","exp":"frgbld","fl":true,"host":"google.com","jsonp":true,"msgs":{"lcky":"I\u0026#39;m Feeling Lucky","lml":"Learn more","psrc":"This search was removed from your \u003Ca href=\"/history\"\u003EWeb History\u003C/a\u003E","psrl":"Remove","srch":"Google Search"},"ovr":{"fm":1,"l":1,"p":1,"pf":1,"ps":1,"sw":1},"pq":"allintext: -error REMOTE_ADDR REQUEST_METHOD googlebot(at)googlebot.com HTTP_USER_AGENT HTTP_CONNECTION HTTP_HOST HTTP_REFERER HTTP_ACCEPT","scd":10,"sce":5})</script></body></html>'''


sGoogleQuerResult_Chrome = \
'''<!doctype html>
<html itemscope="itemscope" itemtype="http://schema.org/WebPage">
<head>
<meta itemprop="image" content="/images/google_favicon_128.png"/>
<title>allintext: -error REMOTE_ADDR REQUEST_METHOD googlebot(at)googlebot.com HTTP_USER_AGENT HTTP_CONNECTION HTTP_HOST HTTP_REFERER HTTP_ACCEPT - Google Search</title>
<script>window.google={kEI:"wxxzT_2_DJG0iQeR0vjjDw",getEI:function(a){var b;while(a&&!(a.getAttribute&&(b=a.getAttribute("eid"))))a=a.parentNode;return b||google.kEI},https:function(){return window.location.protocol=="https:"},kEXPI:"17259,31700,36683,36822,36888,36934,37102,37197,37358,37431,37501,37573,37645,37655,37671,37676,37682,37753,37761,37775,37827,37864",kCSI:{e:"17259,31700,36683,36822,36888,36934,37102,37197,37358,37431,37501,37573,37645,37655,37671,37676,37682,37753,37761,37775,37827,37864",ei:"wxxzT_2_DJG0iQeR0vjjDw"},authuser:0,
ml:function(){},pageState:"#",kHL:"en",time:function(){return(new Date).getTime()},log:function(a,b,c,e){var d=new Image,h=google,i=h.lc,f=h.li,j="";d.onerror=(d.onload=(d.onabort=function(){delete i[f]}));i[f]=d;if(!c&&b.search("&ei=")==-1)j="&ei="+google.getEI(e);var g=c||"/gen_204?atyp=i&ct="+a+"&cad="+b+j+"&zx="+google.time();
var k=/^http:/i;if(k.test(g)&&google.https()){google.ml(new Error("GLMM"),false,{src:g});delete i[f];return}d.src=g;h.li=f+1},lc:[],li:0,j:{en:1,l:function(){google.fl=true},e:function(){google.fl=true},
b:location.hash&&location.hash!="#",bv:21,cf:"osb",pm:"p",pl:[],mc:0,sc:0.5,u:"c9c918f0"},Toolbelt:{},y:{},x:function(a,b){google.y[a.id]=[a,b];return false}};(function(){var a=
google.j;window.onpopstate=function(){a.psc=1};for(var b=0,c;c=["ad","bc","inpr","is","p","pa","ac","pc","pah","ph","sa","sifp","slp","spf","spn","xx","zc","zz"][b++];)(function(e){a[e]=function(){a.pl.push([e,arguments])}})(c)})();if(!window.chrome)window.chrome={};window.chrome.sv=2.00;window.chrome.userWantsQuery=function(a){google.x({id:"psyapi"},function(){google.nav.search({q:encodeURIComponent(a),
sourceid:"chrome-psyapi1"})})};
window.google.sn="web";window.google.timers={};window.google.startTick=function(a,b){window.google.timers[a]={t:{start:(new Date).getTime()},bfr:!(!b)}};window.google.tick=function(a,b,c){if(!window.google.timers[a])google.startTick(a);window.google.timers[a].t[b]=c||(new Date).getTime()};google.startTick("load",true);try{window.google.pt=window.chrome&&window.chrome.csi&&Math.floor(window.chrome.csi().pageT);}catch(u){}
</script>
<style>#gb{font:13px/27px Arial,sans-serif;height:102px}#gbz,#gbg{position:absolute;white-space:nowrap;top:0;height:30px;z-index:1000}#gbz{left:0;padding-left:4px}#gbg{right:0;padding-right:5px}#gbs{background:transparent;position:absolute;top:-999px;visibility:hidden;z-index:998}.gbto #gbs{background #fff}#gbx3,#gbx4{background-color:#2d2d2d;background-image:none;_background-image:none;background-position:0 -138px;background-repeat:repeat-x;border-bottom:1px solid #000;font-size:24px;height:29px;_height:30px;opacity:1;filter:alpha(opacity=100);position:absolute;top:0;width:100%;z-index:990}#gbx3{left:0}#gbx4{right:0}#gbb{position:relative}#gbbw{right:0;left:0;position:absolute;top:102px;width:100%}.gbtcb{position:absolute;visibility:hidden}#gbz .gbtcb{right:0}#gbg .gbtcb{left:0}.gbxx{display:none !important}.gbm{position:absolute;z-index:999;top:-999px;visibility:hidden;text-align:left;border:1px solid #bebebe;background:#fff;-moz-box-shadow:-1px 1px 1px rgba(0,0,0,.2);-webkit-box-shadow:0 2px 4px rgba(0,0,0,.2);box-shadow:0 2px 4px rgba(0,0,0,.2)}.gbrtl .gbm{-moz-box-shadow:1px 1px 1px rgba(0,0,0,.2)}.gbto .gbm,.gbto #gbs{top:51px;visibility:visible}#gbz .gbm,#gbz #gbs{left:0}#gbg .gbm,#gbg #gbs{right:0}.gbxms{background-color:#ccc;display:block;position:absolute;z-index:1;top:-1px;left:-2px;right:-2px;bottom:-2px;opacity:.4;-moz-border-radius:3px;filter:progid:DXImageTransform.Microsoft.Blur(pixelradius=5);*opacity:1;*top:-2px;*left:-5px;*right:5px;*bottom:4px;-ms-filter:"progid:DXImageTransform.Microsoft.Blur(pixelradius=5)";opacity:1\0/;top:-4px\0/;left:-6px\0/;right:5px\0/;bottom:4px\0/}.gbma{position:relative;top:-1px;border-style:solid dashed dashed;border-color:transparent;border-top-color:#c0c0c0;display:-moz-inline-box;display:inline-block;font-size:0;height:0;line-height:0;width:0;border-width:3px 3px 0;padding-top:1px;left:4px}#gbztms1,#gbi4m1,#gbi4s,#gbi4t{zoom:1}.gbtc,.gbmc,.gbmcc{display:block;list-style:none;margin:0;padding:0}.gbmc{background:#fff;padding:10px 0;position:relative;z-index:2;zoom:1}.gbt{position:relative;display:-moz-inline-box;display:inline-block;line-height:27px;padding:0;vertical-align:top}.gbt{*display:inline}.gbto{box-shadow:0 2px 4px rgba(0,0,0,.2);-moz-box-shadow:0 2px 4px rgba(0,0,0,.2);-webkit-box-shadow:0 2px 4px rgba(0,0,0,.2)}.gbzt,.gbgt{cursor:pointer;display:block;text-decoration:none !important}.gbts{border-left:1px solid transparent;border-right:1px solid transparent;display:block;*display:inline-block;padding:0 5px;position:relative;z-index:1000}.gbts{*display:inline}.gbto .gbts{background:#fff;border-color:#bebebe;color:#36c;padding-bottom:1px;padding-top:2px}.gbz0l .gbts{color:#fff;font-weight:bold}.gbtsa{padding-right:9px}#gbz .gbzt,#gbz .gbgt,#gbg .gbgt{color:#ccc!important}.gbtb2{display:block;border-top:2px solid transparent}.gbto .gbzt .gbtb2,.gbto .gbgt .gbtb2{border-top-width:0}.gbtb .gbts{background:url(//ssl.gstatic.com/gb/images/b_8d5afc09.png);_background:url(//ssl.gstatic.com/gb/images/b8_3615d64d.png);background-position:-27px -22px;border:0;font-size:0;padding:29px 0 0;*padding:27px 0 0;width:1px}.gbzt-hvr,.gbzt:focus,.gbgt-hvr,.gbgt:focus{background-color:transparent;background-image:none;_background-image:none;background-position:0 -102px;background-repeat:repeat-x;outline:none;text-decoration:none !important}.gbpdjs .gbto .gbm{min-width:99%}.gbz0l .gbtb2{border-top-color:transparent!important}#gbi4s,#gbi4s1{font-weight:bold}#gbg6.gbgt-hvr,#gbg6.gbgt:focus{background-color:transparent;background-image:none}.gbg4a{font-size:0;line-height:0}.gbg4a .gbts{padding:27px 5px 0;*padding:25px 5px 0}.gbto .gbg4a .gbts{padding:29px 5px 1px;*padding:27px 5px 1px}#gbi4i,#gbi4id{left:5px;border:0;height:24px;position:absolute;top:1px;width:24px}.gbto #gbi4i,.gbto #gbi4id{top:3px}.gbi4p{display:block;width:24px}#gbi4id,#gbmpid{background:url(//ssl.gstatic.com/gb/images/b_8d5afc09.png);_background:url(//ssl.gstatic.com/gb/images/b8_3615d64d.png)}#gbi4id{background-position:-29px -54px}#gbmpid{background-position:-58px 0px}#gbmpi,#gbmpid{border:none;display:inline-block;margin-top:10px;height:48px;width:48px}.gbmpiw{display:inline-block;line-height:9px;margin-left:20px}#gbmpi,#gbmpid,.gbmpiw{*display:inline}#gbg5{font-size:0}#gbgs5{padding:5px !important}.gbto #gbgs5{padding:7px 5px 6px !important}#gbi5{background:url(//ssl.gstatic.com/gb/images/b_8d5afc09.png);_background:url(//ssl.gstatic.com/gb/images/b8_3615d64d.png);background-position:0 0;display:block;font-size:0;height:17px;width:16px}.gbto #gbi5{background-position:-6px -22px}.gbn .gbmt,.gbn .gbmt:visited,.gbnd .gbmt,.gbnd .gbmt:visited{color:#dd8e27 !important}.gbf .gbmt,.gbf .gbmt:visited{color:#900 !important}.gbmt,.gbml1,.gbmlb,.gbmt:visited,.gbml1:visited,.gbmlb:visited{color:#36c !important;text-decoration:none !important}.gbmt,.gbmt:visited{display:block}.gbml1,.gbmlb,.gbml1:visited,.gbmlb:visited{display:inline-block;margin:0 10px}.gbml1,.gbmlb,.gbml1:visited,.gbmlb:visited{*display:inline}.gbml1,.gbml1:visited{padding:0 10px}.gbml1-hvr,.gbml1:focus{background:#eff3fb;outline:none}#gbpm .gbml1{display:inline;margin:0;padding:0;white-space:nowrap}#gbpm .gbml1-hvr,#gbpm .gbml1:focus{background:none;text-decoration:underline !important}.gbmlb,.gbmlb:visited{line-height:27px}.gbmlb-hvr,.gbmlb:focus{outline:none;text-decoration:underline !important}.gbmlbw{color:#666;margin:0 10px}.gbmt{padding:0 20px}.gbmt-hvr,.gbmt:focus{background:#eff3fb;cursor:pointer;outline:0 solid black;text-decoration:none !important}.gbm0l,.gbm0l:visited{color:#000 !important;font-weight:bold}.gbmh{border-top:1px solid #e5e5e5;font-size:0;margin:10px 0}#gbd4 .gbmh{margin:0}.gbmtc{padding:0;margin:0;line-height:27px}.GBMCC:last-child:after,#GBMPAL:last-child:after{content:'\0A\0A';white-space:pre;position:absolute}#gbd4 .gbpc,#gbmpas .gbmt{line-height:17px}#gbd4 .gbpgs .gbmtc{line-height:27px}#gbmpas .gbmt{padding-bottom:10px;padding-top:10px}#gbmple .gbmt,#gbmpas .gbmt{font-size:15px}#gbd4 .gbpc{display:inline-block;margin:6px 0 10px;margin-right:50px;vertical-align:top}#gbd4 .gbpc{*display:inline}.gbpc .gbps,.gbpc .gbps2{display:block;margin:0 20px}#gbmplp.gbps{margin:0 10px}.gbpc .gbps{color:#000;font-weight:bold}.gbpc .gbps2{font-size:13px}.gbpc .gbpd{margin-bottom:5px}.gbpd .gbmt,.gbmpmtd .gbmt{color:#666 !important}.gbmpme,.gbps2{color:#666;display:block;font-size:11px}.gbp0 .gbps2,.gbmpmta .gbmpme{font-weight:bold}#gbmpp{display:none}#gbd4 .gbmcc{margin-top:5px}.gbpmc{background:#edfeea}.gbpmc .gbmt{padding:10px 20px}#gbpm{*border-collapse:collapse;border-spacing:0;margin:0;white-space:normal}#gbpm .gbmt{border-top:none;color:#666 !important;font:11px Arial,sans-serif}#gbpms{*white-space:nowrap}.gbpms2{font-weight:bold;white-space:nowrap}#gbmpal{*border-collapse:collapse;border-spacing:0;margin:0;white-space:nowrap}.gbmpala,.gbmpalb{font:13px Arial,sans-serif;line-height:27px;padding:10px 20px 0;white-space:nowrap}.gbmpala{padding-left:0;text-align:left}.gbmpalb{padding-right:0;text-align:right}.gbp0 .gbps,.gbmpmta .gbmpmn{color:#000;display:inline-block;font-weight:bold;padding-right:34px;position:relative}.gbp0 .gbps,.gbmpmta .gbmpmn{*display:inline}.gbmpmtc,.gbp0i{background:url(//ssl.gstatic.com/gb/images/b_8d5afc09.png);_background:url(//ssl.gstatic.com/gb/images/b8_3615d64d.png);background-position:-484px -32px;position:absolute;height:21px;width:24px;right:0;top:-3px}.gbsup{color:#dd4b39;font:bold 9px/17px Verdana,Arial,sans-serif;margin-left:4px;vertical-align:top}#gb{height:102px;-moz-user-select:none;-o-user-select:none;-webkit-user-select:none;user-select:none}#gbbw{top:102px;min-width:980px;}#gb.gbet #gbbw,#gb.gbeti #gbbw{min-width:836px;}#gb.gbeu #gbbw,#gb.gbeui #gbbw{min-width:780px;}.gbxx{display:none !important}#gbq,#gbu{position:absolute;top:0px;white-space:nowrap}#gbu{height:71px}#gbu,#gbq1,#gbq3{z-index:987}#gbq{left:0;_overflow:hidden;width:100%}#gbq2{top:0px;z-index:986}#gbu{right:0;height:30px;margin-right:28px;padding-bottom:0;padding-top:20px}#gbu{top:0px}#gbx1,#gbx2{background:#f1f1f1;background:-webkit-gradient(radial,100 36,0,100 -40,120,from(#fafafa),to(#f1f1f1)),#f1f1f1;border-bottom:1px solid #666;border-color:#e5e5e5;height:71px;position:absolute;top:0px;width:100%;z-index:985;min-width:980px;}#gb.gbet #gbx1,#gb.gbeti #gbx1{min-width:836px;}#gb.gbeu #gbx1,#gb.gbeui #gbx1{min-width:780px;}#gbx1.gbxngh,#gbx2.gbxngh{background:-webkit-gradient(radial,100 36,0,100 -40,120,from(#ffffff),to(#f1f1f1)),#f1f1f1}#gbx1{left:0}#gbx2{right:0}#gbq1{left:0;margin:0;padding:0;margin-left:44px;position:absolute}#gbq1 .gbmai{right:4px;top:31px}.gbes#gbq1{margin-left:0}#gbq3{left:220px;padding-bottom:0;padding-top:20px;position:absolute;top:0px}#gbql{background:url(//ssl.gstatic.com/gb/images/j_f11bbae9.png) no-repeat;background-position:0 0;display:block;height:45px;width:116px}#gbqlw{display:table-cell;height:71px;padding-right:16px;position:relative;vertical-align:middle;0}#gbqld{border:none;display:block}.gbqldr{max-height:71px;max-width:160px}#gog{height:99px}.gbh{border-top:none}.gbpl,.gbpr,#gbpx1,#gbpx2{border-top:none !important;top:102px !important}.gbpl,.gbpr{margin-top:4px}.gbi5t{color:#666;display:block;margin:1px 15px;text-shadow:none}#gbq2{display:block;margin-left:220px;padding-bottom:0;padding-top:20px}#gbqf{display:block;margin:0;max-width:572px;min-width:572px;white-space:nowrap}.gbet#gbq2 #gbqf,.gbeti#gb #gbqf{max-width:434px;min-width:434px}.gbeu#gbqf,.gbeui#gb #gbqf{max-width:319px;min-width:319px}.gbqff{border:none;display:inline-block;margin:0;padding:0;vertical-align:top;width:100%}.gbqff{*display:inline}.gbqfqw,#gbqfb,.gbqfwa{vertical-align:top}#gbqfaa,#gbqfab,#gbqfqwb{position:absolute}#gbqfaa{left:0}#gbqfab{right:0}.gbqfqwb,.gbqfqwc{right:0;left:0;cursor:text}.gbqfqwb{padding:0 8px}#gbqfbw{margin:0 15px;display:inline-block}#gbqfbw{*display:inline}.gbqfb{background-color:#4d90fe;background-image:-webkit-gradient(linear,left top,left bottom,from(#4d90fe),to(#4787ed));background-image:-moz-linear-gradient(top,#4d90fe,#4787ed);background-image:-ms-linear-gradient(top,#4d90fe,#4787ed);background-image:-o-linear-gradient(top,#4d90fe,#4787ed);background-image:-webkit-linear-gradient(top,#4d90fe,#4787ed);background-image:linear-gradient(top,#4d90fe,#4787ed);filter:progid:DXImageTransform.Microsoft.gradient(startColorStr='#4d90fe',EndColorStr='#4787ed');border:1px solid #3079ed;-moz-border-radius:2px;-webkit-border-radius:2px;border-radius:2px;-moz-user-select:none;-webkit-user-select:none;color:#fff;cursor:default;display:inline-block;font-weight:bold;height:29px;line-height:29px;min-width:54px;*min-width:70px;text-align:center;text-decoration:none;padding:0 8px}.gbqfb{*display:inline}.gbqfb-hvr{border:1px solid #2f5bb7;background-color:#357ae8;background-image:-webkit-gradient(linear,left top,left bottom,from(#4d90fe),to(#357ae8));background-image:-webkit-linear-gradient(top,#4d90fe,#357ae8);background-image:-moz-linear-gradient(top,#4d90fe,#357ae8);background-image:-ms-linear-gradient(top,#4d90fe,#357ae8);background-image:-o-linear-gradient(top,#4d90fe,#357ae8);background-image:linear-gradient(top,#4d90fe,#357ae8);-webkit-box-shadow:0 1px 1px rgba(0,0,0,.1);-moz-box-shadow:0 1px 1px rgba(0,0,0,.1);box-shadow:0 1px 1px rgba(0,0,0,.1)}.gbqfb:focus{-moz-box-shadow:inset 0 0 0 1px #fff;-webkit-box-shadow:inset 0 0 0 1px #fff;box-shadow:inset 0 0 0 1px #fff;outline:none}.gbqfb::-moz-focus-inner{border:0}.gbqfb-hvr:focus{-moz-box-shadow:inset 0 0 0 1px #fff,0 1px 1px rgba(0,0,0,.1);-webkit-box-shadow:inset 0 0 0 1px #fff,0 1px 1px rgba(0,0,0,.1);box-shadow:inset 0 0 0 1px #fff,0 1px 1px rgba(0,0,0,.1)}.gbqfb:active{-moz-box-shadow:inset 0 1px 2px rgba(0,0,0,.3);-webkit-box-shadow:inset 0 1px 2px rgba(0,0,0,.3);box-shadow:inset 0 1px 2px rgba(0,0,0,.3)}.gbqfi{background:url(//ssl.gstatic.com/gb/images/j_f11bbae9.png);background-position:-12px -50px;display:inline-block;height:13px;margin:7px 19px;width:14px}.gbqfi{*display:inline}.gbqfqw{background:#fff;border:1px solid #d9d9d9;border-top:1px solid #c0c0c0;-moz-border-radius:1px;-webkit-border-radius:1px;border-radius:1px;height:27px}#gbqfqw{position:relative}.gbqfqw-hvr{border:1px solid #b9b9b9;border-top:1px solid #a0a0a0;-moz-box-shadow:inset 0 1px 2px rgba(0,0,0,.1);-webkit-box-shadow:inset 0 1px 2px rgba(0,0,0,.1);box-shadow:inset 0 1px 2px rgba(0,0,0,.1)}.gbqfwa{display:inline-block;width:100%}.gbqfwa{*display:inline}.gbqfwb{width:40%}.gbqfwc{width:60%}.gbqfwb .gbqfqw{margin-left:10px}.gbqfqw:active,.gbqfqwf{border:1px solid #4d90fe;-moz-box-shadow:inset 0 1px 2px rgba(0,0,0,.3);-webkit-box-shadow:inset 0 1px 2px rgba(0,0,0,.3);box-shadow:inset 0 1px 2px rgba(0,0,0,.3);outline:none}#gbqfq,#gbqfqb,#gbqfqc{background:transparent;border:none;height:19px;margin-top:4px;padding:0;vertical-align:top;width:100%}#gbqfq:focus,#gbqfqb:focus,#gbqfqc:focus{outline:none}.gbqfif,.gbqfsf{font:16px arial,sans-serif}#gbqfbwa{display:none;text-align:center;height:0}.gbqfba{background-color:#f5f5f5;background-image:-webkit-gradient(linear,left top,left bottom,from(#f5f5f5),to(#f1f1f1));background-image:-webkit-linear-gradient(top,#f5f5f5,#f1f1f1);background-image:-moz-linear-gradient(top,#f5f5f5,#f1f1f1);background-image:-ms-linear-gradient(top,#f5f5f5,#f1f1f1);background-image:-o-linear-gradient(top,#f5f5f5,#f1f1f1);background-image:linear-gradient(top,#f5f5f5,#f1f1f1);filter:progid:DXImageTransform.Microsoft.gradient(startColorStr='#f5f5f5',EndColorStr='#f1f1f1');border-color:#dcdcdc;border-color:rgba(0,0,0,.1);color:#555;margin:16px 8px}#gbqfbwa .gbqfb-hvr{background-color:#f8f8f8;background-image:-webkit-gradient(linear,left top,left bottom,from(#f8f8f8),to(#f1f1f1));background-image:-webkit-linear-gradient(top,#f8f8f8,#f1f1f1);background-image:-moz-linear-gradient(top,#f8f8f8,#f1f1f1);background-image:-ms-linear-gradient(top,#f8f8f8,#f1f1f1);background-image:-o-linear-gradient(top,#f8f8f8,#f1f1f1);background-image:linear-gradient(top,#f8f8f8,#f1f1f1);filter:progid:DXImageTransform.Microsoft.gradient(startColorStr='#f8f8f8',EndColorStr='#f1f1f1');border-color:#c6c6c6;-webkit-box-shadow:0 1px 1px rgba(0,0,0,.1);-moz-box-shadow:0 1px 1px rgba(0,0,0,.1);box-shadow:0 1px 1px rgba(0,0,0,.1);color:#333}.gbqfba:active{border-color:#c6c6c6;-webkit-box-shadow:inset 0 1px 2px rgba(0,0,0,.1);-moz-box-shadow:inset 0 1px 2px rgba(0,0,0,.1);box-shadow:inset 0 1px 2px rgba(0,0,0,.1);color:#333}.gbqfba:focus{border:1px solid #4d90fe;outline:none}#gbqfsa,#gbqfsb{font:bold 11px/27px Arial,sans-serif !important;vertical-align:top}#gbu .gbm,#gbu #gbs{right:0}.gbpdjs #gbd4{right:5px}#gbu .gbgt{color:#666}#gbu .gbt{margin-left:15px}#gbu .gbto{box-shadow:none;-moz-box-shadow:none;-webkit-box-shadow:none}#gbg4{padding-right:16px}#gbd1 .gbmc,#gbd3 .gbmc{padding:0}#gbns{display:none}.gbmwc{right:0;position:absolute;top:-999px;width:440px;z-index:999}#gbwc.gbmwca{top:0}.gbmsg{display:none;position:absolute;top:0}.gbmsgo .gbmsg{display:block;background:#fff;width:100%;text-align:center;z-index:3;top:30%}.gbmab,.gbmac,.gbmad,.gbmae{left:5px;border-style:dashed dashed solid;border-color:transparent;border-bottom-color:#bebebe;border-width:0 10px 10px;cursor:default;display:-moz-inline-box;display:inline-block;font-size:0;height:0;line-height:0;position:absolute;top:0;width:0;z-index:1000}.gbmab,.gbmac{visibility:hidden}.gbmac{border-bottom-color:#fff}.gbto .gbmab,.gbto .gbmac{visibility:visible}.gbmai{background:url(//ssl.gstatic.com/gb/images/j_f11bbae9.png);background-position:0 -50px;opacity:.8;font-size:0;line-height:0;position:absolute;height:4px;width:7px}.gbgt-hvr .gbmai{opacity:1;filter:alpha(opacity=100)}#gbgs3{background-color:#f8f8f8;background-image:-webkit-gradient(linear,left top,left bottom,from(#f8f8f8),to(#ececec));background-image:-webkit-linear-gradient(top,#f8f8f8,#ececec);background-image:-moz-linear-gradient(top,#f8f8f8,#ececec);background-image:-ms-linear-gradient(top,#f8f8f8,#ececec);background-image:-o-linear-gradient(top,#f8f8f8,#ececec);background-image:linear-gradient(top,#f8f8f8,#ececec);filter:progid:DXImageTransform.Microsoft.gradient(startColorStr='#f8f8f8',EndColorStr='#ececec');border:1px solid #c6c6c6;-moz-border-radius:2px;-o-border-radius:2px;-webkit-border-radius:2px;border-radius:2px;padding:0 10px;position:relative}#gbgsi{background:url(//ssl.gstatic.com/gb/images/j_f11bbae9.png);background-position:-32px -50px;height:10px;opacity:.8;position:absolute;top:8px;_top:10px;width:10px;left:10px}#gbgsa{background:url(//ssl.gstatic.com/gb/images/j_f11bbae9.png);background-position:0 -116px;height:11px;margin-left:-2px;position:absolute;top:8px;width:10px;left:100%}.gbgt-hvr #gbgsa{background-position:0 -228px}#gbg3:active #gbgsa{background-position:-32px -65px}.gbgt-hvr #gbgsi{opacity:1;filter:alpha(opacity=100)}#gbi3{padding-left:18px;vertical-align:top;zoom:1}.gbgt-hvr #gbgs3,#gbg3:focus #gbgs3,#gbg3:active #gbgs3{background-color:#ffffff;background-image:-webkit-gradient(linear,left top,left bottom,from(#ffffff),to(#ececec));background-image:-webkit-linear-gradient(top,#ffffff,#ececec);background-image:-moz-linear-gradient(top,#ffffff,#ececec);background-image:-ms-linear-gradient(top,#ffffff,#ececec);background-image:-o-linear-gradient(top,#ffffff,#ececec);background-image:linear-gradient(top,#ffffff,#ececec);filter:progid:DXImageTransform.Microsoft.gradient(startColorStr='#ffffff',EndColorStr='#ececec');border-color:#bbb}#gbg3:active #gbgs3{border-color:#b6b6b6}#gbg3:active #gbgs3{-moz-box-shadow:inset 0 1px 2px rgba(0,0,0,.2);-webkit-box-shadow:inset 0 1px 2px rgba(0,0,0,.2);box-shadow:inset 0 1px 2px rgba(0,0,0,.2)}#gbgs3 .gbmab{margin:40px 0 0}#gbgs3 .gbmac{margin:41px 0 0}#gbgs1{display:block;overflow:hidden;position:relative}#gbi1a{background-color:#d14836;background-image:-webkit-gradient(linear,left top,left bottom,from(#dd4b39),to(#d14836));background-image:-webkit-linear-gradient(top,#dd4b39,#d14836);background-image:-moz-linear-gradient(top,#dd4b39,#d14836);background-image:-ms-linear-gradient(top,#dd4b39,#d14836);background-image:-o-linear-gradient(top,#dd4b39,#d14836);background-image:linear-gradient(top,#dd4b39,#d14836);filter:progid:DXImageTransform.Microsoft.gradient(startColorStr='#dd4b39',EndColorStr='#d14836');border:1px solid #c13828;-moz-border-radius:2px;-o-border-radius:2px;-webkit-border-radius:2px;border-radius:2px;display:block;height:27px;width:27px}.gbgt-hvr #gbi1a{background-color:#c53727;background-image:-webkit-gradient(linear,left top,left bottom,from(#dd4b39),to(#c53727));background-image:-webkit-linear-gradient(top,#dd4b39,#c53727);background-image:-moz-linear-gradient(top,#dd4b39,#c53727);background-image:-ms-linear-gradient(top,#dd4b39,#c53727);background-image:-o-linear-gradient(top,#dd4b39,#c53727);background-image:linear-gradient(top,#dd4b39,#c53727);filter:progid:DXImageTransform.Microsoft.gradient(startColorStr='#dd4b39',EndColorStr='#c53727');border-color:#b0281a;border-bottom-color:#af301f;-moz-box-shadow:0 1px 1px rgba(0,0,0,.2);-webkit-box-shadow:0 1px 1px rgba(0,0,0,.2);box-shadow:0 1px 1px rgba(0,0,0,.2)}#gbg1:focus #gbi1a,#gbg1:active #gbi1a{background-color:#b0281a;background-image:-webkit-gradient(linear,left top,left bottom,from(#dd4b39),to(#b0281a));background-image:-webkit-linear-gradient(top,#dd4b39,#b0281a);background-image:-moz-linear-gradient(top,#dd4b39,#b0281a);background-image:-ms-linear-gradient(top,#dd4b39,#b0281a);background-image:-o-linear-gradient(top,#dd4b39,#b0281a);background-image:linear-gradient(top,#dd4b39,#b0281a);filter:progid:DXImageTransform.Microsoft.gradient(startColorStr='#dd4b39',EndColorStr='#b0281a');border-color:#992a1b;-moz-box-shadow:inset 0 1px 2px rgba(0,0,0,.3);-webkit-box-shadow:inset 0 1px 2px rgba(0,0,0,.3);box-shadow:inset 0 1px 2px rgba(0,0,0,.3)}.gbid#gbi1a{background-color:#f8f8f8;background-image:-webkit-gradient(linear,left top,left bottom,from(#f8f8f8),to(#ececec));background-image:-webkit-linear-gradient(top,#f8f8f8,#ececec);background-image:-moz-linear-gradient(top,#f8f8f8,#ececec);background-image:-ms-linear-gradient(top,#f8f8f8,#ececec);background-image:-o-linear-gradient(top,#f8f8f8,#ececec);background-image:linear-gradient(top,#f8f8f8,#ececec);filter:progid:DXImageTransform.Microsoft.gradient(startColorStr='#f8f8f8',EndColorStr='#ececec');border-color:#c6c6c6}.gbgt-hvr .gbid#gbi1a,#gbg1:focus .gbid#gbi1a,#gbg1:active .gbid#gbi1a{background-color:#ffffff;background-image:-webkit-gradient(linear,left top,left bottom,from(#ffffff),to(#ececec));background-image:-webkit-linear-gradient(top,#ffffff,#ececec);background-image:-moz-linear-gradient(top,#ffffff,#ececec);background-image:-ms-linear-gradient(top,#ffffff,#ececec);background-image:-o-linear-gradient(top,#ffffff,#ececec);background-image:linear-gradient(top,#ffffff,#ececec);filter:progid:DXImageTransform.Microsoft.gradient(startColorStr='#ffffff',EndColorStr='#ececec');border-color:#bbb}#gbg1:active .gbid#gbi1a{border-color:#b6b6b6;-moz-box-shadow:inset 0 1px 2px rgba(0,0,0,.3);-webkit-box-shadow:inset 0 1px 2px rgba(0,0,0,.3);box-shadow:inset 0 1px 2px rgba(0,0,0,.3)}#gbi1,#gbi1c{left:0;bottom:1px;color:#fff;display:block;font-size:14px;font-weight:bold;position:absolute;text-align:center;text-shadow:0 1px rgba(0,0,0,.1);-moz-transition-property:bottom;-moz-transition-duration:0;-o-transition-property:bottom;-o-transition-duration:0;-webkit-transition-property:bottom;-webkit-transition-duration:0;-moz-user-select:none;-o-user-select:none;-webkit-user-select:none;user-select:none;width:100%}.gbgt-hvr #gbi1,#gbg1:focus #gbi1{text-shadow:0 1px rgba(0,0,0,.3)}.gbids#gbi1,.gbgt-hvr .gbids#gbi1,#gbg1:focus .gbids#gbi1,#gbg1:active .gbids#gbi1{color:#999;text-shadow:none}#gbg1 .gbmab{margin:41px 0 0}#gbg1 .gbmac{margin:42px 0 0}#gbi4t{display:block;margin:1px 0;overflow:hidden;text-overflow:ellipsis}#gbg6 #gbi4t,#gbg4 #gbgs4d{color:#666;text-shadow:none}#gb_70 #gbi4t,#gbg7 .gbit{margin:0 15px}#gbg7 .gbgs{margin-left:10px}#gbgs4,.gbgs{background-color:#f8f8f8;background-image:-webkit-gradient(linear,left top,left bottom,from(#f8f8f8),to(#ececec));background-image:-webkit-linear-gradient(top,#f8f8f8,#ececec);background-image:-moz-linear-gradient(top,#f8f8f8,#ececec);background-image:-ms-linear-gradient(top,#f8f8f8,#ececec);background-image:-o-linear-gradient(top,#f8f8f8,#ececec);background-image:linear-gradient(top,#f8f8f8,#ececec);filter:progid:DXImageTransform.Microsoft.gradient(startColorStr='#f8f8f8',EndColorStr='#ececec');border:1px solid #c6c6c6;display:block;-moz-border-radius:2px;-o-border-radius:2px;-webkit-border-radius:2px;border-radius:2px}#gbgs4d{display:block;position:relative}#gbgs4dn{display:inline-block;overflow:hidden;text-overflow:ellipsis}.gbgt-hvr #gbgs4d{background-color:transparent;background-image:none}#gbg4 #gbgs4{position:relative;height:27px;width:27px}.gbgt-hvr #gbgs4,#gbg4:focus #gbgs4,#gbg4:active #gbgs4,#gbg_70:focus #gbgs4,#gbg_70:active #gbgs4,#gbg7:focus .gbgs,#gbg7:active .gbgs{background-color:#ffffff;background-image:-webkit-gradient(linear,left top,left bottom,from(#ffffff),to(#ececec));background-image:-webkit-linear-gradient(top,#ffffff,#ececec);background-image:-moz-linear-gradient(top,#ffffff,#ececec);background-image:-ms-linear-gradient(top,#ffffff,#ececec);background-image:-o-linear-gradient(top,#ffffff,#ececec);background-image:linear-gradient(top,#ffffff,#ececec);filter:progid:DXImageTransform.Microsoft.gradient(startColorStr='#ffffff',EndColorStr='#ececec');border-color:#bbb}#gbg4:active #gbgs4,#gb_70:active #gbgs4,#gbg7:active .gbgs{border-color:#b6b6b6;-moz-box-shadow:inset 0 1px 2px rgba(0,0,0,.3);-webkit-box-shadow:inset 0 1px 2px rgba(0,0,0,.3);box-shadow:inset 0 1px 2px rgba(0,0,0,.3)}#gbi4i,#gbi4id{left:0;height:27px;position:absolute;top:0;width:27px}#gbmpi,#gbmpid{margin-right:0;height:96px;width:96px}#gbi4id,#gbmpid{background:url(//ssl.gstatic.com/gb/images/j_f11bbae9.png)}#gbi4id{background-position:0 -68px}#gbmpid{background-position:-62px -50px}.gbto #gbi4i,.gbto #gbi4id{top:0}#gbgs4 .gbmai{left:33px;top:12px}#gbgs4d .gbmai{left:100%;margin-left:5px;top:12px}#gbgs4 .gbmab{margin:40px 0 0}#gbgs4 .gbmac{margin:41px 0 0}#gbgs4d .gbmab{margin:41px 0 0}#gbgs4d .gbmac{margin:42px 0 0}#gbgs4d .gbmab,#gbgs4d .gbmac{left:50%;margin-left:-5px}.gbmpmtc,.gbp0i{background:url(//ssl.gstatic.com/gb/images/j_f11bbae9.png);background-position:-91px -228px}.gbiba{margin:10px 20px}.gbem#gb,.gbemi#gb{height:102px}.gbes#gb,.gbesi#gb{height:102px}.gbem#gbx1,.gbem#gbx2,.gbem#gbqlw,.gbemi#gb #gbx1,.gbemi#gb #gbx2,.gbemi#gb #gbqlw{height:71px}.gbem#gb #gbbw,.gbemi#gb #gbbw{top:102px}.gbem#gbu,.gbem#gbq2,.gbem#gbq3,.gbemi#gb #gbu,.gbemi#gb #gbq2,.gbemi#gb #gbq3{padding-top:20px}.gbem#gbq2,.gbemi#gb #gbq2{margin-left:160px;padding-bottom:0}.gbem#gbq3,.gbemi#gb #gbq3{left:160px}.gbem#gbmail,.gbemi#gb #gbmail{top:31px}.gbes#gbx1,.gbes#gbx2,.gbes#gbqlw,.gbesi#gb #gbx1,.gbesi#gb #gbx2,.gbesi#gb #gbqlw{height:57px}.gbes#gb #gbbw,.gbesi#gb #gbbw{top:102px}.gbes#gbu,.gbes#gbq2,.gbes#gbq3,.gbesi#gb #gbu,.gbesi#gb #gbq2,.gbesi#gb #gbq3{padding-top:15px}.gbet#gbq2,.gbeti#gb #gbq2,.gbes#gbq2,.gbesi#gb #gbq2{margin-left:140px;padding-bottom:0}.gbeu#gbq2,.gbeui#gb #gbq2{margin-left:136px;padding-bottom:0}.gbemi#gb .gbto #gbd1,.gbemi#gb .gbto #gbd3,.gbemi#gb .gbto #gbd4,.gbemi#gb .gbto #gbs,.gbto .gbem#gbd1,.gbto .gbem#gbd3,.gbto .gbem#gbd4,.gbto .gbem#gbs{top:51px}.gbesi#gb .gbto #gbd1,.gbesi#gb .gbto #gbd3,.gbesi#gb .gbto #gbd4,.gbesi#gb .gbto #gbs,.gbto .gbes#gbd1,.gbto .gbes#gbd3,.gbto .gbes#gbd4,.gbto .gbes#gbs{top:42px}.gbemi #gbq1.gbto #gbz,.gbemi #gbq1.gbto #gbs,.gbem #gbq1.gbto #gbz,.gbem #gbq1.gbto #gbs{top:71px !important;left:-23px}.gbesi #gbq1.gbto #gbz,.gbesi #gbq1.gbto #gbs,.gbes #gbq1.gbto #gbz,.gbes #gbq1.gbto #gbs{top:57px !important;left:-11px}.gbemi #gbq1 .gbmab,.gbem #gbq1 .gbmab{margin:61px 0 0}.gbemi #gbq1 .gbmac,.gbem #gbq1 .gbmac{margin:62px 0 0}.gbesi #gbq1 .gbmab,.gbes #gbq1 .gbmab{margin:47px 0 0}.gbesi #gbq1 .gbmac,.gbes #gbq1 .gbmac{margin:48px 0 0}.gbemi #gbq1 #gbz,.gbem#gbq1 #gbz,.gbemi #gbq1 #gbs,.gbem#gbq1 #gbs{margin-left:8px}.gbesi #gbq1 #gbz,.gbes#gbq1 #gbz,.gbesi #gbq1 #gbs,.gbes#gbq1 #gbs{margin-left:-4px}.gbes#gbq3,.gbesi#gb #gbq3{left:140px}.gbem#gbq1,.gbemi#gb #gbq1{margin-left:28px}.gbem#gbql,.gbemi#gb #gbql,.gbes#gbql,.gbesi#gb #gbql,.gbet#gbql,.gbeti#gb #gbql,.gbeu#gbql,.gbeui#gb #gbql{background-position:0 -186px;height:37px;width:95px}.gbet#gbq1,.gbeti#gb #gbq1,.gbes#gbq1,.gbesi#gb #gbq1{margin-left:16px}.gbeu#gbq1,.gbeui#gb #gbq1{margin-left:12px}.gbemi#gb .gbqldr,.gbem#gbqlw .gbqldr{max-height:71px;max-width:160px}.gbem#gbu,.gbemi#gb #gbu{margin-right:12px}.gbet#gbu,.gbeti#gb #gbu,.gbeu#gbu,.gbeui#gb #gbu,.gbes#gbu,.gbesi#gb #gbu{margin-right:0px}.gbeu#gbu .gbt,.gbeui#gb #gbu .gbt,.gbet#gbu .gbt,.gbeti#gb #gbu .gbt,.gbes#gbu .gbt,.gbesi#gb #gbu .gbt{margin-left:6px}.gbeti#gb .gbqldr,.gbet#gbqlw .gbqldr,.gbesi#gb .gbqldr,.gbes#gbqlw .gbqldr{max-height:57px;max-width:144px}.gbeui#gb .gbqldr,.gbeu#gbqlw .gbqldr{max-height:57px;max-width:124px}.gbes#gbmail,.gbesi#gb #gbmail{top:24px}.gbemi#gb #gbpr,.gbem#gbpr{left:28px}.gbemi#gb .gbqpa,.gbem#gbpr .gbqpa,.gbesi#gb .gbqpa,.gbes#gbpr .gbqpa{width:95px}.gbesi#gb #gbpr,.gbes#gbpr{left:16px}.gbemi#gb #gbg3 .gbmab,.gbem#gbg3 .gbmab,.gbemi#gb #gbgs4 .gbmab,.gbem#gbg4 .gbmab{margin:40px 0 0}.gbemi#gb #gbg1 .gbmab,.gbem#gbg1 .gbmab{margin:41px 0 0}.gbemi#gb #gbg3 .gbmac,.gbem#gbg3 .gbmac,.gbemi#gb #gbgs4 .gbmac,.gbem#gbg4 .gbmac{margin:41px 0 0}.gbemi#gb #gbg1 .gbmac,.gbem#gbg1 .gbmac{margin:42px 0 0}.gbesi#gb #gbg3 .gbmab,.gbes#gbg3 .gbmab,.gbesi#gb #gbgs4 .gbmab,.gbes#gbg4 .gbmab{margin:32px 0 0}.gbesi#gb #gbg1 .gbmab,.gbes#gbg1 .gbmab{margin:33px 0 0}.gbesi#gb #gbg3 .gbmac,.gbes#gbg3 .gbmac,.gbesi#gb #gbgs4 .gbmac,.gbes#gbg4 .gbmac{margin:33px 0 0}.gbesi#gb #gbg1 .gbmac,.gbes#gbg1 .gbmac{margin:34px 0 0}.gbemi#gb #gbgs4d .gbmab,.gbem#gbg4 #gbgs4d .gbmab{margin:41px 0 0}.gbesi#gb #gbgs4d .gbmab,.gbes#gbg4 #gbgs4d .gbmab{margin:33px 0 0}.gbemi#gb #gbgs4d .gbmac,.gbem#gbg4 #gbgs4d .gbmac{margin:42px 0 0}.gbesi#gb #gbgs4d .gbmac,.gbes#gbg4 #gbgs4d .gbmac{margin:34px 0 0}.gbemi#gb #gbgs4d .gbmac,.gbem#gbg4 #gbgs4d .gbmac,.gbesi#gb #gbgs4d .gbmac,.gbes#gbg4 #gbgs4d .gbmac,.gbemi#gb #gbgs4d .gbmab,.gbem#gbg4 #gbgs4d .gbmab,.gbesi#gb #gbgs4d .gbmab,.gbes#gbg4 #gbgs4d .gbmab{margin-left:-5px}#gb #gbx1,#gb #gbx3{left:0}#gbx1,#gb #gbx1,#gbq,#gbu,#gb #gbq,#gb #gbu{top:30px}#gb #gbu{top:30px}#gbzw #gbz{padding-left:0;z-index:991}#gbz .gbto #gbd,#gbz .gbto #gbs{top:29px}#gbx3{min-width:980px;border-color:#000;background-color:#2d2d2d;background-image:none;background-position:0 -255px;opacity:1;filter:alpha(opacity=100)}#gbz .gbzt,#gbz .gbgt{color:#bbb !important;font-weight:bold}#gbq .gbgt-hvr,#gbq .gbgt:focus,#gbz .gbz0l .gbts,#gbz .gbzt-hvr,#gbz .gbzt:focus,#gbz .gbgt-hvr,#gbz .gbgt:focus,#gbu .gbz0l .gbts,#gbu .gbzt-hvr,#gbu .gbzt:focus,#gbu .gbgt-hvr,#gbu .gbgt:focus{background-color:transparent;background-image:none}#gbz .gbz0l .gbts,#gbz .gbzt-hvr,#gbz .gbzt:focus,#gbz .gbgt-hvr,#gbz .gbgt:focus{color:#fff!important}#gbz .gbma{border-top-color:#aaa}#gbz .gbzt-hvr .gbma,#gbz .gbzt:focus .gbma,#gbz .gbgt-hvr .gbma,#gbz .gbgt:focus .gbma{border-top-color:#fff}#gbq1.gbto{-moz-box-shadow:none;-o-box-shadow:none;-webkit-box-shadow:none;box-shadow:none}#gbz .gbto .gbma,#gbz .gbto .gbzt-hvr .gbma,#gbz .gbto .gbzt:focus .gbma,#gbz .gbto .gbgt-hvr .gbma,#gbz .gbto .gbgt:focus .gbma{border-top-color:#000}#gbz .gbto .gbts,#gbd .gbmt{color:#000 !important;font-weight:bold}#gbd .gbmt-hvr,#gbd .gbmt:focus{background-color:#f5f5f5}#gbz .gbts{padding:0 9px;z-index:991}#gbz .gbto .gbts{padding-bottom:1px;padding-top:2px;z-index:1000}#gbqlw{cursor:default}#gbzw{left:0;height:30px;margin-left:34px;position:absolute;top:0}#gbz{height:30px}.gbemi#gb #gbzw,.gbem#gbzw{height:30px;margin-left:18px}.gbeui#gb #gbzw,.gbeu#gbzw,.gbeti#gb #gbzw,.gbet#gbzw,.gbesi#gb #gbzw,.gbes#gbzw{height:30px;margin-left:6px}.gbeui#gb #gbzw,.gbeu#gbzw{margin-left:2px}.gbemi#gb #gbzw #gbz,.gbem#gbzw #gbz{height:30px}.gbemi#gb #gbx3,.gbem#gbx3{height:29px}.gbesi#gb #gbzw #gbz,.gbes#gbzw #gbz{height:30px}.gbesi#gb #gbx3,.gbes#gbx3{height:29px}#gb.gbet #gbx3,#gb.gbeti #gbx3{min-width:836px;}#gb.gbeu #gbx3,#gb.gbeui #gbx3{min-width:780px;}#gbzw .gbt{line-height:27px}.gbemi#gb #gbzw .gbt .gbem#gbzw .gbt{line-height:27px}.gbesi#gb #gbzw .gbt,.gbes#gbzw .gbt{line-height:27px}.gbqfh#gbq1 #gbql{display:none}.gbqfh#gbx1,.gbqfh#gbx2,.gbem#gb .gbqfh#gbx1,.gbem#gb .gbqfh#gbx2,.gbemi#gb .gbqfh#gbx1,.gbemi#gb .gbqfh#gbx2,.gbes#gb .gbqfh#gbx1,.gbes#gb .gbqfh#gbx2,.gbesi#gb .gbqfh#gbx1,.gbesi#gb .gbqfh#gbx2,.gbet#gb .gbqfh#gbx1,.gbet#gb .gbqfh#gbx2,.gbeti#gb .gbqfh#gbx1,.gbeti#gb .gbqfh#gbx2,.gbeu#gb .gbqfh#gbx1,.gbeu#gb .gbqfh#gbx2,.gbeui#gb .gbqfh#gbx1,.gbeui#gb .gbqfh#gbx2{border-bottom-width:0;height:0}.gbes#gb,.gbesi#gb{height:102px}.gbes#gbx1,.gbes#gbx2,.gbes#gbqlw,.gbesi#gb #gbx1,.gbesi#gb #gbx2,.gbesi#gb #gbqlw{height:71px}#gb .gbes#gbx1,#gb .gbes#gbx2,.gbesi#gb #gbx1,.gbesi#gb #gbx2,#gb .gbes#gbq,#gb .gbes#gbu,.gbesi#gb #gbq,.gbesi#gb #gbu{top:30px}.gbes#gb #gbbw,.gbesi#gb #gbbw{top:102px !important}.gbes#gbu,.gbes#gbq2,.gbes#gbq3,.gbesi#gb #gbu,.gbesi#gb #gbq2,.gbesi#gb #gbq3{padding-top:20px}.gbes#gbq2,.gbesi#gb #gbq2{padding-bottom:0}.gbesi#gb .gbto #gbd1,.gbesi#gb .gbto #gbd3,.gbesi#gb .gbto #gbd4,.gbesi#gb .gbto #gbs,.gbto .gbes#gbd1,.gbto .gbes#gbd3,.gbto .gbes#gbd4,.gbes#gbu .gbto #gbs{top:51px}.gbemi#gb #gbd,.gbem#gbzw #gbd,.gbemi#gb #gbzw .gbto #gbs,.gbem#gbzw .gbto #gbs{top:29px}.gbesi#gb #gbd,.gbes#gbzw #gbd,.gbesi#gb #gbzw .gbto #gbs,.gbes#gbzw .gbto #gbs{top:29px}.gbesi#gb #gbg3 .gbmab,.gbes#gbg3 .gbmab,.gbesi#gb #gbgs4 .gbmab,.gbes#gbg4 .gbmab{margin:40px 0 0}.gbesi#gb #gbg1 .gbmab,.gbes#gbg1 .gbmab{margin:41px 0 0}.gbesi#gb #gbg3 .gbmac,.gbes#gbg3 .gbmac,.gbesi#gb #gbgs4 .gbmac,.gbes#gbg4 .gbmac{margin:41px 0 0}.gbesi#gb #gbg1 .gbmac,.gbes#gbg1 .gbmac{margin:42px 0 0}.gbesi#gb #gbgs4d .gbmab,.gbes#gbg4 #gbgs4d .gbmab{margin:41px 0 0}.gbesi#gb #gbgs4d .gbmac,.gbes#gbg4 #gbgs4d .gbmac{margin:42px 0 0}</style>
<style id=gstyle>body{color:#000;margin:0;overflow-y:scroll}body,#leftnav,#tbdi,#hidden_modes,#hmp{background:#fff}a.gb1,a.gb2,a.gb3,.link{color:#12c!important}.ts{border-collapse:collapse}.ts td{padding:0}.ti,.bl,#res h3{display:inline}.ti{display:inline-table}#tads a.mblink,#tads a.mblink b,#tadsb a.mblink,#tadsb a.mblink b,#tadsto a.mblink,#tadsto a.mblink b,#rhs a.mblink,#rhs a.mblink b{color:#1122cc!important}#tads .ch,#tadsb .ch,#tadsto .ch,#rhs .ch{margin-top:4px;}a:link,.w,#prs a:visited,#prs a:active,.q:active,.q:visited,.kl:active{color:#12c}.mblink:visited,a:visited{color:#61c}.vst:link{color:#61c}.cur,.b{font-weight:bold}.j{width:42em;font-size:82%}.s{max-width:42em}.sl{font-size:82%}.hd{position:absolute;width:1px;height:1px;top:-1000em;overflow:hidden}.f,.f a:link,.m,.c h2,#mbEnd h2,#tads h2,#tadsb h2,#tadsto h2,.descbox{color:#666}.a,cite,cite a:link,cite a:visited,.cite,.cite:link,#mbEnd cite b,#tads cite b,#tadsb cite b,#tadsto cite b,#ans>i,.bc a:link{color:#093;font-style:normal}.mslg cite{display:none}.ng{color:#dd4b39}h1,ol,ul,li{margin:0;padding:0}li.head,li.g,body,html,.std,.c h2,#mbEnd h2,h1{font-size:small;font-family:arial,sans-serif}.c h2,#mbEnd h2,h1{font-weight:normal}.clr{clear:both;margin:0 8px}.blk a{color:#000}#nav a{display:block}#nav .i{color:#a90a08;font-weight:bold}.csb,.ss,.play_icon,.mini_play_icon,.micon,.licon,.close_btn,#tbp,.mbi,.inline-close-btn{background:url(/images/nav_logo107.png) no-repeat;overflow:hidden}.csb,.ss{background-position:0 0;height:40px;display:block}.ss{background-position:0 -91px;position:absolute;left:0;top:0}.cps{height:18px;overflow:hidden;width:114px}.spell{font-size:16px}.spell_orig{font-size:13px;text-decoration:none}a.spell_orig:hover{text-decoration:underline}.mbi{background-position:-153px -70px;display:inline-block;float:left;height:13px;margin-right:3px;margin-top:1px;width:13px}.mbt{color:#11c;float:left;font-size:13px;margin-right:5px;position:relative}.mbt.mbto{bottom:1px}#nav td{padding:0;text-align:center}.ch{cursor:pointer}h3,.med{font-size:medium;font-weight:normal;padding:0;margin:0}.e{margin:2px 0 .75em}.slk div{padding-left:12px;text-indent:-10px}.fc{margin-top:.5em;padding-left:16px}#mbEnd cite{text-align:left}#rhs_block{margin-bottom:-20px}#bsf,.blk{border-top:1px solid #6b90da;background:#f0f7f9}#bsf{border-bottom:1px solid #6b90da}#cnt{clear:both}#res{padding-right:1em;margin:0 16px}.c{background:#fff8e7;margin:0 8px;border:1px solid #fff8e7}.c li{padding:0 3px 0 8px;margin:0}#mbEnd li{margin:1em 0;padding:0}.xsm{font-size:x-small}ol li{list-style:none}#ncm ul li{list-style-type:disc}.sm li{margin:0}.gl,#foot a,.nobr{white-space:nowrap}#mbEnd .med{white-space:normal}.sl,.r{display:inline;font-weight:normal;margin:0}.r{font-size:medium}h4.r{font-size:small}.mr{margin-top:6px}.mrf{padding-top:6px}h3.tbpr{margin-top:.4em;margin-bottom:1.2em}img.tbpr{border:0;width:15px;height:15px;margin-right:3px}.jsb{display:block}.nojsb{display:none}.vshid{display:none}.nwd{font-size:10px;padding:16px;text-align:center}.cpb{max-width:130px;overflow:hidden;position:relative;text-overflow:ellipsis;white-space:nowrap}.cpc{background:url(//ssl.gstatic.com/s2/oz/images/circles/cpw.png) no-repeat scroll 0 -28px;height:13px;margin:7px 5px 0 0;width:13px}div.cpss{height:13px;line-height:13px;font-size:10px;padding:0 6px;margin-bottom:0;margin-top:1px}div.cpss .cpc{background-position:0 -42px;height:10px;margin-top:2px;width:10px}.cpbb{background:-webkit-gradient(linear,left top,left bottom,from(#9e9e9e),to(#999));border:1px solid #999;color:#fff}.cpbb:hover{background:-webkit-gradient(linear,left top,left bottom,from(#9e9e9e),to(#8e8e8e));border:1px solid #888}.cpbb:active{background:-webkit-gradient(linear,left top,left bottom,from(#9e9e9e),to(#7e7e7e));}#ss-box{background:#fff;border:1px solid;border-color:#c9d7f1 #36c #36c #a2bae7;left:0;margin-top:.1em;position:absolute;visibility:hidden;z-index:101}#ss-box a{display:block;padding:.2em .31em;text-decoration:none}#ss-box a:hover{background:#4D90FE;color:#fff!important}a.ss-selected{color:#222!important;font-weight:bold}a.ss-unselected{color:#12c!important}.ss-selected .mark{display:inline}.ss-unselected .mark{visibility:hidden}#ss-barframe{background:#fff;left:0;position:absolute;visibility:hidden;z-index:100}.ri_cb{left:0;margin:6px;position:absolute;top:0;z-index:1}.ri_sp{display:-moz-inline-box;display:inline-block;text-align:center;vertical-align:top;margin-bottom:6px}.ri_of{opacity:0.40;}.ri_sp img{vertical-align:bottom}a.wtall, .f a.wtall, .f a.wtaal, .f a.wtalm{color:#12C;}a.wtaal{white-space:normal}.wtalbal,.wtalbar{background:url(/images/nav_logo107.png) no-repeat}.wtalb{box-shadow:0 4px 16px rgba(0,0,0,0.2);-webkit-box-shadow:0 4px 16px rgba(0,0,0,0.2);outline:1px solid #ccc;background-color:#fff;display:block;visibility:hidden;padding:16px;position:absolute;z-index:120  }.wtalbal{height:11px;position:absolute;width:17px;background-position:0 -212px;right:+32px;top:-11px}.wtalbar{height:11px;position:absolute;width:17px;background-position:-50px -212px;right:+19px;top:-11px}.so{margin-top:4px;position:relative;white-space:normal}.so img{border:0;margin-left:0;margin-right:1px;vertical-align:top}.son{position:relative}.so .soh{background-color:#FFFFD2;border:1px solid #FDF0BF;color:#000;display:none;font-size:8pt;padding:3px;position:absolute;white-space:nowrap;z-index:10}.so.agg{margin-top:0}.soi{background:#ebeff9;line-height:22px;padding:0 4px;position:static;vertical-align:middle}.soi a{white-space:nowrap}.soi img{margin-top:-3px;vertical-align:middle}.soi .lsbb{display:inline-block;height:20px;margin-bottom:4px}.soi .lsb{background-repeat:repeat-x;font-size:small;height:20px;padding:0 5px}#rhs_block .so{display:block;font-size:11px}.siw{display:inline-block;position:relative}.sia{background-color:#4c4c4c;bottom:0;font-size:11px;margin:4px;padding-left:2px;position:absolute}.sia .f,.sia a.fl:link,.sia a.fl:visited{color:#fff!important;overflow:hidden;text-overflow:ellipsis;width:100%;white-space:nowrap}.soih div.so{margin-top:0}.soih div.so_text span.son{display:inline;white-space:normal}.socp div.sogpn{display:none}.snw{ white-space:nowrap}div.so table.ts.inlso {cursor:pointer;-webkit-user-select: none;-khtml-user-select: none;-moz-user-select: none;-o-user-select: none;user-select: none}span.inlbtn{background-image:url(//ssl.gstatic.com/s2/oz/images/stream/expand.png);background-repeat:no-repeat;height:7px;margin-top:5px;margin-left:9px;padding-right:5px;position:absolute;width:8px}li.g.inlexp span.inlbtn{background-image:url(//ssl.gstatic.com/s2/oz/images/stream/collapse.png)}li.g.inlldg span.inlbtn,li.g.inlexp.inlldg span.inlbtn{background-image:url(//ssl.gstatic.com/s2/profiles/images/Spinner.gif);height:16px;margin-right:6px;margin-top:0px;width:16px}div.inlerr{color:#666;padding-top:6px}.ps-map{float:left}.ps-map img{border:1px solid #00c}a.tiny-pin,a.tiny-pin:link,a.tiny-pin:hover{text-decoration:none;color:12c}a.tiny-pin:hover span{text-decoration:underline}.tiny-pin table{vertical-align:middle}.tiny-pin p{background-image:url(/images/nav_logo107.png);background-position:-154px -212px;height:15px;margin:0;padding:0;top:-1px;overflow:hidden;position:relative;width:9px;}.pspa-price{font-size:medium;font-weight:bold}.pspa-call-price{font-size:small;font-weight:bold}.pspa-loyalty{font-size:small;}.pspa-store-avail{color:#093}.pspa-out-of-stock{color:#dd4b39}li.ppl{margin-bottom:11px;padding:6px;position:relative}#ppldir #ppldone, #ppldir #pplundo, #ppldir #pplcancel{color:#00f;cursor:pointer;text-decoration:underline}#ppldir{background:rgb(247,243,181);display:none;line-height:1.5em;outline:1px solid rgb(255,185,23);padding:6px 4px 6px 6px;position:absolute;width:90%;z-index:20}#ppldir.working{display:block}.pplclustered .pplclusterhide{visibility:hidden}.pplclustered .pplfeedback, .pplclustered .pplclusterdrop{display:none !important}.pplfeedback{-webkit-box-shadow:inset 0 1px 0px rgba(255,255,255,.3), 0 1px 0px #aaa;right:5px;background:rgba(235, 242, 252, 1.0);border:1px solid #afafaf;color:#333 !important;cursor:pointer;display:none;font-size:1.0em;float:right;margin-top:5px;margin-right:5px;opacity:1.0;padding:5px 10px;position:absolute;text-decoration:none;top:5px;vertical-align:middle;white-space:nowrap}.pplfeedback:active{background:-webkit-gradient(linear,left top,left bottom,from(#ddd),to(#eee))}li.ppl:hover .pplfeedback{opacity:1.0}.pplclustered:hover{border:0px;background-color:'' !important;margin-left:0px !important}li.ppl:hover{background-color:#ebf2fc;border:1px solid #cddcf9;padding:5px}.pplselected{background-color:#EBF2FC}.ppldragging{background-color:#B2D2FF}li.g.ppld{margin-bottom:0px;padding:3px}li.g.ppld:hover{padding:2px}.ppl_thumb_src{color:#767676;font-size:0.8em;line-height:1.3em;overflow:hidden;text-overflow:ellipsis;padding:0;text-align:center;width:70px}a.pplatt:link{color:#767676;text-decoration:none}a.pplatt:hover{color:#767676;text-decoration:underline}li.ppl:hover .pplfeedback{display:block}.ppl_thy{color:#767676;margin-left:3px}.ppl_crc{margin:35px 10px 0px 0px;display:none}.fbbtn{margin-left:5px;width:35px}div.pplthumb img.th{border:none}div.prf_vis:hover span.vis_tip{display:block!important}#rhs_block li.pplic .so{font-size:inherit}span.malbstb{border-radius:2px;padding:3px 6px;margin-top:6px;display:inline-block}span.malbstb a,div#tadsto span.malbstb a{color:#fff;text-decoration:none}span.malbstl{background:#787878;color:#fff}span.malbstl:hover{background:#007EE7}span.malbstl,span.malbstl a{cursor:pointer;color:#fff}span.malbstl:active{background:#D73E00}span.malbstp{background:#3B3B3B;color:#686868}span.malbstu{color:#787878}span.mavtplay{bottom:0;font-size:11px;font-weight:bold;margin-left:3px;padding:1px 3px;position:absolute;right:0;text-align:right;text-decoration:none}div#tadsto .lbDescription .ac{color:#999}.uh_h,.uh_hp,.uh_hv{display:none;position:fixed;visibility:hidden}.uh_h {height:0px;left:0px;top:0px;width:0px;}.uh_hv{background:#fff;border:1px solid #ccc;-moz-box-shadow:0 4px 16px rgba(0,0,0,0.2);-webkit-box-shadow:0 4px 16px rgba(0,0,0,0.2);-ms-box-shadow:0 4px 16px rgba(0,0,0,0.2);box-shadow:0 4px 16px rgba(0,0,0,0.2);margin:-8px;padding:8px;background-color:#fff;visibility:visible}.uh_hp,.uh_hv,#uh_hp.v{display:block;z-index:5000}#uh_hp{-moz-box-shadow:0px 2px 4px rgba(0,0,0,0.2);-webkit-box-shadow:0px 2px 4px rgba(0,0,0,0.2);box-shadow:0px 2px 4px rgba(0,0,0,0.2);display:none;opacity:.7;position:fixed}#uh_hpl{cursor:pointer;display:block;height:100%;outline-color:-moz-use-text-color;outline-style:none;outline-width:medium;width:100%}.uh_hi {border:0;display:block;margin:0 auto 4px}.uh_hx {opacity:0.5}.uh_hx:hover {opacity:1}.uh_hn,.uh_hr,.uh_ht,.uh_ha{margin:0 1px -1px;padding-bottom:1px;overflow:hidden}.uh_ht{font-size:123%;line-height:120%;max-height:1.2em;word-wrap:break-word}.uh_hn{line-height:120%;max-height:2.4em}.uh_hr{color:#093;white-space:nowrap}.uh_ha{color:#777;white-space:nowrap}a.uh_hal{color:#36c;text-decoration:none}a:hover.uh_hal {text-decoration:underline}.speaker-icon-listen-off{background:url(//ssl.gstatic.com/dictionary/static/images/icons/1/pronunciation.png);opacity:0.55;filter:alpha(opacity=55);border:1px solid transparent;display:inline-block;float:none;height:16px;vertical-align:bottom;width:16px}.speaker-icon-listen-off:hover{opacity:1.0;filter:alpha(opacity=100);cursor:pointer;}.speaker-icon-listen-on{background:url(//ssl.gstatic.com/dictionary/static/images/icons/1/pronunciation.png);opacity:1.0;filter:alpha(opacity=100);border:1px solid transparent;display:inline-block;float:none;height:16px;vertical-align:bottom;width:16px}.speaker-icon-listen-on:hover{opacity:1.0;filter:alpha(opacity=100);cursor:pointer;}.coadlbal,.coadlbar{background:url(/images/nav_logo107.png) no-repeat}.coadlb{box-shadow:0 4px 16px rgba(0,0,0,0.2);-webkit-box-shadow:0 4px 16px rgba(0,0,0,0.2);outline:1px solid #ccc;background-color:#fff;display:none;padding:16px;position:absolute;z-index:120  }.coadlb{width: 210px;}.coadlbal{height:11px;position:absolute;width:17px;background-position:0 -212px;right:+19px;top:-11px}.coadlbar{height:11px;position:absolute;width:17px;background-position:-50px -212px;right:+6px;top:-11px}.coadpdl{font-size:.85em;text-decoration:none;}.coadpdl:hover,.coadpdl:active{text-decoration:underline;}.coadipb {border:1px solid #ccc;font-family:arial,sans-serif;font-size:11px;padding-left:4px;height:17px;}div.ofbb{background-color:#feaa26;background-image:-webkit-linear-gradient(top,#feaa26,#ff9f0c);border:1px solid #ff9a00}div.ofbb:hover{background-color:#fea71f;background-image:-webkit-linear-gradient(top,#fea71f,#f19301);border:1px solid #ea8e00}div#tads a:link,div#tads .w,div#tads .q:active,div#tads .q:visited,div#tads .tbotu,div#tads a.fl:link,div#tads .fl a,div#tads .flt,div#tads a.flt,div#tads .gl a:link,div#tads a.mblink,div#tads .mblink b,div#tadsto a:link,div#tadsto .w,div#tadsto .q:active,div#tadsto .q:visited,div#tadsto .tbotu,div#tadsto a.fl:link,div#tadsto .fl a,div#tadsto .flt,div#tadsto a.flt,div#tadsto .gl a:link,div#tadsto a.mblink,div#tadsto .mblink b,div#tadsb a:link,div#tadsb .w,div#tadsb .q:active,div#tadsb .q:visited,div#tadsb .tbotu,div#tadsb a.fl:link,div#tadsb .fl a,div#tadsb .flt,div#tadsb a.flt,div#tadsb .gl a:link,div#tadsb a.mblink,div#tadsb .mblink b{color:#0e1cb3}div#tads .a,div#tads cite,div#tads cite a:link,div#tads cite a:visited,div#tads .cite,div#tads .cite:link,div#tads #mbEnd cite b,div#tads cite b,div#tads #tadsto cite b,div#tads #ans>i,div#tadsto .a,div#tadsto cite,div#tadsto cite a:link,div#tadsto cite a:visited,div#tadsto .cite,div#tadsto .cite:link,div#tadsto #mbEnd cite b,div#tadsto cite b,div#tadsto #tadsto cite b,div#tadsto #ans>i,div#tadsb .a,div#tadsb cite,div#tadsb cite a:link,div#tadsb cite a:visited,div#tadsb .cite,div#tadsb .cite:link,div#tadsb #mbEnd cite b,div#tadsb cite b,div#tadsb #tadsbto cite b,div#tadsb #ans>i{color:#00802a}div#tads .s,div#tadsb .s,#tadsto .s,div#tads .ac,div#tadsb .ac,div#tadsto .ac{color:#171717}#sx{border:hidden;font-size:small;overflow:hidden}.sxcategory{margin:0 0 1em;padding:0 0 0.5em}.sxheader{margin-right:3em;padding:0 0 0.2em}.sxheader > h3{color:#000;font-size:15px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.sxconditions{border:0;margin:0;padding:0}.sxconditionsquery{font-weight:bold}.sxcondition{line-height:19px}.sxconditionterm{display:inline-block;line-height:1.2em;padding:0 13px;text-indent:-13px;width:11em}.sxconditiondefinition{display:inline-block;max-width:25em;overflow:hidden;text-overflow:ellipsis;vertical-align:top;white-space:nowrap}.sxconditionellipsis{display:none;padding:0 0 0 1px}.sxlink{color:#2200C1;cursor:pointer;text-decoration:none}.sxattribution{color:#666;font-size:11px;padding:0.3em 0 0.5em}.sxattributiondomain{color:#0E774A}.son:hover .soh{display:block;left: 0px;top: 24px}.bili {vertical-align:top;display:inline-block;overflow:hidden;margin-top:0px;margin-right:6px;margin-bottom:6px;margin-left:0px;}.bilir {margin:0px 0px 6px 0px;}.bia {display:block;}.rg_il,.rg_ilbg,.rg_ils{bottom:0;color:#fff;font-size:11px;line-height:100%;padding-right:1px;position:absolute}.rg_il,.rg_ilbg{right:0}.rg_ilbg{background:#000;opacity:0.4;z-index:0}.rg_il{z-index:1}.rg_ils{-webkit-border-top-right-radius:1px;-moz-border-radius-topright:1px;border-top-right-radius:1px;left:0;white-space:nowrap;z-index:1}.rg_ils div.f a{color:#fff!important}.rg_ils img{border:1px solid #333!important;margin:0!important}.rg_ils div.so_text{background:#333;color:#fff;font:normal 13px arial,sans-serif;padding:2px 4px;margin-left:0;opacity:0.8}div.so_text span.son{display:block;overflow:hidden;text-align:left;text-overflow:ellipsis;white-space:nowrap}.so_pl{float:right;font-style:italic;font-weight:bold}.irg{margin-bottom:10px;position:relative;width:100%}.irg h2{display:inline-block;font-size:16px;font-weight:normal;margin:0}.irg p{font-size:85%;margin:0}.irg-inner a{text-decoration:none}.irg-inner a:hover{text-decoration:underline}.irg-inner p{font-size:small;margin:0;padding-top:1px}.irg-column{display:inline-block;float:left;padding-right:16px;white-space:nowrap}.imrg{margin-bottom:26px;position:relative;width:100%}ul.lsnip{font-size:90%}.lsnip > li{overflow:hidden;text-overflow:ellipsis;-ms-text-overflow:ellipsis;-o-text-overflow:ellipsis;white-space:nowrap}table.tsnip{border-spacing:0;border-collapse:collapse;border-style:hidden;margin:2px 0 0}table.tsnip td,table.tsnip th{padding-bottom:0;padding-top:0;padding-right:10px;padding-left:0;margin:0;line-height:16px;text-align:left}table.tsnip th{color:#777;font-weight:normal}#rhs{display:block;left:0;margin-left:712px;padding-bottom:10px;position:absolute;right:0;top:0;min-width:268px;overflow:hidden;}#nyc{bottom:0;display:none;left:0;margin-left:663px;min-width:317px;overflow:hidden;position:fixed;right:0;visibility:visible}.vsvsn{left:200px;margin-top:3px;position:absolute}.vsvsnd{height:16px;padding-right:20px}.vsvsndon{background:transparent url(images/video/audio_icons.png) no-repeat scroll -57px 0}.vsvsndon:hover{background:transparent url(images/video/audio_icons.png) no-repeat scroll -38px 0}.vsvsndoff{background-image:url(images/video/audio_icons.png)}.vsvsndoff:hover{background:transparent url(images/video/audio_icons.png) no-repeat scroll -19px 0}#vsvsna:focus{outline:none}#leftnav div#lc{margin-left:8px}#leftnav #tbpi,#leftnav #swr{margin-left:16px}.mdm #nyc{margin-left:683px}.mdm #rhs{margin-left:732px}.big #nyc{margin-left:743px}.big #rhs{margin-left:792px}body .big #subform_ctrl{margin-left:229px}.rhscf{border:1px solid #eee;padding:0 15px 15px}.rhslink{width:68px}.rhsdw .rhslink{width:156px}.rhsimg{width:70px}.rhsimg.rhsdw{width:158px}.rhsimg.rhsn1st{margin-left:16px}.rhsvw{width:424px}.rhstc4 .rhsvw{width:336px}.rhstc3 .rhsvw{width:248px}.rhstc4 .rhsg4,.rhstc3 .rhsg4,.rhstc3 .rhsg3{background:none!important;display:none!important}.rhstc5 .rhsl5,.rhstc5 .rhsl4,.rhstc4 .rhsl4{background:none!important;display:none!important}.rhstc4 .rhsn4{background:none!important;display:none!important}.nrgt{margin-left:22px}.mslg .vsc{border:1px solid transparent;-webkit-border-radius:2px;-webkit-transition:opacity .2s ease;border-radius:2px;margin-top:2px;padding:3px 0 3px 5px;transition:opacity .2s ease;width:250px}.mslg>td{padding-right:6px;padding-top:4px}body .mslg .vso{border:1px solid #ebebeb;-webkit-box-shadow:0 1px 1px rgba(0,0,0,0.05);box-shadow:0 1px 1px rgba(0,0,0,0.05);opacity:1;-webkit-transition:0;transition:0}.mslg .vsc .vspib{bottom:1px;padding:0;right:0;top:-1px}#cnt .mslg .vsc .vspii{border-right:1px solid #dcdcdc}button.vspib{display:none}div.vspib{background:transparent;bottom:0;cursor:default;height:auto;margin:0;min-height:40px;padding-left:9px;padding-right:4px;position:absolute;right:-37px;top:-2px;width:28px;z-index:3}div.vspib:focus{outline:none}.taf div.vspib,.tas div.vspib{margin-top:14px}.vspii{visibility:hidden}.vspiic{background:url(/images/nav_logo107.png);background-position:-23px -260px;height:13px;margin-left:6px;margin-top:-7px;position:absolute;top:50%;width:15px}.nyc_open .vso .vspiic,.vspii:hover .vspiic{background-position:-3px -260px}.vsti{background:url(/images/nav_logo107.png);display:inline-block;height:9px;width:144px}.vstibtm{background-position:-2px -290px}.vstitop{background-position:-10px -299px}.vsta .vstibtm{background-position:-2px -309px}.vsta .vstitop{background-position:-10px -318px}#tads, #tadsto, #tadsb{width:512px}.nyc_open #nycx{background:url(/images/nav_logo107.png) no-repeat;background-position:-140px -230px;height:11px;width:11px}.vsc{display:inline-block;position:relative;width:100%}#nyc cite button.esw{display:none}button.esw{vertical-align:text-bottom}#res h3.r{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}#res h3.inl{display:inline;white-space:normal}.mbl{margin:1em 0 0}em{font-weight:bold;font-style:normal}li.w0 .ws,td.w0 .ws{opacity:0.5}li.w0:hover .ws,td.w0:hover .ws{opacity:1}ol,ul,li{border:0;margin:0;padding:0}li{line-height:1.2}li.g{margin-top:0;margin-bottom:20px}@media only screen and (min-height:590px){li.g{margin-bottom:23px}}.ibk,#productbox .fmg{display:inline-block;vertical-align:top}.tsw{width:595px}#cnt{margin-left:14px;min-width:833px;margin-left:0;padding-top:0;}.mw{max-width:1197px}.big .mw{max-width:1250px}#cnt #center_col,#cnt #foot,#cnt .ab_center_col{width:528px}.gbh{top:24px}#gbar{margin-left:8px;height:20px}#guser{margin-right:8px;padding-bottom:5px!important}.mbi{margin-bottom:-1px}.uc{margin-left:137px}#center_col,#foot{margin-left:132px;margin-right:254px;padding:0 8px;padding:0 8px 0 8px}.mdm #center_col,.mdm #foot{margin-left:152px;padding:0 8px}.big #center_col,.big #foot{margin-left:212px;padding:0 8px}#subform_ctrl{font-size:11px;min-height:19px;margin-right:480px;position:relative;z-index:99}#subform_ctrl a.gl{color:#12c}#center_col{clear:both}#brs p{margin:0;padding-top:5px}.brs_col{display:inline-block;float:left;font-size:small;white-space:nowrap;padding-right:16px;margin-top:-1px;padding-bottom:1px}#tads,#tadsb,#tadsto{margin-bottom:11px!important;z-index:0}#tads li,#tadsb li,#tadsto li{padding:1px 0}#tads li.taf,#tadsb li.taf,#tadsto li.taf{padding:1px 0 0}#tads li.tam,#tadsb li.tam,#tadsto li.tam{padding:20px 0 0}#tads li.tal,#tadsb li.tal,#tadsto li.tal{padding:20px 0 1px}@media only screen and (min-height:590px){#tads li.tam,#tadsb li.tam,#tadsto li.tam,#tads li.tal,#tadsb li.tal,#tadsto li.tal{padding-top:23px}}#res{border:0;margin:0;padding:0 8px}#ires{padding-top:6px}.mbl{margin-top:10px}.play_icon{background-position:;height:px;margin-left:64px;margin-top:44px;width:px}#leftnav li{display:block}.micon,.licon,.close_btn,.inline-close-btn{border:0}#leftnav h2{font-size:small;color:#767676;font-weight:normal;margin:8px 0 0 8px;padding-left:8px;width:124px}#tbbc dfn{padding:4px}#tbbc.bigger .std{font-size:154%;font-weight:bold;text-decoration:none}#tbbc .tbbclm{text-decoration:none}.close_btn{background-position:-138px -84px;float:right;height:14px;width:14px}.inline-close-btn{display:inline-block;vertical-align:text_bottom;background-position:-138px -84px;height:14px;width:14px}.videobox{padding-bottom:3px}#leftnav a{text-decoration:none}#leftnav a:hover{text-decoration:underline}.mitem,#showmodes{border-bottom:1px solid transparent;line-height:29px;opacity:1.0}.mitem .kl,#showmodes{padding-left:16px}.mitem .kl:hover,.msel .kls:hover,#showmodes:hover{opacity:1.0;background-color:#eee}#ms a:hover{text-decoration:none}.mitem>.kl,#ms>.kl{color:#222;display:block}.msel{color:#dd4b39;cursor:pointer}.msel .kls{border-left:5px solid #dd4b39;padding-left:11px}.mitem>.kl,#ms>.kl,.msel{font-size:13px}.licon{background-position:-153px -99px;float:left;height:14px;margin-right:3px;width:14px}.open .msm,.msl{display:none}.open .msl{display:inline}.open #hidden_modes,.open #hmp{display:block}#swr li{border:0;font-size:13px;line-height:1.2;margin:0 0 4px;margin-right:8px;}#tbd,#atd{display:block;min-height:1px}.tbt{font-size:13px;line-height:1.2}.tbnow{white-space:nowrap}.tbou,.tbos,.tbots,.tbotu{margin-right:8px;padding-left:16px;padding-bottom:3px;text-indent:-8px}.tbos,.tbots{font-weight:bold}#leftnav .tbots a{color:#000!important;cursor:default;text-decoration:none}.tbst{margin-top:8px}#season_{margin-top:8px}#iszlt_sel.tbcontrol_vis{margin-left:0}.tbpc,.tbpo,.lcso{font-size:13px}.tbpc,.tbo .tbpo{display:inline}.tbo .tbpc,.tbpo,.lco .lcso,.lco .lcot,#set_location_section{display:none}.lco #set_location_section{display:block}.lcot{display:block;margin:0 8px;}.tbo #tbp,.lco .licon,.obsmo #obsmti{background-position:-138px -99px!important}#prc_opt label,#prc_ttl{display:block;font-weight:normal;margin-right:2px;white-space:nowrap}#cdr_opt,#loc_opt,#prc_opt{padding-left:8px;text-indent:0}#prc_opt{margin-top:-20px}.tbou #cdr_frm,.tbou #cloc_frm{display:none}#cdr_frm,#cdr_min,#cdr_max{color:rgb(102, 102, 102);}#cdr_min,#cdr_max{font-family:arial,sans-serif;width:100%}#cdr_opt label{display:block;font-weight:normal;margin-right:2px;white-space:nowrap}.cdr_lbl{float:left;padding-top:5px}.cdr_hl{height:0;visibility:hidden}.cdr_inp{min-width:64px;overflow:hidden;padding-right:6px}.cdr_ctr{clear:both;overflow:hidden;padding:1px 0}.cdr_inp.cdr_hint{font-size:84%;font-weight:normal;min-width:70px;padding-bottom:2px;padding-right:0}.cdr_inp.cdr_btn{min-width:70px;padding-right:0}.cdr_err{color:red;font-size:84%;font-weight:normal}.rhss{margin:0 0 32px;margin-left:8px}#mbEnd{margin:5px 0 32px;margin-left:8px}#mbEnd{margin-left:16px;margin-top:2px}#mbEnd h2{color:#767676}#mbEnd li{margin:20px 8px 0 0}a:link,.w,.q:active,.q:visited,.tbotu{color:#12c;cursor:pointer}a.fl:link,.fl a,.flt,a.flt,.gl a:link,a.mblink,.mblink b{color:#12c}.osl a,.gl a,#tsf a,a.mblink,a.gl,a.fl,.slk a,.bc a,.flt,a.flt u,.oslk a,#tads .ac a,#tadsb .ac a,#rhs .ac a,.blg a,#appbar a{text-decoration:none}.osl a:hover,.gl a:hover,#tsf a:hover,a.mblink:hover,a.gl:hover,a.fl:hover,.slk a:hover,.bc a:hover,.flt:hover,a.flt:hover u,.oslk a:hover,.tbotu:hover,#tads .ac a:hover,#tadsb .ac a:hover,#rhs .ac a:hover,.blg a:hover{text-decoration:underline}#ss-box a:hover{text-decoration:none}#tads .mblink,#tadsb .mblink,#tadsto .mblink,#rhs .mblink{text-decoration:underline}.hpn,.osl{color:#777}div#gbi,div#gbg{border-color:#a2bff0 #558be3 #558be3 #a2bff0}div#gbi a.gb2:hover,div#gbg a.gb2:hover,.mi:hover{background-color:#558be3}#guser a.gb2:hover,.mi:hover,.mi:hover *{color:#fff!important}#guser{color:#000}#imagebox_big img{margin:5px!important}#imagebox_bigimages .th{border:0}#g_plus_products .th{border:0}#productbox .fmg{margin-top:7px;padding-right:4px;text-align:left}#productbox .lfmg{padding-right:0}#productbox .fmp,#productbox .fml,#productbox .fmm{padding-top:3px}.vsc:hover .lupin,.intrlu:hover .lupin,.lupin.luhovm{background-image:url('/images/red_pins2.png')!important;}.vsc:hover .lucir,.intrlu:hover .lucir,.lucir.luhovm{background-image:url('/images/red_circles2.png')!important;}.vsc:hover .luadpin,.intrlu:hover .luadpin,#mbEnd li:hover .luadpin,#tads li:hover .luadpin,#tadsb li:hover .luadpin,.luadpin.luhovm{background-image:url('/images/ad_blue_pins.png')!important;}#foot .ftl{margin-right:12px}#foot a.slink{text-decoration:none;color:#12c}#fll a,#bfl a{color:#12c;margin:0 12px;text-decoration:none}.kqfl #fll a{margin:0 24px 0 0!important}#foot a:hover{text-decoration:underline}#foot a.slink:visited{color:#61c}#blurbbox_bottom{color:#767676}.stp{margin:7px 0 17px}.ssp{margin:.33em 0 17px}#mss{margin:.33em 0 0;padding:0;display:table}.mss_col{display:inline-block;float:left;font-size:small;white-space:nowrap;padding-right:16px}#mss p{margin:0;padding-top:5px}#gsr a:active,a.fl:active,.fl a:active,.gl a:active{color:#dd4b39}body{color:#222}.s{color:#222}.s em{color:#000}.s a em{color:#12c}#tads .ac b,#tadsb .ac b,#rhs .ac b{color:#000}#tads .ac a b,#tadsb .ac a b,#rhs .ac a b{color:#12c}.s a:visited em{color:#61c}.s a:active em{color:#dd4b39}#tads .ac a:visited b,#tadsb .ac a:visited b,#rhs .ac a:visited b{color:#61c}#tads .ac a:active b,#tadsb .ac a:active b,#rhs .ac a:active b{color:#dd4b39}.sfcc{width:833px}.big .sfcc{max-width:1129px}.big #tsf{}#sform{height:33px!important}#topstuff .sp_cnt, #topstuff .ssp{padding-top:6px;}#topstuff .obp{padding-top:5px}#ires h3,#res h3,#tads h3,#tadsb h3,#mbEnd h3{font-size:medium}.nrtd li{margin:7px 0 0 0}.osl{margin-top:4px}.osi:before{background:url(/images/nav_logo107.png) -115px -244px;height:10px;width:10px;content:"";float:left;margin-right:5px;margin-left:1px;margin-top:2px}.slk{margin-top:6px!important}a.nlrl:link, a.nlrl:visited{color:#000}a.nlrl:hover, a.lrln:active{color:#12c}.st,.ac{line-height:1.24}.kv,.kvs,.slp{display:block;margin-bottom:1px}.kvs{margin-top:1px}.kt{border-spacing:2px 0;margin-top:1px}.esw{vertical-align:text-bottom}.cpbb,.kpbb,.kprb,.kpgb,.kpgrb,.ksb,.ab_button{-webkit-border-radius:2px;border-radius:2px;cursor:default!important;font-family:arial,sans-serif;font-size:11px;font-weight:bold;height:27px;line-height:27px;margin:2px 0;min-width:54px;padding:0 8px;text-align:center;-webkit-transition:all 0.218s;transition:all 0.218s;-webkit-user-select:none}.kbtn-small{min-width:26px;  width:26px}.ab_button.left{-webkit-border-radius:2px 0 0 2px;border-radius:2px 0 0 2px;border-right-color:transparent;margin-right:0}.ab_button.right{-webkit-border-radius:0 2px 2px 0;border-radius:0 2px 2px 0;margin-left:-1px}.ksb,.ab_button{background-color:#f5f5f5;background-image:-webkit-gradient(linear,left top,left bottom,from(#f5f5f5),to(#f1f1f1));background-image:-webkit-linear-gradient(top,#f5f5f5,#f1f1f1);background-image:linear-gradient(top,#f5f5f5,#f1f1f1);border:1px solid #dcdcdc;border:1px solid rgba(0, 0, 0, 0.1);color:#444}a.ksb,.div.ksb,a.ab_button{color:#444;text-decoration:none}.cpbb:hover,.kpbb:hover,.kprb:hover,.kpgb:hover,.kpgrb:hover,.ksb:hover,.ab_button:hover{-webkit-box-shadow:0 1px 1px rgba(0,0,0,0.1);box-shadow:0 1px 1px rgba(0,0,0,0.1);-webkit-transition:all 0.0s;transition:all 0.0s}.ksb:hover,.ab_button:hover{background-color:#f8f8f8;background-image:-webkit-gradient(linear,left top,left bottom,from(#f8f8f8),to(#f1f1f1));background-image:-webkit-linear-gradient(top,#f8f8f8,#f1f1f1);background-image:linear-gradient(top,#f8f8f8,#f1f1f1);border:1px solid #c6c6c6;color:#222}.ksb:active,.ab_button:active{background-color:#f6f6f6;background-image:-webkit-gradient(linear,left top,left bottom,from(#f6f6f6),to(#f1f1f1));background-image:-webkit-linear-gradient(top,#f6f6f6,#f1f1f1);background-image:linear-gradient(top,#f6f6f6,#f1f1f1);-webkit-box-shadow:inset 0 1px 2px rgba(0,0,0,0.1);box-shadow:inset 0 1px 2px rgba(0,0,0,0.1)}.ksb.ksbs,.ksb.ksbs:hover,.ab_button.selected,.ab_button.selected:hover{background-color:#eee;background-image:-webkit-gradient(linear,left top,left bottom,from(#eee),to(#e0e0e0));background-image:-webkit-linear-gradient(top,#eee,#e0e0e0);background-image:linear-gradient(top,#eee,#e0e0e0);border:1px solid #ccc;-webkit-box-shadow:inset 0 1px 2px rgba(0,0,0,0.1);box-shadow:inset 0 1px 2px rgba(0,0,0,0.1);color:#222;margin:0}.ksb.sbm{height:20px;line-height:18px;min-width:35px}.ksb.sbf{height:21px;line-height:21px;min-width:35px}.ksb.xlt{height:20px;line-height:21px;min-width:35px}.ksb.mini{-webkit-box-sizing:content-box;box-sizing:content-box;height:17px;line-height:17px;min-width:0}#comp-tool-block .ksb.unavail{background-image:-webkit-gradient(linear,left top,left bottom,from(#f5f5f5),to(#f1f1f1));background-image:-webkit-linear-gradient(top,#f5f5f5,#f1f1f1);background-color:#f5f5f5;background-image:linear-gradient(top,#f5f5f5,#f1f1f1);border:1px solid #dcdcdc;box-shadow:inset 0 1px 2px rgba(0,0,0,0.1);}#comp-tool-block .ksb, #comp-tool-block .kprb{color:#777;display:inline-block;font-size:10px;height:16px;line-height:16px;min-width:0;padding:0;text-decoration:none;width:26px;}#comp-tool-block .ksb:hover{color:#222;text-decoration:none;}#comp-tool-block .kprb:hover{text-decoration:none;}#comp-tool-block .kprb{background-color:#dd4b39;border:1px solid #dd4b39;color:#fff;}#comp-tool-block .ksb.unavail, #comp-tool-block .ksb.unavail:hover{background-image:none;box-shadow:none;color:#d5d5d5;}.ktf{-webkit-border-radius:1px;-webkit-box-sizing:content-box;background-color:#fff;border:1px solid #d9d9d9;border-top:1px solid #c0c0c0;box-sizing:content-box;color:#333;display:inline-block;height:29px;line-height:27px;padding-left:8px;vertical-align:top}.ktf:hover{-webkit-box-shadow:inset 0 1px 2px rgba(0,0,0,0.1);border:1px solid #b9b9b9;border-top:1px solid #a0a0a0;box-shadow:inset 0 1px 2px rgba(0,0,0,0.1)}.ktf:focus{-webkit-box-shadow:inset 0 1px 2px rgba(0,0,0,0.3);border:1px solid #4d90fe;box-shadow:inset 0 1px 2px rgba(0,0,0,0.3);outline:none}.ktf.mini{font-size:11px;height:17px;line-height:17px;padding:0 2px}.kcb{-webkit-appearance:none;-webkit-border-radius:1px;-webkit-box-sizing:border-box;width:13px;height:13px;border:1px solid #dcdcdc;margin:0;border-radius:1px;box-sizing:border-box;cursor:default;display:inline-block;position:relative;text-indent:0}.kcb:hover{-webkit-box-shadow:inset 0 1px 1px rgba(0,0,0,0.1);border-color:#c6c6c6;box-shadow:inset 0 1px 1px rgba(0,0,0,0.1)}.kcb:active{border-color:#c6c6c6;background:#ebebeb}.kcb.checked{backgrond-image:none}.kcb.checked::after{content:url(//ssl.gstatic.com/ui/v1/menu/checkmark.png);display:block;position:absolute;top:-6px;left:-5px}.kcb:focus{border-color:#4d90fe;outline:none}#sbfrm_l{visibility:inherit!important}#rcnt{margin-top:21px}#appbar{background:white;min-width:980px;position:relative;-webkit-box-sizing:border-box;width:100%;z-index:3}.ab_center_col{margin-top:-20px;padding-top:20px;text-align:right}.ab_center_col > span{display:inline-block}#ab_name{color:#dd4b39;font:20px "Arial";margin-left:15px;position:absolute;top:17px}#ab_name a{color:#999}#ab_ctls{position:relative;right:16px;float:right;top:14px;z-index:3}#sslock{background:url(images/srpr/safesearchlock_transparent.png) right top no-repeat;height:58px;position:absolute;right:0;top:0;width:260px;-webkit-user-select:none}#ab_ps_c{background-image:url(//ssl.gstatic.com/s2/oz/images/sprites/common-full-409360b9a97ad562fbe42ae2a97a5eaf.png);background-position:0 -94px;display:inline-block;float:left;height:17px;margin-right:3px;width:16px}#ab_ps_r{float:left;margin-left:5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.ab_ps_pic{margin-left:3px;margin-top:-4px;float:left}.ab_ps_pic img{border:0;height:24px;width:24px}.ab_rs_right{left:397px;position:absolute}.ab_ctl{display:inline-block;position:relative;margin-left:16px;vertical-align:top}a.ab_button,a.ab_button:visited{display:inline-block;color:#444;margin:0}a.ab_button:hover{color:#222}#appbar a.ab_button:active,a.ab_button.selected,a.ab_button.selected:hover{color:#333}.ab_button:focus{border:1px solid #4d90fe;outline:none}.ab_icon{background:url(/images/nav_logo107.png) no-repeat;display:inline-block;opacity:0.667;vertical-align:middle}.ab_button:hover > span.ab_icon{opacity:0.9}.ab_text{color:#666;font-size:13px;line-height:29px;margin:0 3px}#ab_loc_icon{background-position:-80px -192px;height:19px;width:19px}#ab_search_icon{background-position:-100px -192px;height:19px;width:19px}#ab_opt_icon{background-position:-42px -259px;height:17px;margin-top:-3px;width:17px}.ab_dropdown{background:#fff;border:1px solid #dcdcdc;border:1px solid rgba(0,0,0,0.2);font-size:13px;padding:0 0 6px;position:absolute;right:0;top:28px;white-space:nowrap;z-index:3;-webkit-transition:opacity 0.218s;transition:opacity 0.218s;-webkit-box-shadow:0 2px 4px rgba(0,0,0,0.2);box-shadow:0 2px 4px rgba(0,0,0,0.2)}.ab_dropdown:focus,.ab_dropdownitem:focus,.ab_dropdownitem a:focus{outline:none}.ab_dropdownitem{margin:0;padding:0;-webkit-user-select:none}.ab_dropdownitem.selected{background-color:#eee}.ab_dropdownitem.checked{background-image:url(//ssl.gstatic.com/ui/v1/menu/checkmark.png);background-position:left center;background-repeat:no-repeat}.ab_dropdownitem.disabled{cursor:default;border:1px solid #f3f3f3;border:1px solid rgba(0,0,0,0.05);pointer-events:none}a.ab_dropdownitem.disabled{color:#b8b8b8}.ab_dropdownitem.active{-webkit-box-shadow:inset 0 1px 2px rgba(0,0,0,0.1);box-shadow:inset 0 1px 2px rgba(0,0,0,0.1)}.ab_arrow{background:url(//ssl.gstatic.com/ui/v1/zippy/arrow_down.png);background-position:right center;background-repeat:no-repeat;display:inline-block;height:4px;margin-left:3px;margin-top:-3px;vertical-align:middle;width:7px}.ab_dropdownlnk,.ab_dropdownlnkinfo{display:block;padding:8px 20px 8px 16px}a.ab_dropdownlnk,a.ab_dropdownlnk:visited,a.ab_dropdownlnk:hover,#appbar a.ab_dropdownlnk:active{color:#333}a.ab_dropdownlnkinfo,a.ab_dropdownlnkinfo:visited,a.ab_dropdownlnkinfo:hover,#appbar a.ab_dropdownlnkinfo:active{color:#15c}.ab_dropdownchecklist{padding-left:30px}.ab_dropdownrule{border-top:1px solid #ebebeb;margin-bottom:10px;margin-top:9px}.tbt{margin-left:8px;margin-bottom:28px}#tbpi.pt.pi{margin-top:-20px}#tbpi.pi{margin-top:0}.tbo #tbpi.pt,.tbo #tbpi{margin-top:-20px}#tbpi.pt{margin-top:8px}#tbpi{margin-top:0}#tbrt{margin-top:-20px}.lnsep{border-bottom:1px solid #efefef;margin-bottom:14px;margin-left:10px;margin-right:4px;margin-top:14px}.tbos,.tbots,.tbotu{color:#dd4b39}#lc a,.tbou > a.q,#tbpi,#tbtro,.tbt label,#prc_opt,#set_location_section a,.tbtctlabel,#swr a{color:#222}.th{border:1px solid #ebebeb}#resultStats,.ab_center_col{color:#999;font-size:13px;margin-left:149px;position:absolute;top:23px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}#spn_nb{margin-left:149px;}.ab_center_col{margin-left:127px!important;}.mdm #resultStats,.mdm #spn_nb{margin-left:169px}.mdm .ab_center_col{margin-left:147px!important}.big #resultStats,.big #spn_nb{margin-left:229px}.big .ab_center_col{margin-left:207px!important}#leftnav{margin-left:0}#subform_ctrl{margin-left:149px}.mdm #leftnav{width:144px!important}.big #leftnav{width:204px!important}.big #subform_ctrl{padding-right:2px;margin-left:229px}.mdm .uc{margin-left:157px}.big .uc{margin-left:217px}.mdm #ab_name{margin-left:27px}.big #ab_name{margin-left:43px}.mdm #ab_ctls{right:28px;}.big #ab_ctls{right:44px;}.mdm #bms{margin-left:12px}.big #bms{margin-left:28px}.mdm .mitem .kl,.mdm #showmodes{padding-left:28px}.big .mitem .kl,.big #showmodes{padding-left:44px}.mdm .msel .kls{padding-left:23px}.big .msel .kls{padding-left:39px}.nbcl{background:url(/images/nav_logo107.png) no-repeat -140px -230px;height:11px;width:11px}.spra img{border:1px solid #ebebeb!important}.obsmo .dp0,.dp1,.rssmo .dp0{display:none}.obsmo .dp1,.rssmo .dp1{display:inline}#obsmtc a,.rscontainer a{text-decoration:none}#obsmtc a:hover .ul,.rscontainer a:hover .ul{text-decoration:underline}.authorship_attr{text-decoration:none;white-space:nowrap}.currency input[type=text]{background-color:white;border:1px solid #d9d9d9;border-top:1px solid #c0c0c0;box-sizing:border-box;color:#333;display:inline-block;height:29px;line-height:27px;padding-left:8px;vertical-align:top;-webkit-border-radius:1px;-webkit-box-sizing:border-box}.currency input[type=text]:hover{border:1px solid #b9b9b9;border-top:1px solid #a0a0a0;box-shadow:inset 0px 1px 2px rgba(0,0,0,0.1);-webkit-box-shadow:inset 0px 1px 2px rgba(0,0,0,0.1)}.currency input[type=text]:focus{border:1px solid #4d90fe;box-shadow:inset 0px 1px 2px rgba(0,0,0,0.3);outline:none;-webkit-box-shadow:inset 0px 1px 2px rgba(0,0,0,0.3)}</style>
<style>.lst-t{width:100%;}.kpbb,.kprb,.kpgb,.kpgrb{-webkit-border-radius:2px;border-radius:2px;color:#fff}.kpbb:hover,.kprb:hover,.kpgb:hover,.kpgrb:hover{-webkit-box-shadow:0 1px 1px rgba(0,0,0,0.1);box-shadow:0 1px 1px rgba(0,0,0,0.1);color:#fff}.kpbb:active,.kprb:active,.kpgb:active,.kpgrb:active{-webkit-box-shadow:inset 0 1px 2px rgba(0,0,0,0.3);box-shadow:inset 0 1px 2px rgba(0,0,0,0.3)}.kpbb{background-image:-webkit-gradient(linear,left top,left bottom,from(#4d90fe),to(#4787ed));background-image:-webkit-linear-gradient(top,#4d90fe,#4787ed);background-color:#4d90fe;background-image:linear-gradient(top,#4d90fe,#4787ed);border:1px solid #3079ed}.kpbb:hover{background-image:-webkit-gradient(linear,left top,left bottom,from(#4d90fe),to(#357ae8));background-image:-webkit-linear-gradient(top,#4d90fe,#357ae8);background-color:#357ae8;background-image:linear-gradient(top,#4d90fe,#357ae8);border:1px solid #2f5bb7}a.kpbb:link,a.kpbb:visited{color:#fff}.kprb{background-image:-webkit-gradient(linear,left top,left bottom,from(#dd4b39),to(#d14836));background-image:-webkit-linear-gradient(top,#dd4b39,#d14836);background-color:#dd4b39;background-image:linear-gradient(top,#dd4b39,#d14836);border:1px solid #dd4b39}.kprb:hover{background-image:-webkit-gradient(linear,left top,left bottom,from(#dd4b39),to(#c53727));background-image:-webkit-linear-gradient(top,#dd4b39,#c53727);background-color:#c53727;background-image:linear-gradient(top,#dd4b39,#c53727);border:1px solid #b0281a;border-color-bottom:#af301f}.kprb:active{background-image:-webkit-gradient(linear,left top,left bottom,from(#dd4b39),to(#b0281a));background-image:-webkit-linear-gradient(top,#dd4b39,#b0281a);background-color:#b0281a;background-image:linear-gradient(top,#dd4b39,#b0281a);}.kpgb{background-image:-webkit-gradient(linear,left top,left bottom,from(#3d9400),to(#398a00));background-image:-webkit-linear-gradient(top,#3d9400,#398a00);background-color:#3d9400;background-image:linear-gradient(top,#3d9400,#398a00);border:1px solid #29691d;}.kpgb:hover{background-image:-webkit-gradient(linear,left top,left bottom,from(#3d9400),to(#368200));background-image:-webkit-linear-gradient(top,#3d9400,#368200);background-color:#368200;background-image:linear-gradient(top,#3d9400,#368200);border:1px solid #2d6200}.kpgrb{background-image:-webkit-gradient(linear,left top,left bottom,from(#f5f5f5),to(#f1f1f1));background-image:-webkit-linear-gradient(top,#f5f5f5,#f1f1f1);background-color:#f5f5f5;background-image:linear-gradient(top,#f5f5f5,#f1f1f1);border:1px solid #dcdcdc;color:#555}.kpgrb:hover{background-image:-webkit-gradient(linear,left top,left bottom,from(#f8f8f8),to(#f1f1f1));background-image:-webkit-linear-gradient(top,#f8f8f8,#f1f1f1);background-color:#f8f8f8;background-image:linear-gradient(top,#f8f8f8,#f1f1f1);border:1px solid #dcdc;color:#333}a.kpgrb:link,a.kpgrb:visited{color:#555}#gbqfq{padding:1px 0 0 9px}#pocs{background:#fff1a8;color:#000;font-size:10pt;margin:0;padding:5px 7px 0px}#pocs.sft{background:transparent;color:#777}#pocs a{color:#11c}#pocs.sft a{color:#36c}#pocs > div{margin:0;padding:0}.gl{white-space:nowrap}.big .tsf-p{padding-left:220px;padding-right:260px}.tsf-p{padding-left:140px;padding-right:32px}.fade #center_col,.fade #rhs,.fade #leftnav{filter:alpha(opacity=33.3);opacity:0.333}.fade-hidden #center_col,.fade-hidden #rhs,.fade-hidden #leftnav{visibility:hidden}.flyr-o,.flyr-w{position:absolute;background-color:#fff;z-index:3;display:block}.flyr-o{filter:alpha(opacity=66.6);opacity:0.666;}.flyr-w{filter:alpha(opacity=20.0);opacity:0.2;}.flyr-h{filter:alpha(opacity=0);opacity:0}.flyr-c{display:none}.flt,.flt u,a.fl{text-decoration:none}.flt:hover,.flt:hover u,a.fl:hover{text-decoration:underline}#knavm{color:#4273db;display:inline;font:11px arial,sans-serif!important;left:-13px;position:absolute;top:2px;z-index:2}#pnprev #knavm{bottom:1px;top:auto}#pnnext #knavm{bottom:1px;left:40px;top:auto}a.noline{outline:0}</style>
<style> #searchform .jsb,#gbqfw .jsb{ display:none } #searchform .nojsb,#gbqfw .nojsb{ display:block } </style>
<style> .lst{padding-top:6px} </style>
<script>var _gjwl=location;function _gjuc(){var b=_gjwl.href.indexOf("#");if(b>=0){var a=_gjwl.href.substring(b+1);if(/(^|&)q=/.test(a)&&a.indexOf("#")==-1&&!/(^|&)cad=h($|&)/.test(a)){_gjwl.replace("/search?"+a.replace(/(^|&)fp=[^&]*/g,"")+"&cad=h");return 1}}return 0}function _gjp(){!(window._gjwl.hash&&window._gjuc())&&setTimeout(_gjp,500)};
function g(c){var d="undefined",a="1";if(c&&c.getElementById)if(typeof XMLHttpRequest!=d)a="2";else if(typeof ActiveXObject!=d){var b,e,f="MSXML2.XMLHTTP",h=[f+".6.0",f+".3.0",f,"Microsoft.XMLHTTP"];for(b=0,e;e=h[b++];)try{new ActiveXObject(e);a="2"}catch(i){}}return a};window.maybeRedirectForGBV=function(c,d,a){var b=g(c);if(b!=a)d.href="http://www.google.com/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&hl=en&prmd=ivns&ei=ihtzT62zBaaYiAfbjInkDw&start=140&sa=N&sei=wxxzT_2_DJG0iQeR0vjjDw&gbv="+b};
maybeRedirectForGBV(document,location,"2");window.rwt=function(a,f,g,l,m,h,c,n,i){return true};
(function(){try{var e=!0,i=!1;var aa=function(a,b,c,d){d=d||{};d._sn=["cfg",b,c].join(".");window.gbar.logger.ml(a,d)};var ba={G:1,I:2,Z:3,B:4,S:5,M:6,u:7,v:8,ca:9,R:10,L:11,z:12,Q:13,w:14,P:15,O:16,aa:17,D:18,N:19,ba:20,$:21,C:22,H:23,ea:24,fa:25,da:26,F:27,j:28,A:29,k:30,Y:31,U:32,V:33,J:34,K:35,X:36,W:37,T:38};var j=window.gbar=window.gbar||{},l=window.gbar.i=window.gbar.i||{};function _tvn(a,b){var c=parseInt(a,10);return isNaN(c)?b:c}function _tvf(a,b){var c=parseFloat(a);return isNaN(c)?b:c}function _tvv(a){return!!a}function m(a,b,c){(c||j)[a]=b}j.bv={n:_tvn("2",0),r:"r_gc.r_pw.r_qf.",f:".36.40.",m:_tvn("2",1)};var o=function(a){return function(){return j.bv.m==a}},ca=o(1),da=o(2);m("sb",ca);m("kn",da);l.a=_tvv;l.b=_tvf;l.c=_tvn;
l.i=aa;var p=window.gbar.i.i;var q={},ea={},r=[],fa=function(a,b){r.push([a,b])},ga=function(a,b){q[a]=b},ha=function(a){return a in q},t={},u=function(a,b){t[a]||(t[a]=[]);t[a].push(b)},v=function(a){u("m",a)},w=function(a){var b=document.createElement("script");b.src=a;(document.getElementById("xjsc")||document.body).appendChild(b)},A=function(a){for(var b=0,c;(c=r[b])&&!(c[0]==a);++b);c&&!c[1].l&&!c[1].s&&(c[1].s=e,x(2,a),c[1].url&&w(c[1].url),c[1].libs&&y&&y(c[1].libs))},B=function(a){u("gc",a)},C=null,ia=function(a){C=a},
x=function(a,b,c){if(C){a={t:a,b:b};if(c)for(var d in c)a[d]=c[d];try{C(a)}catch(g){}}};m("mdc",q);m("mdi",ea);m("bnc",r);m("qGC",B);m("qm",v);m("qd",t);m("lb",A);m("mcf",ga);m("bcf",fa);m("aq",u);m("mdd","");m("has",ha);m("trh",ia);m("tev",x);if(l.a("1")){var D=l.a("1"),ja=l.a(""),ka=window.gapi={},F=function(a,b){j.dgl===E&&m("dgl",F);u("gl",function(){j.dgl(a,b)});A("gl")},E=function(a,b){var c=a.split(":");G.l=G.l.concat(c.sort());b&&(G.cm=b,G.o=1,G.p=c);w(G.ms+G.h.split(";")[1].replace(/__features__/g,c.join(",").replace(/\.|-/g,"_")))},la={},ma=function(a){for(var a=a.split(":"),b;(b=a.pop())&&la[b];);return!b},y=function(a){function b(){for(var b=a.split(":"),d=0,g;g=b[d];++d)la[g]=
1;for(b=0;d=r[b];++b)d=d[1],(g=d.libs)&&!d.l&&d.i&&ma(g)&&d.i()}j.dgl(a,b)},G=window.___jsl={};G.h="m;/_/apps-static/_/js/widget/__features__/rt=j/ver=SvSTGk8PZnM.en./sv=1/am=!K2t8zmDaIyaNjPbXTQ/d=1/";G.ms="https://apis.google.com";G.m="";G.l=[];r.push(["gl",{url:"//ssl.gstatic.com/gb/js/abc/glm_2572388ad06f10d8fe6ef9a09f798c5d.js"}]);var na={"export":D};q.gl=na;D&&m("load",F,ka);var oa=!ja&&/^m;/.test(G.h)&&!/\/gapi\/|ms=gapi/.test(G.h)?E:F;m("dgl",oa);m("agl",ma)};var H=function(){},I=function(){},va=function(a){var b=new Image,c=ra;b.onerror=b.onload=b.onabort=function(){try{delete ua[c]}catch(a){}};ua[c]=b;b.src=a;ra=c+1},ua=[],ra=0;m("logger",{il:I,ml:H});var J=window.gbar.logger;var wa=l.b("0.001",1.0E-4),xa=0;
function _mlToken(a,b){try{if(1>xa){xa++;var c,d=a,g=b||{},f=encodeURIComponent,h=["//www.google.com/gen_204?atyp=i&zx=",(new Date).getTime(),"&jexpid=",f("37102"),"&srcpg=",f("prop=1"),"&jsr=",Math.round(1/wa),"&ogf=",j.bv.f,"&ogv=",f("1332297633.1332543369"),"&ogd=",f("com"),"&ogl=",f("en")];g._sn&&(g._sn="og."+g._sn);for(var n in g)h.push("&"),h.push(f(n)),h.push("="),h.push(f(g[n]));h.push("&emsg=");h.push(f(d.name+":"+d.message));var k=h.join("");ya(k)&&
(k=k.substr(0,2E3));c=k;var s=window.gbar.logger._aem(a,c);va(s)}}catch(z){}}var ya=function(a){return 2E3
<=a.length},za=function(a,b){return b};function Aa(a){H=a;m("_itl",ya,J);m("_aem",za,J);m("ml",H,J);a={};q.er=a}l.a("")?Aa(function(a){throw a;}):l.a("1")&&Math.random()
<wa&&Aa(_mlToken);var _E="left",L=function(a,b){var c=a.className;K(a,b)||(a.className+=(""!=c?" ":"")+b)},M=function(a,b){var c=a.className,d=RegExp("\\s?\\b"+b+"\\b");c&&c.match(d)&&(a.className=c.replace(d,""))},K=function(a,b){var c=RegExp("\\b"+b+"\\b"),d=a.className;return!(!d||!d.match(c))};m("ca",L);m("cr",M);m("cc",K);var Ba=["gb_71","gb_155"],N;function Ca(a){N=a}function Da(a){var b=N&&!a.href.match(/.*\/accounts\/ClearSID[?]/)&&encodeURIComponent(N());b&&(a.href=a.href.replace(/([?&]continue=)[^&]*/,"$1"+b))}function Ea(a){try{var b=(document.forms[0].q||"").value;b&&(a.href=a.href.replace(/([?&])q=[^&]*|$/,function(a,c){return(c||"&")+"q="+encodeURIComponent(b)}))}catch(c){p(c,"sb","pq")}}
var Fa=function(){for(var a=[],b=0,c;c=Ba[b];++b)(c=document.getElementById(c))&&a.push(c);return a},Ga=function(){var a=Fa();return 0
<a.length?a[0]:null},Ha=function(){return document.getElementById("gb_70")},O={},P={},Ia={},Q={},T=void 0,Na=function(a,b){try{var c=document.getElementById("gb");L(c,"gbpdjs");U();Ja(document.body)&&L(c,"gbrtl");if(b&&b.getAttribute){var d=b.getAttribute("aria-owns");if(d.length){var g=document.getElementById(d);if(g){var f=b.parentNode;if(T==d)T=void 0,M(f,"gbto");
else{if(T){var h=document.getElementById(T);if(h&&h.getAttribute){var n=h.getAttribute("aria-owner");if(n.length){var k=document.getElementById(n);k&&k.parentNode&&M(k.parentNode,"gbto")}}}Ka(g)&&La(g);T=d;L(f,"gbto")}}}}v(function(){j.tg(a,b,e)});Ma(a)}catch(s){p(s,"sb","tg")}},Oa=function(a){v(function(){j.close(a)})},Ja=function(a){var b,c="direction",d=document.defaultView;d&&d.getComputedStyle?(a=d.getComputedStyle(a,""))&&(b=a[c]):b=a.currentStyle?a.currentStyle[c]:a.style[c];return"rtl"==b},
Qa=function(a,b,c){if(a)try{var d=document.getElementById("gbd5");if(d){var g=d.firstChild,f=g.firstChild,h=document.createElement("li");h.className=b+" gbmtc";h.id=c;a.className="gbmt";h.appendChild(a);if(f.hasChildNodes()){for(var c=[["gbkc"],["gbf","gbe","gbn"],["gbkp"],["gbnd"]],d=0,n=f.childNodes.length,g=i,k=-1,s=0,z;z=c[s];s++){for(var pa=0,R;R=z[pa];pa++){for(;d
<n&&K(f.childNodes[d],R);)d++;if(R==b){f.insertBefore(h,f.childNodes[d]||null);g=e;break}}if(g){if(d+1
<f.childNodes.length){var qa=
f.childNodes[d+1];!K(qa.firstChild,"gbmh")&&!Pa(qa,z)&&(k=d+1)}else if(0
<=d-1){var sa=f.childNodes[d-1];!K(sa.firstChild,"gbmh")&&!Pa(sa,z)&&(k=d)}break}0
<d&&d+1
<n&&d++}if(0
<=k){var S=document.createElement("li"),ta=document.createElement("div");S.className="gbmtc";ta.className="gbmt gbmh";S.appendChild(ta);f.insertBefore(S,f.childNodes[k])}j.addHover&&j.addHover(a)}else f.appendChild(h)}}catch(cb){p(cb,"sb","al")}},Pa=function(a,b){for(var c=b.length,d=0;d
<c;d++)if(K(a,b[d]))return e;return i},Ra=
function(a,b,c){Qa(a,b,c)},Sa=function(a,b){Qa(a,"gbe",b)},Ta=function(){v(function(){j.pcm&&j.pcm()})},Ua=function(){v(function(){j.pca&&j.pca()})},Va=function(a,b,c,d,g,f,h,n,k,s){v(function(){j.paa&&j.paa(a,b,c,d,g,f,h,n,k,s)})},Wa=function(a,b){O[a]||(O[a]=[]);O[a].push(b)},Xa=function(a,b){P[a]||(P[a]=[]);P[a].push(b)},Ya=function(a,b){Ia[a]=b},Za=function(a,b){Q[a]||(Q[a]=[]);Q[a].push(b)},Ma=function(a){a.preventDefault&&a.preventDefault();a.returnValue=i;a.cancelBubble=e},V=null,La=function(a,
b){U();if(a){W(a,"Opening&hellip;");X(a,e);var c="undefined"!=typeof b?b:1E4,d=function(){$a(a)};V=window.setTimeout(d,c)}},ab=function(a){U();a&&(X(a,i),W(a,""))},$a=function(a){try{U();var b=a||document.getElementById(T);b&&(W(b,"This service is currently unavailable.%1$sPlease try again later.","%1$s"),X(b,e))}catch(c){p(c,"sb","sdhe")}},W=function(a,b,c){if(a&&b){var d=Ka(a);if(d){if(c){d.innerHTML="";for(var b=b.split(c),c=0,g;g=b[c];c++){var f=document.createElement("div");f.innerHTML=g;d.appendChild(f)}}else d.innerHTML=
b;X(a,e)}}},X=function(a,b){var c=void 0!==b?b:e;c?L(a,"gbmsgo"):M(a,"gbmsgo")},Ka=function(a){for(var b=0,c;c=a.childNodes[b];b++)if(K(c,"gbmsg"))return c},U=function(){V&&window.clearTimeout(V)};m("so",Ga);m("sos",Fa);m("si",Ha);m("tg",Na);m("close",Oa);m("addLink",Ra);m("addExtraLink",Sa);m("pcm",Ta);m("pca",Ua);m("paa",Va);m("ddld",La);m("ddrd",ab);m("dderr",$a);m("rtl",Ja);m("bh",O);m("abh",Wa);m("dh",P);m("adh",Xa);m("ch",Q);m("ach",Za);m("eh",Ia);m("aeh",Ya);m("qs",Ea);m("setContinueCb",Ca);
m("pc",Da);l.d=Ma;var bb={};q.base=bb;r.push(["m",{url:"//ssl.gstatic.com/gb/js/sem_8e56e5be46cb600be9ba1b375de5d016.js"}]);var db=l.c("1",0),eb=/\bgbmt\b/,fb=function(a){try{var b=document.getElementById("gb_"+db),c=document.getElementById("gb_"+a);b&&M(b,eb.test(b.className)?"gbm0l":"gbz0l");c&&L(c,eb.test(c.className)?"gbm0l":"gbz0l")}catch(d){p(d,"sj","ssp")}db=a},gb=j.qs,hb=function(a){var b;b=a.href;var c=window.location.href.match(/.*?:\/\/[^\/]*/)[0],c=RegExp("^"+c+"/search\\?");if((b=c.test(b))&&!/(^|\\?|&)ei=/.test(a.href))if((b=window.google)&&b.kEXPI)a.href+="&ei="+b.kEI},ib=function(a){gb(a);hb(a)};
m("slp",fb);m("qs",ib);m("qsi",hb);if(l.a("1")){var jb=l.a("");r.push(["gc",{auto:jb,url:"//ssl.gstatic.com/gb/js/abc/gci_78c17c085d1740ee894d9fec9ece5033.js",libs:"googleapis.client:plusone"}]);var kb={version:"gcm_f33b375e36e8c1fa70957777bf47af4a.js",index:"",lang:"en"};q.gc=kb;var Y=function(a){window.googleapis&&window.iframes?a&&a():(a&&B(a),A("gc"))};m("lGC",Y);l.a("1")&&m("lPWF",Y)};window.__PVT="";var lb=l.b("0.001",1.0E-4),mb=l.b("0.01",1),nb=i,ob=i;if(l.a("1")){var pb=Math.random();pb
<=lb&&(nb=e);pb
<=mb&&(ob=e)}var Z=ba;
function qb(a,b){var c=lb,d=nb,g;g=34>=a?a
<=Z.w?a==Z.u||a==Z.v||a==Z.z?i:e:a>=Z.j&&a
<=Z.k?e:i:200
<=a?e:i;g&&(c=mb,d=ob);if(d){d=encodeURIComponent;c=["//www.google.com/gen_204?atyp=i&zx=",(new Date).getTime(),"&oge=",a,"&ogex=",d("37102"),"&ogf=",j.bv.f,"&ogp=",d("1"),"&ogsr=",Math.round(1/c),"&ogv=",d("1332297633.1332543369"),"&ogd=",d("com"),"&ogl=",d("en")];if(b){"ogw"in b&&(c.push("&ogw="+b.ogw),delete b.ogw);var f;g=b;var h=[];for(f in g)0!=h.length&&
h.push(","),h.push(f),h.push("."),h.push(g[f]);f=h.join("");""!=f&&(c.push("&ogad="),c.push(d(f)))}va(c.join(""))}}I=qb;m("il",I,J);var rb={};q.il=rb;var sb=function(){j.prm&&j.prm()},tb=function(a){u("m",function(){j.spn(a)})},ub=function(a){u("m",function(){j.spp(a)})},vb=function(){u("m",function(){j.spd()})};m("spn",tb);m("spp",ub);m("spd",vb);Wa("gbd4",sb);if(l.a("")){var wb={g:l.a(""),d:l.a(""),e:"",m:"",p:"//ssl.gstatic.com/gb/images/avatar_b96.png",xp:l.a("1"),mg:"%1$s (delegated)",md:"%1$s (default)"};q.prf=wb};if(l.a("1")&&l.a("1")){var $=function(a){Y(function(){u("pw",a);A("pw")})};m("lPW",$);r.push(["pw",{url:"//ssl.gstatic.com/gb/js/abc/pwm_9f2309242efa34f253d8a3f7d8abb48c.js"}]);var xb=[],yb=function(a){xb[0]=a},zb=function(a,b){var c=b||{};c._sn="pw";H(a,c)},Ab={signed:xb,elog:zb,base:"https://plusone.google.com/u/0",loadTime:(new Date).getTime()};q.pw=Ab;var Bb=function(a,b){for(var c=b.split("."),d=function(){var b=arguments;a(function(){for(var a=j,d=0,f=c.length-1;d
<f;++d)a=a[c[d]];a[c[d]].apply(a,b)})},g=j,f=0,h=c.length-
1;f
<h;++f)g=g[c[f]]=g[c[f]]||{};return g[c[f]]=d};Bb($,"pw.clk");Bb($,"pw.hvr");m("su",yb,j.pw)};function Cb(){function a(){for(var b;(b=f[h++])&&!("m"==b[0]||b[1].auto););b&&(x(2,b[0]),b[1].url&&w(b[1].url),b[1].libs&&y&&y(b[1].libs));h
<f.length&&setTimeout(a,0)}function b(){0
<g--?setTimeout(b,0):a()}var c=l.a("1"),d=l.a(""),g=3,f=r,h=0,n=window.gbarOnReady;if(n)try{n()}catch(k){p(k,"ml","or")}d?m("ldb",a):c?window.addEventListener?window.addEventListener("load",b,i):window.attachEvent("onload",b):b()}m("rdl",Cb);}catch(e){window.gbar&&gbar.logger&&gbar.logger.ml(e,{"_sn":"cfg.init"});}})();
(function(){try{var b=window.gbar;var c=function(a,d){b[a]=function(){return window.navigator&&window.navigator.userAgent?d(window.navigator.userAgent):!1}},e=function(a){return!(/AppleWebKit\/.+(?:Version\/[35]\.|Chrome\/[01]\.)/.test(a)||-1!=a.indexOf("Firefox/3.5."))},f=function(a){return-1==a.indexOf("iPad")};c("bs_w",e);c("bs_s",f);}catch(e){window.gbar&&gbar.logger&&gbar.logger.ml(e,{"_sn":"cfg.init"});}})();
(function(){try{var a=window.gbar;a.mcf("sf",{});}catch(e){window.gbar&&gbar.logger&&gbar.logger.ml(e,{"_sn":"cfg.init"});}})();
(function(){try{var c=window.gbar;var e=c.i;var aa=window.gbar.i.i;var h,m,q=function(a,d){aa(a,"es",d)},r=function(a){return document.getElementById(a)},s=function(a,d){var g=Array.prototype.slice.call(arguments,1);return function(){var b=Array.prototype.slice.call(arguments);b.unshift.apply(b,g);return a.apply(this,b)}},u=void 0,v=void 0,w=void 0,ba=e.c("640"),ca=e.c("590"),da=e.c("1252"),ea=e.c("1060"),fa=e.c("995"),ga=e.c("851"),
x={},y={},z={},C={},D={};x.h=e.c("102");x.m=e.c("44");x.f=e.c("220");y.h=e.c("102");y.m=e.c("28");y.f=e.c("160");z.h=e.c("102");z.m=e.c("16");z.f=e.c("140");C.h=e.c("102");C.m=e.c("16");C.f=e.c("140");
D.h=e.c("102");D.m=e.c("12");D.f=e.c("136");
var G=e.c("16"),ha=e.c("572"),ia=e.c("434"),ja=e.c("319"),ka=e.c("572"),la=e.c("434"),ma=e.c("319"),na=e.c("220"),oa=e.c("160"),J=e.c("140"),pa=e.c("136"),
qa=e.c("15"),ra=e.c("15"),K=e.c("6"),sa=e.c("44"),ta=e.c("28"),L=e.c("16");e.c("12");var ua=e.c("15");e.a("1");
var va=e.c("980"),wa="gb,gbq,gbu,gbzw,gbpr,gbq2,gbqf,gbqff,gbq3,gbq1,gbqlw,gbql,gbmail,gbx1,gbx2,gbx3,gbx4,gbg1,gbg3,gbg4,gbd1,gbd3,gbd4,gbs,gbwc,gbprc".split(","),M=e.a(""),N=[],O=!0,Q=function(a){try{c.close(),"lg"==a?P(""):"md"==a?P("gbem"):"sm"==a?P("gbes"):"ty"==a?P("gbet"):"ut"==a&&P("gbeu")}catch(d){q(d,"stem")}},xa=s(Q,"lg"),ya=s(Q,"md"),za=s(Q,"sm"),Aa=s(Q,"ty"),Ba=s(Q,"ut"),U=function(a){try{Q(a);var d=R("Height"),g=R("Width"),b=x;"ut"==a?
b=D:"ty"==a?b=C:"sm"==a?b=z:"md"==a&&(b=y);S(d,g,a,b);T()}catch(n){q(n,"seme")}},Ca=function(a){try{N.push(a)}catch(d){q(d,"roec")}},V=function(){if(O)try{for(var a=0,d;d=N[a];++a)d(h)}catch(g){q(g,"eoec")}},Da=function(a){try{return O=a}catch(d){q(d,"ear")}},R=function(a){var d="inner"+a,a="offset"+a;return window[d]?window[d]:document.documentElement&&document.documentElement[a]?document.documentElement[a]:0},W=function(){var a=R("Height"),d=R("Width"),g=x,b="lg";if(d
<ga&&M)b="ut",g=D;else if(d
<fa&&M)b="ty",g=C;else if(d
<ea||a
<ca)b="sm",g=z;else if(d
<da||a
<ba)b="md",g=y;S(a,d,b,g);return b},T=function(){try{var a=r("gbx1");if(a){var d=c.rtl(document.body),g=a.clientWidth,a=g
<=va,b=r("gb_70");if(!u)if(b)u=b.clientWidth;else{var n=r("gbg6");if(n)u=n.clientWidth;else{var j=r("gbg4");if(j)u=j.clientWidth;else return}}if(!v){var p=r("gbg3");p&&(v=p.clientWidth)}var f=h.mo,n=sa,j=qa,k=na;"md"==f?(n=ta,j=ra,k=oa):"sm"==f?(n=L-G,j=K,k=J):"ty"==f?(n=L-G,j=K,k=J):"ut"==f&&(n=L-G,j=K,k=pa);var l=c.snw&&
c.snw();l&&(k+=l+j);var l=u,t=r("gbg1");t&&(l+=t.clientWidth+j);(p=r("gbg3"))&&(l+=v+j);var A=r("gbg4"),B=r("gbgs4dn");A&&!B&&(l+=A.clientWidth+j);var l=Math.min(304,l),k=k+n,H=r("gbqfbw");H&&(H.style.display="",k+=H.clientWidth+2*ua);var f=g-k,o=r("gbqf"),Y=r("gbqff"),i=c.gpcc&&c.gpcc();if(o&&Y&&!i){i=g-l-k;switch(m){case "ut":i=Math.min(i,ma);i=Math.max(i,ja);break;case "ty":i=Math.min(i,la);i=Math.max(i,ia);break;default:i=Math.min(i,ka),i=Math.max(i,ha)}o.style.maxWidth=i+"px";Y.style.maxWidth=
i+"px";f-=i}var E=r("gbi3");E&&((o=236>=f)?(o=d,w||(w=E.innerHTML),E.innerHTML="",o="padding"+(o?"Right":"Left"),E.style[o]="7px"):(o=d,w&&(E.innerHTML=w,o="padding"+(o?"Right":"Left"),E.style[o]="")));t&&(t.style.display="",f-=t.clientWidth+j);p&&(p.style.display="",f-=p.clientWidth+j);A&&!B&&(f-=A.clientWidth+j);var A=B?0:35,I=B||r("gbi4t");if(I&&!b){f>A?(I.style.display="",I.style.maxWidth=f+"px"):I.style.display="none";var Z=r("gbg6");Z&&(Z.style.width=f
<u&&f>A?f+"px":"");B="left";u>f^d&&(B="right");
I.style.textAlign=B}p&&0>f&&(f+=p.clientWidth,p.style.display="none");t&&0>f&&(f+=t.clientWidth,t.style.display="none");if(H&&(0>f||b&&f
<b.clientWidth))H.style.display="none";var b=d?"right":"left",d=d?"left":"right",F=r("gbu"),Ea=""!=F.style[b];a?(F.style[b]=g-F.clientWidth-n+"px",F.style[d]="auto"):(F.style[b]="",F.style[d]="");a!=Ea&&c.swsc&&c.swsc(a)}}catch(Fa){q(Fa,"cb")}},S=function(a,d,g,b){h={};h.mo=g;h.vh=a;h.vw=d;h.es=b;g!=m&&(V(),e.f&&e.f())},Ga=function(a){x.h+=a;y.h+=a;z.h+=a;C.h+=a;
D.h+=a},Ha=function(){return h},Ia=function(){try{if(!0==O){var a=m;m=W();if(a!=m)switch(m){case "ut":Ba();break;case "ty":Aa();break;case "sm":za();break;case "md":ya();break;default:xa()}}T()}catch(d){q(d,"sem")}},P=function(a){var d=r("gb");d&&(c.cr(d,""),c.cr(d,"gbemi"),c.cr(d,"gbesi"),c.cr(d,"gbeti"),c.cr(d,"gbeui"));for(var d=[],g=0,b;b=wa[g];g++)if(b=r(b))""==a&&(c.cr(b,"gbem"),c.cr(b,"gbes"),c.cr(b,"gbet"),c.cr(b,"gbeu"),c.ca(b,a)),"gbem"==a&&(c.cr(b,""),c.cr(b,"gbes"),c.cr(b,"gbet"),c.cr(b,
"gbeu"),c.ca(b,a)),"gbes"==a&&(c.cr(b,""),c.cr(b,"gbem"),c.cr(b,"gbet"),c.cr(b,"gbeu"),c.ca(b,a)),"gbet"==a&&(c.cr(b,""),c.cr(b,"gbem"),c.cr(b,"gbes"),c.cr(b,"gbeu"),c.ca(b,a)),"gbeu"==a&&(c.cr(b,""),c.cr(b,"gbem"),c.cr(b,"gbes"),c.cr(b,"gbet"),c.ca(b,a)),d.push(b);return d},$=function(){try{if(!0==O)switch(m=W(),m){case "ut":X("gbeui");break;case "ty":X("gbeti");break;case "sm":X("gbesi");break;case "md":X("gbemi");break;default:X("")}T()}catch(a){q(a,"semol")}},X=function(a){var d=r("gb");d&&c.ca(d,
a)};c.eli=$;c.elg=Ia;c.ell=s(U,"lg");c.elm=s(U,"md");c.els=s(U,"sm");c.elr=Ha;c.elc=Ca;c.elx=V;c.elh=Ga;c.ela=Da;c.elp=T;c.upel=s(U,"lg");c.upes=s(U,"md");c.upet=s(U,"sm");$();c.mcf("el",{});}catch(e){window.gbar&&gbar.logger&&gbar.logger.ml(e,{"_sn":"cfg.init"});}})();
(function(){try{var a=window.gbar;var d=function(){return document.getElementById("gbqfqw")},h=function(){return document.getElementById("gbqfq")},i=function(){return document.getElementById("gbqf")},j=function(){return document.getElementById("gbqfb")},l=function(b){var c=document.getElementById("gbqfaa");c.appendChild(b);k()},m=function(b){var c=document.getElementById("gbqfab");c.appendChild(b);k()},k=function(){var b=document.getElementById("gbqfqwb");if(b){var c=document.getElementById("gbqfaa"),e=document.getElementById("gbqfab");
if(c||e){var f="left",g="right";a.rtl(document.body)&&(f="right",g="left");c&&(b.style[f]=c.offsetWidth+"px");e&&(b.style[g]=e.offsetWidth+"px")}}},n=function(b){a.qm(function(){a.qfhi(b)})};a.qfgw=d;a.qfgq=h;a.qfgf=i;a.qfas=l;a.qfae=m;a.qfau=k;a.qfhi=n;a.qfsb=j;}catch(e){window.gbar&&gbar.logger&&gbar.logger.ml(e,{"_sn":"cfg.init"});}})();
(function(){try{var a=window.gbar;var d=window.gbar.i.i;var f="gbq1,gbq2,gbpr,gbqfbwa,gbx1,gbx2".split(","),h=!0,i=function(b){var c=document.getElementById("gbqld");if(c&&(c.style.display=b?"none":"block",c=document.getElementById("gbql")))c.style.display=b?"block":"none"},j=function(){try{for(var b=0,c;c=f[b];b++){var e=document.getElementById(c);e&&a.ca(e,"gbqfh")}h&&a.gpoas();a.elp&&a.elp();i(!0)}catch(g){d(g,"gas","ahcc")}},k=function(){try{for(var b=0,c;c=f[b];b++){var e=document.getElementById(c);e&&a.cr(e,"gbqfh")}h&&a.gpcas();a.elp&&a.elp();i(!1)}catch(g){d(g,
"gas","rhcc")}},l=function(b){var c=document.getElementById("gbq1");c&&(a[b](c,"gbto"),a[b](c,"gbtoc"))},m=function(){try{l("ca"),a.qm(function(){a.gpoas()})}catch(b){d(b,"gas","oas")}},n=function(){try{l("cr"),a.qm(function(){a.gpcas()})}catch(b){d(b,"gas","cas")}},o=function(){try{var b=document.getElementById(f[0]);return b&&a.cc(b,"gbqfh")}catch(c){d(c,"gas","ih")}};a.gpca=j;a.gpcr=k;a.gpcc=o;a.gpoas=m;a.gpcas=n;}catch(e){window.gbar&&gbar.logger&&gbar.logger.ml(e,{"_sn":"cfg.init"});}})();
(function(){try{var b=window.gbar;var c=window.gbar.i.i;var f=function(d){try{var a=document.getElementById("gbom");a&&d.appendChild(a.cloneNode(!0))}catch(e){c(e,"omas","aomc")}};b.aomc=f;}catch(e){window.gbar&&gbar.logger&&gbar.logger.ml(e,{"_sn":"cfg.init"});}})();
(function(){try{var a=window.gbar;a.mcf("pm",{p:""});}catch(e){window.gbar&&gbar.logger&&gbar.logger.ml(e,{"_sn":"cfg.init"});}})();
(function(){try{window.gbar.rdl();}catch(e){window.gbar&&gbar.logger&&gbar.logger.ml(e,{"_sn":"cfg.init"});}})();
</script> </head>
<body dir="ltr" lang="en" id="gsr">
<noscript>
<style> .jsb{ display:none } .nojsb{ display:block } .nojsv{ visibility:visible } </style></noscript>
<div id="pocs" style="display:none;position:absolute">
<div id="pocs0">
<span>
<span>Google</span> Instant is unavailable. Press enter to search.</span>
<a href="/support/websearch/bin/answer.py?answer=186645&amp;form=bb&amp;hl=en">Learn more</a></div>
<div id="pocs1">
<span>Google</span> Instant is off due to connection speed. Press Enter to search.</div>
<div id="pocs2">Press Enter to search.</div></div>
<div id="mngb">
<div id=gb>
<script>window.gbar&&gbar.eli&&gbar.eli()</script>
<div id=gbw>
<div id=gbzw>
<div id=gbz>
<span class=gbtcb></span>
<ol id=gbzc class=gbtc>
<li class=gbt>
<a onclick=gbar.logger.il(1,{t:119}); class=gbzt id=gb_119 href="https://plus.google.com/?gpsrc=ogpy0&tab=wX">
<span class=gbtb2></span>
<span class=gbts>+You</span></a></li>
<li class=gbt>
<a onclick=gbar.logger.il(1,{t:1}); class="gbzt gbz0l gbp1" id=gb_1 href="http://www.google.com/webhp?hl=en&tab=ww">
<span class=gbtb2></span>
<span class=gbts>Search</span></a></li>
<li class=gbt>
<a onclick=gbar.qs(this);gbar.logger.il(1,{t:2}); class=gbzt id=gb_2 href="http://www.google.com/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&hl=en&prmd=ivns&gbv=2&um=1&ie=UTF-8&tbm=isch&source=og&sa=N&tab=wi">
<span class=gbtb2></span>
<span class=gbts>Images</span></a></li>
<li class=gbt>
<a onclick=gbar.qs(this);gbar.logger.il(1,{t:8}); class=gbzt id=gb_8 href="http://maps.google.com/maps?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&hl=en&prmd=ivns&gbv=2&um=1&ie=UTF-8&sa=N&tab=wl">
<span class=gbtb2></span>
<span class=gbts>Maps</span></a></li>
<li class=gbt>
<a onclick=gbar.logger.il(1,{t:78}); class=gbzt id=gb_78 href="https://play.google.com/?hl=en&tab=w8">
<span class=gbtb2></span>
<span class=gbts>Play
<span class=gbsup>NEW</span></span></a></li>
<li class=gbt>
<a onclick=gbar.qs(this);gbar.logger.il(1,{t:36}); class=gbzt id=gb_36 href="http://www.youtube.com/results?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&hl=en&prmd=ivns&gbv=2&um=1&ie=UTF-8&sa=N&tab=w1">
<span class=gbtb2></span>
<span class=gbts>YouTube</span></a></li>
<li class=gbt>
<a onclick=gbar.logger.il(1,{t:5}); class=gbzt id=gb_5 href="http://news.google.com/nwshp?hl=en&tab=wn">
<span class=gbtb2></span>
<span class=gbts>News</span></a></li>
<li class=gbt>
<a onclick=gbar.logger.il(1,{t:23}); class=gbzt id=gb_23 href="https://mail.google.com/mail/?tab=wm">
<span class=gbtb2></span>
<span class=gbts>Gmail</span></a></li>
<li class=gbt>
<a onclick=gbar.logger.il(1,{t:25}); class=gbzt id=gb_25 href="https://docs.google.com/?tab=wo">
<span class=gbtb2></span>
<span class=gbts>Documents</span></a></li>
<li class=gbt>
<a onclick=gbar.logger.il(1,{t:24}); class=gbzt id=gb_24 href="https://www.google.com/calendar?tab=wc">
<span class=gbtb2></span>
<span class=gbts>Calendar</span></a></li>
<li class=gbt>
<a class=gbgt id=gbztm href="http://www.google.com/intl/en/options/" onclick="gbar.tg(event,this)" aria-haspopup=true aria-owns=gbd>
<span class=gbtb2></span>
<span id=gbztms class="gbts gbtsa">
<span id=gbztms1>More</span>
<span class=gbma></span></span></a>
<div class=gbm id=gbd aria-owner=gbztm>
<div class=gbmc>
<ol class=gbmcc>
<li class=gbmtc>
<a onclick=gbar.qs(this);gbar.logger.il(1,{t:51}); class=gbmt id=gb_51 href="http://translate.google.com/?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&hl=en&prmd=ivns&gbv=2&um=1&ie=UTF-8&sa=N&tab=wT">Translate</a></li>
<li class=gbmtc>
<a onclick=gbar.logger.il(1,{t:17}); class=gbmt id=gb_17 href="http://www.google.com/mobile/?tab=wD">Mobile</a></li>
<li class=gbmtc>
<a onclick=gbar.qs(this);gbar.logger.il(1,{t:10}); class=gbmt id=gb_10 href="http://www.google.com/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&hl=en&prmd=ivns&gbv=2&um=1&ie=UTF-8&tbo=u&tbm=bks&source=og&sa=N&tab=wp">Books</a></li>
<li class=gbmtc>
<a onclick=gbar.logger.il(1,{t:172}); class=gbmt id=gb_172 href="https://www.google.com/offers/home?utm_source=xsell&utm_medium=el&utm_campaign=sandbar&tab=wG#!details/">Offers</a></li>
<li class=gbmtc>
<a onclick=gbar.logger.il(1,{t:212}); class=gbmt id=gb_212 href="https://wallet.google.com/manage/?tab=wa">Wallet</a></li>
<li class=gbmtc>
<a onclick=gbar.qs(this);gbar.logger.il(1,{t:6}); class=gbmt id=gb_6 href="http://www.google.com/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&hl=en&prmd=ivns&gbv=2&um=1&ie=UTF-8&tbo=u&tbm=shop&source=og&sa=N&tab=wf">Shopping</a></li>
<li class=gbmtc>
<a onclick=gbar.logger.il(1,{t:30}); class=gbmt id=gb_30 href="http://www.blogger.com/?tab=wj">Blogger</a></li>
<li class=gbmtc>
<a onclick=gbar.logger.il(1,{t:32}); class=gbmt id=gb_32 href="http://www.google.com/reader/view/?hl=en&tab=wy">Reader</a></li>
<li class=gbmtc>
<a onclick=gbar.qs(this);gbar.logger.il(1,{t:27}); class=gbmt id=gb_27 href="http://www.google.com/finance?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&hl=en&prmd=ivns&gbv=2&um=1&ie=UTF-8&sa=N&tab=we">Finance</a></li>
<li class=gbmtc>
<a onclick=gbar.qs(this);gbar.logger.il(1,{t:31}); class=gbmt id=gb_31 href="http://picasaweb.google.com/lh/view?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&hl=en&prmd=ivns&gbv=2&um=1&ie=UTF-8&sa=N&tab=wq">Photos</a></li>
<li class=gbmtc>
<a onclick=gbar.qs(this);gbar.logger.il(1,{t:12}); class=gbmt id=gb_12 href="http://www.google.com/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&hl=en&prmd=ivns&gbv=2&um=1&ie=UTF-8&tbo=u&tbm=vid&source=og&sa=N&tab=wv">Videos</a></li>
<li class=gbmtc>
<div class="gbmt gbmh"></div></li>
<li class=gbmtc>
<a onclick=gbar.logger.il(1,{t:66}); href="http://www.google.com/intl/en/options/" class=gbmt>Even more</a></li></ol></div></div></li></ol></div></div>
<div id=gbq>
<div id=gbq1 class="gbt">
<div id=gbqlw class=gbgt>
<span id=gbql></span></div></div>
<div id=gbq2 class=gbt>
<div id=gbqfw class=gbqfr>
<form id=gbqf name=gbqf method=get action="/search" onsubmit="gbar.logger.il(31);">
<fieldset class=gbxx>
<legend class=gbxx>Hidden fields</legend>
<div id=gbqffd>
<input type=hidden name="hl" value="en">
<input type=hidden name="gbv" value="2">
<input type=hidden name="sclient" value="psy-ab"></div></fieldset>
<fieldset class=gbqff id=gbqff>
<legend class=gbxx></legend>
<div class="gbqfwa ">
<div id=gbqfqw class=gbqfqw>
<div id=gbqfqwb class=gbqfqwc>
<input id=gbqfq class=gbqfif name=q type=text autocomplete=off value="allintext: -error REMOTE_ADDR REQUEST_METHOD googlebot(at)googlebot.com HTTP_USER_AGENT HTTP_CONNECTION HTTP_HOST HTTP_REFERER HTTP_ACCEPT"></div></div></div></fieldset>
<div id=gbqfbw>
<button id=gbqfb aria-label="Google Search" class=gbqfb name=btnG>
<span class=gbqfi></span></button></div>
<div id=gbqfbwa class=jsb>
<button id=gbqfba aria-label="Google Search" name=btnK class="gbqfb gbqfba">
<span id=gbqfsa>Google Search</span></button>
<button id=gbqfbb aria-label="I'm Feeling Lucky" name=btnI class="gbqfb gbqfba" onclick="if(this.form.q.value)this.checked=1;else window.top.location='/doodles/'">
<span id=gbqfsb>I'm Feeling Lucky</span></button></div></form></div></div></div>
<div id=gbu>
<div id=gbvg class=gbvg>
<h2 class=gbxx>Account Options</h2>
<span class=gbtcb></span>
<ol class=gbtc>
<li class=gbt></li>
<li class=gbt>
<a href="https://accounts.google.com/ServiceLogin?hl=en&continue=http://www.google.com/search%3Fq%3Dallintext:%2B-error%2BREMOTE_ADDR%2BREQUEST_METHOD%2Bgooglebot(at)googlebot.com%2BHTTP_USER_AGENT%2BHTTP_CONNECTION%2BHTTP_HOST%2BHTTP_REFERER%2BHTTP_ACCEPT%26hl%3Den%26prmd%3Divns%26ei%3DihtzT62zBaaYiAfbjInkDw%26start%3D140%26sa%3DN%26sei%3DvxxzT_3bIKyyiQeXrIDkDw%26gbv%3D2" onclick="gbar.logger.il(9,{l:'i'})" id=gb_70 class=gbgt>
<span id=gbgs4>
<span id=gbi4t>Sign in</span></span></a></li>
<div style="display:none">
<div class=gbm id=gbd5 aria-owner=gbg5>
<div class=gbmc>
<ol id=gbom class=gbmcc>
<li class="gbkc gbmtc">
<a  class=gbmt href="/preferences?hl=en">Search settings</a></li>
<li class=gbmtc>
<div class="gbmt gbmh"></div></li>
<li class="gbe gbmtc">
<a  class=gbmt href="/history/optout?hl=en">Web History</a></li>
<li class="gbe gbmtc">
<a  id=gmlas class=gbmt href="/advanced_search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&hl=en&gbv=2">Advanced search</a></li></ol></div></div></div></ol></div></div></div>
<div id=gbx1 ></div>
<div id=gbx3></div>
<script>window.gbar&&gbar.elp&&gbar.elp()</script></div></div>
<script>if(google.j.b)document.body.style.display='none';</script>
<iframe src="/blank.html" onload="google.j.l()" onerror="google.j.e()" name="wgjf" style="display:none"></iframe>
<textarea name="csi" id="csi" style="display:none"></textarea>
<textarea name="wwcache" id="wwcache" style="display:none"></textarea>
<textarea name="wgjc" id="wgjc" style="display:none"></textarea>
<textarea name="hcache" id="hcache" style="display:none"></textarea>
<a href="/setprefs?prev=http://www.google.com/search%3Fq%3Dallintext:%2B-error%2BREMOTE_ADDR%2BREQUEST_METHOD%2Bgooglebot(at)googlebot.com%2BHTTP_USER_AGENT%2BHTTP_CONNECTION%2BHTTP_HOST%2BHTTP_REFERER%2BHTTP_ACCEPT%26hl%3Den%26prmd%3Divns%26ei%3DihtzT62zBaaYiAfbjInkDw%26start%3D140%26sa%3DN%26gbv%3D2&amp;sig=0_SzbvU4UwYxQq_aDNITX3eUvhGvs%3D&amp;suggon=2" style="left:-1000em;position:absolute">Screen reader users, click here to turn off Google Instant.</a>
<noscript>
<meta HTTP-EQUIV="refresh" content="0;url=http://www.google.com/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&hl=en&prmd=ivns&ei=ihtzT62zBaaYiAfbjInkDw&start=140&sa=N&gbv=1&sei=wxxzT_2_DJG0iQeR0vjjDw">
<style>
<!--
table,div,span,font,p{display:none}
--></style>
<div style="display:block">Please click
<a href="http://www.google.com/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&hl=en&prmd=ivns&ei=ihtzT62zBaaYiAfbjInkDw&start=140&sa=N&gbv=1&sei=wxxzT_2_DJG0iQeR0vjjDw">here</a> if you are not redirected within a few seconds.</div></noscript>
<div class="jsrp" id="searchform" style="display:none;top:50px">
<div class="sfbg nojsv" style="top:-20px">
<div class="sfbgg"></div>  </div>
<form action="/search" id="tsf" method="GET" onsubmit="return q.value!=''" role="search" name="f" style="display:block;background:none">
<input value="psy-ab" name="sclient" type="hidden"/>
<span id="tophf">
<input type=hidden name=hl value="en">
<input type=hidden name=gbv value="2">  </span>
<div class="tsf-p" style="position:relative">
<div class="nojsv" id="logocont" style="left:0;position:absolute;padding:">
<h1>
<a id=logo href="http://www.google.com/webhp?hl=en" title="Go to Google Home">Google
<img width=167 height=389 src="/images/nav_logo107.png" alt=""></a></h1></div>
<div style="padding-bottom:2px;padding-top:3px">
<table border="0" cellpadding="0" cellspacing="0" width="100%">
<tr>
<td width="100%">
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="position:relative;border-bottom:1px solid transparent">
<tr>
<td class="lst-td" id="sftab" width="100%" style="border:0">
<div class="lst-d lst-tbb">
<input class="lst lst-tbb" value="allintext: -error REMOTE_ADDR REQUEST_METHOD googlebot(at)googlebot.com HTTP_USER_AGENT HTTP_CONNECTION HTTP_HOST HTTP_REFERER HTTP_ACCEPT" title="Search" size="41" type="text" autocomplete="off" id="lst-ib" name="q" maxlength="2048"/>
<span id="tsf-oq" style="display:none">allintext: -error REMOTE_ADDR REQUEST_METHOD googlebot(at)googlebot.com HTTP_USER_AGENT HTTP_CONNECTION HTTP_HOST HTTP_REFERER HTTP_ACCEPT</span> </div> </td>
<td>
<div class="nojsb">
<div class="ds" id="sbds">
<div class="lsbb kpbb" id="sblsbb">
<button class="lsb" value="Search" type="submit" name="btnG">
<span class="sbico"></span> </button> </div> </div> </div> </td> </tr> </table> </td>
<td>
<div class="nojsv" id="sfopt" style="height:30px;position:relative">
<div class="lsd">
<div id=ss-bar style=white-space:nowrap;z-index:98></div>   </div> </div> </td> </tr>
<tr>
<td>
<div id="pocs" style="display:none">
<div id="pocs0">
<span>
<span>Google</span> Instant is unavailable. Press enter to search. </span>
<a href="/support/websearch/bin/answer.py?answer=186645&amp;form=bb&amp;hl=en">Learn more</a> </div>
<div id="pocs1">
<span>Google</span> Instant is off due to connection speed. Press Enter to search. </div>
<div id="pocs2">Press Enter to search.</div> </div>
<div id="pets" style="color:#767676;display:none;font-size:9pt;margin:5px 0 0 8px">Press Enter to search.</div> </td> </tr> </table> </div>
<div class="jsb" style="padding-top:2px">
<center>
<input value="Google Search" name="btnK" type="submit" onclick="this.checked=1"/>
<input value="I'm Feeling Lucky" name="btnI" type="submit" onclick="if(this.form.q.value)this.checked=1; else top.location='/doodles/'"/> </center> </div> </div> </form> </div>
<div id="gac_scont"></div>
<div id="main">
<div>
<div id="cnt">
<script>(function(){var _j=1250;var _t=false;var _tl=847;var _th=980;try{var _c=document.getElementById('cnt');var _s=document.getElementById('searchform');var _w=document['body']&&document.body['offsetWidth'];var _n='';if(gbar.elr){var _m=gbar.elr().mo;_n=(_m=='md'?' mdm':(_m=='lg'?' big':''));}else{if(_w&&_w>=_j){_n=' big';}
}
if (_t&&_w&&_w
<_th){_n=_w
<_tl?' tmlo':' tmhi';}
_c&&(_c.className+=_n);_s&&(_s.className+=_n);}catch(e){}})();</script>
<div class="mw">
<div id="sfcnt" style="display:none">
<div id="sform" style="height:36px"></div>
<div class="tsf-p" style="visibility:hidden">
<span style="float:left"></span></div></div>
<div id="srchdsc"></div>
<div id="sdb">   </div>
<div id="subform_ctrl" style="display:none"></div></div>
<div id="appbar">
<div style="border-bottom:1px solid #dedede;height:57px">
<div id="ab_name">
<span id="ab_label">
<span>Search</span></span></div>
<div>
<div id=resultStats>Page 15 of about 4,230,000 results
<nobr>  (0.12 seconds)&nbsp;</nobr></div></div>
<ol id="ab_ctls">
<li class="ab_ctl" id="ab_ctl_opt">
<a class="ab_button" href="/preferences?hl=en" id="abar_button_opt" unselectable="on" onclick="return google.x(this,(function(event){ return function(){google.kennedy.toggleDropdown(event)} })(event))" role="button" aria-expanded="false" aria-haspopup="true" tabindex="0">
<span class="ab_icon" title="Options" id="ab_opt_icon" unselectable="on"></span></a>
<div class="ab_dropdown" onclick="google.util.stopPropagation(event)" id="ab_options" role="menu" tabindex="-1" style="visibility:hidden">
<ul>
<li class="ab_dropdownitem" role="menuitem" aria-selected="false">
<a class="ab_dropdownlnk" href="/preferences?hl=en" tabindex="-1">
<div>Search settings</div></a></li>
<li class="ab_dropdownitem" role="menuitem" aria-selected="false">
<a class="ab_dropdownlnk" href="/advanced_search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns" id="ab_as" tabindex="-1">
<div>Advanced search</div></a></li>
<li class="ab_dropdownitem" role="menuitem" aria-selected="false">
<a class="ab_dropdownlnk" href="/history/optout?hl=en" tabindex="-1">
<div>Web History</div></a></li>
<li class="ab_dropdownitem" role="menuitem" aria-selected="false">
<a class="ab_dropdownlnk" href="//www.google.com/support/websearch/?source=g&amp;hl=en" tabindex="-1">
<div>Search Help</div></a></li></ul></div></li>
<script>var gear = document.getElementById('gbg5');var opt = document.getElementById('ab_ctl_opt');if (opt){opt.style.display = gear ?'none' :'inline-block';}
</script></ol></div></div>
<div class="mw" id="ucs"></div>
<div class="mw">
<div id="arcntc"></div>
<div id="rcnt" style="clear:both;position:relative;zoom:1">
<div id="leftnavc">
<div id="leftnav" role="navigation" onclick="google.psy&amp;&amp;google.psy.qs(event)" style="position:absolute;top:1px;width:132px">
<div id=ms>
<ul>
<li class="mitem msel">
<div class="kls">Everything</div></li>
<li class="mitem">
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;source=lnms&amp;tbm=isch&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=mode_link&amp;ct=mode&amp;cd=2&amp;ved=0CAsQ_AUoATiMAQ" class="kl">Images</a></li>
<li class="mitem">
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;source=lnms&amp;tbm=vid&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=mode_link&amp;ct=mode&amp;cd=3&amp;ved=0CAwQ_AUoAjiMAQ" class="kl">Videos</a></li>
<li class="mitem">
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;source=lnms&amp;tbm=nws&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=mode_link&amp;ct=mode&amp;cd=4&amp;ved=0CA0Q_AUoAziMAQ" class="kl">News</a></li>
<li class="mitem">
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;source=lnms&amp;tbm=shop&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=mode_link&amp;ct=mode&amp;cd=5&amp;ved=0CA4Q_AUoBDiMAQ" class="kl">Shopping</a></li></ul>
<ul class=nojsb  id="hidden_modes">
<li class="mitem">
<a href="http://maps.google.com/maps?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;prmd=ivns&amp;gbv=2&amp;um=1&amp;ie=UTF-8&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=mode_link&amp;ct=mode&amp;cd=2&amp;ved=0CA8Q_AUoATiMAQ" class="kl">Maps</a></li>
<li class="mitem">
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;source=lnms&amp;tbm=bks&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=mode_link&amp;ct=mode&amp;cd=3&amp;ved=0CBAQ_AUoAjiMAQ" class="kl">Books</a></li>
<li class="mitem">
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;source=lnms&amp;tbm=plcs&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=mode_link&amp;ct=mode&amp;cd=4&amp;ved=0CBEQ_AUoAziMAQ" class="kl">Places</a></li>
<li class="mitem">
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;source=lnms&amp;tbm=blg&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=mode_link&amp;ct=mode&amp;cd=5&amp;ved=0CBIQ_AUoBDiMAQ" class="kl">Blogs</a></li>
<li class="mitem">
<a href="http://www.google.com/flights/gwsredirect?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;source=lnms&amp;tbm=flm&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=mode_link&amp;ct=mode&amp;cd=6&amp;ved=0CBMQ_AUoBTiMAQ" class="kl">Flights</a></li>
<li class="mitem">
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;source=lnms&amp;tbm=dsc&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=mode_link&amp;ct=mode&amp;cd=7&amp;ved=0CBQQ_AUoBjiMAQ" class="kl">Discussions</a></li>
<li class="mitem">
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;source=lnms&amp;tbm=rcp&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=mode_link&amp;ct=mode&amp;cd=8&amp;ved=0CBUQ_AUoBziMAQ" class="kl">Recipes</a></li>
<li class="mitem">
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;source=lnms&amp;tbm=app&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=mode_link&amp;ct=mode&amp;cd=9&amp;ved=0CBYQ_AUoCDiMAQ" class="kl">Applications</a></li>
<li class="mitem">
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;source=lnms&amp;tbm=pts&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=mode_link&amp;ct=mode&amp;cd=10&amp;ved=0CBcQ_AUoCTiMAQ" class="kl">Patents</a></li></ul>
<a href="#" id=showmodes class="jsb nj kl" onclick="google.x(this.id,function(){google.srp.toggleModes()});google.log('', '\x26ved\x3d0CAkQ_gU4jAE' +'&ei=' + google.kEI);return false">
<span class="msm">More</span>
<span class="msl">Fewer</span></a></div>
<div id="bms">
<div class="lnsep"></div>
<div style="clear:both;overflow:hidden">
<h2 class=hd>Search Options</h2>
<ul id=tbd class="med">
<li class=jsb style='display:none'>
<ul class="tbt"></ul>
<li class=jsb style='display:none'>
<ul class="tbt"></ul></ul>
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;start=140&amp;hl=en&amp;sa=N&amp;gbv=2&amp;prmd=ivns&amp;tbo=1" class="nj q pi" id=tbpi onclick="return google.x(this,function(){return google.Toolbelt.togglePromotedTools('0CAcQwxE4jAE')});" style="clear:both;display:block;">
<span class=tbpo>Hide search tools</span>
<span class=tbpc>Show search tools</span></a></div></div></div></div>
<div id="center_col">
<span id="taw" style="margin-right:0">
<div></div>     </span>
<div class="med" id="res" role="main">
<div id="topstuff">        </div>
<div id="search">
<!--a-->
<h2 class="hd">Search Results</h2>
<div id="ires">
<ol eid="wxxzT_2_DJG0iQeR0vjjDw" id="rso">
<!--m-->
<li class="g">
<div class="vsc" pved="0CB4QkgowADiMAQ" bved="0CB8QkQo4jAE" sig="vuX">
<h3 class="r">
<a href="http://www.sg-as.ru/myip" class=l onmousedown="return rwt(this,'','','','141','AFQjCNGaxQ39uvqrikSmm2GGXK75dWw7Cg','','0CCQQFjAAOIwB',null,event)">подробнее - Стерлинг Групп А.С.</a></h3>
<div class="s">
<div class="f kv">
<cite>www.sg-as.ru/myip</cite>
<span class="gl"> -
<a href="http://webcache.googleusercontent.com/search?q=cache:fAyGKgF5gcIJ:www.sg-as.ru/myip+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;cd=141&amp;hl=en&amp;ct=clnk" onmousedown="return rwt(this,'','','','141','AFQjCNH5HAIK9YdiMC4ImJPFBo-gmM1RWA','','0CCEQIDAAOIwB',null,event)">Cached</a></span>
<span class="std">&nbsp;
<span class=gl>-</span>
<a href="http://translate.google.com/translate?hl=en&amp;sl=ru&amp;u=http://www.sg-as.ru/myip&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=translate&amp;ct=result&amp;resnum=1&amp;ved=0CCIQ7gEwADiMAQ&amp;prev=/search%3Fq%3Dallintext:%2B-error%2BREMOTE_ADDR%2BREQUEST_METHOD%2Bgooglebot(at)googlebot.com%2BHTTP_USER_AGENT%2BHTTP_CONNECTION%2BHTTP_HOST%2BHTTP_REFERER%2BHTTP_ACCEPT%26start%3D140%26hl%3Den%26sa%3DN%26gbv%3D2%26prmd%3Divns" class=fl>Translate this page</a></span></div>
<div class="esc slp" id="poS140" style="display:none">You +1'd this publicly.&nbsp;
<a href="#" class="fl">Undo</a></div>
<span class="f">15+ items &ndash; </span>
<span class="st"><b>...</b> (HostName): crawl-66-249-72-83.<em>googlebot.com</em>. Проверить <b>...</b>
<br></span>
<table class="tsnip">
<tbody>
<tr>
<td>Переменные сервера (Server Variables)
<td>Значения (Values)
<tr>
<td>ALL_RAW
<td>Connection: Keep-alive Content ...</table></div></div>
<!--n--></li>
<!--m-->
<li class="g">
<div class="vsc" pved="0CCcQkgowATiMAQ" bved="0CCgQkQo4jAE" sig="FC_">
<h3 class="r">
<a href="http://shop.tut.by/out/?m=b&amp;i=22231643&amp;s=1" class=l onmousedown="return rwt(this,'','','','142','AFQjCNF5SmsGb8vRL9I3UT0L2ZlTfOChzg','','0CC0QFjABOIwB',null,event)">Ошибка 404</a></h3>
<div class="s">
<div class="f kv">
<cite>shop.tut.by/out/?m=b&amp;i=22231643...</cite>
<span class="gl"> -
<a href="http://webcache.googleusercontent.com/search?q=cache:2Hbk1oxdf9UJ:shop.tut.by/out/%3Fm%3Db%26i%3D22231643%26s%3D1+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;cd=142&amp;hl=en&amp;ct=clnk" onmousedown="return rwt(this,'','','','142','AFQjCNHTHQKqxBDKDRHsz7bJWs8CJ3Gm4g','','0CCoQIDABOIwB',null,event)">Cached</a></span>
<span class="std">&nbsp;
<span class=gl>-</span>
<a href="http://translate.google.com/translate?hl=en&amp;sl=ru&amp;u=http://shop.tut.by/out/%3Fm%3Db%26i%3D22231643%26s%3D1&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=translate&amp;ct=result&amp;resnum=2&amp;ved=0CCsQ7gEwATiMAQ&amp;prev=/search%3Fq%3Dallintext:%2B-error%2BREMOTE_ADDR%2BREQUEST_METHOD%2Bgooglebot(at)googlebot.com%2BHTTP_USER_AGENT%2BHTTP_CONNECTION%2BHTTP_HOST%2BHTTP_REFERER%2BHTTP_ACCEPT%26start%3D140%26hl%3Den%26sa%3DN%26gbv%3D2%26prmd%3Divns" class=fl>Translate this page</a></span></div>
<div class="esc slp" id="poS141" style="display:none">You +1'd this publicly.&nbsp;
<a href="#" class="fl">Undo</a></div>
<span class="st">Ошибка: Undefined index: <em>HTTP_REFERER</em> в файле <b>...</b> &#39;<em>HTTP_ACCEPT</em>&#39; =&gt; &#39;*/*&#39;, &#39;HTTP_ACCEPT_ENCODING&#39; =&gt; &#39;gzip,deflate&#39;, &#39;<em>HTTP_CONNECTION</em>&#39; =&gt; &#39;close&#39;, &#39;<wbr>HTTP_FROM&#39; =&gt; &#39;<em>googlebot</em>(<em>at</em>)<em>googlebot.com</em>&#39;, &#39;<em>HTTP_HOST</em>&#39; =&gt; &#39;shop.tut.by&#39;, &#39;<wbr><em>HTTP_USER_AGENT</em>&#39; =&gt; &#39;Mozilla/5.0 (compatible; <em>Googlebot</em>/2.1; <b>...</b>
<br></span></div></div>
<!--n--></li>
<!--m-->
<li class="g">
<div class="vsc" pved="0CC8QkgowAjiMAQ" bved="0CDAQkQo4jAE" sig="yTT">
<h3 class="r">
<a href="http://wwwkusi.freehost.pl/env-php.php" class=l onmousedown="return rwt(this,'','','','143','AFQjCNHNkomI2J_8W9LA0efCwdGbSE0xmg','','0CDUQFjACOIwB',null,event)">top $_SERVER Array ( [DOCUMENT_ROOT] =&gt; /ww1/htdocs <b>...</b></a></h3>
<>
<div class="s">
<div class="f kv">
<cite>wwwkusi.freehost.pl/env-php.php</cite>
<span class="gl"> -
<a href="http://webcache.googleusercontent.com/search?q=cache:Er0XEKSiyrcJ:wwwkusi.freehost.pl/env-php.php+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;cd=143&amp;hl=en&amp;ct=clnk" onmousedown="return rwt(this,'','','','143','AFQjCNHHHmEKo0VLKld5E5kRaZMtkzEMBQ','','0CDIQIDACOIwB',null,event)">Cached</a></span>
<span class="std">&nbsp;
<span class=gl>-</span>
<a href="http://translate.google.com/translate?hl=en&amp;sl=ja&amp;u=http://wwwkusi.freehost.pl/env-php.php&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=translate&amp;ct=result&amp;resnum=3&amp;ved=0CDMQ7gEwAjiMAQ&amp;prev=/search%3Fq%3Dallintext:%2B-error%2BREMOTE_ADDR%2BREQUEST_METHOD%2Bgooglebot(at)googlebot.com%2BHTTP_USER_AGENT%2BHTTP_CONNECTION%2BHTTP_HOST%2BHTTP_REFERER%2BHTTP_ACCEPT%26start%3D140%26hl%3Den%26sa%3DN%26gbv%3D2%26prmd%3Divns" class=fl>Translate this page</a></span></div>
<div class="esc slp" id="poS142" style="display:none">You +1'd this publicly.&nbsp;
<a href="#" class="fl">Undo</a></div>
<span class="f">40+ items &ndash; </span>
<span class="st"><b>...</b> [HTTP_FROM] =&gt; <em>googlebot</em>(<em>at</em>)<em>googlebot.com</em> [<em>HTTP_HOST</em>] <b>...</b>
<br></span>
<table class="tsnip">
<thead>
<tr>
<th>環境変数名
<th>値
<tbody>
<tr>
<td>REMOTE_HOST
<td>ユーザのホスト名
<tr>
<td>REMOTE_IDENT
<td>ユーザ名（IDENTプロトコルに対応している場合</table></div></div>
<!--n--></li>
<!--m-->
<li class="g">
<div class="vsc" pved="0CDgQkgowAziMAQ" bved="0CDkQkQo4jAE" sig="TwT">
<h3 class="r">
<a href="http://www.veloso.adm.br/ASPInfo.asp?comID=200" class=l onmousedown="return rwt(this,'','','','144','AFQjCNESYJZCx0orwLbL-ooDo1WZ96laBw','','0CD4QFjADOIwB',null,event)">ASP Component Test - http://www.pensaworks.com</a></h3>
<div class="s">
<div class="f kv">
<cite>www.veloso.adm.br/ASPInfo.asp?comID...</cite>
<span class="gl"> -
<a href="http://webcache.googleusercontent.com/search?q=cache:66qfE0SQP8AJ:www.veloso.adm.br/ASPInfo.asp%3FcomID%3D200+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;cd=144&amp;hl=en&amp;ct=clnk" onmousedown="return rwt(this,'','','','144','AFQjCNH0p_bR4_At2FVT-v7y2R70LrBE0Q','','0CDsQIDADOIwB',null,event)">Cached</a></span>
<span class="std">&nbsp;
<span class=gl>-</span>
<a href="http://translate.google.com/translate?hl=en&amp;sl=pt&amp;u=http://www.veloso.adm.br/ASPInfo.asp%3FcomID%3D200&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=translate&amp;ct=result&amp;resnum=4&amp;ved=0CDwQ7gEwAziMAQ&amp;prev=/search%3Fq%3Dallintext:%2B-error%2BREMOTE_ADDR%2BREQUEST_METHOD%2Bgooglebot(at)googlebot.com%2BHTTP_USER_AGENT%2BHTTP_CONNECTION%2BHTTP_HOST%2BHTTP_REFERER%2BHTTP_ACCEPT%26start%3D140%26hl%3Den%26sa%3DN%26gbv%3D2%26prmd%3Divns" class=fl>Translate this page</a></span></div>
<div class="esc slp" id="poS143" style="display:none">You +1'd this publicly.&nbsp;
<a href="#" class="fl">Undo</a></div>
<span class="st"><em>HTTP_USER_AGENT</em> Tipo de versão do navegador bem como o sistema operacional  do visitante. <em>HTTP_REFERER</em> Página em que o usuário este antes de entra na página <b>...</b> ALL_HTTP, <em>HTTP_CONNECTION</em>:Keep-alive <em>HTTP_ACCEPT</em>:*/* <b>...</b> HTTP_FROM:<em>googlebot</em>(<em>at</em>)<em>googlebot.com HTTP_HOST</em>:<wbr>www.veloso.adm.br <b>...</b>
<br></span></div></div>
<!--n--></li>
<!--m-->
<li class="g">
<div class="vsc" pved="0CEAQkgowBDiMAQ" bved="0CEEQkQo4jAE" sig="7-o">
<h3 class="r">
<a href="http://www.avege.ru/russian/tempsite/perl/perl02.shtml" class=l onmousedown="return rwt(this,'','','','145','AFQjCNH6JuOEWeBiVQ7a_GFY7b8GJPWBIw','','0CEcQFjAEOIwB',null,event)">Пример скрипта perl - информации о переменных окружения <b>...</b></a></h3>
<>
<div class="s">
<div class="f kv">
<cite>www.avege.ru/russian/.../perl/perl02.shtml</cite>
<span class="gl"> -
<a href="http://webcache.googleusercontent.com/search?q=cache:E85R70LT_C0J:www.avege.ru/russian/tempsite/perl/perl02.shtml+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;cd=145&amp;hl=en&amp;ct=clnk" onmousedown="return rwt(this,'','','','145','AFQjCNGa6WjJ8QJrNSfymQ8RnBC-1I460Q','','0CEMQIDAEOIwB',null,event)">Cached</a></span>
<span class="vshid">
<a href="/search?hl=en&amp;gbv=2&amp;q=related:www.avege.ru/russian/tempsite/perl/perl02.shtml+allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;tbo=1&amp;sa=X&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;ved=0CEQQHzAEOIwB">Similar</a></span>
<span class="std">&nbsp;
<span class=gl>-</span>
<a href="http://translate.google.com/translate?hl=en&amp;sl=ru&amp;u=http://www.avege.ru/russian/tempsite/perl/perl02.shtml&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=translate&amp;ct=result&amp;resnum=5&amp;ved=0CEUQ7gEwBDiMAQ&amp;prev=/search%3Fq%3Dallintext:%2B-error%2BREMOTE_ADDR%2BREQUEST_METHOD%2Bgooglebot(at)googlebot.com%2BHTTP_USER_AGENT%2BHTTP_CONNECTION%2BHTTP_HOST%2BHTTP_REFERER%2BHTTP_ACCEPT%26start%3D140%26hl%3Den%26sa%3DN%26gbv%3D2%26prmd%3Divns" class=fl>Translate this page</a></span></div>
<div class="esc slp" id="poS144" style="display:none">You +1'd this publicly.&nbsp;
<a href="#" class="fl">Undo</a></div>
<span class="st">
<span class="f">6 июн 2008 &ndash; </span><em>HTTP_CONNECTION</em>, close. HTTP_FROM, <em>googlebot</em>(<em>at</em>)<em>googlebot.com</em>. <em>HTTP_HOST</em>, www.avege.ru. HTTP_IF_MODIFIED_SINCE, Tue, 28 <b>...</b>
<br></span></div></div>
<!--n--></li>
<!--m-->
<li class="g">
<div class="vsc" pved="0CEkQkgowBTiMAQ" bved="0CEoQkQo4jAE" sig="8AW">
<h3 class="r">
<a href="http://owssd.org/arts/animation/" class=l onmousedown="return rwt(this,'','','','146','AFQjCNGm9-oLR_RlIw-7Ft7vrp22j6Fqrg','','0CE0QFjAFOIwB',null,event)">Animation « Arts « Occupy Wall Street Supporters Directory <b>...</b></a></h3>
<>
<div class="s">
<div class="f kv">
<cite>owssd.org/arts/animation/</cite>
<span class="gl"> -
<a href="http://webcache.googleusercontent.com/search?q=cache:ofX05aYpkPwJ:owssd.org/arts/animation/+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;cd=146&amp;hl=en&amp;ct=clnk" onmousedown="return rwt(this,'','','','146','AFQjCNGDuxibdChWaqTXZYergzvoErzQIg','','0CEwQIDAFOIwB',null,event)">Cached</a></span></div>
<div class="esc slp" id="poS145" style="display:none">You +1'd this publicly.&nbsp;
<a href="#" class="fl">Undo</a></div>
<span class="st"><b>...</b> [<em>HTTP_HOST</em>] =&gt; owssd.org [<em>HTTP_CONNECTION</em>] =&gt; close [<em>HTTP_ACCEPT</em>] =&gt; */* [HTTP_FROM] =&gt; <em>googlebot</em>(<em>at</em>)<em>googlebot.com</em> [<em>HTTP_USER_AGENT</em>] <b>...</b> 184.168.26.1 [SERVER_PORT] =&gt; 80 [<em>REMOTE_ADDR</em>] =&gt; 66.249.67.119 <b>...</b> CGI/1.1 [SERVER_PROTOCOL] =&gt; HTTP/1.1 [<em>REQUEST_METHOD</em>] =&gt; GET <b>...</b>
<br></span></div></div>
<!--n--></li>
<!--m-->
<li class="g">
<div class="vsc" pved="0CE8QkgowBjiMAQ" bved="0CFAQkQo4jAE" sig="eR5">
<h3 class="r">
<a href="http://fiskal.dk/" class=l onmousedown="return rwt(this,'','','','147','AFQjCNGlugHo8jjYW7QjvUmou_8sJgzBAg','','0CFUQFjAGOIwB',null,event)">Domene-redirect informasjon</a></h3>
<div class="s">
<div class="f kv">
<cite>fiskal.dk/</cite>
<span class="gl"> -
<a href="http://webcache.googleusercontent.com/search?q=cache:Qt47sEbCtd4J:fiskal.dk/+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;cd=147&amp;hl=en&amp;ct=clnk" onmousedown="return rwt(this,'','','','147','AFQjCNEk-AM_WkL8utDa99wBNVf89ilQ6g','','0CFIQIDAGOIwB',null,event)">Cached</a></span>
<span class="std">&nbsp;
<span class=gl>-</span>
<a href="http://translate.google.com/translate?hl=en&amp;sl=da&amp;u=http://fiskal.dk/&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=translate&amp;ct=result&amp;resnum=7&amp;ved=0CFMQ7gEwBjiMAQ&amp;prev=/search%3Fq%3Dallintext:%2B-error%2BREMOTE_ADDR%2BREQUEST_METHOD%2Bgooglebot(at)googlebot.com%2BHTTP_USER_AGENT%2BHTTP_CONNECTION%2BHTTP_HOST%2BHTTP_REFERER%2BHTTP_ACCEPT%26start%3D140%26hl%3Den%26sa%3DN%26gbv%3D2%26prmd%3Divns" class=fl>Translate this page</a></span></div>
<div class="esc slp" id="poS146" style="display:none">You +1'd this publicly.&nbsp;
<a href="#" class="fl">Undo</a></div>
<span class="st">Array ( [<em>HTTP_HOST</em>] =&gt; fiskal.dk [<em>HTTP_CONNECTION</em>] =&gt; Keep-alive [<wbr><em>HTTP_ACCEPT</em>] <b>...</b> [HTTP_FROM] =&gt; <em>googlebot</em>(<em>at</em>)<em>googlebot.com</em> [<wbr><em>HTTP_USER_AGENT</em>] <b>...</b> 95.141.83.26 [SERVER_PORT] =&gt; 80 [<wbr><em>REMOTE_ADDR</em>] =&gt; 66.249.66.237 <b>...</b> CGI/1.1 [SERVER_PROTOCOL] =&gt; HTTP/<wbr>1.1 [<em>REQUEST_METHOD</em>] =&gt; GET <b>...</b>
<br></span></div></div>
<!--n--></li>
<!--m-->
<li class="g">
<div class="vsc" pved="0CFcQkgowBziMAQ" bved="0CFgQkQo4jAE" sig="UEQ">
<h3 class="r">
<a href="http://www.kio-price.ru/articles/item-12.html" class=l onmousedown="return rwt(this,'','','','148','AFQjCNEMHTMwB_Mnm7ZMtTDqWF9W1TPQVg','','0CF0QFjAHOIwB',null,event)">Коннект без проводов</a></h3>
<div class="s">
<div class="f kv">
<cite>www.kio-price.ru/articles/item-12.html</cite>
<span class="gl"> -
<a href="http://webcache.googleusercontent.com/search?q=cache:l1EChW1aPbUJ:www.kio-price.ru/articles/item-12.html+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;cd=148&amp;hl=en&amp;ct=clnk" onmousedown="return rwt(this,'','','','148','AFQjCNHq0hk02IzsJPbM4iWPiMIru9BxSw','','0CFoQIDAHOIwB',null,event)">Cached</a></span>
<span class="std">&nbsp;
<span class=gl>-</span>
<a href="http://translate.google.com/translate?hl=en&amp;sl=ru&amp;u=http://www.kio-price.ru/articles/item-12.html&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=translate&amp;ct=result&amp;resnum=8&amp;ved=0CFsQ7gEwBziMAQ&amp;prev=/search%3Fq%3Dallintext:%2B-error%2BREMOTE_ADDR%2BREQUEST_METHOD%2Bgooglebot(at)googlebot.com%2BHTTP_USER_AGENT%2BHTTP_CONNECTION%2BHTTP_HOST%2BHTTP_REFERER%2BHTTP_ACCEPT%26start%3D140%26hl%3Den%26sa%3DN%26gbv%3D2%26prmd%3Divns" class=fl>Translate this page</a></span></div>
<div class="esc slp" id="poS147" style="display:none">You +1'd this publicly.&nbsp;
<a href="#" class="fl">Undo</a></div>
<span class="st"><em>HTTP_USER_AGENT</em>: Mozilla/5.0 (compatible; <em>Googlebot</em>/2.1; <b>...</b> REQUEST_URI<wbr>: /articles/item-12.html; <em>HTTP_REFERER</em>: <em>REQUEST_METHOD</em>: GET. Server Vars: <b>...</b> string(12) &quot;gzip,deflate&quot; [&quot;<em>HTTP_CONNECTION</em>&quot;]=&gt; string(5) &quot;close&quot; [&quot;<wbr>HTTP_FROM&quot;]=&gt; string(26) &quot;<em>googlebot</em>(<em>at</em>)<em>googlebot.com</em>&quot; [&quot;<em>HTTP_HOST</em>&quot;]=&gt; string(16) <b>...</b>
<br></span></div></div>
<!--n--></li>
<!--m-->
<li class="g">
<div class="vsc" pved="0CF8QkgowCDiMAQ" bved="0CGAQkQo4jAE" sig="Ger">
<h3 class="r">
<a href="http://sunpillar.jf.land.to/bekkan/cgi-bin/info/info.cgi" class=l onmousedown="return rwt(this,'','','','149','AFQjCNH8bff2mi4Jj8wCikFSu3-3wpafwg','','0CGUQFjAIOIwB',null,event)">SUNPILLAR情報舘 実験棟</a></h3>
<div class="s">
<div class="f kv">
<cite>sunpillar.jf.land.to/bekkan/cgi-bin/.../info.c...</cite>
<span class="gl"> -
<a href="http://webcache.googleusercontent.com/search?q=cache:VhwwIeL2iToJ:sunpillar.jf.land.to/bekkan/cgi-bin/info/info.cgi+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;cd=149&amp;hl=en&amp;ct=clnk" onmousedown="return rwt(this,'','','','149','AFQjCNHY93ikRiKYv7R99jdSiWzc3Qy25A','','0CGIQIDAIOIwB',null,event)">Cached</a></span>
<span class="std">&nbsp;
<span class=gl>-</span>
<a href="http://translate.google.com/translate?hl=en&amp;sl=ja&amp;u=http://sunpillar.jf.land.to/bekkan/cgi-bin/info/info.cgi&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=translate&amp;ct=result&amp;resnum=9&amp;ved=0CGMQ7gEwCDiMAQ&amp;prev=/search%3Fq%3Dallintext:%2B-error%2BREMOTE_ADDR%2BREQUEST_METHOD%2Bgooglebot(at)googlebot.com%2BHTTP_USER_AGENT%2BHTTP_CONNECTION%2BHTTP_HOST%2BHTTP_REFERER%2BHTTP_ACCEPT%26start%3D140%26hl%3Den%26sa%3DN%26gbv%3D2%26prmd%3Divns" class=fl>Translate this page</a></span></div>
<div class="esc slp" id="poS148" style="display:none">You +1'd this publicly.&nbsp;
<a href="#" class="fl">Undo</a></div>
<span class="st">
<span class="f">1 日前 &ndash; </span><em>REMOTE_ADDR</em>（クライアント側IPアドレス） 66.249.67.151 <b>...</b> <em>HTTP_USER_AGENT</em>（ブラウザ名・OS情報等〔偽装可能〕） <b>...</b> <em>HTTP_REFERER</em>（<wbr>リンク元のアドレス） (none) <em>HTTP_ACCEPT</em>（ブラウザがサポートするメディアタイプ・<wbr>MIMEタイプ） */* <b>...</b> <em>HTTP_HOST</em>（接続先のホスト名） <b>...</b> <em>googlebot</em>(<em>at</em>)<em>googlebot.com</em> <b>...</b>
<br></span></div></div>
<!--n--></li>
<!--m-->
<li class="g">
<div class="vsc" pved="0CGcQkgowCTiMAQ" bved="0CGgQkQo4jAE" sig="ZI0">
<h3 class="r">
<a href="http://norfipc.com/web/como-mostrar-direccion-ip-visitantes-paginas-web.php" class=l onmousedown="return rwt(this,'','','','150','AFQjCNEMMQX4dH9Y1P2bZlyaubU7e5p9oA','','0CG8QFjAJOIwB',null,event)">Como mostrar la direccion IP de los visitantes en las paginas web</a></h3>
<div class="s">
<div class="f kv">
<cite>
<span class=bc>norfipc.com &rsaquo;
<a href="/url?url=http://norfipc.com/web/index.html&amp;rct=j&amp;sa=X&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;ved=0CGsQ6QUoADAJOIwB&amp;q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;usg=AFQjCNHZCDCO6IssuDXlnuLB6zNX2S8zdw">Diseño y edición web</a></span></cite>
<span class="gl"> -
<a href="http://webcache.googleusercontent.com/search?q=cache:yCKqaJBsFbUJ:norfipc.com/web/como-mostrar-direccion-ip-visitantes-paginas-web.php+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;cd=150&amp;hl=en&amp;ct=clnk" onmousedown="return rwt(this,'','','','150','AFQjCNHebifX4HtvswYlvgS9tfgLRdLaNA','','0CGoQIDAJOIwB',null,event)">Cached</a></span>
<span class="std">&nbsp;
<span class=gl>-</span>
<a href="http://translate.google.com/translate?hl=en&amp;sl=es&amp;u=http://norfipc.com/web/como-mostrar-direccion-ip-visitantes-paginas-web.php&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;sa=X&amp;oi=translate&amp;ct=result&amp;resnum=10&amp;ved=0CG0Q7gEwCTiMAQ&amp;prev=/search%3Fq%3Dallintext:%2B-error%2BREMOTE_ADDR%2BREQUEST_METHOD%2Bgooglebot(at)googlebot.com%2BHTTP_USER_AGENT%2BHTTP_CONNECTION%2BHTTP_HOST%2BHTTP_REFERER%2BHTTP_ACCEPT%26start%3D140%26hl%3Den%26sa%3DN%26gbv%3D2%26prmd%3Divns" class=fl>Translate this page</a></span></div>
<div class="esc slp" id="poS149" style="display:none">You +1'd this publicly.&nbsp;
<a href="#" class="fl">Undo</a></div>
<span class="st">Lo que se ha hecho es utilizar la variable &quot;<em>REMOTE_ADDR</em>&quot;, mediante la cual el <b>...</b> &#39;<em>HTTP_REFERER</em>&#39; para conocer la página de referencia <b>...</b> &#39;<wbr><em>HTTP_USER_AGENT</em>&#39; para mostrar el agente de usuario de tu navegador <b>...</b> <em>HTTP_ACCEPT</em>, */* <b>...</b> <em>HTTP_CONNECTION</em>, keep-alive. HTTP_FROM, <em>googlebot</em>(<em>at</em>)<em>googlebot.com</em> <b>...</b>
<br></span></div></div>
<!--n--></li></ol>   </div>
<!--z--> </div>  </div>
<div id="bottomads"></div>
<div class="med" id="extrares" style="padding:0 8px">
<div>
<div id="botstuff">
<div id=uh_hp>
<a id=uh_hpl href="#"></a></div>
<div id=uh_h>
<a id=uh_hl></a></div>  </div> </div> </div>  </div>
<div id="rhscol">  </div>  </div>
<div class="tsf-p" id="foot" role="contentinfo">
<span id="xjs">
<div id="navcnt">
<table id="nav" style="border-collapse:collapse;text-align:left;margin:17px auto 0;direction:ltr">
<tr valign="top">
<td class="b navend">
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;start=130&amp;sa=N" class="pn" id="pnprev" style="text-decoration:none">
<span class="csb gbil ch" style="background-position:0 0;width:53px;float:right"></span>
<span style="display:block;margin-right:35px;clear:right;text-decoration:underline">Previous</span></a></td>
<td>
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;start=90&amp;sa=N" class="fl">
<span class="csb gbil ch" style="background-position:-74px 0;width:20px"></span>10</a></td>
<td>
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;start=100&amp;sa=N" class="fl">
<span class="csb gbil ch" style="background-position:-74px 0;width:20px"></span>11</a></td>
<td>
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;start=110&amp;sa=N" class="fl">
<span class="csb gbil ch" style="background-position:-74px 0;width:20px"></span>12</a></td>
<td>
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;start=120&amp;sa=N" class="fl">
<span class="csb gbil ch" style="background-position:-74px 0;width:20px"></span>13</a></td>
<td>
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;start=130&amp;sa=N" class="fl">
<span class="csb gbil ch" style="background-position:-74px 0;width:20px"></span>14</a></td>
<td class="cur">
<span class="csb gbil" style="background-position:-53px 0;width:20px"></span>15</td>
<td>
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;start=150&amp;sa=N" class="fl">
<span class="csb gbil ch" style="background-position:-74px 0;width:20px"></span>16</a></td>
<td>
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;start=160&amp;sa=N" class="fl">
<span class="csb gbil ch" style="background-position:-74px 0;width:20px"></span>17</a></td>
<td>
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;start=170&amp;sa=N" class="fl">
<span class="csb gbil ch" style="background-position:-74px 0;width:20px"></span>18</a></td>
<td>
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;start=180&amp;sa=N" class="fl">
<span class="csb gbil ch" style="background-position:-74px 0;width:20px"></span>19</a></td>
<td class="b navend">
<a href="/search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns&amp;ei=wxxzT_2_DJG0iQeR0vjjDw&amp;start=150&amp;sa=N" class="pn" id="pnnext" style="text-decoration:none;text-align:left">
<span class="csb gbil ch" style="background-position:-96px 0;width:71px"></span>
<span style="display:block;margin-left:53px;text-decoration:underline">Next</span></a></td></tr></table></div>      </span>
<div style="height:13px;line-height:0"></div>
<div>
<p id="bfl" style="margin:6px 0 0;text-align:center">
<span id="fblmi"></span>
<a class="gl nobr" href="/advanced_search?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns" id="sflas">Advanced search</a>
<span id="fblsh">
<a href="/support/websearch/bin/answer.py?answer=134479&amp;hl=en&amp;p=" class="fl">Search Help</a></span>
<a class="fl" href="/quality_form?q=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT&amp;hl=en&amp;gbv=2&amp;prmd=ivns" target="_blank" id="fblqf">Give us feedback</a></p></div>
<div id="gfn"></div>
<div id="fll" style="margin:19px auto;text-align:center">
<a href="/">Google&nbsp;Home</a>‎<wbr>
<a href="/intl/en/ads/">Advertising&nbsp;Programs</a>‎<wbr>
<a href="/services/">Business Solutions</a>‎<wbr>
<a href="/intl/en/policies/">Privacy & Terms</a>‎<wbr>
<a href="/intl/en/about.html">About Google</a>‎<wbr></div>   </div>
<div id="bfoot">
<div id=nyc style="display:none" role="dialog">
<div id=nycp>
<div id=nycxh>
<button id=nycx title="Hide result details"></button> </div>
<div id=nycntg></div>
<div id=nycpp>
<div style="position:absolute;left:0;right:0;text-align:center;top:45%">
<img id=nycli></img>
<div id=nycm></div></div>
<div id=nycprv></div></div></div>
<div id=nyccur></div></div>
<div id=nycf></div> </div></div>
<script>function _gjp(){!(location.hash && _gjuc())&& setTimeout(_gjp,500);}


google.j[1]={
cc:[],
co:[
'cnt','xfoot','xjsi'
],css:document.getElementById('gstyle').innerHTML,main:'
<div id=cnt></div>
<div id=xfoot></div>
<div id=xjsi></div>',bl:['mngb','gb_']
};</script>
<script data-url="/extern_chrome/3c09e860528ab082.js?hl=en" id="extern_chrome_script">function wgjp(){var xjs=document.createElement('script');xjs.src=document.getElementById('extern_chrome_script').
getAttribute('data-url');

(document.getElementById('xjsd')||
document.body).appendChild(xjs)
};</script>
<div id="xfoot">
<div id=xjsd></div>
<div id=xjsi>
<script>if(google.y)google.y.first=[];google.dlj=function(b){window.setTimeout(function(){var a=document.createElement("script");a.src=b;document.getElementById("xjsd").appendChild(a)},0)};
if(google.y)google.y.first=[];if(!google.xjs){google.dstr=[];google.rein=[];if(google.timers&&google.timers.load.t){google.timers.load.t.xjsls=new Date().getTime();}google.dlj('/extern_js/f/CgJlbiswRTgALCswWjgALCswDjgALCswFzgALCswPDgALCswUTgALCswWTgALCswCjgAmgICY2MsKzCYATgALCswFjgALCswGTgALCswKzgALCswQTgALCswTTgALCswTjgALCswUzgALCswVDgALCswaTgALCswkAE4ACwrMJIBOAAsKzCXATgALCswowE4ACwrMKcBOAAsKzCsATgALCsw0QE4ACwrMNUBOAAsKzDYATgALCsw2wE4ACwrMHQ4ACwrMB04ACwrMFw4ACwrMBg4ACwrMCY4ACyAAmuQAm4/zg1kaqOzMbc.js');google.xjs=1}window.mbtb1={tbm:"",tbs:"",docid:"12031578450409248854",usg:"7023"};google.base_href='/search?q\x3dallintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT\x26start\x3d140\x26hl\x3den\x26sa\x3dN\x26gbv\x3d2\x26prmd\x3divns\x26oq\x3dallintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT';google.sn='web';google.Toolbelt.atg=[7,9];google.Toolbelt.pbt=[];google.Toolbelt.pti={};google.mc=[];google.mc=google.mc.concat([[69,{}],[14,{}],[60,{}],[23,{}],[81,{}],[10,{"client":"serp","dh":true,"ds":"","exp":"llsin","fl":true,"host":"google.com","jsonp":true,"lyrs":29,"msgs":{"lcky":"I\u0026#39;m Feeling Lucky","lml":"Learn more","psrc":"This search was removed from your \u003Ca href=\"/history\"\u003EWeb History\u003C/a\u003E","psrl":"Remove","srch":"Google Search"},"ovr":{"fm":1,"l":1,"mc":1,"p":1,"pf":1,"ps":1,"sp":1,"sw":1},"pq":"allintext: -error REMOTE_ADDR REQUEST_METHOD googlebot(at)googlebot.com HTTP_USER_AGENT HTTP_CONNECTION HTTP_HOST HTTP_REFERER HTTP_ACCEPT","psy":"p","scd":10,"sce":4}],[152,{}],[43,{"qir":true,"rctj":true,"ref":false,"uff":false}],[83,{}],[65,{}],[213,{"pberr":"\u003Cfont color=red\u003EError:\u003C/font\u003E The server could not complete your request.  Try again in 30 seconds."}],[78,{}],[25,{"g":28,"k":true,"m":{"app":true,"bks":true,"blg":true,"dsc":true,"evn":true,"fin":true,"flm":true,"frm":true,"isch":true,"klg":true,"mbl":true,"nws":true,"plcs":true,"ppl":true,"prc":true,"pts":true,"rcp":true,"shop":true,"vid":true},"t":null}],[216,{}],[105,{}],[22,{"db":false,"m_errors":{"32":"Sorry, no more results to show.","default":"\u003Cfont color=red\u003EError:\u003C/font\u003E The server could not complete your request.  Try again in 30 seconds."},"m_tip":"Click for more information","nlpm":"-153px -84px","nlpp":"-153px -70px","utp":true}],[77,{}],[146,{}],[209,{}],[144,{}],[219,{}],[167,{"MESSAGES":{"msg_img_from":"Image from %1$s","msg_ms":"More sizes","msg_si":"Similar"}}],[84,{"cm_hov":true,"uab":true}],[151,{"ab":{"on":true},"ajax":{"gl":"us","gwsHost":"","hl":"en","maxPrefetchConnections":2,"prefetchTotal":5,"q":"allintext: -error REMOTE_ADDR REQUEST_METHOD googlebot(at)googlebot.com HTTP_USER_AGENT HTTP_CONNECTION HTTP_HOST HTTP_REFERER HTTP_ACCEPT","requestPrefix":"/ajax/rd?"},"css":{"def":true,"hIconsLarge":true},"elastic":{"hideLeftnav":false,"js":true,"rhs4Col":1088,"rhs5Col":1176,"rhsOn":true,"tiny":false},"exp":{},"kfe":{"adsClientId":33,"clientId":29,"kfeHost":"clients1.google.com","kfeUrlPrefix":"/webpagethumbnail?r=4\u0026f=3\u0026s=400:585\u0026query=allintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT\u0026hl=en\u0026gl=us","vsH":585,"vsW":400},"logging":{"csiFraction":0.050},"msgs":{"details":"Result details","hPers":"Hide personal results","loading":"Still loading...","mute":"Mute","noPreview":"Preview not available","sPers":"Show personal results","unmute":"Unmute"},"nokjs":{"on":true},"time":{"hOff":300,"hOn":300,"hSwitch":200,"loading":100,"timeout":2500},"vp":{"setUserPrefsUrl":"/setprefs?vpsndts=%(exptime)s\u0026sig=0_SzbvU4UwYxQq_aDNITX3eUvhGvs=\u0026noredirect=1"}}],[116,{"bd":[],"bk":[],"bu":[],"gl":"","mb":500,"msgs":{"a":"Block all %1$s results","b":"\u003Cb\u003ENot helpful?\u003C/b\u003E You can block \u003Cb\u003E%1$s\u003C/b\u003E results when you\u0026#39;re signed in to search.","c":"We will not show you results from \u003Cb\u003E%1$s\u003C/b\u003E again.","d":"Manage blocked sites","e":"Undo","f":"Unblock %1$s","g":"Unblocked %1$s"},"q":"allintext: -error REMOTE_ADDR REQUEST_METHOD googlebot(at)googlebot.com HTTP_USER_AGENT HTTP_CONNECTION HTTP_HOST HTTP_REFERER HTTP_ACCEPT","rb":true}],[29,{"cspd":0,"icmt":false,"jck":true,"mcr":5}],[92,{"ae":true,"avgTtfc":2000,"biav":true,"bpe":false,"brba":false,"dlen":24,"dper":3,"fbdc":500,"fbdu":3000,"fbh":true,"fd":1000,"focus":true,"fs":true,"gpsj":true,"hiue":true,"hpt":299,"iavgTtfc":2000,"kn":true,"knrt":true,"maxCbt":1500,"mds":"clir,clue,dfn,evn,frim,klg,prc,rl,show,sp,sts,mbl_he,mbl_hs,mbl_re,mbl_rs,mbl_sv","msg":{"dym":"Did you mean:","gs":"Google Search","kntt":"Use the up and down arrow keys to select each result. Press Enter to go to the selection.","sif":"Search instead for","srf":"Showing results for"},"odef":true,"ophe":true,"pmt":250,"pq":true,"rpt":50,"sfcs":false,"tct":" \\u3000?","tdur":50,"ufl":true}],[24,{}],[38,{}]]);(function(){var r=(function(){google.y.first.push(function(){try{;var b={hover:{}};b.hover.HOVER_DELAY=400;b.hover.k=[];b.hover.a={};b.hover.init=function(){for(var a=google.dom.getAll(".son"),c=0,d;d=a[c];c++)b.hover.initHoversForParent(d)};b.hover.initHoversForParent=function(a){var c=google.dom.getAll(".soha",a),a=google.dom.getAll(".soh",a);if(c.length==a.length)for(var d=0,e;e=c[d];d++){var f=a[d];b.hover.m(e,f)}};b.hover.m=function(a,c){b.hover.h(a,"mouseover",b.hover.getOnMouseOver(a,c));b.hover.h(a,"mouseout",b.hover.getOnMouseOut(a,c))};
b.hover.h=function(a,c,d){google.listen(a,c,d);a={object:a,eventType:c,handler:d};b.hover.k.push(a)};b.hover.showHover=function(a){a.style.display="block";a.style.top="24px";a.style.left="0"};b.hover.hideHover=function(a){a.style.display="none"};b.hover.getOnMouseOver=function(a,c){return function(a){if(void 0==b.hover.a[a]){var e=window.setTimeout(function(){b.hover.showHover(c)},b.hover.HOVER_DELAY);b.hover.a[a]=e}}};
b.hover.getOnMouseOut=function(a,c){return function(a){window.clearTimeout(b.hover.a[a]);b.hover.a[a]=void 0;b.hover.hideHover(c)}};b.hover.g=function(){for(var a;a=b.hover.k.pop();)google.unlisten(a.object,a.eventType,a.handler);for(var c in b.hover.a)window.clearTimeout(b.hover.a[c]);b.hover.a={}};google.dstr.push(b.hover.g);google.rein.push(function(){b.hover.g();b.hover.init()});google.sos=b;google.sos.hover.init();
;google.rrep=function(b,c,d,a){google.log(b,c,"",document.getElementById(a));document.getElementById(d).style.display="";document.getElementById(a).style.display="none"};
;google.sc=google.sc||{};if(!google.sc['riu'])google.sc['riu']={'u':'/extern_js/f/CgJlbiswPzgALIACa5ACbqICA3JpdQ/X_-dUXdZBPU.js','cb':[]};google.smc=google.smc||[];google.smc=google.smc.concat([[63,{"cnfrm":"Reported","prmpt":"Report"}]]);;google.riul={render:function(){google.util.xjsl('riu',function(){google.riu.render();})}};;google.sc=google.sc||{};if(!google.sc['rvu'])google.sc['rvu']={'u':'/extern_js/f/CgJlbiswcjgALIACa5ACbqICA3J2dQ/DCEIoFnnAfk.js','cb':[]};google.smc=google.smc||[];google.smc=google.smc.concat([[114,{"rvu_report_msg":"Report","rvu_reported_msg":"Reported"}]]);;}catch(e){google.ml(e,false,{'cause':'defer'});}if(google.med){google.med('init');google.initHistory();google.med('history');}google.History&&google.History.initialize('/search?q\x3dallintext:+-error+REMOTE_ADDR+REQUEST_METHOD+googlebot(at)googlebot.com+HTTP_USER_AGENT+HTTP_CONNECTION+HTTP_HOST+HTTP_REFERER+HTTP_ACCEPT\x26amp;hl\x3den\x26amp;prmd\x3divns\x26amp;ei\x3dihtzT62zBaaYiAfbjInkDw\x26amp;start\x3d140\x26amp;sa\x3dN\x26amp;sei\x3dvxxzT_3bIKyyiQeXrIDkDw\x26amp;gbv\x3d2')});});r();var l=window.location.hash?window.location.href.substr(window.location.href.indexOf('#')):'#';if(l=='#'&&google.defre){google.defre=1;google.y.first.push(function(){if(google.j&&google.j.init){google.rein&&google.rein.push(r);}});}})();if(google.j&&google.j.en&&google.j.xi){window.setTimeout(google.j.xi,0);}</script></div>
<script>(function(){
var b,d,e,f;function g(a,c){if(a.removeEventListener){a.removeEventListener("load",c,false);a.removeEventListener("error",c,false)}else{a.detachEvent("onload",c);a.detachEvent("onerror",c)}}function h(a){f=(new Date).getTime();++d;a=a||window.event;var c=a.target||a.srcElement;g(c,h)}var i=document.getElementsByTagName("img");b=i.length;d=0;for(var j=0,k;j
<b;++j){k=i[j];if(k.complete||typeof k.src!="string"||!k.src)++d;else if(k.addEventListener){k.addEventListener("load",h,false);k.addEventListener("error",
h,false)}else{k.attachEvent("onload",h);k.attachEvent("onerror",h)}}e=b-d;function l(){if(!google.timers.load.t)return;google.timers.load.t.ol=(new Date).getTime();google.timers.load.t.iml=f;google.kCSI.imc=d;google.kCSI.imn=b;google.kCSI.imp=e;if(google.stt!==undefined)google.kCSI.stt=google.stt;google.timers.load.t.xjs&&google.report&&google.report(google.timers.load,google.kCSI)}if(window.addEventListener)window.addEventListener("load",
l,false);else if(window.attachEvent)window.attachEvent("onload",l);google.timers.load.t.prt=(f=(new Date).getTime());
})();
</script></div></div></div></div></body></html>'''


sGoogleQuerResult_Firefox = \
'''truncated'''

sWikiPediaTopLevelDomains = \
'''
'''

if __name__ == "__main__":
    #
    from six            import print_ as print3
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #

    #
    sayTestResult( lProblems )