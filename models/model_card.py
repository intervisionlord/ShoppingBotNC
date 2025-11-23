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
        match line:
            case line if line.startswith("- [ ] "):
                return line[6:].strip()  # Убираем "- [ ] "
            case line if line.startswith("- [x] "):
                return line[6:].strip()  # Убираем "- [x] "
            case line if line.startswith("- ") or line.startswith("* "):
                return line[2:].strip()  # Убираем "- " или "* "
            case line if line[0].isdigit() and ". " in line:
                return line.split(". ", 1)[1].strip()  # Убираем "1. "
            case _:
                return line.strip() if line.strip() else None

    def update_list_items(self, items: List[str]) -> str:
        """
        Обновить элементы списка в формате задач, сохраняя состояние выполненных элементов

        :param items: Список элементов для добавления
        :type items: List[str]
        :return: Отформатированное описание карточки
        :rtype: str
        """
        if not items:
            return ""

        # Создаем словарь для отслеживания состояния элементов
        item_states = {}

        # Парсим текущее описание, чтобы сохранить состояния
        if self.description:
            lines = self.description.split("\n")
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Определяем состояние элемента с помощью match case
                match line:
                    case line if line.startswith("- [x] "):
                        item_text = line[6:].strip()
                        item_states[item_text] = "checked"
                    case line if line.startswith("- [ ] "):
                        item_text = line[6:].strip()
                        item_states[item_text] = "unchecked"
                    case line if line.startswith("- ") or line.startswith("* "):
                        item_text = line[2:].strip()
                        item_states[item_text] = "unchecked"
                    case line if line[0].isdigit() and ". " in line:
                        item_text = line.split(". ", 1)[1].strip()
                        item_states[item_text] = "unchecked"
                    case _:
                        item_text = line.strip()
                        item_states[item_text] = "unchecked"

        # Создаем новые строки с сохранением состояний
        list_lines = []
        for item in items:
            # Используем сохраненное состояние или создаем новый unchecked элемент
            state = item_states.get(item, "unchecked")
            checkbox = "- [x] " if state == "checked" else "- [ ] "
            list_lines.append(f"{checkbox}{item}")

        return "\n".join(list_lines)

    def get_list_items_with_states(self) -> List[dict]:
        """
        Получить элементы списка с их состояниями

        :return: Список словарей с элементами и их состояниями
        :rtype: List[dict]
        """
        if not self.description:
            return []

        items = []
        lines = self.description.split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Определяем состояние элемента с помощью match case
            match line:
                case line if line.startswith("- [x] "):
                    item_text = line[6:].strip()
                    items.append({"text": item_text, "checked": True})
                case line if line.startswith("- [ ] "):
                    item_text = line[6:].strip()
                    items.append({"text": item_text, "checked": False})
                case line if line.startswith("- ") or line.startswith("* "):
                    item_text = line[2:].strip()
                    items.append({"text": item_text, "checked": False})
                case line if line[0].isdigit() and ". " in line:
                    item_text = line.split(". ", 1)[1].strip()
                    items.append({"text": item_text, "checked": False})
                case _:
                    item_text = line.strip()
                    items.append({"text": item_text, "checked": False})

        return items
