import sys

from package import Package
from package.source import PackageSource
from utils import hardware


class Kubectl(Package):
    name = 'kubectl'
    description = 'Kubernetes command-line tool allows to run commands against Kubernetes clusters'

    repo = 'kubernetes/kubernetes'
    source = PackageSource.GITHUB_RELEASE

    bin_pattern = './kubectl'

    async def download_url(self) -> str:
        arch = 'amd64' if hardware.is_x86_64 else '386'
        planned_version = await self.planned_version()
        return f'https://dl.k8s.io/release/v{planned_version}/bin/{sys.platform}/{arch}/kubectl'
