#!/usr/bin/pythonTest
#
# Shape functions in_or_out
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

# based on
# Improved point in polygon test which includes edge
# and vertex points
# by Joel Lawhead, PMP
# http://geospatialpython.com/2011/08/point-in-polygon-2-on-line.html

from Numb.Test import getCloseEnoughTester

closeEnoughDot13 = getCloseEnoughTester( 13 ) # within 0.0000000000001 % !!!


def _isBetweenPoints( n, p1, p2 ):
    #
    return min( p1, p2 ) < n < max( p1, p2 )


def _isPointWithinBoundingBox( x, y, lBoundingBox ):
    #
    nMinX, nMinY, nMaxX, nMaxY = lBoundingBox
    #
    return nMinX <= x <= nMaxX and nMinY <= y <= nMaxY




def getBoundingBox( oPoly ):
    #
    from Shapes.ShapeTuples import getPointsBoundingBox
    #
    nMinX, nMinY, nMaxX, nMaxY = getPointsBoundingBox( ( oPoly, ) )
    #
    return nMinX, nMinY, nMaxX, nMaxY

    

    
_tAllResults = ( "IN", "ON_BOUNDARY", "ON_VERTEX", "OUT", "OUT_OF_BOUNDS" )


def point_in_poly_verbose( x, y, oPoly, tParts = (0,), lBoundingBox = None ):
    #
    '''
    function will return whether a point is within a polynomial
    pass
    x, y the coordinates of the point to be tested
    oPoly the points defining the polynomial
    tParts the index of the start point
      if there is only one polynomial, it will always be (0,) or [0]
      if the polynomial is a multi, one starting index for each one
    lBoundingBox is the bounding box if available
    this 
    '''
    from Iter.AllVers import iRange
    from Iter.Get     import getSequencePairsThisWithNext as getWithNext
    #
    if lBoundingBox is None :
        #
        lBoundingBox = getBoundingBox( oPoly )
        #
    #
    if not _isPointWithinBoundingBox( x, y, lBoundingBox ):
        #
        return "OUT_OF_BOUNDS"
        #
    #
    iPolyLen = len( oPoly )
    #
    if len( tParts ) > 1:
        #
        lPoly = list( oPoly )
        #
        lMoreParts = list( tParts )
        #
        lMoreParts.append( iPolyLen + 1 )
        #
        def point_in_poly( lPart ):
            #
            return point_in_poly_verbose( x, y, lPart )
        #
        tParts = [ lPoly[ t[0] : t[1] ] for t in getWithNext( lMoreParts ) ]
        #
        lResults = [ point_in_poly( lPart ) for lPart in tParts ]
        #
        for sResult in _tAllResults:
            #
            if sResult in lResults:
                #
                return sResult
    #
    # check if point is a vertex
    #
    if isinstance( oPoly[0], list ):
        uTest = [x,y]
    else:
        uTest = (x,y)
    #
    if uTest in oPoly: return "ON_VERTEX"
    #
    x,y = float( x ), float( y )
    #
    # check if point is on a boundary
    #
    for i in iRange( iPolyLen - 1 ):
        #
        p1 = oPoly[i]
        p2 = oPoly[i+1]
        #
        bBetweenPointsX = _isBetweenPoints( x, p1[0], p2[0] )
        bBetweenPointsY = _isBetweenPoints( y, p1[1], p2[1] )
        #
        # horizontal boundary
        if  (   p1[1] == p2[1] and
                closeEnoughDot13( p1[1], y ) and
                bBetweenPointsX ):
            return "ON_BOUNDARY"
        #
        # vertical boundary
        if  (   p1[0] == p2[0] and 
                closeEnoughDot13( p1[0], x ) and
                bBetweenPointsY ):
            return "ON_BOUNDARY"
        #
        risePoly = p2[1] - float( p1[1] )
        runPoly  = p2[0] - float( p1[0] )
        #
        riseP1 = y - p1[1]
        runP1  = x - p1[0]
        #
        riseP2 = p2[1] - y
        runP2  = p2[0] - x
        #
        if (    runPoly != 0    and
                runP1   != 0    and 
                runP2   != 0    and 
                bBetweenPointsX and
                bBetweenPointsY and
                closeEnoughDot13( risePoly / runPoly, riseP1 / runP1 ) and
                closeEnoughDot13( risePoly / runPoly, riseP2 / runP2 ) ):
            #
            return "ON_BOUNDARY"
            #
    #
    inside = False
    #
    p1x,p1y = oPoly[0]
    for i in iRange( iPolyLen + 1 ):
        p2x,p2y = oPoly[i % iPolyLen]
        if (    min(p1y,p2y) < y <= max(p1y,p2y) and
                               x <= max(p1x,p2x) ):
            if p1y != p2y:
                xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
            if p1x == p2x or x <= xints:
                inside = not inside
        p1x,p1y = p2x,p2y
    #
    if inside: return "IN"
    else:      return "OUT"




