from typing import Tuple
from math import sqrt
from pathfinding import *
from src.clustering import clustering

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
    # Import data
    stops = import_stops("../data/stops.txt")
    edges = import_edges("../data/stop_times.txt")
    print("Data imported")

    # Construct graph
    GRAPH = Graph(stops.values(), compute_weight=lambda u, v: sqrt(
        (v.position[0] - u.position[0]) ** 2 + (v.position[1] - u.position[1]) ** 2))
    for edge in edges:
        GRAPH.add_edge(edge[0], edge[1])
    print("Graph built")

    # Construct pathfinders
    #BFS = Pathfinder(GRAPH, bfs)
    DIJKSTRA = Pathfinder(GRAPH, dijkstra)


    # 4 : Detect clustering
    #print(edges)
    clustering(DIJKSTRA, stops.keys(), 5)
