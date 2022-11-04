start = ""
terminals = []
nonterminals = []
symbols = []
error = 0
G = {}
C = {}

first_seen = []
follow_seen = []

grammars = open("grammar.txt")
parse_table = [[""] for c in range(len(terminals) + len(nonterminals) + 1) for r in range(len(C))]


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
    for heads in list(G):
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
        item_len = len(J) + sum(len(v) for v in J.values())
        for heads in list(J):
            for productions in J[heads]:
                dotPos = productions.index(".")
                if dotPos + 1 < len(productions):
                    production_after_dot = productions[dotPos + 1]
                    if production_after_dot in nonterminals:
                        for production in G[production_after_dot]:
                            item = ["."] + production
                            if production_after_dot not in list(J):
                                J[production_after_dot] = [item]
                            elif item not in J[production_after_dot]:
                                J[production_after_dot].append(item)
        if item_len == len(J) + sum(len(v) for v in J.values()):
            return J


# function to calculate GOTO state at nonterminal X from state I

def GOTO(I, X):
    goto = {}
    for heads in list(I):
        for productions in I[heads]:
            for i in range(len(productions) - 1):
                if "." == productions[i] and X == productions[i + 1]:
                    temp_prods = productions[:]
                    temp_prods[i], temp_prods[i + 1] = temp_prods[i + 1], temp_prods[i]
                    prod_closure = CLOSURE({heads: [temp_prods]})
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
        item_len = len(C) + sum(len(v) for v in C.values())
        for I in list(C):
            for X in symbols:
                if GOTO(C[I], X) and GOTO(C[I], X) not in C.values():
                    C['I' + str(i)] = GOTO(C[I], X)
                    i += 1
        if item_len == len(C) + sum(len(v) for v in C.values()):
            return


# function to parse the input string

def ACTION(i, a):
    global error
    for heads in C["I" + str(i)]:
        for productions in C["I" + str(i)][heads]:
            for j in range(len(productions) - 1):
                if productions[j] == "." and productions[j + 1] == a:
                    for k in range(len(C)):
                        if GOTO(C["I" + str(i)], a) == C["I" + str(k)]:
                            if a in terminals:
                                if "r" in parse_table[i][terminals.index(a)]:
                                    if error != 1:
                                        print("ERROR: SHIFT-REDUCE conflict at state " + str(i) + ", symbol\'" + str(
                                            terminals.index((a))) + "\'")
                                    error = 1
                                    if "s" + str(k) not in parse_table[i][terminals.index(a)]:
                                        parse_table[i][terminals.index(a)] = parse_table[i][
                                                                                 terminals.index(a)] + "/s" + str(k)
                                    return parse_table[i][terminals.index(a)]

                                else:
                                    parse_table[i][terminals.index(a)] = "s" + str(k)
                            else:
                                parse_table[i][len(terminals) + nonterminals.index(a)] = str(k)
                            return "s" + str(k)

    for heads in C["I" + str(i)]:
        if heads != start:
            for productions in C['I' + str(i)][heads]:
                if productions[-1] == '.':  # final item
                    k = 0
                    for head in list(G):
                        for Gproductions in G[head]:
                            if head == heads and (Gproductions == productions[:-1]) and (a in terminals or a == "$"):
                                for terms in FOLLOW(heads):
                                    if terms == "$":
                                        index = len(terminals)
                                    else:
                                        index = terminals.index(terms)

                                    if "s" in parse_table[i][index]:
                                        if error != 1:
                                            print(
                                                "ERROR: SHIFT-REDUCE conflict at state " + str(i) + ", symbol \'" + str(
                                                    terms) + "\'")
                                        error = 1
                                        if "r" + str(k) not in parse_table[i][index]:
                                            parse_table[i][index] = parse_table[i][index] + "/r" + str(k)
                                        return parse_table[i][index]
                                    elif parse_table[i][index] and parse_table[i][index] != "r" + str(k):
                                        if error != 1:
                                            print("ERROR: REDUCE-REDUCE conflict at state " + str(
                                                i) + ", symbol \'" + str(
                                                terms) + "\'")
                                        error = 1
                                        if "r" + str(k) not in parse_table[i][index]:
                                            parse_table[i][index] = parse_table[i][index] + "/r" + str(k)
                                        return parse_table[i][index]
                                    else:
                                        parse_table[i][index] = "r" + str(k)
                                    return "r" + str(k)
                                k += 1
    if start in C['I' + str(i)] and G[start][0] + ['.'] in C['I' + str(i)][start]:
        parse_table[i][len(terminals)] = "acc"
        return "acc"
    return ""


# function to parse the grammar

def parse_grammar():
    global G, start, terminals, nonterminals, symbols
    for line in grammars:
        line = " ".join(line.split())
        if line == "\n":
            break
        head = line[:line.index("->")].strip()
        prods = [l.strip().split(' ') for l in ''.join(line[line.index("->") + 2:]).split('|')]
        if not start:
            start = head + "'"
            G[start] = [[head]]
            nonterminals.append(start)
        if head not in G:
            G[head] = []
        if head not in nonterminals:
            nonterminals.append(head)
        for prod in prods:
            G[head].append(prod)
            for char in prod:
                if not char.isupper() and char not in terminals:
                    terminals.append(char)
                elif char.isupper() and char not in nonterminals:
                    nonterminals.append(char)
                    G[char] = []  # nonterminals dont produce other symbols
    symbols = nonterminals + terminals


