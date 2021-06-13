import importlib
import os

from aiopath import AsyncPath

from utils.configs import PROJECT_DIR


async def load_collection():
    """Preload all collection classes."""

    collection = AsyncPath(os.path.join(PROJECT_DIR, 'collection'))

    async for path in collection.iterdir():
        if path.suffix != '.py':
            continue

        importlib.import_module(f'collection.{path.stem}')
