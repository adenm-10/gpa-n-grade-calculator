import sys

from save_mka import read_transcript
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 200)
        self.setWindowTitle("GPA Calculator")

        self.tab_widget = MyTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.show()


    
class MyTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.courses_tab = QWidget()
        self.grades_tab = QWidget()

        self.tabs.addTab(self.courses_tab, "GPA")
        self.tabs.addTab(self.grades_tab, "Grades")

        self.setup_courses_tab()
        self.setup_grades_tab()

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def setup_grades_tab(self): 
        return

    def setup_courses_tab(self):
        self.cur_grades = [[0, 0, 0] for i in range(5)]

        self.courses_tab.grid = QGridLayout(self)

        self.courses_tab.grid.addWidget(QLabel("Course Name"), 0, 0)
        self.courses_tab.grid.addWidget(QLabel("Credits"), 0, 1)
        self.courses_tab.grid.addWidget(QLabel("Grade"), 0, 2)

        for i in range(1, 6):
            combo = QComboBox()
            combo.addItems(["Grade", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"])

            self.courses_tab.grid.addWidget(QLineEdit(), i, 0)
            self.courses_tab.grid.addWidget(QLineEdit(), i, 1)
            self.courses_tab.grid.addWidget(combo, i, 2)

        self.button = QPushButton(text="Calculate GPA", parent=self)
        self.button.clicked.connect(lambda: self.display_grades())
        self.courses_tab.grid.addWidget(self.button, 7, 2, 1, 1)

        self.semester_output_label = QLabel(text="", parent=self)
        self.courses_tab.grid.addWidget(self.semester_output_label, 7, 0, 1, 2)

        self.career_output_label = QLabel(text="", parent=self)
        self.courses_tab.grid.addWidget(self.career_output_label, 8, 0, 1, 2)
        
        self.courses_tab.setLayout(self.courses_tab.grid)
    
    def display_grades(self):
        counter = 0
        credits = 0

        for i in range(1, 6):
            self.cur_grades[i-1][0] = self.courses_tab.grid.itemAtPosition(i, 0).widget().text()
            self.cur_grades[i-1][1] = self.courses_tab.grid.itemAtPosition(i, 1).widget().text()
            self.cur_grades[i-1][2] = self.courses_tab.grid.itemAtPosition(i, 2).widget().currentText()

            try:
                self.cur_grades[i-1][1] = int(self.cur_grades[i-1][1])
            except:
                continue

            counter += self.cur_grades[i-1][1] * gpa_weights[self.cur_grades[i-1][2]]
            credits += self.cur_grades[i-1][1]

        self.semester_output_label.setText("Semester GPA: " + str(round(counter/credits, 3)))

        career_credits, career_gpa = read_transcript()
        self.career_output_label.setText("Career GPA: " + str(round((counter + (career_credits * career_gpa))/(credits + career_credits), 3)))

        return 



def main():
    
    app = QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec_()) 

main()