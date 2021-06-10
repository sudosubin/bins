import importlib
import os

from utils.configs import PROJECT_DIR


def load_collection():
    """Preload all collection classes."""

    for name in os.listdir(os.path.join(PROJECT_DIR, 'collection')):
        if not name.endswith('.py'):
            continue

        module = name.replace('.py', '')
        importlib.import_module(f'collection.{module}')
