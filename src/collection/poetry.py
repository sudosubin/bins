import imp
import sys
from typing import Any

from aiopath import AsyncPath
from anyio import AsyncFile

from package import Package
from package.source import PackageSource
from utils.configs import BIN_DIR
from utils.glob import create_symlink_base, make_executable
from utils.request import request


class Poetry(Package):
    name = 'poetry'
    description = 'Dependency management and packaging tool in Python'

    repo = 'python-poetry/poetry'
    source = PackageSource.GITHUB_RELEASE

    if sys.platform == 'linux':
        asset_pattern = r'.*linux\.tar\.gz'
    elif sys.platform == 'darwin':
        asset_pattern = r'.*darwin\.tar\.gz'

    async def get_poetry_py(self) -> Any:
        planned_version = await self.planned_version()
        script_url = f'https://raw.githubusercontent.com/python-poetry/poetry/{planned_version}/get-poetry.py'

        response = await request.session.get(script_url)
        script_content = await response.text()

        get_poetry = imp.new_module('get-poetry')
        exec(script_content, get_poetry.__dict__)

        return get_poetry

    async def postinstall(self):
        bin_dir = AsyncPath(self.package_out_dir, 'bin')
        bin_poetry_dir = AsyncPath(bin_dir, 'poetry')
        home_poetry_dir = AsyncPath(BIN_DIR, 'poetry')

        lib_dir = AsyncPath(self.package_out_dir, 'lib', 'poetry')
        poetry_dir = AsyncPath(self.package_out_dir, 'poetry')

        # Rename ./poetry -> ./lib
        await lib_dir.mkdir(parents=True, exist_ok=True)
        await poetry_dir.rename(lib_dir)

        # Create ./bin/poetry
        await bin_poetry_dir.parent.mkdir(parents=True, exist_ok=True)
        await bin_poetry_dir.touch()

        get_poetry = await self.get_poetry_py()
        bin_poetry_content = f'#!/usr/bin/env python3\n{get_poetry.BIN}'

        async with await bin_poetry_dir.open(mode='w') as file:
            file: AsyncFile
            await file.write(bin_poetry_content)  # type: ignore

        # Post create ./bin/poetry
        await make_executable(bin_poetry_dir)
        await create_symlink_base(target=bin_poetry_dir, dest=home_poetry_dir, is_executable=True)
