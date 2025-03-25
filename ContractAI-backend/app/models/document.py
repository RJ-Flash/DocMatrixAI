from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class Document(Base):
    """Document model for storing document metadata."""
    
    __tablename__ = "documents"
    
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False)
    file_size = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False, default="uploaded")
    original_path = Column(String(255), nullable=False)
    text_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    
    # Relationships (uncomment when implementing related models)
    # extractions = relationship("Extraction", back_populates="document", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"Document(id={self.id}, filename={self.filename}, status={self.status})"


class DocumentText(Base):
    """Model for storing the extracted text content."""
    
    __tablename__ = "document_texts"
    
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False)
    content = Column(Text, nullable=False)
    language = Column(String(10), nullable=True)
    extraction_method = Column(String(50), nullable=False, default="ocr")
    confidence_score = Column(Integer, nullable=True)  # 0-100 score for extraction quality
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    
    def __repr__(self):
        return f"DocumentText(document_id={self.document_id}, extraction_method={self.extraction_method})" 