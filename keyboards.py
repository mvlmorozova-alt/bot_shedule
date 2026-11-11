"""Клавиатуры бота (inline — кнопки прямо под сообщением)."""

from vkbottle import Keyboard, KeyboardButtonColor, Text

import texts
from schedule_data import SCHEDULES


def main_menu() -> str:
    """Главное меню: расписание и помощь."""
    keyboard = Keyboard(inline=True)
    keyboard.add(Text(texts.BTN_SCHEDULE), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text(texts.BTN_HELP), color=KeyboardButtonColor.SECONDARY)
    return keyboard.get_json()


def groups_keyboard() -> str:
    """Выбор номера группы и кнопка отмены."""
    keyboard = Keyboard(inline=True)
    for group in SCHEDULES:
        keyboard.add(Text(group), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text(texts.BTN_CANCEL), color=KeyboardButtonColor.NEGATIVE)
    return keyboard.get_json()
