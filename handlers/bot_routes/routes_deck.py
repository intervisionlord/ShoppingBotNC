"""Основной роутер для бота списка покупок (сборка всех подроутеров)"""

from aiogram import Router

from handlers.bot_routes.route_list_cards import list_router
from handlers.bot_routes.route_view_card import view_router
from handlers.bot_routes.route_edit_items import edit_router

# Создаем главный роутер и включаем все подроутеры
nc_deck_router = Router()
nc_deck_router.include_router(list_router)
nc_deck_router.include_router(view_router)
nc_deck_router.include_router(edit_router)
