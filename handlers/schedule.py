"""Диалоговый сценарий «Расписание».

Расписание → бот просит выбрать группу (состояние WAITING_GROUP)
→ пользователь нажимает 101/102/103 → бот присылает расписание
и сбрасывает состояние. «Отмена» выходит из сценария.
"""

from vkbottle.bot import BotLabeler, Message

import keyboards
import texts
from schedule_data import get_schedule
from states import ScheduleState, state_dispenser

labeler = BotLabeler()
labeler.vbml_ignore_case = True


@labeler.message(command="schedule")
@labeler.message(text=[texts.BTN_SCHEDULE, "Когда занятия?"])
async def schedule_request_handler(message: Message) -> None:
    """Начинает сценарий: запоминает состояние и предлагает выбрать группу."""
    await state_dispenser.set(message.peer_id, ScheduleState.WAITING_GROUP)
    await message.answer(texts.ASK_GROUP, keyboard=keyboards.groups_keyboard())


@labeler.message(state=ScheduleState.WAITING_GROUP, text=texts.BTN_CANCEL)
async def cancel_handler(message: Message) -> None:
    """Выход из сценария без выбора группы."""
    await state_dispenser.delete(message.peer_id)
    await message.answer(texts.CANCELLED, keyboard=keyboards.main_menu())


@labeler.message(state=ScheduleState.WAITING_GROUP)
async def group_input_handler(message: Message) -> None:
    """Обрабатывает номер группы, пока бот ждёт его."""
    group = message.text.strip()
    schedule = get_schedule(group)
    if schedule is None:
        await message.answer(
            texts.GROUP_NOT_FOUND, keyboard=keyboards.groups_keyboard()
        )
        return
    await state_dispenser.delete(message.peer_id)
    await message.answer(
        texts.schedule_message(group, schedule), keyboard=keyboards.main_menu()
    )
