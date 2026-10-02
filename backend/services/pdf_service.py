import fitz # PyMuPDF
import os

def extract_text_from_pdf(file_path: str):
    """
    Extracts text page by page from a PDF file using PyMuPDF.
    Returns a list of dicts: [{'page': page_num, 'text': page_text}, ...]
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found at {file_path}")

    doc = fitz.open(file_path)
    pages_data = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        if text.strip():
            pages_data.append({
                "page": page_num + 1,
                "text": text.strip()
            })

    doc.close()
    return pages_data, len(doc)
