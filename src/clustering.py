from pathfinding import Pathfinder


def clustering(DIJKSTRA: Pathfinder, nodes, n):
	"""
	Clustering method (first try)
	"""

	print("\nCreating", n, "clusters...")

	n_clusters = 0  # Number of clusters

	while n_clusters < n:  # As long as the right number of clusters has not been constituted

		edge_betweenness = {}  # Betweenness of each edge
		nodes_found = set()  # List of discovered nodes
		n_clusters = 0  # Reset the number of clusters
		highest_betweenness = ["", 0]  # Edge with the biggest betweeness
		nodes_to_explore = nodes  # List of nodes to explore

        while nodes_to_explore:  # As long as there is still unexplored nodes
            #print(len(nodes_to_explore), "nodes to explore left")
            starting_node = nodes_to_explore.pop()  # Take a node to explore

            # If the node not been discovered report the discovery of a new cluster
            if starting_node not in nodes_found:
                n_clusters += 1
                #print("Cluster n°", n_clusters, " found!", sep='')
            nodes_found.add(starting_node)  # Add the node to the discovered nodes list

			for target_node in nodes_to_explore:  # Search every other node

                path = DIJKSTRA.get_path(starting_node, target_node)  # Search a path between the two nodes
                print("hello", path)

				if path is not None:  # Iff there is a path...

					# Set the second node as discovered (it is is the same cluster than the first one)
					if target_node not in nodes_found:
						nodes_found.add(target_node)

					last_node = path.pop()  # Get the last node of the path between the two nodes

					while path:  # For each edge of the path...

						previous_node = path.pop()  # Get the previous node
						edge_name = (previous_node, last_node)  # Compute the name of the edge between them


						# Compute the new edge betweenness
						if edge_name in edge_betweenness:
							edge_betweenness[edge_name] += 1
						else:
							edge_betweenness[edge_name] = 1

						# Check if the new betweenness is the higher
						if edge_betweenness[edge_name] > highest_betweenness[1]:
							highest_betweenness = [edge_name, edge_betweenness[edge_name]]

						last_node = previous_node

			#print("Temp edges betweenness:", edge_betweenness)

		#print("Edges betweenness:", edge_betweenness)
		print(n_clusters, "clusters found")
		print("Highest betweenness:", highest_betweenness[1],
			  "(between", highest_betweenness[0][0], "and", highest_betweenness[0][1], ")")

		# Deleting the edge by deleting its name from the neighbors_out list of the start node
		DIJKSTRA.graph[highest_betweenness[0][0]].neighbors_out.remove(highest_betweenness[0][1])
		"""
		Doing so should delete de facto the edge from the graph.
		A ghost edge will still be listed in neighbors_in but it shouldn't be used by the program
		"""

	print(n, "clusters obtained")
