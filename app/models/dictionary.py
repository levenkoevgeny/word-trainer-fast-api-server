from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Dictionary(Base):
    id = Column(Integer, primary_key=True, index=True)
    dictionary_name = Column(String, index=True)
    date_time_created = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="dictionaries")

    class Config:
        orm_mode = True


