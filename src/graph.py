from typing import Callable, Generic, Iterable, Iterator, List, Set, Tuple, TypeVar

T = TypeVar("T")
Adjacency = Tuple[int, float]


class Node(Generic[T]):
	"""Graph node representation

	# Generic
	- `T` - Type of the node value

	# Properties
	- `value` - Value of the node
	- `neighbors_out` - Outward neighbors of the node
	- `neighbors_in` - Inward neighbors of the node
	"""


	def __init__(self, value: T):
		self.__value = value
		self.__neighbors_out: Set[Adjacency] = set()
		self.__neighbors_in: Set[Adjacency] = set()


	def __repr__(self) -> str:
		return repr(self.__value)


	def __eq__(self, other: 'Node') -> bool:
		return self.value == other.value \
			and self.neighbors_out == other.neighbors_out \
			and self.neighbors_in == other.neighbors_in

	def __hash__(self) -> int:
		return hash((self.__value, frozenset(self.__neighbors_out), frozenset(self.__neighbors_in)))


	@property
	def value(self) -> T:
		return self.__value

	@property
	def neighbors_out(self) -> Set[Adjacency]:
		return self.__neighbors_out

	"""
	Ne devrait pas être utilisée, j'update neighbors_out pour détruire des edges mais pas neighbors_in,
	l'utiliser peut donc générer des erreurs
	"""
	@property
	def neighbors_in(self) -> Set[Adjacency]:
		return self.__neighbors_in


class Graph(Generic[T]):
	"""Graph (weighted directed) representation

	# Generic
	- `T` - Type of the nodes

	# Properties
	- `nodes` - List of nodes
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

	def add_node(self, node: T) -> int:
		"""Add a node to the graph

		# Arguments
		- `node` - Node value to add

		# Return value
		Key of the newly-added node
		"""
		self.__nodes.append(Node(node))
		return len(self.__nodes) - 1


	def get_node(self, node: int) -> Node:
		return self.__nodes[node]


	def add_edge(self, u: int, v: int):
		"""Add an edge `u-(weight)->v` to the graph

		Will compute the weight using the `compute_weight` property.
		If `compute_weight` is `None`, the weight will be 0.

		# Arguments
		- `start` - Key of the first node
		- `end` - Key of the second node

		# Errors thrown
		- `ValueError` if both keys are equal
		"""
		if u == v:
			raise ValueError("u={0} and v={0} are equal".format(u, v))
		else:
			weight = float(0) if self.__compute_weight is None \
				else self.__compute_weight(self.__nodes[u].value, self.__nodes[v].value)
			self.__nodes[u].neighbors_out.add((v, weight))
			self.__nodes[v].neighbors_in.add((u, weight))
			self.__size += 1
