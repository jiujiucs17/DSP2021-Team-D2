# -*- coding: utf-8 -*-
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QTableWidgetItem
import Clustering

colours = [(255, 255, 255), (242, 242, 242)]
# colours = [(150, 206, 180), (255, 238, 173), (255, 173, 96), (254, 236, 233), (254, 126, 109)]

class Ui_DetailViewWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(9, 10, 781, 541))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.tabWidget = QtWidgets.QTabWidget(self.gridLayoutWidget)
        self.tabWidget.setObjectName("tabWidget")

        # set table for view by group, table name: self.tableWidget
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.tab)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 771, 511))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableWidget = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.gridLayout_2.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.tab.setLayout(self.gridLayout_2)

        # set table for all station view, tabel name: self.tableWidget_2
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.tab_2)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 771, 511))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.gridLayoutWidget_3)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget_2.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.gridLayout_3.addWidget(self.tableWidget_2, 0, 0, 1, 1)
        self.tab_2.setLayout(self.gridLayout_3)

        self.tabWidget.addTab(self.tab_2, "")
        self.tabWidget.addTab(self.tab, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.centralwidget.setLayout(self.gridLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Clustering Details"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "View By Group"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "All Stations"))


class DetailViewWindow(QMainWindow, Ui_DetailViewWindow):
    def __init__(self, parent=None, cluster=int, data=pd.DataFrame):
        super(DetailViewWindow, self).__init__(parent)
        self.setupUi(self)

        self.cluster = Clustering.clusters[cluster]  # name of the cluster (str)
        self.data = data[['Petrol Station Name', self.cluster, "Effect_Score"]]  # name of station, cluster index, risk score (pd.datafram)
        self.grouped = self.data.groupby(self.cluster).count()  # data grouped by cluster (pd.dataframe.groupby)
        self.clusterNumber = self.grouped.shape[0]  # number of clusters under current algorithm (int)
        self.indexes = self.grouped.index.values  # indexes of clusters (ndarrat)
        self.biggestCluster = self.grouped["Effect_Score"].max()
        self.resultAscending = False

        # fill in the table for "view by group"
        self.tableWidget.setColumnCount(2*self.clusterNumber)
        self.tableWidget.setRowCount(2+self.biggestCluster)
        for i in range(self.clusterNumber):
            colour = None
            if i > len(colours) - 1:
                colour = colours[i % len(colours)]
            else:
                colour = colours[i]

            # if Noise data(datapoint to which not able to assign cluster) exist,
            # then change the first column name to Noise and start count from 1 for other clusters
            subdata = self.data[self.data[self.cluster] == self.indexes[i]].sort_values(by="Effect_Score",
                                                                                        ascending=self.resultAscending)
            if self.data[self.data[self.cluster] == self.indexes[0]].iloc[0, 2] == -1:
                if i == 0:
                    title = QTableWidgetItem("NOISE")
                else:
                    title = QTableWidgetItem("GROUP " + str(i) + " (Total: " + str(subdata.shape[0]) + ")")
            else:
                title = QTableWidgetItem("GROUP " + str(i + 1) + " (Total: " + str(subdata.shape[0]) + ")")
            stationName = QTableWidgetItem("Station Name")
            riskScore = QTableWidgetItem("Effect Score")

            title.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            stationName.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            riskScore.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            title.setBackground(QtGui.QColor(colour[0], colour[1], colour[2]))
            stationName.setBackground(QtGui.QColor(colour[0], colour[1], colour[2]))
            riskScore.setBackground(QtGui.QColor(colour[0], colour[1], colour[2]))

            self.tableWidget.setItem(0, i * 2, title)
            self.tableWidget.setItem(1, i * 2, stationName)
            self.tableWidget.setItem(1, i * 2 + 1, riskScore)
            self.tableWidget.setSpan(0, i * 2, 1, 2)

            for i2 in range(self.biggestCluster):
                if i2 < subdata.shape[0]:
                    name = QTableWidgetItem(str(subdata.iloc[i2, 0]))
                    rs = QTableWidgetItem(str(subdata.iloc[i2, 2]))
                else:
                    name = QTableWidgetItem("")
                    rs = QTableWidgetItem("")

                name.setBackground(QtGui.QColor(colour[0], colour[1], colour[2]))
                rs.setBackground(QtGui.QColor(colour[0], colour[1], colour[2]))

                self.tableWidget.setItem(i2+2, i * 2, name)
                self.tableWidget.setItem(i2+2, i*2+1, rs)

        # fill in the table for "all stations"
        self.tableWidget_2.setColumnCount(9)
        self.tableWidget_2.setRowCount(20)
        subdata = self.data.sort_values(by="Effect_Score", ascending=self.resultAscending)
        subdata = [subdata.iloc[:20], subdata.iloc[20:40], subdata.iloc[40:45]]
        self.tableWidget_2.setHorizontalHeaderLabels(["Station Name", "Group", "Effect Score", "Station Name", "Group", "Effect Score", "Station Name", "Group", "Effect Score"])
        for i in range(3):
            for i2 in range(subdata[i].shape[0]):
                name = QTableWidgetItem(str(subdata[i].iloc[i2, 0]))
                group = QTableWidgetItem(str(subdata[i].iloc[i2, 1] + 1))
                score = QTableWidgetItem(str(subdata[i].iloc[i2, 2]))

                name.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                group.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                score.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                name.setBackground(QtGui.QColor(255, 255, 255))  # white
                group.setBackground(QtGui.QColor(242, 242, 242))  # grey
                score.setBackground(QtGui.QColor(242, 242, 242))  # grey

                self.tableWidget_2.setItem(i2, i * 3, name)
                self.tableWidget_2.setItem(i2, i * 3 + 1, group)
                self.tableWidget_2.setItem(i2, i * 3 + 2, score)