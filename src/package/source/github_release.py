import re

from typing import Any, Dict, List, Optional

from utils.configs import GITHUB_TOKEN
from utils.request import request


def get_headers() -> Dict[str, str]:
    if GITHUB_TOKEN:
        return {'Authorization': f'token {GITHUB_TOKEN}'}
    return {}


async def get_latest_version(repo: str) -> str:
    """Get latest release version using api"""
    endpoint = f'https://api.github.com/repos/{repo}/releases/latest'
    data = await request.get(endpoint, headers=get_headers())
    return data['tag_name']


async def get_assets(repo: str, tag_name: str) -> List[Dict[str, Any]]:
    """Get release assets with specific version"""
    endpoint = f'https://api.github.com/repos/{repo}/releases'
    data = await request.get(endpoint, headers=get_headers())
    assets = [release['assets'] for release in data if release['tag_name'] == tag_name]

    if len(assets) != 1:
        raise ValueError(f'Release for {repo} ({tag_name}) was not found!')

    return assets[0]


async def download_assets(repo: str, version: str, asset_pattern: Optional[str]):
    """Download github release assets"""
    tag_name = await get_latest_version(repo)
    assets = await get_assets(repo, tag_name)
    asset_search_pattern = asset_pattern or r'.*'

    matched = [asset for asset in assets if re.match(asset_search_pattern, asset['name'])]

    if len(matched) != 1:
        raise ValueError(f'Release for {repo} ({version}) has zero, or multiple assets!')

    # download_url = matched[0]['browser_download_url']
    print(matched[0]['browser_download_url'])
    # data = await request.get(download_url)
