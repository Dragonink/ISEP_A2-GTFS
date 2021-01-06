from pathfinding import Pathfinder


def clustering(DIJKSTRA: Pathfinder, keys, n):
    """
    Clustering method (first try)

    Putain c'est trop long cette merde il y a des sérieux pbs d'optimisation quelque part
    """

    keys = set(keys)

    edge_betweenness = {}

    while keys:
        print(len(keys), "nodes to explore left")
        first_node = keys.pop()

        for second_node in keys:

            if DIJKSTRA.has_path(first_node, second_node):

                nodes = DIJKSTRA.get_path(first_node, second_node)

                last_node = nodes.pop()

                while nodes:
                    previous_node = nodes.pop()

                    edge_name = [previous_node, last_node]
                    edge_name.sort()
                    edge_name = tuple(edge_name)
                    if edge_name in edge_betweenness:
                        edge_betweenness[edge_name] += 1
                    else:
                        edge_betweenness[edge_name] = 1

                    last_node = previous_node

    print("Edges betweenness:", edge_betweenness)
