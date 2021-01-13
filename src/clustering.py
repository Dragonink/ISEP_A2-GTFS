from pathfinding import Pathfinder

def clustering(DIJKSTRA: Pathfinder, nodes, n=2, minimal_size=0, precise=True, chatty=False):
	"""
	Clustering algorithm

	# Arguments
	- `DIJKSTRA` - Graph and Pathfinder used
	- `nodes` - List of the nodes to explore
	- `n` - Number of clusters to create
	- `minimal_size` - Minimal size of the clusters displayed (float value between 0 and 100%)
	- `precise` - If deactivated the program will be much faster but can also generate a few more clusters than
				  requested (convenient for quickly creating numerous clusters)
	- `chatty` - Display or not the execution steps of the algorithm
	"""

	print("\nCreating", n, "clusters...")
	clusters = []  # Content of the clusters
	n_nodes = len(nodes)  # Number of nodes
	iteration = 0
	n_removals = 1

	while len(clusters) < n:  # As long as the right number of clusters has not been constituted
		if chatty:
			iteration += 1
			print("\nIteration", iteration)
		edge_betweenness = {}  # Betweenness of each edge
		DIJKSTRA.reset()  # Reset the Dijkstra algorithm
		nodes_found = set()  # List of discovered nodes
		nodes_to_explore = nodes.copy()  # List of nodes to explore
		progress = 0
		clusters = []  # List of clusters and their content
		current_cluster = -1  # Cluster being explored

		while nodes_to_explore:  # As long as there is still unexplored nodes

			# Displaying the progress
			if chatty:
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
						current_cluster = i

			else:  # If the node hasn't been discovered report the discovery of a new cluster

				clusters.append({starting_node})  # Create a new entry for the new cluster containing its first node
				current_cluster = len(clusters) - 1  # Set the new cluster as the current one

			nodes_found.add(starting_node)  # Add the node to the discovered nodes list

			for target_node in nodes_to_explore:  # Search every other node
				# (paths), exetime = timing(DIJKSTRA.get_paths)(starting_node, target_node)
				# print("Dijkstra of {0} in {1}ms".format(starting_node, exetime * 1e3))
				paths = DIJKSTRA.get_paths(starting_node, target_node)  # Search a path between the two nodes

				if len(paths) > 0:  # If there is a path...

					# Generating list of contents of each cluster
					if target_node in nodes_found:  # If the node has already been found

						# Search the node in the lists of the others clusters
						for other_cluster in range(len(clusters)):
							if current_cluster != other_cluster:
								if target_node in clusters[other_cluster]:

									# Add the content of the other cluster to the current cluster
									clusters[current_cluster].update(clusters[other_cluster])
									del clusters[other_cluster]  # Delete the other cluster

									# If the deleted cluster was older take into account the shift of keys in the list
									if other_cluster < current_cluster:
										current_cluster -= 1
									break

					else:  # If the node hasn't been found...

						# Set the second node as discovered at add it to the same cluster as the first one
						nodes_found.add(target_node)
						clusters[current_cluster].add(target_node)

					n_paths = len(paths)  # Number of paths of equal length found

					for path in paths:  # For each path...
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

		n_clusters = len(clusters)  # Count the number of clusters
		if chatty:
			print(n_clusters, "clusters found")

		if not precise:
			n_removals = n - n_clusters  # Delete as many edges as there are clusters to create

		for i in range(n_removals):

			# Get the edge with the highest betweenness
			highest_betweenness = max(edge_betweenness, key=edge_betweenness.get)

			if chatty:
				print("Deleting the edge between ", highest_betweenness[0], " and ", highest_betweenness[1],
					  " (Betweenness: ", edge_betweenness[highest_betweenness], ")", sep='')

			del edge_betweenness[highest_betweenness]  # Delete it from the list of edges betweenness

			# Deleting the edge by deleting its name from the neighbors_out list of the start node
			del DIJKSTRA.graph[highest_betweenness[0]].neighbors_out[highest_betweenness[1]]
			"""
			Doing so should delete de facto the edge from the graph.
			A ghost edge will still be listed in neighbors_in but it shouldn't be used by the program
			"""

	# Displaying the clusters created
	crumbs=0
	for i in range(len(clusters)):
		size = len(clusters[i])
		size_percentage = 100 * len(clusters[i]) / n_nodes
		if size_percentage > minimal_size:
			print("Cluster ", i + 1, ": size: ", size, " (", round(size_percentage), "%), content: ",
				  sorted(clusters[i]), sep='')
		else:
			crumbs += size
	if minimal_size > 0:
		print("Nodes isolated in small clusters: ", crumbs, " (", round(100 * crumbs / n_nodes), "%)", sep='')
