from pydantic import BaseModel
from typing import Optional


class WordBase(BaseModel):
    word_rus: str
    word_eng: str
    dictionary_id: int


class WordCreate(WordBase):
    pass


class WordUpdate(WordBase):
    word_rus: Optional[str]
    word_eng: Optional[str]
    dictionary_id: Optional[int]


class WordInDb(WordBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Word(WordInDb):
    pass