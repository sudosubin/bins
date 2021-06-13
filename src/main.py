import asyncio

from command import Command
from package.load import load_collection


async def main():
    # preload collection
    await load_collection()

    # run command
    await Command.run()


if __name__ == '__main__':
    asyncio.run(main())
