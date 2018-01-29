import utils
from collections import defaultdict
import sys


def gll_method(grammar_filename, graph_filename, out=None, test=False):
    graph = utils.get_graph(graph_filename)
    grammar = utils.get_grammar_automata(grammar_filename)
    gss = defaultdict(lambda: defaultdict(set))
    popped = defaultdict(list)
    q = set()
    used = set()
    res = []
    fins = []

    for it in grammar.f.values():
        for element in it:
            fins.append(element)

    for i in range(len(graph)):
        for j in grammar.s:
            for k in grammar.s[j]:
                q.add((i, k, (j, i)))

    while q:
        conf = q.pop()
        if (conf[0], conf[1], conf[2]) in used:
            continue
        used.add((conf[0], conf[1], conf[2]))

        if conf[1] in fins:
            q.update((conf[0], x, j) for j in gss[conf[2]] for x in gss[conf[2]][j])
            res.append((conf[2][1], conf[2][0], conf[0]))
            popped[conf[2]].append(conf[0])
        for i, labels_grammar in enumerate(grammar.g[conf[1]]):
            for j, lbls_graph in enumerate(graph[conf[0]]):

                for lbl_grammar in labels_grammar:
                    if lbl_grammar not in grammar.t:
                        gss[(lbl_grammar, conf[0])][conf[2]].add(i)
                        gss_node = (lbl_grammar, conf[0])
                        for st in grammar.s[lbl_grammar]:
                            q.add((conf[0], st, gss_node))

                        if gss_node in popped:
                            for v in popped[gss_node]:
                                if (v, i, conf[2]) not in used:
                                    q.add((v, i, conf[2]))
                    for lbl_graph in lbls_graph:
                        if lbl_grammar == lbl_graph and lbl_grammar in grammar.t:
                            q.add((j, i, conf[2]))

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
        gll_method(sys.argv[1], sys.argv[2], out=sys.argv[3])
    elif len(sys.argv) == 3:
        gll_method(sys.argv[1], sys.argv[2])
    else:
        print('Wrong numbers of arguments. Should be: '
              'python3 matrix_method.py [automaton] [grammar] [output]')
