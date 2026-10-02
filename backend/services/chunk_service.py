import re
from config import CHUNK_SIZE, CHUNK_OVERLAP

def clean_text(text: str) -> str:
    """Cleans extracted PDF text by removing extra whitespaces and weird characters."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_pages(pages_data, document_id: str, filename: str, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    """
    Splits page texts into chunks with configurable chunk_size and chunk_overlap.
    Returns a list of chunk dictionaries with metadata.
    """
    chunks = []
    chunk_counter = 0

    for page_info in pages_data:
        page_num = page_info["page"]
        text = clean_text(page_info["text"])

        if not text:
            continue

        start = 0
        text_length = len(text)

        while start < text_length:
            end = min(start + chunk_size, text_length)
            chunk_text = text[start:end]

            chunks.append({
                "chunk_id": f"{document_id}_p{page_num}_c{chunk_counter}",
                "document_id": document_id,
                "filename": filename,
                "page": page_num,
                "chunk_index": chunk_counter,
                "text": chunk_text
            })

            chunk_counter += 1
            if end == text_length:
                break
            start += (chunk_size - chunk_overlap)

    return chunks
