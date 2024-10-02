user_information = """

{
  "name": "Harsha Bellala",
  "date_of_birth": "2004-02-04T00:00:00",
  "home_city": "Hyderabad",
  "home_airport_code": "HYD",
  "most_preferred_class": "Economy",
  "visited_cities": [
    {"city_code": "HYD", "city_name": "Hyderabad", "visit_count": 10},
    {"city_code": "BLR", "city_name": "Bengaluru", "visit_count": 5},
    {"city_code": "DEL", "city_name": "Delhi", "visit_count": 3}
  ],
  "preferred_seats": [
    {"seat": "4F", "booking_count": 4},
    {"seat": "5F", "booking_count": 2},
    {"seat": "3E", "booking_count": 1}
  ],
  "preferred_departure_time": {
    "start": "10:00 AM",
    "end": "7:00 PM"
  },
  "food_preferences": [
    {"item": "Coffee + Sandwich", "selection_count": 3},
    {"item": "Tea + Snack Bag", "selection_count": 2}
  ],
  "flight_durations": {
    "morning": {"count": 4, "time_range": "5:00 AM - 11:59 AM"},
    "noon": {"count": 3, "time_range": "12:00 PM - 5:59 PM"},
    "evening": {"count": 5, "time_range": "6:00 PM - 9:59 PM"},
    "midnight": {"count": 2, "time_range": "10:00 PM - 4:59 AM"}
  },
  "joined_akasa": "2024-05",
  "email": "harshasrikasyap807@gmail.com",
  "phone": "+919876543210",
  "nationality" : "indian"
}


"""




f1_json = """
{
    "general" : {
        "response" : "when user input is not present and when user queries any other info. response to the user include , greeting, and if needed tell the user what you are capable of"
    
    },
  "booking": 
    {
        "data-complete": "[True if source , destination and dateofdeparture are filled from user inputs and user has confirmed the fields else False]",
        "Name": "[Name of the user for the booking]",
        "flightNumber": "[flight number if mentioned else 'not-applicable']",
        "firstName": "[first name of the user for the booking]",
        "lastName": "[last name of the user for the booking]",
        "passportNumber": "[passport number of the user if mentioned else 'not-applicable']",
        "nationality": "[populate with user information]",
        "contactEmail": "[email of the user if mentioned else 'not-applicable']",
        "contactPhone": "[phone number of the user if mentioned else 'not-applicable' or also prepopulate with user info]",
        "class": "[categorize it to business or economy else 'not-applicable']",
        "seat": "[seat preference if mentioned else 'not-applicable' or can also prepopulate with user information most preferred]",
        "source": "[source city from where the booking is for else 'not-applicable']",
        "destination": "[destination city where the booking is for else 'not-applicable']",
        "source_airport_code": "[source airport code else 'not-applicable']",
        "destination_airport_code": "[destination airport code else 'not-applicable']",
        "meal": "[meal preference if mentioned else 'not-applicable']",
        "response": "[text to user to ask additional missing info and confirm prepopulated fields, if destination source cities are not in airport cities tell user there is not flight]",
        "dateofdeparture": "[DD/MM/YYYY user can provide date in any format]",
        "timeofdeparture": "[HH/MM user can provide date in any format]",
        "createdAt": "[timestamp when the booking was created]",
        "updatedAt": "[timestamp when the booking was last updated]"
    }
  ,
  "cancelling": 
    {
        "data-complete": "[True if all fields are filled from user input else False]",
        "Name": "[Name of the user for the cancellation]",
        "pnr_number": "[flight number if mentioned else 'not-applicable']",
        "reason": "[reason for cancellation if mentioned else 'not-applicable']",
        "flight_number": "[flight number if mentioned else 'not-applicable']"
    }
  ,
  "flight_info": 
    {
        "data-complete": "[True if all fields are filled from user input else False]",
        "Name": "[Name of the user requesting flight info]",
        "flight_number": "[flight number if mentioned else 'not-applicable']",
        "date_of_travel": "[date of travel if mentioned else 'not-applicable']"
    }
  ,
  "change_flight": 
    {
        "data-complete": "[True if all fields are filled from user input else False]",
        "Name": "[Name of the user for the change request]",
        "flight_number": "[current flight number if mentioned else 'not-applicable']",
        "new_date": "[new date of travel if mentioned else 'not-applicable']",
        "new_time": "[new time of travel if mentioned else 'not-applicable']"
    }
  ,
  "change_preferences": 
    {
        "data-complete": "[True if all fields are filled from user input else False]",
        "Name": "[Name of the user changing preferences]",
        "flight_number": "[flight number if mentioned else 'not-applicable']",
        "class": "[new class preference if mentioned else 'not-applicable']",
        "seat": "[new seat preference if mentioned else 'not-applicable']",
        "meal": "[meal preference if mentioned else 'not-applicable']"
    }
  
  

}


"""

