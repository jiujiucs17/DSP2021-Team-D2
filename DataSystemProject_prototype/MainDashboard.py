# -*- coding: utf-8 -*-
import time

from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QHeaderView, QTableWidgetItem
import os
import pandas as pd
import Clustering
import DetailView
import ExplainClusterView
import GoogleAPI_by_TeamD2
import Map
import WeightEditor

rawDataFile = "raw_data/Input_template.xlsx"
updatedDataFile = "raw_data/Input_template_API.xlsx"

class Ui_MainDashboardWindow(object):
    def setupUi(self, MainWindow):
        copyData = pd.read_excel(rawDataFile)
        copyData.to_excel(updatedDataFile, index=False)

        self.map = Map.map(updatedDataFile)  # store the map object
        #self.map.buildClusteredMap(radius=1, cluster=0)
        self.map.map_amsterdam.save("MapOutput.html")
        mapPath = os.path.join(os.path.abspath('.'), "MapOutput.html")
        mapUrl = QtCore.QUrl.fromLocalFile(mapPath)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(6, 5, 851, 641))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")

        self.clusterApplyButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.clusterApplyButton.setObjectName("clusterApplyButton")
        self.clusterApplyButton.setMaximumSize(QtCore.QSize(135, 32))
        self.verticalLayout.addWidget(self.clusterApplyButton)

        self.adjustWeightButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.adjustWeightButton.setObjectName("adjustWeightButton")
        self.adjustWeightButton.setMaximumSize(QtCore.QSize(135, 32))
        self.verticalLayout.addWidget(self.adjustWeightButton)

        self.viewDetailButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.viewDetailButton.setObjectName("viewDetailButton")
        self.viewDetailButton.setMaximumSize(QtCore.QSize(135, 32))
        self.verticalLayout.addWidget(self.viewDetailButton)

        self.explanationButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.explanationButton.setObjectName("explanationButton")
        self.explanationButton.setMaximumSize(QtCore.QSize(135, 32))
        self.verticalLayout.addWidget(self.explanationButton)

        self.line = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)

        self.clusterLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.clusterLabel.setObjectName("clusterLabel")
        self.clusterLabel.setMaximumSize(QtCore.QSize(135, 21))
        self.verticalLayout.addWidget(self.clusterLabel)

        self.clusterComboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.clusterComboBox.setObjectName("clusterComboBox")
        self.clusterComboBox.setMaximumSize(QtCore.QSize(135, 32))
        self.verticalLayout.addWidget(self.clusterComboBox)

        self.line_2 = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.label.setMaximumSize(QtCore.QSize(69, 21))
        self.horizontalLayout_2.addWidget(self.label)

        self.radiusEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.radiusEdit.setMaximumSize(QtCore.QSize(50, 21))
        self.radiusEdit.setObjectName("radiusEdit")
        self.radiusEdit.setText("0.2")
        self.horizontalLayout_2.addWidget(self.radiusEdit)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.line_3 = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)

        self.updateLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.updateLabel.setObjectName("updateLabel")
        self.updateLabel.setMaximumSize(QtCore.QSize(135, 21))
        self.verticalLayout.addWidget(self.updateLabel)

        self.updateDataButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.updateDataButton.setObjectName("updateDataButton")
        self.updateDataButton.setMaximumSize(QtCore.QSize(135, 32))
        self.verticalLayout.addWidget(self.updateDataButton)

        self.line_4 = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout.addWidget(self.line_4)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.legendLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.legendLabel.setObjectName("legendLabel")
        self.legendLabel.setMaximumSize(QtCore.QSize(135, 21))
        self.legendLabel.setVisible(False)
        self.verticalLayout.addWidget(self.legendLabel)

        self.colorLegendWidget = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.colorLegendWidget.setObjectName("tableWidget")
        self.colorLegendWidget.setColumnCount(2)
        self.colorLegendWidget.setRowCount(0)
        self.colorLegendWidget.setMaximumSize(135, 999)
        self.colorLegendWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.colorLegendWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.colorLegendWidget.setHorizontalHeaderLabels(["Color", "Group"])
        # self.tableWidget.horizontalHeader().setVisible(False)
        self.colorLegendWidget.verticalHeader().setVisible(False)
        self.colorLegendWidget.setVisible(False)
        self.verticalLayout.addWidget(self.colorLegendWidget)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.mapWebEngineWidget = QtWebEngineWidgets.QWebEngineView()
        self.mapWebEngineWidget.setUrl(mapUrl)
        self.horizontalLayout.addWidget(self.mapWebEngineWidget)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.centralwidget.setLayout(self.gridLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Fire Effect Dashboard"))
        self.clusterApplyButton.setText(_translate("MainWindow", "Apply Clustering"))
        self.adjustWeightButton.setText(_translate("MainWindow", "Scoring Weight"))
        self.viewDetailButton.setText(_translate("MainWindow", "Cluster Results"))
        self.explanationButton.setText(_translate("MainWindow", "Cluster Explained"))
        self.updateDataButton.setText(_translate("MainWindow", "Update Data"))
        self.clusterLabel.setText(_translate("MainWindow", " Choose Algorithm:"))
        self.updateLabel.setText(_translate("MainWindow", " Google Map API:"))
        self.legendLabel.setText(_translate("MainWindow", " Color Legend:"))
        self.clusterComboBox.addItems(Clustering.clusters[:-1])
        self.label.setText(_translate("MainWindow", " Radius KM"))
        self.viewDetailButton.setEnabled(False)
        self.explanationButton.setEnabled(False)

class MainDashboardWindow(QMainWindow, Ui_MainDashboardWindow):
    clusterIndex = []
    rainbow = [
        (56,170,221), (87,87,87), (144,176,38), (208,81,184),
        (246,151,48), (114,130,36), (187,249,112), (0,103,163),
        (138,218,255), (91,57,107), (67,105,120), (162,162,162)]
    def __init__(self, parent=None):
        super(MainDashboardWindow, self).__init__(parent)
        self.setupUi(self)
        self.clusterApplyButton.clicked.connect(self.clusterApplyButtonClicked)
        self.adjustWeightButton.clicked.connect(self.weightEditButtonClicked)
        self.viewDetailButton.clicked.connect(self.viewDetailButtonClicked)
        self.updateDataButton.clicked.connect(self.updateDataButtonClicked)
        self.explanationButton.clicked.connect(self.explanationButtonClicked)
        # self.clusterComboBox.currentIndexChanged.connect(self.clusterApplyButtonClicked)
        # self.radiusEdit.textChanged.connect(self.clusterApplyButtonClicked)

        self.explainClusterWindow = None
        self.detailViewWindow = None
        self.weightEditWindow = None
        self.msgBox = None

    def clusterApplyButtonClicked(self):
        if not self.viewDetailButton.isEnabled():
            self.viewDetailButton.setEnabled(True)
            self.explanationButton.setEnabled(True)

        if self.radiusEdit.text() == "":
            self.radiusEdit.setText("0.2")
        cluster_number = self.clusterComboBox.currentIndex()
        cluster_radius = float(self.radiusEdit.text())

        print("cluster apply button clicked with index: " + str(cluster_number) + " radius: " + str(cluster_radius))

        self.clearWindows()

        self.map.buildClusteredMap(radius=cluster_radius, cluster=cluster_number)
        self.map.map_amsterdam.save("MapOutput.html")
        mapPath = os.path.join(os.path.abspath('.'), "MapOutput.html")
        mapUrl = QtCore.QUrl.fromLocalFile(mapPath)
        self.mapWebEngineWidget.setUrl(mapUrl)

        self.colorLegendWidget.setVisible(True)
        self.legendLabel.setVisible(True)
        print(MainDashboardWindow.clusterIndex)
        # update the color legend
        self.colorLegendWidget.setRowCount(MainDashboardWindow.clusterIndex.shape[0])
        for i in range(MainDashboardWindow.clusterIndex.shape[0]):
            rgb = MainDashboardWindow.rainbow[MainDashboardWindow.clusterIndex[i]]
            color = QTableWidgetItem("")
            group = QTableWidgetItem(str(MainDashboardWindow.clusterIndex[i] + 1))
            group.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            color.setBackground(QtGui.QColor(rgb[0], rgb[1], rgb[2]))
            self.colorLegendWidget.setItem(i, 0, color)
            self.colorLegendWidget.setItem(i, 1, group)

    def weightEditButtonClicked(self):
            print("weight edit button clicked")
            self.weightEditWindow = WeightEditor.WeightEditWindow()
            self.weightEditWindow.show()

    def explanationButtonClicked(self):
        print("view explanation button clicked")
        self.clearWindows()
        if self.clusterComboBox.currentIndex() == 1:
            dbscan = True
        else:
            dbscan = False
        self.explainClusterWindow = ExplainClusterView.ExplainClusterViewWindow(DBSCAN=dbscan)
        self.explainClusterWindow.show()

    def viewDetailButtonClicked(self):
        print("view cluster result button clicked")
        self.clearWindows()
        self.detailViewWindow = DetailView.DetailViewWindow(cluster=self.clusterComboBox.currentIndex(),
                                                            data=self.map.data)
        self.detailViewWindow.show()

    def updateDataButtonClicked(self):
        print("update data button clicked")
        self.clearWindows()
        if self.radiusEdit.text() == "":
            self.radiusEdit.setText("1")
        cluster_radius = float(self.radiusEdit.text())
        msgBox = QMessageBox.information(self, "Update Data", "This might take a while, click on OK to proceed.", QMessageBox.Ok)
        
        ########################################################
        ##           The google api is disabled now           ##  
        ## To enable it, uncomment the following line of code ##
        ########################################################
        
        # GoogleAPI_by_TeamD2.Update_Dataset(updatedDataFile, radius=cluster_radius * 1000)
        
        
        QMessageBox.information(self, "Update Data", "Complete!")
        self.map.updateData(updatedDataFile)
        self.map.showStationWithoutCLustering()

        self.map.map_amsterdam.save("MapOutput.html")  # save the map as html
        mapPath = os.path.join(os.path.abspath('.'), "MapOutput.html")  # get the path of the html file
        mapUrl = QtCore.QUrl.fromLocalFile(mapPath)  # get the url of the html file
        self.mapWebEngineWidget.setUrl(mapUrl)

        if self.viewDetailButton.isEnabled():
            self.viewDetailButton.setEnabled(False)
            self.explanationButton.setEnabled(False)
        if self.colorLegendWidget.isVisible():
            self.colorLegendWidget.setVisible(False)
            self.legendLabel.setVisible(False)

        #self.clusterApplyButtonClicked()

    def comboBoxChanged(self):
        self.clearWindows()

    def clearWindows(self):
        if self.detailViewWindow is not None:
            self.detailViewWindow.close()
            self.detailViewWindow = None

        if self.weightEditWindow is not None:
            self.weightEditWindow.close()
            self.weightEditWindow = None

        if self.explainClusterWindow is not None:
            self.explainClusterWindow.close()
            self.explainClusterWindow = None
