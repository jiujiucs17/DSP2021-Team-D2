# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView

import DetailView
import Map

displayedFeatureNames = ['Fuel Type (Diesel)', 'Fuel Type (Petrol)', 'Fuel Type (CNG)', 'Fuel Type (LPG)', 'Shop open for 24/7', 'Hospitals', 'Education Premises', 'Children Day Care', 'Elderly House', 'Residential Area', 'Business Area', 'Leisure Area', 'Industrial Area', 'Public Transport', 'Highways (A)', 'Highways (N)', 'Highways (S)', 'Hotels', 'Store, Restaurant, Gym, Cinema', 'Distance to Fire Station (min)']

class Ui_ExplainClusterViewWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(750, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 651, 591))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.weightTableWidget = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.weightTableWidget.setObjectName("weightTableWidget")
        self.weightTableWidget.setColumnCount(0)
        self.weightTableWidget.setRowCount(0)
        self.weightTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.horizontalLayout.addWidget(self.weightTableWidget)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.centralwidget.setLayout(self.gridLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 676, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.DBSCAN = False

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Importance of Features"))
        self.weightTableWidget.horizontalHeader().setVisible(False)
        # self.weightTableWidget.verticalHeader().setVisible(False)
        self.weightTableWidget.setVerticalHeaderLabels(displayedFeatureNames)


class ExplainClusterViewWindow(QMainWindow, Ui_ExplainClusterViewWindow):

    def __init__(self, parent=None, DBSCAN = False):
        super(ExplainClusterViewWindow, self).__init__(parent)
        self.setupUi(self)
        self.DBSCAN = DBSCAN
        self.updateTable(Map.map.clusterImportance)
        self.weightTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def updateTable(self, defaultWeights):
        self.setTableFormat(defaultWeights)
        featureColumnName = QTableWidgetItem("Feature Name")
        featureColumnName.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.weightTableWidget.setItem(0, 0, featureColumnName)

        # fill in feature names
        for i in range(defaultWeights.shape[0]):
            name = QTableWidgetItem(displayedFeatureNames[i])  # QTableWidgetItem(str(weights.iloc[i][0]))
            name.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.weightTableWidget.setItem(1 + i, 0, name)

        # fill in suggested weights and used weights for each clusters
        for i in range(defaultWeights.shape[1] - 1):
            colour = None
            if i + 1 > len(DetailView.colours) - 1:
                colour = DetailView.colours[(i + 1) % len(DetailView.colours)]
            else:
                colour = DetailView.colours[i + 1]
            if self.DBSCAN:
                if i == 0:
                    continue
                else:
                    clusterNumber = QTableWidgetItem("Group " + str(i) + " Importance")
            else:
                clusterNumber = QTableWidgetItem("Group " + str(i+1) + " Importance")
            clusterNumber.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            clusterNumber.setBackground(QtGui.QColor(colour[0], colour[1], colour[2]))
            self.weightTableWidget.setItem(0, i + 1, clusterNumber)

            for i2 in range(defaultWeights.shape[0]):
                suggestedWeight = QTableWidgetItem(str(round(defaultWeights.iloc[i2][i+1], 2)))
                suggestedWeight.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                suggestedWeight.setBackground(QtGui.QColor(colour[0], colour[1], colour[2]))
                self.weightTableWidget.setItem(i2+1, i + 1, suggestedWeight)


    def setTableFormat(self, weights):
        self.weightTableWidget.setRowCount(weights.shape[0] + 1)
        self.weightTableWidget.setColumnCount(weights.shape[1])