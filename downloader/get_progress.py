from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress,SpinnerColumn,TextColumn,BarColumn,TimeRemainingColumn,TransferSpeedColumn
import logging

_console = Console()
_progress = None


def start_ui():
    global _progress
    handler = RichHandler(console=_console,markup=True)
    logging.basicConfig(level=logging.INFO,handlers=[handler],force=True)

    _progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=None),
        TimeRemainingColumn(),
        console=_console,
        refresh_per_second=10,
    )
    _progress.start()
    return _progress


def get_progress():
    return _progress

def stop_ui():
    global _progress
    if _progress:
        _progress.stop()
        _progress = None