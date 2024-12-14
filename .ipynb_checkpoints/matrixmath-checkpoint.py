import math as m 
from shapely.geometry import Point, Polygon
import numpy as np
import pandas as pd

def getRadius(midpoint, shape):
    rads = []
    for i in shape: 
        rads.append(m.dist(midpoint, i))
    return max(rads)
    
def rotate(origin, point, angle):
    ox, oy = origin
    px, py = point
    qx = ox + m.cos(angle) * (px - ox) - m.sin(angle) * (py - oy)
    qy = oy + m.sin(angle) * (px - ox) + m.cos(angle) * (py - oy)
    return qx, qy

def calc_matrix(limits,matrix_res,midpoint,crop_bearing):
    
    matrix = []
    matrix_rotated = []
    
    opx = [limits[0][0]]
    opy = [limits[0][1]]
    
    stepX = (limits[1][0] - limits[0][0])/matrix_res
    stepY = (limits[1][1] - limits[0][1])/matrix_res
      
    for j in range(1,matrix_res):
        opy.append(limits[0][1]+(stepY*j))
        opx.append(limits[0][0]+(stepX*j))
        
    opx.append(limits[1][0])
    opy.append(limits[1][1])
    
    for x in opx:
        for y in opy:
            matrix.append([x,y])
    
    for point in matrix:
        matrix_rotated.append(rotate(midpoint ,point, -m.radians(crop_bearing)))
         
    return matrix_rotated 


def check_within_poly(coords, matrix_coords):
    poly = Polygon(coords)

    op_matrix = []
    for matrix_point in matrix_coords:
        p = Point(matrix_point[0],matrix_point[1])
        if p.within(poly):
            op_matrix.append(matrix_point)

    return op_matrix


def check_within_poly_logic(coords, point):
    poly = Polygon(coords)
    p = Point(point)
    if p.within(poly):
        return True
    else:
        return False


def calc_matrix_proto(coords,limits,matrix_res,midpoint,crop_bearing):
    
    matrix = []
    matrix_rotated = []
    
    opx = [limits[0][0]]
    opy = [limits[0][1]]
    
    stepX = (limits[1][0] - limits[0][0])/matrix_res
    stepY = (limits[1][1] - limits[0][1])/matrix_res
      
    for j in range(1,matrix_res):
        opy.append(limits[0][1]+(stepY*j))
        opx.append(limits[0][0]+(stepX*j))
        
    opx.append(limits[1][0])
    opy.append(limits[1][1])
    
    for x in opx:
        for y in opy:
            matrix.append([x,y])
    
    for point in matrix:
        if check_within_poly_logic(coords, point) == True:
            matrix_rotated.append(rotate(midpoint ,point, -m.radians(crop_bearing)))
    
    return matrix_rotated 

def genMatrix(coords, midpoint,  rowcol, bearing):
    radius = getRadius(midpoint, coords)
    refpoint = [(midpoint[0] - radius), (midpoint[1] - radius)]
    spacing = (2*radius)/rowcol

    xpts = (refpoint[0]+(np.array(list(range(0,rowcol+1)))*spacing))
    ypts = (refpoint[1]+(np.array(list(range(0,rowcol+1)))*spacing))

    ptsMatrix = []
    for x in xpts: 
        for y in ypts:
            ptsMatrix.append([x,y])

    circMatrix = []
    for pt in ptsMatrix:
        if(pt[0] - midpoint[0])**2 + (pt[1] - midpoint[1])**2 <radius**2:
            circMatrix.append(pt)

    if (bearing != 0):
        rotMatrix = []
        for pt in circMatrix:
            rotMatrix.append(rotate(midpoint,pt,bearing))
    else: 
        rotMatrix = circMatrix

            
    return check_within_poly(coords, rotMatrix)
    
def generateSensorPointsDF(name, matrix_coords):
    IDS = []
    for i in range(len(matrix_coords)):
        IDS.append('{:06X}'.format(i))
    return pd.DataFrame({'fieldID': name, 'ID':IDS, 'Coord':matrix_coords})

    
def get_matrix(coords,limits,matrix_res,midpoint,crop_bearing):
    return check_within_poly(coords,calc_matrix(limits,matrix_res,midpoint,crop_bearing))