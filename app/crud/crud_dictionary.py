from sqlalchemy.orm import Session

from typing import Any, Optional, List, Union, Dict

from app.models import Dictionary, User
from app.schemas import DictionaryCreate, DictionaryUpdate
from fastapi.encoders import jsonable_encoder


class CRUDDictionary:
    def get(self, db: Session, id: int) -> Optional[Dictionary]:
        return db.query(Dictionary).filter(Dictionary.id == id).first()

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Dictionary]:
        return db.query(Dictionary).offset(skip).limit(limit).all()

    def get_multi_by_owner(self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100) -> List[Dictionary]:
        return db.query(Dictionary).filter(Dictionary.owner_id == owner_id).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: DictionaryCreate) -> Dictionary:
        db_obj = Dictionary(
            dictionary_name=obj_in.dictionary_name,
            owner_id=obj_in.owner_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: Dictionary, obj_in: Union[DictionaryUpdate, Dict[str, Any]]
    ) -> Dictionary:
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

    def delete(self, db: Session, *, db_obj: Dictionary):
        db.delete(db_obj)
        db.commit()
        return db_obj


dictionary = CRUDDictionary()