def point_in_poly__out_is_out( x,y,oPoly, tParts = (0,), lBoundingBox = None ):
    #
    result = point_in_poly_verbose( x,y,oPoly, tParts, lBoundingBox )
    #
    if result.startswith( 'OUT' ): result = 'OUT'
    #
    return result




setVERTEX_or_BOUNDARY_RESULT = frozenset( ( "ON_VERTEX", "ON_BOUNDARY" ) )


def point_in_poly__edges_are_in( x, y, oPoly, tParts = (0,), lBoundingBox = None ):
    #
    result = point_in_poly__out_is_out( x, y, oPoly, tParts, lBoundingBox )
    #
    if result in setVERTEX_or_BOUNDARY_RESULT:
        return 'IN'
    else:
        return result


def point_in_poly__edges_are_out( x, y, oPoly, tParts = (0,), lBoundingBox = None ):
    #
    result = point_in_poly__out_is_out( x, y, oPoly, tParts, lBoundingBox )
    #
    if result in setVERTEX_or_BOUNDARY_RESULT:
        return 'OUT'
    else:
        return result


def getShapesOnPoint( x, y, oShapeFile ):
    #
    from Iter.AllVers import iRange, tFilter
    #
    if hasattr( oShapeFile, 'bbox'):
        #
        if not _isPointWithinBoundingBox( x, y, oShapeFile.bbox ):
            #
            return []
            #
        #
    #
    oShapes = oShapeFile.shapes()
    #
    #def point_in_poly( o ):
    #   return point_in_poly__out_is_out( x, y, o.points, o.parts, o.bbox )
    #
    #lShapesOnPoint =  [ ( i, point_in_poly( oShapes[i] ) )
    #                    for i in iRange( len( oShapes ) ) ]
    #
    #lShapesOnPoint = [ t for t in lShapesOnPoint if t[1] != 'OUT' ]
    #
    # commented code above could handle overlapping shapes
    #
    # code below assumes non-overlapping shapes, as
    # it stops testing one one shape is found for which point is within
    #
    lShapesOnPoint = []
    #
    for i in iRange( len( oShapes ) ):
        #
        o = oShapes[i]
        #
        sResult = point_in_poly__out_is_out( x, y, o.points, o.parts, o.bbox )
        #
        if sResult != 'OUT':
            lShapesOnPoint.append( ( i, sResult ) )
        #
        if sResult == 'IN': break
        #
    #
    return lShapesOnPoint



def getShapeOnPointWantOne( x, y, oShapeFile ):
    #
    lShapesOnPoint = getShapesOnPoint( x, y, oShapeFile )
    #
    # print lShapesOnPoint
    if len( lShapesOnPoint ) == 1:
        #
        result = lShapesOnPoint[0][0]
        #
    elif lShapesOnPoint: # multiple
        #
        lShapesCompletelyOnPoint = [ t for t in lShapesOnPoint if t[1] != 'IN' ]
        #
        if len( lShapesCompletelyOnPoint ) == 1:
            #
            result = lShapesCompletelyOnPoint[0][0]
            #
        else:
            #
            result = tuple( lShapesOnPoint )
            #
    else: # none
        #
        result = None
        #
    #
    return result


def getShapeObjectFromTuples( tBBox, tPoints, tBBoxes, tParts ):
    #
    from Iter.AllVers import iRange
    #
    class ShapeFile( list ): pass
    class Shape(   object ): pass
    #
    oShapeFile = ShapeFile()
    #
    oShapeFile.bbox = tBBox
    oShapeFile.numRecords = len( tPoints )
    #
    for i in iRange( oShapeFile.numRecords  ):
        #
        oShape = Shape()
        oShape.bbox   = tBBoxes[ i ]
        oShape.parts  = tParts[  i ]
        oShape.points = tPoints[ i ]
        #
        oShapeFile.append( oShape )
        #
    #
    def _shapes():
        return [ oShape for oShape in oShapeFile ]
    #
    oShapeFile.shapes = _shapes
    #
    return oShapeFile



