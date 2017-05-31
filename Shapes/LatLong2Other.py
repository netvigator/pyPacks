#!/usr/bin/pythonTest
#
# Shape projections / point transformations
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
# Copyright 2012-2016 Rick Graves
#
# depends on python-pyproj

'''
convert lat/long coordinates to other coordinate systems
see self test code for examples from various USA States
'''


from pyproj import Proj

'''

i = 2
points = oShapes[i].points
bbox = oShapes[i].bbox
lPoints = [[]] * 4
for t in points:
    if t[0] == bbox[0]: lPoints[0].append( t )
    if t[0] == bbox[2]: lPoints[2].append( t )
    if t[1] == bbox[1]: lPoints[1].append( t )
    if t[1] == bbox[3]: lPoints[3].append( t )

'''

def getDecimalDegreesOffDegMinSec( nD, nM, nS ):
    #
    return nD + ( nM / 60.0 ) + ( nS / 3600.0 )

def _meters_2_US_feet(   nMeters ): return nMeters / 0.3048006096012192

def _meters_2_Intl_feet( nMeters ): return nMeters / 0.3048

def _US_feet_2_meters(   nFeet ):   return nFeet   * 0.3048006096012192

def _Intl_feet_2_meters( nFeet ):   return nFeet   * 0.3048



proj_IN = Proj( proj="utm", zone=16, datum='NAD83' )

def _Meta_IN():
    #
    # sIndiana
    #
    sMeta = '''
    PROJCS["NAD_1983_UTM_Zone_16N",
    GEOGCS["GCS_North_American_1983",
    DATUM["D_North_American_1983",
    SPHEROID["GRS_1980",6378137.0,298.257222101]],
    PRIMEM["Greenwich",0.0],
    UNIT["Degree",0.0174532925199433]],
    PROJECTION["Transverse_Mercator"],
    PARAMETER["False_Easting",500000.0],
    PARAMETER["False_Northing",0.0],
    PARAMETER["Central_Meridian",-87.0],
    PARAMETER["Scale_Factor",0.9996],
    PARAMETER["Latitude_Of_Origin",0.0],
    UNIT["Meter",1.0]]
    '''
    #
    pass

proj_KY = Proj( "+proj=lcc "
                "+lat_1=38.66666666666666 "
                "+lat_2=37.08333333333334 "
                "+lat_0=36.33333333333334 "
                "+lon_0=-85.75 "
                "+x_0=1500000.22 "
                "+y_0=1000000" )

def _Meta_KY():
    #
    # Kentucky has two shapefiles
    # one Kentucky_Statewide, one Lat/Long
    #
    # http://www.remotesensing.org/geotiff/proj_list/lambert_conic_conformal_2sp.html
    #
    sMeta = '''
    PROJCS["NAD_1983_StatePlane_Kentucky_Statewide_(2001)_FIPS_1600",
    GEOGCS["GCS_GRS_1980",
    DATUM["D_GRS_1980",
    SPHEROID["GRS_1980",6378137,298.2572221]],
    PRIMEM["Greenwich",0],
    UNIT["Degree",0.0174532925199433]],
    PROJECTION["Lambert_Conformal_Conic"],
    PARAMETER["False_Easting",1500000],
    PARAMETER["False_Northing",1000000],
    PARAMETER["Central_Meridian",-85.75],
    PARAMETER["Standard_Parallel_1",38.66666666666666],
    PARAMETER["Standard_Parallel_2",37.08333333333334],
    PARAMETER["Latitude_Of_Origin",36.33333333333334],
    UNIT["Meter",1]]
    '''
    #
    pass


proj_ME = Proj(proj="utm",zone=19,datum='NAD83')

def _Meta_ME():
    #
    # Maine have points from state, could use better ones
    #
    sMeta = '''
    PROJCS["NAD_1983_UTM_Zone_19N",
    GEOGCS["GCS_North_American_1983",
    DATUM["D_North_American_1983",
    SPHEROID["GRS_1980",6378137.0,298.257222101]],
    PRIMEM["Greenwich",0.0],
    UNIT["Degree",0.0174532925199433]],
    PROJECTION["Transverse_Mercator"],
    PARAMETER["False_Easting",500000.0],
    PARAMETER["False_Northing",0.0],
    PARAMETER["Central_Meridian",-69.0],
    PARAMETER["Scale_Factor",0.9996],
    PARAMETER["Latitude_Of_Origin",0.0],
    UNIT["Meter",1.0]]
    '''
    #
    pass

proj_MI = Proj( "+proj=omerc "
                "+lat_0=45.30916666666666 "
                "+lonc=-86 "
                "+alpha=337d15m20s "
                "+k_0=0.9996 "
                "+x_0=2546731.496 "
                "+y_0=-4354009.816 "
                "+no_uoff" )

def _Meta_MI():
    #
    # Michigan
    # state sent CORCON.EXE which can convert to/from Lat/Long
    # several points in state converted
    #
    # http://www.remotesensing.org/geotiff/proj_list/hotine_oblique_mercator.html
    #
    sMeta = '''
    PROJCS["NAD83 / Michigan Oblique Mercator",
    GEOGCS["NAD83",
        DATUM["North_American_Datum_1983",
            SPHEROID["GRS 1980",6378137,298.257222101,
                AUTHORITY["EPSG","7019"]],
            AUTHORITY["EPSG","6269"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.01745329251994328,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4269"]],
    UNIT["metre",1,
        AUTHORITY["EPSG","9001"]],
    PROJECTION["Hotine_Oblique_Mercator"],
    PARAMETER["latitude_of_center",45.30916666666666],
    PARAMETER["longitude_of_center",-86],
    PARAMETER["azimuth",337.25556],
    PARAMETER["rectified_grid_angle",337.25556],
    PARAMETER["scale_factor",0.9996],
    PARAMETER["false_easting",2546731.496],
    PARAMETER["false_northing",-4354009.816],
    AUTHORITY["EPSG","3078"],
    AXIS["X",EAST],
    AXIS["Y",NORTH]]
    '''
    #
    pass

proj_MN = Proj(proj="utm",zone=15,datum='NAD83')

def _Meta_MN():
    #
    # Minnesota
    #
    sMeta = '''
    PROJCS["NAD_1983_UTM_Zone_15N",
    GEOGCS["GCS_North_American_1983",
    DATUM["D_North_American_1983",
    SPHEROID["GRS_1980",6378137.0,298.257222101]],
    PRIMEM["Greenwich",0.0],
    UNIT["Degree",0.0174532925199433]],
    PROJECTION["Transverse_Mercator"],
    PARAMETER["False_Easting",500000.0],
    PARAMETER["False_Northing",0.0],
    PARAMETER["Central_Meridian",-93.0],
    PARAMETER["Scale_Factor",0.9996],
    PARAMETER["Latitude_Of_Origin",0.0],
    UNIT["Meter",1.0]]
    '''
    #
    pass

