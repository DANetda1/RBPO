from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.reading import (
    ReadingItem,
    ReadingItemCreate,
    ReadingItemUpdate,
    Status,
)
from app.services.reading_service import create_item as svc_create
from app.services.reading_service import delete_item as svc_delete
from app.services.reading_service import get_item as svc_get
from app.services.reading_service import list_items as svc_list
from app.services.reading_service import update_item as svc_update

router = APIRouter(prefix="/reading-list", tags=["reading-list"])


@router.post("", response_model=ReadingItem, status_code=201)
def create_item(payload: ReadingItemCreate, db: Session = Depends(get_db)):
    return svc_create(db, payload)


@router.get("", response_model=List[ReadingItem])
def list_items(
    status: Optional[Status] = None,
    tag: Optional[str] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return svc_list(db, status, tag, q)


@router.get("/{item_id}", response_model=ReadingItem)
def get_item(item_id: int, db: Session = Depends(get_db)):
    try:
        return svc_get(db, item_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="item not found")


@router.patch("/{item_id}", response_model=ReadingItem)
def update_item(item_id: int, patch: ReadingItemUpdate, db: Session = Depends(get_db)):
    try:
        return svc_update(db, item_id, patch)
    except KeyError:
        raise HTTPException(status_code=404, detail="item not found")


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    try:
        svc_delete(db, item_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="item not found")
    return None
