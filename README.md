
<div align="center">
  <img src="./docs/static/PSDM_icon_extended_360px.png" width="200">
</div>

----

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

A data model for the description of electrical power systems.

- [Field of Application](#field-of-application)
  - [Grid Topology](#grid-topology)
  - [Topology Case](#topology-case)
  - [Steadystate Case](#steadystate-case)
- [General Remarks](#general-remarks)
- [Installation](#installation)
- [Development](#development)
- [Attribution](#attribution)

## Field of Application

This data model is intended to describe electrical power systems.
It provides a hierarchical structure/schema to describe unique entity relations as well as parameter sets.

The data model is structured as the following schema:

### Grid Topology
This is the base topology containing all elements of the exported grid:
- Branches (symmetrical: overhead lines, cables, fuses from type "branch")
- Nodes
- Transformers (symmetrical: 2- or 3-winding)
- External grids
- Loads (consumer, producer, grid assets)
![topology relationship diagram](./docs/entity_rel__topology.png)

In addition to the explicitly defined element attributes, it is possible to save user-specific additional information as optional AttributeData ([Export example of powerfactory-tools](https://github.com/ieeh-tu-dresden/powerfactory-tools/blob/main/examples/powerfactory_export.ipynb)).

### Topology Case
This holds information about disabled elements to represent a specific operational case based on the base topology.
  ![topology case relationship diagram](./docs/entity_rel__topology_case.png)

### Steadystate Case
This holds information for a specific operational case such as:
- power draw/infeed of load
- tap posistion of transformer
- operating point of external grid
  ![steadystate case relationship diagram](./docs/entity_rel__steady_state_case.png)

## General Remarks

Please find below some important general remarks and assumptions to consider for consistent usage across different applications:
- The passive sign convention should be used for all types of loads (consumer as well as producer).
- Numeric values should be set using the SI unit convention.
- Topology
  - Only **symmetrical** grid assets, e.g. transformer or line, are supported.
  - The `Rated Power` should always be defined positive (absolute value).
- The interaction between load models and controllers are depicted in the following schematic:
  ![active/reactive power schematics](./docs/power_schematics.png)

## Installation

Just install via pip:

```bash
pip install ieeh-power-system-data-model
```

## Development

[Install the Python package and project manager uv](https://github.com/astral-sh/uv)

Clone `power-system-data-model`

```bash
git@github.com:ieeh-tu-dresden/power-system-data-model.git
```

```bash
cd power-system-data-model
```

Install `power-system-data-model` as a production tool

```bash
uv sync --no-dev
```

Install `power-system-data-model` in development mode

```bash
uv sync
```

For development in [Visual Studio Code](https://github.com/microsoft/vscode), all configurations are already provided:

- [ruff](https://github.com/astral-sh/ruff)
- [mypy](https://github.com/python/mypy)

## Attribution

Please provide a link to this repository:

<https://github.com/ieeh-tu-dresden/power-system-data-model>

Please cite as:

Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, _Power System Data Model - A data model for the description of electrical power systems_, Zenodo, 2023. <https://doi.org/10.5281/zenodo.8087079>.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8087079.svg)](https://doi.org/10.5281/zenodo.8087079)
