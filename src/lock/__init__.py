import json
import os
from collections import OrderedDict
from typing import Any, Literal, Optional
from typing import OrderedDict as _OrderedDict

from aiopath import AsyncPath
from anyio import AsyncFile

from utils.configs import INSTALL_DIR

_PackageLockKey = Literal['name', 'version', 'bins']


class PackageLock(object):
    """Manages package's lock file

    Attributes:
        package_name: Package's name
        lock_content: Lock file's content
    """

    package_name: str
    lock_content: Optional[_OrderedDict[_PackageLockKey, Any]] = None

    def __init__(self, name: str):
        self.package_name = name

    @property
    def lock_file(self):
        return AsyncPath(os.path.join(INSTALL_DIR, self.package_name, 'lock.json'))

    async def read(self):
        """Read lock file's content"""

        if self.lock_content is not None:
            return self.lock_content

        # Create if not exists
        await self.lock_file.parent.mkdir(parents=True, exist_ok=True)
        await self.lock_file.touch()

        # Read lock file
        async with await self.lock_file.open() as file:
            file: AsyncFile
            lock_content = await file.read()

            try:
                self.lock_content = OrderedDict(json.loads(lock_content))
            except (json.JSONDecodeError, KeyError):
                self.lock_content = OrderedDict()

        return self.lock_content

    async def write(self, **kwargs):
        """Write lock content to lock file"""

        raw_content = {**(self.lock_content or {}), **kwargs}
        lock_content = OrderedDict(sorted(raw_content.items(), key=lambda item: item[0]))

        async with await self.lock_file.open(mode='wb', encoding=None, errors=None, newline=None) as file:
            file: AsyncFile

            raw_data = json.dumps(lock_content, indent=2).encode()
            await file.write(raw_data)

        self.lock_content = lock_content  # type: ignore
