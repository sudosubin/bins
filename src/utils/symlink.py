import os
from pathlib import Path
from typing import Dict, List, Tuple, Union

from aiopath import AsyncPath


async def create_symlink(src_dir: Union[str, Path], link_pattern: Dict[str, str]):
    symlink_pattern: List[Tuple[AsyncPath, AsyncPath]] = []

    # Translate link_pattern to symlink_pattern
    for key, value in link_pattern.items():
        key_candidates: List[AsyncPath] = [path async for path in AsyncPath(src_dir).glob(key)]

        if len(key_candidates) != 1:
            raise ValueError('Multiple src file found during linking files!')

        symlink_key = key_candidates[0]
        symlink_value = AsyncPath(os.path.expanduser(value))

        symlink_pattern.append((symlink_key, symlink_value))

    # Link files
    for src_path, dest_path in symlink_pattern:
        await dest_path.parent.mkdir(parents=True, exist_ok=True)

        is_directory = await src_path.is_dir()

        await dest_path.unlink(missing_ok=True)
        await dest_path.symlink_to(src_path, target_is_directory=is_directory)
