from typing import Dict, Tuple
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

# https://stackoverflow.com/questions/13407468/how-can-i-list-all-the-stops-associated-with-a-route-using-gtfs
#TODO use stop_times.txt
