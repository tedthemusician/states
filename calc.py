import json
from math import atan2, cos, pi, sin, sqrt


# radius in miles
EARTH_RADIUS = 3958.8


def deg_to_rad(d):
    return d * (pi / 180)


def distance(lat1, lat2, lon1, lon2):
    phi1 = deg_to_rad(lat1)
    phi2 = deg_to_rad(lat2)
    lambda_1 = deg_to_rad(lon1)
    lambda_2 = deg_to_rad(lon2)
    d_phi = phi2 - phi1
    d_lambda = lambda_2 - lambda_1

    a = (sin(d_phi / 2) ** 2)\
        + (cos(phi1) * cos(phi2) * (sin(d_lambda / 2) ** 2))

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return c * EARTH_RADIUS


def get_dims(lat1, lat2, lon1, lon2):
    lat_avg = (lat1 + lat2) / 2
    lon_avg = (lon1 + lon2) / 2
    width  = distance(lat_avg, lat_avg, lon1, lon2)
    height = distance(lat1, lat2, lon_avg, lon_avg)
        
    return width, height


def get_points(lat1, lat2, lon1, lon2):
    north = max(lat1, lat2)
    south = min(lat1, lat2)
    west  = -max(lon1, lon2)
    east  = -min(lon1, lon2)
    
    return north, south, east, west


def get_elongation(width, height):
    ratio = width / height
    return ratio if ratio >= 1 else 1 / ratio


def get_info(state):
    name = state['name']
    lat1, lat2 = state['lats']
    lon1, lon2 = state['lons']
    north, south, east, west = get_points(lat1, lat2, lon1, lon2)
    width, height = get_dims(lat1, lat2, lon1, lon2)
    elongation = get_elongation(width, height)
    return {
        'name':       name,
        'north':      north,
        'south':      south,
        'east':       east,
        'west':       west,
        'width':      width,
        'height':     height,
        'elongation': elongation,
    }


def main():
    with open('./points.json', 'r') as f:
        states_points = json.load(f)
    states_info = [get_info(s) for s in states_points]
    with open('./data.json', 'w') as f:
        json.dump(states_info, f)


if __name__ == '__main__':
    main()
