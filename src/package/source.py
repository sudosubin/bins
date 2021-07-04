from enum import Enum, unique

from source.github_release import GitHubReleasePackageSource


@unique
class PackageSource(Enum):
    GITHUB_RELEASE = GitHubReleasePackageSource
    NONE = None
