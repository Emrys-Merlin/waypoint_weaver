from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pandas as pd
import pytest

from waypoint_weaver.storage import store_tables
from waypoint_weaver.typing import Format


@pytest.fixture
def dummy_tables() -> dict[str, pd.DataFrame]:
    return {
        "table1": pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}),
        "table2": pd.DataFrame({"c": [7, 8, 9], "d": [10, 11, 12]}),
    }


@pytest.mark.parametrize(
    argnames="format",
    argvalues=list(Format),
)
def test_store_tables(
    format: Format,
    dummy_tables: dict[str, pd.DataFrame],
):
    with TemporaryDirectory() as temp_dir:
        output = Path(temp_dir)
        if format == Format.xls:
            output = output / "test.xlsx"

        store_tables(
            format=format,
            output=output,
            tables=dummy_tables,
        )

        if format == Format.xls:
            assert output.exists()
        elif format == Format.md:
            assert (output / "table1.md").exists()
            assert (output / "table2.md").exists()
        elif format == Format.csv:
            assert (output / "table1.csv").exists()
            assert (output / "table2.csv").exists()
        else:
            raise ValueError(f"Unknown format: {format}")


@patch("waypoint_weaver.storage.STORAGE_DICT", {})
def test_empty_storage_dict():
    with pytest.raises(ValueError):
        store_tables(
            format=Format.xls,
            output=Path("test.xlsx"),
            tables={},
        )
