from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.dictionary import DictionaryCreate
from app.tests.utils.utils import random_lower_string
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings


def create_random_dictionary(db: Session, *, owner_id: Optional[int] = None) -> models.Dictionary:
    dictionary_name = random_lower_string()
    dictionary_in = DictionaryCreate(dictionary_name=dictionary_name, owner_id=owner_id)
    return crud.dictionary.create(db=db, obj_in=dictionary_in)


