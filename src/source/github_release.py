import re
from typing import Dict, List

from source.base import BasePackageSource
from utils.configs import GITHUB_TOKEN
from utils.formatters import semantic_release
from utils.request import request


class GitHubReleasePackageSource(BasePackageSource):
    @staticmethod
    def _get_headers() -> Dict[str, str]:
        if GITHUB_TOKEN:
            return {'Authorization': f'token {GITHUB_TOKEN}'}

        return {}

    async def planned_version(self) -> str:
        if self._planned_version is not None:
            return self._planned_version

        # Search for latest
        if self.package.version is None:
            endpoint = f'https://api.github.com/repos/{self.package.repo}/releases/latest'
            data = await request.get(endpoint, headers=self._get_headers())

            tag_name: str = data['tag_name']
            self._planned_version = semantic_release(tag_name)
            return self._planned_version

        endpoint = f'https://api.github.com/repos/{self.package.repo}/releases'
        data = await request.get(endpoint, headers=self._get_headers())

        tag_names: List[str] = [
            release['tag_name'] for release in data if self.package.version == semantic_release(release['tag_name'])
        ]

        if len(tag_names) != 1:
            raise ValueError(f'Correct release for {self.package.name} ({self.package.version}) was not found! '
                             f'({len(tag_names)} found)')

        self._planned_version = semantic_release(tag_names[0])
        return self._planned_version

    async def download_url(self) -> str:
        planned_version = await self.planned_version()

        endpoint = f'https://api.github.com/repos/{self.package.repo}/releases'
        data = await request.get(endpoint, headers=self._get_headers())

        release = next((release for release in data if planned_version == semantic_release(release['tag_name'])))
        assets = [asset for asset in release['assets'] if re.match(self.package.asset_pattern or '', asset['name'])]

        if len(assets) != 1:
            raise ValueError(f'Correct asset for {self.package.name} ({self.package.version}) was not found! '
                             f'({len(assets)} found)')

        return assets[0]['browser_download_url']