# function to display

def print_info():
    print("GRAMMAR:")
    for head in list(G):
        if head == start:
            continue
        print("{:>{width}} ->".format(head, width=len(max(G.keys(), key=len))))
        num_prods = 0
        for prods in G[head]:
            if num_prods > 0:
                print("|"),
            for prod in prods:
                print(prod),
            num_prods += 1
        print()
    print("\nAUGMENTED GRAMMAR:")
    i = 0
    for head in G.keys():
        for prods in G[head]:
            print("{:>{width}}:".format(str(i), width=len(str(sum(len(v) for v in G.values()) - 1))))
            print ("{:>{width}} ->".format(head, width=len(max(G.keys(), key=len))))
            for prod in prods:
                print(prod)
            print()
            i += 1
    print("\nTERMINALS   :", terminals)
    print("NON-TERMINALS:", nonterminals)
    print("SYMBOLS     :", symbols)
    print("\nFIRST:")
    for head in G:
        print("{:>{width}} =".format(head, width=len(max(G.keys(), key=len)))),
        print("{"),
        num_terms = 0
        for terms in FIRST(head):
            if num_terms > 0:
                print(", "),
            print(terms),
            num_terms += 1
        print("}")

    print("\nFOLLOW:")
    for head in G:
        print("{:>{width}} =".format(head, width=len(max(G.keys(), key=len))))
        print("{")
        num_terms = 0
        for terms in FOLLOW(head):
            if num_terms > 0:
                print(", "),
            print(terms),
            num_terms += 1
        print("}")

    print("\nITEMS:")
    for i in range(len(C)):
        print ('I' + str(i) + ':')
        for keys in C['I' + str(i)]:
            for prods in C['I' + str(i)][keys]:
                print ("{:>{width}} ->".format(keys, width=len(max(G.keys(), key=len))))
                for prod in prods:
                    print(prod)
                print()
        print()

    for i in range(len(parse_table)):       #len gives number of states
        for j in symbols:
            ACTION(i, j)

    print("PARSING TABLE:")
    print("+" + "--------+" * (len(terminals) + len(nonterminals) + 1))
    print("|{:^8}|".format('STATE'))
    for terms in terminals:
        print("{:^7}|".format(terms))
    print("{:^7}|".format("$"), end=' ')
    for nonterms in nonterminals:
        if nonterms == start:
            continue
        print("{:^7}|".format(nonterms), end=' ')
    print("\n+" + "--------+" * (len(terminals) + len(nonterminals) + 1))
    for i in range(len(parse_table)):
        print("|{:^8}|".format(i), end=' ')
        for j in range(len(parse_table[i]) - 1):
            print("{:^7}|".format(parse_table[i][j]), end=' ')
        print()
    print("+" + "--------+" * (len(terminals) + len(nonterminals) + 1))


def process_input():
    get_input = input("\nEnter Input: ")
    to_parse = " ".join((get_input + " $").split()).split(" ")
    pointer = 0
    stack = ['0']

    print("\n+--------+----------------------------+----------------------------+----------------------------+")
    print("|{:^8}|{:^28}|{:^28}|{:^28}|".format("STEP", "STACK", "INPUT", "ACTION"))
    print("+--------+----------------------------+----------------------------+----------------------------+")

    step = 1
    while True:
        curr_symbol = to_parse[pointer]
        top_stack = int(stack[-1])
        stack_content = ""
        input_content = ""

        print("|{:^8}|".format(step), end=' ')
        for i in stack:
            stack_content += i
        print("{:27}|".format(stack_content), end=' ')
        i = pointer
        while i < len(to_parse):
            input_content += to_parse[i]
            i += 1
        print("{:>26} | ".format(input_content), end=' ')

        step += 1
        get_action = ACTION(top_stack, curr_symbol)
        if "/" in get_action:
            print("{:^26}|".format(get_action + ". So conflict"))
            break
        if "s" in get_action:
            print("{:^26}|".format(get_action))
            stack.append(curr_symbol)
            stack.append(get_action[1:])
            pointer += 1
        elif "r" in get_action:
            print("{:^26}|".format(get_action))
            i = 0
            for head in list(G):
                for prods in G[head]:
                    if i == int(get_action[1:]):
                        for j in range(2 * len(prods)):
                            stack.pop()
                        state = stack[-1]
                        stack.append(head)
                        stack.append(parse_table[int(state)][len(terminals) + nonterminals.index(head)])
                    i += 1
        elif get_action == "acc":
            print("{:^26}|".format("ACCEPTED"))
            break
        else:
            print("ERROR: Unrecognized symbol", curr_symbol, "|")
            break
    print("+--------+----------------------------+----------------------------+----------------------------+")
