package en;

import java.util.*;
import java.util.AbstractMap.SimpleEntry;


public class DijkstraSP extends analyseGraph {
    // implement the Dijkstra algorithm for detecting shortest paths in weighted-digraphs


    DijkstraSP(WDgraph G, int s) {
        // implements the Dijkstra algorithm for shortest paths from a root node s

        source = s;
        vertices = G.vertices;
        previous = new int[vertices];
        visited = new boolean[vertices];
        edgeDistance = new int[vertices];

        distance = new double[vertices];
        for (int i = 0; i < vertices; i++) {
            if (i != s) {
                distance[i] = Double.MAX_VALUE;  // Initialize all distances to "infinity" except for sourceNode
            }
        }

        // Initialize an ordered set (override the comparator to do the sorting based keys)
        TreeSet<SimpleEntry<Double, Integer>> treeSet = new TreeSet<>(new PairComparator());

        // add the pair (distance, node) of the sourceNode to the set
        treeSet.add(new SimpleEntry<>(0.0, s));

        // while tree set is not empty
        while (!treeSet.isEmpty()) {

            // find and remove the (distance, node) pair with the minimum distance and get the node number
            int extractedNode = treeSet.pollFirst().getValue();

            if (!visited[extractedNode]) {  // If the extracted node has not been visited...

                visited[extractedNode] = true;  // mark the node as visited

                // take all the adjacent nodes
                List<WDgraph.Edge> neighbours = G.adjacencylist[extractedNode];

                neighbours.removeIf(edge -> visited[edge.to()]);  // remove already visited nodes

                // iterate over every neighbor/adjacent node
                for (WDgraph.Edge edge : neighbours) {

                    int destination = edge.to();  // get the Edge destination node

                    if (!visited[destination]) {  // If the destination node has not been visited...

                        // calculate the new distance via extractedNode and the edge.weight
                        double newDistance = edge.weight() + distance[extractedNode];
                        //System.out.println(edge.to() + " : " + edge.weight() + "+" + distance.get(extractedNode) + "=" + newDistance);

                        // if the current distance of the destination node is bigger than newDistance update it
                        if (newDistance < distance[destination]) {

                            previous[destination] = extractedNode;

                            // create a (newDistance, destination) pair and add it to the treeSet
                            treeSet.add(new SimpleEntry<>(newDistance, destination));

                            // update the distance for the destination node to the newDistance
                            distance[destination] = newDistance;
                        }
                    }
                }
            }
        }

        // Compute the distances of the nodes
        for (int i = 0; i < vertices; i++) {
            edgeDistance[i] = distTo(i);
        }
    }

    static class PairComparator implements Comparator<Object> {

        @Override
        public int compare(Object o1, Object o2) {
            /*
            Implement a method to compare instances (o1 and o2) of java.util.AbstractMap.SimpleEntry
            where the key is a double (to implement an ascending value ordering)
             */

            // Using Math.signum makes sure that a value |x| < 0.5 keeps it sign and is not changed to 0
            return (int) Math.signum((double) ((SimpleEntry) o1).getKey() - (double) ((SimpleEntry) o2).getKey());
        }
    }
}
