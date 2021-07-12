import sys

from package import Package
from package.source import PackageSource


class AwsVault(Package):
    name = 'aws-vault'
    description = 'A vault for securely storing and accessing AWS credentials in development environments'

    repo = '99designs/aws-vault'
    source = PackageSource.GITHUB_RELEASE

    if sys.platform == 'linux':
        asset_pattern = r'aws-vault-linux-amd64'

    bin_pattern = ['./aws-vault-*']
    link_pattern = {'./aws-vault-*': '$BIN_DIR/aws-vault'}