def getExampleShapeObject():
    #
    lBBox = [ 3, 0, 13, 12 ]
    #
    lBBoxes = [
        [ 3, 0, 13, 12 ],
        [ 5, 2, 11, 10 ],
        [ 3, 0, 11, 8 ] ]
    #
    lPoints = [
        [ [3,6], [9,12], [12,9], [11,8], [9,10], [5,6], [9,2], [12,5], [13,4], [9,0], [3,6] ],
        [ [5,6], [9,10], [11,8], [10,7], [9,8], [7,6], [9,4], [10,5], [11,4], [9,2], [5,6] ],
        [ [7,6], [9,8], [11,6], [9,4], [7,6], [3,2], [5,4], [7,2], [5,0], [3,2] ] ]
    #
    lParts = [
        [0],
        [0],
        [0,5] ]
    #
    #
    #          /\
    #         /  \
    #        /    \
    #       /      \
    #      /   /\   \
    #     /   /  \   \
    #    /   /    \  /
    #   /   /   /\ \/
    #  /   /   /  \/
    # / 0 / 1 / 2  \
    # \   \   \ A  /
    #  \   \   \  /\/\
    #   \   \   \/ /  \
    #   /\   \    /   /
    #  /  \   \  /   /
    # / 2  \   \/   /
    # \ B  /\      /
    #  \  /  \    /
    #   \/    \  /
    #          \/ 
    #
    return getShapeObjectFromTuples( lBBox, lPoints, lBBoxes, lParts )




