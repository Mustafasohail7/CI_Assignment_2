from ReadFile import ReadFile

class Ant:
    def __init__(self,routes,distance) -> None:
        self.routes = routes
        self.distance = distance

class ACO:
    def __init__(self,alpha,beta,iterations,num,rho,path) -> None:
        self.alpha = alpha
        self.beta = beta
        self.iterations = iterations
        self.num = num
        self.evaporation_rate = 1-rho
        self.path = path
        # self.ants = [Ant()]

        try:
            self.vertices,self.edges,self.numVertices,self.numEdges = ReadFile(self.path)
        except FileNotFoundError:
            print("File not found")
            exit(1)

        self.pheromones = self.initialize_pheromones()
        self.heurestics = self.initialize_heurestics()

    def initialize_pheromones(self):
        return [[1 for _ in range(self.numVertices)] for _ in range(self.numVertices)]
    
    def initialize_heurestics(self):
        return [[1 for _ in range(self.numVertices)] for _ in range(self.numVertices)]
    
    def run(self):
        for _ in range(self.iterations):
            for ant in range(self.num):
                pass
        
