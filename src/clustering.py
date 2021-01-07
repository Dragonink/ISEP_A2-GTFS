from pathfinding import Pathfinder


def clustering(DIJKSTRA: Pathfinder, nodes, n):
	"""
	Clustering method (first try)
	"""

	print("\nCreating", n, "clusters...")

	clusters = []
	n_nodes = len(nodes)

	while len(clusters) < n:  # As long as the right number of clusters has not been constituted

		edge_betweenness = {}  # Betweenness of each edge
		nodes_found = set()  # List of discovered nodes
		new_cluster = False  # Reset the number of clusters
		highest_betweenness = ["", 0]  # Edge with the biggest betweeness
		nodes_to_explore = nodes.copy()  # List of nodes to explore
		progress = 0
		clusters = []

		while nodes_to_explore:  # As long as there is still unexplored nodes

			new_progress = round(100 * (1 - len(nodes_to_explore) / n_nodes), 1)
			if new_progress > progress:
				progress = new_progress
				print(progress, "%", sep='')

			starting_node = nodes_to_explore.pop()  # Take a node to explore

			# If the node not been discovered report the discovery of a new cluster
			if starting_node not in nodes_found:
				new_cluster = True  # Optimistic
				clusters.append({starting_node})

			nodes_found.add(starting_node)  # Add the node to the discovered nodes list

			for target_node in nodes_to_explore:  # Search every other node

				path = DIJKSTRA.get_path(starting_node, target_node)  # Search a path between the two nodes

				if path is not None:  # If there is a path...

					if target_node in nodes_found:
						for i in range(len(clusters) - 1):
							if target_node in clusters[i]:
								clusters[i].update(clusters[len(clusters) - 1])
								del clusters[len(clusters) - 1]
								new_cluster = False
					else:
						# Set the second node as discovered at add it to the same cluster as the first one
						nodes_found.add(target_node)
						clusters[len(clusters) - 1].add(target_node)

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

			if new_cluster:
				n_clusters = len(clusters) + 1
				size_cluster = len(clusters[n_clusters-2])

				print("Cluster n°", n_clusters, " found: entry: ", starting_node, ", current size: ", size_cluster,
					  " (", round(100 * size_cluster / n_nodes), "%)", sep='')
				size_cluster = 0

				new_cluster = False

		# print("Temp edges betweenness:", edge_betweenness)

		# print("Edges betweenness:", edge_betweenness)
		print(len(clusters), "clusters found")
		for i in range(len(clusters)):
			print("Cluster n°", i, " found: size (not final): ", len(clusters[i]),
				  " (", round(100 * len(clusters[i]) / n_nodes), "%)", sep='')
		print("Highest betweenness:", highest_betweenness[1],
			  "(between", highest_betweenness[0][0], "and", highest_betweenness[0][1], ")")

		# Deleting the edge by deleting its name from the neighbors_out list of the start node
		DIJKSTRA.graph[highest_betweenness[0][0]].neighbors_out.remove(highest_betweenness[0][1])
		"""
		Doing so should delete de facto the edge from the graph.
		A ghost edge will still be listed in neighbors_in but it shouldn't be used by the program
		"""

	print(n, "clusters obtained")
