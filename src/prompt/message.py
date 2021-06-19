import rich


def print_package_collecting():
    rich.print('[blue]Collecting packages\n')


def print_package_operations(install_count: int, update_count: int, removal_count: int):
    rich.print(f'[bold]Package operations[/bold]: '
               f'[not bold blue]{install_count}[/not bold blue] installs, '
               f'[not bold blue]{update_count}[/not bold blue] updates, '
               f'[not bold blue]{removal_count}[/not bold blue] removals\n')