proj_NC = Proj( "+proj=lcc "
                "+lat_1=34.33333333333334 "
                "+lat_2=36.16666666666666 "
                "+lat_0=33.75 "
                "+lon_0=-79.0 "
                "+x_0=609601.22 "
                "+y_0=0" )

def _Meta_NC():
    #
    # North Carolina North_Carolina
    #
    # http://www.remotesensing.org/geotiff/proj_list/lambert_conic_conformal_2sp.html
    #
    sMeta = '''
    PROJCS["NAD_1983_StatePlane_North_Carolina_FIPS_3200",
    GEOGCS["GCS_North_American_1983",
    DATUM["D_North_American_1983",
    SPHEROID["GRS_1980",6378137.0,298.257222101]],
    PRIMEM["Greenwich",0.0],
    UNIT["Degree",0.0174532925199433]],
    PROJECTION["Lambert_Conformal_Conic"],
    PARAMETER["False_Easting",609601.22],
    PARAMETER["False_Northing",0.0],
    PARAMETER["Central_Meridian",-79.0],
    PARAMETER["Standard_Parallel_1",34.33333333333334],
    PARAMETER["Standard_Parallel_2",36.16666666666666],
    PARAMETER["Latitude_Of_Origin",33.75],
    UNIT["Meter",1.0]]
    '''
    #
    pass

_proj_NH_meters = Proj( "+proj=tmerc "
                        "+lat_0=42.5 "
                        "+lon_0=-71.66666666666667 "
                        "+k_0=0.9999666666666667 "
                        "+x_0=300000.0 "
                        "+y_0=0 "
                        "+units=us-ft" )

def proj_NH( nLong, nLat ):
    #
    from Iter.AllVers import tMap
    #
    return tMap( _meters_2_US_feet, _proj_NH_meters( nLong, nLat ) )


def _Meta_NH():
    #
    # New Hampshire New_Hampshire
    # State Plane Coordinate System 1983
    # http://www.remotesensing.org/geotiff/proj_list/transverse_mercator.html
    #
    sMeta = '''
    PROJCS["NAD_1983_StatePlane_New_Hampshire_FIPS_2800_Feet",
    GEOGCS["GCS_North_American_1983",
    DATUM["D_North_American_1983",
    SPHEROID["GRS_1980", 6378137.0, 298.257222101]],
    PRIMEM["Greenwich",0.0],
    UNIT["Degree",0.0174532925199433]],
    PROJECTION["Transverse_Mercator"],
    PARAMETER["False_Easting",984250.0],
    PARAMETER["False_Northing",0.0],
    PARAMETER["Central_Meridian",-71.66666666666667],
    PARAMETER["Scale_Factor",0.9999666666666667],
    PARAMETER["Latitude_Of_Origin",42.5],
    UNIT["Foot_US",0.3048006096012192]]
    '''
    #
    pass

def _Meta_OR(): # Oregon
    #
    sMeta = '''
    http://www.remotesensing.org/geotiff/proj_list/lambert_conic_conformal_2sp.html
    
    PROJCS["NAD_1983_Oregon_Statewide_Lambert_Feet_Intl",
    GEOGCS["GCS_North_American_1983",
    DATUM["D_North_American_1983",
    SPHEROID["GRS_1980",6378137.0,298.257222101]],
    PRIMEM["Greenwich",0.0],
    UNIT["Degree",0.0174532925199433]],
    PROJECTION["Lambert_Conformal_Conic"],
    PARAMETER["False_Easting",1312335.958005249],
    PARAMETER["False_Northing",0.0],
    PARAMETER["Central_Meridian",-120.5],
    PARAMETER["Standard_Parallel_1",43.0],
    PARAMETER["Standard_Parallel_2",45.5],
    PARAMETER["Latitude_Of_Origin",41.75],
    UNIT["Foot",0.3048]],
    VERTCS["NAD_1983",
    DATUM["D_North_American_1983",
    SPHEROID["GRS_1980",6378137.0,298.257222101]],
    PARAMETER["Vertical_Shift",0.0],
    PARAMETER["Direction",1.0],
    UNIT["Meter",1.0]]
    '''
    #
    pass

#_proj_OR_meters = Proj( "+proj=lcc "
                        #"+lat_0=41.75 "
                        #"+lat_1=43.0 "
                        #"+lat_2=45.5 "
                        #"+lon_0=-120.5 "
                        #"+x_0=400000 "
                        #"+y_0=0.0 "
                        #"+units=ft " )

_proj_OR_meters = Proj( "+init=epsg:2992" )

def proj_OR( nLong, nLat ):
    #
    from Iter.AllVers import tMap
    #
    return tMap( _meters_2_Intl_feet, _proj_OR_meters( nLong, nLat ) )



proj_TX = Proj( "+proj=lcc "
                "+lat_1=34.91666666666666 "
                "+lat_2=27.41666666666667 "
                "+lat_0=31.16666666666667 "
                "+lon_0=-100.0 "
                "+x_0=1000000.0 "
                "+y_0=1000000.0" )

def _Meta_TX():
    #
    # Texas
    # have a point from state, maybe better to get better ones
    #
    # http://www.remotesensing.org/geotiff/proj_list/lambert_conic_conformal_2sp.html
    #
    sMeta = '''
    PROJCS["NAD_1983_Lambert_Conformal_Conic",
    GEOGCS["GCS_North_American_1983",
    DATUM["D_North_American_1983",
    SPHEROID["GRS_1980",6378137.0,298.257222101]],
    PRIMEM["Greenwich",0.0],
    UNIT["Degree",0.0174532925199433]],
    PROJECTION["Lambert_Conformal_Conic"],
    PARAMETER["False_Easting",1000000.0],
    PARAMETER["False_Northing",1000000.0],
    PARAMETER["Central_Meridian",-100.0],
    PARAMETER["Standard_Parallel_1",34.91666666666666],
    PARAMETER["Standard_Parallel_2",27.41666666666667],
    PARAMETER["Latitude_Of_Origin",31.16666666666667],
    UNIT["Meter",1.0]]
    '''
    #
    pass


proj_UT = Proj( proj="utm", zone=12, datum='NAD83' )

