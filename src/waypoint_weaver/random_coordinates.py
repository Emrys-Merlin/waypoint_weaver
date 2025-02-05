from random import randint, uniform
from typing import Generic, TypeVar

import pandas as pd
from pydantic import BaseModel, model_validator

T = TypeVar("T", int, float)


class Range(BaseModel, Generic[T]):
    min: T
    max: T

    @model_validator(mode="after")
    def validate_range(self) -> "Range[T]":
        if self.min > self.max:
            raise ValueError(
                f"min value ({self.min}) must be less than or equal "
                f"to max value ({self.max})"
            )
        return self


class RandomCoordinates(BaseModel):
    count: int
    range: Range[int]
    lon: Range[float]
    lat: Range[float]

    # TODO add seed option
    def generate_dataframe(
        self, invalid_solutions: set[int] | None = None
    ) -> pd.DataFrame:
        """Generate random coordinates and append them to the existing DataFrame.

        Args:
            invalid_solutions: Set of solutions that should not be used

        Returns:
            DataFrame with random coordinates appended
        """
        invalid_solutions = invalid_solutions or set()
        result = []

        for _ in range(self.count):
            while True:
                sol = randint(self.range.min, self.range.max)
                if sol not in invalid_solutions:
                    break

            lon = uniform(self.lon.min, self.lon.max)
            lat = uniform(self.lat.min, self.lat.max)

            result.append((sol, f"{lat}, {lon}"))

        return pd.DataFrame(
            {
                "solution": [sol for sol, _ in result],
                "coordinate": [coord for _, coord in result],
            }
        )
