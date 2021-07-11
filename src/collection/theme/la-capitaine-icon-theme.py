import os

from aiopath import AsyncPath

from package import Package
from package.source import PackageSource
from utils.glob import create_symlink_base


class LaCapitaineIconTheme(Package):
    name = 'theme/la-capitaine-icon-theme'
    description = 'Icon pack designed to integrate with most desktop environments'

    repo = 'keeferrourke/la-capitaine-icon-theme'
    source = PackageSource.GITHUB_TAG

    async def postinstall(self):
        # Consider top directory
        theme_dirs = [path async for path in AsyncPath(self.package_out_dir).iterdir() if await path.is_dir()]

        if len(theme_dirs) != 1:
            raise ValueError(f'LaCapitaineIconTheme has multiple root folders! ({len(theme_dirs)})')

        theme_dir = str(theme_dirs[0]).strip()

        home_theme_dir = AsyncPath(os.path.expanduser('~'), '.local/share/icons/la-capitaine-icon-theme')
        await home_theme_dir.parent.mkdir(parents=True, exist_ok=True)

        await create_symlink_base(target=theme_dir, dest=home_theme_dir)
