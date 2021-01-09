from typing import Callable, Dict, Generic, List, Set, Tuple, TypeVar
from os.path import isfile
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
	- `save` - Location of the save file
	"""

	def __init__(self, graph: Graph[T], method: Callable[['Pathfinder[T]', int], None], save: str):
		self.graph = graph
		self._previous: Dict[int, Dict[int, Set[int]]] = dict()
		self._distance: Dict[int, Dict[int, float]] = dict()
		self.__method = method
		self.__save = save
		if isfile(self.__save):
			self.__import()
		else:
			# Create save file
			with open(self.__save, "xt"):
				pass

	def __import(self):
		"""Import data from save file"""
		with open(self.__save, "rt") as file:
			for i, line in enumerate(file):
				for node, previous in enumerate(line.strip().split(";")):
					if len(previous) > 0:
						if i not in self._previous:
							self._previous[i] = dict()
						self._previous[i][node] = set([int(p) for p in previous.split(",")])

	def compute(self, start: int):
		"""Execute the pathfinding method from a certain node

		Save the newly computed data to the save file

		# Arguments
		- `start` - Key of the starting node
		"""
		if start not in self._previous:
			self.__method(self, start)
			# Save newly computed data to save file
			with open(self.__save, "r+t") as file:
				lines = file.readlines()
				while start > len(lines):
					lines.append("\n")
				line = ""
				for node in range(self.graph.order):
					if node in self._previous[start]:
						line += ",".join([str(p) for p in self._previous[start][node]])
					if node < self.graph.order - 1:
						line += ";"
				line += "\n"
				lines.append(line)
				file.seek(0)
				file.truncate()
				file.writelines(lines)

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
		if start not in self._distance:
			# Data has been imported, we need to compute distances
			self._distance[start] = dict()
			def __recurse(_acc: float, node: int) -> float:
				if node in self._distance[start]:
					return _acc + self._distance[start][node]
				elif node in self._previous[start]:
					previous = list(self._previous[start][node])[0]
					if self.__method == bfs:
						return __recurse(_acc + 1, previous)
					elif self.__method == dijkstra:
						return __recurse(_acc + self.graph[node].neighbors_in[previous], previous)
				else:
					return inf
			for node in self._previous[start]:
				distance = __recurse(node)
				if distance < inf:
					self._distance[start][node] = distance
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


"""
def dijkstra(self: Pathfinder, source: int):
	#Dijkstra method for `Pathfinder`

	self._previous[source] = dict()
	self._distance[source] = {source: 0}
	marked: Set[int] = set()
	queue = {0: source}

	while len(queue) > 0:
		current = queue.pop(min(queue))

		if current not in marked:
			marked.add(current)
			for (destination, weight) in self.graph[current].neighbors_out:
				if destination not in marked:
					self._distance[source]
					old = self._distance[source][current]
					new_distance = old + weight

					if destination not in self._distance[source] or \
						new_distance < self._distance[source][destination]:
						self._previous[source][destination] = current
						self._distance[source][destination] = new_distance

						queue[new_distance] = destination
"""
