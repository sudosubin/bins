import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
PROJECT_DIR = os.path.join(ROOT_DIR, 'src')

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', None)
