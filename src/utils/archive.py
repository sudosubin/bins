import shutil
from pathlib import Path
from typing import Union

import aioshutil
from aiopath import AsyncPath


def is_archive_file(file_name: str) -> bool:
    for _, exts, _ in shutil.get_unpack_formats():
        for extension in exts:
            if file_name.endswith(extension):
                return True

    return False


async def unarchive_file(file_dir: str, extract_dir: Union[str, Path]):
    """Unarchive or copy file. It cleans extract_dir first."""

    # Clean and create extract_dir
    await aioshutil.rmtree(extract_dir, ignore_errors=True)
    await AsyncPath(extract_dir).mkdir(parents=True, exist_ok=True)

    if is_archive_file(file_dir):
        await aioshutil.unpack_archive(file_dir, extract_dir)
        await AsyncPath(file_dir).unlink()
    else:
        file_name = file_dir.split('/')[-1]
        await aioshutil.move(file_dir, AsyncPath(extract_dir, file_name))
