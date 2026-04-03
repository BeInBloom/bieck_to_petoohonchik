import asyncio

from granian.constants import Interfaces
from granian.server.embed import Server

from app.asgi import app


async def run() -> None:
    server = Server(app, interface=Interfaces.ASGI)
    await server.serve()


def main() -> None:
    asyncio.run(run())
