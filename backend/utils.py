from pypdf import PdfReader
import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  
    text = text.strip()
    return text

def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


    
