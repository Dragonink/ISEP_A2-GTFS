from typing import Dict, Generic, Iterable, Iterator, List, Set, Tuple, TypeVar

T = TypeVar("T")
Adjacency = Tuple[str, str]
class Graph(Generic[T]):
	"""Graph (unweighted directed) representation

	# Generic
	- `T` - Type of the nodes

	# Fields
	- `nodes` - Set of nodes
	- `adjacency` - Adjacency list: set of tuples `(u,v)` which represent `u->v`
	"""
	def __init__(self, nodes: Iterable[T]):
		self.__nodes: Dict[str, T] = dict()
		for node in nodes:
			self.add_node(node)
		self.__adjacency: Set[Adjacency] = set()
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

	def has_node(self, v: str) -> bool:
		"""Check if a node key exists

		# Arguments
		- `v` - Key of the node

		# Return value
		`True` if the node exists; `False` otherwise
		"""
		return v in self.__nodes
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
		"""Add an edge `u->v` to the graph

		# Arguments
		- `u` - Key of the first node
		- `v` - Key of the second node

		# Errors thrown
		- `ValueError` if both keys are equal, or if one key does not exist
		"""
		if u == v:
			raise ValueError("u={0} and v={0} are equal".format(u, v))
		elif not self.has_node(u):
			raise ValueError("u={0} does not refer to a node".format(u))
		elif not self.has_node(v):
			raise ValueError("v={0} does not refer to a node".format(v))
		else:
			self.__adjacency.add((u,v))
	def neighbors_out(self, v: str) -> List[str]:
		"""Get the outward neighbors of a node

		# Arguments
		- `v` - Key of the node

		# Return value
		List of the keys of nodes that can be accessed from `v`
		"""
		neighbors: List[str] = []
		for (u, w) in self.__adjacency:
			if u == v and u != w and w not in neighbors:
				neighbors.append(w)
		return neighbors
	def neighbors_in(self, v: int) -> List[str]:
		"""Get the inward neighbors of a node

		# Arguments
		- `v` - Key of the node

		# Return value
		List of the keys of nodes that can access `v`
		"""
		neighbors: List[str] = []
		for (u, w) in self.__adjacency:
			if w == v and u != w and u not in neighbors:
				neighbors.append(u)
		return neighbors
