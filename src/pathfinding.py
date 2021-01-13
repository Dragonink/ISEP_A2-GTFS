from typing import Callable, Dict, Generic, List, Set, Tuple, TypeVar
from math import inf
from heapq import heapify, heappop, heappush
from graph import Graph

T = TypeVar("T")
class Pathfinder(Generic[T]):
	"""Wrapping class to allow pathfinding in graphs

	# Generic
	- `T` - Type of the graph nodes

	# Properties
	- `graph` - Graph used to compute pathfinding
	- `previous` - Dictionnary `from => to => previous` where `previous` is a list of the previous nodes of `to` when searching from `from`
	- `distance` - Dictionnary `from => to => distance`
	- `method` - Function to compute shortest paths from a node
	"""
	def __init__(self, graph: Graph[T], method: Callable[['Pathfinder[T]', int], None]):
		self.graph = graph
		self._previous: Dict[int, Dict[int, Set[int]]] = dict()
		self._distance: Dict[int, Dict[int, float]] = dict()
		self.__method = method
	def reset(self):
		"""Reset the pathfinding results"""
		Pathfinder.__init__(self, self.graph, self.__method)
	def compute(self, start: int):
		"""Execute the pathfinding method from a certain node

		Save the newly computed data to the save file

		# Arguments
		- `start` - Key of the starting node
		"""
		if start not in self._previous:
			self.__method(self, start)
	def has_path(self, start: int, end: int) -> bool:
		"""Check if a path exist between two nodes

		# Arguments
		- `start` - Key of the starting node
		- `end` - Key of the ending node

		# Errors thrown
		- `ValueError` if both keys are equal

		# Return value
		`True` if a path exists; `False` otherwise
		"""
		if start == end:
			raise ValueError("start={0} and end={0} are equal".format(start, end))
		else:
			if start not in self._previous:
				self.compute(start)
			return end in self._previous[start]
	def get_paths(self, start: int, end: int) -> List[List[int]]:
		"""Get the shortest path between two nodes

		# Arguments
		- `start` - Key of the starting node
		- `end` - Key of the ending node

		# Errors thrown
		- `ValueError` if both keys are equal

		# Return value
		List of paths, with a path being a list of node indexes
		"""
		if start == end:
			raise ValueError("start={0} and end={0} are equal".format(start, end))
		else:
			if start not in self._previous:
				self.compute(start)
			paths: List[List[int]] = []
			def __recurse(path: List[int], pos: int):
				if path[pos] == start:
					paths.append(path[:pos + 1][::-1])
				else:
					for previous in self._previous[start][path[pos]]:
						if len(path) < pos + 2:
							path.append(previous)
						else:
							path[pos + 1] = previous
						__recurse(path, pos + 1)
			if self.has_path(start, end):
				__recurse([end], 0)
			return paths
	def get_distance(self, start: int, end: int) -> float:
		"""Get the distance between two nodes

		# Arguments
		- `start` - Key of the starting node
		- `end` - Key of the ending node

		# Return value
		Distance from `start` to `end`, in edges
		"""
		if start not in self._previous:
			self.compute(start)
		return self._distance[start][end] if end in self._distance[start] else inf

def bfs(self: Pathfinder[T], start: int):
	"""Breadth-First Search method for `Pathfinder`"""
	if start not in self._previous:
		self._previous[start] = dict()
		self._distance[start] = dict()
		self._distance[start][start] = 0
		queue = [start]
		heapify(queue)
		while len(queue) > 0:
			current = heappop(queue)
			for u in self.graph[current].neighbors_out:
				if u not in self._distance[start]:
					self._previous[start][u] = set()
					self._distance[start][u] = self._distance[start][current] + 1
					heappush(queue, u)
				if self._distance[start][u] == self._distance[start][current] + 1:
					self._previous[start][u].add(current)
def dijkstra(self: Pathfinder[T], start: int):
	"""Dijkstra method for `Pathfinder`"""
	if start not in self._previous:
		self._previous[start] = dict()
		self._distance[start] = dict()
		self._distance[start][start] = 0
		marked: Set[int] = set()
		queue: List[Tuple[float, int]] = [(0, start)]
		heapify(queue)
		while len(queue) > 0:
			_, current = heappop(queue)
			marked.add(current)
			for (u, weight) in self.graph[current].neighbors_out.items():
				tentative_distance = self._distance[start][current] + weight
				if u not in self._distance[start] or tentative_distance < self._distance[start][u]:
					self._previous[start][u] = set()
					self._distance[start][u] = tentative_distance
				if self._distance[start][u] == tentative_distance:
					self._previous[start][u].add(current)
				if u not in marked:
					heappush(queue, (self._distance[start][u], u))
