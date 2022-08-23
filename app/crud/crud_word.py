from sqlalchemy.orm import Session

from typing import Any, Optional, List, Union, Dict

from app.models import Word
from app.schemas import WordCreate, WordUpdate
from fastapi.encoders import jsonable_encoder


class CRUDWord:
    def get(self, db: Session, id: Any) -> Optional[Word]:
        return db.query(Word).filter(Word.id == id).first()

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Word]:
        return db.query(Word).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: WordCreate) -> Word:
        db_obj = Word(
            word_rus=obj_in.word_rus,
            word_eng=obj_in.word_eng,
            dictionary_id=obj_in.dictionary_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: Word, obj_in: Union[WordUpdate, Dict[str, Any]]
    ) -> Word:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, db_obj: Word):
        db.delete(db_obj)
        db.commit()
        return db_obj


word = CRUDWord()