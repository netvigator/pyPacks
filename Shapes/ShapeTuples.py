#!/usr/bin/pythonTest
#
# Shape tuples get shapefiles as tuples
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
# Copyright 2012 Rick Graves
#
# depends on python-pyshp

from Iter.AllVers   import iRange
from Numb.Test      import areEquals

def getShapeObject( sFileSpec ):
    #
    from sys            import exc_info
    #
    from shapefile      import Reader
    #
    from File.Get       import FileNotThereError
    from File.Test      import isFileThere 
    #
    error = msg = ''
    oShapeFile  = None
    #
    if not sFileSpec.lower().endswith( '.shp' ):
        #
        sShapeFileName = sFileSpec + '.shp'
        sShapeFileNAME = sFileSpec + '.SHP'
        #
    #
    if (    isFileThere( sFileSpec      ) or
            isFileThere( sShapeFileName ) or
            isFileThere( sShapeFileNAME ) ):
        #
        pass
        #
    else:
        #
        raise FileNotThereError( sFileSpec )
        #
    #
    oShapeFile = Reader( sFileSpec )
    #
    return oShapeFile


def getShapeTuplesOffObject( oShapeFile ):
    #
    from Iter.AllVers import tMap
    #
    tBBox = tuple( oShapeFile.bbox )
    #
    oShapes = oShapeFile.shapes()
    #
    lPoints = []
    #
    iShapeLen = len( oShapes )
    #
    for i in iRange( iShapeLen ):
        #
        lPoints.append( tMap( tuple, oShapes[i].points  )  )
        #
    #
    tPoints = tuple( lPoints )
    #
    tBBoxes = [ tuple( oShapes[i].bbox  ) for i in iRange( iShapeLen ) ]
    #
    tParts  = [ tuple( oShapes[i].parts ) for i in iRange( iShapeLen ) ]
    #
    oShapes = lPoints = None # cut down on memory useage
    #
    return tBBox, tPoints, tuple( tBBoxes ), tuple( tParts )



def getShapeTuples( sFileSpec ):
    #
    tBBox = tPoints = ()
    #
    oShapeFile = getShapeObject( sFileSpec )
    #
    tBBox, tPoints, tBBoxes, tParts = getShapeTuplesOffObject( oShapeFile )
    #
    oShapeFile = None # cut down on memory useage
    #
    return tBBox, tPoints, tBBoxes, tParts



def getPointsBoundingBox( tPoints ):
    #
    nMaxX = nMinX = tPoints[0][0][0]
    nMaxY = nMinY = tPoints[0][0][1]
    #
    for i in iRange( len( tPoints ) ):
        #
        for j in iRange( len( tPoints[i] ) ):
            #
            nMaxX = max( nMaxX, tPoints[i][j][0] )
            nMinX = min( nMinX, tPoints[i][j][0] )
            #
            nMaxY = max( nMaxY, tPoints[i][j][1] )
            nMinY = min( nMinY, tPoints[i][j][1] )
            #
        #
    #
    return nMinX, nMinY, nMaxX, nMaxY



