# Graph class modified from the WGU course material to fit this project

class Vertex:
    def __init__(self, label):
        self.label = label


class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.distance = {}

    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []

    # Since directed edges aren't relevant to this project all edges can be added as undirected
    def add_edge(self, vertex_a, vertex_b, weight):
        self.distance[(vertex_a, vertex_b)] = weight
        self.distance[(vertex_b, vertex_a)] = weight
        self.adjacency_list[vertex_a].append(vertex_b)
        self.adjacency_list[vertex_b].append(vertex_a)
