import random
import json

class Node:
    def __init__(self):
        self.sibbs = []
        self.is_colored = False
        self.color = 0

    def color(self):
        self.is_colored = True
        self.color = 1

    def color(self, color):
        # For refactoring
        self.is_colored = True

    def add_sibb(self, sibb):
        self.sibbs.append(sibb)

    def get_sibbs(self):
        return self.sibbs

    def decide_force(self):
        if self.is_colored:
            uncolored_sibbs = [sibb for sibb in self.sibbs if not sibb.is_colored]
            if len(uncolored_sibbs) == 1:
                return uncolored_sibbs[0]
        return None

    def forced_sibb(self):
        if self.is_colored:
            uncolored_sibbs = [sibb for sibb in self.sibbs if not sibb.is_colored]
            if len(uncolored_sibbs) == 1:
                return uncolored_sibbs[0]
        return None

    def find_needs_coloring(self, visited_nodes, needs_coloring):
        if self not in visited_nodes:
            visited_nodes.add(self)
            forced_node = self.forced_sibb()

            if forced_node:
                needs_coloring.add(forced_node)

            for node in self.sibbs:
                node.find_needs_coloring(visited_nodes, needs_coloring)

class BicolorNode(Node):
    def __init__(self):
        self.sibbs = []
        self.is_colored = False
        self.color = 0   # Color can be 0 (uncolored), 1 or 2.

    def set_color(self, new_color):
        self.is_colored = True
        self.color = new_color

    def decide_force(self):
        # This is written with generalization in mind, so it looks a little weird                           v TODO: Max color number + 1
        colors = [(color_num, sum(sibb.color == color_num for sibb in self.sibbs)) for color_num in range(1,3)] # <= [(color_num, frequency in neighbors)]
        colors = sorted(colors, key=lambda color: color[1], reverse=True) # Sort by frequency
        print("Current: {}, colors: {}".format(self.color, colors))
        if colors[0][1] > colors[1][1] and colors[0][0] != self.color: # Most common color is more frequent than next
            return (self, colors[0][0]) # TODO: This works fine for two colors, but requires more thought for more colors

        return None

    def find_needs_coloring(self, visited_nodes, needs_coloring):
        if self not in visited_nodes:
            visited_nodes.add(self)
            forced_node = self.decide_force()

            if forced_node:
                needs_coloring.add(forced_node)

            for node in self.sibbs:
                node.find_needs_coloring(visited_nodes, needs_coloring)

# [[0,0,0,1,0],[0,0,0,1,1],[0,0,0,0,1],[1,1,0,0,0],[0,1,1,0,0]]
def make_graph(adj_matrix, num_colored=4, colored_nodes=None):
    # Create all nodes
    nodes = [BicolorNode() for row in adj_matrix]

    # Make edges
    for source_node_idx, row in enumerate(adj_matrix):
        for target_node_idx, is_connected in enumerate(row):
            if is_connected:
                nodes[source_node_idx].add_sibb(nodes[target_node_idx])

    if colored_nodes: # list of node colors in order of nodes
        for node_idx, given_color in enumerate(colored_nodes):
            nodes[node_idx].set_color(given_color)
    else:
        for node in random.sample(nodes, num_colored):
            node.set_color(random.randint(1,2)) # TODO: Generalize to more colors.

    return nodes

def make_adj(node_list):
    numbered_nodes = {n : i for i, n in enumerate(node_list)}
    adj = []
    for _ in range(len(node_list)):
        adj.append([0]*len(node_list)) # creating a square matrix of 0s
    for n in node_list:
        n_idx = numbered_nodes[n]
        for sibb in n.get_sibbs():
            s_idx = numbered_nodes[sibb]
            adj[n_idx][s_idx] = 1
    labels = [n.color if n.is_colored else None for n in node_list]
    return adj, labels

def print_json(adj, labels):
    print(json.dumps(adj))
    print(json.dumps(labels))

def run_forcing(node_list):
    """
    Takes a graph with certain colored nodes, runs the forcing propagation,
    returns propagation time #and list of colored nodes
    """
    graph_head = node_list[0]
    num_steps = -1
    colored_count = 1

    colorings_done = set() # If the same nodes need to be colored again, we've hit a loop.

    while colored_count>0:
        num_steps += 1
        needs_coloring = set()
        visited_nodes = set()

        # Find which nodes to color (needs_coloring)
        graph_head.find_needs_coloring(visited_nodes, needs_coloring)


        print()
        if frozenset(needs_coloring) in colorings_done:
            break
        colorings_done.add(frozenset(needs_coloring))

        for node, new_color in needs_coloring:
            node.set_color(new_color)

        colored_count = len(needs_coloring)

    is_finished = all(n.is_colored for n in node_list)
    return num_steps, is_finished

def exhaustively_test_until_stable():
    adj = [[0,1,0,0,1,0,0,0,0,0,0,0],[1,0,1,0,0,1,0,0,0,0,0,0],[0,1,0,1,0,0,1,0,0,0,0,0],[0,0,1,0,0,0,0,1,0,0,0,0],[1,0,0,0,0,1,0,0,1,0,0,0],[0,1,0,0,1,0,1,0,0,1,0,0],[0,0,1,0,0,1,0,1,0,0,1,0],[0,0,0,1,0,0,1,0,0,0,0,1],[0,0,0,0,1,0,0,0,0,1,0,0],[0,0,0,0,0,1,0,0,1,0,1,0],[0,0,0,0,0,0,1,0,0,1,0,1],[0,0,0,0,0,0,0,1,0,0,1,0]]

    finished_times = {}
    un_finished_times = {}
    max_num = 1<<len(adj)
    for bitstring in range(1, max_num): # iterating through all possible bitstrings of length of # of nodes
        colored = []
        for idx in range(len(adj)):
            if bitstring & (1<<idx): # 1<<idx creates a num where the bit at idx is 1, '&' will output 0 if the bitstring does not have a 1 at that idx
                colored.append(idx)
        graph_nodes = make_graph(adj, colored_nodes=colored)

        prop_time, is_finished = run_forcing(graph_nodes)
        
        if is_finished:
            finished_times[len(colored)] = finished_times.get(len(colored), []) + [prop_time]
        else:
            un_finished_times[len(colored)] = un_finished_times.get(len(colored), []) + [prop_time]

        if len(colored) == 0:
            print(bitstring)
    return finished_times, un_finished_times


if __name__ == '__main__':
    print("Making graph")
    # graph = make_graph([[0,1,0,0,0,0,0,0,0,0,0],[1,0,1,0,0,0,0,0,0,0,0],[0,1,0,1,0,0,0,0,0,0,0],[0,0,1,0,1,0,0,0,0,0,0],[0,0,0,1,0,1,0,0,0,0,0],[0,0,0,0,1,0,1,0,0,0,0],[0,0,0,0,0,1,0,1,0,0,0],[0,0,0,0,0,0,1,0,1,0,0],[0,0,0,0,0,0,0,1,0,1,0],[0,0,0,0,0,0,0,0,1,0,1],[0,0,0,0,0,0,0,0,0,1,0]],
    #                         colored_nodes=[1,1,1,1,0,0,2,2,2,2,2])
    graph = make_graph([[0,1,1,0],[1,0,1,1],[1,1,0,1],[0,1,1,0]], colored_nodes=[1,2,1,2])
    print("\nRun force")
    print(run_forcing(graph))
    print("\nAdjacency matrix")
    print_json(*make_adj(graph))
    # exhaustively_test()