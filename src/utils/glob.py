import os
import stat
from pathlib import Path
from typing import List, Optional, Union

from aiopath import AsyncPath

from utils.configs import BIN_DIR


async def make_executable(path: Path):
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)


async def create_symlink(src_dir: Union[str, Path], glob_patterns: List[str], symlink_name: Optional[str]):
    symlink_paths: List[Path] = [path for glob_pattern in glob_patterns for path in Path(src_dir).glob(glob_pattern)]

    dest_paths: List[str] = []

    if len(symlink_paths) == 0:
        raise ValueError('No symlink paths were found!')

    # If symlink_name is specified, only one symlink available
    if symlink_name is not None and len(symlink_paths) > 1:
        raise ValueError('Only one symlink is available when symlink name is specified!')

    await AsyncPath(BIN_DIR).mkdir(parents=True, exist_ok=True)

    for target_path in symlink_paths:
        dest_path = AsyncPath(os.path.join(BIN_DIR, symlink_name or target_path.name))
        target_is_directory = target_path.is_dir()

        if not target_is_directory:
            await make_executable(target_path)

        await dest_path.unlink(missing_ok=True)
        await dest_path.symlink_to(target_path, target_is_directory=target_is_directory)

        dest_paths.append(str(dest_path))

    return dest_paths
