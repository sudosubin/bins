from package import Package
from package.source import PackageSource


class FiraMono(Package):
    name = 'fonts/firamono'
    description = 'Mozilla\'s new typeface, used in Firefox OS'

    repo = 'ryanoasis/nerd-fonts'
    source = PackageSource.GITHUB_RELEASE
    asset_pattern = r'FiraMono\.zip'

    link_pattern = {
        './Fira Mono Bold Nerd Font Complete Mono.otf':
        '~/.local/share/fonts/FiraMono/Fira Mono Bold Nerd Font Complete Mono.otf',
        './Fira Mono Medium Nerd Font Complete Mono.otf':
        '~/.local/share/fonts/FiraMono/Fira Mono Medium Nerd Font Complete Mono.otf',
        './Fira Mono Regular Nerd Font Complete Mono.otf':
        '~/.local/share/fonts/FiraMono/Fira Mono Regular Nerd Font Complete Mono.otf'
    }
