from ReadFile import ReadFile
import networkx as nx
import random
import numpy as np

class Ant:
    # create new ant
    # alpha: the relative importance of pheromone (si_ij)
    # beta: the relative importance of heuristic value (n_ij)
    def __init__(self, alpha=1, beta=3):
        self.graph = None
        self.colors = {}
        self.start = None
        self.visited = []
        self.unvisited = []
        self.alpha = alpha
        self.beta = beta
        self.distance = 0 # number of used colors on a valid solution
        self.number_colisions = 0 # only for consistency check, should be always 0
        self.colors_available = []
        self.colors_assigned = {}

    # reset everything for a new solution
    # start: starting node in g (random by default)
    # return: Ant
    def initialize(self, g_nodes_int, colors, start=None):
        self.colors_available = sorted(colors.copy())
        # init assigned colors with None
        keys = [n for n in g_nodes_int]
        self.colors_assigned = {key: None for key in keys}
        
        # start node
        if start is None:
            self.start = random.choice(g_nodes_int)
        else:
            self.start = start
        
        self.visited = []
        self.unvisited = g_nodes_int.copy()
        
        # assign min. color number to the start node
        if (len(self.visited)==0):
            self.assign_color(self.start, self.colors_available[0])
        return self

    # assign color to node and update the node lists
    def assign_color(self, node, color):
        self.colors_assigned[node] = color
        self.visited.append(node)
        self.unvisited.remove(node)
    
    # assign a color to each node in the graph
    def colorize(self,phero_matrix,N,adj_matrix):
        len_unvisited = len(self.unvisited)
        tabu_colors = []
        # assign color to each unvisited node
        for i in range(len_unvisited):
            next = self.next_candidate(phero_matrix,N,adj_matrix)
            tabu_colors = []
            # add colors of neighbours to tabu list
            for j in range(N):
                if (adj_matrix[next-1,j-1]==1):
                    tabu_colors.append(self.colors_assigned[j+1])
            # assign color with the smallest number that is not tabu
            for k in self.colors_available:
                if (k not in tabu_colors):
                    self.assign_color(next,k)
                    break
        # save distance of the current solution
        self.distance = len(set(self.colors_assigned.values()))
        # consitency check
        ##self.number_colisions = self.colisions()
        ##print('colisions: ' + str(self.number_colisions))
        
    # return the number of different colors among the neighbours of node
    def dsat(self, N, adj_matrix, node=None):
        # print("inside dsat",adj_matrix)
        if node is None:
            node = self.start
        col_neighbors = []
        for j in range(N):
            if (adj_matrix[node-1, j-1]==1):
                col_neighbors.append(self.colors_assigned[j+1])
        return len(set(col_neighbors))

    # return the pheromone trail of the pair (node,adj_node)
    def si(self, node, adj_node, phero_matrix):
        return phero_matrix[node-1, adj_node-1]

    # select next candidate node according to the transition rule
    def next_candidate(self, phero_matrix,N,adj_matrix):
        if (len(self.unvisited)==0):
           candidate = None
        elif (len(self.unvisited)==1):
            candidate = self.unvisited[0]
        else:
            max_value = 0
            heuristic_values = []
            candidates = []
            candidates_available = []
            for j in self.unvisited:
                heuristic_values.append((self.si(self.start, j, phero_matrix)**self.alpha)*(self.dsat(N,adj_matrix,j)**self.beta))
                candidates.append(j)
            max_value = max(heuristic_values)
            for i in range(len(candidates)):
                if (heuristic_values[i] >= max_value):
                   candidates_available.append(candidates[i])
            candidate = random.choice(candidates_available)
        self.start = candidate
        return candidate
    
    # return your own pheromone trail
    def pheromone_trail(self,g_nodes_int,N):
        phero_trail = np.zeros((N, N), float)
        for i in g_nodes_int:
            for j in g_nodes_int:
                if (self.colors_assigned[i]==self.colors_assigned[j]):
                    phero_trail[i-1,j-1] = 1
        return phero_trail

    # consistency check --> should always return 0
    def colisions(self):
        colisions = 0
        for key in self.colors_assigned:
            node = key
            col = self.colors_assigned[key]
            # check colors of neighbours
            for j in range(number_nodes):
                if (adj_matrix[node, j]==1 and self.colors_assigned[j]==col):
                    colisions = colisions+1
        return colisions


