from typing import Dict, List, Optional

from app.schemas.reading import (
    ReadingItem,
    ReadingItemCreate,
    ReadingItemUpdate,
    Status,
)

_DB: Dict[int, ReadingItem] = {}
_SEQ: int = 0


def _next_id() -> int:
    global _SEQ
    _SEQ += 1
    return _SEQ


def create_item(payload: ReadingItemCreate) -> ReadingItem:
    item = ReadingItem(id=_next_id(), status=Status.todo, **payload.dict())
    _DB[item.id] = item
    return item


def list_items(
    status: Optional[Status] = None,
    tag: Optional[str] = None,
    q: Optional[str] = None,
) -> List[ReadingItem]:
    items = list(_DB.values())
    if status is not None:
        items = [i for i in items if i.status == status]
    if tag is not None:
        items = [i for i in items if tag in i.tags]
    if q is not None:
        ql = q.lower()
        items = [i for i in items if ql in i.title.lower()]
    return items


def get_item(item_id: int) -> ReadingItem:
    item = _DB.get(item_id)
    if not item:
        raise KeyError("not_found")
    return item


def update_item(item_id: int, patch: ReadingItemUpdate) -> ReadingItem:
    item = _DB.get(item_id)
    if not item:
        raise KeyError("not_found")
    data = patch.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(item, field, value)
    _DB[item_id] = item
    return item


def delete_item(item_id: int) -> None:
    if item_id not in _DB:
        raise KeyError("not_found")
    del _DB[item_id]
