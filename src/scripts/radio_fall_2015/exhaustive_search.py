from lib.labeling import Labeling
from lib.graph import Graph
from lib.labeler import LPolynomialLabeler
from tabulate import tabulate

def phi(n):
    l = n // 4
    r = n % 4
    if r ==2:
        return l + 4
    return l + 3

def lower_bound(n):
    r = n % 4
    phi_n = phi(n)
    if r % 2 == 0:
        return ((n-2)/2) * phi_n + 2
    return ((n-1)/2) * phi_n

def main():
    ns = range(3, 14, 1)
    lambdas = []
    labelings = []
    for n in ns:
        print("labeling %d cycle" % n)
        graph = Graph.new_cycle(n)
        diam = n//2
        labeler = LPolynomialLabeler(constraints=tuple(reversed(range(1, diam+3))))
        bound = lower_bound(n)
        labeling = labeler.complete_labeling(graph, None, bound, bound*2)
        lambdas.append(max(labeling.labels))
        labelings.append(labeling.labels)
        print("lambda is %d" % lambdas[-1])
        print("labeling is %s" % labelings[-1])
    table = [ns, lambdas, labelings]
    table = [list(i) for i in zip(*table)]
    print(tabulate(table, headers=["n", "lambda", "labeling"]))
if __name__ == '__main__':
    main()
