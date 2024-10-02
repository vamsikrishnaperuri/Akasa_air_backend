import json
import re
from datetime import datetime

def extract_json_from_string(input_string):
    # Find the first '{' and the last '}'
    first_brace = input_string.find('{')
    last_brace = input_string.rfind('}')

    # Check if both braces were found
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        # Extract the substring from the first '{' to the last '}'
        return input_string[first_brace:last_brace + 1]
    else:
        return None


def get_flights(collection_flight_dates, source: str, destination: str, departure_date: str):
    try:
        departure_date_cleaned = departure_date.strip()
        departure_date_obj = datetime.strptime(departure_date_cleaned, '%d/%m/%Y')
        day_of_week_str = departure_date_obj.strftime('%A')

        # Log the input parameters and computed values
        print(f"Requesting flights with source: {source}, destination: {destination}, departure_date: {departure_date_cleaned}")
        print(f"Computed day_of_week: {day_of_week_str}")

        # Prepare the query
        query = {
            "origin": source,
            "destination": destination,
            "validFrom": {"$gte": departure_date_obj.strftime('%d/%m/%Y')},
            # "validTo": {"$gte": departure_date_obj.strftime('%d/%m/%Y')}
        }

        print(f"Query criteria: {query}")

        flights = list(collection_flight_dates.find(query))
        print("Fetched flights:", flights)

        valid_flights = [
            flight for flight in flights if day_of_week_str in flight['dayOfWeek'].split(',')
        ]
        print("Valid flights after filtering:", valid_flights)

        sorted_flights = sorted(valid_flights, key=lambda x: datetime.strptime(x['scheduledDepartureTime'], '%H:%M:%S'))

        result = [{
            "flightNumber": flight['flightNumber'],
            "airline": flight['airline'],
            "departureTime": flight['scheduledDepartureTime'],
            "arrivalTime": flight['scheduledArrivalTime'],
            "origin": flight['origin'],
            "destination": flight['destination'],
        } for flight in sorted_flights]

        return {"flights": result, 'day_of_week': day_of_week_str}

    except ValueError as ve:
        return {"error": str(ve)}
    except Exception as e:
        return {"error": str(e)}


def getmeal():
    meal = """
    Mixed Nuts
A healthy mix of almonds, cashews, walnuts, and pistachios.

Bhel Puri
A popular Indian street food made with puffed rice, sev, peanuts, and tangy tamarind chutney.

Roasted Cashews (Rosa Cashews)
Lightly salted and roasted cashews for a crunchy snack.

Chocolate Pistachio
A sweet treat combining pistachios with a rich chocolate coating.

Vada Pav
A Mumbai-style spicy potato fritter served in a soft bun, accompanied by garlic chutney.

Makhana (Fox Nuts)
Roasted fox nuts flavored with spices, offering a light and crunchy snack.

Chicken Club Sandwich
A sandwich made with grilled chicken, lettuce, tomato, and mayonnaise, in toasted bread.

Chicken Malabar Pocket
A flaky pastry filled with spicy Malabar-style chicken curry.

Veg cup noodles 
A fragrant noodles with vegetables and subtle spices.

Fruit Salad (Fruit Fit)
A fresh, healthy mix of seasonal fruits for a light snack.
""" 
    return meal


import random

def generate_airplane_seats():
    seats = {}
    free_seats = []
    
    rows = 30
    columns = ['A', 'B', 'C', 'D', 'E', 'F']
    
    # Determine how many seats are booked randomly between 10 to 30
    total_booked_seats = random.randint(10, 30)
    booked_seats = set()

    # Generate the seat IDs (e.g., 1A, 1B,...30F) and randomly book some
    for row in range(1, rows + 1):
        for column in columns:
            seat = f"{row}{column}"
            if len(booked_seats) < total_booked_seats and random.choice([True, False]):
                booked_seats.add(seat)
            else:
                free_seats.append(seat)

    # Create the seat dictionary with booked status
    for row in range(1, rows + 1):
        row_dict = {}
        for column in columns:
            seat = f"{row}{column}"
            row_dict[seat] = {'booked': seat in booked_seats}
        seats[f"Row {row}"] = row_dict
    
    # Return the seats dictionary and free seats list
    return { "freeseats": free_seats}

# Example of running the function
# airplane_seats = generate_airplane_seats()
# print(airplane_seats)
# # Example usage
# json_string = ''' ```json
# {

#   "booking": 
#     {
#       "data-complete":
#  "False",
#       "Name": "Harsha Bellala",

#       "class": "Economy",
#       "seat": "4F",
#       "source": "Bengaluru",
#       "destination": "Visakhapatnam
# ",
#       "source_airport_code": "BLR",
#       "destination_airport_code": "VTZ",
#       "meal":
#  "Coffee + Sandwich",
#       "response": "Okay, I'm finding flights from Bengaluru to Visakhapatnam on 04:02:2025.  What time would you like to depart?",
#       "
# dateofdeparture": "04:02:2025",
#       "timeofdeparture": "not-applicable"
#     }
  
# }
# ```
# '''

# # Call the function and print the result
# extracted_json = extract_json_from_string(json_string)
# print(json.loads(extracted_json))




