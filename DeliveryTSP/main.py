# Andrew Stowe, Student ID: 000806380, WGU Package Delivery Routing
import csv
import datetime

from Graph import Graph, Vertex
from Package import Package
from PackageHashTable import PackageHashTable
from Truck import Truck

delivered_package_id_list = []
package_hash = PackageHashTable(10)
option = "99"
package_input = "99"
pid_list = []
graph = Graph()
vertex_list = []

# Open the distance data
with open("DistanceTable.csv", encoding='utf-8-sig') as DistanceFile:
    distance_data = csv.reader(DistanceFile)
    # set locations to the first line of the distance file
    locations = next(distance_data)
    # Iterate through the first line in the file, adding all the addresses to the list of vertexes
    # and adding those vertexes to the graph based on the index i
    # O(n)
    for i, location in enumerate(locations):
        vertex_list.append(Vertex(location))
        graph.add_vertex(vertex_list[i])

    # Iterate through the rest of the distance file tracking the row with index j and the column with index k
    # Add edges between all the vertexes using the indexes to assign them appropriately
    # O(n^2)
    for j, row in enumerate(distance_data):
        for k, distance in enumerate(row):
            if distance != '':
                graph.add_edge(vertex_list[j], vertex_list[k], float(distance))

# Open the package data
with open("PackageFile.csv", encoding='utf-8-sig') as PackageFile:
    package_data = csv.reader(PackageFile)
    # Create a package for every line in the file then store its id in a list and insert the package into the
    # hash table, then loop through the addresses and assign the appropriate destination vertex to the package
    # O(n^2)
    for line in package_data:
        pid = line[0]
        p_address = line[1]
        p_city = line[2]
        p_state = line[3]
        p_zip = line[4]
        p_deadline = line[5]
        p_weight = line[6]
        p_status = "At Hub"

        pid_list.append(pid)
        this_package = Package(pid, p_address, p_deadline, p_city, p_state, p_zip, p_weight, p_status)
        package_hash.insert(this_package)

        for vertex in vertex_list:
            if vertex.label.endswith(p_address):
                this_package.add_vertex(vertex)

# Create lists of packages for each truck
first_truck_packages = ["1", "7", "8", "9", "13", "14", "15", "16", "19", "20", "21", "29", "30", "34", "39"]
second_truck_packages = ["3", "4", "5", "6", "18", "25", "26", "28", "31", "32", "36", "37", "38", "40"]
third_truck_packages = ["2", "10", "11", "12", "17", "22", "23", "24", "27", "33", "35"]

# Create each truck
truck1 = Truck(vertex_list[0])
truck2 = Truck(vertex_list[0])
truck3 = Truck(vertex_list[0])

# Load all the packages in the lists to the trucks inventory
# O(n)
for pid in first_truck_packages:
    truck1.load(package_hash.search(pid))
for pid in second_truck_packages:
    truck2.load(package_hash.search(pid))
for pid in third_truck_packages:
    truck3.load(package_hash.search(pid))

# Start the deliveries for the first two trucks
truck1.start_route(datetime.timedelta(hours=8), graph)
truck2.start_route(datetime.timedelta(hours=9, minutes=5), graph)

delayed = datetime.timedelta(hours=10, minutes=20)

# Return the trucks to the main hub after their deliveries
truck1.return_to_hub(vertex_list[0], graph)
truck2.return_to_hub(vertex_list[0], graph)

# Calculate how long each of the first two trucks were out
truck1_time = datetime.timedelta(hours=truck1.miles / truck1.speed)
truck2_time = datetime.timedelta(hours=truck2.miles / truck2.speed)

# Add the length of each of the first two trucks trips to their respective start times
truck1_finish = truck1.start_time + truck1_time
truck2_finish = truck2.start_time + truck2_time

# Find the earliest return of the first two trucks
truck3_start = min(truck1_finish, truck2_finish)

# If both trucks return before the misaddressed package is corrected delay the start time of the
# third truck till the correction happens
if truck3_start < delayed:
    truck3_start = delayed

# Start the deliveries for the third truck, then return it to the hub when it is done
truck3.start_route(truck3_start, graph)
truck3.return_to_hub(vertex_list[0], graph)

# Calculate the total mileage of all three trucks
total_mileage = truck1.miles + truck2.miles + truck3.miles

print("Total mileage: ")
print(total_mileage)

# Display menu until user quits
while option != "0":
    print("Please select one of the following options by entering the corresponding number:")
    print("1: Check all package status")
    print("2: Check specific package status")
    print("0: Quit")
    option = input()
    # If the user selects 1 collect a time from them then display all the package information based on that time
    if option == "1":
        print("Please input a time in the format HH:MM")
        try:
            time_input = input()
            (hour, minute) = time_input.split(":")
            time = datetime.timedelta(hours=int(hour), minutes=int(minute), seconds=0)

            for pid in pid_list:
                package = package_hash.search(pid)
                package.set_entered_time(time)
                package.print_package()
        except ValueError:
            print("Invalid time entry")

    # If the user selects option 2 collect a package id and if it is valid collect a time then display information
    elif option == "2":
        print("Please input a package ID")
        id_input = input()
        selected_package = package_hash.search(id_input)
        if selected_package is None:
            print("Invalid package ID")
        else:
            print("Please input a time in the format HH:MM")
            try:
                time_input = input()
                (hour, minute) = time_input.split(":")
                time = datetime.timedelta(hours=int(hour), minutes=int(minute), seconds=0)

                selected_package.set_entered_time(time)
                selected_package.print_package()
            except ValueError:
                print("Invalid time entry")

    # If the user selects option 0 quit the program
    elif option == "0":
        print("Goodbye!")
        exit()

    # If the user types something else tell them it is invalid
    else:
        print("Invalid input")
