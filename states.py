"""Состояния диалога и общее хранилище состояний (в памяти)."""

from vkbottle import BaseStateGroup, BuiltinStateDispenser


class ScheduleState(BaseStateGroup):
    """Шаги сценария «Расписание»."""

    WAITING_GROUP = "waiting_group"


# Одно хранилище на весь бот: передаётся в Bot и используется в обработчиках.
state_dispenser = BuiltinStateDispenser()
