from typing import Callable, Dict, Generic, Iterable, Iterator, Set, Tuple, TypeVar

T = TypeVar("T")
Adjacency = Tuple[str, str, float]

class Graph(Generic[T]):
	"""Graph (weighted directed) representation

	# Generic
	- `T` - Type of the nodes

	# Properties
	- `nodes` - Dictionnary `id => node`
	- `adjacency` - Adjacency list: set of tuples `(u,v,weight)` which represent `u-(weight)->v`
	- `compute_weight` - Function to compute edge weight from two nodes
	"""

	def __init__(self, nodes: Iterable[T], compute_weight: Callable[[T, T], float] = None):
		self.__nodes: Dict[str, T] = dict()
		for node in nodes:
			self.add_node(node)
		self.__adjacency: Set[Adjacency] = set()
		self.__compute_weight = compute_weight

	def __repr__(self) -> str:
		return repr(self.__adjacency)

	def __iter__(self) -> Iterator[Tuple[str, T]]:
		return iter(self.__nodes.items())

	def __getitem__(self, key: str) -> T:
		return self.__nodes[key]

	@property
	def order(self) -> int:
		return len(self.__nodes)

	@property
	def size(self) -> int:
		return len(self.__adjacency)


	def add_node(self, node: T) -> str:
		"""Add a node to the graph

		# Arguments
		- `node` - Node to add

		# Errors thrown
		- `RuntimeError` if the computed key already exists

		# Return value
		Key of the newly-added node
		"""
		key = str(node.id if hasattr(node, "id") else self.order)
		if key not in self.__nodes:
			self.__nodes[key] = node
			return key
		else:
			raise RuntimeError("{0} already exists as a node key".format(key))


	def add_edge(self, u: str, v: str):
		"""Add an edge `u-(weight)->v` to the graph

		Will compute the weight using the `compute_weight` property.
		If `compute_weight` is `None`, the weight will be 0.

		# Arguments
		- `u` - Key of the first node
		- `v` - Key of the second node

		# Errors thrown
		- `ValueError` if both keys are equal, or if one key does not exist
		"""
		if u == v:
			raise ValueError("u={0} and v={0} are equal".format(u, v))
		elif u not in self.__nodes:
			raise ValueError("u={0} does not refer to a node".format(u))
		elif v not in self.__nodes:
			raise ValueError("v={0} does not refer to a node".format(v))
		else:
			weight = float(0) if self.__compute_weight is None else self.__compute_weight(self.__nodes[u], self.__nodes[v])
			self.__adjacency.add((u,v,weight))


	def neighbors_out(self, v: str) -> Set[Tuple[str, float]]:
		"""Get the outward neighbors of a node

		# Arguments
		- `v` - Key of the node

		# Return value
		Set of the keys of nodes that can be accessed from `v`, and the weights of the edges
		"""
		neighbors: Set[Tuple[str, float]] = set()
		for (u, w, weight) in self.__adjacency:
			if u == v and u != w and w not in neighbors:
				neighbors.add((w, weight))
		return neighbors


	def neighbors_in(self, v: int) -> Set[Tuple[str, float]]:
		"""Get the inward neighbors of a node

		# Arguments
		- `v` - Key of the node

		# Return value
		Set of the keys of nodes that can access `v`, and the weights of the edges
		"""
		neighbors: Set[Tuple[str, float]] = set()
		for (u, w, weight) in self.__adjacency:
			if w == v and u != w and u not in neighbors:
				neighbors.add((u, weight))
		return neighbors


	def neighbors(self, v: int) -> Set[Tuple[str, float]]:
		"""Get all neighbors of a node

		# Arguments
		- `v` - Key of the node

		# Return value
		Set of the keys of neighbors of `v`, and the weights of the edges
		"""
		return self.neighbors_in(v).union(self.neighbors_out(v))
