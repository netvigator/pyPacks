#!/usr/bin/pythonTest
#
from six import print_ as print3

from twisted.internet   import reactor

def printInfo( data ):
    #
    print3( 'got page, length is %s bytes' % len( data ) )
    #
    reactor.stop()


def getSayError( oError ):
    #
    sError      = repr( oError )[ 1 : -1 ]
    #
    return sError.split()[ 1 ]


def sayError( self, oError ):
    #
    sError      = repr( oError )[ 1 : -1 ]
    #
    return sError.split()[ 1 ]


def printError( oFailure ):
    #
    from sys import stderr
    #
    try:
        sayError = getSayError( oFailure )
    except:
        sayError = 'getSayError() gave an error!'
    #
    print3( 'Error:', sayError, file=stderr )
    #
    reactor.stop()


def _WebCat( sURL ):
    #
    from twisted.web        import client
    #
    client.getPage( sURL ).addCallback( printInfo ).addErrback( printError )
    #
    reactor.run()


if __name__ == "__main__":
    #
    from sys import argv
    #
    if len( argv ) == 2:
        _WebCat( sys.argv[1] )
    else:
        print3( 'Usage: webcat.py <URL>' )
