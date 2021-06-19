import sys
from typing import Sequence

import rich

from package import Package
from package.load import load_packages_removal
from package.status import PackageStatus
from prompt import message


class Command(object):
    """Package manager commands.

    Attributes:
        packages: Package instances
    """

    packages: Sequence[Package]

    @classmethod
    async def init(cls):
        """Common jobs for check, install packages"""

        message.print_package_collecting()

        # Instantiate packages
        cls.packages = [package() for package in await Package.collection()]

        # Package statuses
        package_statuses = [await package.status() for package in cls.packages]
        install_count = len(tuple(filter(lambda x: x is PackageStatus.INSTALL, package_statuses)))
        update_count = len(tuple(filter(lambda x: x is PackageStatus.UPDATE, package_statuses)))
        removal_count = len(await load_packages_removal())

        message.print_package_operations(install_count, update_count, removal_count)

    @classmethod
    async def check(cls):
        for package in cls.packages:
            await package.check()

    @classmethod
    async def install(cls):
        for package in cls.packages:
            await package.install()

    @classmethod
    async def execute(cls):
        await cls.init()

        if 'check' in sys.argv:
            await cls.check()

        if 'install' in sys.argv:
            await cls.install()
