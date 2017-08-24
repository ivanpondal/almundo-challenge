import sys
from math import floor, ceil
from dijkstra import dijkstra
from agencies_graph_builder import build_agencies_graph
from score_calculator import calculate_cost, KM_PRICE, AGENCY_D_DISCOUNT, AGENCY_D_KM_DISCOUNT

def minimum_trip(trips):
    minimum_cost = float("inf")
    minimum_agency = 'default'
    for trip in trips:
        if trips[trip] < minimum_cost:
            minimum_cost = trips[trip]
            minimum_agency = trip
    return minimum_agency

def to_int(float_num):
    return int(ceil(float_num))

def solve_knapsack_problem(d_trips, max_distance):
    max_weight = to_int(max_distance)
    max_values = [[0]*(max_weight + 1) for i in range(len(d_trips) + 1)]
    max_d_trips = [[[]]*(max_weight + 1) for i in range(len(d_trips) + 1)]
    for i in range(1, len(d_trips) + 1):
        k = i - 1
        for j in range(max_weight + 1):
            d_trip_weight = to_int(d_trips[k][2])
            max_values[i][j] = max_values[i - 1][j]
            max_d_trips[i][j] = max_d_trips[i - 1][j]
            if d_trip_weight <= j:
                value = max_values[i - 1][j - d_trip_weight] + \
                    (d_trips[k][2]*KM_PRICE - d_trips[k][3])
                if value > max_values[i - 1][j]:
                    max_values[i][j] = value
                    max_d_trips[i][j] = [d_trips[k]]
                    max_d_trips[i][j].extend(max_d_trips[i - 1][j - d_trip_weight])
    return max_d_trips[len(d_trips)][max_weight]

def apply_agency_d_optimization(agencies, distances):
    d_trips = []
    d_trip_init = 0
    d_trip_dist = 0
    d_trip_count = 0
    total_d_distance = 0
    for i in range(len(agencies)):
        if agencies[i] == 'D':
            if d_trip_count == 0:
                d_trip_init = i
            d_trip_dist += distances[i]
            d_trip_count += 1
            total_d_distance += distances[i]
        else:
            if d_trip_count > 0:
                d_trip_distances = distances[d_trip_init:(d_trip_init + d_trip_count)]
                optimized_trip = calculate_minimum_cost_agencies(d_trip_distances, float("inf"))
                d_trip_cost = calculate_cost(optimized_trip, d_trip_distances)
                d_trips.append((d_trip_init, d_trip_count, d_trip_dist, d_trip_cost, optimized_trip))
                d_trip_dist = 0
                d_trip_count = 0
    d_trips = sorted(d_trips, key = lambda d: d[2])
    d_remainder = total_d_distance - floor(total_d_distance / AGENCY_D_KM_DISCOUNT) * AGENCY_D_KM_DISCOUNT
    optimized_d_trips = solve_knapsack_problem(d_trips, d_remainder)
    for optimized_d_trip in optimized_d_trips:
        agencies[optimized_d_trip[0]:(optimized_d_trip[0] + optimized_d_trip[1])] = optimized_d_trip[4] 
    return agencies

def calculate_minimum_cost_agencies(distances, agency_d_discount = AGENCY_D_DISCOUNT):
    agencies_graph = build_agencies_graph(distances, agency_d_discount)
    minimum_cost_path = dijkstra('I', agencies_graph)
    last_trip = str(len(distances) - 1)
    last_trips = {
            'A_3_' + last_trip: minimum_cost_path['A_3_' + last_trip][0],
            'B_' + last_trip: minimum_cost_path['B_' + last_trip][0],
            'C_' + last_trip: minimum_cost_path['C_' + last_trip][0],
            'D_' + last_trip: minimum_cost_path['D_' + last_trip][0]
        }
    agency = minimum_trip(last_trips)
    agencies = [agency[0]]
    while minimum_cost_path[agency][1] != agency:
        agencies.append(minimum_cost_path[agency][1][0])
        agency = minimum_cost_path[agency][1]
    del agencies[len(agencies) - 1]
    agencies.reverse()
    return agencies

def calculate_agency_tour(tour, distances):
    agencies = calculate_minimum_cost_agencies(distances)
    agencies = apply_agency_d_optimization(agencies, distances)

    # return final agency tour
    agency_tour = []
    for i in range(len(tour) - 1):
        agency_tour.append((tour[i], agencies[i], tour[i + 1]))
    return agency_tour

def print_solution(agency_tour):
    for flight in agency_tour:
        print(str(flight[0]) + "," + str(flight[1]) + "," + str(flight[2]))

def main():
    tour_file_path = sys.argv[1]
    distances_file_path = sys.argv[2]

    tour = []
    with open(tour_file_path, 'r') as tour_file:
        for line in tour_file:
            tour.append(int(line))

    distances = []
    with open(distances_file_path, 'r') as distances_tour_file:
        for line in distances_tour_file:
            distances.append(float(line))

    print_solution(calculate_agency_tour(tour, distances))

if __name__ == "__main__":
    main()
