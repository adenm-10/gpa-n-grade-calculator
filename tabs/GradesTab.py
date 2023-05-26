from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Class for the Grades Tab, is a child of the Tab class in main.py
# Extremely similar to Courses tab, except with less buttons and no career implementation
class Grades_Tab(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.cur_grades = [[0, 0, 0] for i in range(21)]
        self.tab_depth = 2

        # Grid layout is reused to row shifting 
        self.grid = QGridLayout()

        # First row reserved for adding and removing grade rows below
        self.add_button = QPushButton(text="Add Field", parent=self)
        self.add_button.clicked.connect(self.add_grade)
        self.grid.addWidget(self.add_button, 0, 0, 1, 1)

        self.remove_button = QPushButton(text="Remove Field", parent=self)
        self.remove_button.clicked.connect(self.remove_grade)
        self.grid.addWidget(self.remove_button, 0, 1, 1, 1)

        # Row two reserved for labels to denote inputs
        self.grid.addWidget(QLabel("Field Name"), 1, 0)
        self.grid.addWidget(QLabel("Weight (%)"), 1, 1)
        self.grid.addWidget(QLabel("Current Grade (%)"), 1, 2)

        # Prototype for a grade row, three lineedit inputs
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

    # Calculate current overall grade, and display how much of the class is accounted for
    def display_grades(self):
        grade = 0
        percentage = 0

        # Take input from all existing rows
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

        # Output Calculations
        try:
            self.current_grade.setText("Current Grade: " + str(round(100 * (grade / percentage), 3)))
        except:
            self.current_grade.setText("Current Grade: N/A")

        try:
            self.grade_accounted_for.setText("Total Grade Accounted For: " + str(round(percentage, 3)))
        except:
            self.grade_accounted_for.setText("Total Grade Accounted For: N/A")

    # Exact same as add_course from CoursesTab.py
    def add_grade(self):
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
    
    # Exact same as remove_course from CoursesTab.py
    def remove_grade(self):
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
