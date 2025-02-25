import sys
import os
from algorithms import bfs_algorithm, dfs_algorithm, dls_algorithm, ids_algorithm, ucs_algorithm, greedy_algorithm, a_star_algorithm
from utility import read, heuristic_value

# List of available algorithms
algorithms = ["bfs", "ucs", "dfs", "dls", "ids", "greedy", "a*"]


if len(sys.argv) < 3:
    print("Error: Not enough arguments provided.")
    sys.exit(1)


start_file = sys.argv[1]
goal_file = sys.argv[2]


algo = "a*" if len(sys.argv) < 4 else sys.argv[3]


if algo not in algorithms:
    print(f"Error: '{algo}' is not a valid algorithm. Choose from {algorithms}.")
    sys.exit(1)

# Check if the input files exist
if not os.path.isfile(start_file):
    print("didn't found start file")
    sys.exit(1)

if not os.path.isfile(goal_file):
    print(f"didn't found goal file")
    sys.exit(1)


Flag = "false"
if len(sys.argv) > 4:
    d = sys.argv[4]
    if d == "true":
        Flag = "true"

# Read the input files
try:
    start = read(start_file)
    goal = read(goal_file)
except Exception as e:
    print(f"Error reading input files: {e}")
    sys.exit(1)

if Flag == "true":
    with open("dump.txt", "w") as file1:
        file1.write("\n Algorithm : {}".format(algo))
        file1.write("\nRunning {}".format(algo))

# Initialize fringe and other variables
fringe = {
    "nodes": [],
    "cost": [],
    "level": [],
    "path": [],
    "action": [],
    "heuristic": [],
    "total_cost": []
}

closed_set = []
Length_of_fringe = 0
node = start.copy()
fringe["nodes"].append(node)
fringe["cost"].append(0)
fringe["level"].append(0)
route = [None]
fringe["path"].append(route)
move = [None]
fringe["action"].append(move)

nodes_popped = 0
nodes_expanded = 0
nodes_generated = 1

fringe["heuristic"].append(heuristic_value(node, goal))
fringe["total_cost"].append(fringe["cost"][0] + fringe["heuristic"][0])

# Select and run the appropriate algorithm
if algo == 'bfs':
    bfs_algorithm(fringe, goal, closed_set, Flag, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe)
elif algo == 'dfs':
    dfs_algorithm(fringe, goal, closed_set, Flag, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe)
elif algo == 'dls':
    limit = int(input("Enter the depth limit: "))
    dls_algorithm(goal, limit, algo, Flag, fringe, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe)
elif algo == 'ids':
    ids_algorithm(start, goal, Flag)
elif algo == 'ucs':
    ucs_algorithm(fringe, goal, closed_set, Flag, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe)
elif algo == 'greedy':
    greedy_algorithm(fringe, goal, closed_set, Flag, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe)
elif algo == 'a*':
    a_star_algorithm(fringe, goal, closed_set, Flag, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe)
