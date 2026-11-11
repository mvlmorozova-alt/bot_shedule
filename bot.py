"""Точка входа: создаёт бота vkbottle и запускает Long Poll."""

from vkbottle import API
from vkbottle.bot import Bot

from config import load_config
from handlers import labelers
from states import state_dispenser


def create_bot(token: str) -> Bot:
    """Собирает бота: API, хранилище состояний и все обработчики."""
    bot = Bot(api=API(token), state_dispenser=state_dispenser)
    for labeler in labelers:
        bot.labeler.load(labeler)
    return bot


def main() -> None:
    """Читает настройки и запускает бесконечный цикл получения сообщений."""
    config = load_config()
    bot = create_bot(config.vk_token)
    bot.run_forever()


if __name__ == "__main__":
    main()
