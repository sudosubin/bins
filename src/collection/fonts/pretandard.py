import os

from aiopath import AsyncPath

from package import Package
from package.source import PackageSource
from utils.glob import create_symlink_base


class Pretandard(Package):
    name = 'fonts/pretandard'
    description = 'A system-ui alternative font that can be used on any platform'

    repo = 'orioncactus/pretendard'
    source = PackageSource.GITHUB_RELEASE

    asset_pattern = r'Pretendard-.*\.zip'

    async def postinstall(self):
        bin_font_dir = os.path.join(self.package_out_dir, 'public', 'static')
        home_font_dir = AsyncPath(os.path.expanduser('~'), '.local/share/fonts/Pretandard')
        await home_font_dir.parent.mkdir(parents=True, exist_ok=True)

        await create_symlink_base(target=bin_font_dir, dest=home_font_dir)
