from Graph import Vertex


class Package:
    def __init__(self, pid, address, deadline, city, state, zipcode, weight, status):
        self.destination_vertex = None
        self.pid = pid
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zipcode = zipcode
        self.weight = weight
        self.status = status
        self.state = state
        self.delivery_time = None
        self.entered_time = None
        self.start_time = None

    # print package information based on the time entered by the user
    def print_package(self):
        if self.entered_time < self.start_time:
            self.status = "At hub"
        elif self.delivery_time < self.entered_time:
            self.status = "Delivered at " + str(self.delivery_time)
        else:
            self.status = "En route"

        print(self.pid + ", "
              + self.address + ", "
              + self.city + ", "
              + self.state + ", "
              + self.zipcode + ", "
              + self.weight + ", "
              + self.deadline + ", "
              + self.status)

    def add_vertex(self, vertex: Vertex):
        self.destination_vertex = vertex

    def set_entered_time(self, entered_time):
        self.entered_time = entered_time

    def set_delivery_time(self, delivery_time):
        self.delivery_time = delivery_time
