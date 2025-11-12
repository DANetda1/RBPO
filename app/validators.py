import re


def validate_search_query(q: str | None) -> str | None:
    if q is None:
        return None

    if len(q) > 100:
        raise ValueError("Search query too long (max 100 characters)")

    if not re.match(r"^[\w\s\-.,!?()]+$", q):
        raise ValueError("Search query contains invalid characters")

    q_clean = q.strip()
    if len(q_clean) < 1:
        return None

    return q_clean


def validate_tag(tag: str | None) -> str | None:
    if tag is None:
        return None

    if len(tag) > 24:
        raise ValueError("Tag too long (max 24 characters)")

    if not re.match(r"^[a-zA-Z0-9_-]+$", tag):
        raise ValueError("Tag contains invalid characters")

    return tag.strip()
