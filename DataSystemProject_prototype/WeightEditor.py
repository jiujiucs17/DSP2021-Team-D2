# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView

import DetailView
import Map

displayedFeatureNames = ['Fuel Type (Diesel)', 'Fuel Type (Petrol)', 'Fuel Type (CNG)', 'Fuel Type (LPG)', 'Shop open for 24/7', 'Hospitals', 'Education Premises', 'Children Day Care', 'Elderly House', 'Residential Area', 'Business Area', 'Leisure Area', 'Industrial Area', 'Public Transport', 'Highways (A)', 'Highways (N)', 'Highways (S)', 'Hotels', 'Store, Restaurant, Gym, Cinema', 'Distance to Fire Station (min)']

class Ui_WeightEditWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 700)
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
        self.horizontalLayout.addWidget(self.weightTableWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.saveButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setMinimumSize(QtCore.QSize(0, 0))
        self.saveButton.setObjectName("saveButton")
        self.verticalLayout.addWidget(self.saveButton)
        self.cancelButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.cancelButton.setObjectName("cancelButton")
        self.verticalLayout.addWidget(self.cancelButton)
        self.resetButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.resetButton.setObjectName("resetButton")
        self.verticalLayout.addWidget(self.resetButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Weight Editor"))
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.cancelButton.setText(_translate("MainWindow", "Cancel"))
        self.resetButton.setText(_translate("MainWindow", "Reset"))
        # self.weightTableWidget.horizontalHeader().setVisible(False)
        # self.weightTableWidget.verticalHeader().setVisible(False)


class WeightEditWindow(QMainWindow, Ui_WeightEditWindow):

    def __init__(self, parent=None):
        super(WeightEditWindow, self).__init__(parent)
        self.setupUi(self)

        self.updateTable(Map.map.defaultWeight, Map.map.featureWeight)
        self.weightTableWidget.setHorizontalHeaderLabels(["Feature Name", "Default Weight", "Used Weight"])

        self.saveButton.clicked.connect(self.applyButtonClicked)
        self.cancelButton.clicked.connect(self.cancelButtonClicked)
        self.resetButton.clicked.connect(self.resetButtonClicked)
        self.weightTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def applyButtonClicked(self): # need change (save weight and calculate new scores)
        print("save button clicked")
        for i in range(Map.map.featureWeight.shape[0]):
            Map.map.featureWeight.iloc[i, 1] = float(self.weightTableWidget.item(i, 2).text())
        # print("saved weight: \n", Map.map.featureWeight.iloc[:, 1])
        self.close()

    def cancelButtonClicked(self):
        print("cancel button clicked")
        self.close()

    def resetButtonClicked(self):
        print("reset button clicked")
        self.updateTable(Map.map.defaultWeight, Map.map.defaultWeight)

    def updateTable(self, defaultWeights, featureWeights):
        self.setTableFormat(defaultWeights)

        for i in range(defaultWeights.shape[0]):
            featureName = QTableWidgetItem(displayedFeatureNames[i])
            defaultWeight = QTableWidgetItem(str(round(defaultWeights.iloc[i, 1], 4)))
            usedWeight = QTableWidgetItem(str(round(featureWeights.iloc[i, 1], 4)))

            featureName.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            defaultWeight.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            usedWeight.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            self.weightTableWidget.setItem(i, 0, featureName)
            self.weightTableWidget.setItem(i, 1, defaultWeight)
            self.weightTableWidget.setItem(i, 2, usedWeight)

    def setTableFormat(self, weights):
        self.weightTableWidget.setRowCount(weights.shape[0])
        self.weightTableWidget.setColumnCount(weights.shape[1] + 1)