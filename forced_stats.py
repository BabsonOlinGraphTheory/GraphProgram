from forced_graph import exhaustively_test_until_stable

import matplotlib.pyplot as plt
import math
import numpy as np

def exhaustive_test_until_stable_graph():
    times = exhaustively_test_until_stable()


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

def hist_one_size(times):
    pass
    # >>> from forced_graph import exhaustively_test_until_stable
# >>> times = exhaustively_test_until_stable()
# >>> 
# >>> from collections import Counter
# >>> count6= Counter(times[6])
# >>> import matplotlib.pyplot as plt
# >>> nums = list(count6.elements())
# >>> vals = [count6[n] for n in nums]
# >>> plt.bar(nums, vals)
# <Container object of 924 artists>
# >>> plt.show()


if __name__ == '__main__':
    result = exhaustive_test_until_stable_graph()

