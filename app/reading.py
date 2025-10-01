from enum import Enum
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl, conint, constr

router = APIRouter(prefix="/reading-list", tags=["reading-list"])


class Status(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


TitleStr = constr(min_length=1, max_length=120, strip_whitespace=True)
TagStr = constr(min_length=1, max_length=24, strip_whitespace=True)
PriorityInt = conint(ge=1, le=5)


class ReadingItemBase(BaseModel):
    title: TitleStr
    url: Optional[HttpUrl] = None
    tags: List[TagStr] = []
    priority: PriorityInt = 3


class ReadingItemCreate(ReadingItemBase):
    pass


class ReadingItemUpdate(BaseModel):
    title: Optional[TitleStr] = None
    url: Optional[HttpUrl] = None
    tags: Optional[List[TagStr]] = None
    priority: Optional[PriorityInt] = None
    status: Optional[Status] = None


class ReadingItem(ReadingItemBase):
    id: int
    status: Status = Status.todo


_DB: Dict[int, ReadingItem] = {}
_SEQ: int = 0


def _next_id() -> int:
    global _SEQ
    _SEQ += 1
    return _SEQ


@router.post("", response_model=ReadingItem, status_code=201)
def create_item(payload: ReadingItemCreate):
    item = ReadingItem(id=_next_id(), status=Status.todo, **payload.dict())
    _DB[item.id] = item
    return item


@router.get("", response_model=List[ReadingItem])
def list_items(
    status: Optional[Status] = None, tag: Optional[str] = None, q: Optional[str] = None
):
    items = list(_DB.values())
    if status is not None:
        items = [i for i in items if i.status == status]
    if tag is not None:
        items = [i for i in items if tag in i.tags]
    if q is not None:
        ql = q.lower()
        items = [i for i in items if ql in i.title.lower()]
    return items


@router.get("/{item_id}", response_model=ReadingItem)
def get_item(item_id: int):
    item = _DB.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    return item


@router.patch("/{item_id}", response_model=ReadingItem)
def update_item(item_id: int, patch: ReadingItemUpdate):
    item = _DB.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    data = patch.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(item, field, value)
    _DB[item_id] = item
    return item


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int):
    if item_id not in _DB:
        raise HTTPException(status_code=404, detail="item not found")
    del _DB[item_id]
    return None
