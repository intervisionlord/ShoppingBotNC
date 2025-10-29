"""Модели данных для стеков NextCloud Deck"""

from typing import List, Optional

from pydantic import BaseModel


class ModelStack(BaseModel):
    """Модель стека карточек"""

    title: str
    boardId: int
    deletedAt: int
    lastModified: int
    cards: Optional[List] = None
    order: int
    id: int
