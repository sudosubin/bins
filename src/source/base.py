from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from package import Package


class BasePackageSource(object):
    """Control package from specific source.

    Attributes:
        package: Package object to access package's information

        _planned_version: Memory cache for planned_version
    """

    package: 'Package'

    _planned_version: Optional[str] = None

    def __init__(self, package: 'Package'):
        self.package = package

    async def planned_version(self) -> str:
        raise NotImplementedError