#draw the graph and display the weights on the edges
def draw_graph(g, col_val):
    pos = nx.spring_layout(g)
    values = [col_val.get(node, 'blue') for node in g.nodes()]
    nx.draw(g, pos, with_labels = True, node_color = values, edge_color = 'black' ,width = 1, alpha = 0.7)  #with_labels=true is to show the node number in the output graph

def nodes_number(g):
    for i in g:
        print(i)

# initiate a selection of colors for the coloring and compute the min. number of colors needed for a proper coloring
def init_colors(g):
    # grundy (max degree+1)
    colors = []
    grundy = len(nx.degree_histogram(g))
    for c in range(grundy):
       colors.append(c)
    return colors


# calculate the adjacency matrix of the graph    
def adjacency_matrix(g_nodes_int,g,N):
    adj_matrix = np.zeros((N, N), int)
    # print("adj_matrix",adj_matrix)
    for node in g_nodes_int:
        for adj_node in g.neighbors(node):
            adj_matrix[node-1, adj_node-1] = 1
    return adj_matrix

# apply decay rate to the phero_matrix
def apply_decay(g_nodes_int,p_matrix,phero_decay):
    for node in g_nodes_int:
        for adj_node in g_nodes_int:
            p_matrix[node-1, adj_node-1] = p_matrix[node-1, adj_node-1]*(1-phero_decay)

class ACO:
    def __init__(self, path, num_ants=10, iterations=10, alpha=1, beta=3, evaporation_rate=0.8):
        self.num_ants = num_ants
        self.iterations = iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate

        try:
            self.vertices,self.edges,self.numVertices,self.numEdges = ReadFile(path)
            print(len(self.edges))
            g = nx.Graph()
            for edge in self.edges:
                g.add_edge(int(edge[0]),int(edge[1]))
            self.graph = g
        except FileNotFoundError:
            print("File not found")
            exit(1)

    def solve(self):
        final_solution = {} # coloring of the graph
        final_costs = 0 # number of colors in the solution
        iterations_needed = 0
          
        self.number_nodes = nx.number_of_nodes(self.graph)
        self.g_nodes_int = []
        for node in self.graph:
            self.g_nodes_int.append(node)
        self.g_nodes_int = list(map(int, sorted(self.g_nodes_int)))
        self.adj_matrix = adjacency_matrix(self.g_nodes_int,self.graph,self.numVertices)
        self.colors = init_colors(self.graph)
        self.phero_matrix = self.init_pheromones()

        # ACO_GCP daemon
        for i in range(self.iterations):
            self.ants = self.create_colony()
            # let colony find solutions
            for ant in self.ants:
                ant.colorize(self.phero_matrix,self.number_nodes,self.adj_matrix)
            # apply decay rate
            apply_decay(self.g_nodes_int,self.phero_matrix,self.evaporation_rate)
            # select elite and update si_matrix
            elite_dist, elite_sol = self.update_elite()
            # estimate global solution so far
            if (final_costs==0):
                final_costs = elite_dist
                final_solution = elite_sol
                iterations_needed = i+1
            elif (elite_dist<final_costs):
                final_costs = elite_dist
                final_solution = elite_sol
                iterations_needed = i+1
        return final_costs, final_solution, iterations_needed
    
    def init_pheromones(self):
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

        elite_phero_matrix = elite_ant.pheromone_trail(self.g_nodes_int,self.number_nodes)
        self.phero_matrix = self.phero_matrix + elite_phero_matrix
        return elite_ant.distance, elite_ant.colors_assigned
    
    def create_colony(self):
        ants = []
        ants.extend([Ant().initialize(self.g_nodes_int, self.colors) for i in range(self.num_ants)])
        return ants
            

ant = ACO('queen11_11.col')
a,b,c = ant.solve()
print(a)
print(b)
print(c)

