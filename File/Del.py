#!/usr/bin/pythonTest
#
# File functions Del
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


def DeleteIfExists( *sFileSpec ):
    #
    from os      import remove
    #
    from File.Spec import getFullSpec
    #
    sFileSpec = getFullSpec( *sFileSpec )
    #
    try:
        #
        remove( sFileSpec )
        #
    except OSError: # does not exist
        #
        pass




if __name__ == "__main__":
    #
    lProblems = []
    #
    from os.path        import exists
    #
    from File.Get       import getTempFile
    from Utils.Result   import sayTestResult
    #
    sTemp = getTempFile()
    #
    wasTemp = exists( sTemp )
    #
    DeleteIfExists( sTemp )
    #
    isTemp  = exists( sTemp )
    #
    if not( wasTemp and not isTemp ):
        #
        lProblems.append( 'DeleteIfExists()' )
        #
    #

    #
    sayTestResult( lProblems )