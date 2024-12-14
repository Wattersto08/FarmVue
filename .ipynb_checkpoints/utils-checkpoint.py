from datetime import datetime, timedelta
import pandas as pd 
import random as r 

def generate_date_strings(start_date, end_date):
    date_list = []
    current_date = start_date

    while current_date <= end_date:
        date_list.append(current_date.strftime('%Y-%m-%d'))  # Format the date as a string
        current_date += timedelta(days=1)  # Move to the next day

    return date_list


def spoofDataSets(sd,ed,name,opPath,features):
    date_strings = generate_date_strings(sd, ed)

    print('     Generating Data for ' + name + '\n')
    
    for dt in date_strings:
        datapoints_list = pd.DataFrame(columns=['fieldID', 'ID', 'Coord'])
        filename = (name+'-'+dt+'.csv')
        filepath = (opPath + filename)
        
        print('\tGenerating Data for ' + dt)

        if(type(features) is list):
            for feature in features: 
                datapoints_list = pd.concat([datapoints_list,feature.sensorPoints])
        else:
            datapoints_list = features.sensorPoints

        ESCA = []
        BlackLeaf = []
        Humidity = []
        
        for i in range(len(datapoints_list)):
            ESCA.append(r.randint(0,100)/100)
            BlackLeaf.append(r.randint(0,100)/100)
            Humidity.append(r.randint(0,100)/100)
        
        datapoints_list['ESCA'] = ESCA
        datapoints_list['BlackLeaf'] = BlackLeaf
        datapoints_list['Humidity'] = Humidity
        datapoints_list.to_csv(filepath)
    print('\n\t    * * * Complete! * * * ')