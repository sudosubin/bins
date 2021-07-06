import os
import stat
from pathlib import Path
from typing import List, Optional, Union

from aiopath import AsyncPath

from utils.configs import BIN_DIR


async def make_executable(path: Union[str, Path]):
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)


async def create_symlink_base(target: Union[str, Path], dest: Union[str, Path], is_executable: bool = False):
    dest_dir = AsyncPath(dest)
    target_is_directory = await AsyncPath(target).is_dir()

    if is_executable and not target_is_directory:
        await make_executable(target)

    await dest_dir.unlink(missing_ok=True)
    await dest_dir.symlink_to(target, target_is_directory=target_is_directory)


async def create_symlink(src_dir: Union[str, Path], glob_patterns: List[str], symlink_name: Optional[str]):
    symlink_paths: List[Path] = [path for glob_pattern in glob_patterns for path in Path(src_dir).glob(glob_pattern)]

    dest_paths: List[str] = []

    if glob_patterns and len(symlink_paths) == 0:
        raise ValueError('No symlink paths were found!')

    # If symlink_name is specified, only one symlink available
    if symlink_name is not None and len(symlink_paths) > 1:
        raise ValueError('Only one symlink is available when symlink name is specified!')

    await AsyncPath(BIN_DIR).mkdir(parents=True, exist_ok=True)

    for target in symlink_paths:
        dest = os.path.join(BIN_DIR, symlink_name or target.name)
        dest_paths.append(dest)

        await create_symlink_base(target=target, dest=dest, is_executable=True)

    return dest_paths
