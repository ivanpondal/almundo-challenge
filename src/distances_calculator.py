import sys
import math

def euc_distance(d1, d2):
    return math.sqrt((d1[0] - d2[0])**2 + (d1[1] - d2[1])**2)

def main():
    tour_file_path = sys.argv[1]
    instance_file_path = sys.argv[2]

    tour = []
    with open(tour_file_path, 'r') as tour_file:
        for line in tour_file:
            tour.append(int(line))

    cities = {}
    with open(instance_file_path, 'r') as instance_file:
        for line in instance_file:
            splitted_line = line.split(',')
            cities[int(splitted_line[0])] = (float(splitted_line[1]), float(splitted_line[2]))

    for i in range(len(tour) - 1):
        print euc_distance(cities[tour[i]], cities[tour[i + 1]])

if __name__ == "__main__":
    main()
