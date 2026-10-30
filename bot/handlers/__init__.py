"""Сборка всех роутеров handlers."""

from bot.handlers import admin, commands, feedback, media, text


def get_routers():
    return [
        admin.router,
        feedback.router,
        commands.router,
        media.router,
        text.router,
    ]
