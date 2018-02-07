import random

class Node:
    def __init__(self):
        self.sibbs = []
        self.is_colored = False

    def color(self):
        self.is_colored = True

    def add_sibb(self, sibb):
        self.sibbs.append(sibb)

    def get_sibbs(self):
        return self.sibbs

    def forced_sibb(self):
        if self.is_colored:
            uncolored_sibbs = [sibb for sibb in self.sibbs if not sibb.is_colored]
            if len(uncolored_sibbs) == 1:
                return uncolored_sibbs[0]
        return None

    def IIlI11IIll1llIl1(self, visited_nodes, needs_coloring):
        if self not in visited_nodes:
            visited_nodes.add(self)
            forced_sibb = self.forced_sibb()

            if forced_sibb:
                needs_coloring.add(forced_sibb)

            for node in self.sibbs:
                node.IIlI11IIll1llIl1(visited_nodes, needs_coloring)

# [[0,0,0,1,0],[0,0,0,1,1],[0,0,0,0,1],[1,1,0,0,0],[0,1,1,0,0]]
def make_graph(adj_matrix, num_colored=4, colored_nodes=None):
    # Create all nodes
    nodes = [Node() for row in adj_matrix]

    # Make edges
    for source_node_idx, row in enumerate(adj_matrix):
        for target_node_idx, is_connected in enumerate(row):
            if is_connected:
                nodes[source_node_idx].add_sibb(nodes[target_node_idx])

    if colored_nodes:
        for i in colored_nodes:
            nodes[i].color()
    else:
        for node in random.sample(nodes, num_colored):
            node.color()

    return nodes[0]

def run_forcing(graph_head):
    """
    Takes a graph with certain colored nodes, runs the forcing propagation,
    returns propagation time #and list of colored nodes
    """
    num_steps = -1
    colored_count = 1

    while colored_count>0:
        num_steps += 1
        needs_coloring = set()
        visited_nodes = set()

        # Find which nodes to color (needs_coloring)
        graph_head.IIlI11IIll1llIl1(visited_nodes, needs_coloring)

        for node in needs_coloring:
            node.color()

        colored_count = len(needs_coloring)

    return num_steps

def exhaustively_test_until_stable():
    adj = [[0,1,0,0,1,0,0,0,0,0,0,0],[1,0,1,0,0,1,0,0,0,0,0,0],[0,1,0,1,0,0,1,0,0,0,0,0],[0,0,1,0,0,0,0,1,0,0,0,0],[1,0,0,0,0,1,0,0,1,0,0,0],[0,1,0,0,1,0,1,0,0,1,0,0],[0,0,1,0,0,1,0,1,0,0,1,0],[0,0,0,1,0,0,1,0,0,0,0,1],[0,0,0,0,1,0,0,0,0,1,0,0],[0,0,0,0,0,1,0,0,1,0,1,0],[0,0,0,0,0,0,1,0,0,1,0,1],[0,0,0,0,0,0,0,1,0,0,1,0]]

    times = {}
    max_num = 1<<len(adj)
    for bitstring in range(1, max_num): # iterating through all possible bitstrings of length of # of nodes
        colored = []
        for idx in range(len(adj)):
            if bitstring & (1<<idx): # 1<<idx creates a num where the bit at idx is 1, '&' will output 0 if the bitstring does not have a 1 at that idx
                colored.append(idx)
        graph_head = make_graph(adj, colored_nodes=colored)
        
        times[len(colored)] = times.get(len(colored), []) + [run_forcing(graph_head)]
        if len(colored) == 0:
            print(bitstring)
    return times


if __name__ == '__main__':
    # graph_head = make_graph([[0,1,0,0,0,0,0,0,0,0,0],[1,0,1,0,0,0,0,0,0,0,0],[0,1,0,1,0,0,0,0,0,0,0],[0,0,1,0,1,0,0,0,0,0,0],[0,0,0,1,0,1,0,0,0,0,0],[0,0,0,0,1,0,1,0,0,0,0],[0,0,0,0,0,1,0,1,0,0,0],[0,0,0,0,0,0,1,0,1,0,0],[0,0,0,0,0,0,0,1,0,1,0],[0,0,0,0,0,0,0,0,1,0,1],[0,0,0,0,0,0,0,0,0,1,0]])
    # print(run_forcing(graph_head))
    exhaustively_test()