# Bins

![python](https://img.shields.io/badge/python-3.8%20%7C%203.9-blue.svg)

Personal binary package manager, installs some useful softwares.

## Install

```sh
# install requirements
apt install python3 python3-venv build-essential

# alias, paths
alias bins="make -f $HOME/path/to/Makefile"
export PATH="$PATH:$HOME/bin"

# install dependencies
bins prepare

# install bins
bins check
bins install
```

## Configurations

If you want to avoid github api rate limit, do below.

```properties
# .makerc
GITHUB_TOKEN=...
```

## License

Bins is [MIT Licensed](./LICENSE).
