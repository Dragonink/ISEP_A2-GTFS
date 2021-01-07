from typing import Callable, Dict, List, Set
from math import inf
from graph import Graph


class Pathfinder:
	"""Wrapping class to allow pathfinding in graphs

	# Properties
	- `graph` - Graph used to compute pathfinding
	- `previous` - Dictionnary `from => to => previous` where `previous` is the previous node of `to` when searching from `from`
	- `distance` - Dictionnary `from => to => distance`
	- `method` - Function to compute shortest paths from a node
	"""

	def __init__(self, graph: Graph, method: Callable[['Pathfinder', int], None]):
		self.graph = graph
		self._previous: Dict[int, Dict[int, int]] = dict()
		self._distance: Dict[int, Dict[int, float]] = dict()
		self.__method = method

	def has_path(self, start: int, end: int) -> bool:
		"""Check if a path exist between two nodes

		# Arguments
		- `start` - Key of the starting node
		- `end` - Key of the ending node

		# Return value
		`True` if a path exists; `False` otherwise
		"""
		if start not in self._previous:
			self.__method(self, start)
		return end in self._previous[start]

	def get_path(self, start: int, end: int) -> List[int]:
		"""Get the shortest path between two nodes

		# Arguments
		- `start` - Key of the starting node
		- `end` - Key of the ending node

		# Return value
		Ordered list of node keys; or `None` if a path does not exist
		"""
		if not self.has_path(start, end):
			return None
		else:
			path: List[str] = [end]
			current = end
			while current != start:
				next = self._previous[start][current]
				path.append(next)
				current = next
			path.reverse()
			return path

	def get_distance(self, start: int, end: int) -> float:
		"""Get the distance between two nodes

		# Arguments
		- `start` - Key of the starting node
		- `end` - Key of the ending node

		# Return value
		Distance from `u` to `v`, in edges
		"""

		if start not in self._previous:  # # If the connections between source and the other nodes have not been referenced
			self.__method(self, start)  # ...do it using the search algorithm chosen

		return self._distance[start][end] if v in self._distance[start] else inf


def bfs(self: Pathfinder, v: int):
	"""Breadth-First Search method for `Pathfinder`"""
	if v not in self._previous:
		self._previous[v] = dict()
		self._distance[v] = dict()
		self._distance[v][v] = 0
		queue = [v]
		while len(queue) > 0:
			current = queue.pop(0)
			for (u, _) in self.graph[current].neighbors_out:
				if u not in self._previous[v]:
					self._previous[v][u] = current
					self._distance[v][u] = self._distance[v][current] + 1
					queue.append(u)


def dijkstra(self: Pathfinder, source: int):
	"""Dijkstra method for `Pathfinder`"""

	print("true that")

	self._previous[source] = dict()
	self._distance[source] = {source: 0}
	marked: Set[int] = set()
	#queue = [source]
	queue = {0: source}

	while len(queue) > 0:
		#current = queue.pop(0)
		current = queue.pop(min(queue))

		#if current in marked:
		if True:
			marked.add(current)
			for (destination, weight) in self.graph[current].neighbors_out:
				#if destination in marked:
				if True:
					new_distance = self._distance[source][current] + weight

					if destination not in self._distance[source] or \
						new_distance < self._distance[source][destination]:
						self._previous[source][destination] = current
						self._distance[source][destination] = new_distance

						queue[new_distance] = destination
						if destination in marked:
							print("fuck")

					#if destination not in marked:
					#	queue.append(destination)
	print("end")
