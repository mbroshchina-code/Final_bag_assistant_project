"""Базовые команды бота."""

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from bot.handlers.streaming import service_error_message
from bot.services.backend_client import BackendClient

router = Router()

def session_keyboard() -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Новая сессия")]
        ],
        resize_keyboard=True,
        is_persistent=True,
    )


@router.message(Command("new"))
@router.message(F.text == "Новая сессия")
async def cmd_new_session(
    message: types.Message,
    backend: BackendClient,
    state: FSMContext,
) -> None:
    try:
        chat_id = await backend.create_new_chat(
            owner_external_id=str(message.from_user.id),
            interface="telegram",
        )
    except Exception as exc:
        await message.answer(service_error_message(exc))
        return

    await state.clear()
    await message.answer(
        f"Новая сессия создана.\n"
        f"Номер сессии: {chat_id}\n"
        "Опишите проблему клиента.",
        reply_markup=session_keyboard(),
    )

@router.message(Command("start"))
async def cmd_start(message: types.Message, backend: BackendClient) -> None:
    """Приветствие + создание чата в backend."""
    try:
        await backend.get_or_create_chat(
            owner_external_id=str(message.from_user.id),
            interface="telegram",
        )
    except Exception as exc:
        await message.answer(service_error_message(exc))
        return
    await message.answer(
        "Привет! Опишите проблему клиента — я найду известные баги.\n"
        "/new — новая сессия\n"
        "/clear — очистить историю текущей сессии\n"
        "/help — справка",
        reply_markup=session_keyboard(),
    )


@router.message(Command("help"))
async def cmd_help(message: types.Message) -> None:
    """Справка по командам."""
    await message.answer(
        "Доступные команды:\n"
        "/start — начать диалог\n"
        "/new — новая сессия без удаления предыдущей\n"
        "/clear — очистить историю диалога\n"
        "/help — эта справка"
    )


@router.message(Command("clear"))
async def cmd_clear(message: types.Message, backend: BackendClient) -> None:
    """Очистка истории чата."""
    try:
        chat_id = await backend.get_or_create_chat(
            owner_external_id=str(message.from_user.id),
            interface="telegram",
        )
        await backend.clear_messages(chat_id)
        await message.answer("История очищена.")
    except Exception as exc:
        await message.answer(service_error_message(exc))

