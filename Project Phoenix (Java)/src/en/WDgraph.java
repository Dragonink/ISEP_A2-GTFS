package en;

import java.util.ArrayList;

/*
To create fully functional graph
classes:
- Graph
- Dgraph
- WDgraph
- DirectedEdge
 */


public class WDgraph {
    /*
    A weighted directed graph
     */

    final ArrayList<Edge>[] adjacencylist;  // array of adjacency lists, one per vertex
    int vertices;  // number of vertices


    WDgraph(int vertices) {
        // create a graph with a specified number of vertices
        this.vertices = vertices;

        // create a new array of ArrayLists with size equal to the number of vertices
        adjacencylist = new ArrayList[vertices];

        // initialize adjacency lists for all the vertices with empty ArrayLists
        for (int i = 0; i < vertices; i++) {
            adjacencylist[i] = new ArrayList<>();
        }
    }


    // add a directed edge
    public void addEdge(int source, int destination, double weight) {

        // add the source -> destination edge to the appropriate adjacencylist
        adjacencylist[source].add(new Edge(source, destination, weight));
    }


    // Get the nodes near
    public ArrayList<Edge> getNeighbours(int node) {

        // return a copy of adjacencyList to preserve the former
        return new ArrayList<>(this.adjacencylist[node]);
    }

    public void addEdge(int end, int end1) {
        System.out.println("Error");
    }


    // Name in the instructions: Digraph
    public static class Dgraph extends WDgraph {
        /*
        A unweighted graph
         */

        Dgraph(int vertices) {
            super(vertices);
        }

        // method to add an unweighted edge
        public void addEdge(int source, int destination) {
            addEdge(source, destination, 1);
        }
    }

    public static class Wgraph extends WDgraph {
        /*
        A weighted undirected graph
         */

        Wgraph(int vertices) {
            super(vertices);
        }

        // method to add an undirected edge
        public void addEdge(int source, int destination, double weight) {

            super.addEdge(source, destination, weight);
            super.addEdge(destination, source, weight);
        }
    }


    public static class Graph extends WDgraph {
        /*
        A weighted directed graph
         */

        Graph(int vertices) {
            super(vertices);
        }

        // method to add a directed weighted edge
        public void addEdge(int source, int destination, double weight) {

            super.addEdge(source, destination, 1);
            super.addEdge(destination, source, 1);
        }
    }


    // Name in the instructions: public class DirectedEdge
    public static class Edge {
    /*
    represents a directed weighted edge between two vertices in a graph
     */


        private final int v;
        private final int w;
        private final double weight;

        public Edge(int v, int w, double weight) {
            this.v = v;
            this.w = w;
            this.weight = weight;
        }

        public int from() {
            return v;
        }

        public int to() {
            return w;
        }

        public double weight() {
            return weight;
        }
    }
}
