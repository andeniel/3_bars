import json
import argparse
from math import sin, cos, sqrt, atan2, radians
from geomath.point import Point


def get_distance(lon1, lat1, lon2, lat2):
    return Point(float(lon1), float(lat1)) \
            .distance(Point(float(lon2), float(lat2)))


def load_data(file_path):
    with open(file_path, 'r') as data_file:
        return json.load(data_file)


def get_biggest_bar(json_data):
    bars = json_data['features']
    bar_max = max(
        bars,
        key=lambda p: p['properties']['Attributes']['SeatsCount'])
    return bar_max['properties']['Attributes']


def get_smallest_bar(json_data):
    bars = json_data['features']
    bar_min = min(
        bars,
        key=lambda p: p['properties']['Attributes']['SeatsCount'])
    return bar_min['properties']['Attributes']


def get_closest_bar(json_data, longitude, latitude):
    bars = json_data['features']
    bar_min_dist = min(
        bars,
        key=lambda p: get_distance(
            p['geometry']['coordinates'][0],
            p['geometry']['coordinates'][1],
            longitude,
            latitude))
    min_dist = get_distance(
        bar_min_dist['geometry']['coordinates'][0],
        bar_min_dist['geometry']['coordinates'][1], longitude, latitude)
    return min_dist, bar_min_dist['properties']['Attributes']

if __name__ == '__main__':
    aparser = argparse.ArgumentParser()
    aparser.add_argument("-f", "--file", required=True, help="Filepath")
    aparser.add_argument("-ln", "--lon", required=True, help="Longitute")
    aparser.add_argument("-lt", "--lat", required=True, help="Latitude")
    args = aparser.parse_args()
    json_data = load_data(args.file)

    bar_attribute = get_biggest_bar(json_data)
    print(
        "Biggest ->", bar_attribute['Name'], ",", bar_attribute['Address'],
        "| Max Seats ->", bar_attribute['SeatsCount'])

    bar_attribute = get_smallest_bar(json_data)
    print(
        "Smallest ->", bar_attribute['Name'], ",", bar_attribute['Address'],
        "| Min Seats ->", bar_attribute['SeatsCount'])

    min_dist, bar_attribute = get_closest_bar(
        json_data,  args.lon, args.lat)
    print(
        "Closest ->", bar_attribute['Name'], ",", bar_attribute['Address'],
        "| Min dist -> ", min_dist)