def _Meta_UT():
    #
    sMeta = '''
    PROJCS["NAD_1983_UTM_Zone_12N",
    GEOGCS["GCS_North_American_1983",
    DATUM["D_North_American_1983",
    SPHEROID["GRS_1980",6378137.0,298.257222101]],
    PRIMEM["Greenwich",0.0],
    UNIT["Degree",0.0174532925199433]],
    PROJECTION["Transverse_Mercator"],
    PARAMETER["False_Easting",500000.0],
    PARAMETER["False_Northing",0.0],
    PARAMETER["Central_Meridian",-111.0],
    PARAMETER["Scale_Factor",0.9996],
    PARAMETER["Latitude_Of_Origin",0.0],
    UNIT["Meter",1.0]]
    '''
    #
    pass


proj_WI = Proj( "+proj=tmerc "
                "+lat_0=0.0 "
                "+lon_0=-90.0 "
                "+k_0=0.9996 "
                "+x_0=520000.0 "
                "+y_0=-4480000.0" )

def _Meta_WI():
    #
    # Wisconsin
    # +proj=tmerc +lat_0=0.0 +lon_0=-90.0 +k_0=0.9996 +x_0=520000.0 +y_0=-4480000.0
    #
    sMeta = '''
    PROJCS["NAD_1983_HARN_Wisconsin_TM",
    GEOGCS["GCS_North_American_1983_HARN",
    DATUM["D_North_American_1983_HARN",
    SPHEROID["GRS_1980",6378137.0,298.257222101]],
    PRIMEM["Greenwich",0.0],
    UNIT["Degree",0.0174532925199433]],
    PROJECTION["Transverse_Mercator"],
    PARAMETER["False_Easting",520000.0],
    PARAMETER["False_Northing",-4480000.0],
    PARAMETER["Central_Meridian",-90.0],
    PARAMETER["Scale_Factor",0.9996],
    PARAMETER["Latitude_Of_Origin",0.0],
    UNIT["Meter",1.0]]
    '''
    #
    pass


def getLatLongReversed( nLat, nLong ):
    #
    '''
    simple function for lat/long shape files
    shape files points are x, y order
    lat/long is y, x order
    plug compatible with coordinate system converters
    '''
    #
    #
    return float( nLong ), float( nLat )


_dStateConverters = dict(
        IN = proj_IN,
        KY = proj_KY,
        ME = proj_ME,
        MI = proj_MI,
        MN = proj_MN,
        NC = proj_NC,
        TX = proj_TX,
        UT = proj_UT,
        WI = proj_WI )


def getStateConverter( sState ):
    #
    '''
    factory for converting coordinates
    '''
    if sState in _dStateConverters:
        #
        oProj = _dStateConverters[ sState ]
        #
        def getConverted( nLat, nLong ):
            #
            return oProj( nLong, nLat )
        #
    else:
        #
        getConverted = getLatLongReversed
        #
    #
    return getConverted


