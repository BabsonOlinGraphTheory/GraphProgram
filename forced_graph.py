import random
import json

class Node:
    def __init__(self):
        self.sibbs = []
        self.is_colored = False

    def color(self):
        self.is_colored = True

    def uncolor(self):
        self.is_colored = False

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

    def find_needs_coloring(self, visited_nodes, needs_coloring):
        if self not in visited_nodes:
            visited_nodes.add(self)
            forced_sibb = self.forced_sibb()

            if forced_sibb:
                needs_coloring.add(forced_sibb)

            for node in self.sibbs:
                node.find_needs_coloring(visited_nodes, needs_coloring)

class DataCollector:
    def each_run(self, color_set, nodes_list, prop_time, is_finished):
        raise NotImplementedError("you must use a subclass")

    def finish(self):
        raise NotImplementedError("you must use a subclass")

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
    labels = [1 if n.is_colored else None for n in node_list]
    return adj, labels

def print_json(adj, labels):
    print(json.dumps(adj))
    print(json.dumps(labels))

def run_forcing(node_list):
    """
    Takes a graph with certain colored nodes, runs the forcing propagation,
    returns propagation time
    """
    graph_head = node_list[0]
    num_steps = -1
    colored_count = 1

    while colored_count>0:
        num_steps += 1
        needs_coloring = set()
        visited_nodes = set()

        # Find which nodes to color (needs_coloring)
        graph_head.find_needs_coloring(visited_nodes, needs_coloring)

        for node in needs_coloring:
            node.color()

        colored_count = len(needs_coloring)

    is_finished = all(n.is_colored for n in node_list)
    return num_steps, is_finished

def test_until_stable(adj, sampling_func, data_collector_obj=None, sample_func_args={}):
    """ Problems: sometimes we sample inexhaustively, so we're just using the
        defualt argument for uniformly_sample...it's fine I swear
    """
    finished_times = {}
    un_finished_times = {}
    for color_set in sampling_func(adj, **sample_func_args):
        graph_nodes = make_graph(adj, colored_nodes=color_set)
        prop_time, is_finished = run_forcing(graph_nodes)
        if is_finished:
            finished_times[len(color_set)] = finished_times.get(len(color_set), []) + [prop_time]
        else:
            un_finished_times[len(color_set)] = un_finished_times.get(len(color_set), []) + [prop_time]
        if data_collector_obj:
            data_collector_obj.each_run(color_set, graph_nodes, prop_time, is_finished)
    if data_collector_obj:
        data_collector_obj.finish()
    return finished_times, un_finished_times

def exhaustively_sample(adj):
    max_num = 1<<len(adj)
    for bitstring in range(1, max_num): # iterating through all possible bitstrings of length of # of nodes
        colored = []
        for idx in range(len(adj)):
            if bitstring & (1<<idx): # 1<<idx creates a num where the bit at idx is 1, '&' will output 0 if the bitstring does not have a 1 at that idx
                colored.append(idx)
        yield colored

def uniformly_sample(adj, sample_num=10000):
    finished_times = {}
    un_finished_times = {}
    proto_graphs = []
    proto_proto_graphs = set()
    num_possibilities = 2**len(adj)
    sample_num = min(sample_num, num_possibilities)
    while len(proto_proto_graphs) < sample_num:
        proto_proto_graphs.add(random.randint(0,num_possibilities))
    for bitstring in proto_proto_graphs: # iterating through all possible bitstrings of length of # of nodes
        colored = []
        for idx in range(len(adj)):
            if bitstring & (1<<idx): # 1<<idx creates a num where the bit at idx is 1, '&' will output 0 if the bitstring does not have a 1 at that idx
                colored.append(idx)
        yield colored

def one_size_exhaustively_sample(adj, set_size=1):
    pass


def import_graph(fname):
    graph_deets = json.load(open(fname))
    matrix = graph_deets["adjacency_matrix"]
    return graph_deets, matrix

def export_graph(fname, graph_deets, graph_nodes):
    adj, labels = make_adj(graph_nodes)
    graph_deets["labeling"] = labels
    json.dump(graph_deets, open(fname, 'w'))

if __name__ == '__main__':
    # graph = make_graph([[0,1,0,0,0,0,0,0,0,0,0],[1,0,1,0,0,0,0,0,0,0,0],[0,1,0,1,0,0,0,0,0,0,0],[0,0,1,0,1,0,0,0,0,0,0],[0,0,0,1,0,1,0,0,0,0,0],[0,0,0,0,1,0,1,0,0,0,0],[0,0,0,0,0,1,0,1,0,0,0],[0,0,0,0,0,0,1,0,1,0,0],[0,0,0,0,0,0,0,1,0,1,0],[0,0,0,0,0,0,0,0,1,0,1],[0,0,0,0,0,0,0,0,0,1,0]], num_colored=3)
    # print(run_forcing(graph))
    # print_json(*make_adj(graph))
    # exhaustively_test()
    adj=[[0,1,0,0,1,0,0,0,0,0,0,0],[1,0,1,0,0,1,0,0,0,0,0,0],[0,1,0,1,0,0,1,0,0,0,0,0],[0,0,1,0,0,0,0,1,0,0,0,0],[1,0,0,0,0,1,0,0,1,0,0,0],[0,1,0,0,1,0,1,0,0,1,0,0],[0,0,1,0,0,1,0,1,0,0,1,0],[0,0,0,1,0,0,1,0,0,0,0,1],[0,0,0,0,1,0,0,0,0,1,0,0],[0,0,0,0,0,1,0,0,1,0,1,0],[0,0,0,0,0,0,1,0,0,1,0,1],[0,0,0,0,0,0,0,1,0,0,1,0]]

    graph_obj, matrix = import_graph("test_graph.json")
    graph = make_graph(matrix)
    print(run_forcing(graph))
    export_graph("test_graph_after.json",graph_obj, graph)

    print(test_until_stable(adj, uniformly_sample))

    # graph_obj, nodes = import_graph("test_graph.json")
    # print(run_forcing(graph))
    # export_graph("test_graph_after.json",graph_obj, nodes)
