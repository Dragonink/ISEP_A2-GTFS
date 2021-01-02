from typing import Dict, List, Tuple
from numpy import pi

Position = Tuple[float, float]

EARTH_CIRCUMFERENCE: float = 2 * pi * 6.371e3
# Phoenix is located at 33.448377° N, 112.074037° W
PHOENIX_POS: Position = (33.448377, -112.074037)

class Stop:
	"""Stop representation

	# Fields
	- `id` - Unique identifier
	- `position` - Cartesian position of the stop, with `PHOENIX_POS` as origin
	"""
	def __init__(self, id: str, lat: float, lon: float):
		self.__id: str = id
		# Convert (lat,lon) to (x,y) with PHOENIX_POS as origin
		rlat, rlon = (lat - PHOENIX_POS[0]) / 360, (lon - PHOENIX_POS[1]) / 360
		self.__position: Position = (rlon * EARTH_CIRCUMFERENCE, rlat * EARTH_CIRCUMFERENCE)
	def from_csv(line: str) -> 'Stop':
		data = line.split(",")
		return Stop(data[0], float(data[4]), float(data[5]))
	def __repr__(self) -> str:
		return "{0}: {1}".format(self.__id, self.__position)

	@property
	def id(self) -> str:
		return self.__id
	@property
	def position(self) -> Position:
		return self.__position

def import_stops(file: str) -> Dict[str, Stop]:
	stops: Dict[str, Stop] = dict()
	with open(file, "rt") as data:
		lines = data.readlines()[1:]
		for line in lines:
			stop = Stop.from_csv(line)
			stops[stop.id] = stop
	return stops

def import_edges(file: str) -> Dict[str, List[str]]:
	edges: Dict[str, Dict[int, str]] = dict()
	# Import raw data
	with open(file, "rt") as data:
		lines = data.readlines()[1:]
		for line in lines:
			cols = line.split(",")
			if cols[0] not in edges:
				edges[cols[0]] = dict()
			edges[cols[0]][int(cols[4])] = cols[3]
	# Transform data into a sequence of stop IDs
	for (trip, stops) in edges.items():
		edges[trip] = [stops[seq] for seq in sorted(stops)]
	return edges
