import json
import sys
import networkx as nx
import matplotlib.pyplot as plt


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


def main():
    args = sys.argv[1:]
    if len(args) != 2:
        print('Usage: python main.py <infile> <argument>')
        sys.exit(1)
    else:
        infile = args[0]
        argument = args[1]

        with open(infile) as f:
            data = json.load(f)
        
            arguments = data['Arguments']
            attacks = data['Attack Relations']

            argument in arguments or sys.exit("Argument not found in the argumentation framework.")

            show_graph(attacks, arguments)

            print("Arguments: " + str(list(arguments.keys())))
            attacks = [str(list(arguments.keys()).index(a)) + " -> " + str(list(arguments.keys()).index(b)) for a, b in attacks]
            print("Attacks: " + str(attacks))




if __name__ == "__main__":
    main()