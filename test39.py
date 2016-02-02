from labeling import Labeling
from graph import Graph
from labeler import LPolynomialLabeler
from tabulate import tabulate

def phi(n):
    l = n // 4
    r = n % 4
    if r ==2:
        return l + 4
    return l + 3

def near_distance_cycle(n, di=None, fi=None):
    diam = n//2
    f_sum = phi(n)
    d_sum = 2 * diam - f_sum + 4
    cycle = [i*d_sum % n for i in range(n)]
    if di == None or fi == None:
        di, fi = di_and_fi_from_cycle(cycle)
    graph = Graph.new_cycle(n)
    labeler = LPolynomialLabeler(constraints=tuple(reversed(range(1, diam+2))))

    labels = [0] * n
    index = 0
    label = 0

    for i in range(n - 1):
        d = di[i]
        f = fi[i]
        index = (index + d) % n
        label += f
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

def di_and_fi_from_cycle(cycle):
    n = len(cycle)
    diam = n//2
    f_sum = phi(n)
    d_sum = 2 * diam - f_sum + 4
    firsts = cycle[:diam-1]
    middle = cycle[diam-1:diam+3]
    lasts = cycle[diam+3:]
    d1 = lasts[0] % n
    d2 = (middle[2] - firsts[-1]) % n
    di = (d1, d_sum - d1, d2, d_sum - d2)
    fi = tuple(diam + 2 - d for d in di)
    return (di, fi)

if __name__ == '__main__':
    di = [19, 11] * 12
    di.extend([19, 10])
    di.extend([15] * 12)
    fi = [2, 10] * 12
    fi.extend([2, 11])
    fi.extend([6] * 12)
    near_distance_cycle(39, di, fi)
    max_n = 50
    #for k in xrange(1, 17):
        #near_distance_cycle(4 * k + 3)
