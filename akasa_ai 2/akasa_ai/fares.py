import random

# Base minimum fare
BASE_FARE = 3500

# Additional costs for seat types
ADDITIONAL_COSTS = {
    'normal': 0,
    'window': 200,
    'aisle': 300,
    'high': 500
}

# Distance data between cities (source, destination, distance in km)
city_distances = {('Agra', 'Delhi'): 240, ('Agra', 'Lucknow'): 334, ('Agra', 'Kanpur'): 277, ('Ahmedabad', 'Mumbai'): 526, ('Ahmedabad', 'Pune'): 663, ('Ahmedabad', 'Jaipur'): 660, ('Ahmedabad', 'Udaipur'): 258, ('Bengaluru', 'Pune'): 839, ('Bengaluru', 'Hyderabad'): 576, ('Bengaluru', 'Chennai'): 346, ('Bengaluru', 'Goa'): 562, ('Bhubaneswar', 'Kolkata'): 442, ('Bhubaneswar', 'Vishakhapatnam'): 444, ('Bhubaneswar', 'Patna'): 831, ('Chennai', 'Hyderabad'): 626, ('Chennai', 'Bengaluru'): 345, ('Chennai', 'Kochi'): 690, ('Chennai', 'Mumbai'): 1335, ('Chennai', 'Kolkata'): 1666, ('Delhi', 'Jaipur'): 307, ('Delhi', 'Agra'): 243, ('Delhi', 'Lucknow'): 548, ('Delhi', 'Chennai'): 2208, ('Delhi', 'Bengaluru'): 2174, ('Delhi', 'Mumbai'): 1452, ('Delhi', 'Hyderabad'): 1582, ('Goa', 'Hyderabad'): 674, ('Goa', 'Kochi'): 755, ('Goa', 'Mumbai'): 585, ('Goa', 'Pune'): 442, ('Goa', 'Thiruvananthapuram'): 1305, ('Hyderabad', 'Pune'): 562, ('Hyderabad', 'Bengaluru'): 576, ('Hyderabad', 'Chennai'): 627, ('Hyderabad', 'Goa'): 674, ('Hyderabad', 'Mumbai'): 708, ('Hyderabad', 'Delhi'): 1583, ('Hyderabad', 'Kolkata'): 1489, ('Jaipur', 'Ahmedabad'): 659, ('Jaipur', 'Udaipur'): 397, ('Jaipur', 'Delhi'): 308, ('Jaipur', 'Mumbai'): 1170, ('Jaipur', 'Pune'): 1191, ('Kanpur', 'Agra'): 301, ('Kanpur', 'Lucknow'): 115, ('Kanpur', 'Varanasi'): 328, ('Kochi', 'Chennai'): 690, ('Kochi', 'Bengaluru'): 547, ('Kochi', 'Goa'): 754, ('Kochi', 'Thiruvananthapuram'): 206, ('Kolkata', 'Varanasi'): 680, ('Kolkata', 'Patna'): 554, ('Kolkata', 'Bhubaneswar'): 442, ('Kolkata', 'Chennai'): 1668, ('Kolkata', 'Delhi'): 1563, ('Lucknow', 'Delhi'): 553, ('Lucknow', 'Agra'): 333, ('Lucknow', 'Kanpur'): 89, ('Mumbai', 'Pune'): 148, ('Mumbai', 'Ahmedabad'): 526, ('Mumbai', 'Delhi'): 1453, ('Mumbai', 'Hyderabad'): 713, ('Mumbai', 'Bengaluru'): 984, ('Mumbai', 'Kolkata'): 1886, ('Mumbai', 'Chennai'): 1338, ('Patna', 'Varanasi'): 256, ('Patna', 'Kolkata'): 578, ('Pune', 'Mumbai'): 150, ('Pune', 'Ahmedabad'): 660, ('Pune', 'Hyderabad'): 560, ('Pune', 'Bengaluru'): 842, ('Thiruvananthapuram', 'Kochi'): 206,
                   ('Thiruvananthapuram', 'Goa'): 1305, ('Udaipur', 'Ahmedabad'): 257, ('Udaipur', 'Jaipur'): 397, ('Udaipur', 'Mumbai'): 767, ('Udaipur', 'Delhi'): 688, ('Varanasi', 'Kanpur'): 328, ('Varanasi', 'Patna'): 259, ('Varanasi', 'Kolkata'): 683, ('Varanasi', 'Lucknow'): 312, ('Vishakhapatnam', 'Bhubaneswar'): 441, ('Vishakhapatnam', 'Hyderabad'): 618, ('Vishakhapatnam', 'Kolkata'): 882, ('Agra', 'Vishakhapatnam'): 2764, ('Agra', 'Ahmedabad'): 602, ('Agra', 'Goa'): 258, ('Agra', 'Hyderabad'): 3382, ('Agra', 'Pune'): 1265, ('Agra', 'Jaipur'): 1262, ('Agra', 'Chennai'): 4009, ('Agra', 'Udaipur'): 860, ('Agra', 'Patna'): 2204, ('Agra', 'Varanasi'): 2460, ('Agra', 'Bhubaneswar'): 3205, ('Agra', 'Thiruvananthapuram'): 1563, ('Agra', 'Bengaluru'): 3958, ('Agra', 'Kochi'): 1013, ('Agra', 'Kolkata'): 3646, ('Agra', 'Mumbai'): 1128, ('Vishakhapatnam', 'Agra'): 2670, ('Vishakhapatnam', 'Ahmedabad'): 3272, ('Vishakhapatnam', 'Goa'): 2928, ('Vishakhapatnam', 'Pune'): 3935, ('Vishakhapatnam', 'Jaipur'): 3932, ('Vishakhapatnam', 'Chennai'): 6679, ('Vishakhapatnam', 'Udaipur'): 3530, ('Vishakhapatnam', 'Patna'): 4874, ('Vishakhapatnam', 'Varanasi'): 5130, ('Vishakhapatnam', 'Kanpur'): 2947, ('Vishakhapatnam', 'Thiruvananthapuram'): 4233, ('Vishakhapatnam', 'Bengaluru'): 6628, ('Vishakhapatnam', 'Delhi'): 2910, ('Vishakhapatnam', 'Kochi'): 3683, ('Vishakhapatnam', 'Lucknow'): 3004, ('Vishakhapatnam', 'Mumbai'): 3798, ('Ahmedabad', 'Agra'): 1330, ('Ahmedabad', 'Vishakhapatnam'): 4094, ('Ahmedabad', 'Goa'): 1588, ('Ahmedabad', 'Hyderabad'): 4712, ('Ahmedabad', 'Chennai'): 5339, ('Ahmedabad', 'Patna'): 3534, ('Ahmedabad', 'Varanasi'): 3790, ('Ahmedabad', 'Bhubaneswar'): 4535, ('Ahmedabad', 'Kanpur'): 1607, ('Ahmedabad', 'Thiruvananthapuram'): 2893, ('Ahmedabad', 'Bengaluru'): 5288, ('Ahmedabad', 'Delhi'): 1570, ('Ahmedabad', 'Kochi'): 2343, ('Ahmedabad', 'Lucknow'): 1664, ('Ahmedabad', 'Kolkata'): 4976, ('Goa', 'Agra'): 1569, ('Goa', 'Vishakhapatnam'): 4333, ('Goa', 'Ahmedabad'): 2171, ('Goa', 'Jaipur'): 2831, ('Goa', 'Chennai'): 5578, ('Goa', 'Udaipur'): 2429, ('Goa', 'Patna'): 3773, ('Goa', 'Varanasi'): 4029, ('Goa', 'Bhubaneswar'): 4774, ('Goa', 'Kanpur'): 1846, ('Goa', 'Delhi'): 1809, ('Goa', 'Lucknow'): 1903, ('Goa', 'Kolkata'): 5215, ('Hyderabad', 'Agra'): 2243, ('Hyderabad', 'Ahmedabad'): 2845, ('Hyderabad', 'Jaipur'): 3505, ('Hyderabad', 'Udaipur'): 3103, ('Hyderabad', 'Patna'): 4447, ('Hyderabad', 'Varanasi'): 4703, ('Hyderabad', 'Bhubaneswar'): 5448, ('Hyderabad', 'Kanpur'): 2520, ('Hyderabad', 'Thiruvananthapuram'): 3806, ('Hyderabad', 'Kochi'): 3256, ('Hyderabad', 'Lucknow'): 2577, ('Pune', 'Agra'): 1990, ('Pune', 'Vishakhapatnam'): 4754, ('Pune', 'Chennai'): 5999, ('Pune', 'Udaipur'): 2850, ('Pune', 'Patna'): 4194, ('Pune', 'Varanasi'): 4450, ('Pune', 'Bhubaneswar'): 5195, ('Pune', 'Kanpur'): 2267, ('Pune', 'Thiruvananthapuram'): 3553, ('Pune', 'Delhi'): 2230, ('Pune', 'Kochi'): 3003, ('Pune', 'Lucknow'): 2324, ('Pune', 'Kolkata'): 5636, ('Jaipur', 'Agra'): 1989, ('Jaipur', 'Vishakhapatnam'): 4753, ('Jaipur', 'Goa'): 2247, ('Jaipur', 'Hyderabad'): 5371, ('Jaipur', 'Chennai'): 5998, ('Jaipur', 'Patna'): 4193, ('Jaipur', 'Varanasi'): 4449, ('Jaipur', 'Bhubaneswar'): 5194, ('Jaipur', 'Kanpur'): 2266, ('Jaipur', 'Thiruvananthapuram'): 3552, ('Jaipur', 'Bengaluru'): 5947, ('Jaipur', 'Kochi'): 3002, ('Jaipur', 'Lucknow'): 2323, ('Jaipur', 'Kolkata'): 5635, ('Chennai', 'Agra'): 2869, ('Chennai', 'Vishakhapatnam'): 5633, ('Chennai', 'Ahmedabad'): 3471, ('Chennai', 'Goa'): 3127, ('Chennai', 'Pune'): 4134, ('Chennai', 'Jaipur'): 4131, ('Chennai', 'Udaipur'): 3729, ('Chennai', 'Patna'): 5073, ('Chennai', 'Varanasi'): 5329, ('Chennai', 'Bhubaneswar'): 6074, ('Chennai', 'Kanpur'): 3146, ('Chennai', 'Thiruvananthapuram'): 4432, ('Chennai', 'Lucknow'): 3203, ('Udaipur', 'Agra'): 1587, ('Udaipur', 'Vishakhapatnam'): 4351, ('Udaipur', 'Goa'): 1845, ('Udaipur', 'Hyderabad'): 4969, ('Udaipur', 'Pune'): 2852, ('Udaipur', 'Chennai'): 5596, ('Udaipur', 'Patna'): 3791, ('Udaipur', 'Varanasi'): 4047, ('Udaipur', 'Bhubaneswar'): 4792, ('Udaipur', 'Kanpur'): 1864, ('Udaipur', 'Thiruvananthapuram'): 3150, ('Udaipur', 'Bengaluru'): 5545, ('Udaipur', 'Kochi'): 2600, ('Udaipur', 'Lucknow'): 1921, ('Udaipur', 'Kolkata'): 5233, ('Patna', 'Agra'): 1437, ('Patna', 'Vishakhapatnam'): 4201, ('Patna', 'Ahmedabad'): 2039, ('Patna', 'Goa'): 1695, ('Patna', 'Hyderabad'): 4819, ('Patna', 'Pune'): 2702, ('Patna', 'Jaipur'): 2699, ('Patna', 'Chennai'): 5446, ('Patna', 'Udaipur'): 2297, ('Patna', 'Kanpur'): 1714, ('Patna', 'Thiruvananthapuram'): 3000, ('Patna', 'Bengaluru'): 5395, ('Patna', 'Delhi'): 1677, ('Patna', 'Kochi'): 2450, ('Patna', 'Lucknow'): 1771, ('Patna', 'Mumbai'): 2565, ('Varanasi', 'Agra'): 1696, ('Varanasi', 'Vishakhapatnam'): 4460, ('Varanasi', 'Ahmedabad'): 2298, ('Varanasi', 'Goa'): 1954, ('Varanasi', 'Hyderabad'): 5078, ('Varanasi', 'Pune'): 2961, ('Varanasi', 'Jaipur'): 2958, ('Varanasi', 'Chennai'): 5705, ('Varanasi', 'Udaipur'): 2556, ('Varanasi', 'Bhubaneswar'): 4901, ('Varanasi', 'Thiruvananthapuram'): 3259, ('Varanasi', 'Bengaluru'): 5654, ('Varanasi', 'Delhi'): 1936, ('Varanasi', 'Kochi'): 2709, ('Varanasi', 'Mumbai'): 2824, ('Bhubaneswar', 'Agra'): 3114, ('Bhubaneswar', 'Ahmedabad'): 3716, ('Bhubaneswar', 'Goa'): 3372, ('Bhubaneswar', 'Hyderabad'): 6496, ('Bhubaneswar', 'Pune'): 4379, ('Bhubaneswar', 'Jaipur'): 4376, ('Bhubaneswar', 'Chennai'): 7123, ('Bhubaneswar', 'Udaipur'): 3974, ('Bhubaneswar', 'Varanasi'): 5574, ('Bhubaneswar', 'Kanpur'): 3391, ('Bhubaneswar', 'Thiruvananthapuram'): 4677, ('Bhubaneswar', 'Bengaluru'): 7072, ('Bhubaneswar', 'Delhi'): 3354, ('Bhubaneswar', 'Kochi'): 4127, ('Bhubaneswar', 'Lucknow'): 3448, ('Bhubaneswar', 'Mumbai'): 4242, ('Kanpur', 'Vishakhapatnam'): 3065, ('Kanpur', 'Ahmedabad'): 903, ('Kanpur', 'Goa'): 559, ('Kanpur', 'Hyderabad'): 3683, ('Kanpur', 'Pune'): 1566, ('Kanpur', 'Jaipur'): 1563, ('Kanpur', 'Chennai'): 4310, ('Kanpur', 'Udaipur'): 1161, ('Kanpur', 'Patna'): 2505, ('Kanpur', 'Bhubaneswar'): 3506, ('Kanpur', 'Thiruvananthapuram'): 1864, ('Kanpur', 'Bengaluru'): 4259, ('Kanpur', 'Delhi'): 541, ('Kanpur', 'Kochi'): 1314, ('Kanpur', 'Kolkata'): 3947, ('Kanpur', 'Mumbai'): 1429, ('Thiruvananthapuram', 'Agra'): 2874, ('Thiruvananthapuram', 'Vishakhapatnam'): 5638, ('Thiruvananthapuram', 'Ahmedabad'): 3476, ('Thiruvananthapuram', 'Hyderabad'): 6256, ('Thiruvananthapuram', 'Pune'): 4139, ('Thiruvananthapuram', 'Jaipur'): 4136, ('Thiruvananthapuram', 'Chennai'): 6883, ('Thiruvananthapuram', 'Udaipur'): 3734, ('Thiruvananthapuram', 'Patna'): 5078, ('Thiruvananthapuram', 'Varanasi'): 5334, ('Thiruvananthapuram', 'Bhubaneswar'): 6079, ('Thiruvananthapuram', 'Kanpur'): 3151, ('Thiruvananthapuram', 'Bengaluru'): 6832, ('Thiruvananthapuram', 'Delhi'): 3114, ('Thiruvananthapuram', 'Lucknow'): 3208, ('Thiruvananthapuram', 'Kolkata'): 6520, ('Thiruvananthapuram', 'Mumbai'): 4002, ('Bengaluru', 'Agra'): 2131, ('Bengaluru', 'Vishakhapatnam'): 4895, ('Bengaluru', 'Ahmedabad'): 2733, ('Bengaluru', 'Jaipur'): 3393, ('Bengaluru', 'Udaipur'): 2991, ('Bengaluru', 'Patna'): 4335, ('Bengaluru', 'Varanasi'): 4591, ('Bengaluru', 'Bhubaneswar'): 5336, ('Bengaluru', 'Kanpur'): 2408, ('Bengaluru', 'Thiruvananthapuram'): 3694, ('Bengaluru', 'Lucknow'): 2465, ('Bengaluru', 'Kolkata'): 5777,
                   ('Delhi', 'Vishakhapatnam'): 3007, ('Delhi', 'Ahmedabad'): 845, ('Delhi', 'Goa'): 501, ('Delhi', 'Pune'): 1508, ('Delhi', 'Patna'): 2447, ('Delhi', 'Varanasi'): 2703, ('Delhi', 'Bhubaneswar'): 3448, ('Delhi', 'Kanpur'): 520, ('Delhi', 'Thiruvananthapuram'): 1806, ('Delhi', 'Kochi'): 1256, ('Kochi', 'Agra'): 2323, ('Kochi', 'Vishakhapatnam'): 5087, ('Kochi', 'Ahmedabad'): 2925, ('Kochi', 'Hyderabad'): 5705, ('Kochi', 'Pune'): 3588, ('Kochi', 'Jaipur'): 3585, ('Kochi', 'Udaipur'): 3183, ('Kochi', 'Patna'): 4527, ('Kochi', 'Varanasi'): 4783, ('Kochi', 'Bhubaneswar'): 5528, ('Kochi', 'Kanpur'): 2600, ('Kochi', 'Delhi'): 2563, ('Kochi', 'Lucknow'): 2657, ('Kochi', 'Kolkata'): 5969, ('Kochi', 'Mumbai'): 3451, ('Lucknow', 'Vishakhapatnam'): 3097, ('Lucknow', 'Ahmedabad'): 935, ('Lucknow', 'Goa'): 591, ('Lucknow', 'Hyderabad'): 3715, ('Lucknow', 'Pune'): 1598, ('Lucknow', 'Jaipur'): 1595, ('Lucknow', 'Chennai'): 4342, ('Lucknow', 'Udaipur'): 1193, ('Lucknow', 'Patna'): 2537, ('Lucknow', 'Bhubaneswar'): 3538, ('Lucknow', 'Thiruvananthapuram'): 1896, ('Lucknow', 'Bengaluru'): 4291, ('Lucknow', 'Kochi'): 1346, ('Lucknow', 'Kolkata'): 3979, ('Lucknow', 'Mumbai'): 1461, ('Kolkata', 'Agra'): 4537, ('Kolkata', 'Ahmedabad'): 5139, ('Kolkata', 'Goa'): 4795, ('Kolkata', 'Pune'): 5802, ('Kolkata', 'Jaipur'): 5799, ('Kolkata', 'Udaipur'): 5397, ('Kolkata', 'Kanpur'): 4814, ('Kolkata', 'Thiruvananthapuram'): 6100, ('Kolkata', 'Bengaluru'): 8495, ('Kolkata', 'Kochi'): 5550, ('Kolkata', 'Lucknow'): 4871, ('Mumbai', 'Agra'): 1856, ('Mumbai', 'Vishakhapatnam'): 4620, ('Mumbai', 'Patna'): 4060, ('Mumbai', 'Varanasi'): 4316, ('Mumbai', 'Bhubaneswar'): 5061, ('Mumbai', 'Kanpur'): 2133, ('Mumbai', 'Thiruvananthapuram'): 3419, ('Mumbai', 'Kochi'): 2869, ('Mumbai', 'Lucknow'): 2190}

