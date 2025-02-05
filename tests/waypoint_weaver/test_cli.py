from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from typer.testing import CliRunner

from waypoint_weaver.cli import main
from waypoint_weaver.typing import Format


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.mark.parametrize(
    argnames="option",
    argvalues=[
        "-o",
        "--output",
    ],
)
def test_get_config(
    runner: CliRunner,
    option: str,
):
    with TemporaryDirectory() as temp_dir:
        config = Path(temp_dir) / "config.yaml"
        result = runner.invoke(main, ["get-config", option, str(config)])
        assert result.exit_code == 0
        assert "Storing example config file at" in result.stdout
        assert config.exists()


def test_get_config_no_overwrite(
    runner: CliRunner,
):
    with TemporaryDirectory() as temp_dir:
        config = Path(temp_dir) / "config.yaml"
        config.touch()
        result = runner.invoke(
            main,
            ["get-config", "-o", str(config)],
            input="n\n",
        )
        assert result.exit_code == 1
        assert "Config file" in result.stdout
        assert "already exists. Overwrite?" in result.stdout


def test_get_config_overwrite_with_prompt(
    runner: CliRunner,
):
    with TemporaryDirectory() as temp_dir:
        config = Path(temp_dir) / "config.yaml"
        config.touch()
        result = runner.invoke(
            main,
            ["get-config", "-o", str(config)],
            input="y\n",
        )
        assert result.exit_code == 0


@pytest.mark.parametrize(
    argnames="option",
    argvalues=[
        "-y",
        "--yes",
    ],
)
def test_get_config_overwrite_with_skip(
    runner: CliRunner,
    option: str,
):
    with TemporaryDirectory() as temp_dir:
        config = Path(temp_dir) / "config.yaml"
        config.touch()
        result = runner.invoke(
            main,
            ["get-config", "-o", str(config), option],
        )
        assert result.exit_code == 0


def test_create_no_config(
    runner: CliRunner,
):
    result = runner.invoke(
        main,
        ["create"],
    )
    assert result.exit_code == 1
    assert "Config file" in result.stdout
    assert "does not exist." in result.stdout


def test_create_no_overwrite(
    runner: CliRunner,
    test_file: Path,
):
    with TemporaryDirectory() as temp_dir:
        output = Path(temp_dir) / "waypoints.xlsx"
        output.touch()
        result = runner.invoke(
            main,
            ["create", "-c", str(test_file), "-o", str(output)],
            input="n\n",
        )
        assert result.exit_code == 1
        assert "Output file" in result.stdout
        assert "already exists. Overwrite?" in result.stdout


def test_create_overwrite_with_prompt(
    runner: CliRunner,
    test_file: Path,
):
    with TemporaryDirectory() as temp_dir:
        output = Path(temp_dir) / "waypoints.xlsx"
        output.touch()
        result = runner.invoke(
            main,
            ["create", "-c", str(test_file), "-o", str(output)],
            input="y\n",
        )
        assert result.exit_code == 0


def test_create_overwrite_with_skip(
    runner: CliRunner,
    test_file: Path,
):
    with TemporaryDirectory() as temp_dir:
        output = Path(temp_dir) / "waypoints.xlsx"
        output.touch()
        result = runner.invoke(
            main,
            ["create", "-c", str(test_file), "-o", str(output), "-y"],
        )
        assert result.exit_code == 0


@pytest.mark.parametrize(
    argnames="format",
    argvalues=list(Format),
)
def test_create(
    runner: CliRunner,
    test_file: Path,
    format: Format,
):
    with TemporaryDirectory() as temp_dir:
        output = Path(temp_dir)
        if format == Format.xls:
            output = output / "waypoints.xlsx"
        else:
            output = output / "waypoints"

        result = runner.invoke(
            main,
            [
                "create",
                "--config",
                str(test_file),
                "--output",
                str(output),
                "--format",
                str(format),
            ],
        )
        assert result.exit_code == 0
        assert "Stored tables to" in result.stdout
