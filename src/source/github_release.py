from typing import Dict, List

from source.base import BasePackageSource
from utils.configs import GITHUB_TOKEN
from utils.request import request
from utils.validators import semantic_release


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
            release['tag_name'] for release in data
            if (release['tag_name'] == self.package.version) or (release['tag_name'] == f'v{self.package.version}')
        ]

        if len(tag_names) != 1:
            raise ValueError(f'Release for {self.package.name} ({self.package.version}) was not found!')

        self._planned_version = semantic_release(tag_names[0])
        return self._planned_version
