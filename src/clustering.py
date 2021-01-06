from src.pathfinding import Pathfinder


def clustering(DIJKSTRA: Pathfinder, nodes, n):
    """
    Clustering method (first try)
    """

    edge_betweenness = {}

    highest_betweenness = ["",0]

    while nodes:
        print(len(nodes), "nodes to explore left")
        starting_node = nodes.pop()

        for target_node in nodes:

            path = DIJKSTRA.get_path(starting_node, target_node)

            if path is not None:
                last_node = path.pop()

                while path:
                    previous_node = path.pop()

                    edge_name = tuple([previous_node, last_node])
                    if edge_name in edge_betweenness:
                        edge_betweenness[edge_name] += 1

                        if edge_betweenness[edge_name] > highest_betweenness[1]:
                            highest_betweenness = [edge_name, edge_betweenness[edge_name]]
                    else:
                        edge_betweenness[edge_name] = 1

                    last_node = previous_node

        #print("Temp edges betweenness:", edge_betweenness)

    #print("Edges betweenness:", edge_betweenness)

    """
    Bon dans le fonctionnement actuel du programme il faudrait que je trouve un moyen de récupérer le poids de la
    liaison pour pouvoir la trouver dans adjacency et la supprimer. De fait le poids ne devrait pas être compris dans
    l'ID d'un edge du coup je laisse comme ça le temps que Tanguy modifie la structure du graph et du pathfinder
    """
    DIJKSTRA.graph.__adjacency.remove((edge_name[0], edge_name[1], 42))
