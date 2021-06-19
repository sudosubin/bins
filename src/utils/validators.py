import re


def semantic_release(version: str):
    if re.match(r'^v\d', version):
        return version[1:]

    return version
