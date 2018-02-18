import sys
import forced_graph
import forced_stats

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fname = sys.argv[1]
        graph_obj, matrix = forced_graph.import_graph(fname)
        finished_times, un_finished_times = forced_graph.exhaustively_test_until_stable(matrix)
        forced_stats.hist_all_sizes(finished_times, len(matrix), secondary_times=un_finished_times, percentage=True)

    else:
        print("You must pass in a json file as an argument")