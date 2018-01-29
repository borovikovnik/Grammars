import re
from collections import defaultdict


class RFA:
    def __init__(self):
        self.s = defaultdict(list)
        self.f = defaultdict(list)
        self.t = set()
        self.g = []


def get_graph(filename):
    with open(filename) as f:
        lines = f.readlines()
        size = lines[2].count(";")
        Gr = [[[] for i in range(size)] for i in range(size)]
        rules_re = r"(?P<lr>\d*) -> (?P<rr>\d*).*\"(?P<lbl>\w*)\".*"
        rules = re.compile(rules_re)
        for line in lines[2:]:
            res = rules.match(line)
            if res:
                i = int(res.group('lr'))
                j = int(res.group('rr'))
                label = res.group('lbl')
                Gr[int(i)][int(j)].append(label)
    return Gr


def get_grammar_homsky(filename):
    gram = defaultdict(list)
    epsilons = []
    with open(filename) as f:

        lines = f.readlines()
        for line in lines:
            l, r = line.split(' -> ')
            r = r.rstrip('\n')
            gram[l].append(r.split(' '))
            if r == "eps":
                epsilons.append(l)
    return gram, epsilons


def get_grammar_automata(filename):
    grammar = RFA()
    f = open(filename, 'r')
    content = f.readlines()
    f.close()
    size = content[2].count(";")
    grammar.g = [[[] for i in range(size)] for i in range(size)]

    for l in content[3:]:
        line = l.replace(" = ", '=')
        line = re.findall('(\d+)\[label="(\w+)",[\w|=, "]*color="green"\]', line)
        if line:
            state, nonterminal = line[0]
            grammar.s[nonterminal].append(int(state))

    for l in content[3:]:
        line = l.replace(" = ", '=')
        line = re.findall('(\d+)\[label="(\w+)", shape="doublecircle"*', line)
        if line:
            state, nonterminal = line[0]
            grammar.f[nonterminal].append(int(state))

    for l in content[3:]:
        line = l.replace(" -> ", '->').replace(" = ", '=')
        line = re.findall('(\d+)->(\d+)\[label="(\w+|.)"\]', line)
        if line:
            i, j, label = line[0]
            i, j = int(i), int(j)
            grammar.g[i][j].append(label)
            if not label.isupper():
                grammar.t.add(label)
    return grammar


def count_res(res):
    return len(list(filter(lambda x: x[1] == 'S', res)))
