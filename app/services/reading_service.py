from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.reading import ReadingItemModel
from app.schemas.reading import (
    ReadingItem,
    ReadingItemCreate,
    ReadingItemUpdate,
    Status,
)


def create_item(db: Session, payload: ReadingItemCreate) -> ReadingItem:
    db_item = ReadingItemModel(
        title=payload.title,
        url=str(payload.url) if payload.url else None,
        tags=payload.tags,
        priority=payload.priority,
        status=Status.todo,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return ReadingItem(
        id=db_item.id,
        title=db_item.title,
        url=db_item.url,
        tags=db_item.tags or [],
        priority=db_item.priority,
        status=db_item.status,
    )


def list_items(
    db: Session,
    status: Optional[Status] = None,
    tag: Optional[str] = None,
    q: Optional[str] = None,
) -> List[ReadingItem]:
    query = db.query(ReadingItemModel)

    if status is not None:
        query = query.filter(ReadingItemModel.status == status)

    if q is not None:
        query = query.filter(ReadingItemModel.title.ilike(f"%{q}%"))

    db_items = query.all()

    if tag is not None:
        db_items = [item for item in db_items if item.tags and tag in item.tags]

    return [
        ReadingItem(
            id=item.id,
            title=item.title,
            url=item.url,
            tags=item.tags or [],
            priority=item.priority,
            status=item.status,
        )
        for item in db_items
    ]


def get_item(db: Session, item_id: int) -> ReadingItem:
    db_item = db.query(ReadingItemModel).filter(ReadingItemModel.id == item_id).first()
    if not db_item:
        raise KeyError("not_found")
    return ReadingItem(
        id=db_item.id,
        title=db_item.title,
        url=db_item.url,
        tags=db_item.tags or [],
        priority=db_item.priority,
        status=db_item.status,
    )


def update_item(db: Session, item_id: int, patch: ReadingItemUpdate) -> ReadingItem:
    db_item = db.query(ReadingItemModel).filter(ReadingItemModel.id == item_id).first()
    if not db_item:
        raise KeyError("not_found")

    data = patch.model_dump(exclude_unset=True)
    for field, value in data.items():
        if field == "url" and value is not None:
            setattr(db_item, field, str(value))
        else:
            setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return ReadingItem(
        id=db_item.id,
        title=db_item.title,
        url=db_item.url,
        tags=db_item.tags or [],
        priority=db_item.priority,
        status=db_item.status,
    )


def delete_item(db: Session, item_id: int) -> None:
    db_item = db.query(ReadingItemModel).filter(ReadingItemModel.id == item_id).first()
    if not db_item:
        raise KeyError("not_found")
    db.delete(db_item)
    db.commit()
