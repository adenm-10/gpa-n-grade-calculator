import csv
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Dictionary to convert selections into numbers
gpa_weights = {    "Grade": 0, "A": 4, "A-": 3.75,
                   "B+": 3.25, "B": 3, "B-": 2.75,
                   "C+": 2.25, "C": 2, "C-": 1.75,
                   "D+": 1.25, "D": 1, "D-": 0.75,
                   "F": 0, "S": 0}

# Class for the Courses Tab, is a child of the Tab class in main.py
class Courses_Tab(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        # Start with a multidimensional list of courses, with max 15
        self.cur_grades = [[0, 0, 0] for i in range(15)]
        self.tab_depth = 2

        # Selected grid layout for easy organization
        # All widgets in this tab are organizaed according to this grid
        self.grid = QGridLayout()

        # First row hosts multiple buttons
        self.add_button = QPushButton(text="Add Course", parent=self)
        self.add_button.clicked.connect(self.add_course)
        self.grid.addWidget(self.add_button, 0, 0, 1, 1)

        self.remove_button = QPushButton(text="Remove Course", parent=self)
        self.remove_button.clicked.connect(self.remove_course)
        self.grid.addWidget(self.remove_button, 0, 1, 1, 1)

        self.import_button = QPushButton(text="Save Courses", parent=self)
        self.import_button.clicked.connect(self.save_courses)
        self.grid.addWidget(self.import_button, 0, 2, 1, 1)

        # Second row hosts labels for each of the entry points
        self.grid.addWidget(QLabel("Course Code"), 1, 0)
        self.grid.addWidget(QLabel("Credits"), 1, 1)
        self.grid.addWidget(QLabel("Grade"), 1, 2)

        # Third row shows two boxes of text entry and a combo box, 
        # can be seen as prototype for all potential inputs on this tab
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

    # Allows user to save all courses currently in tab to be saved to csv generated from MKA parser
    # Requires upload_mka.py to be run first
    def save_courses(self):
        try:
            with open('MKA\courses.csv', 'r') as csvfile:
                courses = list(csv.DictReader(csvfile))
        except:
            return

        # Creates temporary dict to import from csv
        career = {} 
        career = dict(courses[-1])

        courses[-1]['code'] = self.grid.itemAtPosition(2, 0).widget().text()
        courses[-1]['ucf'] = 1
        courses[-1]['credits'] = self.grid.itemAtPosition(2, 1).widget().text()
        courses[-1]['grade'] = self.grid.itemAtPosition(2, 2).widget().currentText()

        # Append current courses to temp dict imported above
        for i in range(3, self.tab_depth + 1):
            course = {}

            course['code'] = self.grid.itemAtPosition(i, 0).widget().text()
            course['ucf'] = 1
            course['credits'] = self.grid.itemAtPosition(i, 1).widget().text()
            course['grade'] = self.grid.itemAtPosition(i, 2).widget().currentText()

            courses.append(course)

        career.append(courses)

        field_names = ['code', 'ucf', 'credits', 'grade']

        # Save off dict back to existing csv
        with open("MKA\courses.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = field_names)
            writer.writeheader()
            writer.writerows(courses)

    # Calculates what a students semester and career gpa would be with current inputs
    def display_grades(self):
        counter = 0
        credits = 0

        # Total up all credit hours and grades currently inputted
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

        # Try to improt current career grades
        try:
            with open('MKA\courses.csv', 'r') as csvfile:
                reader = list(csv.DictReader(csvfile))

            career = reader[-1]

            career_credits = int(float(career['credits']))
            career_gpa = float(career['grade'])
        except:
            career_credits = 0

        # Relabel Semester and Career GPA labels
        if credits == 0:
            self.semester_output_label.setText("Semester GPA: NA") 
        else:
            self.semester_output_label.setText("Semester GPA: " + str(round(counter/credits, 3)))

        if career_credits == 0:
            self.career_output_label.setText("Career GPA: NA") 
        else:
            self.career_output_label.setText("Career GPA: " + str(round((counter + (career_credits * career_gpa))/(credits + career_credits), 3)))
    
    # Add a new course row beneath existing, to a limit of 15
    def add_course(self):
        if self.tab_depth == 15:
            return

        # Delete the buttons and labels below current row
        self.grid.itemAtPosition(self.tab_depth + 1, 0).widget().deleteLater()
        self.grid.itemAtPosition(self.tab_depth + 1, 1).widget().deleteLater()
        self.grid.itemAtPosition(self.tab_depth + 1, 2).widget().deleteLater()
        self.grid.itemAtPosition(self.tab_depth + 2, 0).widget().deleteLater()

        QApplication.processEvents()

        self.tab_depth += 1

        # Add a new course row
        combo = QComboBox()
        combo.addItems(["Grade", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"])

        self.grid.addWidget(QLineEdit(), self.tab_depth, 0)
        self.grid.addWidget(QLineEdit(), self.tab_depth, 1)
        self.grid.addWidget(combo, self.tab_depth, 2)

        # Remake buttons and labels below courses
        self.gpa_button = QPushButton(text="Calculate GPA", parent=self)
        self.gpa_button.clicked.connect(lambda: self.display_grades())
        self.grid.addWidget(self.gpa_button, self.tab_depth + 1, 2, 1, 1)

        self.semester_output_label = QLabel(text="", parent=self)
        self.grid.addWidget(self.semester_output_label, self.tab_depth + 1, 0, 1, 2)

        self.career_output_label = QLabel(text="", parent=self)
        self.grid.addWidget(self.career_output_label, self.tab_depth + 2, 0, 1, 2)
    
    # Remove a course row, same process to adding coruses except delete instead of add last row
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
