import fitz
from docx import Document
import openpyxl

def parse_file(filepath):
    text = ""

    if filepath.endswith('.pdf'):
        text = parse_pdf(filepath)
    elif filepath.endswith('.docx'):
        text = parse_docx(filepath)
    elif filepath.endswith('.xlsx') or filepath.endswith('.xls'):
        text = parse_excel(filepath)
    elif filepath.endswith('.txt'):
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()

    return text[:8000]

def parse_pdf(filepath):
    text = ""
    doc = fitz.open(filepath)
    for page in doc:
        text += page.get_text()
    return text

def parse_docx(filepath):
    doc = Document(filepath)
    text = ""
    for para in doc.paragraphs:
        if para.text.strip():
            text += para.text + "\n"
    return text

def parse_excel(filepath):
    wb = openpyxl.load_workbook(filepath)
    text = ""
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        text += f"Sheet: {sheet_name}\n"
        for row in ws.iter_rows(values_only=True):
            row_text = " | ".join([str(c) for c in row if c is not None])
            if row_text.strip():
                text += row_text + "\n"
    return text