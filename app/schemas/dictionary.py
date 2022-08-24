from pydantic import BaseModel
from typing import Optional, List, Any
from app.schemas.word import Word


class DictionaryBase(BaseModel):
    dictionary_name: str


class DictionaryCreate(DictionaryBase):
    owner_id: int


class DictionaryUpdate(DictionaryBase):
    pass


class DictionaryInDb(DictionaryBase):
    id: Optional[int] = None
    words: Optional[List[Word]]

    class Config:
        orm_mode = True


class Dictionary(DictionaryInDb):
    pass