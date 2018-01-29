import utils
from collections import defaultdict
import sys


def matrix_method(grammar_filename, graph_filename, out=None, test=False):
    graph = utils.get_graph(graph_filename)
    grammar_rules, epsilons = utils.get_grammar_homsky(grammar_filename)
    N = len(graph)
    A = [[[] for i in range(N)] for j in range(N)]
    terms = set()
    transitions = defaultdict(list)

    for key in grammar_rules:
        for rule in grammar_rules[key]:
            lhs = ''.join(x for x in rule)
            transitions[lhs].append(key)
            if len(rule) == 1:
                terms.add(rule[0])

    for i in range(N):
        for j in range(N):
            for element in graph[i][j]:
                if element in terms:
                    A[i][j] += transitions[element]
    for key in epsilons:
        for i in range(N):
            A[i][i].append(key)
    changed = True
    while changed:
        changed = False
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    for part1 in A[i][j]:
                        for part2 in A[j][k]:
                            rule = part1 + part2
                            if rule in transitions:
                                lhs = transitions[rule]
                                for element in lhs:
                                    if element not in A[i][k]:
                                        A[i][k].append(element)
                                        changed = True
    res = []
    for i in range(N):
        for j in range(N):
            for k in A[i][j]:
                res.append((i, k, j))

    if not test:
        if out is None:
            for (i, N, j) in res:
                print(str(i) + ',' + N + ',' + str(j))
        else:
            with open(out, 'w') as f:
                for (i, N, j) in res:
                    f.write(str(i) + ',' + N + ',' + str(j) + '\n')
    return res


if __name__ == '__main__':

    if len(sys.argv) == 4:
        matrix_method(sys.argv[1], sys.argv[2], out=sys.argv[3])
    elif len(sys.argv) == 3:
        matrix_method(sys.argv[1], sys.argv[2])
    else:
        print('Wrong numbers of arguments. Should be: '
              'python3 matrix_method.py [automaton] [grammar] [output_file]')
