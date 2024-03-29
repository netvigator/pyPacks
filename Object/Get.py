#!/home/rick/.local/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Object functions get
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
# Copyright 2004-2023 Rick Graves
#

# note getObjFromFileContent() and PutReprInTemp() are in File.Get & File.Write
# note getObjFromFileContent() and PutReprInTemp() are in File.Get & File.Write
# note getObjFromFileContent() and PutReprInTemp() are in File.Get & File.Write
# note getObjFromFileContent() and PutReprInTemp() are in File.Get & File.Write

import inspect

from pprint                 import pprint, pformat
from random                 import shuffle
from string                 import digits
from string                 import ascii_letters as letters

try:
    from ..Collect.Cards    import ShuffleAndCut
    from ..Dict.Get         import getKeyIter
    from ..Iter.AllVers     import lRange, tFilter, tZip
    from ..Dict.Get         import getKeyList
    from ..Utils.Both2n3    import PYTHON3
except ( ValueError, ImportError ):
    from Collect.Cards      import ShuffleAndCut
    from Dict.Get           import getKeyIter
    from Iter.AllVers       import lRange, tFilter, tZip
    from Dict.Get           import getKeyList
    from Utils.Both2n3      import PYTHON3


class QuickObject( object ):
    #
    '''
    This only returns an object.
    You would probably use this to add values later, like this:.
    Colors          = QuickObject()
    Colors.alarm    = 'red'
    Colors.warning  = 'orange'
    Colors.normal   = 'green'
    Also take a look at ValueContainer,
    which can pre-load values with less typing.
    '''
    pass



class ValueContainer( object ):
    #
    """No need for self.foo = foo, self.bar = bar, etc.
    From "Collecting a Bunch of Named Items" in Python Cookbook."""
    #
    def __init__( self, **kwargs ):
        #
        self.__dict__.update( kwargs )



class ObjectCanPrint( object ):
    #
    def __str__( self ): # print() calls this
        #
        lItems = [  ( k, v )
                    for k, v in self.__dict__.items()
                    if not k.startswith( '__' ) ]
        #
        lItems.sort()
        #
        return '\n'.join( '  %s: %s' % t for t in lItems )
    #

    def __repr__(self): # pprint() calls this
        #
        return '\n%s' % pformat( vars(self), indent=4, width=1 )


class ValueContainerCanPrint( ObjectCanPrint, ValueContainer ):

    pass


class BufferClass( object ):
    """
    email.Generator.Generator() requires an output file as argument,
    or another storage object that supports write methods.
    Writing to files is adequate for larger messages, but keeping the
    process in the buffer is better when the messages are to be sent
    immediately and large memmory is not required.
    http://mail.python.org/pipermail/tutor/2004-August/031524.html
    """
    #
    # only called here
    #
    def __init__(self):
        self.lContents = []

    def write(self,var):
        self.lContents.append( var )

    def read(self):
        return ''.join( self.lContents )

    def close(self):
        "Just to be compliant with files"
        return True


class SequencerClass( object ):
    #
    '''call o.getNextInSeq() or self.getNextInSeq() to get next in sequence'''
    #
    def __init__( self ):
        #
        self.iLast = -1
        #
    def getNextInSeq( self ):
        #
        self.iLast += 1
        #
        return self.iLast
        #
    def __next__( self ): return self.getNextInSeq()
    def   next(   self ): return self.getNextInSeq()



