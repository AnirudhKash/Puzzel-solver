# utility.py

import numpy as np

def read(file):
    l = []
    with open(file, "r") as txt_file:
        for i in txt_file:
            i = i.strip()
            if i == "END OF FILE":
                break
            l += i.split()
    l = [int(x) for x in l]
    return np.array(l).reshape(3, 3)


#function to calculate heuristic value. here weighted manhattan distance is used for problem solving
def heuristic_value(node, goal):
    heuristic = 0
    for i in range(1, 9):
        node_index = np.where(node == i)
        goal_index = np.where(goal == i)
        
        if len(node_index[0]) > 0 and len(goal_index[0]) > 0:
            heuristic += (abs(node_index[0][0] - goal_index[0][0]) + abs(node_index[1][0] - goal_index[1][0]))*i
    
    return heuristic


#function to write informed algorithm in the dump file
def informed_file(fringe, closed_set, algo, node, cost, level, route, move, child_nodes, total_cost=None):
    with open("dump.txt", "a") as file1:
        if total_cost is not None:
            file1.write("\nGenerating child_nodes to < state = {}, action = {}, g(n) = {}, d = {}, f(n) = {}, parent = {} >:".format(node, move, cost, level, total_cost, route))
        else:
            file1.write("\nGenerating child_nodes to < state = {}, action = {}, g(n) = {}, d = {}, parent = {} >:".format(node, move, cost, level, route))
        file1.write("\n{} child_nodes generated".format(child_nodes))
        file1.write("\nClosed: {}".format(closed_set))
        file1.write("\nFringe:")
        for i in range(len(fringe["nodes"])):
            if total_cost is not None:
                file1.write("\n< state = {}, action = {}, g(n) = {}, d = {}, f(n) = {}, parent = {} >".format(
                    fringe["nodes"][i], fringe["action"][i][-1], fringe["cost"][i], fringe["level"][i], fringe["total_cost"][i], fringe["path"][i][-1]))
            else:
                file1.write("\n< state = {}, action = {}, g(n) = {}, d = {}, parent = {} >".format(
                    fringe["nodes"][i], fringe["action"][i][-1], fringe["cost"][i], fringe["level"][i], fringe["path"][i][-1]))


#function to write informed algorithm goal part in the dump file
def informed_goalfile(node, cost, level, route, move, total_cost, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe):
    with open("dump.txt", "a") as file1:
        if total_cost is not None:
            file1.write("\nGoal Found: < state = {}, action = {}, g(n) = {}, d = {}, f(n) = {}, parent = {} >:".format(node, move, cost, level, total_cost, route))
        else:
            file1.write("\nGoal Found: < state = {}, action = {}, g(n) = {}, d = {}, parent = {} >:".format(node, move, cost, level, route))
        file1.write("\nNodes Popped: {}".format(nodes_popped))
        file1.write("\nNodes Expanded: {}".format(nodes_expanded))
        file1.write("\nNodes Generated: {}".format(nodes_generated))
        file1.write("\nMax Fringe Size: {}".format(Length_of_fringe))


#function to write uninformed algorithm in the dump file

def uninformed_file(fringe, closed_set, node, level, route, move, child_nodes):
    with open("dump.txt", "a") as file1:
        file1.write("\nGenerating child_nodes to < state = {}, action = {}, d = {}, parent = {} >:".format(node, move, level, route))
        file1.write("\n{} child_nodes generated".format(child_nodes))
        file1.write("\nClosed: {}".format(closed_set))
        file1.write("\nFringe:")
        for i in range(len(fringe["nodes"])):
            file1.write("\n< state = {}, action = {}, d = {}, parent = {} >".format(
                fringe["nodes"][i], fringe["action"][i][-1], fringe["level"][i], fringe["path"][i][-1]))


#function to write uninformed algorithm goal part in the dump file
def uninformed_goalfile(node, level, route, move, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe):
    with open("dump.txt", "a") as file1:
        file1.write("\nGoal Found: < state = {}, action = {}, d = {}, parent = {} >:".format(node, move, level, route))
        file1.write("\nNodes Popped: {}".format(nodes_popped))
        file1.write("\nNodes Expanded: {}".format(nodes_expanded))
        file1.write("\nNodes Generated: {}".format(nodes_generated))
        file1.write("\nMax Fringe Size: {}".format(Length_of_fringe))



#function used in informed algorithm to print the outputs if goal is reached

def goal_print_statement_informed(node, goal, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe, level, cost, move):
    if (node == goal).all():
        print("Nodes Popped: ", nodes_popped)
        print("Nodes Expanded: ", nodes_expanded)
        print("Nodes Generated: ", nodes_generated)
        print("Max Fringe Size: ", Length_of_fringe)
        print("Goal reached at depth {} at a cost of {}.".format(level, cost))
        print("Steps :")
        for step in move[1:]:
            print(step)
        return True
    return False



