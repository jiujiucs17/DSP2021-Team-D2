# -*- coding: utf-8 -*-
# Created by Liya, modified by Mengqi

import pandas as pd
import numpy as np
import Map
import sys
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering, MeanShift, estimate_bandwidth
from sklearn.linear_model import LogisticRegression
from kmodes.kprototypes import KPrototypes

clusters = ["KMeans", "DBSCAN", "Mean_Shift", "KPrototype", "Effect_Score"]


class clustering():

    def __init__(self, datafilepath, radius=1, cluster=0):
        self.dataFilePath = datafilepath
        self.radius = radius
        # self.userWeight = Map.map.getPlainWeight()
        self.data = pd.read_excel(self.dataFilePath)

        # Postcode included
        self.X = self.data.iloc[:, 1:22]
        self.X.PostCode = self.X.PostCode.str[:4].astype(int)
        self.X = self.X.to_numpy()

        # Postcode not included
        self.X1 = self.data.iloc[:, 1:21]
        self.X1 = self.X1.to_numpy()

        self.c_result = None

        # build clusters using different algorithms
        if cluster == 0:
            self.c_result = self.kmeans(self.X1, k=4)
        elif cluster == 1:
            self.c_result = self.dbscan(self.X1, k=4)
        elif cluster == 2:
            self.c_result = self.meanshift(self.X1)
        elif cluster == 3:
            self.c_result = self.kprototype(self.kprotoDataCleaning(self.data), n=3)


        # calculate importacne for each cluster
        self.calculate_importance(self.c_result, self.kprotoDataCleaning(self.data))

        # save cluster label
        self.data[clusters[cluster]] = self.c_result

        # calculate effect score base on default/userinput weight
        weight = Map.map.featureWeight.iloc[:, 1].to_numpy()
        score = self.scoring_model(features=self.X1, u_weight=weight, score_min=0, score_max=5)
        self.data[clusters[4]] = score

    def scoring_model(self, features, u_weight, score_min=0, score_max=10):
        # print("used scoring weight: ", u_weight)
        e = sys.float_info.epsilon
        if u_weight is None:
            ini_weight = np.random.rand(features.shape[1])
        else:
            ini_weight = u_weight
        weight = ini_weight / ini_weight.sum()
        score = np.dot(features, weight.T)
        ini_score = np.dot(features, weight.T)
        score_scaled = (ini_score - ini_score.min()) / (ini_score.max() - ini_score.min() + e)
        score = np.round(score_scaled * (score_max - score_min) + score_min, 1)
        return score

    '''def scoring_model(self, features, weight, score_min=0, score_max=10, c_result=None):
        scaledWeight = weight.to_numpy()

        # calculate risk score according to the corresponding cluster's weight
        score = []
        for i in range(features.shape[0]):
            individualScore = np.dot(features[i], scaledWeight[:,c_result[i]].T)
            score.append(individualScore)
        score = np.array(score)

        # delete the score of the station that belongs to cluster -1
        negativeClusterIndex = []
        for i in range(features.shape[0]):
            if c_result[i] == -1:
                negativeClusterIndex.append(i)
        score = np.delete(score, negativeClusterIndex)

        # rescale score
        score = (((score - score.min()) / (score.max() - score.min())) * (score_max - score_min)).round(1)

        # re-insert the risk score as -1 for stations that belong to cluster -1
        for i in range(len(negativeClusterIndex)):
            score = np.insert(score, negativeClusterIndex[i], -1)
        return score'''

    def kmeans(self, features, k=4):
        model_Kmeans = KMeans(n_clusters=k)
        model_Kmeans.fit(features)
        clusters = model_Kmeans.predict(features)
        return clusters

    def dbscan(self, features, k=4):
        model_DBSCAN = DBSCAN(eps=k, min_samples=3)
        model_DBSCAN.fit(features)
        clusters = model_DBSCAN.labels_
        return clusters

    def meanshift(self, features):
        MS_data = features
        bandwidth = estimate_bandwidth(MS_data, quantile=0.2, n_samples=45)

        ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
        ms.fit(MS_data)
        labels = ms.labels_
        cluster_centers = ms.cluster_centers_

        labels_unique = np.unique(labels)
        n_clusters_ = len(labels_unique)
        return labels

    def hierarchy(self, features, num_of_clusters=7):
        AHC_data = features
        clustering = AgglomerativeClustering(linkage="single", n_clusters=num_of_clusters)
        clustering.fit(AHC_data)
        labels = clustering.labels_

        return labels

    # k-prototype: data cleaning and clustering

    def kprotoDataCleaning(self, data): # data: DataFrame
        stations = data.iloc[:, :23]
        cleaned_stations = stations.iloc[:, 1:21]
        cleaned_stations["Public_Transport"] = cleaned_stations["Public_Transport"].replace("train track",
                                                                                                      0).astype(int)
        cleaned_stations.loc[cleaned_stations.Public_Transport >= 2, "Public_Transport"] = 1
        cleaned_stations[["Fuel_Type_Diesel", "Fuel_Type_Petrol", "Fuel_Type_CNG", "Fuel_Type_LPG", "Shop_Open_24/7",
                          "Residential_Hotel_Area_R200", "Business_Area_R200", "Leisure_Area_R200",
                          "Industrial_Area_R200", "Public_Transport"]] = cleaned_stations[
            ["Fuel_Type_Diesel", "Fuel_Type_Petrol", "Fuel_Type_CNG", "Fuel_Type_LPG", "Shop_Open_24/7",
             "Residential_Hotel_Area_R200", "Business_Area_R200", "Leisure_Area_R200", "Industrial_Area_R200",
             "Public_Transport"]].astype(bool)

        return cleaned_stations

    def kprototype(self, data, n): # data: cleaned_stations
        # clustering
        kproto = KPrototypes(n_clusters=n)
        labels = kproto.fit_predict(data, categorical=[0,1,2,3,4,9,10,11,12,13])
        return labels

    # suggesting scoring weight

    def logistic_regression(self, clusters, features):
        model = LogisticRegression().fit(X=features.astype(int).to_numpy(), y=clusters.astype(int))
        return model.coef_

    def calculate_importance(self, clusters, features): # clusters: labels; features: cleaned_stations
        k = len(np.unique(clusters))
        weights = np.zeros((len(features.columns), k))
        for i in range(k):
            binary_cluster = (clusters == np.unique(clusters)[i]).astype(int)
            try:
                coeffs = self.logistic_regression(binary_cluster, features)
                weights[:, i] = (coeffs - np.min(coeffs)) / (np.max(coeffs) - np.min(coeffs))
            except:
                print("Regression failed.")

        # creating dataframe of weights
        colnames = [f"Cluster {i}" for i in range(1, k + 1)]
        rownames = features.columns
        weights = pd.DataFrame(weights, columns=colnames).set_index(rownames)
        weights = weights.abs()
        # weights = (weights / weights.sum())
        weights.to_excel(Map.clusterImportancePath)
        print("cluster importance updated")
        Map.map.updateImportance()
        return weights