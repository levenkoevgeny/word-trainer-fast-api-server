from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Word])
def read_words(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve words.
    """
    words = crud.word.get_multi(db, skip=skip, limit=limit)
    return words


@router.get("/{word_id}", response_model=schemas.Word)
def get_by_id(
        *,
        db: Session = Depends(deps.get_db),
        word_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    word = crud.word.get(db, id=word_id)
    if not word:
        raise HTTPException(
            status_code=404,
            detail="The word with this word name does not exist in the system",
        )
    return word


@router.post("/", response_model=schemas.Word)
def create_word(
        *,
        db: Session = Depends(deps.get_db),
        word_in: schemas.WordCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new word.
    """

    word = crud.word.create(db, obj_in=word_in)
    return word


@router.put("/{word_id}", response_model=schemas.Word)
def update_word(
        *,
        db: Session = Depends(deps.get_db),
        word_id: int,
        word_in: schemas.WordUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    word = crud.word.get(db, id=word_id)
    if not word:
        raise HTTPException(
            status_code=404,
            detail="The word with this word name does not exist in the system",
        )
    word = crud.word.update(db, db_obj=word, obj_in=word_in)
    return word


@router.delete("/{word_id}", response_model=schemas.Word)
def delete_word(
        *,
        db: Session = Depends(deps.get_db),
        word_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
):
    word = crud.word.get(db, id=word_id)
    if not word:
        raise HTTPException(
            status_code=404,
            detail="The word with this word name does not exist in the system",
        )
    word = crud.word.delete(db, db_obj=word)
    return word