class RandomFeeder( object ):
    #
    def __init__ ( self,
                   uListDict,
                   bRecycle          = False,
                   bShuffleOnRecycle = False,
                   bShuffle          = True ):
        #
        #
        if isinstance( uListDict, dict ): # dictionary
            #
            self.lList          = getKeyList( uListDict )
            #
        else:
            #
            self.lList          = list( uListDict )
            #
        # self.lList            = lList
        #
        self.lSeq               = lRange( len( self.lList ) )
        self.iNext              = 0
        self.bRecycle           = bRecycle
        self.bShuffleOnRecycle  = bShuffleOnRecycle
        self.iSequence          = 0
        #
        if bShuffle:            self.doShuffle()


    def __len__( self ):
        #
        return len( self.lList )


    def next( self ): return self.getNextOne()

    def __next__( self ): return self.getNextOne()

    def doShuffle( self ):
        #
        #
        shuffle( self.lSeq )
        #
        self.lSeq   = ShuffleAndCut( self.lSeq, iShuffles = 1 )
        #


    def getNextOne( self ):
        #
        if self.iNext >= len( self.lList ):
            #
            if self.bRecycle:
                #
                if self.bShuffleOnRecycle: self.doShuffle()
                #
                self.iNext = 1
                #
            else:
                #
                self.iNext = len( self.lList ) + 1
                #
                return None
                #
            #
        else:
            #
            self.iNext += 1
            #
        #
        self.iSequence  += 1
        #
        return self.lList[ self.lSeq[ self.iNext - 1 ] ]



    def getNextSome( self, iHowMany ):
        #
        lReturn = []
        #
        iWantHowMany    = iHowMany
        #
        if iHowMany > len( self.lList ):  iHowMany = len( self.lList )
        #
        while iHowMany > 0:
            #
            iHowManyBeg = 0
            iHowManyEnd = iHowMany
            #
            if self.iNext > len( self.lList ): self.iNext = len( self.lList )
            #
            if self.iNext + iHowMany > len( self.lList ):
                #
                #
                iHowManyEnd     = len( self.lList ) - self.iNext
                # iHowManyEnd     = len( self.lList ) - self.iNext
                #
                if self.bRecycle:
                    #
                    iHowManyBeg = iHowMany - iHowManyEnd
                    #
            #
            if iHowManyEnd > 0:
                #
                lGetThese   = self.lSeq[ self.iNext : self.iNext + iHowManyEnd ]
                #
                iHowMany   -= len( lGetThese )
                #
                lReturn     = [ self.lList[ iThisOne ] for iThisOne in lGetThese ]
                #
                self.iNext += iHowManyEnd
                #
            #
            #
            if iHowManyBeg > 0:
                #
                if self.bShuffleOnRecycle: self.doShuffle()
                #
                lGetThese   = self.lSeq[ : iHowManyBeg ]
                #
                iHowMany   -= len( lGetThese )
                #
                lReturn    += [ self.lList[ iThisOne ] for iThisOne in lGetThese ]
                #
                self.iNext  = iHowManyBeg
                #
            #
        #
        self.iSequence      += iHowMany
        #
        if iHowMany > 0 and iWantHowMany > iHowMany:
            #
            iMultiplier     = ( iWantHowMany // iHowMany ) + 1
            #
            lReturn         *= iMultiplier
            #
            lReturn         = lReturn[ : iWantHowMany ]
            #
            self.iSequence  = iWantHowMany % len( self.lSeq )
            #
        #
        return lReturn


    def Reset(self):
        #
        self.iNext  = 0
        #
        self.doShuffle()


    def getWholeList(self):
        #
        """Returns list in random order."""
        #
        # not used anywhere
        #
        return [ self.lList[ iThisOne ] for iThisOne in self.lSeq ]


    def ListDump(self):
        #
        """Returns original sequence."""
        #
        return self.lList


    def append( self, uItem ):
        #
        self.lSeq.append( len( self.lList ) )
        #
        self.lList.append( uItem )
        #
        self.doShuffle()


    def extend( self, lItems ):
        #
        iStartLen = len( self.lList )
        #
        self.lSeq.extend( iRange( iStartLen, iStartLen + len( lItems ) ) )
        #
        self.lList.extend( list( lItems ) )
        #
        self.doShuffle()


    def __len__( self ):
        #
        return len( self.lList )


    def hasMoreToDo( self ):
        #
        return self.bRecycle or self.iNext < len( self.lList )


    def getHowManyhasMoreToDo( self ):
        #
        return len( self.lList ) - self.iNext


class _RandomLettersAndNumbers( RandomFeeder ):
    #
    # only called here
    #
    def __init__( self ):
        #
        sLettersNumbers = digits + letters + digits
        #
        RandomFeeder.__init__(
                self, sLettersNumbers,
                bRecycle          = True,
                bShuffleOnRecycle = True )


    def getNextSome( self, iHowMany ):
        #
        lLettersNumbers = RandomFeeder.getNextSome( self, iHowMany )
        #
        return ''.join( lLettersNumbers )



class Null( object ):
    #
    def __init__( self, *args, **kwargs ):  pass
    def __call__( self, *args, **kwargs ):  return None
    def __repr__( self ):                   return "Null()"
    def __nonzero__( self ):                return False
    def __getattr__( self, name ):          return None
    def __setattr__( self, name, value ):   return None
    def __delattr__( self, name ):          return None




class StreamNull( object ):
    #
    def write( self, sText ): pass # supress generic warnings





def _notHidden( sProperty ):
    #
    return not sProperty.startswith( '_' )


def _getObjProperties( oObj ):
    #
    #
    return tFilter( _notHidden, getKeyIter( oObj.__dict__ ) )



def getAllPropertyValues( oObj ):
    #
    """
    returns a tuple of all the property's values
    """
    #
    # not used anywhere
    #
    #
    tProperties = _getObjProperties( oObj )
    #
    lValues     = [ oObj.__dict__.get( sProperty, None ) for sProperty in tProperties ]
    #
    return tZip( tProperties, lValues )


def getPropertyValue( oObj, sProperty ):
    #
    """
    returns the value for one property, returns None if no such property
    """
    # works for dictionaries or objects
    #
    try:
        #
        uValue  = oObj.__dict__.get( sProperty, None )
        #
    except AttributeError:
        #
        uValue  = oObj.get( sProperty, None )
        #
    #
    return uValue


def getPropertyValueList( oObj, *args ):
    #
    """
    pass a list, get a list
    """
    #
    return [ getPropertyValue( oObj, sProperty ) for sProperty in args ]


def getDictOffObject( oObj ):
    #
    return oObj.__dict__




if PYTHON3:

    def getName( uVar ):
        """
        Gets the name of var or object.
        Does it from the out most frame inner-wards.
        :param var: variable to get name from.
        :return: string
        https://stackoverflow.com/questions/18425225/getting-the-name-of-a-variable-as-a-string/18425523
        caveat: watch out of more than one var points to the same object
        """
        for fi in reversed( inspect.stack() ):
            names = [   var_name for var_name, var_val
                        in fi.frame.f_locals.items()
                        if var_val is uVar ]
            if names:
                return names[0]

else:

    def getName( uVar ):
        """
        Gets the name of var or object.
        :param var: variable to get name from.
        :return: string
        https://stackoverflow.com/questions/18425225/getting-the-name-of-a-variable-as-a-string/18425523
        caveat: watch out of more than one var points to the same object
        """
        callers_local_vars = inspect.currentframe().f_back.f_locals.items()
        #
        names = [   var_name for var_name, var_val
                    in callers_local_vars
                    if var_val is uVar ]
        #
        if names:
            return names[0][0]


if __name__ == "__main__":
    #
    from string         import digits
    from string         import ascii_letters as letters
    #
    from six            import print_ as print3
    from six            import next   as getNext
    #
    from Collect.Test   import isSeq1SubsetOfSeq2
    from Iter.AllVers   import iRange, lRange
    from Object.Set     import _getsAttributesFromKWArgs
    from Utils.Both2n3  import print3
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    oBuffer = BufferClass()
    #
    oBuffer.write( 'a' )
    oBuffer.write( 'b' )    
    oBuffer.write( 'c' )
    #
    if oBuffer.read() != 'abc':
        #
        lProblems.append( 'BufferClass() output' )
        #
    #
    if not oBuffer.close():
        #
        lProblems.append( 'BufferClass() close' )
        #
    #
    oValueCont  = ValueContainer(
                        a = 1, b = 2, c = 3 )
    #
    dValues     = dict( a = 1, b = 2, c = 3 )
    #
    if oValueCont.a != 1 or oValueCont.b != 2 or oValueCont.c != 3:
        #
        lProblems.append( 'ValueContainer()' )
        #
    #
    oTest       = _getsAttributesFromKWArgs(
                        a = 1, b = 2, c = 3 )
    #
    if oTest.__dict__ != oValueCont.__dict__:
        #
        lProblems.append( 'getAttributesFromDict & ValueContainer not same' )
        #
    #
    oValueCont  = ValueContainerCanPrint(
                        a = 1, b = 2, c = 3 )
    #
    sExpect = '  a: 1\n  b: 2\n  c: 3'
    #
    if str( oValueCont ) != sExpect:
        #
        lProblems.append( 'str( oValueContainer )' )
        #
    #
    sExpect = '\n'.join(  [ '  %s: %s' % t 
                            for t 
                            in ( ('a', 1), ('b', 2), ('c', 3) ) ] )
    #
    if str( oValueCont ) != sExpect:
        #
        lProblems.append( 'str( oValueCont ) not coming out right' )
        #
    #
    sOut = oValueCont.__repr__()
    #
    sExpect = '''
{   'a': 1,
    'b': 2,
    'c': 3}'''
    #
    if sOut != sExpect:
        #
        lProblems.append( 'oValueCont.__repr__() not coming out right' )
        #
    #
    oTest = RandomFeeder( letters )
    #
    s2chars = oTest.getNextSome( 2 )
    lRandom = oTest.getWholeList()
    lAll    = oTest.ListDump()
    #
    if getNext( oTest ) not in letters:
        #
        lProblems.append( 'RandomFeeder() getNext( oTest ) not in letters' )
        #
    #
    if s2chars[0] not in letters:
        #
        lProblems.append( 'RandomFeeder() s2chars[0] not in letters' )
        #
    #
    if s2chars[1] not in letters:
        #
        lProblems.append( 'RandomFeeder() s2chars[1] not in letters' )
        #
    #
    if not isSeq1SubsetOfSeq2( lAll, letters ):
        #
        lProblems.append( 'RandomFeeder() isSeq1SubsetOfSeq2( lAll, letters )' )
        #
    #
    if not isSeq1SubsetOfSeq2( lRandom, letters ):
        #
        lProblems.append( 'RandomFeeder() isSeq1SubsetOfSeq2( lRandom, letters' )
        #
    #
    #
    oTest.append( '$' )
    oTest.extend( digits )
    #
    if oTest.__len__() != 63:
        #
        print3( 'oTest.__len__():', oTest.__len__() )
        lProblems.append( 'RandomFeeder() oTest.__len__() != 63' )
        #
    #
    if not oTest.hasMoreToDo():
        #
        lProblems.append( 'RandomFeeder() not oTest.hasMoreToDo()' )
        #
    #
    if oTest.getHowManyhasMoreToDo() != 60:
        #
        lProblems.append( 'RandomFeeder() oTest.getHowManyhasMoreToDo() != 60' )
        #
    #
    if oTest.Reset():
        #
        lProblems.append( 'RandomFeeder() oTest.Reset()' )
        #
    #
    #
    oRandomAlphaNum = _RandomLettersAndNumbers()
    #
    if getNext( oRandomAlphaNum ) not in letters + digits:
        #
        lProblems.append( '_RandomLettersAndNumbers()' )
        #
    #
    oNull = Null( object )
    #
    bError      = False
    #
    try:
        del oNull.What
        uTest   = oNull.What
    except:
        print3( 'bError' )
        bError  = True
    #
    if bError or oNull() or oNull.What:
        #
        if oNull(): print3( 'type( oNull() ):', type( oNull() ) )
        if oNull.What: print3( 'type( oNull.What ):', type( oNull.What ) )
        lProblems.append( 'Null()' )
        #
    #
    oStreamNull = StreamNull()
    #
    if oStreamNull.write( 'How now brown cow.' ):
        #
        lProblems.append( 'StreamNull()' )
        #
    #
    lReturned = list( _getObjProperties( oRandomAlphaNum ) )
    lExpected = ['bRecycle', 'bShuffleOnRecycle',
                 'iNext', 'iSequence', 'lList', 'lSeq']
    #
    lReturned.sort()
    lExpected.sort()
    #
    if lReturned != lExpected:
        #
        lProblems.append( '_getObjProperties()' )
        #
    #
    lReturned = list( getAllPropertyValues( oValueCont ) )
    lExpected = [ ('a', 1), ('c', 3), ('b', 2) ]
    #
    lReturned.sort()
    lExpected.sort()
    #
    if lReturned != lExpected:
        #
        lProblems.append( 'getAllPropertyValues()' )
        #
    #
    dTest = dict( a = 1, b = 2, c = 3 )
    #
    if      getPropertyValue( oValueCont, 'a' ) != 1 or \
            getPropertyValue( oValueCont, 'd' )      or \
            getPropertyValue( dTest,      'a' ) != 1 or \
            getPropertyValue( dTest,      'd' ):
        #
        lProblems.append( 'getPropertyValue()' )
        #
    if getPropertyValueList( oValueCont, 'a','b','c' ) != [1, 2, 3]:
        #
        lProblems.append( 'getPropertyValueList()' )
        #
    #
    if getDictOffObject( oValueCont ) != dValues:
        #
        lProblems.append( 'getDictOffObject()' )
        #
    #
    oSequencer = SequencerClass()
    #
    lSequence = [ getNext( oSequencer ) for i in iRange(10) ]
    #
    if lSequence != lRange(10):
        #
        print3( lSequence )
        lProblems.append( 'SequencerClass()' )
        #
    #
    x,y,z = 1,2,3
    #
    if getName( x ) != 'x':
        #
        print3( 'getName( x )' )
        lProblems.append( 'getName( x )' )
        #
    #
    if getName( y ) != 'y':
        #
        print3( 'getName( y )' )
        lProblems.append( 'getName( y )' )
        #
    #
    if getName( z ) != 'z':
        #
        print3( 'getName( z )' )
        lProblems.append( 'getName( z )' )
        #
    #
    sayTestResult( lProblems )
