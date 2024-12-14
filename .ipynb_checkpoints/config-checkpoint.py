import pandas as pd 

class Object:

    def __init__(self,filepath):
        self.path = filepath
        self.df = pd.read_csv(filepath)
        self.grid_res = self.df.query('param=="grid_res"').iloc[0]['value']
        self.bearing_default = self.df.query('param=="bearing_default"').iloc[0]['value']
        
    def __str__(self):
        return "Config Handler"

