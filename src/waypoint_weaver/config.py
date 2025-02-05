from pathlib import Path
from typing import Iterator

import pandas as pd
from pydantic import BaseModel, ConfigDict
from yaml import safe_dump, safe_load

from .random_coordinates import RandomCoordinates
from .storage import store_tables
from .typing import Format


class Coordinate(BaseModel):
    solution: int
    coordinate: str
    name: str


class TeamTable(BaseModel):
    name: str
    start_coordinate: str
    table: pd.DataFrame

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Config(BaseModel):
    coordinates: list[Coordinate]
    random_coords: RandomCoordinates
    destination_coord: str

    @property
    def next_coordinates(self) -> list[Coordinate]:
        return self.coordinates[1:] + [self.coordinates[0]]

    @classmethod
    def from_yaml(cls, yaml_str: str) -> "Config":
        """Create a Config instance from a YAML string.

        Args:
            yaml_str: YAML formatted string

        Returns:
            Instance created from the YAML data
        """
        yaml_data = safe_load(yaml_str)
        return cls(**yaml_data)

    @classmethod
    def from_yaml_file(cls, yaml_file: str | Path) -> "Config":
        """Create a Config instance from a YAML file.

        Args:
            yaml_file: Path to the YAML file

        Returns:
            Instance created from the YAML file
        """
        if isinstance(yaml_file, str):
            yaml_file = Path(yaml_file)

        with open(yaml_file, "r") as f:
            return cls.from_yaml(f.read())

    def to_yaml(self) -> str:
        """Convert the model to a YAML string.

        Returns:
            The model data as a YAML formatted string
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
                "current_coordinate": [coord.coordinate for coord in self.coordinates],
                "current_solution": [coord.solution for coord in self.coordinates],
                "next_name": [coord.name for coord in next_coords],
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
        """Iterate over team-specific solution tables.

        Yields:
            The team tables with specific start coordinate and the common
            destination coordinate placed on the correct solution
        """
        table = self.raw_player_table()
        for coord in self.coordinates:
            table_copy = table.copy()
            table_copy.loc[table_copy["solution"] == coord.solution, "coordinate"] = (
                self.destination_coord
            )
            yield TeamTable(
                name=coord.name,
                start_coordinate=coord.coordinate,
                table=table_copy,
            )

    def save_tables(self, format: Format, output: Path) -> None:
        """Save the tables to the output directory.

        Args:
            format: The output format
            output: The output directory
        """
        tables = {
            "route": self.get_overview_table(),
        }
        starting_locations = []

        for i, team_table in enumerate(self.team_tables(), 1):
            name = f"team_{i:02d}"
            tables[name] = team_table.table
            starting_locations.append(
                {
                    "team": name,
                    "name": team_table.name,
                    "start_coordinate": team_table.start_coordinate,
                }
            )

        tables["starting_locations"] = pd.DataFrame(starting_locations)

        store_tables(
            format=format,
            output=output,
            tables=tables,
        )
