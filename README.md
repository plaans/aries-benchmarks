# Aries benchmark instances


This repository serves as a central point for benchmark instances.

At this point, its coverage is very partial (many instances still live the aries repository) and is main purpose is to gather test cases to assess the correctness of the solver.
Test cases are run in the aries CI.

In the future, it is our intention to also use this repository to track performance over diverse problems.

## Structure

Each problem kind has its own directory, together with an `instances.toml` file that lists all the instances and specifies how to run them.

The solver commands deliberately use `cargo run ...` for running the solvers.
This facilitates debugging as it gives a command that is directly usable for reproducing a test, even when developing.
It wold however only work when this repository is placed as subdirectory of `aries` (i.e. with the `Cargo.toml` in one of the parent directories).

## Usage

The `generate.py` script will go through those files and generate a `run_all.sh` script that will contain one line for each test case.
A test case is in general a single call to aries binary, with a non-zero exit code if the test fails.
Commands with a `# TEST` comment at the end are expected to be fast to run and should be enabled in CI.


The `run_all.sh` script is designed to be runnable with `GNU parallel` to enable parallelism when running the test cases.

For usage, see the `justfile` (you can run its command with [just](https://github.com/casey/just)).