airport_data = """
Delhi – Indira Gandhi International Airport (DEL)
Mumbai – Chhatrapati Shivaji Maharaj International Airport (BOM)
Bangalore – Kempegowda International Airport (BLR)
Hyderabad – Rajiv Gandhi International Airport (HYD)
Chennai – Chennai International Airport (MAA)
Kolkata – Netaji Subhas Chandra Bose International Airport (CCU)
Ahmedabad – Sardar Vallabhbhai Patel International Airport (AMD)
Pune – Pune International Airport (PNQ)
Jaipur – Jaipur International Airport (JAI)
Cochin – Cochin International Airport (COK)
Goa – Dabolim Airport (GOI)
Lucknow – Chaudhary Charan Singh International Airport (LKO)
Trivandrum – Trivandrum International Airport (TRV)
Nagpur – Dr. Babasaheb Ambedkar International Airport (NAG)
Patna – Jay Prakash Narayan International Airport (PAT)
Indore – Devi Ahilya Bai Holkar Airport (IDR)
Amritsar – Sri Guru Ram Dass Jee International Airport (ATQ)
Coimbatore – Coimbatore International Airport (CJB)
Bhubaneswar – Biju Patnaik International Airport (BBI)
Guwahati – Lokpriya Gopinath Bordoloi International Airport (GAU)
Aurangabad – Aurangabad Airport (IXU)
Bagdogra – Bagdogra International Airport (IXB)
Bhopal – Raja Bhoj International Airport (BHO)
Aizawl – Lengpui Airport (AJL)
Imphal – Imphal International Airport (IMF)
Agartala – Maharaja Bir Bikram Airport (IXA)
Tirupati – Tirupati Airport (TIR)
Varanasi – Lal Bahadur Shastri International Airport (VNS)
Rajkot – Rajkot Airport (RAJ)
Visakhapatnam – Visakhapatnam International Airport (VTZ)
Leh – Kushok Bakula Rimpochee Airport (IXL)
Jodhpur – Jodhpur Airport (JDH)
Vijayawada – Vijayawada International Airport (VGA)
Raipur – Swami Vivekananda Airport (RPR)
Udaipur – Maharana Pratap Airport (UDR)
Jammu – Jammu Airport (IXJ)
Srinagar – Sheikh ul-Alam International Airport (SXR)
Gaya – Gaya Airport (GAY)
Khajuraho – Khajuraho Airport (HJR)
Surat – Surat International Airport (STV)
Kannur – Kannur International Airport (CNN)
Hubli – Hubli Airport (HBX)
Dibrugarh – Dibrugarh Airport (DIB)
Mangalore – Mangalore International Airport (IXE)
Dimapur – Dimapur Airport (DMU)
Vadodara – Vadodara Airport (BDQ)
Madurai – Madurai International Airport (IXM)
Port Blair – Veer Savarkar International Airport (IXZ)
Silchar – Silchar Airport (IXS)
"""


def get_f1_context(current_date = "30/09/2024", current_location = "Bengaluru"):
    f1_prompt = f"""
   Classify the user's query into one of these categories: general queries (greetings, any other intents) , booking a flight, cancelling a flight, checking flight info, changing a flight, or changing flight preferences.
Prepopulate any missing fields with the user's most preferred data from their profile if available. Otherwise, use new information from the user's input.
Select only one intent from the user's query and generate the corresponding JSON. Include only fields related to the selected intent.
The response JSON must contain only one 'intent' key with its corresponding value.

    Current date (DD/MM/YYYY): {current_date}

    Current user location (City): {current_location}

    Available cities and airport codes: {airport_data}
"""




    flows = { 'f1' : {'prompt' : f1_prompt , 'json' : f1_json}}

    f1_context = f"""
    You are Akasa Air's AI assistant, responsible for managing user flight-related intents. Follow the instructions below:

    {flows['f1']['prompt']}

    JSON format is
    {flows['f1']['json']}

    Important note : Respond in json and json only dont generate any other text.


    User Information Provided below use it where necessary:
    {user_information}



    """


    return f1_context

    # contexts = {'f1_context' : f1_context}

