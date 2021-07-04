import re
from typing import Union


def semantic_release(version: str):
    if re.match(r'^v\d', version):
        return version[1:]

    return version


def format_bytes(size: Union[int, float]) -> str:
    """Returns human readable file size"""

    size = float(size)

    KB = float(1024)  # 1024
    MB = float(KB**2)  # 1,048,576
    GB = float(KB**3)  # 1,073,741,824
    TB = float(KB**4)  # 1,099,511,627,776

    if size < KB:
        return '{0} B'.format(size)

    if size < MB:
        return '{0:.2f} KB'.format(size / KB)

    if size < GB:
        return '{0:.2f} MB'.format(size / MB)

    if size < TB:
        return '{0:.2f} GB'.format(size / GB)

    raise ValueError('File size is too large to download! ({0:.2f} GB)'.format(size / GB))
