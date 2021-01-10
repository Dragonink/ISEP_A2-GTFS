from typing import Tuple
from sys import argv
from os import getcwd
from os.path import join
from time import perf_counter
from math import sqrt
from timing import timing
from pathfinding import *
from clustering import clustering


Position = Tuple[float, float]

class Stop:
	"""Stop representation

	# Properties
	- `id` - Unique identifier
	- `position` - Position of the stop
	"""

	def __init__(self, id: str, lat: float, lon: float):
		self.__id: str = id
		self.__position: Position = (lat, lon)

	def from_csv(line: str) -> 'Stop':
		"""Construct a Stop instance from CSV data

		# Arguments
		- `line` - CSV line containing data of the stop
		"""
		data = line.split(",")
		return Stop(data[0], float(data[4]), float(data[5]))

	def __repr__(self) -> str:
		return "{0} {1}".format(self.__id, self.__position)

	def __lt__(self, other: 'Stop') -> bool:
		return self.id < other.id

	def __eq__(self, other: 'Stop') -> bool:
		return self.id == other.id and self.position == other.position

	def __hash__(self) -> int:
		return hash((self.__id, self.__position))

	@property
	def id(self) -> str:
		return self.__id

	@property
	def position(self) -> Position:
		return self.__position


def import_stops(path: str) -> Tuple[List[Stop], Dict[str, int]]:
	"""Import stops from GTFS `stops.txt`

	# Arguments
	- `path` - Path to the file

	# Return value
	Tuple `(stops, id_map)` where `stops` is a list of `Stop` instances,
	and `id_map` is a dictionnary `stop.id => node_id` where `node_id` is the index of the node in `stops`
	"""
	stops: List[Stop] = []
	id_map: Dict[str, int] = dict()
	with open(path, "rt") as file:
		for i, line in enumerate(file):
			if i > 0:
				stop = Stop.from_csv(line)
				stops.append(stop)
				id_map[stop.id] = i - 1
	return stops, id_map

def import_edges(path: str) -> Set[Tuple[str, str]]:
	"""Import edges from GTFS `stop_times.txt`

	# Arguments
	- `path` - Path to the file

	# Return value
	Set of ordered tuples of stop IDs
	"""
	trips: Dict[str, List[Tuple[int, str]]] = dict()
	# Import raw data
	with open(path, "rt") as file:
		for i, line in enumerate(file):
			if i > 0:
				data = line.split(",")
				if data[0] not in trips:
					trips[data[0]] = []
				heappush(trips[data[0]], (int(data[4]), data[3]))
	# Transform data
	edges: Set[Tuple[str, str]] = set()
	for trip in trips.values():
		while len(trip) > 1:
			edges.add((heappop(trip)[1], trip[0][1]))
	return edges


if __name__ == "__main__":
	# Get data path
	"""The path to the data files can be set using a script argument.

	For example, if you execute Python from the workspace root, you can enter: `python src/gtfs.py ./data/`.
	Or, if you execute Python from the `src/` directory: `python gtfs.py ../data/`.
	"""
	DATAPATH = argv[1] if len(argv) > 1 else "../data/"

	# Import data
	(stops, id_map), exetime = timing(import_stops)(join(DATAPATH, "stops.txt"))
	print("Imported {0} stops in {1}ms".format(len(stops), round(exetime * 1e3)))
	edges, exetime = timing(import_edges)(join(DATAPATH, "stop_times.txt"))
	print("Imported {0} edges in {1}ms".format(len(edges), round(exetime * 1e3)))

	# Construct graph
	exetime = perf_counter()
	GRAPH = Graph(stops, compute_weight=lambda u, v: sqrt(
		(v.position[0] - u.position[0]) ** 2 + (v.position[1] - u.position[1]) ** 2))
	for edge in edges:
		GRAPH.add_edge(id_map[edge[0]], id_map[edge[1]])
	print("Constructed graph in {0}ms".format(round((perf_counter() - exetime) * 1e3)))

	# Construct pathfinders
	BFS = Pathfinder(GRAPH, bfs, join(DATAPATH, "generated_bfs.txt"))
	DIJKSTRA = Pathfinder(GRAPH, dijkstra, join(DATAPATH, "generated_dijkstra.txt"))

	# Create clustering
	clustering(DIJKSTRA, set(id_map.values()), 5)
