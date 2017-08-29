import json
import argparse
from math import sin, cos, sqrt, atan2, radians


def get_distance(lon1, lat1, lon2, lat2):
    """
    func to get Distance beetween two locations
    return value in KM
    """
    approximate_radius = 6373.0

    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))

    dist_lon = float(lon2) - float(lon1)
    dist_lat = float(lat2) - float(lat1)

    math_tmp = sin(dist_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(dist_lon / 2)**2
    final_dist = 2 * atan2(sqrt(math_tmp), sqrt(1 - math_tmp))

    return approximate_radius * final_dist


def load_data(file_path):
    with open(file_path, 'r') as data_file:
        return json.load(data_file)


def get_biggest_bar(json_data):
    bars = json_data['features']
    bar_max = max(bars, key=lambda p: p['properties']['Attributes']['SeatsCount'])
    return bar_max['properties']['Attributes']


def get_smallest_bar(json_data):
    bars = json_data['features']
    bar_min = min(bars, key=lambda p: p['properties']['Attributes']['SeatsCount'])
    return bar_min['properties']['Attributes']


def get_closest_bar(json_data, longitude, latitude):
    bars = json_data['features']
    bar_min_dist = min(bars, key=lambda p: get_distance(p['geometry']['coordinates'][0], p['geometry']['coordinates'][1], longitude, latitude))
    min_dist = get_distance(bar_min_dist['geometry']['coordinates'][0], bar_min_dist['geometry']['coordinates'][1], longitude, latitude)
    return min_dist, bar_min_dist['properties']['Attributes']

if __name__ == '__main__':
    aparser = argparse.ArgumentParser()
    aparser.add_argument("-f", "--file", required=True, help="Filepath")
    aparser.add_argument("-ln", "--lon", required=True, help="Longitute")
    aparser.add_argument("-lt", "--lat", required=True, help="Latitude")
    args = vars(aparser.parse_args())
    json_data = load_data(args['file'])

    bar_attribute = get_biggest_bar(json_data)
    print("Biggest ->", bar_attribute['Name'], ",", bar_attribute['Address'], "| Max Seats ->", bar_attribute['SeatsCount'])
    bar_attribute = get_smallest_bar(json_data)
    print("Smallest ->", bar_attribute['Name'], ",", bar_attribute['Address'], "| Min Seats ->", bar_attribute['SeatsCount'])
    min_dist, bar_attribute = get_closest_bar(json_data,  args["lon"], args["lat"])
    print("Closest ->", bar_attribute['Name'], ",", bar_attribute['Address'], "| Min dist -> ", min_dist, "km")
