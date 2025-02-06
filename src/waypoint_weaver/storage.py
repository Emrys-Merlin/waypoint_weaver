from pathlib import Path
from typing import Protocol

import pandas as pd

from .typing import Format


def _store_xls(
    output: Path,
    tables: dict[str, pd.DataFrame],
) -> None:
    with pd.ExcelWriter(output) as excel_writer:
        for name, table in tables.items():
            table.to_excel(excel_writer, sheet_name=name, index=False)


def _store_md(
    output: Path,
    tables: dict[str, pd.DataFrame],
) -> None:
    output.mkdir(parents=True, exist_ok=True)

    for name, table in tables.items():
        table.to_markdown(output / f"{name}.md", index=False, tablefmt="github")


def _store_csv(
    output: Path,
    tables: dict[str, pd.DataFrame],
) -> None:
    output.mkdir(parents=True, exist_ok=True)

    for name, table in tables.items():
        table.to_csv(output / f"{name}.csv", index=False)


class _Storage(Protocol):  # pragma: no cover
    def __call__(self, output: Path, tables: dict[str, pd.DataFrame]) -> None: ...


STORAGE_DICT: dict[Format, _Storage] = {
    Format.xls: _store_xls,
    Format.md: _store_md,
    Format.csv: _store_csv,
}


def store_tables(
    format: Format,
    output: Path,
    tables: dict[str, pd.DataFrame],
) -> None:
    """Store the tables to the output directory.

    Args:
        format: The output format
        output: The output directory
        tables: The tables to store
    """
    try:
        store = STORAGE_DICT[format]
    except KeyError as e:
        raise ValueError(
            f"Invalid format '{format}'. Use 'md', 'xls', or 'csv'."
        ) from e

    store(output=output, tables=tables)
