#!/usr/bin/pythonTest
#
# Utility functions TimeLimit
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
# Copyright 2004-2016 Rick Graves
#
#

"""
fn_1 (sleep 2, nTimeLimit 4):  Finished
fn_2 (sleep 2, nTimeLimit 4):  Finished
fn_1 (sleep 4, nTimeLimit 2):  took too long
fn_3 (sleep 4, nTimeLimit 2):  took too long
fn_4 (sleep 4, nTimeLimit 2):  (Caught TimeOverExcept, so cleaining up, and re-raising it) -  took too long
"""

import signal, time

from six import print_ as print3

class TimeOverExcept(Exception):
    def __init__(self, value = "Timed Out"):
        self.value = value
    def __str__(self):
        return repr(self.value)

def TimeLimitWrap(nTimeLimit, f, *args, **kwargs):
    def handler(signum, frame):
        raise TimeOverExcept()

    old = signal.signal(signal.SIGALRM, handler)
    signal.alarm(nTimeLimit)
    try:
        result = f(*args, **kwargs)
    finally:
        signal.signal(signal.SIGALRM, old)
    signal.alarm(0)
    return result


def TimeLimitDecorator(nTimeLimit):
    def decorate(f):
        def handler(signum, frame):
            raise TimeOverExcept()

        def new_f(*args, **kwargs):
            old = signal.signal(signal.SIGALRM, handler)
            signal.alarm(nTimeLimit)
            try:
                result = f(*args, **kwargs)
            finally:
                signal.signal(signal.SIGALRM, old)
                signal.alarm(0)
            return result

        new_f.func_name = f.func_name
        return new_f

    return decorate


def fn_1(secs):
    time.sleep(secs)
    return "Finished"

#@TimeLimitDecorator(4) this syntax is not available on python 2.3
def fn_2(secs):
    time.sleep(secs)
    return "Finished"

#@TimeLimitDecorator(2)
def fn_3(secs):
    time.sleep(secs)
    return "Finished"

#@TimeLimitDecorator(2)
def fn_4(secs):
    try:
        time.sleep(secs)
        return "Finished"
    except TimeOverExcept:
        print3( "(Caught TimeOverExcept, so cleaining up, and re-raising it) - ", end = '' )
        raise TimeOverExcept


if __name__ == '__main__':

    try:
        print3( "fn_1 (sleep 2, nTimeLimit 4): ", end = '' )
        print3( TimeLimitWrap(4, fn_1, 2) )
    except TimeOverExcept:
        print3( "took too long" )

    try:
        print3( "fn_2 (sleep 2, nTimeLimit 4): ", end = '' )
        #print3( fn_2(2) )
        print3( TimeLimitWrap(4, fn_2, 2) )
    except TimeOverExcept:
        print3( "took too long" )

    try:
        print3( "fn_1 (sleep 4, nTimeLimit 2): ", end = '' )
        print3( TimeLimitWrap(2, fn_1, 4) )
    except TimeOverExcept:
        print3( "took too long" )

    try:
        print3( "fn_3 (sleep 4, nTimeLimit 2): ", end = '' )
        #print3( fn_3(4)
        print3( TimeLimitWrap(2, fn_3, 4) )
    except TimeOverExcept:
        print3( "took too long" )

    try:
        print3( "fn_4 (sleep 4, nTimeLimit 2): ", end = '' )
        #print3( fn_4(4)
        print3( TimeLimitWrap(2, fn_4, 4) )
    except TimeOverExcept:
        print3( "took too long" )
