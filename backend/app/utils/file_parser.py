from fastapi import UploadFile
from docx import Document
import pdfplumber

class FileExtractionError(Exception):
    pass


def extract_text_from_file(file: UploadFile) -> str:
    filename = file.filename.lower()

    try:
        if filename.endswith(".txt"):
            content = file.file.read().decode("utf-8")
            return content.strip()

        elif filename.endswith(".pdf"):
            text = []
            with pdfplumber.open(file.file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
            return "\n".join(text).strip()

        elif filename.endswith(".docx"):
            doc = Document(file.file)
            return "\n".join(p.text for p in doc.paragraphs).strip()

        else:
            raise FileExtractionError("Unsupported file type")

    except Exception as e:
        raise FileExtractionError("Failed to extract text from file")
