import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class course:
    def __init__(self, code, name, credits, grade):
        self.code = code
        self.name = name
        self.credits = credits
        self.grade = grade

gpa_weights = {    "Grade": 0, "A": 4, "A-": 3.75,
                   "B+": 3.25, "B": 3, "B-": 2.75,
                   "C+": 2.25, "C": 2, "C-": 1.75,
                   "D+": 1.25, "D": 1, "D-": 0.75,
                   "F": 0}

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.cur_grades = [[0, 0, 0] for i in range(5)]

        self.grid = QGridLayout(self)

        self.setGeometry(10, 10, 400, 200)
        self.setWindowTitle("GPA Calculator")

        self.grid.addWidget(QLabel(""), 0, 0)
        self.grid.addWidget(QLabel("Course Name"), 0, 1)
        self.grid.addWidget(QLabel("Credits"), 0, 2)
        self.grid.addWidget(QLabel("Grade"), 0, 3)

        for i in range(1, 6):
            combo = QComboBox()
            combo.addItems(["Grade", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"])

            cur_course = "Course " + str(i)
            self.grid.addWidget(QLabel(cur_course), i, 0)
            self.grid.addWidget(QLineEdit(), i, 1)
            self.grid.addWidget(QLineEdit(), i, 2)
            self.grid.addWidget(combo, i, 3)

        self.button = QPushButton(text="Calculate GPA", parent=self)
        self.button.clicked.connect(self.display_grades)
        self.grid.addWidget(self.button, 7, 0, 1, 2)

        self.label = QLabel(text="")
        self.grid.addWidget(self.button, 7, 2, 1, 2)
    
    def display_grades(self):
        counter = 0

        for i in range(1,5):
            self.cur_grades[i][0] = self.grid.itemAtPosition(i, 1).widget().text()
            self.cur_grades[i][1] = self.grid.itemAtPosition(i, 2).widget().text()
            self.cur_grades[i][2] = self.grid.itemAtPosition(i, 3).widget().currentText()

            try:
                counter += int(self.cur_grades[i][0]) * gpa_weights[self.cur_grades[i][0]]
            except:
                continue
        

        self.label.setText("Your Semster GPA will be: " + str(counter))

        return 

def add_course():
    a = 1

def main():
    
    app = QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec_()) 

main()