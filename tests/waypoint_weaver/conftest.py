from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Iterator

import pytest
import yaml


@pytest.fixture
def test_data() -> dict[str, Any]:
    return {
        "coordinates": [
            {"solution": 1, "coordinate": "1,1", "name": "test", "location": "test"},
        ],
        "start_coord": "1., 1.",
        "welcome_text": "test",
        "random_coords": {
            "range": {"min": 1, "max": 1},
            "lon": {"min": 1.0, "max": 1.0},
            "lat": {"min": 1.0, "max": 1.0},
            "count": 1,
        },
    }


@pytest.fixture
def test_file(test_data: dict[str, Any]) -> Iterator[Path]:
    with TemporaryDirectory() as temp_dir:
        test_file = Path(temp_dir) / "test.yaml"
        with open(test_file, "w") as f:
            yaml.safe_dump(test_data, f)
        yield test_file
