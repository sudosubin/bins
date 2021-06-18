import sys
from typing import Sequence

from package import Package


class Command(object):
    """Package manager commands.

    Attributes:
        packages:
    """

    packages: Sequence[Package]

    @classmethod
    async def init(cls):
        """Common jobs for check, install packages"""

        # Instantiate packages
        cls.packages = [await package.create() for package in await Package.collection()]

    @classmethod
    async def check(cls):
        for package in await Package.collection():
            await package.check()

    @classmethod
    async def install(cls):
        for package in await Package.collection():
            await package.install()

    @classmethod
    async def execute(cls):
        await cls.init()

        if 'check' in sys.argv:
            await cls.check()

        if 'install' in sys.argv:
            await cls.install()
