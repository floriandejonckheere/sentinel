#!/usr/bin/env python3
import json
import sys
from typing import Optional

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
