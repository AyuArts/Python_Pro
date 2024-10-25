from aiohttp import web
import asyncio

async def handle_root(request):
    """
    Обробник маршруту "/". Повертає простий текст "Hello, World!".
    """
    return web.Response(text="Hello, World!")

async def handle_slow(request):
    """
    Обробник маршруту "/slow". Імітує довгу операцію з затримкою в 5 секунд,
    після чого повертає текст "Operation completed".
    """
    await asyncio.sleep(5)
    return web.Response(text="Operation completed")

async def init_app():
    """
    Ініціалізація та налаштування веб-додатку.
    """
    app = web.Application()
    app.add_routes([
        web.get('/', handle_root),
        web.get('/slow', handle_slow)
    ])
    return app

if __name__ == '__main__':
    web.run_app(init_app())
