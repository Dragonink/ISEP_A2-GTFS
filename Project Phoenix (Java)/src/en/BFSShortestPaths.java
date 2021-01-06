package en;

import java.util.*;


public class BFSShortestPaths extends analyseGraph {
    /*
    implement the BFS algorithm for shortest paths from a given vertex s
     */

    // Name in the instructions: bfs(Digraph G, int s)
    BFSShortestPaths(WDgraph G, int s) {
        /*
        executes the BFS algorithm to calculate all the shortest paths from the root vertex s.
        This function will update the visited, previous and distance arrays.
         */

        source = s;
        vertices = G.vertices;
        previous = new int[vertices];
        edgeDistance = new int[vertices];
        visited = new boolean[vertices];
        visited[s] = true;
        // Queue of nodes to explore
        ArrayDeque<Integer> queue = new ArrayDeque<>(Collections.singletonList(s));

        //System.out.println("Start processing using queue : ");

        while (!queue.isEmpty()) {  // Until there is no node to explore left...

            int node = queue.poll();  // Retreives the first node of the queue (the one put in first)
            //System.out.println("Studied " + node);

            TreeSet<Integer> neighbours = new TreeSet<>();  // Initialize an ordered set

            for (WDgraph.Edge neighbour : G.getNeighbours(node)) {
                if (!visited[neighbour.to()]) {
                    // add the pair (distance, node) of the sourceNode to the set
                    neighbours.add(neighbour.to());
                }
            }

            while (!neighbours.isEmpty()) { // Until there is no neighbours left...

                // find and remove the (distance, node) pair with the minimum distance and get the node number
                int new_node = neighbours.pollFirst();

                previous[new_node] = node;
                visited[new_node] = true;

                // Add it to the queue of nodes to explore
                queue.add(new_node);
            }
        }

        // Compute the distances of the nodes
        distance = new double[vertices];
        for (int i = 0; i < vertices; i++) {
            edgeDistance[i] = distTo(i);
            distance[i] = edgeDistance[i];
        }
    }
}
