from sqlalchemy import Boolean, Column, Integer, String

from app.db.db import Base


class Misclassification(Base):
    __tablename__ = "misclassifications"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    label = Column(Boolean)
