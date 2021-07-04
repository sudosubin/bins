import sys

from package import Package
from package.source import PackageSource
from utils import hardware


class Gh(Package):
    name = 'gh'
    description = 'GitHub\'s official command line tool'

    repo = 'cli/cli'
    source = PackageSource.GITHUB_RELEASE

    if sys.platform == 'linux' and hardware.is_x86_64:
        asset_pattern = r'.*linux_amd64\.tar\.gz'
    elif sys.platform == 'linux' and hardware.is_i386:
        asset_pattern = r'.*linux_386\.tar\.gz'
    elif sys.platform == 'darwin':
        asset_pattern = r'.*macOS_amd64\.tar\.gz'

    bin_pattern = './**/bin/gh'
