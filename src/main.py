import asyncio

import uvloop
from rich import traceback

from command import Command

if __name__ == '__main__':
    traceback.install()
    uvloop.install()
    asyncio.run(Command.execute())
