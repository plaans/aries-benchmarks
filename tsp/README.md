# TSP instance

A collection of TSP instances, either randomly generated or from TSPLIB95:

Source: https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/tspindex.html

## Usage

We provide a script for generating the instance metadata: `init_metadata.py`.

The script loads all instances, solves them with `pyvrp` records the optimal solution value.

The instance is marked for testing if it solved in less than 0.05 second by `pyvrp`.

```
uv run init_metadata.py > instances.toml
```

**Important**:

- `pyvrp` is an heuristic based solver. For small instances, optimal solutions should be found but if an unexpected error occurs, try to add execution time in `init_metadata.py`

- `pyvrp` accepts only integer distance, therefore a rounding is used.
To ensure that the optimal value found is still correct and can be used for testing, only problems with integer distance between nodes should be added:

TSPLIB95 instances are designed with integer variables for distances, therefore more instances can be added with no risk.

Random instances can be generated using the scipt `generate_tsp.py`:

```
uv run generate_tsp.py NB_CITIES_MIN NB_CITIES_MAX NB_INSTANCES [MIN_DIST MAX_DIST]
```