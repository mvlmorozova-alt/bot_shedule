"""Команда /start и кнопка «Начать»: приветствие и главное меню."""

from vkbottle.bot import BotLabeler, Message

import keyboards
import texts
from states import state_dispenser

labeler = BotLabeler()
labeler.vbml_ignore_case = True


@labeler.message(command="start")
@labeler.message(text=texts.BTN_START)
async def start_handler(message: Message) -> None:
    """Сбрасывает незавершённый сценарий и показывает приветствие с меню."""
    await state_dispenser.delete(message.peer_id)
    await message.answer(texts.WELCOME, keyboard=keyboards.main_menu())
