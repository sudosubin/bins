import os
from typing import Optional

from aiopath import AsyncPath
from anyio import AsyncFile

from console import message
from console.dynamic import DynamicConsole
from lock import PackageLock
from package.source import PackageSource
from package.status import PackageStatus
from package.utils.load import load_collection
from source.base import BasePackageSource
from utils.archive import unarchive_file
from utils.configs import INSTALL_DIR
from utils.request import request


class Package(object):
    """Download, install specific package.

    Attributes:
        name: Package name
        version: Package version to install (default to latest)
        description: Package description

        repo: Package vcs repository name
        source: Package source type

        asset_pattern: Asset searching from release, regex pattern (github release)
        bin_pattern: Bin searching from unarchived output, regex pattern (github release)

        _lock: Package lock instance
        _source: Package source instance
    """

    name: str
    version: Optional[str] = None
    description: Optional[str] = None

    repo: Optional[str] = None
    source: PackageSource = PackageSource.NONE

    asset_pattern: Optional[str] = None
    bin_pattern: Optional[str] = None

    _lock: PackageLock
    _source: BasePackageSource

    def __init__(self):
        if self.source is PackageSource.NONE:
            raise ValueError('Package source was not specified!')

        self._lock = PackageLock(self.name)
        self._source = self.source.value(self)

    async def installed_version(self) -> Optional[str]:
        """Returns current installed package's version or None"""

        lock_content = await self._lock.read()
        return lock_content.get('version')

    async def planned_version(self) -> str:
        """Returns specific version to install"""

        return await self._source.planned_version()

    async def status(self) -> PackageStatus:
        """Returns package's status: install, update, removal, none"""

        installed_version = await self.installed_version()
        planned_version = await self.planned_version()

        if installed_version is None:
            return PackageStatus.INSTALL

        if installed_version != planned_version:
            return PackageStatus.UPDATE

        return PackageStatus.NONE

    async def check(self):
        """Get current installed version, and a version to install"""

        prev_version = await self.installed_version()
        next_version = await self.planned_version()

        message.print_package_check(self.name, prev_version, next_version)

    async def install(self):
        """Download package from source"""

        prev_version = await self.installed_version()
        next_version = await self.planned_version()

        def _get_heading(finish: bool = False):
            return message.get_package_install(self.name, prev_version, next_version, finish=finish)

        with DynamicConsole(_get_heading()) as dynamic:
            download_url = await self._source.download_url()
            download_file_name = download_url.split('/')[-1]

            # TODO(sudosubin): Use RFC-6266 'Content-Disposition' header to improve
            download_file_dir = os.path.join(INSTALL_DIR, self.name, download_file_name)
            out_dir = os.path.join(INSTALL_DIR, self.name, 'out')

            # Download file
            async with request.session.get(download_url) as response:
                chunks: bytes = b''
                content_length = int(response.headers.get('Content-Length', '0')) or None

                dynamic.add_message(message.get_package_download(download_file_name, content_length))
                dynamic.add_message(message.get_package_download_progress(content_length, 0))

                async for chunk in response.content.iter_chunked(1024):
                    chunks += chunk
                    dynamic.update_message(message.get_package_download_progress(content_length, len(chunks)))

                async with await AsyncPath(download_file_dir).open(mode='wb', encoding=None, errors=None,
                                                                   newline=None) as file:
                    file: AsyncFile
                    await file.write(chunks)

                dynamic.update_message(message.get_package_download_progress(finish=True))

            if self.bin_pattern is not None:
                dynamic.add_message(message.get_package_install_file(self.bin_pattern))

            # Extract file
            await unarchive_file(download_file_dir, out_dir)

            # Write lock
            await self._lock.write(version=next_version, bins=[])

            dynamic.update_heading(_get_heading(finish=True))

    @classmethod
    async def collection(cls):
        await load_collection()
        return cls.__subclasses__()
