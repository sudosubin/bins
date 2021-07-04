from typing import Dict, List

from source.base import BasePackageSource
from utils.configs import GITHUB_TOKEN
from utils.formatters import semantic_release
from utils.request import request


class GitHubTagPackageSource(BasePackageSource):
    @staticmethod
    def _get_headers() -> Dict[str, str]:
        if GITHUB_TOKEN:
            return {'Authorization': f'token {GITHUB_TOKEN}'}

        return {}

    @staticmethod
    def _get_tag_version(tag: Dict) -> str:
        ref: str = tag.get('ref', '')
        version = ref.replace('refs/tags/', '')
        return semantic_release(version)

    async def planned_version(self) -> str:
        if self._planned_version is not None:
            return self._planned_version

        endpoint = f'https://api.github.com/repos/{self.package.repo}/git/refs/tags'
        data = await request.get(endpoint, headers=self._get_headers())

        # Search for latest
        if self.package.version is None:
            self._planned_version = self._get_tag_version(data[-1])
            return self._planned_version

        tag_versions: List[str] = [
            self._get_tag_version(tag) for tag in data if self.package.version == self._get_tag_version(tag)
        ]

        if len(tag_versions) != 1:
            raise ValueError(f'Correct tag for {self.package.name} ({self.package.version}) was not found! '
                             f'({len(tag_versions)} found)')

        self._planned_version = tag_versions[0]
        return self._planned_version

    async def download_url(self) -> str:
        raise ValueError('GitHub tag does not have any url to download.')
