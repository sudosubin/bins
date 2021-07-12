from package import Package
from package.source import PackageSource


class LaCapitaineIconTheme(Package):
    name = 'theme/la-capitaine-icon-theme'
    description = 'Icon pack designed to integrate with most desktop environments'

    repo = 'keeferrourke/la-capitaine-icon-theme'
    source = PackageSource.GITHUB_TAG

    link_pattern = {'./*': '~/.local/share/icons/la-capitaine-icon-theme'}