#function used in uninformed algorithm to print the outputs if goal is reached
def goal_print_statement_uninformed(node, goal, nodes_popped, nodes_expanded, nodes_generated, Length_of_fringe, level, move):
    if (node == goal).all():
        print("Nodes Popped: ", nodes_popped)
        print("Nodes Expanded: ", nodes_expanded)
        print("Nodes Generated: ", nodes_generated)
        print("Max Fringe Size: ", Length_of_fringe)
        print("Goal reached at depth {}.".format(level))
        print("Steps :")
        for step in move[1:]:
            print(step)
        return True
    return False

def action(tile, direction, move):
    return move + ["Move " + str(tile) + " " + direction]

def path(route, node):
    return route + [node]



#function to create  nodes
def expansion(fringe, node, cost, level, route, move, swap, action_name, goal, algo):
    new_state = node.copy()
    new_cost = cost + new_state[swap[0][0]][swap[0][1]]
    new_path = path(route, node)
    new_action = action(new_state[swap[0][0]][swap[0][1]], action_name, move)
    
    temp = new_state[swap[0][0]][swap[0][1]]
    new_state[swap[0][0]][swap[0][1]] = new_state[swap[1][0]][swap[1][1]]
    new_state[swap[1][0]][swap[1][1]] = temp
    
    addtofringe(fringe, new_state, new_cost, level, new_path, new_action, goal, algo)

#function to expand all possible nodes
def all_nodes(fringe, closed_set, node, cost, level, algo, route, move, goal):
    if node[1][1] == 0:
        expansion(fringe, node, cost, level, route, move, [(1, 0), (1, 1)], "Right", goal, algo)
        expansion(fringe, node, cost, level, route, move, [(0, 1), (1, 1)], "Down", goal, algo)
        expansion(fringe, node, cost, level, route, move, [(1, 2), (1, 1)], "Left", goal, algo)
        expansion(fringe, node, cost, level, route, move, [(2, 1), (1, 1)], "Up", goal, algo)
        return 4
    elif node[1][0] == 0:
        expansion(fringe, node, cost, level, route, move, [(0, 0), (1, 0)], "Down", goal, algo)
        expansion(fringe, node, cost, level, route, move, [(1, 1), (1, 0)], "Left", goal, algo)
        expansion(fringe, node, cost, level, route, move, [(2, 0), (1, 0)], "Up", goal, algo)
        return 3
    elif node[0][0] == 0:
        expansion(fringe, node, cost, level, route, move, [(0, 1), (0, 0)], "Left", goal, algo)
        expansion(fringe, node, cost, level, route, move, [(1, 0), (0, 0)], "Up", goal, algo)
        return 2
    elif node[0][1] == 0:
        expansion(fringe, node, cost, level, route, move, [(0, 2), (0, 1)], "Left", goal, algo)
        expansion(fringe, node, cost, level, route, move, [(1, 1), (0, 1)], "Up", goal, algo)
        expansion(fringe, node, cost, level, route, move, [(0, 0), (0, 1)], "Right", goal, algo)
        return 3
    elif node[0][2] == 0:
        expansion(fringe, node, cost, level, route, move, [(1, 2), (0, 2)], "Up", goal, algo)
        expansion(fringe, node, cost, level, route, move, [(0, 1), (0, 2)], "Right", goal, algo)
        return 2
    elif node[1][2] == 0:
        expansion(fringe, node, cost, level, route, move, [(2, 2), (1, 2)], "Up", goal, algo)
        expansion(fringe, node, cost, level, route, move, [(1, 1), (1, 2)], "Right", goal, algo)
        expansion(fringe, node, cost, level, route, move, [(0, 2), (1, 2)], "Down", goal, algo)
        return 3
    elif node[2][2] == 0:
        expansion(fringe, node, cost, level, route, move, [(2, 1), (2, 2)], "Right", goal, algo)
        expansion(fringe, node, cost, level, route, move, [(1, 2), (2, 2)], "Down", goal, algo)
        return 2
    elif node[2][1] == 0:
        expansion(fringe, node, cost, level, route, move, [(2, 0), (2, 1)], "Right", goal, algo)
        expansion(fringe, node, cost, level, route, move, [(1, 1), (2, 1)], "Down", goal, algo)
        expansion(fringe, node, cost, level, route, move, [(2, 2), (2, 1)], "Left", goal, algo)
        return 3
    else:
        expansion(fringe, node, cost, level, route, move, [(1, 0), (2, 0)], "Down", goal, algo)
        expansion(fringe, node, cost, level, route, move, [(2, 1), (2, 0)], "Left", goal, algo)
        return 2

#function to add the node created to the fringe
def addtofringe(fringe, new_state, new_cost, level, new_path, new_action, goal, algo):
    fringe["nodes"].append(new_state) 
    fringe["cost"].append(new_cost) 
    fringe["level"].append(level + 1)
    fringe["path"].append(new_path)
    fringe["action"].append(new_action)

    if algo == "greedy" or algo == "a*":  
        new_heuristic = heuristic_value(new_state, goal)
        fringe["heuristic"].append(new_heuristic)
        
        if algo == "a*":
            fringe["total_cost"].append(new_cost + new_heuristic)
