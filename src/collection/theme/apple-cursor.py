from package import Package
from package.source import PackageSource


class AppleCursor(Package):
    name = 'theme/apple-cursor'
    description = 'macOS Cursor Theme'

    repo = 'ful1e5/apple_cursor'
    source = PackageSource.GITHUB_RELEASE
    asset_pattern = r'.*macOSBigSur.tar.gz'

    link_pattern = {'./macOSBigSur': '~/.icons/apple-cursor'}
