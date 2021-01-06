package en;

import java.util.*;

public class search {

    // Name in the instructions: List<V> dfs(Graph G)
    public static List<Integer> dfs(WDgraph G, int startingNode) {
        /*
        performs the deep first search (DFS) algorithm in the G G starting from startingNode
         */


        boolean[] visited = new boolean[G.vertices];  // set to true if the node has been visited (false otherwise)
        visited[startingNode] = true;  // Set the starting node as visited
        List<Integer> explored = new ArrayList<>();  // List of the nodes in the order of exploration
        // Stack of nodes to explore
        ArrayDeque<Integer> queue = new ArrayDeque<>(Collections.singletonList(startingNode));

        while (!queue.isEmpty()) {  // Until there is no node to explore left...
            int node = queue.pop();  // Retreives the last node of the stack (on the top)
            explored.add(node);  // Add the node to the explored list

            TreeSet<Integer> neighbours = new TreeSet<>();  // Initialize an ordered set

            // Fill it with the undiscovered neighboring nodes
            for (WDgraph.Edge neighbour : G.getNeighbours(node)) {
                if (!visited[neighbour.to()]) {
                    neighbours.add(neighbour.to());
                }
            }

            while (!neighbours.isEmpty()) {  // Until there is no neighbours left...

                int new_node = neighbours.pollLast();  // find and remove the node with with the biggest identifier
                visited[new_node] = true;  // Mark the node as discovered
                queue.push(new_node);  // Insert it to the queue of nodes to explore
            }
        }
        return explored;  // Return the list of explored nodes
    }

    // Name in the instructions: bfs(Graph G)
    public static List<Integer> bfs(WDgraph G, int startingNode) {
        boolean[] visited = new boolean[G.vertices];  // set to true if the node has been visited (false otherwise)
        visited[startingNode] = true;  // Set the starting node as visited
        List<Integer> explored = new ArrayList<>();  // List of the nodes in the order of exploration
        // Queue of nodes to explore
        ArrayDeque<Integer> queue = new ArrayDeque<>(Collections.singletonList(startingNode));

        while (!queue.isEmpty()) {  // Until there is no node to explore left...
            int node = queue.poll();  // Retreives the first node of the queue (on the bottom)
            explored.add(node);  // Add the node to the explored list

            TreeSet<Integer> neighbours = new TreeSet<>();  // Initialize an ordered set

            // Fill it with the undiscovered neighboring nodes
            for (WDgraph.Edge neighbour : G.getNeighbours(node)) {
                if (!visited[neighbour.to()]) {
                    neighbours.add(neighbour.to());
                }
            }

            while (!neighbours.isEmpty()) {  // Until there is no neighbours left...

                int new_node = neighbours.pollFirst();  // find and remove the node with with the smallest identifier
                visited[new_node] = true;  // Mark the node as discovered
                queue.add(new_node);  // Add it to the queue of nodes to explore
            }
        }
        return explored;  // Return the list of explored nodes
    }

    // Name in the instructions: int cc(WDgraph G)
    static int cc(WDgraph G, int startingNode) {
        return dfs(G, startingNode).size();
    }

    // Name in the instructions: isConnected()
    static boolean isConnected(WDgraph G, int startingNode) {
        // Indicate if all nodes are connected

        return cc(G, startingNode) == G.vertices;
    }
}
