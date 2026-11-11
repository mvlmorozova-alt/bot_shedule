"""Настройки бота из переменных окружения (файл .env)."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    """Параметры запуска бота и сайта."""

    vk_token: str
    vk_group_id: int
    site_host: str
    site_port: int


def load_config() -> Config:
    """Читает .env и проверяет, что токен и ID сообщества заданы."""
    load_dotenv()
    token = os.getenv("VK_TOKEN", "").strip()
    group_id = os.getenv("VK_GROUP_ID", "").strip()
    if not token or not group_id.isdigit():
        raise SystemExit(
            "Заполните VK_TOKEN и VK_GROUP_ID в файле .env (см. .env.example)"
        )
    return Config(
        vk_token=token,
        vk_group_id=int(group_id),
        site_host=os.getenv("SITE_HOST", "127.0.0.1"),
        site_port=int(os.getenv("SITE_PORT", "8080")),
    )
