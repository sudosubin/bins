from typing import Dict, Optional

import rich
from rich.progress import ProgressBar
from rich.style import Style
from rich.table import Table

from package.status import PackageStatus
from utils.formatters import format_bytes


def indent(size: int) -> str:
    return ' ' * size


def print_empty_line():
    rich.print()


def print_package_operations(install_count: int, update_count: int, removal_count: int):
    rich.print(f'[bold]Package operations[/bold]: '
               f'[not bold blue]{install_count}[/not bold blue] installs, '
               f'[not bold blue]{update_count}[/not bold blue] updates, '
               f'[not bold blue]{removal_count}[/not bold blue] removals')


def print_package_check(name: str, prev_version: Optional[str], next_version: Optional[str]):
    def _package_status():
        if prev_version is None:
            return PackageStatus.INSTALL.value.lower()

        if next_version is None:
            return PackageStatus.REMOVAL.value.lower()

        return PackageStatus.UPDATE.value.lower()

    versions = format_package_versions(prev_version, next_version)
    rich.print(f'{indent(2)}[green]•[/green] Planned for {_package_status()} [cyan]{name}[/cyan] {versions}')


def get_package_install(name: str, prev_version: Optional[str], next_version: Optional[str], finish: bool) -> str:
    def _package_status():
        if prev_version is None:
            return 'Installing'

        if next_version is None:
            return 'Removing'

        return 'Updating'

    dot_color = 'green' if finish else 'blue'
    versions = format_package_versions(prev_version, next_version)

    return f'\n{indent(2)}[{dot_color}]•[/{dot_color}] {_package_status()} [cyan]{name}[/cyan] {versions}'


def get_package_install_file(link_pattern: Dict[str, str]) -> str:
    if not link_pattern:
        return f'{indent(6)}[yellow]Warning: You did not specify any pattern to link![/yellow]'

    return f'{indent(6)}Installing {", ".join(link_pattern.keys())}'


def get_package_download(file_name: str, file_size: Optional[int]) -> str:
    readable_size = format_bytes(file_size) if file_size else 'unknown'
    return f'{indent(6)}Downloading {file_name} ({readable_size})'


def get_package_download_progress(total_size: Optional[int] = None, completed_size: int = 0, finish: bool = False):
    bar_styles = {
        'complete_style': Style(color='default'),
        'finished_style': Style(color='green'),
        'pulse_style': Style(color='white'),
    }

    if finish:
        bar = ProgressBar(total=100, completed=100, width=40, **bar_styles)
    elif total_size is None:
        bar = ProgressBar(total=100, completed=0, width=40, pulse=True, **bar_styles)
    else:
        bar = ProgressBar(total=total_size, completed=completed_size, width=40, **bar_styles)

    table = Table.grid(padding=(0, 0))
    table.add_row(indent(8), bar, '{:4.0f}%'.format(bar.percentage_completed))

    return table


def format_package_versions(prev_version: Optional[str], next_version=Optional[str]) -> str:
    def _get_prev_version() -> str:
        if prev_version is None:
            return 'none'

        return f'[not bold default]{prev_version}[/not bold default]'

    def _get_next_version() -> str:
        if next_version is None:
            return '[not bold yellow]none[/not bold yellow]'

        return f'[not bold green]{next_version}[/not bold green]'

    return f'[not bold default]({_get_prev_version()} → {_get_next_version()})[/not bold default]'
