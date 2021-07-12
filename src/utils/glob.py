import os
import stat
from pathlib import Path
from typing import Union


async def make_executable(path: Union[str, Path]):
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)
