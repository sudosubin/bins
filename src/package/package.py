from typing import Optional


class Package(object):
    """Download, install specific package.

    Attributes:
        description: Package description
        repo:
    """

    description: Optional[str] = None

    @classmethod
    def collections(cls):
        return cls.__subclasses__()
