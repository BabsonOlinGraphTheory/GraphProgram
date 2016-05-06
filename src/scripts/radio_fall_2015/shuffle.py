from graphlib.labeling import Labeling
from graphlib.graph import Graph
from graphlib.labeler import LPolynomialLabeler
from tabulate import tabulate

def phi(n):
    l = n // 4
    r = n % 4
    if r ==2:
        return l + 4
    return l + 3

def near_distance_cycle(n):
    diam = n//2
    f_sum = phi(n)
    d_sum = 2 * diam - f_sum + 4
    cycle = [i*d_sum % n for i in range(n)]
    ds, fs = ds_and_fs_from_cycle(cycle)
    change = n - 5
    graph = Graph.new_cycle(n)
    labeler = LPolynomialLabeler(constraints=tuple(reversed(range(1, diam+2))))

    labels = [0] * n
    index = 0
    label = 0
    di = []
    fi = []

    for i in range(n - 1):
        if i % 2 == 0:
            if i < change:
                d = ds[0]
                f = fs[0]
            else:
                d = ds[2]
                f = fs[2]
        else:
            if i < change:
                d = ds[1]
                f = fs[1]
            else:
                d = ds[3]
                f = fs[3]
        index = (index + d) % n
        label += f
        di.append(d)
        fi.append(f)
        labels[index] = label

    labeling = Labeling(labels)
    bound = max(labeling.labels)
    if labeler.confirm_labeling(graph, labeling)[0]:
        print("Valid labeling of %d cycle with max label of %d" % (n, bound))
    else:
        print("Invalid labeling of %d cycle" % n)
    table = [range(n), di + ["-"], fi + ["-"], labeling.labels]
    table = [list(i) for i in zip(*table)]
    print(tabulate(table, headers=["i", "di", "fi", "label"]))

def ds_and_fs_from_cycle(cycle):
    n = len(cycle)
    diam = n//2
    f_sum = phi(n)
    d_sum = 2 * diam - f_sum + 4
    firsts = cycle[:diam-1]
    middle = cycle[diam-1:diam+3]
    lasts = cycle[diam+3:]
    d1 = lasts[0] % n
    d2 = (middle[2] - firsts[-1]) % n
    ds = (d1, d_sum - d1, d2, d_sum - d2)
    fs = tuple(diam + 2 - d for d in ds)
    return (ds, fs)
if __name__ == '__main__':
    #near_distance_cycle(43)
    max_n = 50
    for k in range(1, 17):
        near_distance_cycle(4 * k + 3)
