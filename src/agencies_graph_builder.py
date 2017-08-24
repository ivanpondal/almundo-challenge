from score_calculator import KM_PRICE, AGENCY_A_DISCOUNT, AGENCY_B_DISCOUNT, \
    AGENCY_C_DISCOUNT, AGENCY_D_DISCOUNT

def calculate_agency_cost(distance, agency = 'default', agency_d_discount = AGENCY_D_DISCOUNT):
    cost = distance*KM_PRICE
    if agency == 'A':
        cost *= AGENCY_A_DISCOUNT
    elif agency == 'B':
        cost *= AGENCY_B_DISCOUNT if distance > 200 else 1
    elif agency == 'C':
        cost *= AGENCY_C_DISCOUNT
    elif agency == 'D':
        cost *= agency_d_discount
    return cost

def build_agencies_graph(distances, agency_d_discount = AGENCY_D_DISCOUNT):
    graph = {'I': []}
    trip_distance = distances[0] 
    graph['I'].append(('A_1_0', calculate_agency_cost(trip_distance)))
    graph['I'].append(('B_0', calculate_agency_cost(trip_distance, 'B')))
    graph['I'].append(('D_0', calculate_agency_cost(trip_distance, 'D', agency_d_discount)))
    for i in range(1, len(distances)):
        prev_trip = str(i - 1)
        next_trip = str(i)
        trip_distance = distances[i] 
        common_trip = [
            ('A_1_' + next_trip, calculate_agency_cost(trip_distance)),
            ('B_' + next_trip, calculate_agency_cost(trip_distance, 'B')),
            ('D_' + next_trip, calculate_agency_cost(trip_distance, 'D', agency_d_discount))
        ]
        graph['A_1_' + prev_trip] = [('A_2_' + next_trip,
            calculate_agency_cost(trip_distance))]
        graph['A_2_' + prev_trip] = [('A_3_' + next_trip,
            calculate_agency_cost(trip_distance, 'A'))]
        graph['A_3_' + prev_trip] = []
        graph['A_3_' + prev_trip].extend(common_trip)
        graph['B_' + prev_trip] = [('C_' + next_trip,
            calculate_agency_cost(trip_distance, 'C'))]
        graph['B_' + prev_trip].extend(common_trip)
        graph['C_' + prev_trip] = []
        graph['C_' + prev_trip].extend(common_trip)
        graph['D_' + prev_trip] = []
        graph['D_' + prev_trip].extend(common_trip)
    last_trip = str(len(distances) - 1)
    graph['A_1_' + last_trip] = []
    graph['A_2_' + last_trip] = []
    graph['A_3_' + last_trip] = []
    graph['B_' + last_trip] = []
    graph['C_' + last_trip] = []
    graph['D_' + last_trip] = []
    return graph
