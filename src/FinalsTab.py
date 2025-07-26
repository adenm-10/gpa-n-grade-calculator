from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Class for Final Tab, child of Tab class in main.py
class Finals_Tab(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        # Grid layout for easy organziation and sizing
        self.grid = QGridLayout()

        # First row reserved for labeling inputs
        self.grid.addWidget(QLabel("Current Grade (%)"), 0, 0)
        self.grid.addWidget(QLabel("Final Weight (%)"), 0, 1)
        self.grid.addWidget(QLabel("Desired Grade (%)"), 0, 2)

        # Second row for providing input
        self.grid.addWidget(QLineEdit(), 1, 0)
        self.grid.addWidget(QLineEdit(), 1, 1)
        self.grid.addWidget(QLineEdit(), 1, 2)

        # Third row for outputting calculation
        self.display_text = QLabel(text="", parent=self)
        self.grid.addWidget(self.display_text, 2, 0, 1, 2)

        self.add_button = QPushButton(text="Calculate Needed Final", parent=self)
        self.add_button.clicked.connect(self.calculate_final)
        self.grid.addWidget(self.add_button, 2, 2, 1, 1)     

        self.setLayout(self.grid)   
    
    def calculate_final(self):
        cur_grade = self.grid.itemAtPosition(1, 0).widget().text()
        final_weight = self.grid.itemAtPosition(1, 1).widget().text()
        des_grade = self.grid.itemAtPosition(1, 2).widget().text()

        try:
            cur_grade = float(cur_grade) / 100
            final_weight = float(final_weight) / 100
            des_grade = float(des_grade) / 100
        except:
            self.display_text.setText("Invalid Input")
            return

        needed_grade = (des_grade - ((1-final_weight) * cur_grade))/(final_weight)

        self.display_text.setText("Needed Grade: " + str(round(needed_grade * 100, 3)))
