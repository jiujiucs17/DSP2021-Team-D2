# created by David
import requests
import json
import time
import pandas as pd

API_KEY = "AIzaSyB8qaPf3iYXi8npCM19DpfwTnbCbpwYF80"

base_url_1 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=[LAT]%2C[LNG]&radius=[RADIUS]&type=[PLACE_TYPE]&key=" + API_KEY

base_url_2 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken=[PAGE_TOKEN]&key=" + API_KEY

base_url_3 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=[LAT]%2C[LNG]&rankby=distance&name=[KEYWORD]&type=[PLACE_TYPE]&key=" + API_KEY

base_url_4 = "https://maps.googleapis.com/maps/api/distancematrix/json?destinations=[DEST_LAT]%2C[DEST_LNG]&origins=[ORG_LAT]%2C[ORG_LNG]&key=" + API_KEY

def ClearSpace(input_list):
    output_list = []
    for this_str in input_list:
        this_str = this_str.replace(" ", "_")
        output_list.append(this_str)
    return output_list

def Intersection(list_A, list_B):
    return(list(set(list_A) & set(list_B)))

def Name_Contains(name, target_types):
    output = False
    name = name.lower()
    name = name.replace(" ", "_")
    for this_type in target_types:
        if name.find(this_type) >=0:
            output = True
            break
    return output

def Find_Nearby_Places(latitude = None, longitude = None, radius = None, places = None, page_token = None):

    places = ClearSpace(places)

    if page_token is None:
        place_type = "|".join(places)

        url = base_url_1.replace("[LAT]", str(latitude))
        url = url.replace("[LNG]", str(longitude))
        url = url.replace("[RADIUS]", str(radius))
        url = url.replace("[PLACE_TYPE]", place_type)
    else:
        url = base_url_2.replace("[PAGE_TOKEN]", page_token)

    # print(url)

    payload ={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    response_places = json.loads(response.text)

    count = 0
    for this_place in response_places["results"]:
        # print(this_place["name"])
        if len(Intersection(places, this_place["types"])) > 0 or Name_Contains(this_place["name"], places):
            count += 1

    if response.text.find("next_page_token") >=0:
        time.sleep(2)
        next_page_token = response_places["next_page_token"]
        count += Find_Nearby_Places(places = places, page_token = next_page_token)

    return count

def Find_Nearest_FireStation(latitude, longitude):
    keyword = "fire|station"
    place_type = "fire_station"
    url = base_url_3.replace("[LAT]", str(latitude))
    url = url.replace("[LNG]", str(longitude))
    url = url.replace("[PLACE_TYPE]", place_type)
    url = url.replace("[KEYWORD]", keyword)

    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    response_places = json.loads(response.text)

    return [response_places["results"][1]["geometry"]["location"]["lat"], response_places["results"][1]["geometry"]["location"]["lng"]]

def Get_Distance(from_lat, from_lng, to_lat, to_lng):

    url = base_url_4.replace("[ORG_LAT]", str(from_lat))
    url = url.replace("[ORG_LNG]", str(from_lng))
    url = url.replace("[DEST_LAT]", str(to_lat))
    url = url.replace("[DEST_LNG]", str(to_lng))

    payload ={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    result = json.loads(response.text)

    distance = result["rows"][0]["elements"][0]["distance"]["text"]
    duration = result["rows"][0]["elements"][0]["duration"]["text"]

    return [distance, duration]

def Update_Dataset(file_name, radius):
    data = pd.read_excel(file_name)

    for i in range(data.shape[0]):
        this_lat = data.loc[i, "Latitude"]
        this_lng = data.loc[i, "Longitude"]

        targets = ["hospital", "medisch_centrum", "health"]
        data.loc[i, "Hospitals"] = Find_Nearby_Places(latitude=this_lat, longitude=this_lng, radius=radius,
                                                      places=targets)

        targets = ["school", "primary_school", "secondary_school", "university"]
        data.loc[i, "Education_Premises"] = Find_Nearby_Places(latitude=this_lat, longitude=this_lng, radius=radius,
                                                               places=targets)

        targets = ["kinderopvang", "kindergarten", "nursery"]
        data.loc[i, "Children_Day_Care"] = Find_Nearby_Places(latitude=this_lat, longitude=this_lng, radius=radius,
                                                              places=targets)

        targets = ["nursing_home", "verzorgingshuis"]
        data.loc[i, "Elderly_House"] = Find_Nearby_Places(latitude=this_lat, longitude=this_lng, radius=radius,
                                                          places=targets)

        targets = ["transit_station", "subway_station", "transit_station"]
        data.loc[i, "Public_Transport"] = Find_Nearby_Places(latitude=this_lat, longitude=this_lng, radius=radius,
                                                             places=targets)

        targets = ["hotel", "lodging"]
        data.loc[i, "Hotels"] = Find_Nearby_Places(latitude=this_lat, longitude=this_lng, radius=radius, places=targets)

        targets = ["store", "restaurant", "gym", "movie_theater"]
        data.loc[i, "Store_Restaurant_Gym_Cinema"] = Find_Nearby_Places(latitude=this_lat, longitude=this_lng,
                                                                        radius=radius, places=targets)

        fire_station_loc = Find_Nearest_FireStation(this_lat, this_lng)
        distance_time = Get_Distance(fire_station_loc[0], fire_station_loc[1], this_lat, this_lng)
        distance_time[0] = distance_time[0].replace("km", "")
        distance_time[0] = distance_time[0].strip()
        distance_time[1] = distance_time[1].replace("mins", "")
        distance_time[1] = distance_time[1].strip()
        # data.loc[i, "Distance_FireStation_km"] = distance_time[0]
        data.loc[i, "Distance_FireStation_min"] = distance_time[1]

    data.to_excel(file_name, index = False)
    print("update data done")
