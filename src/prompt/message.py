import asyncio
import contextlib
import datetime

import rich
from rich.live import Live


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
