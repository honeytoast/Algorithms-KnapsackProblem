# Exhaustive search knapsack solution
from itertools import chain, combinations
import sys
import time

class DebianPackage:
    __slots__ = {'_info','name','votes','size'}

    def __init__(self, string):
        self._info = string.split()
        self.name = self._info[0]
        self.votes = int(self._info[1])
        self.size = int(self._info[2])

    def __str__(self):
        return '       {}  {}  {}'.format(self.name, self.size, self.votes)
        

def powerset(l):
    return chain.from_iterable(combinations(l,r) for r in range(len(l) + 1))

def verify_and_compare(candidate, W, best_votes):
    total_size = total_votes = 0
    for package in candidate:
        total_size += package.size
        total_votes += package.votes
        if total_size > W:
            return False, 0
    # if we reach here without returning, then total_size is <= W, which
    # verifies the candidate as a possible solution.
    # then we can just compare its total votes with the best's total votes
    # to see if it should replace the best candidate so far.
    return total_votes > best_votes, total_votes

def exhaustive_knapsack(package_list, W):
    best = None
    best_votes = 0
    for candidate in powerset(package_list):
        # check to see if a candidate satisfies the requirement of
        # total size <= W and total votes > best's total votes.
        # if satisfied, then set that candidate as the new best.
        satisfied, candidate_votes = verify_and_compare(candidate, W, best_votes)
        if satisfied:
            best = candidate
            best_votes = candidate_votes
    return best

def main():
    if len(sys.argv) != 3:
        print('Error, must supply 2 arguments.\n\n' + 
              'Usage: python3 exhaustive_knapsack.py < n > < W >')
        sys.exit(1)

    n = int(sys.argv[1])
    W = int(sys.argv[2])

    filename = 'packages.txt'
    input_file = open(filename, 'r')

    # arbitrarily read the first line since it does not contain a package
    input_file.readline()

    # read up to n packages into the list
    package_list = []
    for i in range(n):
        package_list.append(DebianPackage(input_file.readline()))
    
    # find a list of packages with total size <= W, such that the total number
    # of package votes is maximized
    start = time.perf_counter()
    solution = exhaustive_knapsack(package_list, W)
    end = time.perf_counter()

    # print solution information
    print('----- n = {}  W = {}\n'.format(n, W) + 
          '   --- Exhaustive search solution ---')
    total_size = total_votes = 0
    for package in solution:
        total_size += package.size
        total_votes += package.votes
        print(package)
    print('       Total size = {}, Total votes = {}'.format(total_size,
                                                             total_votes))
    print('       Elapsed time = {:.2f} seconds'.format(end - start))

if __name__ == '__main__':
    main()
