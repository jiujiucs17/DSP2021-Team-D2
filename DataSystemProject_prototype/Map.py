# -*- coding: utf-8 -*-
# Created by Liya, modified by Mengqi
import numpy as np
import pandas as pd
import folium
import Clustering
from geopy.geocoders import Nominatim  # convert an address into latitude and longitude values

import MainDashboard

defaultWeightPath = "raw_data/features_default_weight.xlsx"
clusterImportancePath = "raw_data/cluster_importance_weight.xlsx"
icon_colours = ["#6F69AC", "#95DAC1", "#FFEBA1", "#FD6F96", "#64C9CF", "#FDE49C", "#FFB740", "#DF711B"]
displayedFeatureNames = ['Petrol Station Names', 'Fuel Type (Diesel)', 'Fuel Type (Petrol)', 'Fuel Type (CNG)', 'Fuel Type (LPG)', 'Shop open for 24/7', 'Hospitals', 'Education Premises', 'Children Day Care', 'Elderly House', 'Residential Area', 'Business Area', 'Leisure Area', 'Industrial Area', 'Public Transport', 'Highways (A)', 'Highways (N)', 'Highways (S)', 'Hotels', 'Store, Restaurant, Gym, Cinema', 'Distance to Fire Station (min)']


class map():
    defaultWeight = pd.read_excel(defaultWeightPath)
    featureWeight = pd.read_excel(defaultWeightPath) # the actually used weight
    clusterImportance = pd.read_excel(clusterImportancePath)

    @classmethod
    def updateImportance(cls):
        map.clusterImportance = pd.read_excel(clusterImportancePath)

    def __init__(self, dataFile):
        self.dataFile = dataFile
        address = ' Amsterdam, North Holland, Netherlands'
        geolocator = Nominatim(user_agent="http")
        location = geolocator.geocode(address)
        self.latitude = location.latitude
        self.longitude = location.longitude
        self.list_color = [
            'red', 'blue', 'gray', 'darkred', 'green', 'purple',
            'orange', 'pink', 'beige', 'lightred', 'darkgreen', 'lightgreen', 'darkblue',
            'lightblue', 'darkpurple', 'cadetblue', 'lightgray', 'black']
        self.rainbow = [
            'blue', 'gray', 'green', 'purple',
            'orange', 'beige', 'darkgreen', 'lightgreen', 'darkblue',
            'lightblue', 'darkpurple', 'cadetblue', 'lightgray']
        # clusters
        self.data = Clustering.clustering(self.dataFile).data
        # stores the output map file, can be further output as html ↓
        self.map_amsterdam = folium.Map(location=[self.latitude, self.longitude], zoom_start=13)

        for lat, lng in zip(self.data['Latitude'], self.data['Longitude']):
            folium.Marker([lat, lng]).add_to(self.map_amsterdam)

    def showStationWithoutCLustering(self):
        self.map_amsterdam = folium.Map(location=[self.latitude, self.longitude], zoom_start=13)
        for lat, lng in zip(self.data['Latitude'], self.data['Longitude']):
            folium.Marker([lat, lng]).add_to(self.map_amsterdam)

    def updateData(self, dataFile):
        self.dataFile = dataFile
        self.data = Clustering.clustering(self.dataFile).data
        self.showStationWithoutCLustering()

    def buildClusteredMap(self, radius=1, cluster=0):
        # reload the clustered data with the newest parameters
        self.data = Clustering.clustering(self.dataFile, radius, cluster=cluster).data
        # recreate a new map to exclude the previous added markers(if any)
        self.map_amsterdam = folium.Map(location=[self.latitude, self.longitude], zoom_start=13)
        clusterNumber = []
        for lat, lng, cluster, score, i in zip(self.data['Latitude'], self.data['Longitude'],
                                            self.data[Clustering.clusters[cluster]],
                                            self.data['Effect_Score'],
                                            range(self.data.shape[0])):
            df_details = pd.DataFrame(self.data.iloc[i, 0:21])
            df_details.index = displayedFeatureNames
            print(df_details)
            details = df_details.to_html()
            html = f"<p>Group: {cluster + 1} <p/> \
                  <p>Effect Score: {score} <p/> \
                  <p>Details: <p/>\
                   {details} <p/> "
            iframe = folium.IFrame(html, width=300, height=400)
            label = folium.Popup(iframe, max_width=500, parse_html=True)
            folium.Marker(
                [lat, lng],
                popup=label,
                icon=folium.Icon(color=self.rainbow[cluster])
            ).add_to(self.map_amsterdam)
            clusterNumber.append(cluster)
        clusterNumber = np.unique(np.array(clusterNumber))
        MainDashboard.MainDashboardWindow.clusterIndex = clusterNumber
        # self.map_amsterdam.save("MapOutput.html")
        for lat, lng in zip(self.data['Latitude'], self.data['Longitude']):
            # folium.CircleMarker([lat, lng], radius=2, color='blue', fill=True, fill_color='blue', fill_opacity=1).add_to(map_berlin)
            folium.Circle([lat, lng], radius=200, color='red', fill=True, fill_color='red', fill_opacity=0.4).add_to(
                self.map_amsterdam)
            folium.Circle([lat, lng], radius=radius * 1000, color='orange', fill=True, fill_color='orange',
                          fill_opacity=0.1).add_to(self.map_amsterdam)
