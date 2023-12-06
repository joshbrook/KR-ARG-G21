import json
import sys
import random
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


def check_argument(arguments, attacks, opp, props, opps):
    """Check if the argument is acceptable."""

    opp in arguments or sys.exit("Argument not found in the argumentation framework.")
    for arg in props:
        if [opp, arg] in attacks:
            opp in opps and sys.exit("Your chosen argument has already been used.")
            opps.append(opp)
            return opps

    sys.exit("Your chosen argument does not attack any of the proponent's previous arguments.")    


def respond(opp, opps, arguments, attacks, props):
    """Respond to the opponent's argument."""

    random.shuffle(arguments)
    for arg in arguments:
        if [arg, opp] in attacks and arg not in opps:
            print("The proponent attacks your argument with: " + arg)
            props.append(arg)
            return props
        
    sys.exit("The proponent cannot attack your argument.\nYou win!")


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
        
            arguments = list(data['Arguments'].keys())
            attacks = data['Attack Relations']

            argument in arguments or sys.exit("Argument not found in the argumentation framework.")

            show_graph(attacks, arguments)

            print("Arguments: " + str(list(arguments)))
            print("Attacks: " + str([a + " -> " + b for a, b in attacks]))
            print("Round 1")
            print("Proponent's Chosen Argument: " + argument)

            props = [argument]
            opps = []
            play = True

            while play:
                opp = input("Choose an attacking argument: ")
                opps = check_argument(arguments, attacks, opp, props, opps)
                
                print("Proponent's Used Arguments:", props)
                print("Arguments You've Used:", opps)

                props = respond(opp, opps, arguments, attacks, props)


# sys.argv[1:] = ["input/ex0.json", "1"]
# main()


if __name__ == "__main__":
    main()
