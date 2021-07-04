import os
from typing import Optional

ROOT_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

PROJECT_DIR: str = os.path.join(ROOT_DIR, 'src')
COLLECTION_DIR: str = os.path.join(PROJECT_DIR, 'collection')

INSTALL_DIR: str = os.path.join(ROOT_DIR, 'installs')
BIN_DIR: str = os.path.join(os.path.expanduser('~'), 'bin')

GITHUB_TOKEN: Optional[str] = os.environ.get('GITHUB_TOKEN')
