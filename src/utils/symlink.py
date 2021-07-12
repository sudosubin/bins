import os
import stat
from pathlib import Path
from typing import Dict, List, Tuple, Union

from aiopath import AsyncPath

from utils.configs import BIN_DIR


async def get_symlink_path(src_dir: Union[str, Path], pattern: str) -> AsyncPath:
    candidates: List[AsyncPath] = [path async for path in AsyncPath(src_dir).glob(pattern)]

    if len(candidates) != 1:
        raise ValueError('Multiple src file found during linking files!')

    return candidates[0]


async def make_executable(src_dir: Union[str, Path], bin_pattern: List[str]):

    for path in bin_pattern:
        symlink_path = await get_symlink_path(src_dir, path)
        st = os.stat(symlink_path)
        os.chmod(symlink_path, st.st_mode | stat.S_IEXEC)


async def create_symlink(src_dir: Union[str, Path], link_pattern: Dict[str, str]):
    symlink_pattern: List[Tuple[AsyncPath, AsyncPath]] = []

    # Translate link_pattern to symlink_pattern
    for key, value in link_pattern.items():
        symlink_key = await get_symlink_path(src_dir, key)
        symlink_value = AsyncPath(os.path.expanduser(value).replace('$BIN_DIR', BIN_DIR))

        symlink_pattern.append((symlink_key, symlink_value))

    # Link files
    for src_path, dest_path in symlink_pattern:
        await dest_path.parent.mkdir(parents=True, exist_ok=True)

        is_directory = await src_path.is_dir()

        await dest_path.unlink(missing_ok=True)
        await dest_path.symlink_to(src_path, target_is_directory=is_directory)
