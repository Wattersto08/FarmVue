import random 
from shapely.geometry import Point, Polygon
import math as m
from matrixmath import genMatrix, generateSensorPointsDF
import pandas as pd
import config

path = 'config/parameters.csv'
cfg = config.Object(path)

color_options = ['blue',  'darkgreen', 'darkred', 'green', 'lightblue', 'lightgray', 'lightgreen', 'orange', 'pink','purple', 'red', 'white']

class Object:
    global color_options
    global cfg 
    
    def __init__(self, name, coords, Type, midpoint):
        self.name = name
        self.coords = coords
        self.midpoint = midpoint
        self.Type = Type
        self.color = color_options[random.randint(0,len(color_options)-1)]
        self.crop = 'white_grape'
        self.crop_bearing = cfg.bearing_default
        self.limits = self.get_limits()
        self.matrix_res = cfg.grid_res
        if (self.Type == 'polygon'):
            self.matrix_coords = genMatrix(self.coords,self.midpoint,self.matrix_res,self.crop_bearing)
            self.sensorPoints = generateSensorPointsDF(self, self.matrix_coords)
        else:
            self.matrix_coords = []
            self.sensorPoints = pd.DataFrame(columns=['fieldID', 'ID', 'Coord'])

    def __str__(self):
        return f"{self.name} - {self.crop}"
    
    def dumpdata(self):
        print(self.name)
        print(self.Type)
        print(self.color)
        print(self.coords)
        
    def get_limits(self):
        if self.Type == 'Point':
            self.limits = self.midpoint
        else:
            x = []
            y = []
            for coord in self.coords:
                x.append(coord[0])
                y.append(coord[1])

            self.limits = [[min(x),min(y)],[max(x),max(y)]]
    
    def calc_matrix(self):
        self.matrix_coords = genMatrix(self.coords,self.midpoint,self.matrix_res,self.crop_bearing)