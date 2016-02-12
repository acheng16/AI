# Name: Andrew Cheng.620
# Compiled using Python3 astar.py

import heapq
import copy
import time


# displays the state of the node, used in solution function
def display_state(node):
    print(" %i %i %i" % (node.state[0], node.state[1], node.state[2]))
    print(" %i %i %i" % (node.state[3], node.state[4], node.state[5]))
    print(" %i %i %i" % (node.state[6], node.state[7], node.state[8]))
    print("")


# checks current node against goal_state
def goal_check(current_state, goal_state):
    if current_state == goal_state:
        return 1
    else:
        return 0


# calculates the current state vs goal_state how many tiles are misplaced
def cost2go(state, goal_state):
    misplaced = 0
    for i in range(0, 9):
        if state[i] != goal_state[i]:
            misplaced += 1
    return misplaced


# recursively prints out the solution from step 0 to step x
def solution(node):
    if node is not None:
        solution(node.parent_node)
        print("Step %i: %s" % (node.path_cost, node.action))
        display_state(node)


# Node class used to store the path and priorities and actions
class Node:
    def __init__(self):
        self.state = [0, 3, 5, 4, 2, 7, 6, 8, 1]  # initial state
        self.parent_node = None
        self.action = None
        self.path_cost = 0
        self.depth = 0
        self.cost2go = 0


# custom priority queue that supports multiple priorities to solve issue with nodes with same priority
# and supports iteration
class PriorityQueue:
    def __init__(self):
        self.heap = []

    # two priority to solve issue of two Nodes having the same combined cost2go and path_cost
    # priority 1 is the priority, priority 2 is time.time
    def push(self, priority1, priority2, item):
        pair = (priority1, priority2, item)
        heapq.heappush(self.heap, pair)

    # standard popping the element with least priority off
    def pop(self):
        return heapq.heappop(self.heap)

    # checks if priorityQueue is empty
    def isEmpty(self):
        return len(self.heap) == 0

    # returns the prioriy queue
    def getHeap(self):
        return self.heap

    # gets the length of the priority queue
    def getLength(self):
        return len(self.heap)

    # if the node exist return node else retun none
    def node_exists(self, item):
        for i in self.heap:
            if i[2].state == item.state:
                return i[2]
        return None


# Checks if 0 is capable of moving in that action. If yes return node, else return None
def child_node(node, action, goal_state):
    c_node = Node()
    c_node.state = copy.deepcopy(node.state)
    c_node.parent_node = node
    c_node.action = action
    c_node.path_cost = node.path_cost + 1
    c_node.depth = node.depth + 1
    spot = c_node.state.index(0)
    # swaps a, b and calculates the new cost2go
    if action == 'up':
        if spot > 2:
            a, b = spot - 3, spot
            c_node.state[b], c_node.state[a] = c_node.state[a], c_node.state[b]
            c_node.cost2go = cost2go(c_node.state, goal_state)
            return c_node
    if action == 'down':
        if spot <= 5:
            a, b = spot + 3, spot
            c_node.state[b], c_node.state[a] = c_node.state[a], c_node.state[b]
            c_node.cost2go = cost2go(c_node.state, goal_state)
            return c_node
    if action == 'left':
        if spot != 0 and spot != 3 and spot != 6:
            a, b = spot - 1, spot
            c_node.state[a], c_node.state[b] = c_node.state[b], c_node.state[a]
            c_node.cost2go = cost2go(c_node.state, goal_state)
            return c_node
    if action == 'right':
        if spot != 2 and spot != 5 and spot != 8:
            a, b = spot + 1, spot
            c_node.state[a], c_node.state[b] = c_node.state[b], c_node.state[a]
            c_node.cost2go = cost2go(c_node.state, goal_state)
            return c_node

    return None


# A star algorithm utilizing cost2go and depth as heuristic
def a_star():
    frontier = PriorityQueue()
    explored = PriorityQueue()
    goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    actions = ['up', 'down', 'left', 'right']
    node = Node()
    explored.push((node.cost2go + node.path_cost), time.time(), node)
    # search until node.state = goal_state
    while not goal_check(node.state, goal_state):
        # generates possible child nodes from action sequence
        for i in range(0, 4):
            c_node = child_node(node, actions[i], goal_state)
            # if c_node already in frontier or explored don't add it
            if c_node:
                if frontier.node_exists(c_node):
                    if explored.node_exists(c_node):
                        c_node = None
            # if action is valid and node isn't in frontier or explored, add to frontier
            if c_node:
                frontier.push((c_node.cost2go + c_node.path_cost), time.time(), c_node)
        pair = frontier.pop()
        node = pair[2]  # 3rd element in the array is the actual node
        explored.push((node.cost2go + node.path_cost), time.time(), node)
    # recursively prints out the solution after node.state equals goal_state
    solution(node)


print("A Star Solution:")
a_star()
