# Hash table modified from WGU course material to suit the needs of this project

from Package import Package


class PackageHashTable:
    # Creates a hash table with initial_capacity buckets
    # O(n)
    def __init__(self, initial_capacity: int):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a package into the hash table by taking in the package then using the hash function on
    # that packages id to find the bucket then appending that package to the end of that bucket
    # O(n)
    def insert(self, package: Package):
        bucket = hash(package.pid) % len(self.table)
        bucket_list = self.table[bucket]
        for pid in bucket_list:
            if pid[0] == package.pid:
                pid[1] = package
                return True

        key = [package.pid, package]
        bucket_list.append(key)
        return True

    # Search the hash table for the package with the entered id then return that package if found
    # O(n)
    def search(self, pid):
        bucket = hash(pid) % len(self.table)
        bucket_list = self.table[bucket]

        for pv in bucket_list:
            if pv[0] == pid:
                return pv[1]
        return None

    # Search the hash table for the package with the entered id then remove it from the hash table and
    # return removed item if found
    def remove(self, pid):
        bucket = pid % len(self.table)
        bucket_list = self.table[bucket]

        for pv in bucket_list:
            if pv[0] == pid:
                removed_package = pv[1]
                bucket_list.remove([pv[0], pv[1]])
                return removed_package

