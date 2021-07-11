import os

from aiopath import AsyncPath

from package import Package
from package.source import PackageSource
from utils.glob import create_symlink_base


class AppleCursor(Package):
    name = 'theme/apple-cursor'
    description = 'macOS Cursor Theme'

    repo = 'ful1e5/apple_cursor'
    source = PackageSource.GITHUB_RELEASE

    asset_pattern = r'.*macOSBigSur.tar.gz'

    async def postinstall(self):
        theme_dir = AsyncPath(self.package_out_dir, 'macOSBigSur')

        home_theme_dir = AsyncPath(os.path.expanduser('~'), '.icons/apple-cursor')
        await home_theme_dir.parent.mkdir(parents=True, exist_ok=True)

        await create_symlink_base(target=theme_dir, dest=home_theme_dir)
