from types import TracebackType
from typing import List, Optional, Type

from rich.console import RenderableType
from rich.live import Live
from rich.table import Table


class DynamicConsole(object):
    """Creating messages with rich live object.

    Attributes:
        live: Current live instance
        messages: Multiple messages to print out
    """

    live: Live
    messages: List[RenderableType]

    def __init__(self, heading: RenderableType):
        self.live = Live(heading)
        self.messages = [heading]

    def __enter__(self) -> 'DynamicConsole':
        self.live.__enter__()
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]) -> None:
        self.live.__exit__(exc_type, exc_val, exc_tb)

    def update(self):
        self.live.update(self.get_messages(), refresh=True)

    def get_messages(self) -> RenderableType:
        table = Table.grid(padding=(0, 0))

        for message in self.messages:
            table.add_row(message)

        return table

    def add_message(self, message: RenderableType):
        self.messages.append(message)
        self.update()

    def update_heading(self, heading: RenderableType):
        self.messages[0] = heading
        self.update()

    def update_message(self, message: RenderableType):
        self.messages[-1] = message
        self.update()
