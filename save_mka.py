import PyPDF2

def read_transcript():
    reader = PyPDF2.PdfReader('mka.pdf')
    credits = 0
    gpa = 0
    
    for page in reader.pages:
        text = page.extract_text()
        
        idx = text.find("Unduplicated Semester Units")

        if (idx != -1):
            text = text[idx:idx+180]
            idx = text.find(".00 taken")
            credits = int(text[idx-3:idx-0])
            break

    for page in reader.pages:
        text = page.extract_text()
        
        idx = text.find("Overall/Cumulative Grade Point Average of")

        if (idx != -1):
            text = text[idx:idx+180]
            idx = text.find("GPA: ")
            gpa = float(text[idx+5:idx+10])
            break

    return credits, gpa

