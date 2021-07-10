import asyncio
import os

from aiopath import AsyncPath

from package import Package
from package.source import PackageSource
from utils.configs import BIN_DIR
from utils.glob import create_symlink_base


class Pipenv(Package):
    name = 'pipenv'
    description = 'Python Development Workflow for Humans'

    repo = 'pypa/pipenv'
    source = PackageSource.GITHUB_TAG

    async def postinstall(self):
        # Remove parent dir
        pipenv_dirs = [path async for path in AsyncPath(self.package_out_dir).iterdir() if await path.is_dir()]

        if len(pipenv_dirs) != 1:
            raise ValueError(f'Pipenv has multiple root folders! ({len(pipenv_dirs)})')

        pipenv_dir = str(pipenv_dirs[0]).strip()

        venv_dir = os.path.join(pipenv_dir, '.venv')
        venv_pip_dir = os.path.join(venv_dir, 'bin', 'pip')

        bin_pipenv_dir = os.path.join(venv_dir, 'bin', 'pipenv')
        home_pipenv_dir = os.path.join(BIN_DIR, 'pipenv')

        proc = await asyncio.create_subprocess_shell(
            f'/usr/bin/python3 -m venv {venv_dir} && {venv_pip_dir} install -q {pipenv_dir}',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        await proc.wait()

        # Post create ./.venv/bin/pipenv
        await create_symlink_base(target=bin_pipenv_dir, dest=home_pipenv_dir, is_executable=True)
