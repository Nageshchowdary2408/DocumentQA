import os
import uuid
import json
from fastapi import APIRouter, UploadFile, File, HTTPException
from config import UPLOAD_DIR
from services.pdf_service import extract_text_from_pdf
from services.chunk_service import chunk_pages
from services.embedding_service import generate_embeddings
from services.vector_service import store_chunks

router = APIRouter()
METADATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "documents_meta.json")

def load_documents_meta():
    if os.path.exists(METADATA_FILE):
        try:
            with open(METADATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_documents_meta(meta):
    with open(METADATA_FILE, "w") as f:
        json.dump(meta, f, indent=2)

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    document_id = str(uuid.uuid4())[:8]
    safe_filename = file.filename.replace(" ", "_")
    file_path = os.path.join(UPLOAD_DIR, f"{document_id}_{safe_filename}")

    try:
        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="Uploaded PDF file is empty.")

        with open(file_path, "wb") as f:
            f.write(contents)

        # Extract text & page count
        pages_data, total_pages = extract_text_from_pdf(file_path)
        if not pages_data:
            raise HTTPException(status_code=400, detail="No extractable text found in PDF (might be scanned).")

        # Chunk text
        chunks = chunk_pages(pages_data, document_id, file.filename)
        if not chunks:
            raise HTTPException(status_code=400, detail="Failed to create text chunks from PDF.")

        # Generate embeddings
        texts = [c["text"] for c in chunks]
        embeddings = generate_embeddings(texts)

        # Store in ChromaDB
        store_chunks(chunks, embeddings)

        # Save metadata
        meta = load_documents_meta()
        meta[document_id] = {
            "document_id": document_id,
            "filename": file.filename,
            "pages": total_pages,
            "file_path": file_path
        }
        save_documents_meta(meta)

        return {
            "success": True,
            "document_id": document_id,
            "filename": file.filename,
            "pages": total_pages,
            "message": "Document processed successfully"
        }
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))
