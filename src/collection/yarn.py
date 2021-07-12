from package import Package
from package.source import PackageSource


class Yarn(Package):
    name = 'yarn'
    description = 'Fast, reliable, and secure dependency management'

    repo = 'yarnpkg/yarn'
    source = PackageSource.GITHUB_RELEASE
    asset_pattern = r'.*\.tar\.gz$'

    bin_pattern = ['./*/bin/yarn']
    link_pattern = {'./*/bin/yarn': '$BIN_DIR/yarn'}
