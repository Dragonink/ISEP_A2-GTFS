from typing import Callable, Dict, List, Set
from math import inf
from graph import Graph


class Pathfinder:
	"""Wrapping class to allow pathfinding in graphs

	# Properties
	- `graph` - Graph used to compute pathfinding
	- `previous` - Dictionnary `from => to => previous` where `previous` is the previous node of `to` when searching
					from `from`
	- `distance` - Dictionnary `from => to => distance`
	- `method` - Function to compute shortest paths from a node
	"""

	def __init__(self, graph: Graph, method: Callable[['Pathfinder', int], None]):
		self.graph = graph
		self._previous: Dict[int, Dict[int, int]] = dict()
		self._distance: Dict[int, Dict[int, float]] = dict()
		self.__method = method

	def has_path(self, u: int, v: int) -> bool:
		"""Check if a path exist between two nodes

		# Arguments
		- `start` - Key of the starting node
		- `end` - Key of the ending node

		# Return value
		`True` if a path exists; `False` otherwise
		"""
		return u in self._previous and v in self._previous[u]

	def get_path(self, u: int, v: int):
		"""Get the shortest path between two nodes

		# Arguments
		- `u` - Key of the starting node
		- `v` - Key of the ending node

		# Return value
		Ordered list of node keys; or `None` if a path does not exist
		"""
		if not self.has_path(u, v):
			return None
		else:
			path: List[str] = [v]
			current = v
			while current != u:
				next = self._previous[u][current]
				path.append(next)
				current = next
			path.reverse()
			return path

	def get_distance(self, u: int, v: int) -> float:
		"""Get the distance between two nodes

		# Arguments
		- `start` - Key of the starting node
		- `end` - Key of the ending node

		# Return value
		Distance from `u` to `v`, in edges
		"""
		if u not in self._previous:
			self.__method(self, u)
		return self._distance[u][v] if v in self._distance[u] else inf


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

def dijkstra(self: Pathfinder, v: int):
	"""Dijkstra method for `Pathfinder`"""

	if v not in self._previous:
		self._previous[v] = dict()
		self._distance[v] = dict()
		self._distance[v][v] = 0
		marked: Set[int] = set()
		queue = [v]
		while len(queue) > 0:
			current = queue.pop(0)
			marked.add(current)
			for (u, weight) in self.graph[current].neighbors_out:
				tentative_distance = self._distance[v][current] + weight
				if u not in self._distance[v] or tentative_distance < self._distance[v][u]:
					self._previous[v][u] = current
					self._distance[v][u] = tentative_distance
				if u not in marked:
					queue.append(u)
