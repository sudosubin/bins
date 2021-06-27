import re
import shutil


def semantic_release(version: str):
    if re.match(r'^v\d', version):
        return version[1:]

    return version


def is_unpackable(file_name: str) -> bool:
    for _, exts, _ in shutil.get_unpack_formats():
        for extension in exts:
            if file_name.endswith(extension):
                return True

    return False
