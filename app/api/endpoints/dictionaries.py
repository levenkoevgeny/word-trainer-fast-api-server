from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Dictionary])
def read_dictionaries(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100
) -> Any:
    """
    Retrieve users.
    """
    dictionaries = crud.dictionary.get_multi(db, skip=skip, limit=limit)
    return dictionaries


@router.post("/", response_model=schemas.Dictionary)
def create_dictionary(
        *,
        db: Session = Depends(deps.get_db),
        dictionary_in: schemas.DictionaryCreate,
) -> Any:
    """
    Create new dictionary.
    """

    dictionary = crud.dictionary.create(db, obj_in=dictionary_in)
    return dictionary


@router.put("/{dictionary_id}", response_model=schemas.Dictionary)
def update_dictionary(
        *,
        db: Session = Depends(deps.get_db),
        dictionary_id: int,
        dictionary_in: schemas.DictionaryUpdate,
) -> Any:
    dictionary = crud.dictionary.get(db, id=dictionary_id)
    if not dictionary:
        raise HTTPException(
            status_code=404,
            detail="The dictionary with this dictionary name does not exist in the system",
        )
    dictionary = crud.dictionary.update(db, db_obj=dictionary, obj_in=dictionary_in)
    return dictionary