def _getPointsTouchingBBox(
        tPoints, tBBox = None, areCloseEnough = areEquals ):
    #
    from copy         import deepcopy
    #
    from Iter.AllVers import tRange, iReverseRange
    from Numb.Test    import getCloseEnoughTester
    #
    iShapes = tRange( len( tPoints ) )
    #
    if tBBox is None: tBBox = getPointsBoundingBox( tPoints )
    #
    nMinX, nMinY, nMaxX, nMaxY = tBBox
    #
    lCoordinatesMinX = [ [ [], [], [], [] ] for i in iShapes  ]
    lCoordinatesMinY = [ [ [], [], [], [] ] for i in iShapes  ]
    lCoordinatesMaxX = [ [ [], [], [], [] ] for i in iShapes  ]
    lCoordinatesMaxY = [ [ [], [], [], [] ] for i in iShapes  ]
    #
    lPointIndexsMinX = deepcopy( lCoordinatesMinX )
    lPointIndexsMinY = deepcopy( lCoordinatesMinY )
    lPointIndexsMaxX = deepcopy( lCoordinatesMaxX )
    lPointIndexsMaxY = deepcopy( lCoordinatesMaxY )
    #
    bGotMinX = bGotMinY = bGotMaxX = bGotMaxY = False
    #
    for i in iRange( len( tPoints ) ):
        #
        for j in iRange( len( tPoints[i] ) ):
            #
            if areCloseEnough( tPoints[i][j][0], nMinX ):
                #
                lCoordinatesMinX[i][0].append( tPoints[i][j] )
                lPointIndexsMinX[i][0].append( j )
                #
                bGotMinX = True
                #
            if areCloseEnough( tPoints[i][j][1], nMinY ):
                #
                lCoordinatesMinY[i][1].append( tPoints[i][j] )
                lPointIndexsMinY[i][1].append( j )
                #
                bGotMinY = True
                #
            if areCloseEnough( tPoints[i][j][0], nMaxX ):
                #
                lCoordinatesMaxX[i][2].append( tPoints[i][j] )
                lPointIndexsMaxX[i][2].append( j )
                #
                bGotMaxX = True
                #
            if areCloseEnough( tPoints[i][j][1], nMaxY ):
                #
                lCoordinatesMaxY[i][3].append( tPoints[i][j] )
                lPointIndexsMaxY[i][3].append( j )
                #
                bGotMaxY = True
                #
            #
        #
    #
    # float errors can get you
    # closeEnoughDot13 = getCloseEnoughTester( 13 )
    #
    while ( areCloseEnough == areEquals and
            not ( bGotMinX and bGotMinY and bGotMaxX and bGotMaxY ) ):
        #
        for i in iReverseRange( 14 ):
            #
            closeEnough = getCloseEnoughTester( i )
            #
            t = _getPointsTouchingBBox( tPoints, tBBox, closeEnough )
            #
            tGots = t[2]
            #
            if tGots[0] and not bGotMinX:
                #
                lCoordinatesMinX = t[0][0]
                lPointIndexsMinX = t[1][0]
                #
                bGotMinX = True
                #
            if tGots[1] and not bGotMinY:
                #
                lCoordinatesMinY = t[0][1]
                lPointIndexsMinY = t[1][1]
                #
                bGotMinY = True
                #
            if tGots[2] and not bGotMaxX:
                #
                lCoordinatesMaxX = t[0][2]
                lPointIndexsMaxX = t[1][2]
                #
                bGotMaxX = True
                #
            if tGots[3] and not bGotMaxY:
                #
                lCoordinatesMaxY = t[0][3]
                lPointIndexsMaxY = t[1][3]
                #
                bGotMaxY = True
                #
            #
            if bGotMinX and bGotMinY and bGotMaxX and bGotMaxY:
                #
                # print 'success at level %s' % i
                break
                #
            #
        #
    #
    return (
      ( lCoordinatesMinX,
        lCoordinatesMinY,
        lCoordinatesMaxX,
        lCoordinatesMaxY ),
      ( lPointIndexsMinX,
        lPointIndexsMinY,
        lPointIndexsMaxX,
        lPointIndexsMaxY ),
      ( bGotMinX,
        bGotMinY,
        bGotMaxX,
        bGotMaxY ) )


def getPointsTouchingBBox( tPoints, tBBox = None, areCloseEnough = areEquals ):
    #
    t = _getPointsTouchingBBox( tPoints, tBBox, areCloseEnough )
    #
    return t[ : 2 ]


def getPointCountsTouchingBBox( tBBox, tPoints ):
    #
    tCoordinates, tPointIndexs = getPointsTouchingBBox( tPoints, tBBox )
    #
    (   lCoordinatesMinX,
        lCoordinatesMinY,
        lCoordinatesMaxX,
        lCoordinatesMaxY ) = tCoordinates
    #
    lPointCounts = [ [ 0 ] * 4 for t in tPoints ]
    #
    for i in iRange( len( tPoints ) ):
        #
        lPointCounts[i][0] = len( lCoordinatesMinX[i][0] )
        lPointCounts[i][1] = len( lCoordinatesMinY[i][1] )
        lPointCounts[i][2] = len( lCoordinatesMaxX[i][2] )
        lPointCounts[i][3] = len( lCoordinatesMaxY[i][3] )
    #
    return lPointCounts



