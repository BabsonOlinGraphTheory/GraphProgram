import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def color_and_show_nodes(graphx, location_data, node_labeling, values=[1,2], colors=['r','b']):
	for idx in range(len(values)):
		nx.draw_networkx_nodes(graphx, location_data,
		nodelist=[node_idx for node_idx, val in enumerate(node_labeling) if val == values[idx]],
		node_color=colors[idx],
		node_size=500)

def show_edges(graphx, location_data):
	nx.draw_networkx_edges(graphx, location_data)

def draw(graphx, labeling_list):
	for labeling in labeling_list:
		plt.figure()
		color_and_show_nodes(graphx, node_positions, labeling)
		show_edges(graphx, node_positions)
		plt.axis('off')
		plt.show()

if __name__ == "__main__":
	input_graph = {"adjacency_matrix":[[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]],"location_data":[{"x":140.75,"y":234},{"x":244.75,"y":238},{"x":142.75,"y":346},{"x":247.75,"y":342}],"labeling":[1,1,2,2]}

	node_positions = [[node['x'], node['y']] for node in input_graph["location_data"]]
	node_labeling = input_graph["labeling"]
	adjacency_matrix = input_graph["adjacency_matrix"]

	# Make networkx graph
	adj = np.matrix(adjacency_matrix)
	graphx = nx.from_numpy_matrix(adj)

	draw(graphx, [node_labeling, [1,1,1,1],[2,2,2,2]])
