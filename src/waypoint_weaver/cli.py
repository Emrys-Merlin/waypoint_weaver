from pathlib import Path
from typing import Annotated

from typer import Option, Typer, confirm, echo

from . import EXAMPLE_CONFIG
from .config import Config
from .typing import Format

main = Typer()


@main.command()
def get_config(
    output: Annotated[
        Path, Option("-o", "--output", help="Destination for the config file")
    ] = Path("./config.yaml"),
    skip_confirmation: Annotated[
        bool, Option("-y", "--yes", help="Skip confirmation")
    ] = False,
) -> None:
    """Get an example config file."""
    if not skip_confirmation and output.exists():
        message = f"Config file '{output}' already exists. Overwrite?"
        if not confirm(message):
            exit(1)

    echo(f"Storing example config file at {output}")

    with open(EXAMPLE_CONFIG) as f:
        text = f.read()

    with open(output, "w") as f:
        f.write(text)


@main.command()
def create(
    config_file: Annotated[
        Path, Option("-c", "--config", help="Path to config file")
    ] = Path("./config.yaml"),
    output: Annotated[
        Path,
        Option(
            "-o",
            "--output",
            help="Output file if --format=xls. Otherwise, output directory",
        ),
    ] = Path("./waypoints.xlsx"),
    format: Annotated[
        Format, Option("-f", "--format", help="Output format (md, xls, or csv)")
    ] = Format.xls,
    skip_confirmation: Annotated[
        bool, Option("-y", "--yes", help="Skip confirmation")
    ] = False,
):
    """Create one or more waypoint files from a config file."""
    if not config_file.exists():
        echo(f"Config file '{config_file}' does not exist.", err=True)
        exit(1)

    if not skip_confirmation and output.exists():
        message = f"Output file '{output}' already exists. Overwrite?"
        if not confirm(message):
            exit(1)

    config = Config.from_yaml_file(config_file)

    config.save_tables(output=output, format=format)
    echo(f"Stored tables to {output}")


if __name__ == "__main__":  # pragma: no cover
    main()
