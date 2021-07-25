from typing import Dict, List, Optional

from source.base import BasePackageSource
from utils.configs import GITHUB_TOKEN
from utils.formatters import semantic_release
from utils.request import request


class GitHubTagPackageSource(BasePackageSource):
    _planned_version_raw: Optional[Dict] = None

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        if GITHUB_TOKEN:
            return {'Authorization': f'token {GITHUB_TOKEN}'}

        return {}

    @staticmethod
    def _get_tag_version(tag: Dict) -> str:
        tag_name = tag.get('name', '')
        return semantic_release(tag_name)

    async def planned_version_raw(self) -> Dict:
        if self._planned_version_raw is not None:
            return self._planned_version_raw

        endpoint = f'https://api.github.com/repos/{self.package.repo}/tags'
        data: List[Dict] = await request.get(endpoint, headers=self._get_headers())
        data = [item for item in data if semantic_release(item['name'])[0].isdigit()]

        # Search for latest
        if self.package.version is None:
            self._planned_version_raw = data[0]
            return self._planned_version_raw

        tag_versions: List[Dict] = [tag for tag in data if self.package.version == self._get_tag_version(tag)]

        if len(tag_versions) != 1:
            raise ValueError(f'Correct tag for {self.package.name} ({self.package.version}) was not found! '
                             f'({len(tag_versions)} found)')

        self._planned_version_raw = tag_versions[0]
        return self._planned_version_raw

    async def planned_version(self) -> str:
        if self._planned_version is not None:
            return self._planned_version

        planned_version_raw = await self.planned_version_raw()
        self._planned_version = self._get_tag_version(planned_version_raw)
        return self._planned_version

    async def download_url(self) -> str:
        planned_version_raw = await self.planned_version_raw()
        return planned_version_raw.get('tarball_url', '')
