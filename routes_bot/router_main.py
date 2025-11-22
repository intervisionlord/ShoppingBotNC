"""Основной роутер, собирающий дополнительные роутеры"""

from aiogram import Router
from routes_bot.router_callback_cardslist import router as cardlist_router

main_router = Router()
main_router.include_router(cardlist_router)
