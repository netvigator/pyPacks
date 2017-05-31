#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Parser functions
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
'''
obsolete wrapper for OptionParser
Config.py is current, use that
'''

__version__ = '1.0'

def getParserOptions( _addParserOptions, sUsage = None, sVersion = None ):
    #
    """
    requires either Python >= 2.3 or Optik >= 1.4.1
    see http://optik.sourceforge.net/
    the module calling this needs its own _addParserOptions.
    """
    #
    from optparse import OptionParser
    #
    oParser = OptionParser( usage = sUsage, version = sVersion )
    #
    _addParserOptions( oParser )
    #
    oOptions, lArgs = oParser.parse_args()
    #
    return oOptions, lArgs



def addParserOptionsBasic( oParser ):
    #
    oParser.add_option( "-c", "--config",
                dest    = "Config",
                help    = "[CONFIG] - specify the config file to use" )
    #
    oParser.add_option( "-d", "--database",
                action  = "store_true",
                dest    = "bPromptUser",
                help    = "create a new database if one does not already exist",
                default = False )
    #
    oParser.add_option( "-v", "--verbose",
                action  = "store_true",
                dest    = "bVerbose",
                help    = "verbose mode (default from shell, but turn on to redirect output)",
                default = False )
    #
    oParser.add_option( "-S", "--status",
                action  = "store_true",
                dest    = "bGetStatus",
                help    = "is this already running?",
                default = False )


if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    # from Utils.Parser import getParserOptions
    #
    global oOptions
    #
    oOptions, lArgs = \
        getParserOptions(   addParserOptionsBasic,
                            sUsage      = '-h for help',
                            sVersion    = '%sprog %s' % ( '%', __version__ ) )
    #
    if oOptions.bVerbose:
        #
        lProblems.append( 'getParserOptions()' )
        #

    #
    sayTestResult( lProblems )
