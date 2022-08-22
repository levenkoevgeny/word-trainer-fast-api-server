from pydantic import BaseModel
from typing import Optional


class DictionaryBase(BaseModel):
    dictionary_name: str


class DictionaryCreate(DictionaryBase):
    owner_id: int


class DictionaryUpdate(DictionaryBase):
    pass


class DictionaryInDb(DictionaryBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Dictionary(DictionaryInDb):
    pass