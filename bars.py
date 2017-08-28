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
    seats_max = None
    bar_attribute = None
    for row in json_data['features']:
        seats_count = row['properties']['Attributes']['SeatsCount']
        ok = False
        if seats_max is None:
            ok = True
        elif seats_count > seats_max:
            ok = True
        if ok:
            seats_max = seats_count
            bar_attribute = row['properties']['Attributes']

    return seats_max, bar_attribute


def get_smallest_bar(json_data):
    seats_min = None
    bar_attribute = None
    for row in json_data['features']:
        seats_count = row['properties']['Attributes']['SeatsCount']
        ok = False
        if seats_min is None:
            ok = True
        elif seats_count < seats_min:
            ok = True

        if ok:
            seats_min = seats_count
            bar_attribute = row['properties']['Attributes']

    return seats_min, bar_attribute


def get_closest_bar(json_data, longitude, latitude):
    min_distance = None
    bar_attribute = None
    for row in json_data['features']:
        current_distance = get_distance(row['geometry']['coordinates'][0], row['geometry']['coordinates'][1], longitude, latitude)
        ok = False
        if min_distance is None:
            ok = True
        elif current_distance < min_distance:
            ok = True

        if ok:
            min_distance = current_distance
            bar_attribute = row['properties']['Attributes']

    return min_distance, bar_attribute

if __name__ == '__main__':
    aparser = argparse.ArgumentParser()
    aparser.add_argument("-f", "--file", required=True, help="Filepath")
    aparser.add_argument("-ln", "--lon", required=True, help="Longitute")
    aparser.add_argument("-lt", "--lat", required=True, help="Latitude")
    args = vars(aparser.parse_args())
    json_data = load_data(args['file'])

    seats_max, bar_attribute = get_biggest_bar(json_data)
    print("Biggest ->", bar_attribute['Name'], ",", bar_attribute['Address'], "| Max Seats ->", seats_max)
    seats_min, bar_attribute = get_smallest_bar(json_data)
    print("Smallest ->", bar_attribute['Name'], ",", bar_attribute['Address'], "| Min Seats ->", seats_min)
    dist_min, bar_attribute = get_closest_bar(json_data,  args["lon"], args["lat"])
    print("Closest ->", bar_attribute['Name'], ",", bar_attribute['Address'], "| Distance ->", dist_min, "km")
