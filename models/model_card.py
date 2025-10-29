"""Модели данных для карточек NextCloud Deck"""

from typing import Optional, List
from pydantic import BaseModel


class ShoppingCard(BaseModel):
    """Упрощенная модель карточки для списка покупок"""

    id: int
    title: str
    description: Optional[str] = None
    stack_id: int

    @property
    def short_title(self) -> str:
        """Сокращенный заголовок для кнопок"""
        if len(self.title) > 30:
            return self.title[:27] + "..."
        return self.title

    def get_list_items(self) -> List[str]:
        """Получить элементы списка из описания"""
        if not self.description:
            return []

        items = []
        lines = self.description.split("\n")
        for line in lines:
            line = line.strip()
            if line and (
                line.startswith("- ")
                or line.startswith("* ")
                or line.startswith("- [ ] ")
                or line.startswith("- [x] ")
                or line[0].isdigit()
                and ". " in line
            ):
                # Очищаем от маркеров списка
                clean_line = line
                if line.startswith("- [ ] ") or line.startswith("- [x] "):
                    clean_line = line[6:]  # Убираем "- [ ] " или "- [x] "
                elif line.startswith("- ") or line.startswith("* "):
                    clean_line = line[2:]  # Убираем "- " или "* "
                elif ". " in line and line[0].isdigit():
                    clean_line = line.split(". ", 1)[1]  # Убираем "1. "

                items.append(clean_line.strip())

        return items

    def update_list_items(self, items: List[str]) -> str:
        """Обновить элементы списка в формате задач"""
        if not items:
            return ""

        list_lines = []
        for item in items:
            # Форматируем как задачи
            list_lines.append(f"- [ ] {item}")  # noqa: E201

        return "\n".join(list_lines)
