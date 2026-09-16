import os
import random
import sys


def generate_explicit_tsp(
    num_nodes: int,
    filename: str,
    name: str = "custom_tsp",
    comment: str = "Explicit integer matrix TSP",
    min_dist: int = 1,
    max_dist: int = 100,
    seed: int = None,
):
    """Generates an explicit FULL_MATRIX TSPLIB (.tsp) file with integer distances."""
    if seed is not None:
        random.seed(seed)

    # 1. Generate the distance matrix
    matrix = [[0] * num_nodes for _ in range(num_nodes)]

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            weight = random.randint(min_dist, max_dist)
            matrix[i][j] = weight
            matrix[j][i] = weight

    # Diagonal is strictly 0
    for i in range(num_nodes):
        matrix[i][i] = 0

    # 2. Write TSPLIB formatted file
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"NAME: {name}\n")
        f.write(f"COMMENT: {comment}\n")
        f.write("TYPE: TSP\n")
        f.write(f"DIMENSION: {num_nodes}\n")
        f.write("EDGE_WEIGHT_TYPE: EXPLICIT\n")
        f.write("EDGE_WEIGHT_FORMAT: FULL_MATRIX\n")
        f.write("EDGE_WEIGHT_SECTION\n")

        for row in matrix:
            # Print row formatted with space separators
            f.write(" " + " ".join(f"{weight:4d}" for weight in row) + "\n")

        f.write("EOF\n")

    print(f"Generated {filename} (N={num_nodes})")


if __name__ == "__main__":

    if len(sys.argv) < 4 or len(sys.argv) > 6:
        print(f"Unexpected number of arguments, usage:\n{sys.argv[0]} NB_CITIES_MIN NB_CITIES_MAX NB_INSTANCES [MIN_DIST MAX_DIST]", file=sys.stderr)
        exit(1)

    nb_cities_min = int(sys.argv[1])
    nb_cities_max = int(sys.argv[2])
    nb_instances = int(sys.argv[3])

    min_dist = 1
    max_dist = 200

    if len(sys.argv) == 6:
        min_dist = int(sys.argv[4])
        max_dist = int(sys.argv[5])

    output_dir = "tsp_files"
    for size in range(nb_cities_min, nb_cities_max + 1):
        for nb_instance in range(nb_instances):
            generate_explicit_tsp(
                num_nodes=size,
                filename=f"{output_dir}/random_n{size}_{nb_instance}.tsp",
                name=f"random_n{size}_{nb_instance}",
                min_dist=min_dist,
                max_dist=max_dist,
                seed=size * nb_instance,  # Reproducible seed
            )