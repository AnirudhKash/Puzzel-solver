# algorithms.py

from utility import informed_file, informed_goalfile, uninformed_file, uninformed_goalfile, heuristic_value, goal_print_statement_uninformed, goal_print_statement_informed, all_nodes

def bfs_algorithm(fringe, goal, closed_set, Flag, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe):
    while fringe["nodes"]:
        node = fringe["nodes"].pop(0)
        cost = fringe["cost"].pop(0)
        level = fringe["level"].pop(0)
        route = fringe["path"].pop(0)
        move = fringe["action"].pop(0)

        nodes_popped += 1

        # Check if the current node is the goal
        if goal_print_statement_uninformed(node, goal, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe, level, move):
            uninformed_goalfile(node, level, route[-1], move[-1], nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe)
            break
        else:
            
            if any((node == x).all() for x in closed_set):
                continue
            else:
                # Generate child nodes and add them to the fringe
                child_nodes = all_nodes(fringe, closed_set, node, cost, level, "bfs", route, move, goal)
                nodes_generated += child_nodes
                closed_set.append(node)

                if Flag == "true":
                    uninformed_file(fringe, closed_set, node, level, route[-1], move[-1], child_nodes)

                nodes_expanded += 1
                Length_of_fringe = max(Length_of_fringe, len(fringe["nodes"]))

    return {
        "nodes_popped": nodes_popped,
        "nodes_expanded": nodes_expanded,
        "nodes_generated": nodes_generated,
        "Length_of_fringe": Length_of_fringe
    }

def dfs_algorithm(fringe, goal, closed_set, Flag, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe):
    while fringe["nodes"]:
        node = fringe["nodes"].pop()
        cost = fringe["cost"].pop()
        level = fringe["level"].pop()
        route = fringe["path"].pop()
        move = fringe["action"].pop()

        nodes_popped += 1

       
        if goal_print_statement_uninformed(node, goal, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe, level, move):
            uninformed_goalfile(node, level, route[-1], move[-1], nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe)
            break
        else:
           
            if any((node == x).all() for x in closed_set):
                continue

          
            child_nodes = all_nodes(fringe, closed_set, node, cost, level, "dfs", route, move, goal)
            nodes_generated += child_nodes
            closed_set.append(node)

            if Flag == "true":
                uninformed_file(fringe, closed_set, node, level, route[-1], move[-1], child_nodes)

            nodes_expanded += 1
            Length_of_fringe = max(Length_of_fringe, len(fringe["nodes"]))


def dls_algorithm(goal, limit, algo, Flag, fringe, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe):
    depth_limit_reached = False
    while fringe["nodes"]:
        node = fringe["nodes"].pop()
        cost = fringe["cost"].pop()
        level = fringe["level"].pop()
        route = fringe["path"].pop()
        move = fringe["action"].pop()
        nodes_popped += 1

      
        if goal_print_statement_uninformed(node, goal, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe, level, move):
            uninformed_goalfile(node, level, route[-1], move[-1], nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe)
            return True
        
        # Checking if the depth limit is reached
        if level >= limit:
            if not depth_limit_reached:
                print("Depth limit reached at depth {}.".format(level))
                depth_limit_reached = True
        else:
            # Generate child nodes and add them to the fringe
            child_nodes = all_nodes(fringe, closed_set=[], node=node, cost=cost, level=level, algo=algo, route=route, move=move, goal=goal)
            nodes_generated += child_nodes
            if Flag == "true":
                uninformed_file(fringe, closed_set=[], node=node, level=level, route=route[-1], move=move[-1], child_nodes=child_nodes)
            nodes_expanded += 1
            Length_of_fringe = max(Length_of_fringe, len(fringe["nodes"]))

    # If depth limit is reached but goal is not reached it will print no of goals generated
    if depth_limit_reached and not goal_print_statement_uninformed(node, goal, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe, level, move):
        print(f"Goal not found. Nodes generated till depth limit: {nodes_generated}")
    
    return False


def ids_algorithm(start, goal, Flag):
    limit = 0
    found = False
    while not found:
        fringe = {
            "nodes": [],
            "cost": [],
            "level": [],
            "path": [],
            "action": [],
            "heuristic": [],
            "total_cost": []
        }
        fringe["nodes"].append(start)
        fringe["cost"].append(0)
        fringe["level"].append(0)
        route = [None]
        fringe["path"].append(route)
        move = [None]
        fringe["action"].append(move)
        found = dls_algorithm(goal, limit, "ids", Flag, fringe, 0, 0, 1, 0)
        limit += 1