if __name__ == "__main__":
    #
    from six            import print_ as print3
    #
    from Iter.AllVers   import tMap, tZip
    from Numb.Test      import areClose, getHowClose, getCloseEnoughTester
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if getDecimalDegreesOffDegMinSec( 40, 30, 0 ) != 40.5:
        #
        lProblems.append( 'getDecimalDegreesOffDegMinSec() 40 30 0' )
        #
    #
    closeEnoughDot0 = getCloseEnoughTester( 0 )
    closeEnoughDot1 = getCloseEnoughTester( 1 )
    closeEnoughDot2 = getCloseEnoughTester( 2 )
    closeEnoughDot3 = getCloseEnoughTester( 3 )
    closeEnoughDot4 = getCloseEnoughTester( 4 )
    closeEnoughDot5 = getCloseEnoughTester( 5 )
    closeEnoughDot6 = getCloseEnoughTester( 6 )
    #
    # Indiana
    #
    sIndiana = '''
    http://www.findlatitudeandlongitude.com/
    NE corner (3rd Dist)
    Address: 10001-11999 Mellon Rd, Camden, IN 49232, USA
    Latitude:41.7591643
    Longitude:-84.8099366
    #
    S point (8th Dist)
    Address:Old Dam 49 Rd, Mt Vernon, IN 47620, USA
    Latitude:37.7769722
    Longitude:-87.9538001
    '''
    #
    easting, northing = proj_IN( -84.8099366, 41.7591643 ) # Indiana
    # NE corner (3rd Dist)
    #
    want_X, want_Y = 682397.2131537399, 4625475.441409135
    #
    sGotThisAsFollows = ''''
    from doShapeFileLookUps import getStateShapeFile
    sState = 'IN'
    tBBox, tPoints, tShapeBBoxes = getStateShapeFile( sState )
    tBBox
    [403477.7882552211, 4180915.2359783, 692181.814949563, 4625475.441409135]
    l3rdN = [ t for t in tPoints[2] if t[1] == tBBox[3] ]
    len(l3rdN)
    2
    l3rdN
    [[682397.2131537399, 4625475.441409135], [682397.2131537399, 4625475.441409135]]
    l3rdN[0] == l3rdN[1]
    True
    '''
    #
    if not closeEnoughDot1( easting, want_X ):
        #
        print3( 'easting, want_X:', easting, want_X )
        print3( 'easting:', getHowClose( easting, want_X ) )
        lProblems.append( 'proj_MI() Indiana NE corner (3rd Dist) easting' )
        #
    if not closeEnoughDot2( northing, want_Y ):
        #
        print3( 'northing, want_Y:', northing, want_Y )
        print3( 'northing:', getHowClose( northing, want_Y ) )
        lProblems.append( 'proj_MI() Indiana NE corner (3rd Dist) northing' )
        #
    #
    easting, northing = proj_IN( -87.9538001, 37.7769722 ) # Indiana
    # S point (8th Dist)
    #
    want_X, want_Y = 416127.16583947977, 4180915.2359783
    #
    sGotThisAsFollows = '''
    from doShapeFileLookUps import getStateShapeFile
    sState = 'IN'
    tBBox, tPoints, tShapeBBoxes = getStateShapeFile( sState )
    tBBox
    [403477.7882552211, 4180915.2359783, 692181.814949563, 4625475.441409135]
    oShapes[7].bbox
    [403477.7882552211, 4180915.2359783, 559478.7838101505, 4444346.983670331]
    lBottom = [ t for t in tPoints[7] if t[1] == oShapes[7].bbox[1] ]
    lBottom
    [[416127.16583947977, 4180915.2359783]]
    '''
    #
    if not closeEnoughDot1( easting, want_X ):
        #
        print3( 'easting, want_X:', easting, want_X )
        print3( 'easting:', getHowClose( easting, want_X ) )
        lProblems.append( 'proj_IN() Indiana S point (8th Dist) easting' )
        #
    if not closeEnoughDot1( northing, want_Y ):
        #
        print3( 'northing, want_Y:', northing, want_Y )
        print3( 'northing:', getHowClose( northing, want_Y ) )
        lProblems.append( 'proj_IN() Indiana S point (8th Dist) northing' )
        #
    #
    # Kentucky
    #
    easting, northing = proj_KY( -89.571201, 36.551429 ) # Kentucky
    # westernmost point of state (5th Dist)
    #
    want_X, want_Y = 1157918.4989276303, 1031211.2006528883
    #
    sGotThisAsFollows = '''
    from doShapeFileLookUps import getStateShapeFile
    sState = 'KY'
    tBBox, tPoints, tShapeBBoxes = getStateShapeFile( sState )
    tBBox
    [1157918.4989276303, 1020719.1128834931, 1834402.5530060388, 1312845.552078662]
    lWest = [ lP for lP in oShapes[4].points if lP[0] == tBBox[0] ]
    lWest
    [[1157918.4989276303, 1031211.2006528883]]
    oShapes[4].points.index( lWest[0] )
    51

    oLLShapeFile, oLLShapes = getStateShapeFile( 'KY/Shapes_Lat_n_Long' )
    oLLShapes[4].points[51]
    [-89.571201, 36.551429]
    '''
    #
    if not closeEnoughDot4( easting, want_X ):
        #
        print3( 'easting, want_X:', easting, want_X )
        print3( 'easting:', getHowClose( easting, want_X ) )
        lProblems.append( 'proj_KY() W point of Kentucky (5th dist) easting' )
        #
    if not closeEnoughDot6( northing, want_Y ):
        #
        print3( 'northing, want_Y:', northing, want_Y )
        print3( 'northing:', getHowClose( northing, want_Y ) )
        lProblems.append( 'proj_KY() W point of Kentucky (5th dist) northing' )
        #
    #
    easting, northing = proj_KY( -81.964788, 37.542243 ) # Kentucky
    # easternmost point of state (2nd Dist)
    #
    want_X, want_Y = 1834402.5530060388, 1140950.869067373
    #
    sGotThisAsFollows = '''
    lEast = [ lP for lP in oShapes[1].points if lP[0] == tBBox[2] ]
    lEast
    [[1834402.5530060388, 1140950.869067373]]
    oShapes[1].points.index( lEast[0] )
    12075

    lLLEast = [ lP for lP in oLLShapes[1].points if lP[0] == oLLShapeFile.bbox[2] ]
    lLLEast
    [[-81.964788, 37.542243]]
    oLLShapes[1].points.index( lLLEast[0] )
    12075
    '''
    #
    if not closeEnoughDot4( easting, want_X ):
        #
        print3( 'easting, want_X:', easting, want_X )
        print3( 'easting:', getHowClose( easting, want_X ) )
        lProblems.append( 'proj_KY() E point of Kentucky (2nd dist) easting' )
        #
    if not closeEnoughDot6( northing, want_Y ):
        #
        print3( 'northing, want_Y:', northing, want_Y )
        print3( 'northing:', getHowClose( northing, want_Y ) )
        lProblems.append( 'proj_KY() E point of Kentucky (2nd dist) northing' )
        #
    #
    easting, northing = proj_KY( -84.744371, 39.147732 ) # Kentucky
    # northernmost point of state (1st Dist)
    #
    want_X, want_Y = 1586944.072629744, 1312845.552078662
    #
    sGotThisAsFollows = '''
    lNorth = [ lP for lP in oShapes[0].points if lP[1] == tBBox[3] ]
    lNorth
    [[1586944.072629744, 1312845.552078662]]
    lLLNorth = [ lP for lP in oLLShapes[0].points if lP[1] == oLLShapeFile.bbox[3] ]
    lLLNorth
    [[-84.744371, 39.147732]]
    oShapes[0].points.index( lNorth[0] )
    1301
    oLLShapes[0].points.index( lLLNorth[0] )
    1301
    '''
    #
    if not closeEnoughDot4( easting, want_X ):
        #
        print3( 'easting, want_X:', easting, want_X )
        print3( 'easting:', getHowClose( easting, want_X ) )
        lProblems.append( 'proj_KY() N point of Kentucky (1st dist) easting' )
        #
    if not closeEnoughDot6( northing, want_Y ):
        #
        print3( 'northing, want_Y:', northing, want_Y )
        print3( 'northing:', getHowClose( northing, want_Y ) )
        lProblems.append( 'proj_KY() N point of Kentucky (1st dist) northing' )
        #
    #
    # Maine
    #
    sMaine = '''
    http://www.findlatitudeandlongitude.com/
    Northern point (Aroostook Co, 2nd Dist)
    Estcourt Rd, ESTCOURT STATION, ME 04741, USA
    Latitude:47.451502
    Longitude:-69.1979361
    #
    Western edge, North End (Oxford Co, 1st Dist)
    Magalloway Rd, ERROL, ME 03579, USA
    Latitude:45.2999144
    Longitude:-71.0421582
    '''
    #
    easting, northing = proj_ME( -68.204, 44.392 ) # Maine
    #
    if False in tMap( closeEnoughDot3,
                    tZip( ( easting, northing ),
                          ( 563394, 4915741 ) ) ):
        #
        print3( easting, 563394 )
        print3( 'easting:', getHowClose( easting, 563394 ) )
        print3( northing, 4915741 )
        print3( 'northing:', getHowClose( northing, 4915741 ) )
        lProblems.append( 'proj_ME() Proj wharf in Bar Harbor' )
        #
    #
    easting, northing = proj_ME( -70.208, 43.623 )
    #
    if False in tMap( closeEnoughDot2,
                    tZip( ( easting, northing ),
                          ( 402548, 4830727 ) ) ):
        #
        print3( easting, 402548 )
        print3( 'easting:', getHowClose( easting, 402548 ) )
        print3( northing, 4830727 )
        print3( 'northing:', getHowClose( northing, 4830727 ) )
        lProblems.append( 'proj_ME() Proj Portland Head Lighthouse' )
        #
    #
    #
    sMichigan = '''
    http://www.findlatitudeandlongitude.com/
    Western most point (1st)
    Address:600-618 E Tamarack St, Ironwood, MI 49938, USA
    Latitude:46.4470696
    Longitude:-90.1510458
    46 26 49.45 90 9 3.76
    181092.963 663401.694
    #
    http://www.findlatitudeandlongitude.com/?loc=1425+Riverside+Drive+Sault+Ste+Marie%2C+MI+49783&id=1259343
    1409-1445 Riverside Dr, Sault Ste. Marie, MI 49783, USA
    Latitude:46.4854251
    Longitude:-84.3032953
    46 29 7.53 84 18 11.86
    630074.358 660690.799
    #
    ### should be most "easterly" point of MI in Mich GeoRef ###
    http://www.lat-long.com/Latitude-Longitude-1623175-Michigan-Drummond_Island.html
    Drummond Island, MI (eastern end of upper MI) (1st)
    Latitude: 46.0000214
    Longitude: -83.6666664
    46 0 0.07 83 39 59.99
    680522.825 607993.090
    #
    #
    http://www.amtrak.com/servlet/ContentServer?pagename=am/am2Station/StationInfoPopup&code=PTH
    Port Huron, MI (PTH) (Eastern most point of MI)
    Station Building (with waiting room)
    2223 16th Street
    Port Huron, MI 48060
    Latitude, Longitude: 42.960419, -82.443805
    42 57 37.5 82 26 37.69
    789848.943 273938.363
    #
    http://www.mapquest.com/?q=42.11187,-86.45134%28First+Congregational+Church%29&zoom=13&maptype=hybrid
    First Congregational Church
    Benton Harbor, MI 49022
    Latitude: 42.11187 Longitude: -86.45134
    42 6 42.73 86 27 4.82
    462581.148 173552.971
    #
    http://www.mapquest.com/?q=41.7713890076,-83.6466674805
    Latitude: 41.7713890076 Longitude: -83.6466674805
    Lambertville, MI 48144
    41 46 17 83 38 48
    695511.205 138486.174 
    #
    #
    SW corner of Lower MI (6th) 
    most "westerly" point of 6th
    3826 Ponchartrain Trail, New Buffalo, MI 49117, USA
    Latitude:41.761714
    Longitude:-86.818624
    #
    from doShapeFileLookUps import getStateShapeFile
    tBBox, tPoints, tShapeBBoxes = getStateShapeFile( 'MI' )
    i = 5
    lDist = oShapes[ i ].points
    MinX = 10**10
    for l in lDist:
      if l[0] < MinX:
         MinX = l[0]
         tWest = tuple( l )
     
    tWest
    (431325.47312499955, 134714.93637499958)
    oShapes[ i ].bbox
    [431325.47312499955, 134322.65300000086, 558782.7852500007, 246471.0857499987]
    '''
    #
    easting, northing = proj_MI( -84.3032953, 46.4854251 )
    #
    want_X, want_Y = 630074.358, 660690.799
    #
    if not closeEnoughDot1( easting, want_X ):
        #
        print3( 'easting, want_X:', easting, want_X )
        print3( 'easting:', getHowClose( easting, want_X ) )
        lProblems.append( 'proj_MI() Sault Ste. Marie easting' )
        #
    if not closeEnoughDot1( northing, want_Y ):
        #
        print3( 'northing, want_Y:', northing, want_Y )
        print3( 'northing:', getHowClose( northing, want_Y ) )
        lProblems.append( 'proj_MI() Sault Ste. Marie northing' )
        #
    #
    easting, northing = proj_MI( -86.818624, 41.761714 )
    #
    want_X, want_Y = (431325.47312499955, 134714.93637499958)
    #
    if not closeEnoughDot3( easting, want_X ):
        #
        print3( 'easting, want_X:', easting, want_X )
        print3( 'easting:', getHowClose( easting, want_X ) )
        lProblems.append( 'proj_MI() most "westerly" point of 6th easting' )
        #
    #
    if not closeEnoughDot1( northing, want_Y ):
        #
        print3( 'northing, want_Y:', northing, want_Y )
        print3( 'northing:', getHowClose( northing, want_Y ) )
        lProblems.append( 'proj_MI() most "westerly" point of 6th northing' )
        #
    #
    easting, northing = proj_MI( -83.6666664, 46.0000214 )
    #
    want_X, want_Y = (680522.825, 607993.090)
    #
    if not closeEnoughDot1( easting, want_X ):
        #
        print3( 'easting, want_X:', easting, want_X )
        print3( 'easting:', getHowClose( easting, want_X ) )
        lProblems.append( 'proj_MI() Drummond Island eastern end of upper MI easting' )
        #
    #
    if not closeEnoughDot1( northing, want_Y ):
        #
        print3( 'northing, want_Y:', northing, want_Y )
        print3( 'northing:', getHowClose( northing, want_Y ) )
        lProblems.append( 'proj_MI() Drummond Island eastern end of upper MI northing' )
        #
    #
    easting, northing = proj_MI( -82.443805, 42.960419 )
    #
    want_X, want_Y = (789848.943, 273938.363)
    #
    if not closeEnoughDot1( easting, want_X ):
        #
        print3( 'easting, want_X:', easting, want_X )
        print3( 'easting:', getHowClose( easting, want_X ) )
        lProblems.append( 'proj_MI() Port Huron Eastern most point of MI easting' )
        #
    #
    if not closeEnoughDot1( northing, want_Y ):
        #
        print3( 'northing, want_Y:', northing, want_Y )
        print3( 'northing:', getHowClose( northing, want_Y ) )
        lProblems.append( 'proj_MI() Port Huron Eastern most point of MI northing' )
        #
    #
    easting, northing = proj_MI( -86.45134, 42.11187 )
    #
    want_X, want_Y = (462581.148, 173552.971)
    #
    if not closeEnoughDot0( easting, want_X ):
        #
        print3( 'easting, want_X:', easting, want_X )
        print3( 'easting:', getHowClose( easting, want_X ) )
        lProblems.append( 'proj_MI() First Congregational Church Benton Harbor easting' )
        #
    #
    if not closeEnoughDot1( northing, want_Y ):
        #
        print3( 'northing, want_Y:', northing, want_Y )
        print3( 'northing:', getHowClose( northing, want_Y ) )
        lProblems.append( 'proj_MI() First Congregational Church Benton Harbor northing' )
        #
    #
    #
    # Minnesota
    #
    sMinnesota = '''
    http://www.findlatitudeandlongitude.com/
    Northern most point (7th Dist)
    Unnamed Rd, Angle Inlet, MN 56711, USA
    Latitude:49.3572263
    Longitude:-95.1405876
    #
    SE corner (1st Dist)
    21463 State Highway 26, Caledonia, MN 55921, USA
    Latitude:43.5067659
    Longitude:-91.2815108
    #
    SW corner (1st Dist)
    County Highway 17, Hills, MN 56138, USA
    Latitude:43.5232413
    Longitude:-96.4320013
    '''
    #
    easting, northing = proj_MN( -95.1405876, 49.3572263 ) # Minnesota
    # northernmost point of state (7th Dist)
    #
    want_X, want_Y = 343722.2230079655, 5472414.143679132
    #
    sGotThisAsFollows = '''
    from doShapeFileLookUps import getStateShapeFile
    sState = 'MN'
    tBBox, tPoints, tShapeBBoxes = getStateShapeFile( sState )
    tBBox
    [189777.1888735082, 4816289.640107582, 762236.9588447501, 5472414.143679132]
    lNorth = [ lP for lP in oShapes[6].points if lP[1] == tBBox[3] ]
    lNorth
    [[343722.2230079655, 5472414.143679132]]
    '''
    #
    if not closeEnoughDot0( easting, want_X ):
        #
        print3( 'easting, want_X:', easting, want_X )
        print3( 'easting:', getHowClose( easting, want_X ) )
        lProblems.append( 'proj_MN() N point of state (7th dist) easting' )
        #
    #
    if not closeEnoughDot1( northing, want_Y ):
        #
        print3( 'northing, want_Y:', northing, want_Y )
        print3( 'northing:', getHowClose( northing, want_Y ) )
        lProblems.append( 'proj_MI() N point of state (7th dist) northing' )
        #
    #
    easting, northing = proj_MN( -91.2815108, 43.5067659 ) # Minnesota
    # SE corner of state 1st Dist)
    # want max x min y
    #
    want_X, want_Y = 644088.3080590538, 4817945.38641254
    #
    sGotThisAsFollows = '''
    nDiff = oShapes[0].points[0][0] - oShapes[0].points[0][1]
    nDiff
    -4397012.928581983
    for t in oShapes[0].points:
       if t[0] - t[1] > nDiff:
         nDiff = t[0] - t[1]
         tSE = t
     
    nDiff
    -4173857.0783534865
    tSE
    [644088.3080590538, 4817945.38641254]
    '''
    #
    if not closeEnoughDot0( easting, want_X ):
        #
        print3( 'easting, want_X:', easting, want_X )
        print3( 'easting:', getHowClose( easting, want_X ) )
        lProblems.append( 'proj_MN() SE corner of state 1st Dist) easting' )
        #
    #
    if not closeEnoughDot1( northing, want_Y ):
        #
        print3( 'northing, want_Y:', northing, want_Y )
        print3( 'northing:', getHowClose( northing, want_Y ) )
        lProblems.append( 'proj_MI() SE corner of state 1st Dist) northing' )
        #
    #
    easting, northing = proj_MN( -96.4320013, 43.5232413 ) # Minnesota
    # SW corner of state (1st Dist)
    # want min x min y
    #
    want_X, want_Y = 220816.24458556, 4822179.697546681
    #
    sGotThisAsFollows = '''
    nSum = oShapes[0].points[0][0] + oShapes[0].points[0][1]
    nSum
    5390435.002100645
    for t in oShapes[0].points:
        if t[0] + t[1] < nSum:
        nSum = t[0] + t[1]
        tSW = t
    
    nSum
    5042995.942132241
    tSW
    [220816.24458556, 4822179.697546681]
    '''
    #
    if not closeEnoughDot0( easting, want_X ):
        #
        print3( 'easting, want_X:', easting, want_X )
        print3( 'easting:', getHowClose( easting, want_X ) )
        lProblems.append( 'proj_MN() SW corner of state (1st Dist) easting' )
        #
    #
    if not closeEnoughDot1( northing, want_Y ):
        #
        print3( 'northing, want_Y:', northing, want_Y )
        print3( 'northing:', getHowClose( northing, want_Y ) )
        lProblems.append( 'proj_MI() SW corner of state (1st Dist) northing' )
        #
    #
    #
    # North_Carolina North Carolina
    #
    sNorth_Carolina = '''
    http://ballotpedia.org/wiki/index.php/File:NCCongProposed.jpg
    http://www.findlatitudeandlongitude.com/
    NE corner (3rd, dangerous)
    2400 Sandfiddler Rd, Corolla, NC 27927, USA
    Latitude:36.5506394
    Longitude:-75.8680113
    #
    SE corner (7th, dangerous)
    214 Station House Way, Bald Head Island, NC 28461, USA
    Latitude:33.846932
    Longitude:-77.960559
    #
    SW corner (11th)
    Streamside Ln, Murphy, NC 28906, USA
    Latitude:34.9983777
    Longitude:-84.318326
    '''
    #
    easting, northing = proj_NC( -75.8680113, 36.5506394 ) # North Carolina
    # NE corner of state 3rd Dist)
    # want max x max y
    #
    want_X, want_Y = 398333.46411161125, 254620.23529478535
    #
    sGotThisAsFollows = '''
    from doShapeFileLookUps import getStateShapeFile
    sState = 'NC'
    tBBox, tPoints, tShapeBBoxes = getStateShapeFile( sState )
    nSum = oShapes[2].points[0][0] + oShapes[2].points[0][1]
    nSum
    632744.2369194701
    for t in oShapes[2].points:
        if t[0] + t[1] > nSum:
            nSum = t[0] + t[1]
            tNE = t
    
    tNE
    [398333.46411161125, 254620.23529478535]
    '''
    #
    #if not closeEnoughDot6( easting, want_X ):
        ##
        #print3( 'easting, want_X:', easting, want_X )
        #print3( 'easting:', getHowClose( easting, want_X ) )
        #lProblems.append( 'proj_NC() NE corner of state (3rd Dist) easting' )
        ##
    ##
    #if not closeEnoughDot6( northing, want_Y ):
        ##
        #print3( 'northing, want_Y:', northing, want_Y )
        #print3( 'northing:', getHowClose( northing, want_Y ) )
        #lProblems.append( 'proj_NC() NE corner of state (3rd Dist) northing' )
        ##
    #
    #
    easting, northing = proj_NC( -84.318326, 34.9983777 ) # North Carolina
    # SW corner of state 11th Dist)
    # want min x min y
    #
    want_X, want_Y = 123998.52270330489, 150396.45493598655
    #
    sGotThisAsFollows = '''
    from doShapeFileLookUps import getStateShapeFile
    sState = 'NC'
    tBBox, tPoints, tShapeBBoxes = getStateShapeFile( sState )
    tBBox
    [123998.52270330489, 822.5376727283001, 935803.798693958, 318099.5217798877]
    SW - NE
    lWest = [ lP for lP in oShapes[2].points if lP[0] == tBBox[0] ]
    lWest
    [[123998.52270330489, 150396.45493598655]]
    '''
    #
    if not closeEnoughDot0( easting, want_X ):
        #
        print3( 'easting, want_X:', easting, want_X )
        print3( 'easting:', getHowClose( easting, want_X ) )
        lProblems.append( 'proj_NC() SW corner of state (11th Dist) easting' )
        #
    #
    if not closeEnoughDot0( northing, want_Y ):
        #
        print3( 'northing, want_Y:', northing, want_Y )
        print3( 'northing:', getHowClose( northing, want_Y ) )
        lProblems.append( 'proj_MI() SW corner of state (11th Dist) northing' )
        #
    #
    #
    #
    sNew_Hampshire = '''
    http://www.findlatitudeandlongitude.com/
    Northern point (2nd)
    E Inlet Rd, Pittsburg, NH 03592, USA
    Latitude:45.2984372
    Longitude:-71.0843279
    #
    SW corner (2nd)
    1-17 Harbourt Dr, Winchester, NH 03470, USA
    Latitude:42.7298923
    Longitude:-72.4485866
    #
    along Southern border, Eastern end (2nd)
    1-11 Meadow Ln, Pelham, NH 03076, USA
    Latitude:42.7030611
    Longitude:-71.2928689
    #
    PINE TREE MONUMENT 99
    42, 41, 50.02729000000 = 42.69722980277778
    71, 19, 20.23866000000 = 71.32228851666666
    #
    NORTHINGM, EASTINGM = 21966.03300000000, 328217.48400000000
    EastingF, NorthingF = 1076829.0157437243, 72067.03740128654

    '''
    #
    easting, northing = proj_NH( -71.32228851666666, 42.69722980277778 ) # New Hampshire
    # first data row in geodeticnh.dbf
    #
    want_X, want_Y = 1076826.86209, 72066.8932675
    #
    sGotThisAsFollows = '''
    first data row in geodeticnh.dbf 
    NH geodetic control points from the NH GRANIT website
    PINE TREE MONUMENT 99
    '''
    #
    if not closeEnoughDot6( easting, want_X ):
        #
        print3( 'easting, want_X:', easting, want_X )
        print3( 'easting:', getHowClose( easting, want_X ) )
        lProblems.append( 'proj_NH() PINE TREE MONUMENT 99 easting' )
        #
    #
    if not closeEnoughDot4( northing, want_Y ):
        #
        print3( 'northing, want_Y:', northing, want_Y )
        print3( 'northing:', getHowClose( northing, want_Y ) )
        lProblems.append( 'proj_NH() PINE TREE MONUMENT 99 northing' )
        #
    #
    easting, northing = proj_NH( -71.08398726944444, 45.30546871944444 ) # New Hampshire
    # last data row in geodeticnh.dbf
    #
    want_X, want_Y = 1134171.3635425002, 1023198.1143608333
    #
    sGotThisAsFollows = '''
    last data row in geodeticnh.dbf 
    NH geodetic control points from the NH GRANIT website
    MON 475 IBC
    '''
    #
    if not closeEnoughDot6( easting, want_X ):
        #
        print3( 'easting, want_X:', easting, want_X )
        print3( 'easting:', getHowClose( easting, want_X ) )
        lProblems.append( 'proj_NH() MON 475 IBC easting' )
        #
    #
    if not closeEnoughDot6( northing, want_Y ):
        #
        print3( 'northing, want_Y:', northing, want_Y )
        print3( 'northing:', getHowClose( northing, want_Y ) )
        lProblems.append( 'proj_NH() MON 475 IBC 99 northing' )
        #
    #

    #
    easting, northing = proj_NH( -71.0843279, 45.2984372 ) # New Hampshire
    # northern point (2nd Dist)
    #
    want_X, want_Y = 398333.46411161125, 254620.23529478535
    #
    sGotThisAsFollows = '''
    not sure right now
    '''
    #
    easting, northing = proj_NH( -72.588552, 42.693891 ) # New Hampshire
    # northern point (2nd Dist)
    #
    want_X, want_Y = 745473.8751627404, 72029.90624999696
    #
    sGotThisAsFollows = '''
    from doShapeFileLookUps import getStateShapeFile
    sState = 'NH'
    tBBox, tPoints, tShapeBBoxes = getStateShapeFile( sState )
    tBBox
    [745473.8751627404, 72029.90624999696, 1242053.0000937672, 1023283.999999998]
    from geodeticnh.html:
        West_Bounding_Coordinate: -72.588552
        East_Bounding_Coordinate: -70.672045
        North_Bounding_Coordinate: 45.291923
        South_Bounding_Coordinate: 42.693891
    
    '''
    #
    sOregon = '''
    http://www.findlatitudeandlongitude.com/
    SE corner of state (2nd)
    max X min Y so max X - Y
    Address:State and County Line Rd, JORDAN VALLEY, OR 97910, USA
    Latitude:42.0029747
    Longitude:-117.0377191
    572425.0495406836, 172986.72867454588
    #
    NE corner of state (2nd)
    max Y and max Y so max X + Y
    Unnamed Rd, Joseph, OR 97846, USA
    Latitude:45.9523527
    Longitude:-116.9532878
    1002910.6049868762, 1326709.8421916068
    #
    NW corner of state (1st)
    min X and max Y so max Y - X
    Address:Jetty Rd, Hammond, OR 97121, USA
    Latitude:46.2265301
    Longitude:-124.0097902
    #
    SW corner of state (4th)
    min X and min Y so min X + Y
    Address:14400-14558 Oregon Coast Hwy, Brookings, OR 97415, USA
    Latitude:42.0021667
    Longitude:-124.2089189
    
    E most point
    45.614818
    -116.463726
    http://www.findlatitudeandlongitude.com/
    2345137.5423228294, 1430204.1095800549
    
    '''
    #
    sGotThisAsFollows = ''''
    E most point
    http://www.findlatitudeandlongitude.com/
    http://maps.google.com/
    from pprint import pprint
    from doShapeFileLookUps import getStateShapeFile
    import Shapes.ShapeTuples
    sState = 'OR'
    tBBox, tPoints, tShapeBBoxes = getStateShapeFile( sState )
    tBBox
    tCoordinates, tPointIndexs = Shapes.ShapeTuples.getPointsTouchingBBox( tPoints, tBBox )
    pprint( tCoordinates )
    '''
    #
    easting, northing = proj_OR( -117.0377191, 42.0029747 )
    # SE corner of state (2nd)
    want_X, want_Y = 572425.0495406836, 172986.72867454588
    #
    if 0 and not closeEnoughDot6( easting, want_X ):
        #
        print3( 'easting, want_X:', easting, want_X )
        print3( 'easting:', getHowClose( easting, want_X ) )
        lProblems.append( 'proj_OR() SE corner of state (2nd) easting' )
        #
    if 0 and not closeEnoughDot6( northing, want_Y ):
        #
        print3( 'northing, want_Y:', northing, want_Y )
        print3( 'northing:', getHowClose( northing, want_Y ) )
        lProblems.append( 'proj_OR() SE corner of state (2nd) northing' )
        #
    #
    easting, northing = proj_OR( -116.463726, 45.614818 )
    #
    want_X, want_Y = 2345137.5423228294, 1430204.1095800549
    #
    if not closeEnoughDot1( easting, want_X ):
        #
        print3( 'easting, want_X:', easting, want_X )
        print3( 'easting:', getHowClose( easting, want_X ) )
        lProblems.append( 'proj_OR() E most point easting' )
        #
    if not closeEnoughDot0( northing, want_Y ):
        #
        print3( 'northing, want_Y:', northing, want_Y )
        print3( 'northing:', getHowClose( northing, want_Y ) )
        lProblems.append( 'proj_OR() E most point northing' )
        #
    #
    #
    sTexas = '''
    Southernmost point along Rio Grande (34th)
    48499 Southpoint, Brownsville, TX 78521, USA
    Latitude:25.8551989
    Longitude:-97.397609
    #
    Westernmost point (16th)
    5 Paseo De Paz, El Paso, TX 79932, USA
    Latitude:31.897044
    Longitude:-106.645392
    #
    along Northern border, East corner (13th)
    County Road 31, Follett, TX 79034, USA
    Latitude:36.4966669
    Longitude:-100.0070321
    '''
    #
    easting, northing = proj_TX( -97.734, 30.277 )
    #
    want_X, want_Y = 1217516, 903786.6
    #
    if not closeEnoughDot2( easting, want_X ):
        #
        print3( 'easting, want_X:', easting, want_X )
        print3( 'easting:', getHowClose( easting, want_X ) )
        lProblems.append( 'proj_TX() given test numbers easting' )
        #
    if not closeEnoughDot2( northing, want_Y ):
        #
        print3( 'northing, want_Y:', northing, want_Y )
        print3( 'northing:', getHowClose( northing, want_Y ) )
        lProblems.append( 'proj_TX() given test numbers northing' )
        #
    #
    easting, northing = proj_UT( -111.79, 40.67 )
    #
    if False in tMap( closeEnoughDot6,
                    tZip( ( easting, northing ),
                          ( 433229.200074, 4502424.98334 ) ) ):
        #
        print3( easting, northing )
        lProblems.append( 'proj_UT() near Salt Lake City' )
        #
    #
    if False in tMap( closeEnoughDot6,
                    tZip( proj_UT( -111.8819291, 40.5707527 ),
                          ( 425348.84999999963, 4491482.01 ) ) ):
        #
        lProblems.append( 'proj_UT() given test numbers' )
        #
    #
    easting, northing = proj_UT( -111.8819291, 40.5707527 )
    #
    if False in tMap( closeEnoughDot6,
                    tZip( ( easting, northing ),
                          ( 425348.84999999963, 4491482.01 ) ) ):
        #
        lProblems.append( 'proj_UT() Proj and given test numbers' )
        #
    #
    sWisconsin = '''
    from the Lat/Long districting shapefiles:
    
    Western most point (7th)
    index 29550
    Lat:  45.64120292600006
    Long:-92.88943290699996
    294824.82019999996, 578245.1380000003
    
    min Y (S most) in 1st (first of two points):
    Lat:  42.491914749000046
    Long:-88.77642250099996, 
    index 4400
    620550.2652000003, 225120.59820000082

    max X (E most) in 8th:
    Lat:  45.39472389200006
    Long:-86.76398658799997,
    index 51717
    773288.3969999999, 551895.9298999999

    max Y (N most) in 7th:
    Lat:  47.08077430700007
    Long:-90.72933387699999,
    index 40391
    464635.6983000003, 734398.3846000005
    index 40390

    '''
    #
    easting, northing = proj_WI( -92.88943290699996, 45.64120292600006 )
    #
    if False in tMap( closeEnoughDot6,
                    tZip( ( easting, northing ),
                          ( 294824.82019999996, 578245.1380000003 ) ) ):
        #
        print3( easting, northing )
        lProblems.append( 'proj_WI() Western most point (7th)' )
        #
    #
    easting, northing = proj_WI( -88.77642250099996, 42.491914749000046 )
    #
    if False in tMap( closeEnoughDot6,
                    tZip( ( easting, northing ),
                          ( 620550.2652000003, 225120.59820000082 ) ) ):
        #
        print3( easting, northing )
        lProblems.append( 'proj_WI() min Y (S most) in 1st' )
        #
    #
    easting, northing = proj_WI( -86.76398658799997, 45.39472389200006 )
    #
    if False in tMap( closeEnoughDot6,
                    tZip( ( easting, northing ),
                          ( 773288.3969999999, 551895.9298999999 ) ) ):
        #
        print3( easting, northing )
        lProblems.append( 'proj_WI() max X (E most) in 8th' )
        #
    #
    easting, northing = proj_WI( -90.72933387699999, 47.08077430700007 )
    #
    if False in tMap( closeEnoughDot6,
                    tZip( ( easting, northing ),
                          ( 464635.6983000003, 734398.3846000005 ) ) ):
        #
        lProblems.append( 'proj_WI() max Y (N most) in 7th' )
        #
    #
    getConverted = getStateConverter( 'WI' )
    #
    easting, northing = getConverted( 45.39472389200006, -86.76398658799997 )
    #
    if False in tMap( closeEnoughDot6,
                    tZip( ( easting, northing ),
                          ( 773288.3969999999, 551895.9298999999 ) ) ):
        #
        lProblems.append( 'getStateConverter() WI' )
        #
    #
    getConverted = getStateConverter( 'WA' )
    #
    easting, northing = getConverted( 45.39472389200006, -86.76398658799997 )
    #
    if ( easting, northing ) != ( -86.76398658799997, 45.39472389200006 ):
        #
        lProblems.append( 'getStateConverter() WA' )
        #
    #
    #
    #
    sayTestResult( lProblems ) 