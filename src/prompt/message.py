import asyncio
import contextlib
import datetime
from typing import Optional

import rich
from rich.live import Live

from package.status import PackageStatus


@contextlib.contextmanager
def print_package_collecting():
    start_at = datetime.datetime.now()

    def _get_message():
        seconds = (datetime.datetime.now() - start_at).total_seconds()
        duration = '{:.1f}'.format(round(seconds, 2))
        return f'[blue]Collecting packages...[/blue] [not bold black]({duration}s)[/not bold black]'

    with Live(_get_message()) as live:

        async def _update_message():
            while True:
                live.update(_get_message(), refresh=True)
                await asyncio.sleep(0.1)

        asyncio.create_task(_update_message())
        yield

    # Empty line after all output
    rich.print()


def print_package_operations(install_count: int, update_count: int, removal_count: int):
    rich.print(f'[bold]Package operations[/bold]: '
               f'[not bold blue]{install_count}[/not bold blue] installs, '
               f'[not bold blue]{update_count}[/not bold blue] updates, '
               f'[not bold blue]{removal_count}[/not bold blue] removals\n')


def _format_version(version: Optional[str]) -> str:
    if version is None:
        return '[not bold yellow]none[/not bold yellow]'

    return f'[not bold default]{version}[/not bold default]'


def print_package_check(name: str, prev_version: Optional[str], next_version: Optional[str]):
    def package_status():
        if prev_version is None:
            return PackageStatus.INSTALL.value.lower()

        if next_version is None:
            return PackageStatus.REMOVAL.value.lower()

        return PackageStatus.UPDATE.value.lower()

    rich.print(f'  [green]•[/green] Planned for {package_status()} [cyan]{name}[/cyan] '
               f'[not bold]({_format_version(prev_version)} → {_format_version(next_version)})[/not bold]')