# List of all cities
cities = set([city for route in city_distances.keys() for city in route])

# # Function to find missing pairs of cities
# def find_missing_pairs(cities, city_distances):
#     missing_pairs = []
#     for city1 in cities:
#         for city2 in cities:
#             if city1 != city2 and (city1, city2) not in city_distances and (city2, city1) not in city_distances:
#                 print(1)
#                 missing_pairs.append((city1, city2))
#     return missing_pairs

# Function to estimate distance using an intermediate city
def estimate_distance(source, destination, city_distances):
    for intermediate_city in cities:
        if (source, intermediate_city) in city_distances and (intermediate_city, destination) in city_distances:
            return city_distances[(source, intermediate_city)] + city_distances[(intermediate_city, destination)]
    # If no intermediate city found, return a random distance
    return random.randint(100, 3000)

# Fill missing city pairs with estimated distances
# missing_pairs = find_missing_pairs(cities, city_distances)

# for source, destination in missing_pairs:
#     estimated_distance = estimate_distance(source, destination, city_distances)
#     city_distances[(source, destination)] = estimated_distance

# print(city_distances)


# Function to estimate minimum economy fare based on distance
def estimate_fare(distance):
    fare = BASE_FARE + (distance * 2)  # Adjust the multiplier if necessary
    return fare

