import asyncio
import os

from aiopath import AsyncPath

from package import Package
from package.source import PackageSource


class Pipenv(Package):
    name = 'pipenv'
    description = 'Python Development Workflow for Humans'

    repo = 'pypa/pipenv'
    source = PackageSource.GITHUB_TAG

    bin_pattern = ['./*/.venv/bin/pipenv']
    link_pattern = {'./*/.venv/bin/pipenv': '$BIN_DIR/pipenv'}

    async def preinstall(self):
        # Use top directory
        pipenv_dirs = [path async for path in AsyncPath(self.package_out_dir).iterdir() if await path.is_dir()]

        if len(pipenv_dirs) != 1:
            raise ValueError(f'Pipenv has multiple root folders! ({len(pipenv_dirs)})')

        pipenv_dir = str(pipenv_dirs[0])
        venv_dir = os.path.join(pipenv_dir, '.venv')
        venv_pip_dir = os.path.join(venv_dir, 'bin', 'pip')

        proc = await asyncio.create_subprocess_shell(
            f'/usr/bin/python3 -m venv {venv_dir} && {venv_pip_dir} install -q {pipenv_dir}',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        await proc.wait()
