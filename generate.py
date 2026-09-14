import tomllib

PROFILE = "ci"

with open("knapsack/instances.toml", "rb") as f:
    instances = tomllib.load(f)

    for instance in instances["instances"]:
        base_cmd = instances["solver"]
        cmd = base_cmd.format(**instance, profile=PROFILE)
        if "optimal" in instance:
            cmd += instances["optimal_arg"].format(**instance)
        if "test" in instance and instance["test"]:
            cmd += "  # TEST" # add flag to facilitate grepping
        print(cmd)
