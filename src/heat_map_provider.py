import numpy as np
from scipy.stats import norm
import json
from math import sin, cos, sqrt, atan2, radians, exp


def do_the_job(message_data):
    
    parameters = {}
    for aspect in message_data['tags']:
        parameters[aspect['name']] = (aspect['pref']-1.5)*2
        
    filter_tag = parameters.keys()
    
    location_by_tags = {}
    for key in filter_tag:
        location_by_tags[key] = set()
        
    with open('resources/places.json', encoding="utf8") as json_file:
        places_data = json.load(json_file)
        for place in places_data['data']:
            for tag in place['tags']:
                if tag['name'] in filter_tag:
                    location = (place['location']['lat'], place['location']['lon'])
                    location_by_tags[tag['name']].add(location)
    
    
    min_lat = 60.14
    min_lon = 24.91
    max_lat = 60.19
    max_lon = 24.99
    
    lats = np.arange(min_lat, max_lat, .001)
    lons = np.arange(min_lon, max_lon, .002)
    
    def lat_lon_distance(lat1, lon1, lat2, lon2):
        R = 6373.0
        
        x1 = radians(lat1)
        y1 = radians(lon1)
        x2 = radians(lat2)
        y2 = radians(lon2)
        
        dlon = y2 - y1
        dlat = x2 - x1
        
        a = sin(dlat / 2)**2 + cos(x1) * cos(x2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        return R * c
    
    
    def calculate_relevance_place_in_distance(dist):
        return exp(-(dist**2)/(2*(0.1)))/2.50662827
    
    def value_of_location(chosen_lat, chosen_lon, locations):
        value = 0
        for location in locations:
            value += calculate_relevance_place_in_distance(lat_lon_distance(chosen_lat, chosen_lon, location[0], location[1]))
        return value
    
    heat_map = np.zeros(shape=(lats.shape[0], lons.shape[0]))
    
    for tag_name in location_by_tags:
        for i, chosen_lat in enumerate(lats):
            for j, chosen_lon in enumerate(lons):
                heat_map[i, j] += value_of_location(chosen_lat, chosen_lon, location_by_tags[tag_name]) * parameters[tag_name]
    
    values_by_location_list = list()
    for i, lat in enumerate(lats):
        for j, lon in enumerate(lons):
            values_by_location_list.append(
                {
                       'latitude': lat,
                       'longitude': lon,
                       'weight': heat_map[i, j],
                })
         
    return values_by_location_list

