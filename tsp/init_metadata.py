import os
import sys
import time
import numpy as np

import tsplib95
from pyvrp import Client, Depot, Location, Model, ProblemData, VehicleType
from pyvrp.stop import MaxRuntime, MaxIterations, MultipleCriteria

TSP_DIR = "tsp_files"

print("""
class = "tsp"
solver = "cargo -q run --profile {profile} --example tsp -- tsp/{file}"
optimal_arg = " --expected-value {optimal}"
""")

files = os.listdir(TSP_DIR)
files.sort()

for filename in files:
    if not filename.endswith(".tsp"):
        continue

    total_cost = None

    try:
        # 1. Import the TSP file
        problem = tsplib95.load(os.path.join(TSP_DIR, filename))
    except Exception as e:
        print(f"Unexpected error while parsing {filename} : {e}", file=sys.stderr)
        continue

    nodes = list(problem.get_nodes())
    n = len(nodes)

    if n <= 1:
        continue

    # 2. Build integer distance matrix (int64 required by PyVRP)
    matrix = np.array(
        [[int(problem.get_weight(u, v)) for v in nodes] for u in nodes],
        dtype=np.int64,
    )

    # FORCE DIAGONAL TO ZERO: PyVRP strictly requires dist(i, i) == 0
    np.fill_diagonal(matrix, 0)

    # 3. Create PyVRP data model (Latest PyVRP 0.9+ API)
    # A. Define spatial locations (we don't strictly need x, y for the matrix to work)
    locations = [Location(x=0, y=0) for _ in range(n)]
    
    # B. Define logical entities mapping to location indices
    depots = [Depot(location=0)]
    clients = [Client(location=i) for i in range(1, n)]
    
    # C. One vehicle for TSP
    vehicle_types = [VehicleType(num_available=1)]

    # D. Build ProblemData
    data = ProblemData(
        locations=locations,
        clients=clients,
        depots=depots,
        vehicle_types=vehicle_types,
        distance_matrices=[matrix],
        duration_matrices=[matrix],
    )

    # 4. Solve with PyVRP
    try:
        model = Model.from_data(data)
        
        start = time.time()
        # MaxRuntime in seconds. Increase for very large instances if needed.
        res = model.solve(stop=MultipleCriteria([MaxIterations(1000), MaxRuntime(2.0)]), display=False)
        end = time.time()

        total_cost = res.cost()
        solve_time = end - start

        # 5. Format output
        print()
        print("[[instances]]")
        print(f"file = '{TSP_DIR}/{filename}'")
        
        if total_cost is not None:
            print(f"optimal = {total_cost}")
            
        print(f"pyvrp_solve_time = {solve_time:.4f}")
        
        if solve_time < 0.05:
            print("test = true")

    except Exception as e:
        print(f"Error solving {filename} with PyVRP: {e}", file=sys.stderr)