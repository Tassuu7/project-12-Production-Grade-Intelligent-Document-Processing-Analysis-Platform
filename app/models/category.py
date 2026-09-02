"""
Document Category ORM Model for taxonomy and classification labels.
"""
from sqlalchemy import Column, Integer, String, Text, Boolean
from app.core.database import Base
from app.models.base import TimestampMixin

class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    keywords = Column(Text, nullable=True)  # JSON array of category keywords
    is_system = Column(Boolean, default=False, nullable=False)
    color_code = Column(String(20), default="#2563eb", nullable=False)

    def __repr__(self):
        return f"<Category id={self.id} name={self.name}>"