def getCorners( tPoints ):
    #
    '''
    pass points of shape file 
    returns dict as follows {
    'NE': {'coordinates': (9, 5), 'indexes': (1, 2)},
    'NW': {'coordinates': (2, 5), 'indexes': (0, 1)},
    'SE': {'coordinates': (9, 2), 'indexes': (1, 3)},
    'SW': {'coordinates': (2, 2), 'indexes': (0, 0)} }
    '''
    #
    # SE corner max X & min Y so max X - Y
    # NE corner max Y & max Y so max X + Y
    # NW corner min X & max Y so max Y - X
    # SW corner min X & min Y so max -1 * ( X + Y ), i.e., min X + Y
    #
    def getValuSE( t ): return        t[0] - t[1]
    def getValuNE( t ): return        t[0] + t[1]
    def getValuNW( t ): return        t[1] - t[0]
    def getValuSW( t ): return -1 * ( t[0] + t[1] )
    #
    tSE = tPoints[0][0]
    tNE = tPoints[0][0]
    tNW = tPoints[0][0]
    tSW = tPoints[0][0]
    #
    nSE = getValuSE( tSE )
    nNE = getValuNE( tNE )
    nNW = getValuNW( tNW )
    nSW = getValuSW( tSW )
    #
    iSE = 0, 0
    iNE = 0, 0
    iNW = 0, 0
    iSW = 0, 0
    #
    for i in iRange( len( tPoints ) ):
        #
        for j in iRange( len( tPoints[i] ) ):
            #
            tTest = tPoints[i][j]
            #
            nTestSE = getValuSE( tTest )
            nTestNE = getValuNE( tTest )
            nTestNW = getValuNW( tTest )
            nTestSW = getValuSW( tTest )
            #
            if nTestSE > nSE:
                #
                nSE = nTestSE
                tSE = tTest
                iSE = i, j
                #
            if nTestNE > nNE:
                #
                nNE = nTestNE
                tNE = tTest
                iNE = i, j
                #
            if nTestNW > nNW:
                #
                nNW = nTestNW
                tNW = tTest
                iNW = i, j
                #
            if nTestSW > nSW:
                #
                nSW = nTestSW
                tSW = tTest
                iSW = i, j
                #
            #
        #
    #
    return dict(
        SE = dict( indexes = iSE, coordinates = tSE ),
        NE = dict( indexes = iNE, coordinates = tNE ),
        NW = dict( indexes = iNW, coordinates = tNW ),
        SW = dict( indexes = iSW, coordinates = tSW ) )


