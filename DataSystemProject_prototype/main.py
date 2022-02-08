import sys
import MainDashboard
import DetailView
import WeightEditor
import Map
import Clustering
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    mainWindow = MainDashboard.MainDashboardWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()



