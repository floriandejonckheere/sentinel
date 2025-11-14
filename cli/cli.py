#!/usr/bin/env python3
import json
import sys
from typing import Optional
from urllib.parse import urlparse

import typer

app = typer.Typer()


@app.command()
def main(
    name: Optional[str] = typer.Option(None, "--name", help="Name of the application"),
    url: Optional[str] = typer.Option(None, "--url", help="URL of the application"),
):
    """
    CLI application that takes either --name or --url and outputs a JSON object.
    """
    # Validate that exactly one argument is provided
    if name is None and url is None:
        typer.echo("Error: Either --name or --url must be provided", err=True)
        raise typer.Exit(code=1)

    if name is not None and url is not None:
        typer.echo("Error: Cannot provide both --name and --url", err=True)
        raise typer.Exit(code=1)

    # Validate URL if provided
    if url is not None:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            typer.echo(f"Error: Invalid URL format: {url}", err=True)
            typer.echo("URL must include scheme (http/https) and domain", err=True)
            raise typer.Exit(code=1)
        if parsed.scheme not in ["http", "https"]:
            typer.echo(f"Error: URL scheme must be http or https, got: {parsed.scheme}", err=True)
            raise typer.Exit(code=1)

    # Create the output JSON object
    output = {
        "name": name if name is not None else "",
        "vendor": "",  # Default empty vendor
        "url": url if url is not None else "",
    }

    # Output as JSON
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    app()
