"""
System Setting ORM Model for dynamic runtime application configuration.
"""
from sqlalchemy import Column, Integer, String, Text, Boolean
from app.core.database import Base
from app.models.base import TimestampMixin

class SystemSetting(Base, TimestampMixin):
    __tablename__ = "system_settings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key = Column(String(100), unique=True, index=True, nullable=False)
    value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    value_type = Column(String(50), default="string", nullable=False) # string, integer, float, boolean, json
    is_editable = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<SystemSetting {self.key}={self.value}>"
