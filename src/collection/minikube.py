import sys

from package import Package
from package.source import PackageSource
from utils import hardware


class Minikube(Package):
    name = 'minikube'
    description = 'Local Kubernetes, focusing on making it easy to learn and develop for Kubernetes'

    repo = 'kubernetes/minikube'
    source = PackageSource.GITHUB_RELEASE

    bin_name = 'minikube'
    bin_pattern = './minikube-*'

    async def download_url(self) -> str:
        arch = 'amd64' if hardware.is_x86_64 else '386'
        planned_version = await self.planned_version()
        return f'https://storage.googleapis.com/minikube/releases/v{planned_version}/minikube-{sys.platform}-{arch}'
