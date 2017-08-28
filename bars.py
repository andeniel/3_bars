import json
import argparse
from math import sin, cos, sqrt, atan2, radians

def get_distance(lon1, lat1, lon2, lat2):
    """func to get Distance beetween two locations, result in KM"""
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))

    dlon = float(lon2) - float(lon1)
    dlat = float(lat2) - float(lat1)

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def load_data(filepath):
    """func to read a file to data"""
    with open(filepath, 'r') as data_file:
        return json.load(data_file)

def get_biggest_bar(data):
    """func to get biggest bar by seatscount"""
    seats = None
    barAttr = None
    for row in data['features']:
        cnt = row['properties']['Attributes']['SeatsCount']
        ok = False
        if seats is None:            
            ok = True
        elif cnt > seats:
            ok = True        
        if ok:
            seats = cnt
            barAttr = row['properties']['Attributes']

    return seats, barAttr

def get_smallest_bar(data):
    """func to get smallest bar by seatscount"""
    seats = None
    barAttr = None
    for row in data['features']:
        cnt = row['properties']['Attributes']['SeatsCount']
        ok = False
        if seats is None:
            ok = True
        elif cnt < seats:        
            ok = True
        
        if ok:
            seats = cnt
            barAttr = row['properties']['Attributes']

    return seats, barAttr

def get_closest_bar(data, longitude, latitude):
    """func to get closest bar by lon and lat"""
    minDist = None
    barAttr = None
    for row in data['features']:
        dist = get_distance(
            row['geometry']['coordinates'][0], 
            row['geometry']['coordinates'][1],
            longitude,
            latitude
            )
        ok = False
        if minDist is None:
            ok = True
        elif dist < minDist:
            ok = True

        if ok:
            minDist = dist
            barAttr = row['properties']['Attributes']

    return minDist, barAttr

if __name__ == '__main__':
    aparser = argparse.ArgumentParser()
    aparser.add_argument("-f", "--file", required=True, help="Filepath")
    # 37.621587946152012, 55.765366956608361
    aparser.add_argument("-ln", "--lon", required=True, help="Longitute")
    aparser.add_argument("-lt", "--lat", required=True, help="Latitude")
    args = vars(aparser.parse_args())
    jsondata = load_data(args['file'])

    seats, bar = get_biggest_bar(jsondata)
    print("Biggest ->", bar['Name'], ",", bar['Address'], "| Max Seats ->", seats)
    seats, bar = get_smallest_bar(jsondata)    
    print("Smallest ->", bar['Name'], ",", bar['Address'], "| Min Seats ->", seats)
    dist, bar = get_closest_bar(jsondata,  args["lon"], args["lat"])
    print("Closest ->", bar['Name'], ",", bar['Address'], "| Distance ->", dist,"km")    
