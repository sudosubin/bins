import sys

from package import Package


class Command(object):
    """Package manager commands."""
    @staticmethod
    async def check():
        print('Check')

        for package in Package.collections():
            await package.check()

    @staticmethod
    async def install():
        print('Install')

        for package in Package.collections():
            await package.install()

    @classmethod
    async def run(cls):
        if 'check' in sys.argv:
            await cls.check()

        if 'install' in sys.argv:
            await cls.install()
