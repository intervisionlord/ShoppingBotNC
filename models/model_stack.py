from typing import List, Optional

from pydantic import BaseModel

# "title": "ToDo",
# "boardId": 2,
# "deletedAt": 0,
# "lastModified": 1541426139,
# "cards": [...],
# "order": 999,
# "id": 4


class ModelStack(BaseModel):
    title: str
    boardId: int
    deletedAt: int
    lastModified: int
    cards: Optional[List] = None
    order: int
    id: int