def ucs_algorithm(fringe, goal, closed_set, Flag, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe):
    while fringe["nodes"]:
        lowest_cost = 0

        uc_list = []
        for i in range(len(fringe["cost"])):
            uc_list.append((i, fringe["cost"][i]))
        min_tuple = min(uc_list, key=lambda x: x[1])
        lowest_cost = min_tuple[0]

        node = fringe["nodes"].pop(lowest_cost)
        cost = fringe["cost"].pop(lowest_cost)
        level = fringe["level"].pop(lowest_cost)
        route = fringe["path"].pop(lowest_cost)
        move = fringe["action"].pop(lowest_cost)
        nodes_popped += 1

        # Check if the current node is the goal
        if goal_print_statement_informed(node, goal, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe, level, cost, move):
            informed_goalfile(node, cost, level, route[-1], move[-1], None, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe)
            break
        else:
            # Avoid revisiting nodes already in the closed set
            if any((node == x).all() for x in closed_set):
                pass
            else:
                # Call all_nodes with the required arguments
                child_nodes = all_nodes(fringe, closed_set, node, cost, level, "ucs", route, move, goal)
                nodes_generated += child_nodes
                closed_set.append(node)
                if Flag == "true":
                    informed_file(fringe, closed_set, "ucs", node, cost, level, route[-1], move[-1], child_nodes)
                nodes_expanded += 1
                Length_of_fringe = max(Length_of_fringe, len(fringe["nodes"]))


def greedy_algorithm(fringe, goal, closed_set, Flag, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe):
    while fringe["nodes"]:
        heuristic = fringe["heuristic"][0]
        lowest_heuristic = 0

        greedy_list = []
        for i in range(len(fringe["heuristic"])):
            greedy_list.append((i, fringe["heuristic"][i]))
        min_heuristic_tuple = min(greedy_list, key=lambda x: x[1])
        lowest_heuristic = min_heuristic_tuple[0]

        node = fringe["nodes"].pop(lowest_heuristic)
        cost = fringe["cost"].pop(lowest_heuristic)
        level = fringe["level"].pop(lowest_heuristic)
        route = fringe["path"].pop(lowest_heuristic)
        move = fringe["action"].pop(lowest_heuristic)
        heuristic = fringe["heuristic"].pop(lowest_heuristic)
        nodes_popped += 1

       
        if goal_print_statement_informed(node, goal, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe, level, cost, move):
            informed_goalfile(node, cost, level, route[-1], move[-1], None, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe)
            break
        else:
            # Avoid revisiting nodes already in the closed set
            if any((node == x).all() for x in closed_set):
                pass
            else:
                
                child_nodes = all_nodes(fringe, closed_set, node, cost, level, "greedy", route, move, goal)
                nodes_generated += child_nodes
                closed_set.append(node)
                if Flag == "true":
                    informed_file(fringe, closed_set, "greedy", node, cost, level, route[-1], move[-1], child_nodes)
                nodes_expanded += 1
                Length_of_fringe = max(Length_of_fringe, len(fringe["nodes"]))


def a_star_algorithm(fringe, goal, closed_set, Flag, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe):
    while fringe["nodes"]:
        total_cost = fringe["total_cost"][0]
        lowest_total_cost = 0

        a_list = []
        for i in range(len(fringe["total_cost"])):
            a_list.append((i, fringe["total_cost"][i]))
        min_total_cost_tuple = min(a_list, key=lambda x: x[1])
        lowest_total_cost = min_total_cost_tuple[0]

        node = fringe["nodes"].pop(lowest_total_cost)
        cost = fringe["cost"].pop(lowest_total_cost)
        level = fringe["level"].pop(lowest_total_cost)
        route = fringe["path"].pop(lowest_total_cost)
        move = fringe["action"].pop(lowest_total_cost)
        heuristic = fringe["heuristic"].pop(lowest_total_cost)
        total_cost = fringe["total_cost"].pop(lowest_total_cost)
        nodes_popped += 1

       
        if goal_print_statement_informed(node, goal, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe, level, cost, move):
            informed_goalfile(node, cost, level, route[-1], move[-1], total_cost, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe)
            break
        else:
            # Avoid revisiting nodes already in the closed set
            if any((node == x).all() for x in closed_set):
                pass
            else:
             
                child_nodes = all_nodes(fringe, closed_set, node, cost, level, "a*", route, move, goal)
                nodes_generated += child_nodes
                closed_set.append(node)
                if Flag == "true":
                    informed_file(fringe, closed_set, "a*", node, cost, level, route[-1], move[-1], child_nodes, total_cost)
                nodes_expanded += 1
                Length_of_fringe = max(Length_of_fringe, len(fringe["nodes"]))
