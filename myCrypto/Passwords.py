#!/home/rick/.local/bin/pythonTest
# -*- coding: utf-8 -*-
#
# myCrypto functions Passwords
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
# Copyright 2021 - 2023 Rick Graves
#
#
import string
from sys import exit
try:
    import secrets
except ImportError:
    print( "This requires the secrets package in Python 3" )
    exit(1)

# only include characters that display well and are easy to find on keyboard
easyPunctuation = '!#$%&()*+,-./:;<=>?@[]^_{|}~'


def getPassword( want_length = 18, special_characters = easyPunctuation ):
    alphabet = string.ascii_letters + string.digits + special_characters
    if len(special_characters) == 0: special_characters = string.digits
    while True:
        password = ''.join(
                secrets.choice(alphabet) for i in range(want_length))
        if (    any(c.islower() for c in password) and
                any(c.isupper() for c in password) and
                any(c.isdigit() for c in password) and
                any(c in special_characters
                                for c in password) ):
            break
    return password


if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if len( getPassword( 10 ) ) != 10:
        #
        lProblems.append( 'getPassword() w specials' )
        #
    #
    if len( getPassword( 12, '' ) ) != 12:
        #
        lProblems.append( 'getPassword() w no specials' )
        #
    #
    #
    sayTestResult( lProblems )
