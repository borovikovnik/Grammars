from utils import get_graph, get_grammar_automata
import sys


def dfs(graph, grammar, stars, used):
    changed = False
    first_graph, first_grammar = used[0]
    last_graph, last_grammar = used[-1]

    if last_grammar in grammar.f[stars]:
        if stars not in graph[first_graph][last_graph]:
            graph[first_graph][last_graph].append(stars)
            changed = True

    for curr_last_graph in range(len(graph[last_graph])):
        if not graph[last_graph][curr_last_graph]:
            continue

        labels_graph = graph[last_graph][curr_last_graph]
        for curr_last_grammar, labels_grammar in enumerate(grammar.g[first_grammar]):
            for label_grammar in grammar.g[last_grammar][curr_last_grammar]:
                if label_grammar in labels_graph:
                    if (curr_last_graph, curr_last_grammar) not in used:
                        curr_used = used[:]
                        curr_used.append((curr_last_graph, curr_last_grammar))

                        changed |= dfs(graph, grammar, stars, curr_used)
    return changed


def glr_method(grammar_path, graph_path, out=None, test=False):
    graph = get_graph(graph_path)
    grammar = get_grammar_automata(grammar_path)
    size = len(graph)
    changed = True

    while changed:
        changed = False
        for start in grammar.s:
            for i in range(size):
                for start_grammar in grammar.s[start]:
                    changed |= dfs(graph, grammar, start, [(i, start_grammar)])

    res = []
    for i in range(size):
        for j in range(size):
            for N in graph[i][j]:
                if N in grammar.s:
                    res.append((i, N, j))

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
        glr_method(sys.argv[1], sys.argv[2], out=sys.argv[3])
    elif len(sys.argv) == 3:
        glr_method(sys.argv[1], sys.argv[2])
    else:
        print('Wrong numbers of arguments. Should be: '
              'python3 glr_method.py [automaton] [grammar] [output]')
