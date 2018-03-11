import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

class GraphX:
    def __init__(self, input_graph):
        self.node_positions = [[node['x'], node['y']] for node in input_graph["location_data"]]
        self.current_labeling = input_graph["labeling"]
        self.adjacency_matrix = input_graph["adjacency_matrix"]

        # Make networkx graph
        adj = np.matrix(self.adjacency_matrix)
        self.graphx = nx.from_numpy_matrix(adj)

        self.all_labelings = [self.current_labeling]

    def append_labeling(self, new_labeling):
        self.all_labelings.append(new_labeling)

    def color_and_show_nodes(self, labeling, values=[1,2], colors=['r','b']):
        for idx in range(len(values)):
            nx.draw_networkx_nodes(self.graphx, self.node_positions,
                nodelist=[node_idx for node_idx, val in enumerate(labeling) if val == values[idx]],
                node_color=colors[idx],
                node_size=500)

    def show_edges(self):
        print(self.node_positions)
        nx.draw_networkx_edges(self.graphx, self.node_positions)

    def draw(self):#graphx, labeling_list, node_positions):
        for labeling in self.all_labelings:
            plt.figure()
            self.color_and_show_nodes(labeling)
            self.show_edges()
            plt.axis('off')
            plt.show()

if __name__ == "__main__":
    input_graph = {"adjacency_matrix":[[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]],"location_data":[{"x":140.75,"y":234},{"x":244.75,"y":238},{"x":142.75,"y":346},{"x":247.75,"y":342}],"labeling":[1,1,2,2]}

    graphx = GraphX(input_graph)
    for l in [[2,2,2,2],[1,2,2,1],[2,2,1,1]]:
        graphx.append_labeling(l)
    graphx.draw()
    #draw(graphx, [node_labeling, [1,1,1,1],[2,2,2,2]])
