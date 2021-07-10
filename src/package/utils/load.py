import importlib
import sys
from typing import Dict, List

from aiopath import AsyncPath

from lock import PackageLock
from utils.configs import COLLECTION_DIR, INSTALL_DIR


async def load_collection() -> List[str]:
    """Preload all package classes"""

    collection_packages: List[str] = []

    # Loads from sys.modules
    for module in sys.modules.keys():
        if not module.startswith('collection.'):
            continue

        package = module.replace('collection.', '')
        collection_packages.append(package)

    if collection_packages:
        return collection_packages

    # Import and loads from local modules
    async for path in AsyncPath(COLLECTION_DIR).glob('**/*'):
        if path.suffix != '.py':
            continue

        relative_name = str(path.relative_to(COLLECTION_DIR))
        collection_name = relative_name.replace('/', '.').replace('.py', '')

        importlib.import_module(f'collection.{collection_name}')
        collection_packages.append(path.stem)

    return collection_packages


async def load_packages_removal() -> List[Dict]:
    """Get list of packages to remove from local"""

    removals: List[Dict] = []
    collection_packages = await load_collection()

    async for path in AsyncPath(INSTALL_DIR).iterdir():
        # Only check removal for folders
        if not await path.is_dir():
            continue

        # Should not be removed
        if path.name in collection_packages:
            continue

        lock = await PackageLock(path.name).read()
        removals.append({'name': path.name, 'version': lock.get('version', 'unknown')})

    return removals
