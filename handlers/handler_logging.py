"""Обработчик логирования"""

import sys

from loguru import logger
from config.settings import settings

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:DD-MM-YYYY HH:mm:ss}</green> | "
    "<level>{level}</level> | "
    "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "{message}",
    colorize=True,
    level=settings.LOG_LEVEL.upper(),
)

logger.level("DEBUG", color="<cyan>")
logger.level("INFO", color="<green>")
logger.level("SUCCESS", color="<green><bold>")
logger.level("WARNING", color="<yellow><bold>")
logger.level("ERROR", color="<red>")
logger.level("CRITICAL", color="<red><bold>")
