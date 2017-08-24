import sys

KM_PRICE = 0.01
AGENCY_A_DISCOUNT = 0.65
AGENCY_B_DISCOUNT = 0.85
AGENCY_C_DISCOUNT = 0.80
AGENCY_D_DISCOUNT = 0.85

AGENCY_B_KM_DISCOUNT = 200
AGENCY_D_KM_DISCOUNT = 10000

agency_tour_file_path = sys.argv[1]
distances_file_path = sys.argv[2]

def calculate_cost(agencies, distances):
    agency_a_accum = 0
    agency_d_accum = 0
    cost = 0
    for i in range(len(agencies)):
        if agencies[i] == 'A':
            if agency_a_accum == 2:
                agency_a_accum = 0
                cost += distances[i]*KM_PRICE*AGENCY_A_DISCOUNT
            else:
                cost += distances[i]*KM_PRICE
                agency_a_accum += 1
        elif agencies[i] == 'B':
            if distances[i] > AGENCY_B_KM_DISCOUNT:
                cost += distances[i]*KM_PRICE*AGENCY_B_DISCOUNT
            else:
                cost += distances[i]*KM_PRICE
            agency_a_accum = 0
        elif agencies[i] == 'C':
            if i > 0 and agencies[i - 1] == 'B':
                cost += distances[i]*KM_PRICE*AGENCY_C_DISCOUNT
            else:
                cost += distances[i]*KM_PRICE
            agency_a_accum = 0
        elif agencies[i] == 'D':
            agency_d_accum += distances[i]
            cost += distances[i]*KM_PRICE
            if agency_d_accum >= AGENCY_D_KM_DISCOUNT:
                cost -= 15
                agency_d_accum -= AGENCY_D_KM_DISCOUNT
            agency_a_accum = 0
    return cost

def main():
    agencies = []
    with open(agency_tour_file_path, 'r') as agency_tour_file:
        for line in agency_tour_file:
            splitted_line = line.split(',')
            agencies.append(splitted_line[1])

    distances = []
    with open(distances_file_path, 'r') as distances_tour_file:
        for line in distances_tour_file:
            distances.append(float(line))

    print calculate_cost(agencies, distances)

if __name__ == "__main__":
    main()
