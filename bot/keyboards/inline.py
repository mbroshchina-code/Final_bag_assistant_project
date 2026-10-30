"""Inline-клавиатуры для бота."""

from aiogram.utils.keyboard import InlineKeyboardBuilder


def feedback_kb(message_id: str):
    """Одна оценка на сохранённое backend-сообщение."""
    builder = InlineKeyboardBuilder()
    builder.button(text="👍", callback_data=f"fb:up:{message_id}")
    builder.button(text="👎", callback_data=f"fb:down:{message_id}")
    builder.adjust(2)
    return builder.as_markup()
