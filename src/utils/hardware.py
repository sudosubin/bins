import platform

is_x86_64: bool = platform.machine() == 'x86_64'

is_i386: bool = platform.machine() != 'x86_64'
