from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Dictionary])
def read_dictionaries(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        dictionary_name: str = '',
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    print(dictionary_name)
    """
    Retrieve dictionaries.
    """

    if crud.user.is_superuser(current_user):
        dictionaries = crud.dictionary.get_multi(db, skip=skip, limit=limit, dictionary_name=dictionary_name)
    else:
        dictionaries = crud.dictionary.get_multi_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit,
                                                          dictionary_name=dictionary_name)
    return dictionaries


@router.get("/{dictionary_id}", response_model=schemas.Dictionary)
def get_by_id(
        *,
        db: Session = Depends(deps.get_db),
        dictionary_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    dictionary = crud.dictionary.get(db, id=dictionary_id)
    if not dictionary:
        raise HTTPException(
            status_code=404,
            detail="The dictionary with this dictionary name does not exist in the system",
        )
    return dictionary


@router.post("/", response_model=schemas.Dictionary)
def create_dictionary(
        *,
        db: Session = Depends(deps.get_db),
        dictionary_in: schemas.DictionaryCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
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
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    dictionary = crud.dictionary.get(db, id=dictionary_id)
    if not dictionary:
        raise HTTPException(
            status_code=404,
            detail="The dictionary with this dictionary name does not exist in the system",
        )
    dictionary = crud.dictionary.update(db, db_obj=dictionary, obj_in=dictionary_in)
    return dictionary


@router.delete("/{dictionary_id}", response_model=schemas.Dictionary)
def delete_dictionary(
        *,
        db: Session = Depends(deps.get_db),
        dictionary_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
):
    dictionary = crud.dictionary.get(db, id=dictionary_id)
    if not dictionary:
        raise HTTPException(
            status_code=404,
            detail="The dictionary with this dictionary name does not exist in the system",
        )
    dictionary = crud.dictionary.delete(db, db_obj=dictionary)
    return dictionary
