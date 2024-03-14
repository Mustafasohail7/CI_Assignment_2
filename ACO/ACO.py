from ReadFile import ReadFile
from Ant import Ant
import networkx as nx
import numpy as np

class ACO:
    def __init__(self, path, num_ants=10, iterations=10, alpha=1, beta=3, evaporation_rate=0.8):
        self.num_ants = num_ants
        self.iterations = iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate

        try:
            self.vertices,self.edges,self.numVertices,self.numEdges = ReadFile(path)
            g = nx.Graph()
            for edge in self.edges:
                g.add_edge(int(edge[0]),int(edge[1]))
            self.graph = g
        except FileNotFoundError:
            print("File not found")
            exit(1)

    def solve(self):
        final_solution = {} 
        final_costs = 0 
        iterations_needed = 0

        self.adj_matrix = self.initialize_adj_matrix()
        self.colors = self.intialize_colors()
        self.phero_matrix = self.initialize_pheromone_matrix()

        self.ants = self.create_colony(initialize=True)

        for i in range(self.iterations):
            print("Iteration number:",i+1)
            
            self.ants = self.create_colony()
            # let colony find solutions

            self.apply_decay()

            elite_dist, elite_sol = self.update_elite()

            if (final_costs==0):
                final_costs = elite_dist
                final_solution = elite_sol
            elif (elite_dist<final_costs):
                final_costs = elite_dist
                final_solution = elite_sol

            iterations_needed +=1

            print("best solution so far",final_costs)
            print("-----------------------------------------")

        return (final_costs, final_solution, iterations_needed)
    
    def initialize_pheromone_matrix(self):
        phero_matrix = np.ones((self.numVertices, self.numVertices), float)
        for node in self.graph:
            for adj_node in self.graph.neighbors(node):
                phero_matrix[node-1, adj_node-1] = 0
        return phero_matrix
    
    def update_elite(self):
        best_dist = 0
        elite_ant = None
        for ant in self.ants:
            if (best_dist==0):
                best_dist = ant.distance
                elite_ant = ant
            elif (ant.distance < best_dist):
                best_dist = ant.distance
                elite_ant = ant

        elite_phero_matrix = elite_ant.pheromone_trail()
        self.phero_matrix = self.phero_matrix + elite_phero_matrix
        return elite_ant.distance, elite_ant.colors_assigned
    
    def create_colony(self,initialize=False):
        ants = []
        ants.extend([Ant(self.vertices,self.colors,self.phero_matrix,self.adj_matrix,self.numVertices).colorize(initialize) for i in range(self.num_ants)])
        return ants
    
    def initialize_adj_matrix(self):
        adj_matrix = np.zeros((self.numVertices, self.numVertices), int)

        for node in self.vertices:
            for adj_node in self.graph.neighbors(node):
                adj_matrix[node-1, adj_node-1] = 1
        return adj_matrix
    
    def intialize_colors(self):
        colors = []
        grundy = len(nx.degree_histogram(self.graph))
        for c in range(grundy):
            colors.append(c)
        return colors
            
    def apply_decay(self):
        for node in self.vertices:
            for adj_node in self.vertices:
                self.phero_matrix[node-1, adj_node-1] = self.phero_matrix[node-1, adj_node-1]*(1-self.evaporation_rate)




