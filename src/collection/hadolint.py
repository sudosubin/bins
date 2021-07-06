import sys

from package import Package
from package.source import PackageSource


class Hadolint(Package):
    name = 'hadolint'
    description = 'Dockerfile linter, validate inline bash, written in Haskell'

    repo = 'hadolint/hadolint'
    source = PackageSource.GITHUB_RELEASE

    if sys.platform == 'linux':
        asset_pattern = r'.*Linux.*'
    elif sys.platform == 'darwin':
        asset_pattern = r'.*Darwin.*'

    bin_name = 'hadolint'
    bin_pattern = './hadolint-*'
