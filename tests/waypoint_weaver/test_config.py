from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from unittest.mock import MagicMock, patch

from waypoint_weaver.config import Config, Coordinate
from waypoint_weaver.random_coordinates import RandomCoordinates, Range


def test_meta_data_from_yaml_file(
    test_file: Path,
):
    meta_data = Config.from_yaml_file(test_file)

    assert meta_data.coordinates == [
        Coordinate(solution=1, coordinate="1,1", name="test")
    ]
    assert meta_data.destination_coord == "1., 1."
    assert meta_data.random_coords == RandomCoordinates(
        range=Range[int](min=1, max=1),
        lon=Range[float](min=1.0, max=1.0),
        lat=Range[float](min=1.0, max=1.0),
        count=1,
    )


def test_yaml_loop(
    test_data: dict[str, Any],
):
    meta_data = Config(**test_data)

    with TemporaryDirectory() as temp_dir:
        out = Path(temp_dir) / "test.yaml"
        meta_data.to_yaml_file(out)
        new_meta_data = Config.from_yaml_file(out)

    assert meta_data == new_meta_data


def test_get_overview_table():
    pass


def test_team_tables():
    pass


@patch("waypoint_weaver.config.store_tables")
def test_save_tables(
    store_tables: MagicMock,
    test_config: Config,
):
    pass
