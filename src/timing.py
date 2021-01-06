from typing import Callable, Tuple, TypeVar
from time import perf_counter

R = TypeVar("R")
def timing(f: Callable[..., R]) -> Callable[..., Tuple[R, float]]:
	"""Create a timed function

	# Arguments
	- `f` - Function to time

	# Return value
	Function which takes the same arguments as `f`, but returns a tuple `(result, time)`
	"""
	def timed_f(*args) -> Tuple[R, float]:
		start = perf_counter()
		result = f(*args)
		return (result, perf_counter() - start)
	return timed_f
