import sys, os
import forced_graph
import forced_stats
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

""" Data Collectors """

class UnfinishedForcingSets(forced_graph.DataCollector):
    def __init__(self, graph_json_obj, output_dir):
        self.unfinished_sets = []
        self.json = graph_json_obj
        self.output_dir = output_dir
        self.nodes_list = None
        self.count = 0

    def each_run(self, color_set, nodes_list, prop_time, is_finished):
        self.count += 1
        if self.count % 10000 == 0:
            print(self.count)
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

sns.set(style="white", color_codes=True)

class DataFrameCollector(forced_graph.DataCollector):
    def __init__(self):
        self.columns = ['size','time','finished']
        self.df = pd.DataFrame(columns=self.columns)

    def each_run(self, color_set, nodes_list, prop_time, is_finished):
        current = pd.DataFrame([[len(color_set), prop_time, is_finished]], columns=self.columns)
        self.df = self.df.append(current, ignore_index=True)

    def finish(self):
        sns.stripplot(x='size', y='time', hue='finished', data=self.df, jitter=True)
        plt.show()

class MultiDataCollector(forced_graph.DataCollector):
    def __init__(self, collectorlist):
        self.collectorlist = collectorlist

    def each_run(self, color_set, nodes_list, prop_time, is_finished):
        for c in self.collectorlist:
            c.each_run(color_set, nodes_list, prop_time, is_finished)

    def finish(self):
        for c in self.collectorlist:
            c.finish()

""" 
    Functions that use the data collectors
        Each function takes a filename (json of the graph), 
        a sampling function to use, and optional args to the sampling function
"""

def stripplot(fname, sample_func, sample_func_args={}):
    """ Creates a strip plot """
    graph_obj, matrix = forced_graph.import_graph(fname)
    data_collector = DataFrameCollector()
    finished_times, un_finished_times = forced_graph.test_until_stable(matrix, sample_func, 
        data_collector_obj = data_collector, sample_func_args=sample_func_args)

def write_unfinished(fname, sample_func, sample_func_args={}):
    """ Writes unfinished forcing sets to a folder """
    graph_obj, matrix = forced_graph.import_graph(fname)
    output_dir = fname.split(".")[0]
    data_collector = UnfinishedForcingSets(graph_obj, output_dir)
    finished_times, un_finished_times = forced_graph.test_until_stable_parallel(matrix, sample_func, 
        data_collector_obj = data_collector, sample_func_args=sample_func_args)

def stripplot_and_write_unfinished(fname, sample_func, sample_func_args={}):
    """ Does both `stripplot()` and `write_unfinished()` as above """
    graph_obj, matrix = forced_graph.import_graph(fname)
    output_dir = fname.split(".")[0]
    stripplotter = DataFrameCollector()
    forcingset_writer = UnfinishedForcingSets(graph_obj, output_dir)
    data_collector = MultiDataCollector((stripplotter, forcingset_writer))
    finished_times, un_finished_times = forced_graph.test_until_stable(matrix, sample_func, 
        data_collector_obj = data_collector, sample_func_args=sample_func_args)

""" MAIN """

if __name__ == '__main__':
    fname = 'test_graph_3x4.json'
    if len(sys.argv) > 1:
        fname = sys.argv[1]

    # REFERENCE (as of 03-11-2018)
    # sample funcs: 
        # forced_graph.exhaustively_sample 
        # forced_graph.uniformly_sample 
            # sample_num
        # forced_graph.one_size_exhaustively_sample
            # set_size
    write_unfinished(fname, forced_graph.one_size_exhaustively_sample, sample_func_args={"set_size":21})