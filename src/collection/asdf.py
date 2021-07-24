from package import Package
from package.source import PackageSource


class Asdf(Package):
    name = 'asdf'
    description = 'Extendable version manager with support for Ruby, Node.js, Elixir, Erlang & more'

    repo = 'asdf-vm/asdf'
    source = PackageSource.GITHUB_TAG

    link_pattern = {'./*': '$BIN_DIR/asdf'}
