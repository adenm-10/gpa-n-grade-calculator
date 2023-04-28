import sys
import csv

from save_mka import read_transcript
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

gpa_weights = {    "Grade": 0, "A": 4, "A-": 3.75,
                   "B+": 3.25, "B": 3, "B-": 2.75,
                   "C+": 2.25, "C": 2, "C-": 1.75,
                   "D+": 1.25, "D": 1, "D-": 0.75,
                   "F": 0, "S": 0}

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

class Grades_Tab(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.cur_grades = [[0, 0, 0] for i in range(20)]
        self.tab_depth = 2

        self.grid = QGridLayout()

        self.add_button = QPushButton(text="Add Field", parent=self)
        self.add_button.clicked.connect(self.add_course)
        self.grid.addWidget(self.add_button, 0, 0, 1, 1)

        self.remove_button = QPushButton(text="Remove Field", parent=self)
        self.remove_button.clicked.connect(self.remove_course)
        self.grid.addWidget(self.remove_button, 0, 1, 1, 1)

        self.grid.addWidget(QLabel("Field Name"), 1, 0)
        self.grid.addWidget(QLabel("Weight (%)"), 1, 1)
        self.grid.addWidget(QLabel("Current Grade (%)"), 1, 2)

        self.grid.addWidget(QLineEdit(), self.tab_depth, 0)
        self.grid.addWidget(QLineEdit(), self.tab_depth, 1)
        self.grid.addWidget(QLineEdit(), self.tab_depth, 2)

        self.gpa_button = QPushButton(text="Calculate Grade", parent=self)
        self.gpa_button.clicked.connect(self.display_grades)
        self.grid.addWidget(self.gpa_button, self.tab_depth + 1, 2, 1, 1)

        self.current_grade = QLabel(text="", parent=self)
        self.grid.addWidget(self.current_grade, self.tab_depth + 1, 0, 1, 2)

        self.grade_accounted_for = QLabel(text="", parent=self)
        self.grid.addWidget(self.grade_accounted_for, self.tab_depth + 2, 0, 1, 2)
        
        self.setLayout(self.grid)

    def display_grades(self):
        grade = 0
        percentage = 0

        for i in range(2, self.tab_depth + 1):
            self.cur_grades[i-1][0] = self.grid.itemAtPosition(i, 1).widget().text()
            self.cur_grades[i-1][1] = self.grid.itemAtPosition(i, 2).widget().text()

            try:
                self.cur_grades[i-1][0] = float(self.cur_grades[i-1][0])
                self.cur_grades[i-1][1] = float(self.cur_grades[i-1][1])
            except:
                continue

            grade += self.cur_grades[i-1][0] * (self.cur_grades[i-1][1] / 100)
            percentage += self.cur_grades[i-1][0]

        self.current_grade.setText("Current Grade: " + str(round(100 * (grade / percentage), 3)))
        self.grade_accounted_for.setText("Total Grade Accounted For: " + str(round(percentage, 3)))
    
    def add_course(self):
        if self.tab_depth == 21:
            return

        self.grid.itemAtPosition(self.tab_depth + 1, 0).widget().deleteLater()
        self.grid.itemAtPosition(self.tab_depth + 1, 1).widget().deleteLater()
        self.grid.itemAtPosition(self.tab_depth + 1, 2).widget().deleteLater()
        self.grid.itemAtPosition(self.tab_depth + 2, 0).widget().deleteLater()

        QApplication.processEvents()

        self.tab_depth += 1

        self.grid.addWidget(QLineEdit(), self.tab_depth, 0)
        self.grid.addWidget(QLineEdit(), self.tab_depth, 1)
        self.grid.addWidget(QLineEdit(), self.tab_depth, 2)

        self.gpa_button = QPushButton(text="Calculate Grade", parent=self)
        self.gpa_button.clicked.connect(self.display_grades)
        self.grid.addWidget(self.gpa_button, self.tab_depth + 1, 2, 1, 1)

        self.current_grade = QLabel(text="", parent=self)
        self.grid.addWidget(self.current_grade, self.tab_depth + 1, 0, 1, 2)

        self.grade_accounted_for = QLabel(text="", parent=self)
        self.grid.addWidget(self.grade_accounted_for, self.tab_depth + 2, 0, 1, 2)
    
    def remove_course(self):
        if self.tab_depth == 2:
            return

        self.grid.itemAtPosition(self.tab_depth, 0).widget().deleteLater()
        self.grid.itemAtPosition(self.tab_depth, 1).widget().deleteLater()
        self.grid.itemAtPosition(self.tab_depth, 2).widget().deleteLater()

        self.grid.itemAtPosition(self.tab_depth + 1, 0).widget().deleteLater()
        self.grid.itemAtPosition(self.tab_depth + 1, 1).widget().deleteLater()
        self.grid.itemAtPosition(self.tab_depth + 1, 2).widget().deleteLater()
        self.grid.itemAtPosition(self.tab_depth + 2, 0).widget().deleteLater()

        QApplication.processEvents()

        self.tab_depth -= 1

        self.gpa_button = QPushButton(text="Calculate Grade", parent=self)
        self.gpa_button.clicked.connect(self.display_grades)
        self.grid.addWidget(self.gpa_button, self.tab_depth + 1, 2, 1, 1)

        self.current_grade = QLabel(text="", parent=self)
        self.grid.addWidget(self.current_grade, self.tab_depth + 1, 0, 1, 2)

        self.grade_accounted_for = QLabel(text="", parent=self)
        self.grid.addWidget(self.grade_accounted_for, self.tab_depth + 2, 0, 1, 2)

class Courses_Tab(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.cur_grades = [[0, 0, 0] for i in range(6)]
        self.tab_depth = 2

        self.grid = QGridLayout()

        self.add_button = QPushButton(text="Add Course", parent=self)
        self.add_button.clicked.connect(self.add_course)
        self.grid.addWidget(self.add_button, 0, 0, 1, 1)

        self.remove_button = QPushButton(text="Remove Course", parent=self)
        self.remove_button.clicked.connect(self.remove_course)
        self.grid.addWidget(self.remove_button, 0, 1, 1, 1)

        self.import_button = QPushButton(text="Save Courses", parent=self)
        self.import_button.clicked.connect(self.save_courses)
        self.grid.addWidget(self.import_button, 0, 2, 1, 1)

        self.grid.addWidget(QLabel("Course Code"), 1, 0)
        self.grid.addWidget(QLabel("Credits"), 1, 1)
        self.grid.addWidget(QLabel("Grade"), 1, 2)

        combo = QComboBox()
        combo.addItems(["Grade", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"])

        self.grid.addWidget(QLineEdit(), self.tab_depth, 0)
        self.grid.addWidget(QLineEdit(), self.tab_depth, 1)
        self.grid.addWidget(combo, self.tab_depth, 2)

        self.gpa_button = QPushButton(text="Calculate GPA", parent=self)
        self.gpa_button.clicked.connect(self.display_grades)
        self.grid.addWidget(self.gpa_button, self.tab_depth + 1, 2, 1, 1)

        self.semester_output_label = QLabel(text="", parent=self)
        self.grid.addWidget(self.semester_output_label, self.tab_depth + 1, 0, 1, 2)

        self.career_output_label = QLabel(text="", parent=self)
        self.grid.addWidget(self.career_output_label, self.tab_depth + 2, 0, 1, 2)
        
        self.setLayout(self.grid)

    def save_courses(self):
        career = {}

        with open('MKA\courses.csv', 'r') as csvfile:
            courses = list(csv.DictReader(csvfile))

        career = dict(courses[-1])

        courses[-1]['code'] = self.grid.itemAtPosition(2, 0).widget().text()
        courses[-1]['ucf'] = 1
        courses[-1]['credits'] = self.grid.itemAtPosition(2, 1).widget().text()
        courses[-1]['grade'] = self.grid.itemAtPosition(2, 2).widget().currentText()

        for i in range(3, self.tab_depth + 1):
            course = {}

            course['code'] = self.grid.itemAtPosition(i, 0).widget().text()
            course['ucf'] = 1
            course['credits'] = self.grid.itemAtPosition(i, 1).widget().text()
            course['grade'] = self.grid.itemAtPosition(i, 2).widget().currentText()

            courses.append(course)

        courses.append(career)

        field_names = ['code', 'ucf', 'credits', 'grade']

        with open("MKA\courses.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = field_names)
            writer.writeheader()
            writer.writerows(courses)

    def display_grades(self):
        counter = 0
        credits = 0

        for i in range(2, self.tab_depth + 1):
            self.cur_grades[i-1][0] = self.grid.itemAtPosition(i, 0).widget().text()
            self.cur_grades[i-1][1] = self.grid.itemAtPosition(i, 1).widget().text()
            self.cur_grades[i-1][2] = self.grid.itemAtPosition(i, 2).widget().currentText()

            try:
                self.cur_grades[i-1][1] = int(self.cur_grades[i-1][1])
            except:
                continue

            counter += self.cur_grades[i-1][1] * gpa_weights[self.cur_grades[i-1][2]]
            credits += self.cur_grades[i-1][1]

        with open('courses.csv', 'r') as csvfile:
            reader = list(csv.DictReader(csvfile))

        career = reader[-1]

        career_credits = int(float(career['credits']))
        career_gpa = float(career['grade'])

        if credits == 0:
            self.semester_output_label.setText("Semester GPA: NA") 
        else:
            self.semester_output_label.setText("Semester GPA: " + str(round(counter/credits, 3)))

        self.career_output_label.setText("Career GPA: " + str(round((counter + (career_credits * career_gpa))/(credits + career_credits), 3)))
    
    def add_course(self):
        if self.tab_depth == 7:
            return

        self.grid.itemAtPosition(self.tab_depth + 1, 0).widget().deleteLater()
        self.grid.itemAtPosition(self.tab_depth + 1, 1).widget().deleteLater()
        self.grid.itemAtPosition(self.tab_depth + 1, 2).widget().deleteLater()
        self.grid.itemAtPosition(self.tab_depth + 2, 0).widget().deleteLater()

        QApplication.processEvents()

        self.tab_depth += 1

        combo = QComboBox()
        combo.addItems(["Grade", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"])

        self.grid.addWidget(QLineEdit(), self.tab_depth, 0)
        self.grid.addWidget(QLineEdit(), self.tab_depth, 1)
        self.grid.addWidget(combo, self.tab_depth, 2)

        self.gpa_button = QPushButton(text="Calculate GPA", parent=self)
        self.gpa_button.clicked.connect(lambda: self.display_grades())
        self.grid.addWidget(self.gpa_button, self.tab_depth + 1, 2, 1, 1)

        self.semester_output_label = QLabel(text="", parent=self)
        self.grid.addWidget(self.semester_output_label, self.tab_depth + 1, 0, 1, 2)

        self.career_output_label = QLabel(text="", parent=self)
        self.grid.addWidget(self.career_output_label, self.tab_depth + 2, 0, 1, 2)
    
    def remove_course(self):
        if self.tab_depth == 2:
            return

        self.grid.itemAtPosition(self.tab_depth, 0).widget().deleteLater()
        self.grid.itemAtPosition(self.tab_depth, 1).widget().deleteLater()
        self.grid.itemAtPosition(self.tab_depth, 2).widget().deleteLater()

        self.grid.itemAtPosition(self.tab_depth + 1, 0).widget().deleteLater()
        self.grid.itemAtPosition(self.tab_depth + 1, 1).widget().deleteLater()
        self.grid.itemAtPosition(self.tab_depth + 1, 2).widget().deleteLater()
        self.grid.itemAtPosition(self.tab_depth + 2, 0).widget().deleteLater()

        QApplication.processEvents()

        self.tab_depth -= 1

        self.gpa_button = QPushButton(text="Calculate GPA", parent=self)
        self.gpa_button.clicked.connect(self.display_grades)
        self.grid.addWidget(self.gpa_button, self.tab_depth + 1, 2, 1, 1)

        self.semester_output_label = QLabel(text="", parent=self)
        self.grid.addWidget(self.semester_output_label, self.tab_depth + 1, 0, 1, 2)

        self.career_output_label = QLabel(text="", parent=self)
        self.grid.addWidget(self.career_output_label, self.tab_depth + 2, 0, 1, 2)

def main():
    
    app = QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec_()) 

main()