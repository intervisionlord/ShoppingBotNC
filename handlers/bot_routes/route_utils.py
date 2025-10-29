"""Вспомогательные функции для роутов бота"""


def parse_new_items(text: str) -> list:
    """Парсит новые элементы из текста"""
    new_items_text = text.strip()
    if not new_items_text:
        return []

    if "," in new_items_text:
        return [item.strip() for item in new_items_text.split(",") if item.strip()]
    else:
        return [new_items_text]
