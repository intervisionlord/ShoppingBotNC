"""Модели данных для досок NextCloud Deck"""

from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class Owner(BaseModel):
    """Модель владельца доски"""

    primaryKey: str
    uid: str
    displayname: str


class Permissions(BaseModel):
    """Модель разрешений доски"""

    PERMISSION_READ: bool
    PERMISSION_EDIT: bool
    PERMISSION_MANAGE: bool
    PERMISSION_SHARE: bool


class Settings(BaseModel):
    """Модель настроек доски"""

    notify_due: str
    calendar: bool


class ModelBoard(BaseModel):
    """Основная модель доски"""

    title: str
    owner: Owner
    color: str
    archived: bool
    labels: List[str]
    acl: List[Dict]
    permissions: Permissions
    users: List[Dict]
    shared: int
    deletedAt: int
    id: int
    lastModified: int
    settings: Optional[Union[Settings, List]] = None
