
Name: Anirudh Kashyap Ramesh
Net ID: 1002216351
email ID: axk6351@mavs.uta.edu


programming Language: Python


Use the following command to run the program, specifying the start file, goal file, and desired algorithm:



python main.py start.txt goal.txt [algorithm] [dump_file_flag]

    start.txt: File containing the initial state of the puzzle.

    goal.txt: File containing the goal state of the puzzle.

    [algorithm]: The search algorithm to use. Options include:
        bfs for Breadth-First Search
        dfs for Depth-First Search
        dls for Depth-Limited Search
        ids for Iterative Deepening Search
        ucs for Uniform-Cost Search
        greedy for Greedy Search
        a* for A* Search
    [dump_file_flag]: Optional. Use true to enable detailed output in dump.txt.

    Example Commands
    ->python main.py start.txt goal.txt bfs
    ->python main.py start.txt goal.txt a* true

Code Overview

main.py

    Reads the initial and goal states from input files.
    Determines which algorithm to run based on user input.
    Calls the appropriate function from algorithms.py.

algorithms.py

    Contains implementations for:
        bfs_algorithm: Breadth-First Search
        dfs_algorithm: Depth-First Search
        dls_algorithm: Depth-Limited Search
        ids_algorithm: Iterative Deepening Search
        ucs_algorithm: Uniform-Cost Search
        greedy_algorithm: Greedy Search
        a_star_algorithm: A* Search
   Note
    For algorithms like DFS, which can involve a large number of steps, the detailed output (such as nodes popped, generated, etc.) may not display immediately. It is recommended to test on smaller cases for quicker results and clearer output.

utility.py

    Provides utility functions:
        read: Reads and parses the puzzle state from a file.
        heuristic_value: Computes the heuristic for a given state.
        File handling functions for logging the search process.

Notes

    Make sure the input files are formatted correctly as 3x3 grids of integers.