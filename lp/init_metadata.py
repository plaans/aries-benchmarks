import os
import time

from ortools.linear_solver.python import model_builder

MPS_DIR = "mps_files"

print("""
class = "lp"
solver = "cargo -q run --profile {profile} --example solve_mps -- lp/{file}"
optimal_arg = " --expected-value={optimal}"
""")

files = os.listdir(MPS_DIR)
files.sort()

for filename in files:
    if not filename.endswith(".mps"):
        continue

    value_or = None

    model = model_builder.ModelBuilder()

    # 1. Import the MPS file
    if not model.import_from_mps_file(f"{MPS_DIR}/{filename}"):
        print(f"Error while parsing {filename}")
    else:
        # 2. Init the solver
        solver = model_builder.ModelSolver("glop")

        # 3. Solve
        start = time.time()
        status_or = solver.solve(model)
        end = time.time()

        solve_time = end - start

        exec_time_or = end - start

        if status_or == model_builder.SolveStatus.OPTIMAL:
            value_or = solver.objective_value

        print()
        print("[[instances]]")
        print(f"file = '{MPS_DIR}/{filename}'")
        if value_or:
            print(f"optimal = {value_or}")
        print(f"glop_solve_time = {solve_time}")
        if solve_time < 0.3:
            print("test = true")
