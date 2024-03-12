def ReadFile(filename):
    with open(filename, 'r') as f:
        vertices = set()
        edges = []

        for line in f:
            if line.startswith('p'):
                _,_,numVertices,numEdges = line.split()
            if line.startswith('e'):
                _,v1,v2 = line.split()
                vertices.add(v1)
                vertices.add(v2)
                edges.append((v1,v2))

    return vertices,edges,int(numVertices),int(numEdges)