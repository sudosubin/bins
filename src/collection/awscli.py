import sys

from package import Package
from package.source import PackageSource


class AwsCli(Package):
    name = 'awscli'
    description = 'Universal Command Line Interface for Amazon Web Services'

    repo = 'aws/aws-cli'
    source = PackageSource.GITHUB_TAG

    bin_pattern = ['./aws/dist/aws', './aws/dist/aws_completer']

    async def download_url(self) -> str:
        if sys.platform != 'linux':
            raise ValueError('Currently linux is the only supported platform for aws-cli.')

        planned_version = await self.planned_version()
        return f'https://awscli.amazonaws.com/awscli-exe-linux-x86_64-{planned_version}.zip'
