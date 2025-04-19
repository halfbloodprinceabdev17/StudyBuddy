import fitz # PyMuPDF
import pytesseract
import re
from pdf2image import convert_from_bytes
import numpy as np
import cv2

def extract_mcqs_from_text(text):
    pattern = re.compile(
        r"(?P<question>.*?)(?:\n|^)"
        r"(A\..*?)(?:\n|$)"
        r"(B\..*?)(?:\n|$)"
        r"(C\..*?)(?:\n|$)"
        r"(D\..*?)(?:\n|$)"
        r"(?P<answer>[A-D])?",
        re.DOTALL
    )
    matches = pattern.findall(text)
    questions = []
    for match in matches:
        questions.append({
            "question": match[0].strip(),
            "options": [match[1].strip(), match[2].strip(), match[3].strip(), match[4].strip()],
            "answer": match[5].strip() if match[5] else None
        })
    return questions


def extract_mcqs_from_pdf(file_stream):
    doc = fitz.open(stream=file_stream.read(), filetype="pdf")
    text = "\n".join([page.get_text() for page in doc])

    mcqs = []
    # First regex pattern: numbered format
    pattern1 = re.compile(
        r"(\d+\.\s+.*?)\s+A\.\s+(.*?)\s+B\.\s+(.*?)\s+C\.\s+(.*?)\s+D\.\s+(.*?)\s+Answer:\s+([A-Da-d])",
        re.DOTALL
    )
    # Second regex pattern: Q1 style format
    pattern2 = re.compile(
        r"(Q\d+:\s+.*?)\s+A\.\s+(.*?)\s+B\.\s+(.*?)\s+C\.\s+(.*?)\s+D\.\s+(.*?)\s+Answer:\s+([A-Da-d])",
        re.DOTALL
    )

    for match in pattern1.findall(text) + pattern2.findall(text):
        question, a, b, c, d, answer = match
        mcqs.append({
            "question": question.strip(),
            "options": [
                f"A. {a.strip()}",
                f"B. {b.strip()}",
                f"C. {c.strip()}",
                f"D. {d.strip()}"
            ],
            "answer": answer.strip().upper()
        })

    return mcqs



def extract_mcqs_from_pdf2(file_stream):
    doc = fitz.open(stream=file_stream.read(), filetype="pdf")
    full_text = ""

    for page in doc:
        full_text += page.get_text()

    # Correct regex pattern (no unbalanced parentheses)
    pattern = re.compile(
        r"(\d+\.\s+.*?\?)\s+a\)\s+(.*?)\s+b\)\s+(.*?)\s+c\)\s+(.*?)\s+d\)\s+(.*?)\s+Answer:\s+([a-d])",
        re.DOTALL
    )

    mcqs = []
    for match in pattern.findall(full_text):
        question, a, b, c, d, answer = match
        mcqs.append({
            "question": question.strip(),
            "options": [
                f"a) {a.strip()}",
                f"b) {b.strip()}",
                f"c) {c.strip()}",
                f"d) {d.strip()}"
            ],
            "answer": answer.strip()
        })

    return mcqs