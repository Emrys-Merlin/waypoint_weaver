from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from waypoint_weaver.meta_data import Coordinate, MetaData
from waypoint_weaver.random_coordinates import RandomCoordinates, Range


def test_meta_data_from_yaml_file(
    test_file: Path,
):
    meta_data = MetaData.from_yaml_file(test_file)

    assert meta_data.coordinates == [
        Coordinate(solution=1, coordinate="1,1", name="test", location="test")
    ]
    assert meta_data.start_coord == "1., 1."
    assert meta_data.welcome_text == "test"
    assert meta_data.random_coords == RandomCoordinates(
        range=Range[int](min=1, max=1),
        lon=Range[float](min=1.0, max=1.0),
        lat=Range[float](min=1.0, max=1.0),
        count=1,
    )


def test_yaml_loop(
    test_data: dict[str, Any],
):
    meta_data = MetaData(**test_data)

    with TemporaryDirectory() as temp_dir:
        out = Path(temp_dir) / "test.yaml"
        meta_data.to_yaml_file(out)
        new_meta_data = MetaData.from_yaml_file(out)

    assert meta_data == new_meta_data