# Function to get fare between two cities
def get_flight_fare(source, destination, seat_type='normal', meal= False):
    # Get the distance between the source and destination
    distance = city_distances.get((source, destination), None)
    
    if distance is None:
        return f"No flight available between {source} and {destination}"
    
    # Estimate the minimum economy fare
    base_fare = estimate_fare(distance)
    
    # Add additional cost based on seat type
    additional_cost = ADDITIONAL_COSTS.get(seat_type, 0)

    mealprice = 0
    if meal:
        mealprice = 200
    # Final fare
    total_fare = base_fare + additional_cost
    return total_fare, mealprice

# # Example usage: checking the distance between a pair of cities
# for source, destination in [("Delhi", "Goa"), ("Agra", "Mumbai"), ("Lucknow", "Pune")]:
#     fare = get_flight_fare(source, destination, "normal")
#     print(f"The fare from {source} to {destination} is: Rs. {fare}")


# seat_type = "window"  # Can be 'normal', 'window', 'aisle', 'high'

def classify_seat(seat_number):
    row = int(seat_number[:-1])  # Extract row number
    column = seat_number[-1]  # Extract column letter (A-F)

    # Determine seat type based on the column
    if column in ['A', 'F']:
        seat_type = 'Window'
    elif column in ['C', 'D']:
        seat_type = 'Aisle'
    else:
        seat_type = 'Normal'

    # If the row is in the first few rows, it is a high fare seat
    if row == 1:  # You can adjust this number based on airline policy
        seat_type = 'High'

    return seat_type.lower()




# # Example usage                   
# source = "Delhi"
# destination = "Mumbai"
# seat_number = '2A'

# seat_type = classify_seat(seat_number)


# fare = get_flight_fare(source, destination, seat_type, True)

# print(f"The fare from {source} to {destination} for a {seat_type} seat is: Rs. {fare}")
