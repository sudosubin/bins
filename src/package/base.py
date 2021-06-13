from typing import Optional

from package.source import PackageSource
from package.source import github_release


class Package(object):
    """Download, install specific package.

    Attributes:
        name(required): Package name
        version: Package version to install
        description: Package description

        repo: Package vcs repository name
        source: Package source type

        asset_pattern: Asset searching from release, regex pattern (github release)
        bin_pattern: Bin searching from unarchived output, regex pattern (github release)
    """

    name: str
    version: str = 'latest'
    description: Optional[str] = None

    repo: Optional[str] = None
    source: PackageSource = PackageSource.NONE

    asset_pattern: Optional[str] = None
    bin_pattern: Optional[str] = None

    @classmethod
    def collections(cls):
        return cls.__subclasses__()

    @classmethod
    async def check(cls):
        pass

    @classmethod
    async def install(cls):
        if cls.source is PackageSource.GITHUB_RELEASE:
            if not cls.repo:
                raise ValueError(f'{cls.name} needs `repo` attribute!')

            await github_release.download_assets(cls.repo, cls.version, cls.asset_pattern)
