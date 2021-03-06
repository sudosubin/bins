import sys

from package import Package
from package.source import PackageSource
from utils import hardware


class Lokalise2(Package):
    name = 'lokalise2'
    description = 'Lokalise CLI v2'

    repo = 'lokalise/lokalise-cli-2-go'
    source = PackageSource.GITHUB_RELEASE

    if sys.platform == 'linux' and hardware.is_x86_64:
        asset_pattern = r'.*linux_x86_64.*'
    elif sys.platform == 'linux' and hardware.is_i386:
        asset_pattern = r'.*linux_i386.*'
    elif sys.platform == 'darwin':
        asset_pattern = r'.*darwin.*'

    bin_pattern = ['./lokalise2']
    link_pattern = {'./lokalise2': '$BIN_DIR/lokalise2'}
