import numpy as np
import random

class Ant:
    # create new ant
    # alpha: the relative importance of pheromone (si_ij)
    # beta: the relative importance of heuristic value (n_ij)
    def __init__(self, vertices, colors, phero_matrix,adj_matrix, numVertices, antID,alpha=1, beta=3):
        self.colors = colors
        self.vertices = vertices
        self.phero_matrix = phero_matrix
        self.adj_matrix = adj_matrix
        self.numVertices = numVertices
        self.ID = antID
        self.distance = 0
        self.colors_assigned = {}
        self.alpha = alpha
        self.beta = beta

        self.initialize()

    # reset everything for a new solution
    # start: starting node in g (random by default)
    # return: Ant
    def initialize(self, start=None):
        self.colors_available = sorted(self.colors.copy())
        # init assigned colors with None
        keys = [n for n in self.vertices]
        self.colors_assigned = {key: None for key in keys}
        
        # start node
        if start is None:
            self.start = random.choice(self.vertices)
        else:
            self.start = start
        
        self.visited = []
        self.unvisited = self.vertices.copy()
        
        # assign min. color number to the start node
        if (len(self.visited)==0):
            self.assign_color(self.start, self.colors_available[0])

    # assign color to node and update the node lists
    def assign_color(self, node, color):
        self.colors_assigned[node] = color
        self.visited.append(node)
        self.unvisited.remove(node)
    
    # assign a color to each node in the graph
    def colorize(self,initailize=False):
        len_unvisited = len(self.unvisited)
        tabu_colors = []
        # assign color to each unvisited node
        for i in range(len_unvisited):
            next = self.next_candidate()
            tabu_colors = []
            # add colors of neighbours to tabu list
            for j in range(self.numVertices):
                if (self.adj_matrix[next-1,j-1]==1):
                    tabu_colors.append(self.colors_assigned[j+1])
            # assign color with the smallest number that is not tabu
            for k in self.colors_available:
                if (k not in tabu_colors):
                    self.assign_color(next,k)
                    break
        # save distance of the current solution
        self.distance = len(set(self.colors_assigned.values()))
        print("for ant#",self.ID+1,"distance is:",self.distance)
        return self

        
    # return the number of different colors among the neighbours of node
    def diversity(self, node=None):
        # print("inside dsat",adj_matrix)
        if node is None:
            node = self.start
        col_neighbors = []
        for j in range(self.numVertices):
            if (self.adj_matrix[node-1, j-1]==1):
                col_neighbors.append(self.colors_assigned[j+1])
        return len(set(col_neighbors))

    # return the pheromone trail of the pair (node,adj_node)
    def pheromone(self, node, adj_node):
        return self.phero_matrix[node-1, adj_node-1]

    # select next candidate node according to the transition rule
    def next_candidate(self):
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
                heuristic_values.append((self.pheromone(self.start, j)**self.alpha)*(self.diversity(j)**self.beta))
                candidates.append(j)
            max_value = max(heuristic_values)
            for i in range(len(candidates)):
                if (heuristic_values[i] >= max_value):
                   candidates_available.append(candidates[i])
            candidate = random.choice(candidates_available)
        self.start = candidate
        return candidate
    
    # return your own pheromone trail
    def pheromone_trail(self):
        phero_trail = np.zeros((self.numVertices, self.numVertices), float)
        for i in self.vertices:
            for j in self.vertices:
                if (self.colors_assigned[i]==self.colors_assigned[j]):
                    phero_trail[i-1,j-1] = 1
        return phero_trail