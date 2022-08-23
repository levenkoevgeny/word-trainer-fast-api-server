from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class Dictionary(Base):
    id = Column(Integer, primary_key=True, index=True)
    dictionary_name = Column(String, index=True)
    date_time_created = Column(DateTime, default=datetime.utcnow())
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    owner = relationship("User", back_populates="dictionaries")
    words = relationship("Word", back_populates="dictionary", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return self.dictionary_name

    class Config:
        orm_mode = True


class Word(Base):
    id = Column(Integer, primary_key=True, index=True)
    word_rus = Column(String, index=True)
    word_eng = Column(String, index=True)
    date_time_created = Column(DateTime, default=datetime.utcnow())
    dictionary_id = Column(Integer, ForeignKey("dictionary.id"), nullable=False)
    dictionary = relationship("Dictionary", back_populates="words")

    def __repr__(self):
        return self.word_rus + ' ' + self.word_eng

    class Config:
        orm_mode = True