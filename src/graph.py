from typing import Callable, Dict, Generic, Iterable, Iterator, List, TypeVar

T = TypeVar("T")
class Node(Generic[T]):
	"""Graph node representation

	# Generic
	- `T` - Type of the node value

	# Properties
	- `value` - Value of the node
	- `neighbors_out` - Dictionnary `node => weight` of outward neighbors
	- `neighbors_in` - Dictionnary `node => weight` of inward neighbors
	"""
	def __init__(self, value: T):
		self.__value = value
		self._neighbors_out: Dict[int, float] = dict()
		self._neighbors_in: Dict[int, float] = dict()
	def __repr__(self) -> str:
		return repr(self.__value)
	def __lt__(self, other: 'Node') -> bool:
		return self.value < other.value
	def __eq__(self, other: 'Node') -> bool:
		return self.value == other.value
	def __hash__(self) -> int:
		return hash(self.__value)
	@property
	def value(self) -> T:
		return self.__value
	@property
	def neighbors_out(self) -> Dict[int, float]:
		return self._neighbors_out
	@property
	def neighbors_in(self) -> Dict[int, float]:
		return self._neighbors_in
class Graph(Generic[T]):
	"""Graph (weighted directed) representation

	# Generic
	- `T` - Type of the nodes

	# Properties
	- `nodes` - List of nodes
	- `size` - Size of the graph
	- `compute_weight` - Function to compute edge weight from two nodes
	"""
	def __init__(self, nodes: Iterable[T], compute_weight: Callable[[T, T], float] = None):
		self.__nodes: List[Node[T]] = []
		for node in nodes:
			self.add_node(node)
		self.__size: int = 0
		self.__compute_weight = compute_weight
	def __iter__(self) -> Iterator[Node[T]]:
		return iter(self.__nodes)
	def __getitem__(self, key: int) -> Node[T]:
		return self.__nodes[key]
	@property
	def order(self) -> int:
		return len(self.__nodes)
	@property
	def size(self) -> int:
		return self.__size
	def add_node(self, node: T):
		"""Add a node to the graph

		# Arguments
		- `node` - Node value to add
		"""
		self.__nodes.append(Node(node))
	def add_edge(self, start: int, end: int):
		"""Add an edge `u-(weight)->v` to the graph

		Will compute the weight using the `compute_weight` property.
		If `compute_weight` is `None`, the weight will be 0.

		# Arguments
		- `start` - Key of the first node
		- `end` - Key of the second node

		# Errors thrown
		- `ValueError` if both keys are equal
		"""
		if start == end:
			raise ValueError("start={0} and end={0} are equal".format(start, end))
		else:
			weight = 0 if self.__compute_weight is None else self.__compute_weight(self.__nodes[start].value, self.__nodes[end].value)
			self.__nodes[start].neighbors_out[end] = weight
			self.__nodes[end].neighbors_in[start] = weight
			self.__size += 1
