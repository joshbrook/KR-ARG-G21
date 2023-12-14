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

    opp in arguments or sys.exit("Argument not found in the argumentation framework.\n")
    for arg in props:
        if [opp, arg] in attacks:
            if opp in opps:
                sys.exit("Your chosen argument has already been used.")
            opps.append(opp)
            return opps

    sys.exit("Your chosen argument does not attack any of the proponent's previous arguments.\n")    


def respond(opp, opps, arguments, attacks, props):
    """Respond to the opponent's argument."""

    random.shuffle(arguments)
    for arg in arguments:

        if [arg, opp] in attacks and arg not in opps:
            print("The proponent attacks your argument with: " + arg)
            props.append(arg)
            return props
        
    sys.exit("The proponent cannot attack your argument.\nYou win!\n")


def main():
    args = sys.argv[1:]
    if len(args) != 2:
        print('Usage: python preferred_discussion.py <infile> <argument>\n')
        sys.exit(1)
    else:
        infile = args[0]
        argument = args[1]

        with open(infile) as f:
            data = json.load(f)
        
            arguments = list(data['Arguments'].keys())
            attacks = data['Attack Relations']

            if argument not in arguments:
                sys.exit("Argument not found in the argumentation framework.\n")

            # show_graph(attacks, arguments)

            print()
            print("The Argumentation Framework")
            print("Arguments: " + str(list(arguments)))
            print("Attacks: " + str([a + " -> " + b for a, b in attacks]))
            print()
            print("Round 1")
            print("Proponent's Chosen Argument: " + argument)

            props = [argument]
            opps = []
            play = True
            i = 1

            while play:
                opp = input("Choose an attacking argument: ")
                opps = check_argument(arguments, attacks, opp, props, opps)
                
                print("Proponent's Used Arguments:", props)
                print("Arguments You've Used:", opps)
                print()

                if opp in props:
                    sys.exit("You show that the proponent's argument contradicts itself.\nYou win!\n")

                print("Round " + str(i + 1))

                props = respond(opp, opps, arguments, attacks, props)

                i += 1



# sys.argv[1:] = ["input/ex0.json", "1"]
# main()


if __name__ == "__main__":
    main()