if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    # Test a vertex for inclusion
    poligono = (
        (-33.416032,-70.593016),
        (-33.415370,-70.589604),
        (-33.417340,-70.589046),
        (-33.417949,-70.592351),
        (-33.416032,-70.593016) )
    #
    x = -33.412
    y = -70.593016
    #
    if point_in_poly_verbose( x, y, poligono) != 'OUT_OF_BOUNDS':
        #
        lProblems.append( 'point_in_poly_verbose() OUT_OF_BOUNDS above' )
        #
    #
    x = -33.416032
    y = -70.4
    #
    if point_in_poly_verbose( x, y, poligono) != 'OUT_OF_BOUNDS':
        #
        lProblems.append( 'point_in_poly_verbose() OUT_OF_BOUNDS right' )
        #
    #
    x = -33.416032
    y = -70.593016
    #
    if point_in_poly_verbose( x, y, poligono) != 'ON_VERTEX':
        #
        lProblems.append( 'point_in_poly_verbose() ON_VERTEX' )
        #
    #
    if point_in_poly__edges_are_in( x, y, poligono) != 'IN':
        #
        lProblems.append( 'point_in_poly__edges_are_in() IN ON_VERTEX' )
        #
    #
    # test a point on horizontal boundary for inclusion
    poly2 = ( (1,1), (5,1), (5,5), (1,5), (1,1) )
    #
    x = 3
    y = 1
    #
    if point_in_poly_verbose( x, y, poly2 ) != "ON_BOUNDARY":
        #
        lProblems.append( 'point_in_poly_verbose() ON_BOUNDARY horizontal' )
        #
    #
    if point_in_poly__edges_are_in( x, y, poly2 ) != "IN":
        #
        lProblems.append(
            'point_in_poly__edges_are_in() IN ON_BOUNDARY horizontal' )
        #
    #
    if point_in_poly__edges_are_out( x, y, poly2 ) != "OUT":
        #
        lProblems.append(
            'point_in_poly__edges_are_out() IN ON_BOUNDARY horizontal' )
        #
    #
    # test a point on vertical boundary for inclusion
    x = 1
    y = 3
    #
    if point_in_poly_verbose( x, y, poly2 ) != "ON_BOUNDARY":
        #
        lProblems.append( 'point_in_poly_verbose() ON_BOUNDARY vertical' )
        #
    #
    if point_in_poly__edges_are_in( x, y, poly2 ) != "IN":
        #
        lProblems.append(
            'point_in_poly__edges_are_in() IN ON_BOUNDARY vertical' )
        #
    #
    if point_in_poly__edges_are_out( x, y, poly2 ) != "OUT":
        #
        lProblems.append(
            'point_in_poly__edges_are_out() IN ON_BOUNDARY vertical' )
        #
    #
    # test a point inside for inclusion
    x = 3
    y = 3
    #
    if point_in_poly_verbose( x, y, poly2 ) != 'IN':
        #
        lProblems.append( 'point_in_poly_verbose() IN' )
        #
    #
    poly3 = ( (3,8), (7,12), (12,7), (8,3), (3,8) )
    #
    x =  6
    y = 11
    #
    if point_in_poly_verbose( x, y, poly3 ) != "ON_BOUNDARY":
        #
        lProblems.append( 'point_in_poly_verbose() ON_BOUNDARY diagonal' )
        #
    #
    if point_in_poly__edges_are_in( x, y, poly3 ) != "IN":
        #
        lProblems.append(
            'point_in_poly__edges_are_in() IN ON_BOUNDARY diagonal' )
        #
    #
    if point_in_poly__edges_are_out( x, y, poly3 ) != "OUT":
        #
        lProblems.append(
            'point_in_poly__edges_are_out() IN ON_BOUNDARY diagonal' )
        #
    #
    # test a point inside for inclusion
    #
    x =  6.0
    y = 10.9
    #
    if point_in_poly_verbose( x, y, poly3 ) != "IN":
        #
        lProblems.append( 'point_in_poly_verbose() IN barely' )
        #
    #
    # test a point ouside for exclusion
    #
    x =  6.0
    y = 11.1
    #
    if point_in_poly_verbose( x, y, poly3 ) != "OUT":
        #
        lProblems.append( 'point_in_poly_verbose() OUT barely' )
        #
    #
    poly1 = ( (2,4), (3,8), (9,11), (12,8), (11,7),
              (9,9), (8,8), (12,2), (11,1), (2,4) )
    #
    # test a point inside for inclusion
    #
    x = 11.5
    y =  8.0
    #
    if point_in_poly_verbose(x, y, poly1) != "IN":
        #
        lProblems.append( 'point_in_poly_verbose() IN tip of appendage' )
        #
    #
    # test a point ouside for exclusion
    #
    x = 9
    y = 8
    #
    if point_in_poly_verbose(x, y, poly1) != "OUT":
        #
        lProblems.append( 'point_in_poly_verbose() OUT under armpit' )
        #
    #
    oShapeFile = getExampleShapeObject()
    #
    shapes = oShapeFile.shapes()
    #
    if list( getBoundingBox( shapes[0].points ) ) != oShapeFile.bbox:
        #
        lProblems.append( 'getBoundingBox() inconsistent w oShapeFile.bbox' )
        #
    #
    # test a point on ouside diagonal
    x = 5
    y = 8
    #
    if getShapeOnPointWantOne( x, y, oShapeFile ) != 0:
        #
        lProblems.append( 'getShapeOnPointWantOne() point on outer shape' )
        #
    #
    # test a point on inside shared diagonal
    x = 6
    y = 7
    #
    if getShapeOnPointWantOne(
            x, y, oShapeFile ) != ( (0, 'ON_BOUNDARY'), (1, 'ON_BOUNDARY'), ):
        #
        lProblems.append(
            'getShapeOnPointWantOne() point on inside shared diagonal' )
        #
    #
    # test a point ouside bounding box
    x = 2
    y = 6
    #
    if getShapeOnPointWantOne( x, y, oShapeFile ) is not None:
        #
        lProblems.append(
            'getShapeOnPointWantOne() point ouside bounding box' )
        #
    #
    # test a point on ouside vertex
    x = 11
    y = 6
    #
    if getShapeOnPointWantOne( x, y, oShapeFile ) != 2:
        #
        lProblems.append( 'getShapeOnPointWantOne() point on ouside vertex' )
        #
    #
    # test a point on inside vertex
    x = 7
    y = 6
    #
    # print point_in_poly_verbose( x, y, oShapeFile[1].points )
    if getShapeOnPointWantOne(
            x, y, oShapeFile ) != ( (1, 'ON_VERTEX'), (2, 'ON_VERTEX'), ):
        #
        #print getShapeOnPointWantOne( x, y, oShapeFile )
        lProblems.append( 'getShapeOnPointWantOne() point on inside vertex' )
        #
    #
    # test a point inside bounding box but not in any shape
    x = 11
    y = 7
    #
    if getShapeOnPointWantOne( x, y, oShapeFile ) is not None:
        #
        lProblems.append(
            'getShapeOnPointWantOne() '
            'inside bounding box but not in any shape' )
        #
    #
    # test a point inside first part of 2-part shape
    x = 10
    y = 6
    #
    if getShapeOnPointWantOne( x, y, oShapeFile ) != 2:
        #
        lProblems.append(
            'getShapeOnPointWantOne() inside first part of 2-part shape' )
        #
    #
    # test a point inside 2nd part of 2-part shape
    x = 6
    y = 2
    #
    if getShapeOnPointWantOne( x, y, oShapeFile ) != 2:
        #
        lProblems.append(
            'getShapeOnPointWantOne() inside first part of 2-part shape' )
        #
    #
    # test a point on ouside diagonal of 2-part shape
    x = 4
    y = 3
    #
    if getShapeOnPointWantOne( x, y, oShapeFile ) != 2:
        #
        lProblems.append(
            'getShapeOnPointWantOne() on ouside diagonal of 2-part shape' )
        #
    #
    sayTestResult( lProblems ) 