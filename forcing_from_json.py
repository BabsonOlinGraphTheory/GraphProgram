import sys, os
import forced_graph
import forced_stats

class UnfinishedForcingSets(forced_graph.DataCollector):
    def __init__(self, graph_json_obj, output_dir):
        self.unfinished_sets = []
        self.json = graph_json_obj
        self.output_dir = output_dir
        self.nodes_list = None

    def each_run(self, color_set, nodes_list, prop_time, is_finished):
        if not self.nodes_list:
            self.nodes_list = nodes_list
        if not is_finished:
            self.unfinished_sets.append(color_set)

    def finish(self):
        for n in self.nodes_list:
            n.uncolor() # NOTE: THIS IS NOT A SAFE OPERATION
                        # FIND A BETTER WAY TO COPY ALL THE NODES INTO A NEW LIST SO YOU DON'T CHANGE THE ORIGINAL NODES

        try:
            os.mkdir(self.output_dir)
        except OSError: # directory already exists
            pass

        for color_set in self.unfinished_sets:
            forced_graph.export_graph
            for idx in color_set:
                self.nodes_list[idx].color()

            fname = "{}/unfinishedforcing_size{}_{}.json".format(self.output_dir, len(color_set), "-".join(str(c) for c in color_set))
            forced_graph.export_graph(fname, self.json, self.nodes_list)

            for idx in color_set:
                self.nodes_list[idx].uncolor()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fname = sys.argv[1]
        graph_obj, matrix = forced_graph.import_graph(fname)
        output_dir = fname.split(".")[0]
        data_collector = UnfinishedForcingSets(graph_obj, output_dir)
        finished_times, un_finished_times = forced_graph.test_until_stable(matrix, forced_graph.uniformly_sample, 
            data_collector_obj = data_collector, sample_func_args={"sample_num":100})
        forced_stats.hist_all_sizes(finished_times, len(matrix), secondary_times=un_finished_times, percentage=True)

    else:
        print("You must pass in a json file as an argument")