#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#---------- histogram.py----------#
# Create occurrence counts of words or characters
# A few utility functions for presenting results
# Avoids requirement of recent Python features

from string import punctuation, digits
# from types import *
# import types


from six            import print_ as print3

from Utils.Version  import PYTHON3

if PYTHON3:
    # from types import str
    setStringTypes = frozenset( ( str, bytes ) )
else:
    from types import StringType, UnicodeType
    setStringTypes = frozenset( ( StringType, UnicodeType ) )





def _getFinder():
    #
    from String.Find    import getFinder
    #
    sWantWiped = '%s|%s' % (
        '|\\'.join( tuple( punctuation ) ),
        '|'.join( tuple( digits ) ) )
    #
    return getFinder( sWantWiped )

_oFinder = _getFinder()


def _getWiped( s ):
    #
    from String.Replace import getReplaced
    #
    return getReplaced( s, _oFinder, sWant = ' ' )

def word_histogram(source):
    """Create histogram of normalized words (no punct or digits)"""
    hist = {}
    # trans = maketrans('','')
    if type(source) in setStringTypes:  # String-like src
        source = _getWiped( source )
        for word in source.split():
            # word = word.translate( trans, sWipeThese )
            if len(word) > 0:
                hist[word] = hist.get(word,0) + 1
    elif hasattr(source,'read'):                  # File-like src
        for line in source:
            line = _getWiped( line )
            for word in line.split():
                # word = word.translate( trans, sWipeThese )
                if len(word) > 0:
                    hist[word] = hist.get(word,0) + 1
    else:
        raise TypeError( "source must be a string-like or file-like object" )
    return hist

def char_histogram(source, sizehint=1024*1024):
    hist = {}
    if type(source) in setStringTypes:  # String-like src
        for char in source:
            hist[char] = hist.get(char,0) + 1
    elif hasattr(source,'read'):                  # File-like src
        chunk = source.read(sizehint)
        while chunk:
            for char in chunk:
                hist[char] = hist.get(char,0) + 1
            chunk = source.read(sizehint)
    else:
        raise TypeError( "source must be a string-like or file-like object" )
    return hist

def most_common(hist, num=1):
    from Dict.Get import getItemIter
    pairs = []
    for pair in getItemIter( hist ):
        pairs.append((pair[1],pair[0]))
    pairs.sort()
    pairs.reverse()
    return pairs[:num]

def first_things(hist, num=1):
    from Dict.Get import getKeyList
    pairs = []
    # things = hist keys
    things = getKeyList( hist )
    things.sort()
    for thing in things:
        pairs.append((thing,hist[thing]))
    pairs.sort()
    return pairs[:num]

if __name__ == '__main__':
    #
    from os.path    import join
    from sys        import argv, stdout
    from inspect    import stack
    #
    from Dir.Get    import sTempDir
    #
    if len(argv) > 1:
        sReadFile = argv[1]
        oOutFile  = stdout
    else:
        sReadFile = stack()[0][1]
        oOutFile  = open( join( sTempDir, 'histogram_test_output.txt' ), 'w' )
    #
    hist = word_histogram(open( sReadFile ))
    #
    for pair in most_common(hist,len(hist)):
        print3( pair[1],'\t',pair[0], file = oOutFile )
