## GPA and Grade Calculator GUI

A small, PyQt5-based GUI to calculate potential semester and career GPA, class grades, and needed final grades based off theoretical inputs. Also capable of parsing UCF unofficial transcript documents (myKnightsAudit) via the import transcript button. 

Dependencies:
 1. Python 3.9.13+
 2. PyQt5
 3. PyPDF2

To launch GUI:
.\venv\Scripts\activate
python3 main.py
deactivate

Import transcript button only works on UCF myKnightsAudit Documents

Courses Tab: Used to calculate semester and career gpa depending on inputted course weights and grades, and a loaded parsed transcrtipt. Can be used to look at theoretical GPAs.

Grades Tab: A broad tab application to look at theoretical course grades given all assignment categories, their weights, and their theorretical grades.

Finals Tab: Given percent weight of a final, current grade in a course with all other assignments submitted/graded, and a desired final grade for overall course, will output needed grade on final to achieve desired grade.

![image](https://github.com/adenm-10/gpa-n-grade-calculator/assets/61072840/9b078103-8c2a-4ce5-9ae2-b878e4e99053)

![image](https://github.com/adenm-10/gpa-n-grade-calculator/assets/61072840/7a6403f9-1cec-4f48-bd6f-1616b6b1e6ab)

![image](https://github.com/adenm-10/gpa-n-grade-calculator/assets/61072840/b2b9b0ff-2a68-41ea-ab95-d296850104aa)

