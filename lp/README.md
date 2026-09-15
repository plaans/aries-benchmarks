# LP instance

A collection of LP instances, for testing `aries-lp`

Source: https://github.com/ozy4dm/lp-data-netlib.git


## Usage

We provide a script for generating the instance metadata.

The script loads all instances, solves them with `glop` (part of ORTools) and records the optimal solution value.

The instance is marked for testing if it solved in substantially less than a second by `glop`.

```
uv run init_metadata.py > instances.toml
```


The `instances.toml` is committed in this repository and may have been lightly edited (mostly to ignore some test cases).

The aries-lp solver may still have some stability problems when used as a standalone LP solver (this is the case of two instances in the test cases, which are ignored). This is considered Ok because it usage in the aries-solver will detect and workaround these shortcomings.

This test suite is thus mostly build to detect regression (more instability) and potentially track performance evolution.
