from typing import Optional

from package.load import load_collection
from package.lock import PackageLock
from package.source import PackageSource
from package.status import PackageStatus
from source.base import BasePackageSource


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

    async def planned_version(self) -> str:
        """Returns specific version to install"""

        return await self._source.planned_version()

    async def installed_version(self) -> Optional[str]:
        """Returns current installed package's version or None"""

        lock_content = await self._lock.read()
        return lock_content.get('version')

    async def status(self) -> PackageStatus:
        """Returns package's status: install, update, removal, none"""

        planned_version = await self.planned_version()
        installed_version = await self.installed_version()

        if planned_version is None:
            raise ValueError(f'{self.name}\'s source fetching might failed!')

        if installed_version is None:
            return PackageStatus.INSTALL

        if planned_version != installed_version:
            return PackageStatus.UPDATE

        return PackageStatus.NONE

    async def check(self):
        """Get current installed version, and a version to install"""

        print(await self.planned_version())
        print(await self.installed_version())

    async def install(self):
        pass

    @classmethod
    async def collection(cls):
        await load_collection()
        return cls.__subclasses__()
