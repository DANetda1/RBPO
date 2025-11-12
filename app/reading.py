from fastapi import APIRouter, Depends, HTTPException, Query
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
from app.validators import validate_search_query, validate_tag

router = APIRouter(prefix="/reading-list", tags=["reading-list"])


@router.post("", response_model=ReadingItem, status_code=201)
def create_item(payload: ReadingItemCreate, db: Session = Depends(get_db)):
    return svc_create(db, payload)


@router.get("", response_model=list[ReadingItem])
def list_items(
    status: Status | None = None,
    tag: str | None = Query(None, max_length=24),
    q: str | None = Query(None, max_length=100),
    db: Session = Depends(get_db),
):
    try:
        validated_q = validate_search_query(q) if q else None
        validated_tag = validate_tag(tag) if tag else None
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e

    return svc_list(db, status, validated_tag, validated_q)


@router.get("/{item_id}", response_model=ReadingItem)
def get_item(item_id: int, db: Session = Depends(get_db)):
    try:
        return svc_get(db, item_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="item not found") from None


@router.patch("/{item_id}", response_model=ReadingItem)
def update_item(item_id: int, patch: ReadingItemUpdate, db: Session = Depends(get_db)):
    try:
        return svc_update(db, item_id, patch)
    except KeyError:
        raise HTTPException(status_code=404, detail="item not found") from None


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    try:
        svc_delete(db, item_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="item not found") from None
    return None
