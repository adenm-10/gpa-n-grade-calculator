import sys

from src.GradesTab import Grades_Tab
from src.FinalsTab import Finals_Tab
from src.CoursesTab import Courses_Tab

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

# Main Class for App to hold Tab Widget
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 1000, 200)
        self.setWindowTitle("GPA Calculator")
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.tab_widget = MyTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.show()

# Main Tabbing widget to allow for tab organization
class MyTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.tab_layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.courses_tab = Courses_Tab(self)
        self.grades_tab = Grades_Tab(self)
        self.finals_tab = Finals_Tab(self)

        self.tabs.addTab(self.courses_tab, "GPA")
        self.tabs.addTab(self.grades_tab, "Grades")
        self.tabs.addTab(self.finals_tab, "Final")

        self.tab_layout.addWidget(self.tabs)
        self.setLayout(self.tab_layout)

    def setup_grades_tab(self):
        return


if __name__ == '__main__':
    
    app = QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec_()) 