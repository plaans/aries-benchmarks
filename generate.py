import tomllib

PROFILE = "ci"

COLLECTIONS = ["knapsack/instances.toml", "lp/instances.toml", "tsp/instances.toml"]


for collection in COLLECTIONS:
    with open(collection, "rb") as f:
        instances = tomllib.load(f)

        for instance in instances["instances"]:
            if instance.get("ignore"):
                continue
            base_cmd = instances["solver"]
            cmd = base_cmd.format(**instance, profile=PROFILE)
            if "optimal" in instance and "optimal_arg" in instances:
                cmd += instances["optimal_arg"].format(**instance)
            if instance.get("test"):
                cmd += "  # TEST"  # add flag to facilitate grepping
            print(cmd)
