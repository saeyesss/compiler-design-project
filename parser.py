start = ""
terminals = []
nonterminals = []
symbols = []
error = 0
G = {}
C = {}

first_seen = []
follow_seen = []


# function to calculate FIRST set of any input symbol X

def FIRST(X):
    global first_seen
    first = []
    if X in terminals:
        first.append(X)
    elif X in nonterminals:
        for productions in G[X]:
            if productions[0] in terminals and productions[0] not in first:
                first.append(productions[0])
            else:
                for nonterminal in productions:
                    if nonterminal not in first_seen:
                        for terms in FIRST(nonterminal):
                            if terms not in first:
                                first.append(terms)

    first_seen.remove(X)
    return first


# function to calculate FOLLOW set of any input symbol X

def FOLLOW(X):
    global follow_seen
    follow = []
    follow_seen.append(X)

    if X == start:
        follow.append("$")
    for heads in G.keys():
        for productions in G[heads]:
            follow_head = False
            if X in productions:
                next_symbol_pos = productions.index(X) + 1
                if next_symbol_pos < len(productions):
                    for terms in FIRST(productions[next_symbol_pos]):
                        if terms not in follow:
                            follow.append(terms)
    follow_seen.remove(X)
    return follow


# function to calculate closure of a nonterminal symbol

def CLOSURE(X):
    J = X
    while True:
        item_len = len(J) + sum(len(v) for v in J.itervalues())
        for heads in J.keys():
            for productions in J[heads]:
                dotPos = productions.index(".")
                if dotPos + 1 < len(productions):
                    production_after_dot = productions[dotPos + 1]
                    if production_after_dot in nonterminals:
                        for production in G[production_after_dot]:
                            item = ["."] + production
                            if production_after_dot not in J.keys():
                                J[production_after_dot] = [item]
                            elif item not in J[production_after_dot]:
                                J[production_after_dot].append(item)
        if item_len == len(J) + sum(len(v) for v in J.itervalues()):
            return J


# function to calculate GOTO state at nonterminal X from state I
def GOTO(I, X):
    goto = {}
    for heads in I.keys():
        for productions in I[heads]:
            for i in range(len(productions) - 1):
                if "." == productions[i] and X == productions[i + 1]:
                    temp_prods = productions[:]
                    temp_prods[i], temp_prods[i + 1] = temp_prods[i + 1], temp_prods[i]
                    prod_closure = closure({heads: [temp_prods]})
                    for keys in prod_closure:
                        if keys not in goto.keys():
                            goto[keys] = prod_closure[keys]
                        elif prod_closure[keys] not in goto[keys]:
                            for prod in prod_closure[keys]:
                                goto[keys].append(prod)
    return goto

# function to calculate set of canonical items
def items():
    global C
    i = 1
    C = {'I0': CLOSURE({start: [['.'] + G[start][0]]})}
    while True:
        item_len = len(C) + sum(len(v) for v in C.itervalues())
        for I in C.keys():
            for X in symbols:
                if GOTO(C[I], X) and GOTO(C[I], X) not in C.values():
                    C['I' + str(i)] = GOTO(C[I], X)
                    i += 1
        if item_len == len(C) + sum(len(v) for v in C.itervalues()):
            return

