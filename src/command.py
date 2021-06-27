import sys

from console import live, message
from package import Package
from package.status import PackageStatus
from package.utils.load import load_packages_removal
from package.utils.removal import remove_package


class Command(object):
    """Package manager commands.

    Attributes:
        packages: Package instances
    """
    @classmethod
    async def collect_packages(cls):
        """Collect packages to install, update, or removal"""

        with live.print_package_collecting():
            # Instantiate packages
            packages = [package() for package in await Package.collection()]

            # Package statuses
            installs = [p for p in packages if await p.status() is PackageStatus.INSTALL]
            updates = [p for p in packages if await p.status() is PackageStatus.UPDATE]
            removals = await load_packages_removal()

        message.print_package_operations(len(installs), len(updates), len(removals))

        return installs, updates, removals

    @classmethod
    async def check(cls):
        """Check and print packages to install, update, or remove"""

        installs, updates, removals = await cls.collect_packages()
        message.print_empty_line()

        for package in installs + updates:
            await package.check()

        for package in removals:
            message.print_package_check(package['name'], package['version'], None)

    @classmethod
    async def install(cls):
        """Install, update, or remove packages"""

        installs, updates, removals = await cls.collect_packages()

        for package in installs + updates:
            await package.install()

        for package in removals:
            await remove_package(package['name'], package['version'])

    @classmethod
    async def execute(cls):
        if 'check' in sys.argv:
            await cls.check()

        if 'install' in sys.argv:
            await cls.install()