if __name__ == "__main__":
    #
    from pprint         import pprint
    #
    from File.Get       import FileNotThereError
    from Utils.Result   import sayTestResult
    #
    from In_or_Out      import getExampleShapeObject
    #
    lProblems = []
    #
    # problem is you need a shape file to test
    #
    oShapeFile = getExampleShapeObject()
    #
    tBBox, tPoints, tBBoxes, tParts = getShapeTuplesOffObject( oShapeFile )
    #
    if not ( tBBox == getPointsBoundingBox( tPoints ) == (3, 0, 13, 12) ):
        #
        lProblems.append(
            'getPointsBoundingBox() incorrect result' )
        #
    #
    tTouchPoints = (
        ([[[(3, 6), (3, 6)], [], [], []],
          [[], [], [], []],
          [[(3, 2), (3, 2)], [], [], []]],
        [[[], [(9, 0)], [], []], [[], [], [], []], [[], [(5, 0)], [], []]],
        [[[], [], [(13, 4)], []], [[], [], [], []], [[], [], [], []]],
        [[[], [], [], [(9, 12)]], [[], [], [], []], [[], [], [], []]]),
        ([[[0, 10], [], [], []], [[], [], [], []], [[5, 9], [], [], []]],
        [[[], [9], [], []], [[], [], [], []], [[], [8], [], []]],
        [[[], [], [8], []], [[], [], [], []], [[], [], [], []]],
        [[[], [], [], [1]], [[], [], [], []], [[], [], [], []]])
    )
    if getPointsTouchingBBox( tPoints, tBBox ) != tTouchPoints:
        #
        pprint( getPointsTouchingBBox( tPoints, tBBox ) )
        lProblems.append(
            'getPointsTouchingBBox() getExampleShapeObject()' )
        #
    #
    lWantPointCounts = [[2, 1, 1, 1], [0, 0, 0, 0], [2, 1, 0, 0]]
    #
    if getPointCountsTouchingBBox( tBBox, tPoints ) != lWantPointCounts:
        #
        pprint( getPointCountsTouchingBBox( tBBox, tPoints ) )
        lProblems.append(
            'getPointCountsTouchingBBox() getExampleShapeObject()' )
        #
    #
    dWant = {
        'NE': {'coordinates': ( 9, 12), 'indexes': (0, 1)},
        'NW': {'coordinates': ( 3,  6), 'indexes': (0, 0)},
        'SE': {'coordinates': (13,  4), 'indexes': (0, 8)},
        'SW': {'coordinates': ( 3,  2), 'indexes': (2, 5)}}
    #
    if getCorners( tPoints ) != dWant:
        #
        pprint( getCorners( tPoints ) )
        lProblems.append( 'getCorners()' )
        #
    #
    tPoints = (
      ( ( 2, 2 ),
        ( 2, 9 ),
        ( 9, 9 ),
        ( 9, 2 ),
        ( 2, 2 ) ), ) # one simple box in shape file 
    #
    #
    dWant = {
        'NE': {'coordinates': (9, 9), 'indexes': (0, 2)},
        'NW': {'coordinates': (2, 9), 'indexes': (0, 1)},
        'SE': {'coordinates': (9, 2), 'indexes': (0, 3)},
        'SW': {'coordinates': (2, 2), 'indexes': (0, 0)}}
    #
    if getCorners( tPoints ) != dWant:
        #
        pprint( getCorners( tPoints ) )
        lProblems.append( 'getCorners() one box shape file' )
        #
    #
    tPoints = (
      ( ( 2, 2 ),
        ( 2, 5 ),
        ( 5, 5 ),
        ( 5, 2 ),
        ( 2, 2 ) ),
      ( ( 5, 2 ),
        ( 2, 5 ),
        ( 9, 5 ),
        ( 9, 2 ),
        ( 5, 2 ) ), ) # two boxes in shape file 
    #
    #pprint( getCorners( tPoints ) )
    #
    dWant = {
        'NE': {'coordinates': (9, 5), 'indexes': (1, 2)},
        'NW': {'coordinates': (2, 5), 'indexes': (0, 1)},
        'SE': {'coordinates': (9, 2), 'indexes': (1, 3)},
        'SW': {'coordinates': (2, 2), 'indexes': (0, 0)} }
    #
    if getCorners( tPoints ) != dWant:
        #
        pprint( getCorners( tPoints ) )
        lProblems.append( 'getCorners() two box shape file' )
        #
    #
    tPoints = (
      ( ( 2, 2 ),
        ( 2, 5 ),
        ( 5, 5 ),
        ( 5, 2 ),
        ( 2, 2 ) ),
      ( ( 5, 2 ),
        ( 2, 5 ),
        ( 9, 5 ),
        ( 9, 2 ),
        ( 5, 2 ) ),
      ( ( 2, 5 ),
        ( 2, 9 ),
        ( 9, 9 ),
        ( 9, 5 ),
        ( 2, 5 ) ), ) # three boxes one on top
    #
    dWant = {
        'NE': {'coordinates': (9, 9), 'indexes': (2, 2)},
        'NW': {'coordinates': (2, 9), 'indexes': (2, 1)},
        'SE': {'coordinates': (9, 2), 'indexes': (1, 3)},
        'SW': {'coordinates': (2, 2), 'indexes': (0, 0)}
        }
    #
    if getCorners( tPoints ) != dWant:
        #
        pprint( getCorners( tPoints ) )
        lProblems.append( 'getCorners() three box shape file' )
        #
    #
    #
    try:
        #
        sFileSpec = (
            '/home/Common/USCongressDistricts2012/WI/'
            'xyz' )
        #
        tBBox, tPoints, tBBoxes, tParts = getShapeTuples( sFileSpec )
        #
    except FileNotThereError:
        #
        pass
        #
    else:
        #
        lProblems.append(
            'getShapeObject() should have raised a FileNotThereError' )
        #
    #
    sFileSpec = ( '/home/Common/USCongressDistricts2012/WI/'
                  'Congressional_2012_GEO' )
    #
    tBBox, tPoints, tBBoxes, tParts = getShapeTuples( sFileSpec )
    #
    tCoordinates, tPointIndexs = getPointsTouchingBBox( tPoints, tBBox )
    #
    #pprint( tCoordinates )
    #pprint( tPointIndexs )
    #pprint( getPointCountsTouchingBBox( tBBox, tPoints ) )
    #
    sFileSpec = ( '/home/Common/USCongressDistricts2012/WI/'
                  'Act_44_Congressional_Districts.shp' )
    #
    tBBox, tPoints, tBBoxes, tParts = getShapeTuples( sFileSpec )
    #
    tCoordinates, tPointIndexs = getPointsTouchingBBox( tPoints, tBBox )
    #
    #pprint( tCoordinates )
    #pprint( tPointIndexs )
    #pprint( getPointCountsTouchingBBox( tBBox, tPoints ) )
    #
    sFileSpec = ( '/home/Common/USCongressDistricts2012/OR/'
                  'Congressional_Area_Changes.shp' )
    #
    tBBox, tPoints, tBBoxes, tParts = getShapeTuples( sFileSpec )
    #
    tCoordinates, tPointIndexs = getPointsTouchingBBox( tPoints )
    #
    #pprint( tCoordinates )
    #pprint( tPointIndexs )
    #pprint( getPointCountsTouchingBBox( tBBox, tPoints ) )
    # print tBBox
    #
    #
    sayTestResult( lProblems ) 