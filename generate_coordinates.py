# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pandas",
#     "pyyaml",
#     "tabulate",
#     "typer",
# ]
# ///
from pathlib import Path
from random import randint, uniform

import pandas as pd
from typer import Typer
from yaml import safe_load

main = Typer()


@main.command()
def generate_coordinates(
    meta_data: Path = Path("meta_data.yaml"),
    output: Path = Path("coordinates.md"),
):
    with open(meta_data, "r") as file:
        data = safe_load(file)

    df = pd.DataFrame.from_dict(data["coordinates"])

    invalid_solutions = {coord["solution"] for coord in data["coordinates"]}
    solution = []
    coords = []

    for _ in range(data["random_coords"]["count"]):
        while True:
            sol = randint(
                data["random_coords"]["range"]["min"],
                data["random_coords"]["range"]["max"],
            )
            if sol not in invalid_solutions:
                break
        solution.append(sol)

        lon = uniform(
            data["random_coords"]["lon"]["min"], data["random_coords"]["lon"]["max"]
        )
        lat = uniform(
            data["random_coords"]["lat"]["min"], data["random_coords"]["lat"]["max"]
        )

        coords.append(f"{lat}, {lon}")

    rand_df = pd.DataFrame({"solution": solution, "coordinate": coords})

    df = pd.concat([df, rand_df], ignore_index=True)
    df.sort_values(by="solution", inplace=True)
    df = df[["solution", "coordinate"]]

    coordinates = data["coordinates"]
    qr_code_table_list = []
    for current, previous in zip(coordinates, [coordinates[-1]] + coordinates[:-1]):
        group_df = df.copy()
        name = current["name"]
        start_coordinate = previous["coordinate"]
        qr_code_table_list.append(
            {
                "name": name,
                "location": previous["location"],
                "coordinate": start_coordinate,
            }
        )

        group_df.loc[group_df["solution"] == previous["solution"], "coordinate"] = data[
            "start_coord"
        ]

        group_output = output.parent / f"{output.stem}_{name}{output.suffix}"

        with open(group_output, "w") as f:
            f.write(f"# Team {name}\n\n")
            f.write(data["welcome_text"])
            f.write("\n\n")
            f.write(f"__Start-Koordinate__: {start_coordinate}\n\n")
            f.write("## Koordinatentabelle\n\n")
            group_df.to_markdown(f, index=False)

    pd.DataFrame.from_dict(qr_code_table_list).to_markdown(
        output, index=False, tablefmt="github"
    )


if __name__ == "__main__":
    main()
