import os
from typing import Dict, Optional

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
from utils.formatters import format_download_filename
from utils.request import request
from utils.symlink import create_symlink


class Package(object):
    """Download, install specific package.

    Attributes:
        name: Package name
        version: Package version to install (default to latest)
        description: Package description

        repo: Package vcs repository name
        source: Package source type

        link_pattern: Link from unarhived outputs to specific paths

        asset_pattern: Asset searching from release, regex pattern (github release)

        _lock: Package lock instance
        _source: Package source instance
    """

    name: str
    version: Optional[str] = None
    description: Optional[str] = None

    repo: Optional[str] = None
    source: PackageSource = PackageSource.NONE

    link_pattern: Dict[str, str] = {}

    asset_pattern: Optional[str] = None

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

    async def download_url(self) -> str:
        """Returns url to download bin"""
        return await self._source.download_url()

    @property
    def package_out_dir(self):
        return os.path.join(INSTALL_DIR, self.name, 'out')

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
            download_url = await self.download_url()

            # Download file
            async with request.session.get(download_url) as response:
                chunks: bytes = b''
                content_length = int(response.headers.get('Content-Length', '0')) or None

                download_filename = format_download_filename(response.headers.get('Content-Disposition'), download_url)
                download_file_dir = os.path.join(INSTALL_DIR, self.name, download_filename)

                dynamic.add_message(message.get_package_download(download_filename, content_length))
                dynamic.add_message(message.get_package_download_progress(content_length, 0))

                chunk_unit = int(content_length / 100) if content_length else 1024
                async for chunk in response.content.iter_chunked(chunk_unit):
                    chunks += chunk
                    dynamic.update_message(message.get_package_download_progress(content_length, len(chunks)))

                async with AsyncPath(download_file_dir).open(mode='wb', encoding=None, errors=None,
                                                             newline=None) as file:
                    file: AsyncFile
                    await file.write(chunks)

                dynamic.update_message(message.get_package_download_progress(finish=True))

            dynamic.add_message(message.get_package_install_file(self.link_pattern))

            # Extract and install with glob pattern
            await unarchive_file(download_file_dir, self.package_out_dir)
            # TODO(sudosubin): Remove previous installed symlinks, read from lock file
            await create_symlink(self.package_out_dir, self.link_pattern)

            # Postinstall hook
            await self.postinstall()

            # Write lock
            await self._lock.write(version=next_version, files=tuple(self.link_pattern.values()))

            dynamic.update_heading(_get_heading(finish=True))

    async def postinstall(self):
        """Implemented from each collection, onlt if needed"""
        pass

    @classmethod
    async def collection(cls):
        await load_collection()
        return cls.__subclasses__()
