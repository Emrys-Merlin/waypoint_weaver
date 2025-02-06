![GitHub License](https://img.shields.io/github/license/Emrys-Merlin/waypoint_weaver)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FEmrys-Merlin%2Fwaypoint_weaver%2Fmain%2Fpyproject.toml)

| 3.12 | 3.13 |
|------|------|
|![tests](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FEmrys-Merlin%2Fec2e4e339a048ca0f0b996517d282a4a%2Fraw%2Fwaypoint_weaver_3.12-junit-tests.json)|![tests](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FEmrys-Merlin%2Fec2e4e339a048ca0f0b996517d282a4a%2Fraw%2Fwaypoint_weaver_3.13-junit-tests.json)|
|![Endpoint Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/Emrys-Merlin/ec2e4e339a048ca0f0b996517d282a4a/raw/7bb08f823be14242b40466aed324de8bff518364/waypoint_weaver_3.12-cobertura-coverage.json)|![Endpoint Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/Emrys-Merlin/ec2e4e339a048ca0f0b996517d282a4a/raw/7bb08f823be14242b40466aed324de8bff518364/waypoint_weaver_3.13-cobertura-coverage.json)|

# Waypoint Weaver

Waypoint Weaver is a Python tool that generates coordinate tables for scavenger hunts and treasure hunts. It takes a set of predefined waypoints and can mix them with random coordinates to create engaging outdoor adventures.

The assumption behind this tool is that, at every station of the treasure hunt, there is a riddle that will somehow lead to an integer solution. This tool will create a table with two columns. One containing integer codes (with the real and decoy solutions) and the other containing coordinates leading to the next station (or to a random location).

In addition, this tool assumes that there are multiple teams that each start at a different station, but which should all end up at the same final location. To this end, a separate table for each team is generated, where the solution at the last station is mapped to the common destination.

Next to the team tables, two overview tables are generated for the organizers. First, the route indicating in which order the stations are passed. Second, the starting station and coordinate for each team.

## Features

- Generate coordinate tables from YAML configuration
- Mix fixed waypoints with random coordinates
- Create separate coordinate tables for different teams
- Export tables in Excel, markdown, and csv format

## Installation

```bash
pip install waypoint_weaver
```

## Usage

Generate an example config file using:
```bash
waypoint-weaver get-config
```
You can specify a destination for the config file via `-o <path>`. The default value is `config.yaml`. The configuration will look something like this with inline comments explaining the options

```yaml
# Destination where all teams should end up
destination_coord: "52.4927985225051, 13.37875885386036"

# Coordinates of the waypoints
# Each coordinate consists of 3 parts:
# - name: A note to help the organizer identify the waypoint
# - coordinate: The latitude and longitude of the current waypoint
# - solution: The solution to the riddle at the current waypoint
#   Caution! The solution will point to the next waypoint in the list (not the current coordinate). This is a bit confusing.
# The order of the waypoints is assumed to be the order in which they will be visited. The last waypoint will wrap around to the first waypoint.
# You cannot have more teams than waypoints.
coordinates:
  - name: By the swing
    coordinate: "52.49278232538021, 13.3821449269073"
    solution: 23341
  - name: In front of the bike store
    coordinate: "52.492830925278916, 13.382977953891166"
    solution: 33885
  - name: At the pontoon
    coordinate: "52.49201148456069, 13.383314498071314"
    solution: 17446

# Random coordinates are drawn uniformly at random from the given ranges.
# The number of random coordinates is determined by the count.
# The coordinates are used to create decoy waypoints.
# Solution numbers are not assigned to random coordinates.
random_coords:
  lat:
    min: 52.48680325805024
    max: 52.498326422108214
  lon:
    min: 13.372276871074952
    max: 13.380066006044846
  range:
    min: 10_000
    max: 100_000
  count: 100
```

After adapting the configuration to your setting, you can generate waypoint tables for your treasure hunt teams via
```bash
waypoint-weaver create -c config.yaml
```
assuming your config is in the same directory with name `config.yaml`. This will store the tables as `waypoints.xlsx` in the current directory. You can change the output location via `-o`. Furthermore, you can switch between three output formats using the `-f` param:
- `xls`: The default which stores the output as an excel file.
- `csv`: Stores the tables as a set of csv files in a subdirectory at the specified location.
- `md`: Stores the tables as a set of markdown files in a subdirectory at the specified location.