booking_json = """
{
    "response": "[text to user to ask additional missing info and confirm prepopulated fields at every step]",
    
    "Name": "[Name of the user for the booking]",
    "firstName": "[first name of the user for the booking]",
    "lastName": "[last name of the user for the booking]",
    "passportNumber": "[passport number of the user if mentioned else 'not-applicable']",
    "nationality": "[populate with user information]",
    "contactEmail": "[email of the user if mentioned else 'not-applicable']",
    "contactPhone": "[phone number of the user if mentioned else 'not-applicable' or also prepopulate with user info]",

    "confirm-s-d-dep": "[True if source , destination and dateofdeparture are filled from user inputs and user has confirmed the fields else False]",
    "source": "[source city from where the booking is for else 'not-applicable']",
    "destination": "[destination city where the booking is for else 'not-applicable']",
    "source_airport_code": "[source airport code else 'not-applicable']",
    "destination_airport_code": "[destination airport code else 'not-applicable']",
    "dateofdeparture": "[DD/MM/YYYY user can provide date in any format]",

    "need-flights-data" : "[True if you need flights data to fill in flightNumber , flight_departure_time and other data in next prompt else False]"

    "confirm-fn-fdep": "[True if flightNumber , flight_departure_time are choosen,  filled from user inputs and user has confirmed the fields else False]",
    
    "timeofdeparture": "[HH/MM user can provide time he prefers in any format]",
    
    "flightNumber": "[Assign the flight number assigned upon confirmation]",
    "flight_departure_time": "[Assign based on the confirmed departure time in HH:MM format.",
    "flight_arrival_time": "Assign based on the confirmed arrival time in HH:MM format",

    "need-seat-data" : "[True if you need seat data of a flightNumber on flight_departure_time next prompt else False]"

    "confirm-cls-s": "[True if seat , class are choosen, and optionally fillin meal preferences  confirmed by user input else False]",
    "class": "[categorize it to business  on seat 1A to 1F confirmed or economy else 'not-applicable']",
    "seat": "[seat preference if mentioned else 'not-applicable' or can also prepopulate with user information most preferred]",
    "meal": "[meal preference if mentioned else 'not-applicable']",

    "readyforpayment" : "[True if all fields are filled in to request the payment info on selected preferences from user in next prompt ]",

    "createdAt": "[timestamp when the booking was created]",
    "updatedAt": "[timestamp when the booking was last updated]"

   

    "request_confirmation" : "[set it True to get confirmation request for selected booking from admin ]"

    "cancel" : "True if user wants to cancel current booking at any step else False"

}


"""
def get_booking_context(current_date = "30/09/2024", current_location = "Delhi", prefilled_json = "" ):
    booking_prompt = f"""
    
    You are Akasa Air's AI assistant, responsible for handling user flight-related intents. Follow the instructions below:

    1. Populate user info for booking a flight by updating the New JSON format with data from the prefilled JSON provided to you. First, merge the prefilled data, then request missing fields from the user one step at a time.

    2. Request source, destination, and departure date if not provided, then confirm these details with the user. Ensure these cities are in the available cities list. After confirmation, set "need-flights-data" to True.

    3. Once the dates are confirmed, ask the user which flight they want to choose in a proper format based on the data provided by the admin. Then, set "need-seat-data" to True.

    4. Recommend seat selection based on the user's previous journey preferences. Ask if they want to change their seat.

    5. Suggest meals based on the user's preferences from the provided info. Allow the user to change the selection or accept the suggested meal. Once confirmed, set "readyforpayment" to True.

    6. Confirm pricing with the user and set "request_confirmation" to True. The admin will then send a payment request based on the selected details.

    7. If the user chooses to cancel the booking at any moment, set "cancel" in the JSON to True.

    Important:
    Every response you generate should strictly follow the New JSON format.
    All queries to the user should be placed in the "response" field of the JSON.
    
    Current date (DD/MM/YYYY): {current_date}

    Current user location (City): {current_location}

    Available cities and airport codes: 
    {airport_data}

    
"""




    flows = { 'booking' : {'prompt' : booking_prompt , 'json' : booking_json}}

    booking_context = f"""
    You are Akasa Air's AI assistant, responsible for managing user flight-related intents. Follow the instructions below:

    {flows['booking']['prompt']}


    Prefilled json below

    {prefilled_json}

    New JSON format 2 is to be populated and sent
    {flows['booking']['json']}

    Important note : Respond in json and json only dont generate any other text.


    User Information Provided below use it where necessary:
    {user_information}



    """
    return booking_context

json_res = """
{
            "user": "ai",
            "msg": {
                "data-complete": false,
                "Name": "Harsha Bellala",
                "flightNumber": "not-applicable",
                "firstName": "Harsha",
                "lastName": "Bellala",
                "passportNumber": "not-applicable",
                "nationality": "indian",
                "contactEmail": "harshasrikasyap807@gmail.com",
                "contactPhone": "+919876543210",
                "class": "Economy",
                "seat": "4F",
                "source": "not-applicable",
                "destination": "not-applicable",
                "source_airport_code": "not-applicable",
                "destination_airport_code": "not-applicable",
                "meal": "Coffee + Sandwich",
                "response": "Sure! Where would you like to fly? Please tell me the departure and arrival cities.",
                "dateofdeparture": "not-applicable",
                "timeofdeparture": "not-applicable",
                "createdAt": "not-applicable",
                "updatedAt": "not-applicable"
            }
        }
"""

print(get_booking_context('no date',"Delhi",json_res))