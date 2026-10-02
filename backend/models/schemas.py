from pydantic import BaseModel
from typing import List, Optional

class QuestionRequest(BaseModel):
    question: str
    document_id: Optional[str] = None

class SourceChunk(BaseModel):
    document_id: str
    filename: str
    page: int
    chunk: str

class AnswerResponse(BaseModel):
    success: bool
    answer: str
    sources: List[SourceChunk]

class DocumentInfo(BaseModel):
    document_id: str
    filename: str
    pages: int

class DocumentListResponse(BaseModel):
    documents: List[DocumentInfo]

class UploadResponse(BaseModel):
    success: bool
    document_id: str
    filename: str
    pages: int
    message: str
