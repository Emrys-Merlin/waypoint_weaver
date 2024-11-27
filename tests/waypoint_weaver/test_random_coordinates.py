import pytest

from waypoint_weaver.random_coordinates import RandomCoordinates, Range


def test_range_validation():
    range = Range[int](min=1, max=2)
    assert range.min == 1
    assert range.max == 2

    with pytest.raises(ValueError):
        Range[int](min=2, max=1)


def test_generate_dataframe():
    random_coords = RandomCoordinates(
        range=Range[int](min=1, max=10),
        lon=Range[float](min=1.0, max=2.0),
        lat=Range[float](min=1.0, max=2.0),
        count=3,
    )
    invalid_solutions = {1, 2}

    result_df = random_coords.generate_dataframe(invalid_solutions)
    solutions = set(result_df["solution"].values)
    coords = result_df["coordinate"].str.split(", ", expand=True).astype(float)
    lats = coords.iloc[:, 0].to_list()
    lons = coords.iloc[:, 1].to_list()

    assert len(result_df) == 3
    assert solutions.issubset(range(1, 11))
    assert not solutions.intersection(invalid_solutions)
    assert all(1.0 <= lat <= 2.0 for lat in lats)
    assert all(1.0 <= lon <= 2.0 for lon in lons)
