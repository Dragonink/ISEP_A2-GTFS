package en;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;


public class projectPhoenix {

    static boolean allowLoops = false;

    public static void main(String[] args) throws Exception {

        System.out.println("\nDFS on a simple graph built using data given in graph-BFS-SP.txt:");
        WDgraph G = graphFromFile("simple", "graph-BFS-SP.txt");
        int s = 5;
        System.out.println("Content of the graph: " + search.dfs(G, s));
        System.out.println("Number of connected nodes: " + search.cc(G, s));
        System.out.println("Is this graph connected ? " + search.isConnected(G, s));
        // The first encounter of the nodes is the node 4 and its order is 4
        // The graph have 8 nodes and 9 edges
        // The graph is connected

        System.out.println("\nBFS on a simple graph built using data given in graph-BFS-SP.txt:");
        G = graphFromFile("simple", "graph-BFS-SP.txt");
        System.out.println("Content of the graph: " + search.bfs(G, s));
        // The first encounter of the nodes is the node 4 and its order is 4
        // The graph have 8 nodes and 9 edges
        // The graph is connected

        System.out.println("\nBFS on a directed graph built using data given in graph-BFS-SP.txt:");
        G = graphFromFile("directed","graph-BFS-SP.txt");
        BFSShortestPaths analysedGraph;

        double[] distances = new double[G.vertices];
        double diameter = 0;
        double radius = Double.MAX_VALUE;
        System.out.println("Nodes eccentricity:");
        for (s = 0; s < G.vertices; s++) {
            analysedGraph = new BFSShortestPaths(G, s);
            distances[s] = analysedGraph.eccentricity();

            if (distances[s] > diameter) {
                diameter = distances[s];
            } else if (distances[s] < radius) {
                radius = distances[s];
            }
            System.out.println("Node " + s + ": " + distances[s]);
        }
        System.out.println("Graph diameter: " + diameter + "\nGraph radius: " + radius);


        s = 0;
        int v = 3;
        System.out.println("\nBFS on a weighted directed graph built using data given in graph-WDG.txt:");
        G = graphFromFile("WD", "graph-WDG.txt");
        analysedGraph = new BFSShortestPaths(G, s);
        System.out.println("There is a connection from " + s + " to " + v + ": " + analysedGraph.hasPathTo(v));
        analysedGraph.printSP(v);
        analysedGraph.displayResults();


        System.out.println("\nDijkstra algorithm on a weighted directed graph built using data given in the source code:");
        int vertices = 6;
        G = new WDgraph(vertices);
        G.addEdge(0, 1, 4);
        G.addEdge(0, 2, 3);
        G.addEdge(1, 2, 1);
        G.addEdge(1, 3, 2);
        G.addEdge(2, 3, 4);
        G.addEdge(3, 4, 2);
        G.addEdge(4, 5, 6);
        DijkstraSP analysedGraph2 = new DijkstraSP(G, s);
        analysedGraph2.displayResults();

        System.out.println("\nDijkstra algorithm on a weighted directed graph built using data given in graph-WDG.txt:");
        G = graphFromFile("WD", "graph-WDG.txt");
        analysedGraph2 = new DijkstraSP(G, s);
        System.out.println("There is a connection from " + s + " to " + v + ": " + analysedGraph2.hasPathTo(v));
        analysedGraph2.printSP(v);
        analysedGraph2.displayResults();
    }


    static WDgraph graphFromFile(String type, String name) throws Exception {
        // Creates a graph from the content of a file


        ArrayDeque<double[]> adj = new ArrayDeque<>();  // On initialise la liste de connexions
        int size = 0;

        HashMap<String,Integer> ids = new HashMap<>();//Creating HashMap
        HashMap<Integer,List<Integer>> itineraries = new HashMap<>();//Creating HashMap

        List<Integer>  = new ArrayList<>();  // List of the nodes in the order of exploration

        File file = new File("data/stop_times.txt");
        BufferedReader br = new BufferedReader(new FileReader(file));
        String line;

        br.readLine();  // Pass column names

        int new_id = 0;
        int edge_name;


        while ((line = br.readLine()) != null) {

            String[] edgeData = line.split(",");  // On fait une liste des informations du lien

            if (ids.containsKey(edgeData[3])) {
                edge_name = ids.get(edgeData[3]);
            } else {
                ids.put(edgeData[3], new_id);
                new_id++;
            }

            double[] edge = new double[]{Integer.parseInt(edgeData[0]), Integer.parseInt(edgeData[1]), 1};

            if (edgeData.length == 3) {  // If the weight of the edge is specified in the file use it
                edge[2] = Double.parseDouble(edgeData[2]);
            }

            if (allowLoops || edge[0] != edge[1]) {  // On vérifie que ce n'est pas une boucle

                int newestNode = Math.max((int)edge[0], (int)edge[1]);

                if (newestNode > size) {
                    size = newestNode;
                }

                adj.add(edge);
            }
        }
        WDgraph G;
        if (type.equals("simple")) {
            G = new WDgraph.Graph(size + 1);
        } else if (type.equals("directed")) {
            G = new WDgraph.Dgraph(size + 1);
        } else {
            G = new WDgraph(size + 1);
        }

        while (!adj.isEmpty()) {
            double[] ends = adj.pop();
            if (type.equals("WD")) {
                G.addEdge((int)ends[0], (int)ends[1], ends[2]);
            } else {
                G.addEdge((int)ends[0], (int)ends[1]);
            }
        }
        return G;
    }
}
