## GPA and Grade Calculator GUI

A small, PyQt5-based GUI to calculate potential semester and career GPA, course grades, and required final exam grades based on theoretical inputs. It can also parse UCF unofficial transcript documents (myKnightsAudit) via the **Import Transcript** button.

### Dependencies

- Python 3.9  
- PyQt5  
- PyPDF2  

### Launch the GUI

```bash
# If you don't have Python 3.9
sudo apt update
sudo apt install python3.9 python3.9-venv python3.9-dev

# Virtual environment setup
python3.9 -m venv ./venv
source venv/bin/activate
pip install PyQt5
pip install PyPDF2

# System Launch
python3 main.py
````

> 📄 The **Import Transcript** feature only works with UCF myKnightsAudit PDF documents.

---

### Features

#### Courses Tab

Calculate semester and career GPA using course weights and grades. Can also use a parsed transcript for cumulative GPA calculation. Supports theoretical GPA projections.

#### Grades Tab

Enter assignment categories, their weights, and theoretical scores to calculate current or projected course grades.

#### Finals Tab

Given:

* Final exam weight (%),
* Current grade,
* Desired final course grade,

Calculates the required score on the final exam.

---

### 🖼️ Screenshots

![Courses Tab](https://github.com/adenm-10/gpa-n-grade-calculator/assets/61072840/9b078103-8c2a-4ce5-9ae2-b878e4e99053)

![Grades Tab](https://github.com/adenm-10/gpa-n-grade-calculator/assets/61072840/7a6403f9-1cec-4f48-bd6f-1616b6b1e6ab)

![Finals Tab](https://github.com/adenm-10/gpa-n-grade-calculator/assets/61072840/b2b9b0ff-2a68-41ea-ab95-d296850104aa)


