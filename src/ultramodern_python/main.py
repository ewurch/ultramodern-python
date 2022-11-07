from rich import print
"""This is the main module of the ultramodern_python package."""

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from ultramodern_python import wikipedia

app = typer.Typer()
API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"


@app.callback()
def callback():
    """
    UltraModern Python: A modern Python project template.
    """


@app.command()
def fact(language: str = typer.Option("en", help="Language for Wikipedia.")):
    """
    Gets a random page from Wikipedia.
    """
    with Progress(
        SpinnerColumn(), TextColumn("[bold blue]{task.fields[message]}")
    ) as progress:
        progress.add_task("message", message="Reaching wikipedia API...")
        data = wikipedia.random_page(language=language)

    title = data.title
    extract = data.extract

    print(f"\nTitle: [bold red]{title}[/bold red]")
    print(f"{extract}")
