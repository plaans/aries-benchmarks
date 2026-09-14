
SCRIPT_NAME := "run_all.sh"

# generate the script with all instances to run
generate:
    uv run generate.py > {{ SCRIPT_NAME }}


run_tests: generate
    # bash -e {{SCRIPT_NAME}}   ## this is the simplest variant
    parallel -k --halt-on-error 2 -v < {{ SCRIPT_NAME }}
