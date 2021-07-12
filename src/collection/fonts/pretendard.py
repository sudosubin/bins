from package import Package
from package.source import PackageSource


class Pretendard(Package):
    name = 'fonts/pretandard'
    description = 'A system-ui alternative font that can be used on any platform'

    repo = 'orioncactus/pretendard'
    source = PackageSource.GITHUB_RELEASE
    asset_pattern = r'Pretendard-.*\.zip'

    link_pattern = {'./public/static': '~/.local/share/fonts/Pretendard'}
