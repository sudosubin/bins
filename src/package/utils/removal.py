# flake8: noqa
import os
from typing import Dict, List

import aioshutil
from aiopath import AsyncPath
from rich.live import Live

from console import message
from console.dynamic import DynamicConsole
from lock import PackageLock
from utils.configs import BIN_DIR, INSTALL_DIR


async def check_package(name: str, version: str):
    """Remove installed package check"""
    message.print_package_check(name, version, None)


async def remove_package(name: str, version: str):
    """Remove installed package from local"""
    def _get_heading(finish: bool = False):
        return message.get_package_install(name, version, None, finish=finish)

    with DynamicConsole(_get_heading()) as dynamic:
        package_dir = AsyncPath(os.path.join(INSTALL_DIR, name))

        lock_file = await PackageLock(name).read()
        lock_bins: List[str] = lock_file.get('bins', [])

        for lock_bin in lock_bins:
            # TODO(sudosubin): Remove local installed files together

            # bin_path = os.path.join(BIN_DIR)
            # await AsyncPath(os.)

            pass

        # await aioshutil.rmtree(package_dir)

        dynamic.update_heading(_get_heading(finish=True))
