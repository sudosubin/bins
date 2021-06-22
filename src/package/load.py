import importlib
import sys
from typing import Dict, List, Literal

from aiopath import AsyncPath

from package.lock import PackageLock
from utils.configs import COLLECTION_DIR, INSTALL_DIR

_PackageRemovalKey = Literal['name', 'version']


async def load_collection() -> List[str]:
    """Preload all package classes."""

    collection_dir = AsyncPath(COLLECTION_DIR)
    collection_packages = [path.stem async for path in collection_dir.iterdir() if path.suffix == '.py']

    for name in collection_packages:
        if f'collection.{name}' in sys.modules:
            continue

        importlib.import_module(f'collection.{name}')

    return collection_packages


async def load_packages_removal() -> List[Dict[_PackageRemovalKey, str]]:
    """Get list of packages to remove from local"""
    async def get_package(name: str) -> Dict[_PackageRemovalKey, str]:
        lock_file = await PackageLock(name).read()
        return {'name': name, 'version': lock_file.get('version', 'unknown')}

    installed_dir = AsyncPath(INSTALL_DIR)
    installed_packages = [path.name async for path in installed_dir.iterdir() if await path.is_dir()]
    collection_packages = await load_collection()

    return [await get_package(name) for name in installed_packages if name not in collection_packages]
