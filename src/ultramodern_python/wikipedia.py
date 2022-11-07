"""The wikipedia module."""

from rich import print
import requests
import typer
from typing import Any
from dataclasses import dataclass

API_URL = "https://{language}.wikipedia.org/api/rest_v1/page/random/summary"

@dataclass
class Page:
    """Page resource.

    Attributes:
        title (str): The title of the page.
        extract (str): The extract of the page.
    """
    title: str
    extract: str

def random_page(language: str = "en") -> Page:
    """Return a random page.

    Performs a GET request to the /page/random/summary endpoint.

    Args:
        language: The Wikipedia language edition. By default, the English
            Wikipedia is used ("en").

    Returns:
        A page resource.

    Raises:
        ClickException: The HTTP request failed or the HTTP response
            contained an invalid body.
    Example:
        >>> from hypermodern_python import wikipedia
        >>> page = wikipedia.random_page(language="en")
        >>> bool(page.title)
        True
    """
    try:
        response = requests.get(API_URL.format(language=language))
        response.raise_for_status()
        data = response.json()
        return Page(title=data["title"], extract=data["extract"])
    except requests.exceptions.RequestException as error:
        print(f"Error reaching wikipedia API: {error}")
        raise typer.Exit(code=1)
