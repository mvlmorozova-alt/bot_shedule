"""Команда /help и кнопка «Помощь»: список доступных команд."""

from vkbottle.bot import BotLabeler, Message

import keyboards
import texts

labeler = BotLabeler()
labeler.vbml_ignore_case = True


@labeler.message(command="help")
@labeler.message(text=texts.BTN_HELP)
async def help_handler(message: Message) -> None:
    """Отправляет список команд и главное меню."""
    await message.answer(texts.HELP, keyboard=keyboards.main_menu())
