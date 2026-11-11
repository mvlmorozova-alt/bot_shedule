"""Ответ на любые сообщения, которые не подошли другим обработчикам."""

from vkbottle.bot import BotLabeler, Message

import keyboards
import texts

labeler = BotLabeler()


@labeler.message()
async def fallback_handler(message: Message) -> None:
    """Подсказывает, как получить список команд."""
    await message.answer(texts.UNKNOWN, keyboard=keyboards.main_menu())
