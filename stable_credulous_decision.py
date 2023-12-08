import json
import sys
import random
import networkx as nx
import matplotlib.pyplot as plt
from itertools import chain, combinations


def show_graph(attacks, arguments):
    """Plot a graph of the argumentation framework."""

    G = nx.DiGraph()
    G.add_nodes_from(arguments)
    G.add_edges_from(attacks)
    
    pos = nx.shell_layout(G)
    options = {
        'node_color': '#4dc0fa',
        'node_size': 1500,
        'width': 3,
        'arrowstyle': '->',
        'arrowsize': 15,
        'font_weight': 'bold',
        'font_family': 'Georgia',
        'font_size': 20,
    }

    nx.draw(G, pos, with_labels=True, **options)
    plt.show()

def find_stable_sets(all_attacks, arguments):
    attacks = set(tuple(attack) for attack in all_attacks)

    def powerset(iterable):
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

    def is_conflict_free(subset):
        for arg1 in subset:
            for arg2 in subset:
                if (arg1, arg2) in attacks or (arg2, arg1) in attacks:
                    return False
        return True
    
    def is_attack_complete(subset):
        for arg in (arguments - subset):
            isAttacked = False
            for a in attacks:
                if a[1] == arg and a[0] in subset:
                    isAttacked = True
            if not isAttacked:
                return False
        return True

    stable_sets = []
    for s in powerset(arguments):
        s = set(s)
        if is_conflict_free(s) and is_attack_complete(s):
            stable_sets.append(s)
    
    print('Stable sets: ', stable_sets)
    return stable_sets

def main():
    args = sys.argv[1:]
    if len(args) != 2:
        print('Usage: python stable_credulous_decision.py <infile> <argument>')
        sys.exit(1)
    else:
        infile = args[0]
        argument = args[1]

        with open(infile) as f:
            data = json.load(f)
        
            arguments = set(list(data['Arguments'].keys()))
            attacks = data['Attack Relations']

            argument in arguments or sys.exit("Argument not found in the argumentation framework.")

          #  show_graph(attacks, arguments)

            print("Arguments: " + str(list(arguments)))
            print("Attacks: " + str([a + " -> " + b for a, b in attacks]))
    
    stablesets = find_stable_sets(attacks, arguments)

    for stableset in stablesets:
        if argument in stableset:
            print('YOU SHALL PASS')
            return
    print('YOU SHALL NOT PASS')

        
if __name__ == "__main__":
    main()