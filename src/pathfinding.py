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
	def __init__(self, graph: Graph, method: Callable[['Pathfinder', str], None]):
		self.graph = graph
		self._previous: Dict[str, Dict[str, str]] = dict()
		self._distance: Dict[str, Dict[str, float]] = dict()
		self.__method = method

	def has_path(self, u: str, v: str) -> bool:
		"""Check if a path exist between two nodes

		# Arguments
		- `u` - Key of the starting node
		- `v` - Key of the ending node

		# Return value
		`True` if a path exists; `False` otherwise
		"""
		if u not in self._previous:
			self.__method(self, u)
		return v in self._previous[u]
	def get_path(self, u: str, v: str) -> List[str]:
		"""Get the shortest path between two nodes

		# Arguments
		- `u` - Key of the starting node
		- `v` - Key of the ending node

		# Return value
		Ordered list of node keys; or `None` if a path does not exist
		"""
		if u not in self._previous:
			self.__method(self, u)
		if not self.has_path(u, v):
			return None
		path: List[str] = [v]
		current = v
		while current != u:
			next = self._previous[u][current]
			path.append(next)
			current = next
		path.reverse()
		return path
	def get_distance(self, u: str, v: str) -> int:
		"""Get the distance between two nodes

		# Arguments
		- `u` - Key of the starting node
		- `v` - Key of the ending node

		# Return value
		Distance from `u` to `v`, in edges
		"""
		if u not in self._previous:
			self.__method(self, u)
		return self._distance[u][v] if v in self._distance[u] else inf

def bfs(self: Pathfinder, v: str):
	"""Breadth-First Search method for `Pathfinder`"""
	if v not in self._previous:
		self._previous[v] = dict()
		self._distance[v] = dict()
		self._distance[v][v] = 0
		queue = [v]
		while len(queue) > 0:
			current = queue.pop(0)
			for (u,_) in self.graph.neighbors_out(current):
				if u not in self._previous[v]:
					self._previous[v][u] = current
					self._distance[v][u] = self._distance[v][current] + 1
					queue.append(u)
def dijkstra(self: Pathfinder, v: str):
	"""Dijkstra method for `Pathfinder`"""
	if v not in self._previous:
		self._previous[v] = dict()
		self._distance[v] = dict()
		self._distance[v][v] = 0
		marked: Set[str] = set()
		queue = [v]
		while len(queue) > 0:
			current = queue.pop(0)
			marked.add(current)
			for (u,weight) in self.graph.neighbors_out(current):
				tentative_distance = self._distance[v][current] + weight
				if u not in self._distance[v] or tentative_distance < self._distance[v][u]:
					self._previous[v][u] = current
					self._distance[v][u] = tentative_distance
				if not u in marked:
					queue.append(u)
