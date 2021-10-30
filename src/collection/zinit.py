from package import Package
from package.source import PackageSource


class Zinit(Package):
    name = 'zinit'
    description = 'Flexible and fast Zsh plugin manager'

    repo = 'zdharma-continuum/zinit'
    source = PackageSource.GITHUB_TAG

    link_pattern = {'./*': '$BIN_DIR/zinit'}
