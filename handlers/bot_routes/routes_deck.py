"""Главный роутер для бота списка покупок"""

from aiogram import Router

from handlers.bot_routes.route_list_cards import list_router
from handlers.bot_routes.route_view_card import view_router
from handlers.bot_routes.route_edit_items import edit_router

nc_deck_router = Router()

ROUTERS = (
    list_router,
    view_router,
    edit_router,
)

for router in ROUTERS:
    nc_deck_router.include_router(router)
