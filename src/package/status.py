from enum import Enum, unique


@unique
class PackageStatus(Enum):
    INSTALL = 'install'
    UPDATE = 'update'
    REMOVAL = 'removal'
    NONE = None
