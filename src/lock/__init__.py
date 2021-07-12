import json
import os
from collections import OrderedDict
from typing import Optional

from aiopath import AsyncPath
from anyio import AsyncFile

from utils.configs import INSTALL_DIR


class PackageLock(object):
    """Manages package's lock file

    Attributes:
        package_name: Package's name
        lock_content: Lock file's content (key: name, version, files, ...)
    """

    package_name: str
    lock_content: Optional[OrderedDict] = None

    def __init__(self, package_name: str):
        self.package_name = package_name

    @property
    def lock_file(self):
        lock_dir = os.path.join(INSTALL_DIR, self.package_name, 'lock.json')
        return AsyncPath(lock_dir)

    async def read(self):
        """Read lock file's content"""

        if self.lock_content is not None:
            return self.lock_content

        # Create if not exists
        await self.lock_file.parent.mkdir(parents=True, exist_ok=True)
        await self.lock_file.touch()

        # Read lock file
        async with self.lock_file.open() as file:
            file: AsyncFile
            lock_content = await file.read()

            try:
                self.lock_content = OrderedDict(json.loads(lock_content))
            except json.JSONDecodeError:
                self.lock_content = OrderedDict({'name': self.package_name})

        return self.lock_content

    async def write(self, **kwargs):
        """Write lock content to lock file"""

        raw_content = {**(self.lock_content or {}), **kwargs}
        lock_content = OrderedDict(sorted(raw_content.items(), key=lambda item: item[0]))

        await self.lock_file.write_text(json.dumps(lock_content, indent=2))
        self.lock_content = lock_content
