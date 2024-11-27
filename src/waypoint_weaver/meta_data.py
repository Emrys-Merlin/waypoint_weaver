from pathlib import Path
from typing import Iterator

import pandas as pd
from pydantic import BaseModel, ConfigDict
from yaml import safe_dump, safe_load

from .random_coordinates import RandomCoordinates


class Coordinate(BaseModel):
    solution: int
    coordinate: str
    name: str
    location: str | None = None


class TeamTable(BaseModel):
    name: str
    start_coordinate: str
    table: pd.DataFrame

    model_config = ConfigDict(arbitrary_types_allowed=True)


class MetaData(BaseModel):
    coordinates: list[Coordinate]
    random_coords: RandomCoordinates
    start_coord: str
    welcome_text: str | None = None

    @property
    def next_coordinates(self) -> list[Coordinate]:
        return self.coordinates[1:] + [self.coordinates[0]]

    @classmethod
    def from_yaml(cls, yaml_str: str) -> "MetaData":
        """Create a MetaData instance from a YAML string.

        Args:
            yaml_str: YAML formatted string

        Returns:
            MetaData: Instance created from the YAML data
        """
        yaml_data = safe_load(yaml_str)
        return cls(**yaml_data)

    @classmethod
    def from_yaml_file(cls, yaml_file: str | Path) -> "MetaData":
        """Create a MetaData instance from a YAML file.

        Args:
            yaml_file: Path to the YAML file

        Returns:
            MetaData: Instance created from the YAML file
        """
        if isinstance(yaml_file, str):
            yaml_file = Path(yaml_file)

        with open(yaml_file, "r") as f:
            return cls.from_yaml(f.read())

    def to_yaml(self) -> str:
        """Convert the model to a YAML string.

        Returns:
            str: The model data as a YAML formatted string
        """
        return safe_dump(self.model_dump())

    def to_yaml_file(self, yaml_file: str | Path) -> None:
        """Write the model data to a YAML file.

        Args:
            yaml_file: Path where to write the YAML file
        """
        if isinstance(yaml_file, str):
            yaml_file = Path(yaml_file)

        with open(yaml_file, "w") as f:
            f.write(self.to_yaml())

    def get_solution_next_coord_table(self) -> pd.DataFrame:
        """Get a DataFrame with the solution and the next coordinate.

        Returns:
            pd.DataFrame: DataFrame with the solution and the next coordinate
        """
        next_coords = self.next_coordinates
        return pd.DataFrame(
            {
                "solution": [coord.solution for coord in self.coordinates],
                "coordinate": [coord.coordinate for coord in next_coords],
            }
        )

    def get_overview_table(self) -> pd.DataFrame:
        """Get a DataFrame with the overview of the solutions.

        Returns:
            pd.DataFrame: DataFrame with the overview of the solutions
        """
        next_coords = self.next_coordinates
        return pd.DataFrame(
            {
                "current_name": [coord.name for coord in self.coordinates],
                "current_location": [coord.location for coord in self.coordinates],
                "current_coordinate": [coord.coordinate for coord in self.coordinates],
                "current_solution": [coord.solution for coord in self.coordinates],
                "next_name": [coord.name for coord in next_coords],
                "next_location": [coord.location for coord in next_coords],
                "next_coordinate": [coord.coordinate for coord in next_coords],
            }
        )

    def raw_player_table(self) -> pd.DataFrame:
        """Get a DataFrame with the raw player table.

        Returns:
            pd.DataFrame: DataFrame with the raw player table
        """
        correct_table = self.get_solution_next_coord_table()

        invalid_solutions = {coord.solution for coord in self.coordinates}
        random_table = self.random_coords.generate_dataframe(invalid_solutions)

        return (
            pd.concat([correct_table, random_table], ignore_index=True)
            .sort_values(by="solution")
            .loc[:, ["solution", "coordinate"]]
        )

    def team_tables(self) -> Iterator[TeamTable]:
        table = self.raw_player_table()
        for coord in self.coordinates:
            table_copy = table.copy()
            table_copy.loc[table_copy["solution"] == coord.solution, "coordinate"] = (
                self.start_coord
            )
            yield TeamTable(
                name=coord.name,
                start_coordinate=coord.coordinate,
                table=table_copy,
            )
