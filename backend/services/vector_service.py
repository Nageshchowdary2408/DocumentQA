import chromadb
from config import CHROMA_DIR, TOP_K

chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chroma_client.get_or_create_collection(name="document_chunks")

def store_chunks(chunks: list[dict], embeddings: list[list[float]]):
    """Stores chunks, embeddings, and metadata in ChromaDB."""
    ids = [c["chunk_id"] for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [{
        "document_id": c["document_id"],
        "filename": c["filename"],
        "page": int(c["page"]),
        "chunk_index": int(c["chunk_index"])
    } for c in chunks]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )

def search_similar_chunks(query_embedding: list[float], top_k: int = TOP_K, document_id: str = None) -> list[dict]:
    """Performs similarity search in ChromaDB, optionally filtering by document_id."""
    where_filter = {"document_id": document_id} if document_id else None

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where_filter
    )

    matched_chunks = []
    if results and results["documents"] and results["documents"][0]:
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        for doc, meta in zip(docs, metas):
            matched_chunks.append({
                "document_id": meta.get("document_id"),
                "filename": meta.get("filename"),
                "page": meta.get("page"),
                "chunk": doc
            })

    return matched_chunks

def delete_document_vectors(document_id: str):
    """Deletes all vector records associated with a document_id."""
    try:
        collection.delete(where={"document_id": document_id})
    except Exception as e:
        print(f"Error deleting vectors for {document_id}: {e}")
