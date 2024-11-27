from pathlib import Path

from typer import Typer

from .meta_data import MetaData

main = Typer()


@main.command()
def generate_coordinates(
    meta_data: Path = Path("meta_data.yaml"),
    output_dir: Path = Path("./output"),
):
    output_dir.mkdir(parents=True, exist_ok=True)
    data = MetaData.from_yaml_file(meta_data)

    for i, team_table in enumerate(data.team_tables()):
        team_output = output_dir / f"{i:02d}_{team_table.name}.md"

        with open(team_output, "w") as f:
            f.write(f"# Team {team_table.name}\n\n")
            f.write(data.welcome_text or "")
            f.write("\n\n")
            f.write(f"__Start-Koordinate__: {team_table.start_coordinate}\n\n")
            f.write("## Koordinatentabelle\n\n")
            team_table.table.to_markdown(f, index=False)

    overview_output = output_dir / "overview.md"
    data.get_overview_table().to_markdown(
        overview_output,
        index=False,
        tablefmt="github",
    )


if __name__ == "__main__":
    main()
