from enum import Enum, unique


@unique
class PackageSource(Enum):
    GITHUB_RELEASE = 'github-release'  # package.source.github_release
    NONE = None
