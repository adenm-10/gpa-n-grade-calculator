from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Finals_Tab(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.grid = QGridLayout()

        self.grid.addWidget(QLabel("Current Grade"), 0, 0)
        self.grid.addWidget(QLabel("Grade Accounted For"), 0, 1)
        self.grid.addWidget(QLabel("Desired Grade"), 0, 2)

        self.grid.addWidget(QLineEdit(), 1, 0)
        self.grid.addWidget(QLineEdit(), 1, 1)
        self.grid.addWidget(QLineEdit(), 1, 2)

        self.display_text = QLabel(text="", parent=self)
        self.grid.addWidget(self.display_text, 2, 0, 1, 2)

        self.add_button = QPushButton(text="Calculate Needed Final", parent=self)
        self.add_button.clicked.connect(self.calculate_final)
        self.grid.addWidget(self.add_button, 2, 2, 1, 1)     

        self.setLayout(self.grid)   
    
    def calculate_final(self):
        cur_grade = self.grid.itemAtPosition(1, 0).widget().text()
        total_grade_points = self.grid.itemAtPosition(1, 1).widget().text()
        des_grade = self.grid.itemAtPosition(1, 2).widget().text()

        try:
            cur_grade = float(cur_grade) / 100
            total_grade_points = float(total_grade_points) / 100
            des_grade = float(des_grade) / 100
        except:
            self.display_text.setText("Invalid Input")

        needed_grade = (des_grade - (total_grade_points * cur_grade))/(1-total_grade_points)

        self.display_text.setText("Needed Grade: " + str(round(needed_grade * 100, 3)))
