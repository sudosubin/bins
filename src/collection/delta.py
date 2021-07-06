import sys

from package import Package
from package.source import PackageSource
from utils import hardware


class Delta(Package):
    name = 'delta'
    description = 'A viewer for git and diff output'

    repo = 'dandavison/delta'
    source = PackageSource.GITHUB_RELEASE

    if sys.platform == 'linux' and hardware.is_x86_64:
        asset_pattern = r'.*x86_64-unknown-linux-gnu\.tar\.gz'
    elif sys.platform == 'linux' and hardware.is_i386:
        asset_pattern = r'.*i686-unknown-linux-gnu\.tar\.gz'
    elif sys.platform == 'darwin':
        asset_pattern = r'.*darwin\.tar\.gz'

    bin_pattern = './**/delta'
