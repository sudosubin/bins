import asyncio

import uvloop

from command import Command

if __name__ == '__main__':
    uvloop.install()
    asyncio.run(Command.execute())
