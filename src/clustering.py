from src.pathfinding import Pathfinder


def clustering(DIJKSTRA: Pathfinder, nodes, n):
    """
    Clustering method (first try)
    """
    n_clusters = 0

    while n_clusters < n:
        edge_betweenness = {}

        nodes_found = set()
        n_clusters = 0

        highest_betweenness = ["",0]

        nodes_to_explore = nodes

        while nodes_to_explore:
            print(len(nodes_to_explore), "nodes to explore left")
            starting_node = nodes_to_explore.pop()

            if starting_node not in nodes_found:
                n_clusters += 1
            nodes_found.add(starting_node)

            for target_node in nodes_to_explore:

                path = DIJKSTRA.get_path(starting_node, target_node)

                if path is not None:

                    if target_node not in nodes_found:
                        nodes_found.add(target_node)  # This node is in the same cluster, add it to the found set

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
        print(n_clusters, "clusters found")

        """
        Bon dans le fonctionnement actuel du programme il faudrait que je trouve un moyen de récupérer le poids de la
        liaison pour pouvoir la trouver dans adjacency et la supprimer. De fait le poids ne devrait pas être compris dans
        l'ID d'un edge du coup je laisse comme ça le temps que Tanguy modifie la structure du graph et du pathfinder
        """

        DIJKSTRA.graph.__adjacency.remove((edge_name[0], edge_name[1], 42))

    print(n, "clusters obtained")
