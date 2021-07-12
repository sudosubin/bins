import sys

from package import Package
from package.source import PackageSource
from utils import hardware


class Act(Package):
    name = 'act'
    description = 'Run your GitHub Actions locally'

    repo = 'nektos/act'
    source = PackageSource.GITHUB_RELEASE

    if sys.platform == 'linux' and hardware.is_x86_64:
        asset_pattern = r'act_Linux_x86_64\.tar\.gz'
    elif sys.platform == 'linux' and hardware.is_i386:
        asset_pattern = r'act_Linux_i386\.tar\.gz'
    elif sys.platform == 'darwin':
        asset_pattern = r'act_Darwin_x86_64\.tar\.gz'

    bin_pattern = ['./act']
    link_pattern = {'./act': '$BIN_DIR/act'}
