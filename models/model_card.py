"""Модели данных для карточек NextCloud Deck"""

from typing import Optional, List
from pydantic import BaseModel


class ModelCard(BaseModel):
    """
    Упрощенная модель карточки для списка покупок

    :param id: Уникальный идентификатор карточки
    :type id: int
    :param title: Заголовок карточки
    :type title: str
    :param description: Описание карточки (список покупок)
    :type description: Optional[str]
    :param stack_id: ID стека в котором находится карточка
    :type stack_id: int
    """

    id: int
    title: str
    description: Optional[str] = None
    stack_id: int

    @property
    def short_title(self) -> str:
        """Сокращенный заголовок для кнопок"""
        MAX_TITLE_LENGTH = 30
        ELLIPSIS_LENGTH = 3

        if len(self.title) > MAX_TITLE_LENGTH:
            return self.title[: MAX_TITLE_LENGTH - ELLIPSIS_LENGTH] + "..."
        return self.title

    def get_list_items(self) -> List[str]:
        """
        Получить элементы списка из описания

        :return: Список очищенных элементов
        :rtype: List[str]
        """
        if not self.description:
            return []

        items = []
        lines = self.description.split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Очищаем от маркеров списка
            clean_line = self._clean_list_item(line)
            if clean_line:
                items.append(clean_line)

        return items

    def _clean_list_item(self, line: str) -> Optional[str]:
        """Очистить элемент списка от маркеров"""
        MARKER_CHECKBOX_UNCHECKED = "- [ ] "
        MARKER_CHECKBOX_CHECKED = "- [x] "
        MARKER_DASH = "- "
        MARKER_ASTERISK = "* "

        if line.startswith(MARKER_CHECKBOX_UNCHECKED) or line.startswith(
            MARKER_CHECKBOX_CHECKED
        ):
            return line[6:].strip()  # Убираем "- [ ] " или "- [x] "
        elif line.startswith(MARKER_DASH) or line.startswith(MARKER_ASTERISK):
            return line[2:].strip()  # Убираем "- " или "* "
        elif line[0].isdigit() and ". " in line:
            return line.split(". ", 1)[1].strip()  # Убираем "1. "

        return line.strip() if line.strip() else None

    def update_list_items(self, items: List[str]) -> str:
        """
        Обновить элементы списка в формате задач

        :param items: Список элементов для добавления
        :type items: List[str]
        :return: Отформатированное описание карточки
        :rtype: str
        """
        if not items:
            return ""

        list_lines = []
        CHECKBOX_TEMPLATE = "- [ ] {item}"

        for item in items:
            list_lines.append(CHECKBOX_TEMPLATE.format(item=item))

        return "\n".join(list_lines)
