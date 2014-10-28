# A dynamic programming solution to the knapsack problem.
import sys
import time

class DebianPackage:
    """A class that represents a Debian Package item for the knapsack
    algorithm. The value and weight attribute respectively reperesents
    the vote count and size of the Debian package."""

    __slots__ = {'_info', 'name', 'value', 'weight' }
    
    def __init__(self, string):
        self._info = string.split()
        self.name = self._info[0]
        self.value = int(self._info[1])
        self.weight = int(self._info[2])

    def __str__(self):
        return '    {}  votes = {}  size = {}'.format(self.name, self.value, 
                                                      self.weight)

def knapsack(items, w):
    n = len(items)
    table = [[[] for j in range(w+1)] for i in range(2)]
    for i in range(1,n+1):
        row = (i - 1) % 2
        if row == 0:
            prev_row = 1
        else:
            prev_row = 0
        for j in range(1, w+1):
            without_item = table[prev_row][j]
            spare_weight = j - items[i-1].weight
            if spare_weight >= 0:
                with_item = table[prev_row][spare_weight] + [items[i-1]]
                if total_value(with_item) > total_value(without_item):
                    table[row][j] = with_item
                else:
                    table[row][j] = without_item
            else:
                table[row][j] = without_item
    return table[1][w]

def total_value(items):
    total = 0
    for item in items:
        total += item.value
    return total

def main():
    if len(sys.argv) != 3:
        print('Error, must supply 2 arguments.\n\n' + 
              'Usage: python3 dynamic_knapsack.py < n > < W >')
        sys.exit(1)

    n = int(sys.argv[1])
    w = int(sys.argv[2])

    filename = 'packages.txt'
    input_file = open(filename, 'r')

    # arbitrarily read the first line since it does not contain a package
    input_file.readline()

    # read up to n packages into the list
    package_list = []
    for i in range(n):
        package_list.append(DebianPackage(input_file.readline()))
    print('Loaded {} packages from "packages.txt"'.format(n))

    # find a list of packages with total size <= W, such that the total number
    # of package votes is maximized
    print('solving for n = {}, W = {}'.format(n,w))
    start = time.perf_counter()
    solution = knapsack(package_list, w)
    end = time.perf_counter()

    # print solution information
    total_size = total_votes = 0
    for package in solution:
        total_size += package.weight
        total_votes += package.value
    print('Total votes = {}'.format(total_votes))
    print('Total size = {}'.format(total_size))
    print('Elapsed time = {} seconds'.format(end - start))
    print('First 20 packages:')
    length = len(solution)
    for i in range(min(length,20)):
        print(solution[i])

if __name__ == '__main__':
    main()
