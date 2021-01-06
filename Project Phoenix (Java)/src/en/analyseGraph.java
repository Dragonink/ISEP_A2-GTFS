package en;

import java.text.DecimalFormat;


public class analyseGraph {
    // implement an algorithm for detecting shortest paths in weighted-digraphs

    int source;
    int vertices;
    int[] previous;  // indicates the node preceding v on the shortest path
    double[] distance;  // represents the distance from the source node s to node v

    // Name in the instructions: boolean[] marked
    boolean[] visited;  // set to true if v has been visited (false otherwise)

    // Name in the instructions: int[] distance
    int[] edgeDistance;  // represents the distance (in number of edges) from the source node s to node v

    public void printDistances() {
        DecimalFormat df = new DecimalFormat("#.##"); // Round the distance to a two decimal points number
        System.out.println("Distances from the node " + source + ":");
        for (int i = 0; i < vertices; i++) {
            System.out.println("Node " + i + ": " + df.format(distance[i]));
        }
    }

    int distTo(int v) {
        // returns the length of the shortest path from s to v

        int length = 0;
        boolean[] explored = new boolean[vertices];
        while(!explored[v] && v != source) {
            length++;
            explored[v]= true;
            v = previous[v];
        }
        if (v == source) {
            return length;
        } else {
            return -1;
        }
    }


    boolean hasPathTo(int v) {
        // returns true if there is a path from s to v

        return edgeDistance[v] != -1;
    }


    void printSP(int v) {
        // prints the shortest path from s to v

        StringBuilder path = new StringBuilder();
        boolean[] explored = new boolean[vertices];
        while(!explored[v] && v != source) {
            path.insert(0, " -> " + v);
            explored[v]= true;
            v = previous[v];
        }
        if (v == source) {
            System.out.println("Path: " + source + path);
        } else {
            System.out.println("No path found");
        }
    }


    // Name in the instructions: verifyNonNegative(WDGraph G)
    boolean verifyNonNegative() {
        // takes as input a weidhted-directed graph and verifies than all weights in the graph are non negative

        for (double aDistance : distance) {  // For each distance...
            if (aDistance < 0) {  // If it is negative returns false
                return false;
            }
        }

        return true;  // If no negative distance has been found returns true
    }

    void displayResults() {
        printDistances();  // print Shortest Path Tree
        // Check for negative values
        System.out.println("There are only positive edge distances in the graph: " + verifyNonNegative());
    }

    double eccentricity() {
        double max_distance = distance[0];
        for (int i = 1; i < vertices; i++) {
            if (distance[i] > max_distance) {
                max_distance = distance[i];
            }
        }
        return max_distance;
    }
}
