from math import sqrt
from os.path import join
from sys import argv
from time import perf_counter

from clustering import clustering
from pathfinding import *
from timing import timing

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
				data = line.strip().split(",")
				if data[10] == "TE" and int(data[8]) < 2 and len(data[9]) == 0:  # Filter stops
					stop = Stop(data[0], float(data[4]), float(data[5]))
					stops.append(stop)
					id_map[stop.id] = len(stops) - 1
	return stops, id_map


def import_edges(path: str, id_map: Dict[str, int]) -> Set[Tuple[int, int]]:
	"""Import edges from GTFS `stop_times.txt`

	# Arguments
	- `path` - Path to the file
	- `id_map` - `id_map` returned from `import_stops`

	# Return value
	Set of ordered tuples of stop IDs
	"""
	trips: Dict[str, List[Tuple[int, int]]] = dict()
	# Import raw data
	with open(path, "rt") as file:
		for i, line in enumerate(file):
			if i > 0:
				data = line.strip().split(",")
				if data[3] in id_map:
					if data[0] not in trips:
						trips[data[0]] = []
					heappush(trips[data[0]], (int(data[4]), id_map[data[3]]))
	# Transform data
	edges: Set[Tuple[int, int]] = set()
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
	print("Imported {0} stops in {1}ms".format(len(stops), exetime * 1e3))
	edges, exetime = timing(import_edges)(join(DATAPATH, "stop_times.txt"), id_map)
	print("Imported {0} edges in {1}ms".format(len(edges), exetime * 1e3))

	# Construct graph
	exetime = perf_counter()
	GRAPH = Graph(stops, compute_weight=lambda u, v: sqrt(
		(v.position[0] - u.position[0]) ** 2 + (v.position[1] - u.position[1]) ** 2))
	for start, end in edges:
		GRAPH.add_edge(start, end)
	print("Constructed graph in {0}ms".format((perf_counter() - exetime) * 1e3))

	# Construct pathfinders
	BFS = Pathfinder(GRAPH, bfs)
	DIJKSTRA = Pathfinder(GRAPH, dijkstra)

	# Create clustering
	clustering(DIJKSTRA, set(id_map.values()), 147, chatty=True)
	clustering(DIJKSTRA, set(id_map.values()), 147, precise=False, minimal_size=0.5)
