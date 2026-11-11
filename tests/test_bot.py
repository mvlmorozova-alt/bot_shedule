"""Проверка маршрутизации сообщений без обращения к настоящему VK API."""

import itertools
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import texts  # noqa: E402
from bot import create_bot  # noqa: E402
from states import state_dispenser  # noqa: E402

_ids = itertools.count(1)


def make_event(text: str, peer_id: int) -> dict:
    """Собирает событие message_new в формате Bots Long Poll API."""
    message_id = next(_ids)
    return {
        "type": "message_new",
        "event_id": f"e{message_id}",
        "group_id": 1,
        "object": {
            "message": {
                "id": message_id,
                "date": 0,
                "peer_id": peer_id,
                "from_id": peer_id,
                "text": text,
                "out": 0,
                "conversation_message_id": message_id,
                "fwd_messages": [],
                "attachments": [],
                "important": False,
                "is_hidden": False,
                "version": 1,
            },
            "client_info": {
                "button_actions": ["text"],
                "keyboard": True,
                "inline_keyboard": True,
                "carousel": False,
                "lang_id": 0,
            },
        },
    }


@pytest.fixture
def chat():
    """Возвращает функцию «отправить сообщение боту» → (текст, клавиатура)."""
    bot = create_bot("fake-token")
    sent = []

    async def fake_request(method, data, version=None):
        sent.append((method, data))
        peer_id = data["peer_ids"][0]
        return {"response": [{"peer_id": peer_id, "message_id": 1}]}

    bot.api.request = fake_request

    async def send(text, peer_id=100):
        sent.clear()
        await bot.router.route(make_event(text, peer_id), bot.api)
        assert len(sent) == 1, sent
        method, data = sent[0]
        assert method == "messages.send"
        raw_keyboard = data.get("keyboard")
        keyboard = json.loads(raw_keyboard) if raw_keyboard else None
        return data["message"], keyboard

    return send


def labels(keyboard):
    """Подписи всех кнопок клавиатуры."""
    return [b["action"]["label"] for row in keyboard["buttons"] for b in row]


@pytest.fixture(autouse=True)
async def clean_states():
    """Каждый тест начинается без сохранённых состояний."""
    for peer_id in (100, 200):
        await state_dispenser.delete(peer_id)


@pytest.mark.parametrize("text", ["/start", "Начать", "начать"])
async def test_start(chat, text):
    answer, keyboard = await chat(text)
    assert answer == texts.WELCOME
    assert keyboard["inline"] is True
    assert labels(keyboard) == ["Расписание", "Помощь"]


@pytest.mark.parametrize("text", ["/help", "Помощь"])
async def test_help(chat, text):
    answer, _ = await chat(text)
    assert answer == texts.HELP


async def test_schedule_scenario(chat):
    answer, keyboard = await chat("Расписание")
    assert answer == texts.ASK_GROUP
    assert labels(keyboard) == ["101", "102", "103", "Отмена"]

    answer, _ = await chat("555")
    assert answer == texts.GROUP_NOT_FOUND

    answer, keyboard = await chat("102")
    assert answer == "Расписание для группы 102: вторник/четверг 11:00–14:00."
    assert labels(keyboard) == ["Расписание", "Помощь"]

    # состояние сброшено — номер группы уже не распознаётся
    answer, _ = await chat("101")
    assert answer == texts.UNKNOWN


@pytest.mark.parametrize("text", ["/schedule", "Когда занятия?"])
async def test_schedule_aliases(chat, text):
    answer, _ = await chat(text)
    assert answer == texts.ASK_GROUP


async def test_cancel_and_start_reset_state(chat):
    await chat("Расписание")
    answer, _ = await chat("Отмена")
    assert answer == texts.CANCELLED
    assert (await chat("101"))[0] == texts.UNKNOWN

    await chat("Расписание")
    await chat("/start")
    assert (await chat("101"))[0] == texts.UNKNOWN


async def test_states_are_per_user(chat):
    await chat("Расписание", peer_id=100)
    assert (await chat("101", peer_id=200))[0] == texts.UNKNOWN
    assert "101" in (await chat("101", peer_id=100))[0]


async def test_unknown(chat):
    answer, _ = await chat("Какой сегодня праздник?")
    assert answer == texts.UNKNOWN
