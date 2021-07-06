import sys

from package import Package
from package.source import PackageSource


class Ll(Package):
    name = 'll'
    description = 'A more informative `ls`, based on `k`'

    repo = 'OldhamMade/ll'
    source = PackageSource.GITHUB_RELEASE

    if sys.platform == 'linux':
        asset_pattern = r'.*ubuntu.*'
    elif sys.platform == 'darwin':
        asset_pattern = r'.*macos.*'

    bin_pattern = './ll'
