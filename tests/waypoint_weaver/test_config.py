from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from waypoint_weaver.config import Config, Coordinate
from waypoint_weaver.random_coordinates import RandomCoordinates, Range
from waypoint_weaver.typing import Format


@pytest.mark.parametrize(
    argnames="cast2str",
    argvalues=[
        True,
        False,
    ],
)
def test_meta_data_from_yaml_file(
    test_file: str | Path,
    n_stations: int,
    cast2str: bool,
):
    if cast2str:
        test_file = str(test_file)

    meta_data = Config.from_yaml_file(test_file)

    assert meta_data.coordinates == [
        Coordinate(solution=i, coordinate=f"1,{i}", name=f"test_{i:02d}")
        for i in range(n_stations)
    ]
    assert meta_data.destination_coord == "1., 1."
    assert meta_data.random_coords == RandomCoordinates(
        range=Range[int](min=1, max=20),
        lon=Range[float](min=1.0, max=1.0),
        lat=Range[float](min=1.0, max=1.0),
        count=15,
    )


@pytest.mark.parametrize(
    argnames="cast2str",
    argvalues=[
        True,
        False,
    ],
)
def test_yaml_loop(
    test_data: dict[str, Any],
    cast2str: bool,
):
    meta_data = Config(**test_data)

    with TemporaryDirectory() as temp_dir:
        out: str | Path = Path(temp_dir) / "test.yaml"
        if cast2str:
            out = str(out)
        meta_data.to_yaml_file(out)
        new_meta_data = Config.from_yaml_file(out)

    assert meta_data == new_meta_data


def test_get_overview_table(
    test_config: Config,
    n_stations: int,
):
    columns = [
        "current_name",
        "current_coordinate",
        "current_solution",
        "next_name",
        "next_coordinate",
    ]

    overview_table = test_config.get_overview_table()

    assert overview_table.columns.tolist() == columns
    assert len(overview_table) == n_stations


def test_team_tables(
    test_config: Config,
    n_stations: int,
):
    team_tables = list(test_config.team_tables())

    assert len(team_tables) == n_stations
    for i, table in enumerate(team_tables):
        assert table.name == f"test_{i:02d}"
        assert table.start_coordinate == f"1,{i}"
        assert len(table.table) == test_config.random_coords.count + n_stations
        assert (
            table.table.loc[table.table["solution"] == i, "coordinate"].values[0]
            == test_config.destination_coord
        )


@pytest.mark.parametrize(
    argnames="format",
    argvalues=[
        Format.xls,
        Format.csv,
        Format.md,
    ],
)
@patch("waypoint_weaver.config.store_tables")
def test_save_tables(
    store_tables: MagicMock,
    test_config: Config,
    format: Format,
):
    output = Path("output")

    test_config.save_tables(format=format, output=output)

    store_tables.assert_called_once()
