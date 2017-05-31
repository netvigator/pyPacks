#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions Socket
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
# self test needs internet connection and will access python.org

def getSocketConnection( tConnectTo ):
    #
    # this opens the socket -- don't forget to close it!!!
    #
    # not used anywhere yet
    #
    from socket import socket, AF_INET, SOCK_STREAM
    #
    bConnected      = True
    #
    oSocket         = socket( AF_INET, SOCK_STREAM )
    #
    try:
        #
        oSocket.connect( tConnectTo )
        #
    except:
        #
        bConnected  = False
        #
    #
    return oSocket, bConnected





if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    from Web.Get        import getDotQuadPortFromUrlPort
    #
    lProblems = []
    #
    tQuadPort = getDotQuadPortFromUrlPort( 'http://www.python.org:80/' )
    #
    oSocket, bConnected = getSocketConnection( tQuadPort )
    #
    oSocket.close()
    #
    if not bConnected:
        #
        lProblems.append( 'getSocketConnection()' )
        #

    #
    sayTestResult( lProblems )
    # self test needs internet connection and will access python.org