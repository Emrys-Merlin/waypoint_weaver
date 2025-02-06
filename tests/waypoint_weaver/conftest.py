from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Iterator

import pytest
import yaml

from waypoint_weaver.config import Config


@pytest.fixture
def n_stations() -> int:
    return 5


@pytest.fixture
def test_data(
    n_stations: int,
) -> dict[str, Any]:
    return {
        "coordinates": [
            {
                "solution": i,
                "coordinate": f"1,{i}",
                "name": f"test_{i:02d}",
            }
            for i in range(n_stations)
        ],
        "destination_coord": "1., 1.",
        "random_coords": {
            "range": {"min": 1, "max": 20},
            "lon": {"min": 1.0, "max": 1.0},
            "lat": {"min": 1.0, "max": 1.0},
            "count": 15,
        },
    }


@pytest.fixture
def test_file(test_data: dict[str, Any]) -> Iterator[Path]:
    with TemporaryDirectory() as temp_dir:
        test_file = Path(temp_dir) / "test.yaml"
        with open(test_file, "w") as f:
            yaml.safe_dump(test_data, f)
        yield test_file


@pytest.fixture
def test_config(test_data: dict[str, Any]) -> Config:
    return Config(**test_data)
