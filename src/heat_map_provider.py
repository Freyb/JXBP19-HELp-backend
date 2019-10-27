import numpy as np
from scipy.stats import norm
import json
from math import sin, cos, sqrt, atan2, radians, exp, tanh

def do_the_job(message_data):
    
    parameters = {}
    for aspect in message_data['tags']:
        print(aspect['pref'])
        if aspect['pref'] == 0:
            parameters[aspect['name']] = -3
        elif aspect['pref'] == 1:
            parameters[aspect['name']] = -1
        elif aspect['pref'] == 2:
            parameters[aspect['name']] = 1
        elif aspect['pref'] == 3:
            parameters[aspect['name']] = 3
        else:
            parameters[aspect['name']] = 0
        
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
    
    with open('resources/station_visits.json', encoding="utf8") as json_file:
        station_visits_data = json.load(json_file)
    
    
    max_lat= 60.185437
    min_lat = 60.141590
    min_lon= 24.489979
    max_lon= 25.202071
    
    lats = np.arange(min_lat, max_lat, .003)
    lons = np.arange(min_lon, max_lon, .006)
    
    def calculate_relevance_place_in_distance(dist):
        return exp(-(dist**2)/(2*(0.02)))/2.50662827
    
    def value_of_location(chosen_lat, chosen_lon, locations):
        value = 0
        for location in locations:
            value += calculate_relevance_place_in_distance(lat_lon_distance(chosen_lat, chosen_lon, location[0], location[1]))
        return value
    
    def value_closest_station(chosen_lat, chosen_lon, station_visits_data):
        ret = 0
        min_dist = lat_lon_distance(chosen_lat, chosen_lon, station_visits_data['stations'][0]['latitude'], station_visits_data['stations'][0]['longitude'])
        for station in station_visits_data['stations']:
            dist = lat_lon_distance(chosen_lat, chosen_lon, station['latitude'], station['longitude'])
            if dist < min_dist:
                min_dist = dist
                ret = (station['visitors_normalized'] / 50)
        return ret
    
    heat_map = np.zeros(shape=(lats.shape[0], lons.shape[0]))
    
    for tag_name in location_by_tags:
        for i, chosen_lat in enumerate(lats):
            for j, chosen_lon in enumerate(lons):
                if tag_name == 'Visitors':
                    value = value_closest_station(chosen_lat, chosen_lon, station_visits_data)
                else:
                    value = value_of_location(chosen_lat, chosen_lon, location_by_tags[tag_name])
                heat_map[i, j] += (value * parameters[tag_name])
        
                
        
    print(np.max(heat_map))
    
    heat_map = heat_map - np.min(heat_map)

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

def get_lists_section(list1, list2):
    ret = list()
    for elem in list1:
        if elem["name"] in list2:
            ret.append(elem["name"])

    return ret

def do_the_job_2(message_data):
    with open('resources/places.json', encoding="utf-8") as json_file:
        places_data = json.load(json_file)
    
    ret = list()
    for place in places_data["data"]:
        if lat_lon_distance(message_data["latitude"], message_data["longitude"],
            place["location"]["lat"], place["location"]["lon"]) < 0.5 and len(get_lists_section(place["tags"], message_data["tags"])) > 0:
            ret.append({"name" : place["name"]["en"], "id" : place["id"], "website" : place["info_url"]})

    print(ret)
    return ret
    