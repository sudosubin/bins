import platform


def is_x86_64() -> bool:
    return platform.machine() == 'x86_64'


def is_i386() -> bool:
    return platform.machine() != 'x86_64'
