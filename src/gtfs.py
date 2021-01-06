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
		return "{0}: {1}".format(self.__id, self.__position)

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


def import_stops(file: str) -> Dict[str, Stop]:
	"""Import stops from GTFS `stops.txt`

	# Arguments
	- `file` - Path to the file

	# Return value
	Dictionnary `stop.id => stop`
	"""
	stops: Dict[str, Stop] = dict()
	with open(file, "rt") as data:
		for line in data.readlines()[1:]:
			stop = Stop.from_csv(line)
			stops[stop.id] = stop
	return stops

def import_edges(file: str) -> Set[Tuple[str, str]]:
	"""Import edges from GTFS `stop_times.txt`

	# Arguments
	- `file` - Path to the file

	# Return value
	Set of ordered tuples of stop IDs
	"""
	trips: Dict[str, Dict[int, str]] = dict()
	# Import raw data
	with open(file, "rt") as data:
		for line in data.readlines()[1:]:
			cols = line.split(",")
			if cols[0] not in trips:
				trips[cols[0]] = dict()
			trips[cols[0]][int(cols[4])] = cols[3]
	# Transform data
	edges: Set[Tuple[str, str]] = set()
	for trip in trips.values():
		stop_seq = sorted(trip)
		for (i, stop) in enumerate(stop_seq[:-1]):
			edges.add((trip[stop], trip[stop_seq[i + 1]]))
	return edges


if __name__ == "__main__":
	DATAPATH = argv[1] if len(argv) > 1 else getcwd()
	# Import data
	(stops, exetime) = timing(import_stops)(join(DATAPATH, "stops.txt"))
	print("Imported {0} stops in {1}ms".format(len(stops), exetime * 1e3))
	(edges, exetime) = timing(import_edges)(join(DATAPATH, "stop_times.txt"))
	print("Imported {0} edges in {1}ms".format(len(edges), exetime * 1e3))

	# Construct graph
	exetime = perf_counter()
	GRAPH = Graph(stops.values(), compute_weight=lambda u, v: sqrt(
		(v.position[0] - u.position[0]) ** 2 + (v.position[1] - u.position[1]) ** 2))
	for edge in edges:
		GRAPH.add_edge(edge[0], edge[1])
	print("Constructed graph in {0}ms".format((perf_counter() - exetime) * 1e3))

	# Construct pathfinders
	BFS = Pathfinder(GRAPH, bfs)
	DIJKSTRA = Pathfinder(GRAPH, dijkstra)

	# Detect clustering
	# clustering(DIJKSTRA, stops.keys(), 5)
