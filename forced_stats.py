from forced_graph import exhaustively_test_until_stable, sample_test_until_stable

import matplotlib.pyplot as plt
import math
import numpy as np
from collections import Counter

def exhaustive_test_until_stable_graph(times):
    means = {}
    for size, propagations in times.items():
        means[size] = sum(propagations) / len(propagations)
    print(means)

    variations = {}
    for size, propagations in times.items():
        m = means[size]
        variations[size] = math.sqrt(sum([(p-m)*(p-m) for p in propagations]) / len(propagations))
    print(variations)


    # plotting the actual times
    all_props = [(num_colored, time) for num_colored, prop_times in times.items() for time in prop_times]
    # plt.scatter([num for num, _ in all_props], [time for _, time in all_props])

    # plotting means
    means_list = [(num_colored, mean_time) for num_colored, mean_time in means.items()]
    # plt.scatter([num for num, _ in means_list], [time for _, time in means_list])

    print([[(num, np.percentile(times[num], 25)) for num, _ in means_list], [(num, np.percentile(times[num], 75)) for num, _ in means_list]])

    plt.errorbar(x=[num for num, _ in means_list], y=[time for _, time in means_list],
        yerr=[[mean-np.percentile(times[num], 25) for num, mean in means_list], [np.percentile(times[num], 75)-mean for num, mean in means_list]])

    plt.grid(True)
    plt.show()

def hist_one_size(times, set_size, num_vertices, secondary_times=None, percentage=False):
    count= Counter(times.get(set_size,[]))
    count_secondary = Counter()
    if secondary_times:
        count_secondary = Counter(secondary_times.get(set_size, []))

    nums = list(range(num_vertices-set_size+1))
    vals = [count[n] for n in nums]
    vals_secondary = [count_secondary[n] for n in nums]
    total = sum(vals) + sum(vals_secondary)

    if percentage:
        vals = [v/total for v in vals]
        vals_secondary = [v/total for v in vals_secondary]

    plt.bar(nums, vals)
    plt.bar(nums, vals_secondary, bottom=vals)

    title_str = "size "+str(set_size)
    if percentage:
        title_str += " (" + str(total) + " sets)"
    plt.title(title_str)
    plt.ylabel("number of sets")
    plt.xlabel("propogation time")
    plt.xlim(0, num_vertices)
    plt.xticks(range(0, num_vertices,2))

def hist_all_sizes(times, set_size, num_vertices, secondary_times=None, percentage=False):
    plt.suptitle("Distribution of propogation times for different sizes of forcing sets")
    ax = plt.subplot(2,6,1)
    hist_one_size(times, 1, 12, secondary_times=secondary_times, percentage=percentage)
    for size in range(2, 12):
        plt.subplot(2,6,size, sharey=ax)
        hist_one_size(times, size, 12, secondary_times=secondary_times, percentage=percentage)
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                wspace=0.5, hspace=0.4)
    plt.show()

if __name__ == '__main__':
    adj=[[0,1,0,0,1,0,0,0,0,0,0,0],[1,0,1,0,0,1,0,0,0,0,0,0],[0,1,0,1,0,0,1,0,0,0,0,0],[0,0,1,0,0,0,0,1,0,0,0,0],[1,0,0,0,0,1,0,0,1,0,0,0],[0,1,0,0,1,0,1,0,0,1,0,0],[0,0,1,0,0,1,0,1,0,0,1,0],[0,0,0,1,0,0,1,0,0,0,0,1],[0,0,0,0,1,0,0,0,0,1,0,0],[0,0,0,0,0,1,0,0,1,0,1,0],[0,0,0,0,0,0,1,0,0,1,0,1],[0,0,0,0,0,0,0,1,0,0,1,0]]
    finished_times, un_finished_times = sample_test_until_stable(adj)
    print(finished_times)
    # print(finished_times,un_finished_times)
    hist_all_sizes(finished_times, 1, 12, secondary_times=un_finished_times, percentage=True)
