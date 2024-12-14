import pandas as pd
import random as rd
import bs4 as bs
from bs4 import BeautifulSoup
import kml_object 
import random as rnd 


def parse_coord_string(coord_string):
    longitudes = []
    latitudes = []

    coord_string = coord_string.replace('\n','')
    coord_string = coord_string.replace('\t','')
    coord_string = coord_string.replace(' ',',')
    coord_string = coord_string[:-1]
    coords = coord_string.split(',')


    for i in range(0,len(coords),3):
        longitudes.append(coords[i])
    for i in range(1,len(coords),3):
        latitudes.append(coords[i])
        
    op = []
    for i in range(len(longitudes)):
        op.append([latitudes[i],longitudes[i]])
    
    return op

def convert_coord_lisstring_to_lisfloats(inputlist):
    op = []
    for i in inputlist:
        op.append([float(i[0]),float(i[1])])

    return op 

def get_farm_midpoint(featurelist):
    b = []
    for f in featurelist:
        a = f.coords
        b = b + a 
    return b 

def get_midpoint(list_of_coords):
    xav = 0
    yav=0
    for i in list_of_coords:
        xav = xav+i[0]
        yav = yav+i[1]

    return [(xav/len(list_of_coords),yav/len(list_of_coords))]

def get_limits(coords):
    x = []
    y = []
    for coord in coords:
        x.append(coord[0])
        y.append(coord[1])

    return [[min(x),min(y)],[max(x),max(y)]]


def parse_KML(filename):
    file = open(filename, "r")
    contents = file.read()
    soup = BeautifulSoup(contents, 'xml')
    names = soup.find_all('name')

    features = soup.find_all('Placemark')

    #process names
    project_name = str(names[0])[10:-11]

    obj_list = []

    for feature in features:
        
        featurename = str(feature.find_all('name'))[11:-12]
        coords = convert_coord_lisstring_to_lisfloats(parse_coord_string(feature.coordinates.text))
        midpoint = get_midpoint(coords)[0]
        
        if feature.find('Polygon'):
            featuretype = 'polygon'

        if feature.find('Point'):
            featuretype = 'Point'

        if feature.find('LineString'):
            featuretype = 'LineString'
        
        
        obj_list.append(kml_object.Object(featurename,coords,featuretype,midpoint))
    
    get_farm_midpoint(obj_list)
    
    for obj in obj_list:
        obj.get_limits()
        
    return project_name, get_midpoint(get_farm_midpoint(obj_list))[0], obj_list




