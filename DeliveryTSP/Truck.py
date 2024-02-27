import datetime

from Graph import Vertex, Graph
from Package import Package
from operator import attrgetter


class Truck:
    def __init__(self, current_vertex):
        self.packages = []
        self.miles = 0.0
        self.start_time = None
        self.speed = 18.0
        self.current_vertex = current_vertex

    # Assign package to this truck
    def load(self, package: Package):
        self.packages.append(package)

    # Start the delivery process
    def start_route(self, start_time, graph: Graph):
        self.start_time = start_time

        # Set the start time for all the packages to the trucks start time
        # O(n)
        for package in self.packages:
            package.start_time = start_time

        # Until all packages are off the truck find the closest next delivery by sorting the packages in order of
        # distance then go to that one (greedy algorithm)
        # O(n^2log(n))
        while len(self.packages) > 0:
            self.packages.sort(key=lambda p: graph.distance[self.current_vertex, p.destination_vertex])
            next_package = self.packages[0]
            self.deliver(next_package, graph)

    # Adds mileage to trucks for every delivery, changes the truck's location,
    # sets the delivery time of the package, and removes the package from the truck
    def deliver(self, package: Package, graph: Graph):
        self.miles = self.miles + graph.distance[self.current_vertex, package.destination_vertex]
        self.current_vertex = package.destination_vertex
        package.set_delivery_time(self.start_time + datetime.timedelta(hours=(self.miles / self.speed)))
        self.packages.pop(0)

    # Moves the truck from its current vertex to a new one without executing a delivery
    def return_to_hub(self, new_vertex: Vertex, graph: Graph):
        self.miles = self.miles + graph.distance[self.current_vertex, new_vertex]
        self.current_vertex = new_vertex
