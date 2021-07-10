import os

from aiopath import AsyncPath

from package import Package
from package.source import PackageSource
from utils.glob import create_symlink_base


class FiraMono(Package):
    name = 'fonts/firamono'
    description = 'Mozilla\'s new typeface, used in Firefox OS'

    repo = 'ryanoasis/nerd-fonts'
    source = PackageSource.GITHUB_RELEASE

    asset_pattern = r'FiraMono\.zip'

    async def postinstall(self):
        allow_list = [
            'Fira Mono Bold Nerd Font Complete Mono.otf',
            'Fira Mono Medium Nerd Font Complete Mono.otf',
            'Fira Mono Regular Nerd Font Complete Mono.otf',
        ]

        home_font_dir = os.path.join(os.path.expanduser('~'), '.local/share/fonts/FiraMono')
        await AsyncPath(home_font_dir).mkdir(parents=True, exist_ok=True)

        for file_name in allow_list:
            file_dir = os.path.join(self.package_out_dir, file_name)
            home_file_dir = os.path.join(home_font_dir, file_name)
            await create_symlink_base(target=file_dir, dest=home_file_dir)