import json
import random
import string
from datetime import datetime

# Function to generate dynamic booking reference
def generate_booking_reference():
    return "AA-BR" + ''.join(random.choices(string.digits, k=12))

# Function to generate the booking payload
def create_booking_payload(input_json, user_data_json):
    # Current datetime in ISO format
    current_datetime = datetime.now().isoformat()
    
    # Parse input and user data
    input_data = json.loads(input_json)
    user_data = json.loads(user_data_json)
    
    # Populate the booking payload
    booking_payload = {
        "bookingReference": generate_booking_reference(),
        "passengerDetails": {
            "firstName": user_data.get("name", 'na').split()[0], # Get first name from name
            "lastName": user_data.get("name", 'na').split()[-1], # Get last name from name
            "dateOfBirth": user_data.get("date_of_birth", 'na'),
            "passportNumber": user_data.get("passportNumber", 'na'),
            "nationality": user_data.get("nationality", 'na').capitalize(),
            "contactDetails": {
                "email": user_data.get("email", 'na'),
                "phone": user_data.get("phone", 'na')
            }
        },
        "flightDetails": {
            "flightNumber": input_data.get("flightNumber", 'na'),
            "airline": "Akasa Air",
            "departure": {
                "airport": input_data.get("source_airport_code", 'na'),
                "city": input_data.get("source", 'na'),
                "country": "India",
                "dateTime": f"{input_data.get('dateofdeparture', 'na')}T{input_data.get('flight_departure_time', 'na')}"
            },
            "arrival": {
                "airport": input_data.get("destination_airport_code", 'na'),
                "city": input_data.get("destination", 'na'),
                "country": "India",
                "dateTime": f"{input_data.get('dateofdeparture', 'na')}T{input_data.get('flight_arrival_time', 'na')}"
            },
            "flightClass": input_data.get("class", 'na'),
            "seatNumber": input_data.get("seat", 'na')
        },
        "bookingStatus": "Confirmed",
        "paymentDetails": {
            "amount": input_data.get("fare", 'na'),  # This is hardcoded as per your sample
            "currency": "INR",
            "paymentMethod": "Credit Card",
            "paymentStatus": "Paid",
            "paymentDate": current_datetime
        },
        "specialRequests": input_data.get("meal", 'na'),
        "loyaltyProgram": {
            "programName": "Akasa Air Miles",
            "membershipNumber": user_data.get("membershipNumber", 'na'),
            "pointsEarned": 100  # Assuming fixed points for now
        },
        "createdAt": current_datetime,
        "updatedAt": current_datetime
    }
    
    return booking_payload

# Example Input JSON and User Data JSON
# input_json = '''{
#     "response": "Your booking is confirmed. A payment request has been sent to your email address. Thank you for choosing Akasa Air!",
#     "Name": "Harsha Bellala",
#     "firstName": "Harsha",
#     "lastName": "Bellala",
#     "passportNumber": "not-applicable",
#     "nationality": "indian",
#     "contactEmail": "harshasrikasyap807@gmail.com",
#     "contactPhone": "+919876543210",
#     "confirm-s-d-dep": "True",
#     "source": "Delhi",
#     "destination": "Mumbai",
#     "source_airport_code": "DEL",
#     "destination_airport_code": "BOM",
#     "dateofdeparture": "2024-10-10",
#     "need-flights-data": "True",
#     "confirm-fn-fdep": "True",
#     "timeofdeparture": "14:30:00",
#     "flightNumber": "AA316",
#     "flight_departure_time": "14:30",
#     "flight_arrival_time": "17:30",
#     "need-seat-data": "True",
#     "confirm-cls-s": "True",
#     "class": "Economy",
#     "seat": "5A",
#     "meal": "Vegetarian meal",
#     "confirm-meal": "True",
#     "need-flight-cost": "True",
#     "readyforpayment": "True",
#     "request_confirmation": "True",
#     "cancel": "False",
#     "createdAt": "not-applicable",
#     "fare" :"6400",
#     "updatedAt": "not-applicable"
# }'''

# user_data_json = '''{
#     "name": "Harsha Bellala",
#     "date_of_birth": "1990-05-15T00:00:00",
#     "passportNumber": "A12345678",
#     "joined_akasa": "2024-05",
#     "membershipNumber": "AA12345",
#     "home_city": "Hyderabad",
#     "home_airport_code": "HYD",
#     "most_preferred_class": "Economy",
#     "email": "harshasrikasyap807@gmail.com",
#     "phone": "+919876543210",
#     "nationality": "Indian"
# }'''

# # Generate booking payload
# booking_payload = create_booking_payload(input_json, user_data_json)
# print(json.dumps(booking_payload, indent=4))


import json
def get_bookings_f(email, collection_flight_bookings):
    
    query = {}
    if email:
        query['passengerDetails.contactDetails.email'] = email
    

    bookings = list(collection_flight_bookings.find(query))

    if not bookings:
        return "No bookings for the user exisiting "

    # Convert ObjectId to string
    for booking in bookings:
        booking["_id"] = str(booking["_id"])
    
    return json.dumps(booking)