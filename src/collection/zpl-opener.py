import os

from aiopath import AsyncPath

from package import Package
from package.source import PackageSource
from utils.glob import create_symlink_base


class ZplOpener(Package):
    name = 'zpl-opener'
    description = 'Open zeplin app uri in your default browser'

    repo = 'sudosubin/zeplin-uri-opener'
    source = PackageSource.GITHUB_TAG

    bin_pattern = './**/src/zpl-open'

    async def postinstall(self):
        # Consider parent dir
        project_dirs = [path async for path in AsyncPath(self.package_out_dir).iterdir() if await path.is_dir()]

        if len(project_dirs) != 1:
            raise ValueError(f'ZplOpener has multiple root folders! ({len(project_dirs)})')

        project_dir = str(project_dirs[0]).strip()

        bin_desktop_dir = AsyncPath(project_dir, 'src', 'zpl-opener.desktop')
        home_desktop_dir = AsyncPath(os.path.expanduser('~'), '.local/share/applications/zpl-opener.desktop')
        await AsyncPath(home_desktop_dir).parent.mkdir(parents=True, exist_ok=True)

        await create_symlink_base(target=bin_desktop_dir, dest=home_desktop_dir)
