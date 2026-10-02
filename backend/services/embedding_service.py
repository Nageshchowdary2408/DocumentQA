from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL_NAME

# Load lightweight embedding model suitable for student projects
print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}...")
model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Generates vector embeddings for a list of text strings."""
    embeddings = model.encode(texts, show_progress_bar=False)
    return embeddings.tolist()

def generate_single_embedding(text: str) -> list[float]:
    """Generates vector embedding for a single text string."""
    embedding = model.encode(text, show_progress_bar=False)
    return embedding.tolist()
