import PyPDF2
import csv

gpa_weights = {    "Grade": 0, "A": 4, "A-": 3.75,
                   "B+": 3.25, "B": 3, "B-": 2.75,
                   "C+": 2.25, "C": 2, "C-": 1.75,
                   "D+": 1.25, "D": 1, "D-": 0.75,
                   "F": 0, "S": 0}

def read_transcript():
    reader = PyPDF2.PdfReader('mka.pdf')
    courses = []
    text = []

    name = reader.pages[0].extract_text().split("\n")
    name = name[0]
    print("{" + name + "}")
    
    
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        
        idx = text.find("Unduplicated Semester Units")
        text = text[idx:len(text)]

        if idx == -1:
            continue

        text = text + reader.pages[i+1].extract_text()
        break

    idx = text.find("UPPER LEVEL")
    text = text[0:idx]

    text = text.split("\n")

    for i, string in enumerate(text):

        if (string[0:4] != "Fall") and (string[0:4] != "Sprg") and (string[0:4] != "Summ"):
            text[i] = 0
            continue

        if len(string) < 4:
            text[i] = 0
            continue

        if not string[-4].isnumeric():
            text[i] = string[0:-len(name)]
            continue

    for string in text:
        if string == 0:
            continue

        print(string)
        
        if string[-2:len(string)] == "IP":
            break

        code = string[10:19].strip()

        ucf = 0
        if string[-2:len(string)] == "EN":
            ucf = 1

        idx = string.find(".")
        credits = float(string[idx-1:idx+3])

        grade = string[idx-4:idx-2].strip()

        course = {'code': code, 'ucf': ucf, 'credits': credits, 'grade': grade}
        courses.append(course)

    credits = 0
    gpa = 0

    for course in courses:
        if course['grade'] == 'S':
            continue

        credits += course['credits']
        gpa += gpa_weights[course['grade']] * course['credits']

    gpa = gpa/credits
    courses.append({'code': 'GPA', 'ucf': '0', 'credits': credits, 'grade': gpa})

    field_names = ['code', 'ucf', 'credits', 'grade']

    with open("courses.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        writer.writerows(courses)

    return

read_transcript()