"""Обработчики сообщений. Порядок в labelers важен: он задаёт приоритет."""

from handlers.fallback import labeler as fallback_labeler
from handlers.help import labeler as help_labeler
from handlers.schedule import labeler as schedule_labeler
from handlers.start import labeler as start_labeler

# fallback должен быть последним: он ловит всё, что не подошло остальным.
labelers = [start_labeler, help_labeler, schedule_labeler, fallback_labeler]

__all__ = ["labelers"]
