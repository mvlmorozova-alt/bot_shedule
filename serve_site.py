"""Локальный сервер для страницы сайта с виджетом сообщений VK.

Подставляет VK_GROUP_ID из .env в site/index.html и отдаёт страницу.
Это только демонстрация: на реальном сайте достаточно вставить код
виджета из site/index.html с ID своего сообщества.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from config import load_config

PAGE_PATH = Path(__file__).parent / "site" / "index.html"


def render_page(group_id: int) -> bytes:
    """Возвращает HTML страницы с подставленным ID сообщества."""
    html = PAGE_PATH.read_text(encoding="utf-8")
    return html.replace("{{GROUP_ID}}", str(group_id)).encode("utf-8")


def make_handler(page: bytes) -> type[BaseHTTPRequestHandler]:
    """Создаёт обработчик HTTP, который на любой GET отдаёт страницу."""

    class PageHandler(BaseHTTPRequestHandler):
        """Отдаёт одну и ту же HTML-страницу."""

        def do_GET(self) -> None:  # noqa: N802 (имя задано http.server)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(page)))
            self.end_headers()
            self.wfile.write(page)

    return PageHandler


def main() -> None:
    """Запускает сервер сайта до нажатия Ctrl+C."""
    config = load_config()
    page = render_page(config.vk_group_id)
    server = ThreadingHTTPServer(
        (config.site_host, config.site_port), make_handler(page)
    )
    print(f"Сайт: http://{config.site_host}:{config.site_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
