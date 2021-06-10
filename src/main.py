import fire

from command import Command
from package.load import load_collection


if __name__ == '__main__':
    # preload collection
    load_collection()

    fire.Fire(Command)
