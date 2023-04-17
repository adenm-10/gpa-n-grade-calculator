import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class course:
    def __init__(self, code, name, credits, grade):
        self.code = code
        self.name = name
        self.credits = credits
        self.grade = grade

def display_gpa():
    a = 1

def window():
    app = QApplication([])
    w = QWidget()
    grid = QGridLayout(w)

    w.setGeometry(10, 10, 600, 400)
    w.setWindowTitle("GPA Calculator")

    grid.addWidget(QLabel(""), 0, 0)
    grid.addWidget(QLabel("Course Name"), 0, 1)
    grid.addWidget(QLabel("Credits"), 0, 2)
    grid.addWidget(QLabel("Grade"), 0, 3)

    for i in range(1, 6):
        combo = QComboBox()
        combo.addItems(["Grade", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"])

        cur_course = "Course " + str(i)
        grid.addWidget(QLabel(cur_course), i, 0)
        grid.addWidget(QLineEdit(), i, 1)
        grid.addWidget(QLineEdit(), i, 2)
        grid.addWidget(combo, i, 3)

    w.show()
    sys.exit(app.exec_())

    

def add_class():
    a = 1



def main():
    gpa_weights = {"A": 4, "A-": 3.75,
                   "B+": 3.25, "B": 3, "B-": 2.75,
                   "C+": 2.25, "C": 2, "C-": 1.75,
                   "D+": 1.25, "D": 1, "D-": 0.75,
                   "F": 0}
    
    window()

main()