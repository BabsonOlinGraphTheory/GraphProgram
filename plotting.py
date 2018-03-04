import forced_graph
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

if __name__ == "__main__":
    graph_obj, matrix = forced_graph.import_graph('test_graph_3x4.json')
    data_collector = DataFrameCollector()
    finished_times, un_finished_times = forced_graph.test_until_stable(matrix, forced_graph.exhaustively_sample, data_collector_obj = data_collector)
