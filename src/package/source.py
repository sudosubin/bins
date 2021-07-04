from enum import Enum, unique

from source.github_release import GitHubReleasePackageSource
from source.github_tag import GitHubTagPackageSource


@unique
class PackageSource(Enum):
    GITHUB_RELEASE = GitHubReleasePackageSource
    GITHUB_TAG = GitHubTagPackageSource
    NONE = None
