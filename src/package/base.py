from typing import Optional

from package.load import load_packages
from package.lock import PackageLock
from package.source import PackageSource


class Package(object):
    """Download, install specific package.

    Attributes:
        name: Package name
        version: Package version to install (default to latest)
        description: Package description

        lock: Package lock instance

        repo: Package vcs repository name
        source: Package source type

        asset_pattern: Asset searching from release, regex pattern (github release)
        bin_pattern: Bin searching from unarchived output, regex pattern (github release)
    """

    name: str
    version: Optional[str] = None
    description: Optional[str] = None

    lock: PackageLock

    repo: Optional[str] = None
    source: PackageSource = PackageSource.NONE

    asset_pattern: Optional[str] = None
    bin_pattern: Optional[str] = None

    def __init__(self):
        self.lock = PackageLock(self.name)

    async def planned_version(self) -> str:
        """Returns specific version to install"""

        if self.source is PackageSource.NONE:
            raise ValueError('Package source was not specified!')

        # TODO(sudosubin): Add version fetching operations
        source = self.source.value
        return source

    async def installed_version(self) -> Optional[str]:
        """Returns current installed package's version or None"""

        lock_content = await self.lock.read()
        return lock_content.get('version')

    async def check(self):
        """Get current installed version, and a version to install"""

        pass

    async def install(self):
        pass

    @classmethod
    async def collection(cls):
        await load_packages()
        return cls.__subclasses__()
