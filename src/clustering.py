from pathfinding import Pathfinder
from timing import timing


def clustering(DIJKSTRA: Pathfinder, nodes, n):
	"""
	Clustering method (first try)
	"""

	print("\nCreating", n, "clusters...")

	clusters = []  # Content of the clusters
	n_nodes = len(nodes)  # Number of nodes
	iteration = 0

	while len(clusters) < n:  # As long as the right number of clusters has not been constituted

		iteration += 1
		print("\nIteration", iteration)

		edge_betweenness = {}  # Betweenness of each edge
		DIJKSTRA.reset()
		nodes_found = set()  # List of discovered nodes
		nodes_to_explore = nodes.copy()  # List of nodes to explore
		progress = 0
		# clusters = []
		current_cluster = -1

		while nodes_to_explore:  # As long as there is still unexplored nodes

			# Displaying the progress
			new_progress = int(round(100 * (1 - len(nodes_to_explore) / n_nodes), -1))
			if new_progress > progress:
				progress = new_progress
				print(progress, "%", sep='')

			starting_node = nodes_to_explore.pop()  # Take a node to explore


			# Update the list of clusters
			if starting_node in nodes_found:  # If the node has already been discovered...

				# Search the node in every cluster list
				for i in range(len(clusters)):
					if starting_node in clusters[i]:
						clusters[i].add(starting_node)
						current_cluster = i


			else:  # If the node hasn't been discovered report the discovery of a new cluster

				clusters.append({starting_node})  # Create a new entry for the new cluster containing its first node
				current_cluster = len(clusters) - 1


			nodes_found.add(starting_node)  # Add the node to the discovered nodes list

			for target_node in nodes_to_explore:  # Search every other node

				# (paths), exetime = timing(DIJKSTRA.get_paths)(starting_node, target_node)
				# print("Dijkstra of {0} in {1}ms".format(starting_node, exetime * 1e3))
				paths = DIJKSTRA.get_paths(starting_node, target_node)  # Search a path between the two nodes

				if len(paths) > 0:  # If there is a path...

					# Generating list of contents of each cluster
					if target_node in nodes_found:  # If the node has already been found

						# Search the node in every cluster list
						for other_cluster in range(len(clusters)):
							if target_node in clusters[other_cluster]:

								if current_cluster == other_cluster:
									clusters[current_cluster].add(target_node)
								else:
									clusters[current_cluster].update(clusters[other_cluster])
									del clusters[other_cluster]

									# If the deleted cluster was older take into account the shift of values in the list
									if other_cluster < current_cluster:
										current_cluster -= 1

								break

					else:
						# Set the second node as discovered at add it to the same cluster as the first one
						nodes_found.add(target_node)
						clusters[current_cluster].add(target_node)


					n_paths = len(paths)  # Number of paths of equal length found

					for path in paths:  # For each path

						last_node = path.pop()  # Get the last node of the path between the two nodes

						while path:  # For each edge of the path...

							previous_node = path.pop()  # Get the previous node
							edge_name = (previous_node, last_node)  # Compute the name of the edge between them

							# Compute the new edge betweenness
							if edge_name in edge_betweenness:
								edge_betweenness[edge_name] += 1 / n_paths
							else:
								edge_betweenness[edge_name] = 1 / n_paths

							last_node = previous_node


		n_clusters = len(clusters)
		print(n_clusters, "clusters found")

		# Delete as many edges as there are clusters to create
		for i in range(n - n_clusters):

			highest_betweenness = max(edge_betweenness, key=edge_betweenness.get)  # Get the edge with the highest betweenness
			print("Deleting the edge between ", highest_betweenness[0], " and ", highest_betweenness[1],
				  " (Betweenness: ", edge_betweenness[highest_betweenness], ")", sep='')
			del edge_betweenness[highest_betweenness]  # Delete it from the list of edges betweenness

			# Deleting the edge by deleting its name from the neighbors_out list of the start node
			del DIJKSTRA.graph[highest_betweenness[0]].neighbors_out[highest_betweenness[1]]
			"""
			Doing so should delete de facto the edge from the graph.
			A ghost edge will still be listed in neighbors_in but it shouldn't be used by the program
			"""


	print("\n", n, "clusters obtained:")
	for i in range(len(clusters)):
		print("Cluster n°", i + 1, " found, size: ", len(clusters[i]), " (", round(100 * len(clusters[i]) / n_nodes),
			  "%) : ", sorted(clusters[i]), sep='')
